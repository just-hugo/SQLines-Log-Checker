import importlib.util
"""Run with `python -m unittest discover -s tests` after installing Flask.

Tests the live local server without opening a browser. This test starts two
Python processes, verifies the second cannot replace the first, and then
shuts the first down using the same authorized request as the UI.
"""

import os
from pathlib import Path
import re
import socket
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
from test_integrity import expected_log, failed


def free_port():
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


@unittest.skipUnless(importlib.util.find_spec('flask'), 'Flask not installed in test environment')
class LifecycleTest(unittest.TestCase):
    def test_second_launch_and_quit(self):
        port = free_port()
        base = f"http://127.0.0.1:{port}"
        env = dict(os.environ, SQLINES_PORT=str(port), SQLINES_NO_BROWSER="1")
        first = subprocess.Popen(
            [sys.executable, str(ROOT / "app.py")], cwd=ROOT,
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
        )
        try:
            for _ in range(60):
                try:
                    with urlopen(base + "/_health", timeout=0.3) as response:
                        if response.headers.get("X-SQLines-App") == "SQLinesLogChecker-v1":
                            break
                except (URLError, OSError):
                    if first.poll() is not None:
                        self.fail("First server exited before starting")
                    time.sleep(0.1)
            else:
                self.fail("First server did not start")

            # Upload one error and make sure POST/redirect/GET renders a report.
            # The original bug was that the second launch only rendered the
            # blank upload form, even though the server itself was reused.
            sql_log = expected_log() + failed(
                'ALTER TABLE GROUP1.[category_tb_OLD] ADD PRIMARY KEY ([ca_code]);',
                'The duplicate key value is (HAY ).'
            )
            posted = Request(
                base + "/", data=urlencode({"log_text": sql_log}).encode("utf-8"),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            with urlopen(posted, timeout=5) as response:
                self.assertEqual(response.status, 200)
                self.assertEqual(response.geturl(), base + "/")
                self.assertIn("Validation failed", response.read().decode("utf-8"))

            second = subprocess.run(
                [sys.executable, str(ROOT / "app.py")], cwd=ROOT,
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=10,
            )
            self.assertEqual(second.returncode, 0, second.stderr.decode(errors="replace"))
            self.assertIsNone(first.poll(), "Second launch must not kill the first")
            # A fresh GET (including one opened by the second launch)
            # must show the already-analyzed result, not the initial form.
            with urlopen(base + "/", timeout=2) as response:
                reopened_page = response.read().decode("utf-8")
            self.assertIn("Validation failed", reopened_page)
            self.assertIn("Unexpected errors (1)", reopened_page)
            self.assertIn("category_tb_OLD", reopened_page)


            with urlopen(base, timeout=2) as response:
                page = response.read().decode("utf-8")
            self.assertIn('id="quit-app"', page)
            token_match = re.search(r"'X-SQLines-Shutdown-Token':\s*\"([^\"]+)\"", page)
            self.assertIsNotNone(token_match)

            with self.assertRaises(HTTPError) as error:
                urlopen(Request(base + "/_shutdown", method="POST"), timeout=2)
            self.assertEqual(error.exception.code, 403)

            request = Request(
                base + "/_shutdown", method="POST",
                headers={"X-SQLines-Shutdown-Token": token_match.group(1)},
            )
            with urlopen(request, timeout=2) as response:
                self.assertEqual(response.status, 200)
            first.wait(timeout=8)
            self.assertEqual(first.returncode, 0)

            # The listener is actually released, not just hidden in the UI.
            with socket.socket() as probe:
                probe.bind(("127.0.0.1", port))
        finally:
            if first.poll() is None:
                first.terminate()
                try:
                    first.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    first.kill()
                    first.wait(timeout=3)
            if first.stderr:
                first.stderr.close()


if __name__ == "__main__":
    unittest.main()
