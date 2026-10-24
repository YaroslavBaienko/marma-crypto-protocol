#!/usr/bin/env python3
"""Controlled cross-verified / cross-validated run for the Marma PDF seal.

Phases
  1. preflight   corpus manifest sha256 (180/180), tool versions, git HEAD
  2. tests       the full unittest suite (profiles P1/P2, reserved zone, attacks, cross-runtime,
                 cross-production, KAT, manifests, physical results)
  3. coverage    branch coverage of paper_v3/eval with the knowledge-os venv
  4. matrix      independent cross-validation matrix: 2 profiles x 3 documents x 2 seeds x
                 {exact, trunc-8, trunc-7, single-coordinate edit, flatten}; run twice for
                 determinism and compare the run hash
  5. report      controlled_run/CONTROLLED_RUN_REPORT.md + results.json + coverage.json +
                 environment.json + SHA256SUMS
Exit code 0 only when every gate passes.
"""
from __future__ import annotations
import datetime, hashlib, json, os, platform, subprocess, sys, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "paper_v3" / "eval"
TESTS = ROOT / "paper_v3" / "tests"
OUT = ROOT / "paper_v3" / "tests" / "controlled_run"
VENV_PY = Path.home() / ".venvs" / "knowledge-os" / "bin" / "python"
CORPUS = EVAL / "corpus"
MANIFEST = CORPUS / "corpus_manifest.json"
sys.path.insert(0, str(EVAL))

CORE_MODULES = ["pdf_layer.py", "profiles.py", "harness.py"]
GATES = []

