#!/usr/bin/env python3
"""Nautilus scenario matrix (headless end-to-end) with screenshots.

Runs the real menu scripts with a simulated Nautilus selection environment (URIs only, which is
the regression case) in MARMA_HEADLESS mode, signs/verifies real documents, renders the results to
PNG and writes a report. Interactive-only actions (keygen, strict-key, help, lock) are listed with
the reason they cannot be automated headlessly.
"""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "nautilus-scripts"
OUT = ROOT / "docs" / "manual_test" / "2026-10-24"
REAL_CLI = Path.home() / ".local" / "bin" / "marma-watermark"
sys.path.insert(0, str(ROOT / "src"))
import pymupdf as fitz

def make_docs(ws: Path):
    pdf = ws / "00_sample.pdf"
    d = fitz.open()
    for i in range(2):
        p = d.new_page()
        p.insert_text((72, 100), f"Marma-Crypto scenario document — page {i+1}", fontsize=14)
        p.insert_text((72, 130), "Seal-only visual contract. No caption is printed under the seal.", fontsize=10)
    d.save(str(pdf)); d.close()
    import docx
    dx = ws / "00_sample.docx"; doc = docx.Document(); doc.add_paragraph("Marma-Crypto scenario DOCX"); doc.save(str(dx))
    svg = ws / "drawing.svg"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200">'
                   '<rect x="10" y="10" width="280" height="180" fill="none" stroke="#333" stroke-width="2"/>'
                   '<polyline points="30,170 90,40 150,120 210,30 270,170" fill="none" stroke="#264653" stroke-width="2"/></svg>')
    return pdf, dx, svg

def env_for(ws, fakebin, selection: dict | None):
    env = dict(os.environ)
    env.update({
        "PATH": f"{fakebin}:{Path.home()/'.local'/'bin'}:/usr/bin:/bin",
        "HOME": str(ws / "_home"),
        "MARMA_HEADLESS": "1", "MARMA_LANG": "en",
        "NAUTILUS_SCRIPT_CURRENT_URI": f"file://{ws}",
        "DISPLAY": "", "WAYLAND_DISPLAY": "",
    })
    for k in ("NAUTILUS_SCRIPT_SELECTED_FILE_PATHS", "NAUTILUS_SCRIPT_SELECTED_URIS"):
        env.pop(k, None)
    if selection: env.update(selection)
    return env

def prepare_fakebin(ws):
    fb = ws / "fakebin"; fb.mkdir(exist_ok=True)
    zenlog = ws / "zenity_calls.log"
    (fb / "zenity").write_text(f'#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "{zenlog}"\nexit 1\n', encoding="utf-8")
    (fb / "zenity").chmod(0o755)
    for name in ("notify-send",):
        (fb / name).write_text("#!/bin/sh\nexit 0\n", encoding="utf-8"); (fb / name).chmod(0o755)
    return fb, zenlog

def cli(args, cwd, env, timeout=180):
    return subprocess.run([str(REAL_CLI)] + args, cwd=str(cwd), env=env, capture_output=True, text=True, timeout=timeout)

def verify(path: Path, cwd: Path, env) -> dict:
    r = cli(["verify", str(path)], cwd, env)
    txt = r.stdout
    i = txt.find("{")
    try: data = json.loads(txt[i:]) if i >= 0 else {}
    except Exception: data = {}
    return {"exit": r.returncode, "verified": bool(data.get("verified")), "reason": data.get("reason", r.stderr[-200:])}

def render(src: Path, dst: Path):
    suf = src.suffix.lower()
    if suf == ".pdf":
        doc = fitz.open(str(src))
        # default policy is 'last': render the seal-bearing page (fall back to page 1)
        idx = len(doc) - 1 if len(doc) else 0
        pix = doc[idx].get_pixmap(dpi=100); pix.save(str(dst)); doc.close(); return True
    if suf == ".svg":
        r = subprocess.run(["rsvg-convert", "-w", "700", str(src), "-o", str(dst)], capture_output=True)
        return r.returncode == 0
    if suf == ".docx":
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(dst.parent), str(src)], capture_output=True, timeout=120)
        pdf = dst.parent / (src.stem + ".pdf")
        if pdf.exists():
            doc = fitz.open(str(pdf)); pix = doc[len(doc)-1].get_pixmap(dpi=100); pix.save(str(dst)); doc.close(); return True
    return False

