#!/usr/bin/env python3
"""Nautilus selection resolution tests (regression: file chooser opened despite a selection).

Nautilus may expose the selected item as NAUTILUS_SCRIPT_SELECTED_FILE_PATHS, as
NAUTILUS_SCRIPT_SELECTED_URIS, or only via URIs depending on view/version. The scripts used to
read only the PATH variable, so a selected PDF resulted in an empty list and a fallback zenity
file chooser. `marma_selected_files` now accepts paths, file:// URIs and the split-view fallback.
"""
from __future__ import annotations
import os, shutil, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "nautilus-scripts"
SIGN_SCRIPT = SCRIPTS / "1_stamp_both.sh"

def make_fake_env(tmp: Path):
    fakebin = tmp / "bin"; fakebin.mkdir()
    log = tmp / "cli.log"
    zen = tmp / "zenity.log"
    (fakebin / "marma-watermark").write_text(
        '#!/usr/bin/env bash\nprintf "%s\\n" "$@" >> "' + str(log) + '"\nexit 0\n', encoding="utf-8")
    (fakebin / "marma-watermark").chmod(0o755)
    (fakebin / "notify-send").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    (fakebin / "notify-send").chmod(0o755)
    (fakebin / "zenity").write_text(
        '#!/usr/bin/env bash\nprintf "%s\\n" "$@" >> "' + str(zen) + '"\necho "' + str(tmp / "picked.pdf") + '"\n',
        encoding="utf-8")
    (fakebin / "zenity").chmod(0o755)
    home = tmp / "home"; home.mkdir()
    env = dict(os.environ)
    env.update({"PATH": f"{fakebin}:/usr/bin:/bin", "HOME": str(home), "MARMA_LANG": "en",
                "NAUTILUS_SCRIPT_CURRENT_URI": f"file://{tmp}"})
    for k in ("NAUTILUS_SCRIPT_SELECTED_FILE_PATHS", "NAUTILUS_SCRIPT_SELECTED_URIS",
              "NAUTILUS_SCRIPT_NEXT_PANE_SELECTED_FILE_PATHS"):
        env.pop(k, None)
    return env, log, zen

class TestNautilusSelection(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="nautilus_sel_")); self.addCleanup(shutil.rmtree, self.tmp, True)
        self.doc = self.tmp / "selected doc.pdf"; self.doc.write_bytes(b"%PDF-1.4\n%%EOF\n")
        self.env, self.clilog, self.zenlog = make_fake_env(self.tmp)

    def _run_script(self, extra_env):
        env = dict(self.env); env.update(extra_env)
        r = subprocess.run(["bash", str(SIGN_SCRIPT)], cwd=str(self.tmp), env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr[-600:])
        cli = self.clilog.read_text().splitlines() if self.clilog.exists() else []
        zen = self.zenlog.read_text().splitlines() if self.zenlog.exists() else []
        return cli, zen

    def test_selected_file_paths_used_without_chooser(self):
        cli, zen = self._run_script({"NAUTILUS_SCRIPT_SELECTED_FILE_PATHS": str(self.doc)})
        self.assertIn(str(self.doc), cli)
        self.assertEqual(zen, [])

    def test_selected_uris_only_used_without_chooser(self):
        # regression scenario: Nautilus gives URIs only -> script must not open a file chooser
        cli, zen = self._run_script({"NAUTILUS_SCRIPT_SELECTED_URIS": f"file://{self.doc}"})
        self.assertIn(str(self.doc), cli)
        self.assertEqual(zen, [])

    def test_uri_with_spaces_and_percent_encoding(self):
        doc = self.tmp / "space and ü.pdf"; doc.write_bytes(b"%PDF-1.4\n%%EOF\n")
        from urllib.parse import quote
        uri = "file://" + quote(str(doc))
        env = dict(self.env); env["NAUTILUS_SCRIPT_SELECTED_URIS"] = uri
        r = subprocess.run(["bash", str(SIGN_SCRIPT)], cwd=str(self.tmp), env=env,
                           capture_output=True, text=True, timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr[-600:])
        cli = self.clilog.read_text().splitlines()
        # percent-decoded path should be passed (spaces remain)
        self.assertIn(str(doc), cli)
        self.assertFalse(self.zenlog.exists() and self.zenlog.read_text().strip())

    def test_no_selection_still_opens_fallback_chooser(self):
        cli, zen = self._run_script({})
        self.assertTrue(zen, "fallback file chooser expected when nothing is selected")
        self.assertIn(str(self.tmp / "picked.pdf"), cli)

    def test_helper_unit_paths_uris_and_empty(self):
        helper = f'''
set -euo pipefail
source "{SCRIPTS / '_i18n.sh'}"
marma_selected_files
'''
        def run(env):
            e = dict(self.env); e.update(env)
            r = subprocess.run(["bash", "-c", helper], env=e, capture_output=True, text=True, timeout=15)
            self.assertEqual(r.returncode, 0, r.stderr)
            return [l for l in r.stdout.splitlines() if l]
        self.assertEqual(run({"NAUTILUS_SCRIPT_SELECTED_FILE_PATHS": "/a b/c.pdf"}), ["/a b/c.pdf"])
        self.assertEqual(run({"NAUTILUS_SCRIPT_SELECTED_URIS": "file:///a%20b/c.pdf"}), ["/a b/c.pdf"])
        self.assertEqual(run({}), [])

    def test_all_selection_scripts_use_shared_helper(self):
        expected = 10
        found = [f for f in SCRIPTS.glob("*.sh") if "marma_selected_files" in f.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(found), expected + 1)  # + _i18n.sh itself
        for f in SCRIPTS.glob("*.sh"):
            r = subprocess.run(["bash", "-n", str(f)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{f.name}: {r.stderr}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
