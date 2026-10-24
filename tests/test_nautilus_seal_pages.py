#!/usr/bin/env python3
"""Nautilus seal-placement preference: config file, env override, dialog and settings action."""
from __future__ import annotations
import json, os, shutil, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "nautilus-scripts"
SIGN = SCRIPTS / "1_stamp_both.sh"
SETTINGS = SCRIPTS / "12_seal_pages.sh"

def fake_env(tmp: Path, config: dict | None, dialog_choice: str = "all"):
    fakebin = tmp / "bin"; fakebin.mkdir(exist_ok=True)
    clilog = tmp / "cli.log"; zenlog = tmp / "zenity.log"
    (fakebin / "marma-watermark").write_text(
        '#!/usr/bin/env bash\nprintf "%s\\n" "$@" >> "' + str(clilog) + '"\nexit 0\n', encoding="utf-8")
    (fakebin / "marma-watermark").chmod(0o755)
    for n in ("notify-send",):
        (fakebin / n).write_text("#!/bin/sh\nexit 0\n", encoding="utf-8"); (fakebin / n).chmod(0o755)
    (fakebin / "zenity").write_text(
        '#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "' + str(zenlog) + '"\n'
        'case "$*" in *--file-selection*) echo "' + str(tmp / "picked.pdf") + '";; *) echo "' + dialog_choice + '";; esac\n',
        encoding="utf-8")
    (fakebin / "zenity").chmod(0o755)
    home = tmp / "home"; home.mkdir(exist_ok=True)
    if config is not None:
        cfgdir = home / ".config" / "marma-crypto"; cfgdir.mkdir(parents=True, exist_ok=True)
        (cfgdir / "config.json").write_text(json.dumps(config), encoding="utf-8")
    env = dict(os.environ)
    env.update({"PATH": f"{fakebin}:/usr/bin:/bin", "HOME": str(home), "MARMA_LANG": "en",
                "NAUTILUS_SCRIPT_CURRENT_URI": f"file://{tmp}",
                "NAUTILUS_SCRIPT_SELECTED_FILE_PATHS": str(tmp / "doc.pdf")})
    for k in ("MARMA_SEAL_PAGES", "MARMA_HEADLESS"):
        env.pop(k, None)
    env["DISPLAY"] = ""
    env["WAYLAND_DISPLAY"] = ""
    (tmp / "doc.pdf").write_bytes(b"%PDF-1.4\n%%EOF\n")
    return env, clilog, zenlog, home

class TestNautilusSealPlacement(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="nautilus_pages_")); self.addCleanup(shutil.rmtree, self.tmp, True)

    def _run(self, script, config=None, extra=None, dialog_choice="all"):
        env, clilog, zenlog, home = fake_env(self.tmp, config, dialog_choice)
        env.update(extra or {})
        r = subprocess.run(["bash", str(script)], cwd=str(self.tmp), env=env,
                           capture_output=True, text=True, timeout=60)
        cli = clilog.read_text().splitlines() if clilog.exists() else []
        zen = zenlog.read_text().splitlines() if zenlog.exists() else []
        return r, cli, zen, home

    def test_default_last_no_dialog_headless(self):
        r, cli, zen, _ = self._run(SIGN, None, {"MARMA_HEADLESS": "1"})
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        self.assertIn("--seal-pages", cli); self.assertIn("last", cli)
        self.assertEqual(zen, [])

    def test_config_first_last(self):
        r, cli, zen, _ = self._run(SIGN, {"lang": "en", "seal_pages": "first-last"}, {"MARMA_HEADLESS": "1"})
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        self.assertIn("first-last", cli); self.assertEqual(zen, [])

    def test_env_overrides_config(self):
        r, cli, _, _ = self._run(SIGN, {"seal_pages": "first"}, {"MARMA_HEADLESS": "1", "MARMA_SEAL_PAGES": "all"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("all", cli)

    def test_ask_headless_falls_back_to_last(self):
        r, cli, zen, _ = self._run(SIGN, {"seal_pages": "ask"}, {"MARMA_HEADLESS": "1"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("last", cli); self.assertEqual(zen, [])

    def test_ask_with_display_opens_dialog(self):
        extra = {"DISPLAY": ":0", "WAYLAND_DISPLAY": ""}
        r, cli, zen, _ = self._run(SIGN, {"seal_pages": "ask"}, extra, dialog_choice="all")
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        self.assertTrue(any("--list" in z for z in zen), zen)
        self.assertIn("all", cli)

    def test_invalid_config_falls_back_to_last(self):
        r, cli, _, _ = self._run(SIGN, {"seal_pages": "garbage"}, {"MARMA_HEADLESS": "1"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("last", cli)

    def test_settings_action_saves_choice(self):
        r, cli, zen, home = self._run(SETTINGS, {"lang": "en", "seal_pages": "last"},
                                      {"DISPLAY": ":0", "WAYLAND_DISPLAY": ""}, dialog_choice="first-last")
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        cfg = json.loads((home / ".config" / "marma-crypto" / "config.json").read_text())
        self.assertEqual(cfg["seal_pages"], "first-last")
        self.assertEqual(cfg.get("lang"), "en")

    def test_seal_and_seal_only_scripts_use_policy(self):
        for script in ("1c_stamp_seal.sh", "8_stamp_tryzub.sh"):
            r, cli, _, _ = self._run(SCRIPTS / script, {"seal_pages": "first-last"}, {"MARMA_HEADLESS": "1"})
            self.assertEqual(r.returncode, 0, (script, r.stderr[-300:]))
            self.assertIn("--seal-pages", cli); self.assertIn("first-last", cli)

if __name__ == "__main__":
    unittest.main(verbosity=2)