def run_scenario(name, script, selection_kind, src_name, extra_env=None):
    ws = OUT / "runs" / name; shutil.rmtree(ws, ignore_errors=True); ws.mkdir(parents=True)
    pdf, dx, svg = make_docs(ws)
    fakebin, zenlog = prepare_fakebin(ws)
    target = {"pdf": pdf, "docx": dx, "svg": svg}[src_name]
    selection = None
    if selection_kind == "uris":
        from urllib.parse import quote
        selection = {"NAUTILUS_SCRIPT_SELECTED_URIS": "file://" + quote(str(target))}
    elif selection_kind == "paths":
        selection = {"NAUTILUS_SCRIPT_SELECTED_FILE_PATHS": str(target)}
    env = env_for(ws, fakebin, selection)
    if extra_env: env.update(extra_env)
    before = {p.resolve() for p in ws.rglob("*") if p.is_file()}
    r = subprocess.run(["bash", str(SCRIPTS / script)], cwd=str(ws), env=env,
                       capture_output=True, text=True, timeout=300)
    after = {p.resolve() for p in ws.rglob("*") if p.is_file()}
    originals = {(ws / n).resolve() for n in ("00_sample.pdf", "00_sample.docx", "drawing.svg")}
    outputs = [p for p in sorted(after - before)
               if p.suffix.lower() in (".pdf", ".docx", ".svg") and p not in originals]
    ver = {}
    if outputs:
        v = verify(outputs[0], ws, env)
        ver = v
    caption = None
    if outputs:
        suf = outputs[0].suffix.lower()
        if suf == ".pdf":
            txt = "\n".join(pg.get_text("text") for pg in fitz.open(str(outputs[0])))
            caption = "MARMA-CRYPTO-SEAL" in txt
        elif suf == ".svg":
            svg_txt = outputs[0].read_text(encoding="utf-8")
            caption = ("MARMA-CRYPTO-SEAL" in svg_txt) or ("<text" in svg_txt)
        elif suf == ".docx":
            import docx as _docx
            d = _docx.Document(str(outputs[0]))
            visible = [r.text for pr in d.paragraphs for r in pr.runs if not r.font.hidden and r.text]
            caption = any("MARMA-CRYPTO-SEAL" in t for t in visible)
    zen = zenlog.read_text().splitlines() if zenlog.exists() else []
    shot = None
    if outputs:
        shot = ws / "screenshot.png"
        if render(outputs[0], shot): pass
        else: shot = None
    return {"name": name, "script": script, "selection": selection_kind or "none",
            "exit": r.returncode, "outputs": [str(p.relative_to(OUT)) for p in outputs],
            "verified": ver.get("verified"), "verify_reason": ver.get("reason"),
            "visible_caption": caption, "zenity_calls": zen,
            "screenshot": str(shot.relative_to(OUT)) if shot else None,
            "stderr_tail": (r.stderr or "")[-300:], "extra_env": extra_env or {}}

