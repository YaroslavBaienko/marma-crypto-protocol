#!/usr/bin/env python3
"""Exhaustive Cross-Validation & Cross-Verification Test Suite for Marma-Crypto Protocol v1.2.0.

Covers:
1. Canonical 9-Triangle Sri Yantra Geometry & Bilateral Symmetry Invariants (lx + rx == 300.0).
2. Cross-Runtime Bit-Exactness: Python (`marma_watermark.py`) <-> Node.js (`dstu4145_bridge.js`) <-> Browser JS (`docs/index.html`).
3. Pure-JS FIPS 180-4 SHA-256 & Python-compatible `computePublicSealDigest` cross-verification.
4. DSTU 4145-2002 Elliptic Curve GF(2^257), GOST 34.311-95, DSTU 7564:2014 (Kupyna-256), and RFC 6979 determinism.
5. Full 36-Coordinate Tamper Matrix (lx, rx, by, ay across all 9 triangles) in both Python and Browser JS.
6. Multi-format (PDF modes both/watermark/seal, DOCX with tables, SVG, and Self-Sealed Protocol PDF) round-trip verification.
7. Web Verifier (`docs/index.html`) Attack Simulation & Reset State Machine + Language Toggle + Same-File Re-Upload.
8. Production Whitepaper & PAdES-LTA / CAdES Artifact & Manifest Integrity Audit.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import docx
import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import marma_watermark as mw  # noqa: E402


def run_browser_js_harness(js_body: str) -> dict:
    """Execute a test snippet inside the actual `docs/index.html` JavaScript VM context via Node.js."""
    script_code = f"""
const fs = require("fs");
const vm = require("vm");
const html = fs.readFileSync({json.dumps(str(REPO_ROOT / "docs" / "index.html"))}, "utf8");
const scriptMatch = html.match(/<script>([\\s\\S]*?)<\\/script>/);
if (!scriptMatch) throw new Error("No <script> tag in docs/index.html");

