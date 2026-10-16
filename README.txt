SQLines Log Checker - Investigation Notes & Plain-Text Export
===========================================================

What's new
----------
- Each unexpected error has an investigation/resolution notes box.
- Notes autosave approximately 0.45 seconds after editing (status says Saved).
- Checking Resolved saves the status, changes the badge, and collapses that error.
- Refreshing the page preserves notes, and reopening the same .sql log restores
  them even after the app has been quit and restarted.
- Copy report (two-rectangle icon) and Download .txt are available whenever a
  result is displayed, including PASS results with no unexpected errors.
- Exports show PASS/FAIL/CANNOT VALIDATE, all expected-error checks and counts,
  discrepancies, all unexpected errors, notes, resolved flags and original SQL
  log excerpts. CANNOT VALIDATE reports explicitly identify partial results.

Installation
------------
1. Quit the running SQLines checker (and any older packaged executable).
2. Copy app.py and the templates/index.html file into your project, replacing
   the versions already there.
3. Add notes_store.py and report_export.py alongside app.py.
4. Do NOT replace validator.py, sql_analyzer.py, or log_integrity.py: the
   classification and integrity rules have not changed.
5. Run: python app.py

Tests
-----
Copy tests/test_investigation.py, tests/test_investigation_flask.py, and
 tests/test_template.py into the project's tests directory. The older
 tests/test_lifecycle.py is included with an updated SQLines header fixture.
Run: python -m unittest discover -s tests -v

Notes storage
-------------
Only your notes and Resolved states are saved on disk. Full SQL log contents
are NOT saved on disk by this feature. Notes are associated with a SHA-256
fingerprint of the log's exact text and can be restored by opening the same
file later. Paths:

Windows: %LOCALAPPDATA%\SQLinesLogChecker\notes\
macOS:   ~/Library/Application Support/SQLinesLogChecker/notes/
Linux:   ~/.local/share/SQLinesLogChecker/notes/

For tests, SQLINES_NOTES_DIR overrides the notes directory. Files are local JSON.
When you want a portable record, copy or download the validation report.

Rebuilding the Windows executable
---------------------------------
With the project's Windows virtual environment active:
pyinstaller --onefile --windowed --name SQLinesLogChecker --add-data "templates;templates" app.py

No additional third-party packages are required beyond the app's existing
Flask and build dependencies.


py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask
pip install pyodbc
py app.py