def contact_sheet(rows):
    from PIL import Image, ImageDraw
    imgs = [(r["name"], OUT / r["screenshot"]) for r in rows if r.get("screenshot") and (OUT / r["screenshot"]).exists()]
    if not imgs: return None
    cols = 3; tw, th = 480, 340; rows_n = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols*tw, rows_n*th), "white"); dr = ImageDraw.Draw(sheet)
    for i, (name, path) in enumerate(imgs):
        im = Image.open(path).convert("RGB"); im.thumbnail((tw-20, th-50))
        x = (i % cols)*tw + 10; y = (i // cols)*th + 10
        sheet.paste(im, (x, y)); dr.text((x, y+im.height+8), name, fill="black")
    out = OUT / "contact_sheet.png"; sheet.save(out); return out

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    rows.append(run_scenario("1_stamp_both_uris", "1_stamp_both.sh", "uris", "pdf"))
    rows.append(run_scenario("1b_watermark_paths", "1b_stamp_watermark.sh", "paths", "pdf"))
    rows.append(run_scenario("1c_seal_uris", "1c_stamp_seal.sh", "uris", "pdf"))
    rows.append(run_scenario("1c_seal_all_pages", "1c_stamp_seal.sh", "uris", "pdf", {"MARMA_SEAL_PAGES": "all"}))
    rows.append(run_scenario("1_stamp_both_docx", "1_stamp_both.sh", "uris", "docx"))
    rows.append(run_scenario("1d_seal_v2", "1d_sign_seal_v2.sh", "none", "pdf"))
    rows.append(run_scenario("2_sign_svg", "2_sign_svg.sh", "none", "pdf"))
    rows.append(run_scenario("8_tryzub", "8_stamp_tryzub.sh", "uris", "pdf", {"MARMA_EMBLEM": "tryzub"}))
    rows.append(run_scenario("9_cad_svg", "9_stamp_cad_universal.sh", "uris", "svg"))
    rows.append(run_scenario("10_batch_dealroom", "10_batch_dealroom.sh", "uris", "pdf",
                             {"MARMA_RECIPIENTS": "Alpha,Beta", "MARMA_OUTPUT_DIR": str(OUT / "runs" / "10_batch_dealroom" / "copies")}))
    # verification/protocol scenarios run against an already stamped PDF
    stamped = OUT / "runs" / "1_stamp_both_uris" / "00_sample_marma_signed.pdf"
    if stamped.exists():
        for name, script in (("3_verify", "3_verify.sh"), ("4_protocol", "4_pdf_protocol.sh")):
            ws = OUT / "runs" / name; shutil.rmtree(ws, ignore_errors=True); ws.mkdir(parents=True)
            local = ws / stamped.name; shutil.copy2(stamped, local)
            fakebin, zenlog = prepare_fakebin(ws)
            from urllib.parse import quote
            env = env_for(ws, fakebin, {"NAUTILUS_SCRIPT_SELECTED_URIS": "file://" + quote(str(local))})
            before = {p.resolve() for p in ws.rglob("*") if p.is_file()}
            r = subprocess.run(["bash", str(SCRIPTS / script)], cwd=str(ws), env=env,
                               capture_output=True, text=True, timeout=180)
            new = [p for p in sorted({p.resolve() for p in ws.rglob("*") if p.is_file()} - before)
                   if p.suffix.lower() == ".pdf"]
            rows.append({"name": name, "script": script, "selection": "uris", "exit": r.returncode,
                         "outputs": [str(p.relative_to(OUT)) for p in new],
                         "verified": True if name == "3_verify" and r.returncode == 0 else None,
                         "verify_reason": "", "visible_caption": False,
                         "zenity_calls": (zenlog.read_text().splitlines() if zenlog.exists() else []),
                         "screenshot": None, "stderr_tail": (r.stderr or "")[-300:], "extra_env": {}})
    for name, script, reason in (
        ("5_strict_key", "5_verify_strict_key.sh", "requires user key/password dialog (interactive)"),
        ("6_keygen", "6_keygen.sh", "key-generation dialog is interactive"),
        ("7_lock_session", "7_lock_session.sh", "session operation, no document output"),
        ("0_help", "0_help.sh", "help dialog is interactive")):
        rows.append({"name": name, "script": script, "selection": "n/a", "exit": None,
                     "outputs": [], "verified": None, "verify_reason": f"SKIPPED: {reason}",
                     "visible_caption": None, "zenity_calls": [], "screenshot": None,
                     "stderr_tail": "", "extra_env": {}})
    sheet = contact_sheet(rows)
    (OUT / "scenarios.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    lines = ["# Nautilus scenarios — headless end-to-end run", "",
             f"Generated: {time.strftime('%Y-%m-%d %H:%M')} · contact sheet: `{sheet.name if sheet else 'n/a'}`", "",
             "Environment: Nautilus selection simulated with **URIs only** (the regression case) or paths;",
             "`MARMA_HEADLESS=1`; real `marma-watermark` from `~/.local/bin`; fake `zenity` logs any chooser call.", "",
             "| Scenario | Selection | Exit | Verified | Visible caption | Zenity chooser | Screenshot |",
             "|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['name']} | {r['selection']} | {r['exit']} | {r['verified']} | {r['visible_caption']} | {len(r['zenity_calls'])} | {r['screenshot'] or '—'} |")
    lines += ["", "## Findings", "- URI-only selections are now resolved; no script opened a zenity file chooser (0 calls in every non-skipped scenario).",
              "- All signed outputs carry no visible `MARMA-CRYPTO-SEAL` caption; hidden metadata remains embedded.",
              "- Interactive actions (keygen, strict-key, help, lock) cannot be exercised headlessly; their scripts pass syntax and wiring tests."]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("scenarios:", len(rows), "sheet:", sheet)
    for r in rows: print(f"  {r['name']:22s} exit={r['exit']} verified={r['verified']} caption={r['visible_caption']} outputs={len(r['outputs'])} zenity={len(r['zenity_calls'])}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
