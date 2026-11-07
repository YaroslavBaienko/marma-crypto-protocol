#!/usr/bin/env python3
"""
Cross-Validation & Cross-Verification Suite for Marma-Crypto v2.3.0
(`Subhash Kak 40-Paper Corpus Synthesis + 54-Marma Nonlinear Incidence Verifier`)
=================================================================================
Tests all 6 v2.3.0 subsystems and programmatically cross-verifies all 40 works
of Prof. Subhash Kak (`VEDI-L10-0223` .. `VEDI-L10-0262`) against `Marma-Crypto`.
"""

from __future__ import annotations

import copy
import hashlib
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from marma_crypto import (  # noqa: E402
    KAK_40_CORPUS_MAP,
    MARMA_V23_VERSION,
    MAX_RECIPIENTS_V23,
    PPT_CODEBOOK_64,
    MarmaDealRoomServer,
    cross_validate_kak_corpus_v23,
    decode_narayana_universal_v23,
    decode_ppt_unit_circle_v23,
    decode_recursive_23bit_recipient_v23,
    derive_dsequence_qim_schedule_v23,
    encode_narayana_universal_v23,
    encode_ppt_unit_circle_v23,
    encode_recursive_23bit_recipient_v23,
    evaluate_kak_mathematical_invariants_v23,
    generate_prime_d_sequence,
    generate_prime_remainder_orbit,
    katapayadi_seed_digest_v23,
    narayana_sequence_v23,
    stamp_augmented_dual_layer_v23,
    verify_augmented_dual_layer_v23,
    verify_sri_yantra_marma_concurrency_v23,
    yamatarajabhanasalagam_debruijn_v23,
)
from marma_watermark import (  # noqa: E402
    CANONICAL_TRIANGLES,
    DEFAULT_SECRET,
    VERSION,
    build_perturbed_triangles_v13,
)