const elems = {{}};
const sandbox = {{
  document: {{
    documentElement: {{ lang: "en" }},
    getElementById: (id) => {{
      if (!elems[id]) {{
        elems[id] = {{
          id,
          textContent: "",
          innerHTML: "",
          value: "",
          style: {{}},
          className: "",
          classList: {{ add(){{}}, remove(){{}} }},
          addEventListener(){{}},
          appendChild(){{}}
        }};
      }}
      return elems[id];
    }},
    querySelectorAll: () => [],
    createElement: () => ({{ innerHTML: "", className: "" }})
  }},
  TextEncoder,
  TextDecoder,
  DataView,
  Uint8Array,
  Uint32Array,
  Buffer,
  Response,
  DecompressionStream: globalThis.DecompressionStream,
  console,
  elems,
  fs
}};
vm.createContext(sandbox);
vm.runInContext(scriptMatch[1], sandbox);
const testFn = new vm.Script(`(async () => {{ {js_body} }})()`);
testFn.runInContext(sandbox).then(res => {{
  console.log(JSON.stringify({{ ok: true, result: res }}));
}}).catch(err => {{
  console.log(JSON.stringify({{ ok: false, error: err.message || String(err) }}));
  process.exit(1);
}});
"""
    proc = subprocess.run(
        ["node", "-e", script_code],
        capture_output=True,
        text=True,
        timeout=25,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(f"Browser JS harness failed: {proc.stderr or proc.stdout}")
    last_line = proc.stdout.strip().splitlines()[-1]
    payload = json.loads(last_line)
    if not payload.get("ok"):
        raise AssertionError(f"Browser JS error: {payload.get('error')}")
    return payload["result"]


class TestMarmaCryptoCrossVerification(unittest.TestCase):
    """Comprehensive audit, cross-validation, and cross-verification test suite."""

    def test_01_canonical_geometry_and_bilateral_symmetry(self) -> None:
        """Verify all 9 canonical triangles satisfy lx + rx == 300.0 and valid ordering."""
        self.assertEqual(len(mw.CANONICAL_TRIANGLES), 9)
        names = [t[0] for t in mw.CANONICAL_TRIANGLES]
        self.assertEqual(names, ["D1", "U1", "U3", "U2", "D3", "D2", "U4", "D4", "D5"])
        for name, lx, by, ay, rx, is_up in mw.CANONICAL_TRIANGLES:
            self.assertAlmostEqual(lx + rx, 300.0, places=9, msg=f"Symmetry broken on {name}")
            self.assertGreater(rx, lx, msg=f"rx <= lx on {name}")
            self.assertEqual(name.startswith("U"), is_up)
            if is_up:
                self.assertGreater(by, ay, msg=f"Upward triangle {name} must have by > ay")
            else:
                self.assertLess(by, ay, msg=f"Downward triangle {name} must have by < ay")

    def test_02_cross_runtime_sha256_and_perturbation_derivation(self) -> None:
        """Cross-verify Python hashlib/perturbation math against Browser JS sha256Hex/applySignedPerturbations."""
        test_strings = [
            "",
            "abc",
            "MARMA-CRYPTO-PROTOCOL-V1.2",
            "Баєнко Ярослав Володимирович :: ДСТУ 4145-2002 :: Шрі Янтра 54 марми",
            "A" * 256,
        ]
        expected_hashes = [hashlib.sha256(s.encode("utf-8")).hexdigest() for s in test_strings]

        # Generate 20 deterministic HMAC hex digests and compare Python vs JS offsets & triangle coordinates
        sample_hmacs = [
            hashlib.sha256(f"SEED-{i}".encode("utf-8")).hexdigest() for i in range(20)
        ]
        py_offsets = [mw.derive_offsets_from_hmac_hex(h) for h in sample_hmacs]

        js_res = run_browser_js_harness(f"""
          const strings = {json.dumps(test_strings)};
          const jsHashes = strings.map(s => sha256Hex(s));
          const hmacs = {json.dumps(sample_hmacs)};
          const jsOffsets = hmacs.map(h => deriveOffsetsFromHmac(h));
          const tris150 = applySignedPerturbations(solveBaselineYantra(150.0), hmacs[0], 150.0);
          const tris300 = applySignedPerturbations(solveBaselineYantra(300.0), hmacs[0], 300.0);
          return {{ jsHashes, jsOffsets, tris150, tris300 }};
        """)

        self.assertEqual(js_res["jsHashes"], expected_hashes)
        self.assertEqual(js_res["jsOffsets"], py_offsets)

        # Verify coordinate scaling [0, 300]^2 and [0, 600]^2 between Python and JS
        d150, s150 = mw.verify_triangle_coordinates(js_res["tris150"], py_offsets[0], cx=150.0)
        d300, s300 = mw.verify_triangle_coordinates(js_res["tris300"], py_offsets[0], cx=300.0)
        self.assertEqual(d150, 0.0)
        self.assertEqual(s150, 0.0)
        self.assertEqual(d300, 0.0)
        self.assertEqual(s300, 0.0)

    def test_03_dstu4145_bridge_sign_verify_and_tamper_rejection(self) -> None:
        """Cross-verify dstu4145_bridge.js RFC 6979 determinism, GF(2^257) EC math, and tamper rejection."""
        payload_hex = "EDU-VEDI::CROSS-VERIFICATION-TEST::2026".encode("utf-8").hex()
        sign1 = mw.call_dstu4145_bridge({
            "action": "sign",
            "secretSeed": "Test-Key-Seed-4145",
            "payloadBytesHex": payload_hex,
        })
        sign2 = mw.call_dstu4145_bridge({
            "action": "sign",
            "secretSeed": "Test-Key-Seed-4145",
            "payloadBytesHex": payload_hex,
        })
        self.assertEqual(sign1["status"], "ok")
        # RFC 6979 determinism: signing identical payload with identical key must yield identical (r, s)
        self.assertEqual(sign1["r_hex"], sign2["r_hex"])
        self.assertEqual(sign1["s_hex"], sign2["s_hex"])
        self.assertEqual(sign1["rs_digest_hex"], sign2["rs_digest_hex"])
        self.assertEqual(
            sign1["rs_digest_hex"],
            hashlib.sha256(f"{sign1['r_hex']}::{sign1['s_hex']}".encode("utf-8")).hexdigest(),
        )

        # Valid verification
        ver_ok = mw.call_dstu4145_bridge({
            "action": "verify",
            "payloadBytesHex": payload_hex,
            "dstu4145": sign1,
        })
        self.assertTrue(ver_ok["dstu4145_valid"])
        self.assertTrue(ver_ok["gost34311_match"])
        self.assertTrue(ver_ok["ec_signature_valid"])
        self.assertTrue(ver_ok["rs_digest_match"])

        # Tamper 1: Modified payload bytes
        ver_bad_payload = mw.call_dstu4145_bridge({
            "action": "verify",
            "payloadBytesHex": "EDU-VEDI::CROSS-VERIFICATION-TAMPERED".encode("utf-8").hex(),
            "dstu4145": sign1,
        })
        self.assertFalse(ver_bad_payload["dstu4145_valid"])
        self.assertFalse(ver_bad_payload["gost34311_match"])

        # Tamper 2: Modified vector r_hex on GF(2^257)
        bad_r = dict(sign1)
        bad_r["r_hex"] = sign1["r_hex"][:-2] + ("00" if sign1["r_hex"][-2:] != "00" else "ff")
        ver_bad_r = mw.call_dstu4145_bridge({
            "action": "verify",
            "payloadBytesHex": payload_hex,
            "dstu4145": bad_r,
        })
        self.assertFalse(ver_bad_r["dstu4145_valid"])

        # Tamper 3: Modified rs_digest_hex
        bad_rs_digest = dict(sign1)
        bad_rs_digest["rs_digest_hex"] = "0" * 64
        ver_bad_rs = mw.call_dstu4145_bridge({
            "action": "verify",
            "payloadBytesHex": payload_hex,
            "dstu4145": bad_rs_digest,
        })
        self.assertFalse(ver_bad_rs["dstu4145_valid"])
        self.assertFalse(ver_bad_rs["rs_digest_match"])

    def test_04_36_coordinate_tamper_matrix_python_and_js(self) -> None:
        """Perturb every single coordinate (lx, rx, by, ay) across all 9 triangles (36 tests) and verify 100% detection."""
        with tempfile.TemporaryDirectory(prefix="marma_36coord_") as tmp:
            svg_path = Path(tmp) / "matrix_test.svg"
            payload = "MARMA-36-COORDINATE-AUDIT-MATRIX"
            mw.sign_sri_yantra_svg(payload, mw.DEFAULT_SECRET, svg_path)
            base_svg = svg_path.read_text(encoding="utf-8")

            # Clean baseline must pass in both Python and Browser JS
            py_clean = mw.verify_sri_yantra_svg(base_svg, payload)
            self.assertTrue(py_clean["verified"])
            self.assertEqual(py_clean["max_coordinate_signature_drift"], 0.0)
            self.assertEqual(py_clean["max_bilateral_symmetry_error"], 0.0)

            for tri in py_clean["triangles"]:
                t_name = tri["name"]
                for coord_key in ("lx", "by", "ay", "rx"):
                    orig_val = f'{coord_key}="{tri[coord_key]:.9f}"'
                    tampered_val = f'{coord_key}="{tri[coord_key] + 0.000100000:.9f}"'
                    old_tag_prefix = f'id="tri_{t_name}"'
                    # Replace only inside the target triangle tag
                    lines = []
                    for line in base_svg.splitlines():
                        if old_tag_prefix in line:
                            self.assertIn(orig_val, line)
                            line = line.replace(orig_val, tampered_val, 1)
                        lines.append(line)
                    tampered_svg = "\n".join(lines)

                    py_tamper = mw.verify_sri_yantra_svg(tampered_svg, payload)
                    self.assertFalse(
                        py_tamper["verified"],
                        msg=f"Python verifier missed tamper on {t_name}.{coord_key}",
                    )
                    self.assertGreaterEqual(
                        py_tamper["max_coordinate_signature_drift"],
                        9e-5,
                        msg=f"Python drift not detected on {t_name}.{coord_key}",
                    )

            # Also verify in Browser JS that tampering `by`, `ay`, `public_seal_digest`, or `r_hex` alone is caught!
            js_check = run_browser_js_harness(f"""
              const buf = fs.readFileSync({json.dumps(str(svg_path))});
              const seal = extractMarmaSealFromBytes(new Uint8Array(buf), "matrix_test.svg");
              renderVerificationState(seal, "matrix_test.svg", false);
              const cleanOk = elems.statusBanner.className.includes("ok");

              // Tamper ONLY ay of D5 by +0.0001 (lx + rx remains 300.0!)
              const sealAyTamper = JSON.parse(JSON.stringify(seal));
              sealAyTamper.triangles[8].ay = Number((sealAyTamper.triangles[8].ay + 0.0001).toFixed(9));
              renderVerificationState(sealAyTamper, "ay_tamper.svg", true);
              const ayTamperRejected = elems.statusBanner.className.includes("err");

              // Tamper ONLY by of U4 by -0.0001 (lx + rx remains 300.0!)
              const sealByTamper = JSON.parse(JSON.stringify(seal));
              sealByTamper.triangles[6].by = Number((sealByTamper.triangles[6].by - 0.0001).toFixed(9));
              renderVerificationState(sealByTamper, "by_tamper.svg", true);
              const byTamperRejected = elems.statusBanner.className.includes("err");

              return {{ cleanOk, ayTamperRejected, byTamperRejected }};
            """)
            self.assertTrue(js_check["cleanOk"])
            self.assertTrue(js_check["ayTamperRejected"])
            self.assertTrue(js_check["byTamperRejected"])

    def test_05_pdf_docx_svg_and_protocol_end_to_end_cross_runtime(self) -> None:
        """Sign PDF (all 3 modes), DOCX (paragraphs + tables), SVG, and Protocol PDF; verify in Python & Browser JS."""
        with tempfile.TemporaryDirectory(prefix="marma_e2e_") as tmp:
            tmp_dir = Path(tmp)

            # 1. PDF across modes: both, watermark, seal
            raw_pdf = tmp_dir / "source.pdf"
            doc = pymupdf.open()
            for p_idx in range(2):
                page = doc.new_page()
                page.insert_text((72, 100), f"Marma-Crypto Test Page {p_idx + 1} — Правовий протокол Шрі Янтри", fontsize=12)
            doc.save(str(raw_pdf))
            doc.close()

            for mode in ("both", "watermark", "seal"):
                signed_pdf = tmp_dir / f"signed_{mode}.pdf"
                mw.stamp_pdf_document(raw_pdf, signed_pdf, secret_key=mw.DEFAULT_SECRET, mode=mode)
                py_res = mw.verify_pdf_document(signed_pdf)
                self.assertTrue(py_res["verified"], f"PDF mode={mode} failed Python verification")
                self.assertEqual(py_res["max_coordinate_signature_drift"], 0.0)
                self.assertEqual(py_res["max_bilateral_symmetry_error"], 0.0)

                js_res = run_browser_js_harness(f"""
                  const buf = fs.readFileSync({json.dumps(str(signed_pdf))});
                  const seal = extractMarmaSealFromBytes(new Uint8Array(buf), {json.dumps(signed_pdf.name)});
                  renderVerificationState(seal, {json.dumps(signed_pdf.name)}, false);
                  return {{
                    banner: elems.statusBanner.className,
                    errors: elems.valErrors.textContent
                  }};
                """)
                self.assertIn("ok", js_res["banner"])
                self.assertIn("Δ_sym = 0.000000000000  |  Δ_coord = 0.000000000000", js_res["errors"])

            # 2. Protocol PDF generation & self-verification in Python and Browser JS
            proto_pdf = tmp_dir / "signed_both_protocol.pdf"
            mw.generate_pdf_verification_protocol(tmp_dir / "signed_both.pdf", proto_pdf, lang="uk")
            proto_py = mw.verify_pdf_document(proto_pdf)
            self.assertTrue(proto_py["verified"], "Generated Protocol PDF must itself be verifiable")

            proto_js = run_browser_js_harness(f"""
              const buf = fs.readFileSync({json.dumps(str(proto_pdf))});
              const seal = extractMarmaSealFromBytes(new Uint8Array(buf), "signed_both_protocol.pdf");
              renderVerificationState(seal, "signed_both_protocol.pdf", false);
              return {{ banner: elems.statusBanner.className, errors: elems.valErrors.textContent }};
            """)
            self.assertIn("ok", proto_js["banner"])

            # 3. DOCX with paragraphs and tables — verify in Python and Browser JS (via DecompressionStream)
            raw_docx = tmp_dir / "contract.docx"
            signed_docx = tmp_dir / "contract_signed.docx"
            w = docx.Document()
            w.add_heading("Договір про передачу прав інтелектуальної власності", 0)
            w.add_paragraph("Сторона 1: Баєнко Ярослав Володимирович.")
            tbl = w.add_table(rows=2, cols=2)
            tbl.cell(0, 0).text = "Параметр"
            tbl.cell(0, 1).text = "Значення"
            tbl.cell(1, 0).text = "Стандарт"
            tbl.cell(1, 1).text = "ДСТУ 4145-2002 / Шрі Янтра"
            w.save(str(raw_docx))

            mw.stamp_docx_document(raw_docx, signed_docx, secret_key=mw.DEFAULT_SECRET)
            docx_py = mw.verify_docx_document(signed_docx)
            self.assertTrue(docx_py["verified"])
            self.assertEqual(docx_py["max_coordinate_signature_drift"], 0.0)

            docx_js = run_browser_js_harness(f"""
              const buf = fs.readFileSync({json.dumps(str(signed_docx))});
              const seal = await extractDocxMarmaSeal(new Uint8Array(buf));
              renderVerificationState(seal, "contract_signed.docx", false);
              return {{ banner: elems.statusBanner.className, errors: elems.valErrors.textContent }};
            """)
            self.assertIn("ok", docx_js["banner"])
            self.assertIn("Δ_sym = 0.000000000000  |  Δ_coord = 0.000000000000", docx_js["errors"])

            # Tamper DOCX table cell text and verify Python rejects it
            tampered_docx = tmp_dir / "contract_tampered.docx"
            w_mod = docx.Document(str(signed_docx))
            w_mod.tables[0].cell(1, 1).text = "ДСТУ 4145-2002 (ПІДРОБЛЕНО)"
            w_mod.save(str(tampered_docx))
            docx_tamper_py = mw.verify_docx_document(tampered_docx)
            self.assertFalse(docx_tamper_py["verified"])
            self.assertIn("modified", docx_tamper_py["reason"])

    def test_06_web_verifier_attack_simulation_and_reset_lifecycle(self) -> None:
        """Exhaustively test simulateTamperAttack(), toggle reset, language switch, and re-uploading after attack."""
        res = run_browser_js_harness(f"""
          const states = [];
          // 1. Initial load
          states.push({{
            step: "init",
            banner: elems.statusBanner.className,
            btn: elems.btnSimulateAttack.textContent,
            errors: elems.valErrors.textContent
          }});

          // 2. Click Simulate Attack
          simulateTamperAttack();
          states.push({{
            step: "attack_on",
            banner: elems.statusBanner.className,
            btn: elems.btnSimulateAttack.textContent,
            errors: elems.valErrors.textContent
          }});

          // 3. Language toggle while attack is active (starts in EN -> switches to UK -> back to EN)
          const btnEnAttack = elems.btnSimulateAttack.textContent;
          toggleLanguage();
          const btnUkAttack = elems.btnSimulateAttack.textContent;
          toggleLanguage();

          // 4. Click Reset Attack (second click on same button)
          simulateTamperAttack();
          states.push({{
            step: "attack_reset",
            banner: elems.statusBanner.className,
            btn: elems.btnSimulateAttack.textContent,
            errors: elems.valErrors.textContent
          }});

          // 5. Activate attack again, then load each of the 5 repository artifacts
          const artifactFiles = [
            "docs/whitepaper/Marma_Crypto_Whitepaper_UA.pdf",
            "docs/whitepaper/Marma_Crypto_Whitepaper_EN.pdf",
            "docs/whitepaper/sri_yantra_whitepaper_diagram.svg",
            "docs/whitepaper/Marma_Crypto_Whitepaper_UA_PROTOCOL.pdf",
            "docs/whitepaper/Marma_Crypto_Whitepaper_EN_PROTOCOL.pdf"
          ];
          const postAttackLoads = [];
          for (const relPath of artifactFiles) {{
            simulateTamperAttack(); // put into tampered state first!
            if (!elems.statusBanner.className.includes("err")) {{
              throw new Error("Expected err state before loading " + relPath);
            }}
            const fullPath = {json.dumps(str(REPO_ROOT))} + "/" + relPath;
            const buf = fs.readFileSync(fullPath);
            const seal = extractMarmaSealFromBytes(new Uint8Array(buf), relPath);
            renderVerificationState(seal, relPath, false);
            postAttackLoads.push({{
              file: relPath,
              banner: elems.statusBanner.className,
              btn: elems.btnSimulateAttack.textContent,
              errors: elems.valErrors.textContent,
              tsp: elems.valStandard ? elems.valStandard.textContent : ""
            }});
          }}

          return {{ states, btnEnAttack, btnUkAttack, postAttackLoads, defaultLang: currentLang }};
        """)

        self.assertEqual(res["defaultLang"], "en")
        self.assertEqual(res["states"][0]["banner"], "status-banner ok")
        self.assertEqual(res["states"][1]["banner"], "status-banner err")
        self.assertIn("Reset Attack", res["states"][1]["btn"])
        self.assertIn("Reset Attack", res["btnEnAttack"])
        self.assertIn("Скинути атаку", res["btnUkAttack"])
        self.assertEqual(res["states"][2]["banner"], "status-banner ok")
        self.assertEqual(
            res["states"][2]["errors"],
            "Δ_sym = 0.000000000000  |  Δ_coord = 0.000000000000",
        )

        for item in res["postAttackLoads"]:
            self.assertEqual(item["banner"], "status-banner ok", f"Failed post-attack load on {item['file']}")
            self.assertEqual(
                item["errors"],
                "Δ_sym = 0.000000000000  |  Δ_coord = 0.000000000000",
                f"Non-zero error on {item['file']}",
            )
            self.assertIn("Simulate Attack", item["btn"])
            self.assertIn("2026-10-17 03:20:22 UTC", item["tsp"])

    def test_07_production_whitepapers_pades_lta_and_manifests_audit(self) -> None:
        """Cross-audit production Whitepapers, PAdES-LTA containers, SHA256SUMS.txt, and directory sync."""
        wp_dir = REPO_ROOT / "whitepaper"
        docs_wp_dir = REPO_ROOT / "docs" / "whitepaper"

        # 1. Verify SHA256SUMS.txt matches actual files
        sha_lines = (wp_dir / "SHA256SUMS.txt").read_text(encoding="utf-8").strip().splitlines()
        self.assertGreaterEqual(len(sha_lines), 6)
        for line in sha_lines:
            expected_sha, fname = line.split()
            actual_sha = hashlib.sha256((wp_dir / fname).read_bytes()).hexdigest()
            self.assertEqual(expected_sha, actual_sha, f"SHA256SUMS mismatch for {fname}")

        # 2. Verify docs/whitepaper copies are byte-for-byte identical to whitepaper/
        for shared_name in [
            "Marma_Crypto_Whitepaper_UA.pdf",
            "Marma_Crypto_Whitepaper_EN.pdf",
            "Marma_Crypto_Whitepaper_UA_PROTOCOL.pdf",
            "Marma_Crypto_Whitepaper_EN_PROTOCOL.pdf",
            "sri_yantra_whitepaper_diagram.svg",
            "sri_yantra_whitepaper_diagram.svg.p7s",
            "AUTHORSHIP_MANIFEST.txt",
        ]:
            h1 = hashlib.sha256((wp_dir / shared_name).read_bytes()).hexdigest()
            h2 = hashlib.sha256((docs_wp_dir / shared_name).read_bytes()).hexdigest()
            self.assertEqual(h1, h2, f"Drift between whitepaper/{shared_name} and docs/whitepaper/{shared_name}")

        # 3. Verify PAdES-LTA and DSTU 4145-2002 EC signatures on both Whitepaper PDFs
        for pdf_name in ("Marma_Crypto_Whitepaper_UA.pdf", "Marma_Crypto_Whitepaper_EN.pdf"):
            res = mw.verify_pdf_document(wp_dir / pdf_name)
            self.assertTrue(res["verified"], f"{pdf_name} failed verification")
            self.assertTrue(res["dstu4145_verified"])
            self.assertTrue(res["dstu4145_ec_verified"])
            self.assertTrue(res["pades_cades_verified"])
            self.assertTrue(res["hmac_match"])
            self.assertTrue(res["public_seal_match"])
            self.assertEqual(res["max_coordinate_signature_drift"], 0.0)
            self.assertEqual(res["max_bilateral_symmetry_error"], 0.0)
            self.assertEqual(res["signer_info"]["rnokpp"], "3255419579")
            qes_rep = res["qes_container_report"]
            self.assertEqual(qes_rep["signature_level"], "PAdES-LTA")
            self.assertTrue(qes_rep["has_tsp"])
            self.assertTrue(qes_rep["has_ltv"])
            self.assertTrue(qes_rep["has_ocsp"])
            self.assertTrue(qes_rep["has_pdf_dss"])
            self.assertTrue(qes_rep["is_valid_at_signing"])

        # 4. Verify verify_any_file resolves .typ -> .pdf and .svg.p7s -> .svg
        res_typ = mw.verify_any_file(wp_dir / "Marma_Crypto_Whitepaper_EN.typ")
        self.assertTrue(res_typ["verified"])
        res_p7s = mw.verify_any_file(wp_dir / "sri_yantra_whitepaper_diagram.svg.p7s")
        self.assertTrue(res_p7s["verified"])
        self.assertTrue(res_p7s["pades_cades_verified"])

    def test_08_cryptographic_commitment_and_edge_case_rejections(self) -> None:
        """Verify rejection of public_seal_digest tamper, r||s binding tamper, and unsigned/corrupted files."""
        with tempfile.TemporaryDirectory(prefix="marma_edge_") as tmp:
            tmp_dir = Path(tmp)
            svg_p = tmp_dir / "signed.svg"
            mw.sign_sri_yantra_svg("EDGE-CASE-PAYLOAD", mw.DEFAULT_SECRET, svg_p)
            svg_txt = svg_p.read_text(encoding="utf-8")

            # 1. Tamper data-public-seal in SVG while keeping all coordinates & HMAC intact
            bad_pseal_svg = svg_txt.replace('data-public-seal="', 'data-public-seal="0000', 1)
            bad_pseal_svg = bad_pseal_svg.replace('0000' + svg_txt.split('data-public-seal="')[1][:64], "0" * 64, 1)
            py_bad_pseal = mw.verify_sri_yantra_svg(bad_pseal_svg)
            self.assertFalse(py_bad_pseal["verified"])
            self.assertFalse(py_bad_pseal["public_seal_match"])

            # 2. Tamper r||s binding and public_seal_digest in Browser JS
            js_edge = run_browser_js_harness(f"""
              const buf = fs.readFileSync({json.dumps(str(svg_p))});
              const seal = extractMarmaSealFromBytes(new Uint8Array(buf), "signed.svg");

              // Tamper public_seal_digest
              const badSeal = JSON.parse(JSON.stringify(seal));
              badSeal.public_seal_digest = "f".repeat(64);
              renderVerificationState(badSeal, "bad_pseal.svg", true);
              const psealRejected = elems.statusBanner.className.includes("err");

              // Tamper dstu4145.r_hex (breaks SHA256(r||s) == hmac_sha256)
              const badRS = JSON.parse(JSON.stringify(seal));
              badRS.dstu4145.r_hex = "1".repeat(64);
              renderVerificationState(badRS, "bad_rs.svg", true);
              const rsRejected = elems.statusBanner.className.includes("err");

              // Tamper payload (breaks SHA256(payload) == content_sha256)
              const badPay = JSON.parse(JSON.stringify(seal));
              badPay.payload = "FORGED-PAYLOAD";
              renderVerificationState(badPay, "bad_pay.svg", true);
              const payRejected = elems.statusBanner.className.includes("err");

              return {{ psealRejected, rsRejected, payRejected }};
            """)
            self.assertTrue(js_edge["psealRejected"])
            self.assertTrue(js_edge["rsRejected"])
            self.assertTrue(js_edge["payRejected"])

            # 3. Unsigned PDF and DOCX must be cleanly rejected
            un_pdf = tmp_dir / "unsigned.pdf"
            d = pymupdf.open()
            d.new_page().insert_text((72, 72), "Unsigned PDF")
            d.save(str(un_pdf))
            d.close()
            self.assertFalse(mw.verify_pdf_document(un_pdf)["verified"])

            un_docx = tmp_dir / "unsigned.docx"
            w = docx.Document()
            w.add_paragraph("Unsigned DOCX")
            w.save(str(un_docx))
            self.assertFalse(mw.verify_docx_document(un_docx)["verified"])

    def test_09_official_ukrainian_iit_euscp_czo_verification_and_tsp_timestamp(self) -> None:
        """Directly verify Whitepapers & SVG with official Ukrainian IIT euscp.so + pdfs.so (czo.gov.ua/verify engine)."""
        iit_lib = Path("/opt/iit/eu/sw/euscp.so")
        if not iit_lib.exists():
            self.skipTest("/opt/iit/eu/sw/euscp.so not installed")

        code = f"""