def gate(name, ok, detail=""):
    GATES.append({"gate": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    return ok

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def preflight():
    man = json.loads(MANIFEST.read_text())
    bad = [m["path"] for m in man if sha256(CORPUS / m["path"]) != m["sha256"]]
    gate("corpus manifest", len(man) == 180 and not bad,
         f"{len(man)} files, {len(bad)} hash mismatches")
    head = run(["git", "rev-parse", "HEAD"], cwd=ROOT).stdout.strip()
    dirty = run(["git", "status", "--porcelain"], cwd=ROOT).stdout.strip()
    env = {
        "date": datetime.datetime.now().astimezone().isoformat(),
        "git_head": head, "git_dirty_entries": len(dirty.splitlines()),
        "python": sys.version.split()[0], "platform": platform.platform(),
        "pymupdf": __import__("pymupdf").__version__,
        "node": run(["node", "--version"]).stdout.strip(),
        "typst": run(["typst", "--version"]).stdout.strip(),
        "profiles": json.loads((EVAL / "profiles.json").read_text()) if (EVAL / "profiles.json").exists() else None,
    }
    (OUT / "environment.json").write_text(json.dumps(env, indent=1))
    gate("environment snapshot", bool(head))
    return env

def tests():
    r = run([sys.executable, str(TESTS / "test_controlled.py"), "-v"], cwd=ROOT)
    (OUT / "test_output.txt").write_text(r.stdout + r.stderr)
    ok = r.returncode == 0 and "OK" in (r.stdout + r.stderr)
    import re
    m = re.search(r"Ran (\d+) tests", r.stdout + r.stderr)
    gate("unittest suite", ok, f"{m.group(1) if m else '?'} tests")

def coverage():
    if not VENV_PY.exists():
        gate("coverage", False, "knowledge-os venv missing"); return None
    cov = OUT / "coverage.json"
    cmd = [str(VENV_PY), "-m", "coverage", "run", "--branch",
           f"--source={EVAL}", str(TESTS / "test_controlled.py")]
    r = run(cmd, cwd=ROOT)
    if r.returncode != 0:
        gate("coverage", False, (r.stderr or r.stdout)[-300:]); return None
    r = run([str(VENV_PY), "-m", "coverage", "json", "-o", str(cov)], cwd=ROOT)
    data = json.loads(cov.read_text())
    files = data["files"]
    rel = lambda fn: str(Path("paper_v3") / "eval" / fn)
    def entry(fn):
        return files.get(rel(fn))
    core = {m: (None if entry(m) is None else round(entry(m)["summary"]["percent_covered"], 1))
            for m in CORE_MODULES}
    cc = sum(entry(m)["summary"]["covered_lines"] for m in CORE_MODULES)
    cs = sum(entry(m)["summary"]["num_statements"] for m in CORE_MODULES)
    core_overall = round(100.0 * cc / cs, 1) if cs else 0.0
    overall = round(data["totals"]["percent_covered"], 1)
    thresholds = {"pdf_layer.py": 70.0, "profiles.py": 90.0, "harness.py": 75.0}
    (OUT / "coverage_summary.json").write_text(json.dumps(
        {"overall": overall, "core": core, "core_overall": core_overall,
         "thresholds": thresholds,
         "executed_lines": data["totals"]["covered_lines"],
         "num_statements": data["totals"]["num_statements"]}, indent=1))
    ok = core_overall >= 80.0 and all(
        core[m] is not None and core[m] >= t for m, t in thresholds.items())
    gate("branch coverage", ok,
         f"seal-path {core_overall}% ({core}); overall incl. drivers {overall}%")
    return {"overall": overall, "core": core, "core_overall": core_overall}

def matrix_once(tag):
    import pdf_layer as pl
    from harness import payload_words
    import profiles as pf
    docs = sorted(CORPUS.glob("typst_*_native.pdf"))[:3]
    rows = []
    tmp = Path(tempfile.mkdtemp(prefix="controlled_matrix_"))
    try:
        for p in (pf.P1, pf.P2):
            for di, src in enumerate(docs):
                for seed in range(2):
                    words = payload_words(hashlib.sha256(f"{tag}:{p.id}:{di}:{seed}".encode()).digest(), seed)
                    out = tmp / f"{p.id}_{di}_{seed}.pdf"
                    pf.stamp(src, out, p, words, seed=seed)
                    exact = pf.extract_words(out, p, seed=seed) == words
                    t8 = tmp / f"{p.id}_{di}_{seed}_t8.pdf"; pl.attack_truncate(out, t8, 8)
                    t8ok = pf.extract_words(t8, p, seed=seed) == words
                    t7 = tmp / f"{p.id}_{di}_{seed}_t7.pdf"; pl.attack_truncate(out, t7, 7)
                    t7det = pf.extract_words(t7, p, seed=seed) != words
                    ed = tmp / f"{p.id}_{di}_{seed}_ed.pdf"; pl.attack_edit_coord(out, ed, 1, 0.5)
                    wed = pf.extract_words(ed, p, seed=seed)
                    eddet = wed is not None and sum(a != b for a, b in zip(wed, words)) == 1
                    geo = pf.geometry_ok(out, p)
                    fl = tmp / f"{p.id}_{di}_{seed}_fl.pdf"; pl.flatten(out, fl)
                    absent = pf.extract_words(fl, p, seed=seed) is None
                    rows.append({"profile": p.id, "doc": src.name, "seed": seed,
                                 "exact": exact, "trunc8": t8ok, "trunc7_detected": t7det,
                                 "single_coord_edit": eddet, "geometry_ok": geo,
                                 "flatten_absent": absent})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    h = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    return rows, h

def matrix():
    rows, h1 = matrix_once("matrix")
    _, h2 = matrix_once("matrix")
    n = len(rows)
    checks = {k: all(r[k] for r in rows) for k in
              ("exact", "trunc8", "trunc7_detected", "single_coord_edit",
               "geometry_ok", "flatten_absent")}
    (OUT / "matrix.json").write_text(json.dumps({"rows": rows, "hash": h1}, indent=1))
    gate("cross-validation matrix", n == 12 and all(checks.values()),
         f"{n} samples; {checks}")
    gate("determinism (matrix run twice)", h1 == h2, f"hash {h1[:16]}…")
    return {"rows": rows, "hash": h1, "checks": checks}

def production_profile():
    """P2 profile wired into the production signer wrapper: sign -> verify -> tamper-fail."""
    sys.path.insert(0, str(ROOT / "src"))
    try:
        import marma_seal_profiles as sp
    except Exception as e:  # pragma: no cover
        gate("production P2 profile", False, f"import failed: {e}"); return
    secret = "Sovereign-Vedic-Geometry-Key-108"
    payload = "controlled production profile run"
    tmp = Path(tempfile.mkdtemp(prefix="controlled_prod_"))
    try:
        v2 = tmp / "v2.svg"
        r = sp.sign_seal_svg(payload, secret, v2, profile_id="v2-round42")
        svg = v2.read_text()
        ok_v2 = sp.verify_seal_svg(svg, expected_profile="v2-round42", payload=payload,
                                   secret_key=secret).get("verified") is True
        persisted = 'data-profile="v2-round42"' in svg and 'width="42mm"' in svg
        wrong = sp.verify_seal_svg(svg, expected_profile="v1-geometric", payload=payload,
                                   secret_key=secret).get("verified") is False
        tampered = svg.replace('data-lx="', 'data-lx="1', 1)
        tamper_fail = sp.verify_seal_svg(tampered, payload=payload,
                                         secret_key=secret).get("verified") is False
        v1 = tmp / "v1.svg"
        sp.sign_seal_svg(payload, secret, v1, profile_id="v1-geometric")
        ok_v1 = sp.verify_seal_svg(v1.read_text(), payload=payload, secret_key=secret).get("verified") is True
        ok = all([ok_v2, persisted, wrong, tamper_fail, ok_v1]) and r.get("profile_mm") == 42.0
        gate("production P2 profile", ok,
             f"v2 verified={ok_v2}, profile persisted={persisted}, wrong-profile fail={wrong}, "
             f"tamper fail={tamper_fail}, v1 legacy={ok_v1}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def artifacts():
    files = [EVAL / "pdf_layer.py", EVAL / "profiles.py", EVAL / "harness.py",
             EVAL / "build_corpus.py", EVAL / "profiles.json", TESTS / "test_controlled.py",
             TESTS / "crosscheck_wordmap.js", MANIFEST,
             ROOT / "src" / "marma_seal_profiles.py", ROOT / "src" / "marma_watermark.py"]
    lines = [f"{sha256(f)}  {f.relative_to(ROOT)}" for f in files if f.exists()]
    (OUT / "SHA256SUMS").write_text("\n".join(lines) + "\n")
    gate("artifact hashes", len(lines) == len(files))

def report(env, cov, mat):
    tests_txt = (OUT / "test_output.txt").read_text()
    import re
    m = re.search(r"Ran (\d+) tests", tests_txt)
    n_tests = m.group(1) if m else "?"
    passed = all(g["pass"] for g in GATES)
    lines = [
        "# Controlled cross-verified run — Marma PDF seal",
        "",
        f"**Verdict: {'PASS' if passed else 'FAIL'}** · {env['date']} · git `{env['git_head'][:12]}`",
        "",
        "## Scope",
        "This run covers the *paper profile* P1 (current geometric stamp, no cryptography changes)"
        " and the *product prototype* P2 (42 mm round branded technical stamp with decorative rings,"
        " profile-fixed in the verifier). The payload lattice, word map and key schedule are unchanged.",
        "",
        "## Gates",
        "| Gate | Result | Detail |",
        "|---|---|---|",
    ]
    for g in GATES:
        lines.append(f"| {g['gate']} | {'PASS' if g['pass'] else 'FAIL'} | {g['detail']} |")
    lines += [
        "",
        f"## Tests\nUnittest suite: **{n_tests} tests, {'OK' if passed else 'see test_output.txt'}**."
        " Classes: word-map/KAT, cross-runtime (independent JavaScript), cross-production"
        " (`src/marma_watermark.py`), profile round-trip P1/P2, geometry invariant, truncation,"
        " single-coordinate edit, flatten/fail-closed, wrong-profile rejection, reserved-zone"
        " no-overlap, corpus sha256, physical print-scan results, cross-validation matrix.",
        "",
        "## Coverage (branch)",
        f"Overall: **{cov['overall'] if cov else 'n/a'}%** · core: `{cov['core'] if cov else 'n/a'}`",
        "Uncovered areas are the experiment drivers, baseline implementations and corpus-generator"
        " branches that are not part of the seal path; they are listed in coverage.json.",
        "",
        "## Production profile",
        "P2 is wired into the production signer through the additive wrapper"
        " `src/marma_seal_profiles.py`: the canonical carrier geometry is unchanged, the profile"
        " changes physical size (42 mm), round branding and persists `data-profile` in the SVG"
        " metadata. The verifier fails closed on an unknown or mismatched profile and on tampered"
        " geometry; the legacy v1 path is unchanged.",
        "",
        "## Cross-validation matrix",
        f"12 samples (2 profiles x 3 documents x 2 seeds), run twice: hash `{mat['hash'][:16]}…`."
        f" Checks: `{mat['checks']}`.",
        "",
        "## Cross-run determinism",
        "Matrix hash stable across two independent runs: **"
        + ("PASS" if any(g["gate"].startswith("determinism") and g["pass"] for g in GATES) else "FAIL")
        + "**.",
        "",
        "## Guarantee statement (precise)",
        "Under the stated preconditions — the carrier is written with >=9 decimal places, the"
        " verifier parses the content stream as text, and no rasterisation occurs — the payload is"
        " recovered bit-exactly, 8-decimal re-serialisation is safe, 7-decimal re-serialisation and"
        " single-coordinate edits are detected, flattening fails closed, and an untouched document"
        " yields no carrier. These properties are deterministic and are covered by the gates above.",
        "No absolute 100% guarantee is possible for arbitrary PDF pipelines, hardware or legal"
        " acceptance; those remain out of scope and are stated in the manuscript limitations.",
        "",
        "## Reproduction",
        "```",
        "cd " + str(ROOT),
        "python3 paper_v3/tests/run_controlled.py",
        "```",
        "",
        "## Artifacts",
        "- `results.json` — machine-readable gate results",
        "- `coverage.json`, `coverage_summary.json` — coverage data",
        "- `matrix.json` — cross-validation rows and hash",
        "- `environment.json` — toolchain snapshot",
        "- `SHA256SUMS` — hashes of the tested sources",
        "- `test_output.txt` — full unittest log",
        "",
        "## Out of scope",
        "- full 1,800-sample evaluation (run by `eval/run_pdf_experiments.py`)",
        "- baseline re-implementations, physical printer/scanner population study",
        "- legal validity of a technical seal vs. a company/notary seal (separate review)",
    ]
    (OUT / "CONTROLLED_RUN_REPORT.md").write_text("\n".join(lines) + "\n")
    (OUT / "results.json").write_text(json.dumps(
        {"verdict": "PASS" if passed else "FAIL", "environment": env,
         "gates": GATES, "coverage": cov, "matrix": mat,
         "tests": n_tests}, indent=1))
    return passed

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    env = preflight()
    tests()
    cov = coverage()
    mat = matrix()
    production_profile()
    artifacts()
    ok = report(env, cov, mat)
    print("\nCONTROLLED RUN:", "PASS" if ok else "FAIL", "->", OUT / "CONTROLLED_RUN_REPORT.md")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
