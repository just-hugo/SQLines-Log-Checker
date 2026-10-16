"""Local SQLines log checker: one server per port, with explicit shutdown.

When packaged with PyInstaller, the application uses port 8765.
When run as Python source, it uses port 8766 to avoid a packaged build.
Set SQLINES_PORT to override either default for testing.
"""

import hashlib
import ntpath
import os
import secrets
import sys
import threading
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path

from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.serving import make_server

from validator import validate
from notes_store import MAX_NOTE_LENGTH, load_notes, save_notes
from report_export import build_report


HOST = "127.0.0.1"
PACKAGED = getattr(sys, "frozen", False)
PORT = int(os.environ.get("SQLINES_PORT", "8765" if PACKAGED else "8766"))
URL = f"http://{HOST}:{PORT}/"
APP_ID = "SQLinesLogChecker-v1"

TEMPLATE_FOLDER = (
    Path(sys._MEIPASS) / "templates"
    if PACKAGED
    else Path(__file__).resolve().parent / "templates"
)

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_FOLDER),
    static_folder=os.path.join(
        sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(__file__),
        "static",
    ),
)


@app.after_request
def prevent_cached_app_pages(response):
    response.headers["Cache-Control"] = "no-store"
    return response


_shutdown_token = secrets.token_urlsafe(32)
_server = None

# Latest validation stays in memory until replaced or the server exits.
_latest_result = None
_latest_report_id = None
_latest_source = "Pasted log text"
_result_lock = threading.Lock()


@app.context_processor
def add_shutdown_token():
    return {"shutdown_token": _shutdown_token}


@app.route("/", methods=["GET", "POST"])
def index():
    global _latest_result, _latest_report_id, _latest_source

    if request.method == "POST":
        text = request.form.get("log_text", "")
        uploaded = request.files.get("log_file")
        input_issues = []
        if uploaded and uploaded.filename:
            if not uploaded.filename.lower().endswith(".sql"):
                input_issues.append("Uploaded files must have a .sql extension.")
            else:
                raw = uploaded.read()
                try:
                    # SQLines output may include a UTF-8 BOM or originate from
                    # a Windows ANSI environment (cp1252).
                    text = raw.decode("utf-8-sig")
                except UnicodeDecodeError:
                    try:
                        text = raw.decode("cp1252")
                    except UnicodeDecodeError:
                        input_issues.append("Could not decode the uploaded SQL log.")

        result = validate(text, input_issues=input_issues)
        report_id = hashlib.sha256(text.encode("utf-8")).hexdigest()
        source = (
            ntpath.basename(uploaded.filename)
            if uploaded and uploaded.filename
            else "Pasted log text"
        )
        with _result_lock:
            _latest_result = result
            _latest_report_id = report_id
            _latest_source = source

        # POST -> redirect -> GET: refresh and later launches display the
        # latest report while the application process remains running.
        return redirect(url_for("index"), code=303)

    with _result_lock:
        result = _latest_result
        report_id = _latest_report_id
        annotations = load_notes(report_id) if result is not None else {}
    return render_template(
        "index.html", result=result, report_id=report_id, annotations=annotations
    )


@app.post("/_investigation")
def save_investigation():
    if request.remote_addr != HOST or not secrets.compare_digest(
        request.headers.get("X-SQLines-Shutdown-Token", ""), _shutdown_token
    ):
        abort(403)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Invalid investigation data"), 400
    report_id, index = payload.get("report_id"), payload.get("index")
    note, resolved = payload.get("note"), payload.get("resolved")
    if (
        not isinstance(report_id, str)
        or type(index) is not int
        or not isinstance(note, str)
        or type(resolved) is not bool
        or len(note) > MAX_NOTE_LENGTH
    ):
        return jsonify(
            error=f"Invalid note (maximum {MAX_NOTE_LENGTH} characters)"
        ), 400
    with _result_lock:
        if (
            _latest_result is None
            or report_id != _latest_report_id
            or not (0 <= index < len(_latest_result["unexpected"]))
        ):
            return jsonify(error="The analyzed log has changed. Reload the page."), 409
        notes = load_notes(report_id)
        key = str(index)
        if not note and not resolved:
            notes.pop(key, None)
        else:
            notes[key] = {"note": note, "resolved": resolved}
        save_notes(report_id, notes)
    return jsonify(saved=True)


@app.get("/_report")
def download_report():
    if request.remote_addr != HOST:
        abort(403)
    with _result_lock:
        if _latest_result is None:
            abort(404)
        report = build_report(
            _latest_result, load_notes(_latest_report_id), _latest_source
        )
    response = Response(report, content_type="text/plain; charset=utf-8")
    if request.args.get("download") == "1":
        response.headers["Content-Disposition"] = (
            'attachment; filename="SQLines_Validation_Report.txt"'
        )
    return response


@app.get("/_health")
def health():
    response = jsonify({"app": APP_ID})
    response.headers["X-SQLines-App"] = APP_ID
    response.headers["Cache-Control"] = "no-store"
    return response


@app.post("/_shutdown")
def shutdown():
    supplied = request.headers.get("X-SQLines-Shutdown-Token", "")
    if not secrets.compare_digest(supplied, _shutdown_token):
        abort(403)
    if request.remote_addr != HOST:
        abort(403)
    if _server is None:
        abort(503)
    # Shutdown must happen on a different thread from the active request.
    threading.Thread(target=_server.shutdown, daemon=True).start()
    return jsonify({"stopped": True})


def running_checker():
    """Only reuse a port if a responding server identifies as this app."""
    try:
        # Bypass system proxies: this request must remain on loopback even
        # on a corporate Windows computer with a configured HTTP proxy.
        direct = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with direct.open(f"{URL}_health", timeout=0.5) as response:
            return response.headers.get("X-SQLines-App") == APP_ID
    except (OSError, urllib.error.URLError, ValueError):
        return False


def show_startup_error(message):
    if sys.platform == "win32" and PACKAGED:
        # The Windows executable is windowed, so errors need a visible dialog.
        import ctypes

        ctypes.windll.user32.MessageBoxW(None, message, "SQLines Log Checker", 0x10)
    else:
        print(message, file=sys.stderr)


def main():
    global _server

    if running_checker():
        if os.environ.get("SQLINES_NO_BROWSER") != "1":
            webbrowser.open(URL)
        return

    try:
        # Binding this port is the single-instance guard. Only one process
        # can own the listening socket, even when two instances start at once.
        _server = make_server(HOST, PORT, app, threaded=True)
    except (OSError, SystemExit):
        # Another checker might have started between our check and bind.
        if running_checker():
            if os.environ.get("SQLINES_NO_BROWSER") != "1":
                webbrowser.open(URL)
            return
        show_startup_error(
            f"Cannot start SQLines Log Checker on {URL}\n"
            "The port is already in use by another program.\n"
            "Close that program (or an older checker build) in Task Manager,\n"
            "or set SQLINES_PORT to another port."
        )
        return

    # Socket is listening now, so there's no startup race with the browser.
    if os.environ.get("SQLINES_NO_BROWSER") != "1":
        webbrowser.open(URL)
    try:
        _server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        _server.server_close()
        _server = None


if __name__ == "__main__":
    main()