import ctypes, json, sys
sys.path.insert(0, '/home/attor/legaltech/packages/qes-tools/src')
from token_bridge import load_euscp_lib, init_eusign

class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", ctypes.c_ushort),
        ("wMonth", ctypes.c_ushort),
        ("wDayOfWeek", ctypes.c_ushort),
        ("wDay", ctypes.c_ushort),
        ("wHour", ctypes.c_ushort),
        ("wMinute", ctypes.c_ushort),
        ("wSecond", ctypes.c_ushort),
        ("wMilliseconds", ctypes.c_ushort),
    ]

class EU_TIME_INFO(ctypes.Structure):
    _fields_ = [
        ("dwVersion", ctypes.c_ulong),
        ("bTimeAvail", ctypes.c_int),
        ("bTimeStamp", ctypes.c_int),
        ("Time", SYSTEMTIME),
        ("bSignTimeStampAvail", ctypes.c_int),
        ("SignTimeStamp", SYSTEMTIME),
    ]

lib = load_euscp_lib()
init_eusign(lib)
lib.EUSetUIMode(False)

out = {{}}
for name in ["Marma_Crypto_Whitepaper_EN.pdf", "Marma_Crypto_Whitepaper_UA.pdf"]:
    data = open({json.dumps(str(REPO_ROOT / "whitepaper"))} + "/" + name, "rb").read()
    buf = ctypes.create_string_buffer(data, len(data))
    cnt = ctypes.c_uint32(0)
    rv_cnt = lib.EUPDFGetSignsCount(buf, len(data), ctypes.byref(cnt))
    info_buf = ctypes.create_string_buffer(512)
    rv_ver = lib.EUPDFVerifyData(0, buf, len(data), info_buf)
    p_time = ctypes.POINTER(EU_TIME_INFO)()
    rv_time = lib.EUPDFGetSignTimeInfo(0, buf, len(data), ctypes.byref(p_time))
    st = ctypes.c_uint32(0)
    rv_type = lib.EUPDFGetSignType(0, buf, len(data), ctypes.byref(st))
    out[name] = {{
        "rv_cnt": rv_cnt,
        "count": cnt.value,
        "rv_ver": rv_ver,
        "rv_time": rv_time,
        "bTimeAvail": p_time.contents.bTimeAvail if rv_time == 0 else 0,
        "bTimeStamp": p_time.contents.bTimeStamp if rv_time == 0 else 0,
        "year": p_time.contents.Time.wYear if rv_time == 0 else 0,
        "sign_type": st.value,
    }}