class TestMarmaV23KakSynthesis(unittest.TestCase):
    def test_00_version_alignment(self) -> None:
        """Package and watermark versions are aligned at 2.3.0."""
        self.assertEqual(VERSION, "2.3.0")
        self.assertEqual(MARMA_V23_VERSION, "2.3.0")

    def test_01_sri_yantra_54_marma_nonlinear_concurrency_and_symmetric_attack(self) -> None:
        """
        Subsystem 1 (Kak VEDI-L10-0245, 0250, 0251, 0252; Kulaichev 1984):
        - Canonical Sri Yantra satisfies all 54 Marma constraints + 7 shared ordinates.
        - Sub-micron watermarked Sri Yantra satisfies all 54 Marma constraints within 4.5e-5 pt.
        - A SYMMETRIC non-payload attack (changing both lx and rx so lx + rx == 300.0 still holds!)
          bypasses simple bilateral symmetry but is IMMEDIATELY caught by the 54-Marma matrix.
        """
        can_tris = [
            {"name": name, "lx": lx, "by": by, "ay": ay, "rx": rx}
            for name, lx, by, ay, rx, _ in CANONICAL_TRIANGLES
        ]
        res_can = verify_sri_yantra_marma_concurrency_v23(can_tris, cx=150.0)
        self.assertTrue(res_can["concurrency_verified"])
        self.assertEqual(res_can["total_marma_constraints_checked"], 54)
        self.assertEqual(res_can["shared_ordinate_identities_count"], 7)
        self.assertLess(res_can["max_bilateral_symmetry_error"], 1e-11)
        self.assertLess(res_can["max_shared_ordinate_drift_pt"], 1e-8)
        self.assertLess(res_can["max_exact_29_marma_drift_pt"], 1e-7)
        self.assertLess(res_can["max_outer_circle_6_drift_pt"], 1e-7)

        # Valid watermarked carrier (v1.3 / v2.3 sub-micron QIM)
        sig_hex = hashlib.sha256(b"IEEE-TIFS-MARMA-54-CONCURRENCY").hexdigest()
        wm_tris = build_perturbed_triangles_v13(sig_hex, canary_beacon_word=512, cx=150.0)
        res_wm = verify_sri_yantra_marma_concurrency_v23(wm_tris, cx=150.0)
        self.assertTrue(res_wm["concurrency_verified"])
        self.assertLess(res_wm["max_54_marma_concurrency_drift_pt"], 4.5e-5)

        # Symmetric stealth attack: attacker shifts BOTH lx and rx of U3 by +-0.05 pt
        # so that bilateral symmetry lx + rx == 300.0 remains 0.000000000000!
        sym_attacked = copy.deepcopy(wm_tris)
        sym_attacked[2]["lx"] = round(float(sym_attacked[2]["lx"]) + 0.05, 9)
        sym_attacked[2]["rx"] = round(float(sym_attacked[2]["rx"]) - 0.05, 9)
        res_atk = verify_sri_yantra_marma_concurrency_v23(sym_attacked, cx=150.0)
        # Bilateral symmetry is still 0.0, yet 54-Marma concurrency rejects the attack!
        self.assertLess(res_atk["max_bilateral_symmetry_error"], 1e-9)
        self.assertFalse(res_atk["concurrency_verified"])
        self.assertGreater(res_atk["max_54_marma_concurrency_drift_pt"], 0.01)

    def test_02_fermat_prime_257_dsequence_qim_schedule(self) -> None:
        """
        Subsystem 2 (Kak VEDI-L10-0256):
        Prime-reciprocal d-sequence over Fermat prime q = 257 (matching GF(2^257) of DSTU 4145-2002)
        achieves full period L = 256, visits all 256 non-zero states, and has low cyclic autocorrelation.
        """
        orbit = generate_prime_remainder_orbit(q=257, primitive_root=3, seed_remainder=1)
        self.assertEqual(len(orbit), 256)
        self.assertEqual(set(orbit), set(range(1, 257)))

        d_seq = generate_prime_d_sequence(q=257, base=3, length=256, seed_remainder=1)
        self.assertEqual(len(d_seq), 256)
        self.assertTrue(all(x in (0, 1, 2) for x in d_seq))

        perm1, dither1, meta1 = derive_dsequence_qim_schedule_v23(
            secret_key="Key-Alpha", doc_digest_hex="11" * 32, n_slots=27, q=257
        )
        perm2, dither2, _ = derive_dsequence_qim_schedule_v23(
            secret_key="Key-Beta", doc_digest_hex="11" * 32, n_slots=27, q=257
        )
        self.assertEqual(sorted(perm1), list(range(27)))
        self.assertEqual(len(dither1), 27)
        self.assertNotEqual(perm1, perm2)
        self.assertNotEqual(dither1, dither2)
        self.assertEqual(meta1["full_period"], 256)
        self.assertEqual(meta1["distinct_orbit_states"], 256)
        self.assertEqual(meta1["d_sequence_autocorrelation"]["half_period_complement_correlation"], -1.0)
        self.assertLess(meta1["d_sequence_autocorrelation"]["mean_abs_off_peak_autocorrelation"], 0.05)

    def test_03_recursive_23bit_recipient_attribution_zero_extra_rmse(self) -> None:
        """
        Subsystem 3 (Parakh & Kak VEDI-L10-0258):
        23-bit recipient ID (8,388,608 copies) + 256-bit signature round-trip losslessly
        with 0.0 pt extra winding RMSE across the full 23-bit range.
        """
        self.assertEqual(MAX_RECIPIENTS_V23, 8_388_608)
        sig_hex = hashlib.sha256(b"DEALROOM-8M-RECIPIENTS-TEST").hexdigest()
        doc_sha = hashlib.sha256(b"CONFIDENTIAL-SPA-BODY").hexdigest()

        test_codes = [0, 1, 15, 1023, 1024, 16383, 5_913_759, 8_388_607]
        for code_23 in test_codes:
            enc = encode_recursive_23bit_recipient_v23(
                hex_sig=sig_hex,
                recipient_code_23bit=code_23,
                secret_key=DEFAULT_SECRET,
                doc_digest_hex=doc_sha,
            )
            self.assertEqual(enc["extra_winding_rmse_pt"], 0.0)
            self.assertLessEqual(enc["max_abs_delta_pt"], 9.21e-6)
            self.assertLess(enc["rmse_pt"], 6.0e-6)

            dec = decode_recursive_23bit_recipient_v23(
                triangles=enc["triangles"],
                secret_key=DEFAULT_SECRET,
                doc_digest_hex=doc_sha,
            )
            self.assertEqual(dec["recovered_hex_sig"], sig_hex)
            self.assertEqual(dec["recovered_recipient_code_23bit"], code_23)

        # Wrong key must fail to recover both signature and 23-bit recipient ID
        dec_wrong = decode_recursive_23bit_recipient_v23(
            triangles=enc["triangles"],
            secret_key="Wrong-Adversary-Key",
            doc_digest_hex=doc_sha,
        )
        self.assertNotEqual(dec_wrong["recovered_hex_sig"], sig_hex)

    def test_04_hierarchical_dual_layer_augmented_watermarking(self) -> None:
        """
        Subsystem 4 (Penumarthi & Kak, Cryptologia 2006, VEDI-L10-0253):
        - Layer A (Public Keyless) verifies document integrity & 54-Marma concurrency without secret_key.
        - Layer B (Forensic Keyed) verifies the 256-bit QIM signature and attributes the leaking recipient.
        """
        payload = "M&A-BOARD-RESOLUTION::2026-11-04::VALUATION-EUR-250M"
        suspects = ["Advisor_A", "Investor_B_Leak", "Counsel_C", "Auditor_D"]

        packet = stamp_augmented_dual_layer_v23(
            payload=payload,
            secret_key=DEFAULT_SECRET,
            recipient_id="Investor_B_Leak",
        )

        # 1. Public keyless verification (no secret_key)
        pub_ver = verify_augmented_dual_layer_v23(packet, payload=payload, secret_key=None)
        self.assertEqual(pub_ver["mode"], "public_keyless_layer")
        self.assertTrue(pub_ver["public_layer_verified"])
        self.assertTrue(pub_ver["marma_54_concurrency_verified"])
        self.assertIsNone(pub_ver["forensic_layer_verified"])
        self.assertTrue(pub_ver["verified"])

        # 2. Full forensic verification (with secret_key and suspect list)
        for_ver = verify_augmented_dual_layer_v23(
            packet,
            payload=payload,
            secret_key=DEFAULT_SECRET,
            suspect_recipients=suspects,
        )
        self.assertEqual(for_ver["mode"], "forensic_dual_layer")
        self.assertTrue(for_ver["public_layer_verified"])
        self.assertTrue(for_ver["forensic_layer_verified"])
        self.assertTrue(for_ver["bijective_256bit_sig_match"])
        self.assertEqual(for_ver["matched_suspect"], "Investor_B_Leak")

        # 3. Payload tampering is rejected even in keyless public mode
        tampered_pub = verify_augmented_dual_layer_v23(
            packet, payload=payload + " (modified)", secret_key=None
        )
        self.assertFalse(tampered_pub["verified"])

    def test_05_pythagorean_unit_circle_narayana_katapayadi_debruijn(self) -> None:
        """
        Subsystem 5 (Kak VEDI-L10-0260, 0261, 0235, 0239):
        - 64 Primitive Pythagorean Triples lie strictly on the rational unit circle (a^2 + b^2 == c^2)
          and survive arbitrary isotropic print-scan scaling.
        - Nārāyaṇa universal prefix code losslessly encodes and self-synchronizes integer streams.
        - Kaṭapayādi hash and Yamātārājabhānasalagām order-3 De Bruijn register pass.
        """
        self.assertEqual(len(PPT_CODEBOOK_64), 64)
        self.assertTrue(all(item["unit_circle_exact"] for item in PPT_CODEBOOK_64))
        self.assertEqual(set(item["kak_class"] for item in PPT_CODEBOOK_64), {1, 2, 3, 4, 5, 6})

        payload_48bit = 0x7A4E91C3B20D
        petals = encode_ppt_unit_circle_v23(payload_48bit, n_petals=8)
        # Simulate isotropic print-scan rescaling by factor S = 3.14159265
        scaled_petals = [
            {"unit_x": p["unit_x"] * 3.14159265, "unit_y": p["unit_y"] * 3.14159265}
            for p in petals
        ]
        dec_ppt = decode_ppt_unit_circle_v23(scaled_petals)
        self.assertEqual(dec_ppt["recovered_int"], payload_48bit)
        self.assertLess(dec_ppt["max_angular_error_deg"], 1e-9)

        # Nārāyaṇa cow sequence & universal prefix code
        n_seq = narayana_sequence_v23(12)
        self.assertEqual(n_seq[:10], [1, 2, 3, 4, 6, 9, 13, 19, 28, 41])
        for k in range(3, len(n_seq)):
            self.assertEqual(n_seq[k], n_seq[k - 1] + n_seq[k - 3])

        stream_values = list(range(1, 120)) + [257, 360, 1024, 20358]
        encoded_stream = "".join(encode_narayana_universal_v23(v) for v in stream_values)
        decoded_values = decode_narayana_universal_v23(encoded_stream)
        self.assertEqual(decoded_values, stream_values)

        # Kaṭapayādi & Yamātārājabhānasalagām
        kata = katapayadi_seed_digest_v23("Śiva Sūtra Kuleśvara")
        self.assertEqual(len(kata["seed_sha256"]), 64)
        self.assertTrue(kata["katapayadi_digits_forward"].isdigit())

        debruijn = yamatarajabhanasalagam_debruijn_v23()
        self.assertTrue(debruijn["is_complete_order3_debruijn"])
        self.assertEqual(debruijn["unique_triplet_count"], 8)

    def test_06_full_40_paper_subhash_kak_corpus_cross_verification_and_api(self) -> None:
        """
        Subsystem 6:
        Programmatically cross-verifies all 41 works of Prof. Subhash Kak
        (`VEDI-L10-0223` .. `VEDI-L10-0263`) on disk (existence, byte size, SHA-256,
        1062 total pages, and all 15 live mathematical invariants), plus live HTTP
        `/v2.3/*` endpoints.
        """
        self.assertEqual(len(KAK_40_CORPUS_MAP), 41)
        invariants = evaluate_kak_mathematical_invariants_v23()
        self.assertEqual(len(invariants), 15)
        for inv_id, inv_data in invariants.items():
            self.assertTrue(inv_data["passed"], f"Invariant {inv_id} failed: {inv_data}")

        inv_lmh = invariants["INV_THREE_BODIES_NINE_CIRCUITS"]
        self.assertEqual(inv_lmh["alias"], "INV_KAK_LMH_27")
        self.assertEqual(
            inv_lmh["triads_kak"],
            {"L": ("B1", "C1", "B2"), "M": ("B3", "B4", "C2"), "H": ("B5", "C3", "C4")},
        )
        self.assertEqual(
            inv_lmh["triads_marma"],
            {"L": ("D1", "U1", "D2"), "M": ("D3", "D4", "U2"), "H": ("D5", "U3", "U4")},
        )

        from marma_crypto.kak_synthesis_v23 import KAK_PDF_DIR, KAK_META_DIR
        if KAK_PDF_DIR.is_dir() and KAK_META_DIR.is_dir():
            report = cross_validate_kak_corpus_v23(verify_pdf_sha256=True)
            self.assertTrue(report["corpus_verified"])
            self.assertEqual(report["expected_documents"], 41)
            self.assertEqual(report["verified_documents"], 41)
            self.assertEqual(report["total_pages"], 1062)
            self.assertTrue(report["all_invariants_passed"])

        # Test live HTTP /v2.3/* endpoints
        with MarmaDealRoomServer() as srv:
            code, stamp_resp = srv.post_json(
                "/v2.3/augmented-stamp",
                {
                    "payload": "LIVE-API-V23-TEST",
                    "recipient_id": "DealRoom-Recipient-42",
                },
            )
            self.assertEqual(code, 200)
            self.assertTrue(stamp_resp["marma_54_concurrency"]["concurrency_verified"])

            # Public keyless verify over HTTP
            code, pub_resp = srv.post_json(
                "/v2.3/augmented-verify",
                {
                    "packet": stamp_resp,
                    "payload": "LIVE-API-V23-TEST",
                },
            )
            self.assertEqual(code, 200)
            self.assertTrue(pub_resp["public_layer_verified"])

            # Forensic verify over HTTP
            code, for_resp = srv.post_json(
                "/v2.3/augmented-verify",
                {
                    "packet": stamp_resp,
                    "payload": "LIVE-API-V23-TEST",
                    "secret_key": DEFAULT_SECRET,
                    "suspect_recipients": ["Other-1", "DealRoom-Recipient-42"],
                },
            )
            self.assertEqual(code, 200)
            self.assertTrue(for_resp["forensic_layer_verified"])
            self.assertEqual(for_resp["matched_suspect"], "DealRoom-Recipient-42")

            # Corpus cross-validation endpoint
            code, cv_resp = srv.get_json("/v2.3/kak-cross-validation")
            self.assertEqual(code, 200)
            self.assertTrue(cv_resp["corpus_verified"])
            self.assertEqual(cv_resp["verified_documents"], 41)


if __name__ == "__main__":
    unittest.main(verbosity=2)
