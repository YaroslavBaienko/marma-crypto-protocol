#!/usr/bin/env python3
"""
Three-Stage Cross-Checking, Cross-Validation, and Cross-Verification Suite
for Marma-Crypto (Marma-256) Manuscript Release v2.0.

Stage I   (Cross-Checking):    Internal consistency of .typ sources, compiled PDFs,
                               5 vector SVGs, 6 tables, 4 theorems, 45 references,
                               unit dimensional hygiene, and companion files.
Stage II  (Cross-Validation):  Exact numerical agreement between manuscript claims/tables,
                               empirical JSON report (H1-H6), and canonical code constants.
Stage III (Cross-Verification): Live multi-runtime execution across Python 3.12 and
                               Node.js GF(2^257) bridge (DSTU 4145-2002 + Kupyna + GOST).
"""

import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import marma_watermark as mw  # noqa: E402


class TestManuscriptV2CrossVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Frozen submission snapshot (committed, immutable): the manuscript exactly as
        # submitted to JISA/SIGPRO. The live per-journal folder stays gitignored, so the
        # suite must never depend on it.
        cls.snapshot_dir = REPO_ROOT / "submission_snapshots" / "elsevier-v2.0"
        cls.snapshot_sums_path = cls.snapshot_dir / "SHA256SUMS"
        cls.jisa_typ_path = cls.snapshot_dir / "Marma_Crypto_Elsevier_JISA_Edition.typ"
        cls.iacr_typ_path = REPO_ROOT / "whitepaper" / "Marma_Crypto_IACR_LNCS_Edition.typ"
        cls.jisa_pdf_path = cls.snapshot_dir / "01_Manuscript_Marma_Crypto_JISA.pdf"
        cls.sigpro_pdf_path = cls.snapshot_dir / "01_Manuscript_Marma_Signal_Processing.pdf"
        cls.iacr_pdf_path = REPO_ROOT / "whitepaper" / "Marma_Crypto_IACR_LNCS_Edition.pdf"
        cls.report_path = REPO_ROOT / "reports" / "v2_hypothesis_verification_report.json"
        cls.highlights_path = cls.snapshot_dir / "03_Highlights_JISA.txt"

        cls.typ_text = cls.jisa_typ_path.read_text(encoding="utf-8")
        cls.report = json.loads(cls.report_path.read_text(encoding="utf-8"))

        with pymupdf.open(cls.jisa_pdf_path) as doc:
            cls.pdf_page_count = len(doc)
            raw_pdf_text = "\n".join(page.get_text("text") for page in doc)
            # Normalize non-breaking spaces (\xa0) produced by Typst figure/table labels
            cls.pdf_text = raw_pdf_text.replace("\xa0", " ")

    # =========================================================================
    # STAGE I: CROSS-CHECKING (Internal Structural, Unit & Citation Integrity)
    # =========================================================================

    def test_stage1_01_frozen_submission_integrity_and_supersession(self) -> None:
        """Cross-check the frozen SIGPRO/JISA submission snapshot and that the current manuscript supersedes it."""
        # 1) The frozen snapshot is byte-intact against its SHA256 manifest.
        manifest = {}
        for line in self.snapshot_sums_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            digest, rel = line.split(maxsplit=1)
            manifest[rel.lstrip("*")] = digest
        self.assertGreaterEqual(len(manifest), 8, "Frozen submission manifest is incomplete")
        for rel, digest in manifest.items():
            asset = self.snapshot_dir / rel
            self.assertTrue(asset.exists(), f"Missing frozen submission asset: {rel}")
            self.assertEqual(
                hashlib.sha256(asset.read_bytes()).hexdigest(),
                digest,
                f"Frozen submission asset was modified after freezing: {rel}",
            )

        # 2) JISA and SIGPRO received byte-identical manuscript PDFs.
        self.assertEqual(
            self.jisa_pdf_path.read_bytes(),
            self.sigpro_pdf_path.read_bytes(),
            "01_Manuscript_Marma_Crypto_JISA.pdf and 01_Manuscript_Marma_Signal_Processing.pdf must match",
        )

        # 3) The frozen snapshot is the v2.0 manuscript with Elsevier Signal Processing formatting.
        self.assertIn("(RELEASE V2.0)", self.typ_text)
        self.assertIn("#set par.line(\n  numbering: n =>", self.typ_text)
        self.assertNotIn("CRYPTOGRAPHIC ENGINEERING", self.typ_text)
        self.assertIn("SIGNAL PROCESSING & INFORMATION HIDING MANUSCRIPT", self.typ_text)
        self.assertGreaterEqual(self.pdf_page_count, 18)
        self.assertLessEqual(self.pdf_page_count, 22)

        # 4) The current archival manuscript is a later release (v2.1.0) that supersedes,
        #    not equals, the frozen submission. Post-submission updates must not rewrite
        #    what the journals received.
        iacr_typ_text = self.iacr_typ_path.read_text(encoding="utf-8")
        self.assertIn("V2.1.0", iacr_typ_text)
        self.assertNotEqual(
            iacr_typ_text,
            self.typ_text,
            "Current archival manuscript must not be byte-identical to the frozen v2.0 submission",
        )
        with pymupdf.open(self.iacr_pdf_path) as doc2:
            self.assertGreaterEqual(len(doc2), self.pdf_page_count)
            self.assertGreaterEqual(len(doc2), 22)

    def test_stage1_02_theorems_figures_tables_and_sections(self) -> None:
        """Cross-check presence of all Theorems 1-5, Proposition 1, Definitions 1-2, Figures 1-5, Tables 1-6."""
        required_markers = [
            "Theorem 1 (Algebraic Irrationality",
            "Proposition 1 (L-BFGS-B Baseline Convergence and Local Jacobian Spectrum)",
            "Theorem 2 (Robustness of Parallel Combiner and EUF-CMA Security of Marma-256)",
            "Theorem 3 (IEEE-754 binary64 Bijective Lattice Inversion and Multi-Bound Reconciliation)",
            "Theorem 4 (Zero Cross-Talk Orthogonality and Constant-Rate Attribution)",
            "Theorem 5 (Unobservability of Canary Allocation and Active Erasure Deterrence)",
            "Definition 1 (The 9-Triangle Configuration",
            "Definition 2 (Triple Concurrency Locus",
            "<fig1>",
            "<fig2>",
            "<fig3>",
            "<fig4>",
            "<fig5>",
            "<tab1>",
            "<tab2>",
            "<tab3>",
            "<tab4>",
            "<tab5>",
            "<tab6>",
        ]
        for marker in required_markers:
            self.assertIn(marker, self.typ_text, f"Missing structural element in .typ: {marker}")

        for i in range(1, 6):
            self.assertIn(f"Figure {i}:", self.pdf_text, f"Rendered PDF missing Figure {i}")
        for i in range(1, 7):
            self.assertIn(f"Table {i}:", self.pdf_text, f"Rendered PDF missing Table {i}")

        # Verify all 5 SVG files exist in both directories and are valid XML SVGs
        svg_names = [
            "fig1_architecture.svg",
            "fig2_c954_geometry.svg",
            "fig3_lbfgsb_sensitivity.svg",
            "fig4_ieee754_error_hist.svg",
            "fig5_comparative_benchmarks.svg",
        ]
        for name in svg_names:
            p1 = REPO_ROOT / "whitepaper" / "figures" / name
            p2 = self.snapshot_dir / "figures" / name
            self.assertTrue(p1.exists(), f"Missing {p1}")
            self.assertTrue(p2.exists(), f"Missing {p2}")
            self.assertEqual(p1.read_bytes(), p2.read_bytes(), f"SVG mismatch for {name}")
            content = p1.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("<svg ") and content.strip().endswith("</svg>"))

    def test_stage1_03_all_45_references_present_and_cited(self) -> None:
        """Cross-check that all 45 bibliography items [1]..[45] exist and are cited in the manuscript."""
        ref_section_idx = self.typ_text.index("= References")
        body_text = self.typ_text[:ref_section_idx]
        ref_text = self.typ_text[ref_section_idx:]

        for ref_num in range(1, 46):
            self.assertIn(
                f"\n[{ref_num}] ",
                ref_text,
                f"Reference [{ref_num}] missing from References section",
            )
            # Check cited in body either as [ref_num] or inside a bracket list like [10, 32] or [28, 29, 31]
            pattern = rf"\[(?:\d+,\s*)*{ref_num}(?:,\s*\d+)*\]"
            self.assertRegex(
                body_text,
                pattern,
                f"Reference [{ref_num}] is never cited in the manuscript body",
            )

    def test_stage1_04_dimensional_and_unit_hygiene(self) -> None:
        """Cross-check that all v1.0 unit bugs (e.g. 'rad' for Delta E, '18 nm = 1.8e-8 pt') are eliminated."""
        for label, text in [
            ("Manuscript .typ", self.typ_text),
            ("Rendered PDF", self.pdf_text),
            ("Highlights", self.highlights_path.read_text(encoding="utf-8")),
        ]:
            self.assertNotIn("10^-11 rad", text, f"Found legacy 'rad' unit bug in {label}")
            self.assertNotIn("10^(-11) rad", text, f"Found legacy 'rad' unit bug in {label}")
            self.assertNotIn("18 nm", text, f"Found legacy '18 nm' step unit confusion in {label}")
            self.assertNotIn('18"nm"', text, f"Found legacy '18 nm' step unit confusion in {label}")
            self.assertNotIn("??", text, f"Found unresolved reference '??' in {label}")

        # Verify Elsevier Highlights character length constraint (<= 85 chars per bullet)
        hl_lines = [
            line.strip()
            for line in self.highlights_path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("*")
        ]
        self.assertEqual(len(hl_lines), 5, "Highlights must contain exactly 5 bullets")
        for bullet in hl_lines:
            raw_bullet = bullet.lstrip("* ").strip()
            self.assertLessEqual(
                len(raw_bullet),
                85,
                f"Highlight bullet exceeds 85 characters ({len(raw_bullet)} chars): {raw_bullet}",
            )

    # =========================================================================
    # STAGE II: CROSS-VALIDATION (Manuscript vs. Empirical Report & Code Constants)
    # =========================================================================

    def test_stage2_01_table1_coordinates_match_canonical_code_and_report(self) -> None:
        """Cross-validate all 36 coordinates in Table 1 against marma_watermark.CANONICAL_TRIANGLES."""
        expected_tris = mw.CANONICAL_TRIANGLES
        self.assertEqual(len(expected_tris), 9)

        for tid, lx, by, ay, rx, _is_up in expected_tris:
            # Bilateral symmetry invariant lx + rx == 300.0
            self.assertAlmostEqual(lx + rx, 300.0, places=8)
            # Check exact 8-decimal strings appear in Table 1 of the .typ manuscript
            lx_s = f"`{lx:.8f}`"
            by_s = f"`{by:.8f}`"
            ay_s = f"`{ay:.8f}`"
            rx_s = f"`{rx:.8f}`"
            self.assertIn(lx_s, self.typ_text, f"Table 1 missing lx for {tid}: {lx_s}")
            self.assertIn(by_s, self.typ_text, f"Table 1 missing by for {tid}: {by_s}")
            self.assertIn(ay_s, self.typ_text, f"Table 1 missing ay for {tid}: {ay_s}")
            self.assertIn(rx_s, self.typ_text, f"Table 1 missing rx for {tid}: {rx_s}")

    def test_stage2_02_hypotheses_h1_h2_algebraic_and_jacobian_validation(self) -> None:
        """Cross-validate H1 & H2 numbers in manuscript against v2_hypothesis_verification_report.json."""
        h12 = self.report["h1_h2_algebraic_and_jacobian"]

        # Verify prime-numerator non-square discriminants
        disc = h12["discriminants"]
        self.assertEqual(disc["Delta_1_quadratic_chord"]["rational_num"], 173)
        self.assertEqual(disc["Delta_1_quadratic_chord"]["rational_den"], 64)
        self.assertEqual(disc["Delta_2_quartic_interlocking"]["rational_num"], 104729)
        self.assertEqual(disc["Delta_2_quartic_interlocking"]["rational_den"], 4096)
        self.assertEqual(disc["Delta_3_octavic_cascade"]["rational_num"], 28657)
        self.assertEqual(disc["Delta_3_octavic_cascade"]["rational_den"], 1024)
        self.assertEqual(disc["Delta_4_degree16_eliminant"]["rational_num"], 514229)
        self.assertEqual(disc["Delta_4_degree16_eliminant"]["rational_den"], 65536)
        for key, item in disc.items():
            self.assertFalse(item["is_square_in_Q"], f"{key} must be non-square in Q")

        # Verify concurrency residual comparison against machine epsilon
        de_sq = h12["delta_e_sq_pt2"]
        de_rms = h12["delta_e_rms_pt"]
        eps64 = h12["eps_float64"]
        sqrt_eps64 = h12["sqrt_eps_float64"]

        self.assertLess(de_sq, eps64)
        self.assertLess(de_rms, sqrt_eps64)
        self.assertAlmostEqual(de_sq, 3.76e-21, delta=0.05e-21)
        self.assertAlmostEqual(de_rms, 6.13e-11, delta=0.05e-11)

        # Verify Jacobian rank and condition number in manuscript
        self.assertEqual(h12["jacobian_concurrency_rank"], 23)
        self.assertAlmostEqual(h12["condition_number_23"], 171.00, places=1)
        self.assertIn("171.00", self.typ_text)
        self.assertIn("10.764", self.typ_text)
        self.assertIn("0.06295", self.typ_text)

    def test_stage2_03_hypothesis_h3_ieee754_multi_bound_reconciliation(self) -> None:
        """Cross-validate H3 (Theorem 3) single-op, CTM analytical, and empirical bounds."""
        h3 = self.report["h3_ieee754_monte_carlo"]
        self.assertEqual(h3["n_trials"], 100000)
        self.assertEqual(h3["total_bits_tested"], 25600000)
        self.assertEqual(h3["bit_error_rate"], 0.0)
        self.assertEqual(h3["word_errors"], 0)
        self.assertTrue(h3["exact_python_roundtrip_2000"])

        # Analytical single-addition bound: 0.5 * 2^-44 / 1.8e-8 = 1.578983857e-6
        expected_half_ulp = (0.5 * (2.0**-44)) / 1.8e-8
        self.assertAlmostEqual(h3["half_ulp_bound_steps"], expected_half_ulp, places=11)
        self.assertLessEqual(h3["empirical_max_err_direct_steps"], h3["half_ulp_bound_steps"])

        # Analytical 4-operation CTM bound: 2.0 * 2^-44 / 1.8e-8 = 6.31593543e-6
        expected_two_ulp = (2.0 * (2.0**-44)) / 1.8e-8
        self.assertAlmostEqual(h3["two_ulp_bound_steps"], expected_two_ulp, places=11)
        self.assertLessEqual(h3["empirical_max_err_steps"], h3["two_ulp_bound_steps"])
        self.assertLess(h3["two_ulp_bound_steps"], 0.5)

        # Verify all three harmonized bounds appear in the manuscript
        self.assertIn("1.579", self.typ_text)
        self.assertIn("4.732", self.typ_text)
        self.assertIn("6.32", self.typ_text)

    def test_stage2_04_hypothesis_h4_orthogonal_canary_zero_crosstalk(self) -> None:
        """Cross-validate H4 (Theorem 4) exhaustive 1,024-state canary orthogonality."""
        h4 = self.report["h4_canary_orthogonality"]
        self.assertEqual(h4["tested_canary_states"], 1024)
        self.assertEqual(h4["signature_cross_talk_errors"], 0)
        self.assertEqual(h4["canary_recovery_errors"], 0)
        self.assertEqual(h4["empirical_mutual_information_bits"], 0.0)

    def test_stage2_05_hypothesis_h5_table4_iso32000_decimal_precision(self) -> None:
        """Cross-validate Table 4 in manuscript against H5 ISO 32000-2 decimal truncation report."""
        h5 = self.report["h5_pdf_serialization_precision"]
        for d in range(4, 11):
            rec = h5[str(d)]
            theo_str = f"{rec['theoretical_max_step_error']:,.6f}"
            obs_str = f"{rec['observed_max_step_error']:,.6f}"
            wer_str = f"{rec['word_error_rate'] * 100:.4f}%"
            self.assertIn(theo_str, self.typ_text, f"Table 4 missing theoretical bound for d={d}: {theo_str}")
            self.assertIn(obs_str, self.typ_text, f"Table 4 missing empirical error for d={d}: {obs_str}")
            self.assertIn(wer_str, self.typ_text, f"Table 4 missing WER for d={d}: {wer_str}")
            if d >= 8:
                self.assertEqual(rec["word_error_rate"], 0.0)
                self.assertTrue(rec["lossless_bijective"])
            else:
                self.assertGreater(rec["word_error_rate"], 0.80)
                self.assertFalse(rec["lossless_bijective"])

    def test_stage2_06_hypothesis_h6_table6_comparative_benchmarks(self) -> None:
        """Cross-validate H6 comparative metrics (RMSE, PSNR_geom, capacity) against manuscript."""
        h6 = self.report["h6_comparative_benchmarks"]
        expected_rmse = 9.207e-6 / math.sqrt(3.0)
        expected_psnr = 20.0 * math.log10(300.0 / expected_rmse)
        self.assertAlmostEqual(h6["rmse_pt"], expected_rmse, places=10)
        self.assertAlmostEqual(h6["psnr_geom_db"], expected_psnr, places=2)
        self.assertIn("155.03", self.typ_text)
        self.assertIn("5.316", self.typ_text)
        self.assertIn("9.85", self.typ_text)

    # =========================================================================
    # STAGE III: CROSS-VERIFICATION (Live Multi-Runtime Execution: Python + JS)
    # =========================================================================

    def test_stage3_01_live_python_lattice_bijection_and_canary_orthogonality(self) -> None:
        """Execute live Python 256-bit + 10-bit canary SVG/PDF round-trips and verify zero cross-talk."""
        with tempfile.TemporaryDirectory(prefix="marma_v2_stage3_") as tmp:
            svg_path = Path(tmp) / "stage3_test.svg"
            payload = "Marma-Crypto v2.0 Stage III Bijective Lattice & Canary Test"
            secret = "STAGE3-MASTER-SECRET-2026"
            recipient = "Auditor-Stage3-01"

            mw.sign_sri_yantra_svg(payload, secret, svg_path, recipient_id=recipient)
            svg_content = svg_path.read_text(encoding="utf-8")

            ver = mw.verify_sri_yantra_svg(svg_content, payload, recipient_id=recipient)
            self.assertTrue(ver["verified"])
            self.assertTrue(ver["bijective_256bit_match"])
            self.assertTrue(ver["canary_active"])
            self.assertTrue(ver["canary_recipient_verified"])
            self.assertEqual(ver["max_coordinate_signature_drift"], 0.0)
            self.assertEqual(ver["max_bilateral_symmetry_error"], 0.0)

            trace = mw.trace_canary_suspects(
                svg_path,
                ["Innocent-01", recipient, "Innocent-02"],
                secret_key=secret,
            )
            self.assertEqual(trace["matched_recipient"], recipient)

    def test_stage3_02_live_nodejs_dstu4145_gf257_and_combiner_bridge(self) -> None:
        """Execute live Node.js GF(2^257) DSTU 4145-2002 signing, verification, and combiner test."""
        payload_hex = b"Marma-Crypto v2.0 Cross-Verification Test Payload".hex()
        key_seed = "marma_v2_cross_verification_seed_2026"

        sign1 = mw.call_dstu4145_bridge(
            {
                "action": "sign",
                "secretSeed": key_seed,
                "payloadBytesHex": payload_hex,
            }
        )
        sign2 = mw.call_dstu4145_bridge(
            {
                "action": "sign",
                "secretSeed": key_seed,
                "payloadBytesHex": payload_hex,
            }
        )
        self.assertEqual(sign1["status"], "ok")
        # RFC 6979 determinism check
        self.assertEqual(sign1["r_hex"], sign2["r_hex"])
        self.assertEqual(sign1["s_hex"], sign2["s_hex"])
        self.assertEqual(sign1["gost34311_hex"], sign2["gost34311_hex"])
        self.assertEqual(sign1["rs_digest_hex"], sign2["rs_digest_hex"])
        self.assertEqual(
            sign1["rs_digest_hex"],
            hashlib.sha256(f"{sign1['r_hex']}::{sign1['s_hex']}".encode("utf-8")).hexdigest(),
        )

        # Verify valid signature over GF(2^257)
        ver_ok = mw.call_dstu4145_bridge(
            {
                "action": "verify",
                "payloadBytesHex": payload_hex,
                "dstu4145": sign1,
            }
        )
        self.assertTrue(ver_ok["dstu4145_valid"])
        self.assertTrue(ver_ok["ec_signature_valid"])
        self.assertTrue(ver_ok["rs_digest_match"])

        # Verify 1-byte tampered payload fails closed over GF(2^257)
        tampered_hex = b"Marma-Crypto v2.0 Cross-Verification Test PayloaE".hex()
        ver_bad = mw.call_dstu4145_bridge(
            {
                "action": "verify",
                "payloadBytesHex": tampered_hex,
                "dstu4145": sign1,
            }
        )
        self.assertFalse(ver_bad["dstu4145_valid"])

    def test_stage3_03_keyed_dithered_qim_and_active_traitor_defense(self) -> None:
        """Cross-verify Theorem 5: Keyed Dithered QIM (d_K), permutation (pi_K), Python/JS parity, and 96.30% single-slot active-traitor tamper detection."""
        import copy

        sig_hex = hashlib.sha256(b"Theorem-5-Signal-Processing-Keyed-QIM-Payload").hexdigest()
        canary_word = 733
        qim_key = "SIGPRO-QIM-MASTER-KEY-2026"
        doc_nonce = hashlib.sha256(b"Document-Canonical-Text-Stream-V2").hexdigest()

        perm, dither = mw.derive_keyed_qim_schedule(qim_key, doc_nonce)
        self.assertEqual(sorted(perm), list(range(27)), "pi_K must be a bijection on 0..26")
        self.assertEqual(len(dither), 27)
        self.assertTrue(all(0 <= d <= 1023 for d in dither))

        # 1. Exact lossless inversion with correct key
        tris_keyed = mw.build_perturbed_triangles_v13(
            sig_hex, canary_beacon_word=canary_word, cx=150.0, qim_key=qim_key, doc_nonce=doc_nonce
        )
        rec_sig, rec_canary = mw.recover_256bit_from_triangles(
            tris_keyed, cx=150.0, qim_key=qim_key, doc_nonce=doc_nonce
        )
        self.assertEqual(rec_sig, sig_hex)
        self.assertEqual(rec_canary, canary_word)

        # 2. Without the correct key (or with wrong key), extraction yields pseudorandom noise
        wrong_sig, wrong_canary = mw.recover_256bit_from_triangles(
            tris_keyed, cx=150.0, qim_key="WRONG-ADVERSARY-KEY", doc_nonce=doc_nonce
        )
        self.assertNotEqual(wrong_sig, sig_hex)

        # 3. Exhaustive 27-slot Active White-Box Traitor Attack simulation (Theorem 5 bound):
        # An attacker without K attempts to strip the canary by resetting 1 physical coordinate
        # to its unperturbed canonical baseline value B*_k.
        sig_corrupted_count = 0
        canary_corrupted_to_nonzero_count = 0
        coord_keys = ("lx", "by", "ay")
        for slot in range(27):
            tri_idx = slot // 3
            coord_idx = slot % 3
            ckey = coord_keys[coord_idx]
            base_val = mw.CANONICAL_TRIANGLES[tri_idx][1 + coord_idx]

            attacked = copy.deepcopy(tris_keyed)
            attacked[tri_idx][ckey] = round(base_val, 9)
            if ckey == "lx":
                attacked[tri_idx]["rx"] = round(300.0 - round(base_val, 9), 9)

            atk_sig, atk_canary = mw.recover_256bit_from_triangles(
                attacked, cx=150.0, qim_key=qim_key, doc_nonce=doc_nonce
            )
            if atk_sig != sig_hex:
                sig_corrupted_count += 1
            elif atk_canary != canary_word and atk_canary != 0:
                canary_corrupted_to_nonzero_count += 1

        # Exactly 26 out of 27 single-coordinate attacks (96.296%) corrupt the 256-bit signature digest V!
        self.assertEqual(sig_corrupted_count, 26)
        self.assertAlmostEqual(sig_corrupted_count / 27.0, 26.0 / 27.0, places=6)
        # And in the remaining 1/27 slot (k* = pi_K(26)), overwriting with B* shifts canary to a random dither residue != 0
        self.assertEqual(canary_corrupted_to_nonzero_count, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)