svg_b = open({json.dumps(str(REPO_ROOT / "whitepaper/sri_yantra_whitepaper_diagram.svg"))}, "rb").read()
p7s_b = open({json.dumps(str(REPO_ROOT / "whitepaper/sri_yantra_whitepaper_diagram.svg.p7s"))}, "rb").read()
s_info_buf = ctypes.create_string_buffer(512)
rv_svg = lib.EUVerifyDataSpecific(
    ctypes.create_string_buffer(svg_b, len(svg_b)), len(svg_b),
    0,
    None,
    ctypes.create_string_buffer(p7s_b, len(p7s_b)), len(p7s_b),
    s_info_buf
)
out["svg_p7s_rv"] = rv_svg
print(json.dumps(out))
"""
        import os
        env = {**os.environ, "LD_LIBRARY_PATH": "/opt/iit/eu/sw"}
        proc = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True)
        res = json.loads(proc.stdout.strip().splitlines()[-1])
        for pdf_name in ("Marma_Crypto_Whitepaper_EN.pdf", "Marma_Crypto_Whitepaper_UA.pdf"):
            r = res[pdf_name]
            self.assertEqual(r["rv_cnt"], 0)
            self.assertEqual(r["count"], 1, f"czo.gov.ua/verify EUPDFGetSignsCount != 1 for {pdf_name}")
            self.assertEqual(r["rv_ver"], 0, f"czo.gov.ua/verify EUPDFVerifyData != 0 for {pdf_name}")
            self.assertEqual(r["rv_time"], 0)
            self.assertEqual(r["bTimeAvail"], 1)
            self.assertEqual(r["bTimeStamp"], 1)
            self.assertEqual(r["year"], 2026)
            self.assertEqual(r["sign_type"], 0x10)  # CAdES-X-Long / PAdES-LTA
        self.assertEqual(res["svg_p7s_rv"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)




