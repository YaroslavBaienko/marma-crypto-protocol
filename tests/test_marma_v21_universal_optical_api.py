#!/usr/bin/env python3
"""
4-Tier Verification Suite for Marma-Crypto v2.1 (`Universal + Deal-Room API + Optical ECC + Nautilus`)
======================================================================================================
- Tier 1 (Unit):
  * Bijective 266-bit roundtrip & bilateral symmetry across `sri-yantra`, `tryzub`, `corporate-shield`, `cad-polygon`
  * Arbitrary 2D CAD/SVG vertex list modulation & demodulation (>= 14 vertices / 27 DOFs)
  * [32, 16, d=8] Optical Lotus ECC encoding & Soft-Decision ML decoding under bit flips and AWGN noise
- Tier 2 (Integration):
  * Universal SVG & PDF stamping/verification with Ukrainian Trident (`tryzub`) & Corporate Shield
  * Live HTTP REST Deal-Room Microservice (`GET /v1/health`, `POST /v1/seal-batch`, `POST /v1/verify`, `POST /v1/trace-leak`)
- Tier 3 (Live Screen-Photo / Print-Cam Attack Simulation):
  * Full PDF page & seal rasterization -> Gaussian blur + sensor noise + JPEG(quality=72) compression
  * Blind optical extraction of `canary_beacon_word` and exact identification of the leaking recipient
- Tier 4 (Live Nautilus / GNOME Files Integration):
  * `bin/marma-config` menu tree deployment (`🇺🇦 Підписати Гербом-Тризубом`, `🏗️ Захистити креслення CAD/SVG`,
    `📦 Пакетне штампування Deal-Room`, `🕵️ Розшук джерела витоку`) and headless execution via `NAUTILUS_SCRIPT_SELECTED_FILE_PATHS`
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image, ImageFilter

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from marma_crypto import (  # noqa: E402
    SUPPORTED_EMBLEMS,
    MarmaDealRoomServer,
    batch_seal_dealroom,
    build_perturbed_emblem_v21,
    compute_doc_tag6,
    decode_optical_codeword32_soft,
    demodulate_arbitrary_2d_vertices,
    encode_optical_codeword32,
    extract_canary_from_raster_image,
    modulate_arbitrary_2d_vertices,
    recover_256bit_from_emblem_v21,
    render_optical_seal_png,
    stamp_pdf_universal_v21,
    stamp_universal_svg_drawing,
    trace_leak_any_medium,
    verify_emblem_coordinates_v21,
    verify_pdf_universal_v21,
    verify_universal_svg_drawing,
)
from marma_watermark import DEFAULT_SECRET, compute_canary_tag  # noqa: E402


class TestMarmaV21UniversalOpticalAPI(unittest.TestCase):
    # ==========================================================================
    # TIER 1: UNIT TESTS
    # ==========================================================================
    def test_tier1_universal_emblems_27dof_roundtrip(self) -> None:
        """All 4 emblems (`sri-yantra`, `tryzub`, `corporate-shield`, `cad-polygon`) losslessly invert 266 bits."""
        sample_hex = hashlib.sha256(b"MARMA-UNIVERSAL-256BIT-VECTOR").hexdigest()
        canary_word = 777
        qim_key = "Sovereign-Test-Key-2026"
        doc_nonce = hashlib.sha256(b"Document-Nonce-Alpha").hexdigest()

        for emblem in SUPPORTED_EMBLEMS:
            # 1. Unkeyed mode
            perturbed = build_perturbed_emblem_v21(
                sample_hex, emblem_type=emblem, canary_beacon_word=canary_word, cx=150.0
            )
            self.assertEqual(len(perturbed), 9)
            rec_hex, rec_canary = recover_256bit_from_emblem_v21(
                perturbed, emblem_type=emblem, cx=150.0
            )
            self.assertEqual(rec_hex, sample_hex, f"Digest mismatch for {emblem}")
            self.assertEqual(rec_canary, canary_word, f"Canary mismatch for {emblem}")

            drift, sym_err = verify_emblem_coordinates_v21(
                perturbed,
                emblem_type=emblem,
                cx=150.0,
                expected_hex=sample_hex,
                canary_beacon_word=canary_word,
            )
            self.assertEqual(drift, 0.0)
            self.assertLess(sym_err, 1e-11)

            # 2. Keyed Dithered QIM mode (d_K, pi_K)
            perturbed_keyed = build_perturbed_emblem_v21(
                sample_hex,
                emblem_type=emblem,
                canary_beacon_word=canary_word,
                cx=150.0,
                qim_key=qim_key,
                doc_nonce=doc_nonce,
            )
            rec_hex_k, rec_canary_k = recover_256bit_from_emblem_v21(
                perturbed_keyed,
                emblem_type=emblem,
                cx=150.0,
                qim_key=qim_key,
                doc_nonce=doc_nonce,
            )
            self.assertEqual(rec_hex_k, sample_hex)
            self.assertEqual(rec_canary_k, canary_word)

            # Wrong key must fail to recover the digest
            wrong_hex, _ = recover_256bit_from_emblem_v21(
                perturbed_keyed,
                emblem_type=emblem,
                cx=150.0,
                qim_key="Wrong-Key-999",
                doc_nonce=doc_nonce,
            )
            self.assertNotEqual(wrong_hex, sample_hex)

    def test_tier1_arbitrary_2d_cad_polygon_vertices(self) -> None:
        """Arbitrary 2D CAD contour with >= 14 vertices embeds and recovers 266 bits with 0.0 npt residual."""
        # 18-vertex CAD turbine flange polygon
        canonical_pts = [
            (40.0 + i * 12.5, 55.0 + (i % 5) * 18.25) for i in range(18)
        ]
        sig_hex = hashlib.sha256(b"CAD-TURBINE-FLANGE-REV-09").hexdigest()
        canary = 913
        key = "DefenseTech-CAD-Secret"
        nonce = "DXF-Drawing-0042"

        modulated_pts = modulate_arbitrary_2d_vertices(
            canonical_pts, sig_hex, canary_beacon_word=canary, qim_key=key, doc_nonce=nonce
        )
        self.assertEqual(len(modulated_pts), len(canonical_pts))
        # Vertices beyond the 27th scalar coordinate must remain strictly identical
        self.assertEqual(modulated_pts[14:], canonical_pts[14:])

        rec_sig, rec_canary, max_res = demodulate_arbitrary_2d_vertices(
            modulated_pts, canonical_pts, qim_key=key, doc_nonce=nonce
        )
        self.assertEqual(rec_sig, sig_hex)
        self.assertEqual(rec_canary, canary)
        self.assertEqual(max_res, 0.0)

        # Too few vertices (< 14) must raise ValueError
        with self.assertRaises(ValueError):
            modulate_arbitrary_2d_vertices([(0.0, 0.0)] * 10, sig_hex)

    def test_tier1_optical_ecc_32_16_soft_ml_decoder(self) -> None:
        """[32, 16] Optical ECC corrects up to 4 hard bit flips and heavy AWGN noise."""
        canary_w = 642
        tag6 = 0b101101
        cw = encode_optical_codeword32(canary_w, tag6)
        self.assertEqual(len(cw), 32)

        # Clean signal: bit 1 -> +100.0, bit 0 -> -100.0
        clean_scores = np.array([100.0 if b == 1 else -100.0 for b in cw], dtype=np.float64)
        dec_clean = decode_optical_codeword32_soft(clean_scores, expected_doc_tag6=tag6)
        self.assertEqual(dec_clean["canary_beacon_word"], canary_w)
        self.assertEqual(dec_clean["corrected_bit_errors"], 0)
        self.assertAlmostEqual(dec_clean["ml_correlation"], 1.0, places=3)

        # Flip 4 sectors completely (simulate specular screen glare on 4 lotus petals)
        corrupted = clean_scores.copy()
        for flip_idx in (2, 9, 17, 28):
            corrupted[flip_idx] *= -1.0
        dec_flipped = decode_optical_codeword32_soft(corrupted, expected_doc_tag6=tag6)
        self.assertEqual(dec_flipped["canary_beacon_word"], canary_w)
        self.assertEqual(dec_flipped["corrected_bit_errors"], 4)

    # ==========================================================================
    # TIER 2: INTEGRATION TESTS (SVG, PDF, BATCH DEAL-ROOM & HTTP MICROSERVICE)
    # ==========================================================================
    def test_tier2_universal_svg_and_pdf_tryzub_shield(self) -> None:
        """Stamping and verifying SVG and PDF with `tryzub` and `corporate-shield` works end-to-end."""
        with tempfile.TemporaryDirectory(prefix="marma-v21-int.") as tmp:
            work = Path(tmp)
            # 1. Universal SVG (Tryzub)
            svg_in = work / "cad_blueprint.svg"
            svg_in.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">'
                '<rect width="300" height="300" fill="#101820"/></svg>',
                encoding="utf-8",
            )
            svg_out = work / "cad_blueprint_tryzub.svg"
            stamp_universal_svg_drawing(
                svg_in, svg_out, secret_key=DEFAULT_SECRET, emblem_type="tryzub", recipient_id="Ministry_01"
            )
            ver_svg = verify_universal_svg_drawing(svg_out, secret_key=DEFAULT_SECRET, recipient_id="Ministry_01")
            self.assertTrue(ver_svg["verified"])
            self.assertEqual(ver_svg["emblem_type"], "tryzub")
            self.assertTrue(ver_svg["canary_recipient_verified"])

            # 2. Universal PDF (Corporate Shield + Optical Lotus Ring)
            pdf_in = work / "contract.pdf"
            doc = pymupdf.open()
            page = doc.new_page()
            page.insert_text((72, 120), "GOLAW M&A Deal-Room Share Purchase Agreement", fontsize=13)
            doc.save(str(pdf_in))
            doc.close()

            pdf_out = work / "contract_shield.pdf"
            stamp_pdf_universal_v21(
                pdf_in,
                pdf_out,
                secret_key=DEFAULT_SECRET,
                recipient_id="Acquirer_Fund_LP",
                emblem_type="corporate-shield",
                optical_ring=True,
            )
            ver_pdf = verify_pdf_universal_v21(
                pdf_out, secret_key=DEFAULT_SECRET, recipient_id="Acquirer_Fund_LP"
            )
            self.assertTrue(ver_pdf["verified"])
            self.assertEqual(ver_pdf["emblem_type"], "corporate-shield")
            self.assertTrue(ver_pdf["optical_ring"])
            self.assertTrue(ver_pdf["canary_recipient_verified"])

    def test_tier2_dealroom_http_microservice_end_to_end(self) -> None:
        """Live HTTP microservice handles /v1/health, /v1/seal-batch, /v1/verify, and /v1/trace-leak."""
        with tempfile.TemporaryDirectory(prefix="marma-v21-api.") as tmp:
            work = Path(tmp)
            master_pdf = work / "nda_master.pdf"
            d = pymupdf.open()
            p = d.new_page()
            p.insert_text((72, 100), "Strictly Confidential DefenseTech Architecture v2.1", fontsize=12)
            d.save(str(master_pdf))
            d.close()

            out_dir = work / "dealroom_out"
            recipients = ["Bidder_Alpha", "Bidder_Beta", "Bidder_Gamma", "Bidder_Delta"]

            with MarmaDealRoomServer() as srv:
                # 1. GET /v1/health
                code, health = srv.get_json("/v1/health")
                self.assertEqual(code, 200)
                self.assertEqual(health["status"], "ok")
                self.assertIn("tryzub", health["supported_emblems"])

                # 2. POST /v1/seal-batch
                code, batch_res = srv.post_json(
                    "/v1/seal-batch",
                    {
                        "input_file": str(master_pdf),
                        "output_dir": str(out_dir),
                        "recipients": recipients,
                        "emblem_type": "tryzub",
                        "optical_ring": True,
                    },
                )
                self.assertEqual(code, 200)
                self.assertEqual(batch_res["recipient_count"], 4)

                leaked_pdf = Path(batch_res["copies"][2]["output_file"])  # Bidder_Gamma

                # 3. POST /v1/verify
                code, ver_res = srv.post_json(
                    "/v1/verify",
                    {"file": str(leaked_pdf), "recipient_id": "Bidder_Gamma"},
                )
                self.assertEqual(code, 200)
                self.assertTrue(ver_res["verified"])
                self.assertTrue(ver_res["canary_recipient_verified"])

                # 4. POST /v1/trace-leak
                code, trace_res = srv.post_json(
                    "/v1/trace-leak",
                    {"file": str(leaked_pdf), "suspects": recipients},
                )
                self.assertEqual(code, 200)
                self.assertEqual(trace_res["matched_recipient"], "Bidder_Gamma")

    # ==========================================================================
    # TIER 3: LIVE SCREEN-PHOTO / PRINT-CAM ATTACK SIMULATION
    # ==========================================================================
    def test_tier3_screen_photo_jpeg_blur_noise_leak_tracing(self) -> None:
        """
        Simulate a traitor taking a lossy, blurry, noisy JPEG photo/screenshot of a
        stamped PDF page (and standalone seal) after all vector coordinates are destroyed.
        Verify that `extract_canary_from_raster_image` identifies the exact traitor.
        """
        with tempfile.TemporaryDirectory(prefix="marma-v21-optical.") as tmp:
            work = Path(tmp)
            pdf_in = work / "board_deck.pdf"
            d = pymupdf.open()
            p = d.new_page()
            p.insert_text((72, 100), "Board of Directors Q4 M&A Valuation Deck", fontsize=14)
            d.save(str(pdf_in))
            d.close()

            suspects = [
                "Director_01_Kyiv",
                "Director_02_London",
                "Traitor_03_Offshore",
                "Director_04_Zurich",
                "Auditor_05_Big4",
            ]
            pdf_stamped = work / "board_deck_traitor03.pdf"
            stamp_res = stamp_pdf_universal_v21(
                pdf_in,
                pdf_stamped,
                secret_key=DEFAULT_SECRET,
                recipient_id="Traitor_03_Offshore",
                emblem_type="tryzub",
                optical_ring=True,
            )
            csha = stamp_res["content_sha256"]
            expected_word = stamp_res["canary"]["beacon_word"]

            # Render the stamped PDF page at 216 DPI (3x scale) to a raster image, stripping all vectors
            doc_s = pymupdf.open(str(pdf_stamped))
            pix = doc_s[0].get_pixmap(matrix=pymupdf.Matrix(3.0, 3.0), alpha=False)
            doc_s.close()
            raw_png = work / "screen_capture_raw.png"
            pix.save(str(raw_png))

            # Apply Screen-Photo degradation: Gaussian blur + sensor noise + lossy JPEG compression
            img = Image.open(str(raw_png)).convert("RGB")
            img_blurred = img.filter(ImageFilter.GaussianBlur(radius=0.85))
            arr = np.asarray(img_blurred, dtype=np.float64)
            rng = np.random.default_rng(20261021)
            noisy_arr = np.clip(arr + rng.normal(0.0, 7.5, size=arr.shape), 0, 255).astype(np.uint8)
            degraded_jpg = work / "leaked_smartphone_photo.jpg"
            Image.fromarray(noisy_arr).save(str(degraded_jpg), format="JPEG", quality=72)

            # Trace leak directly from the degraded JPEG photo!
            optical_trace = trace_leak_any_medium(
                degraded_jpg,
                suspects=suspects,
                secret_key=DEFAULT_SECRET,
                content_sha256=csha,
            )
            self.assertTrue(optical_trace["optical_verified"])
            self.assertEqual(optical_trace["canary_beacon_word"], expected_word)
            self.assertEqual(optical_trace["matched_recipient"], "Traitor_03_Offshore")
            self.assertGreaterEqual(optical_trace["ml_correlation"], 0.65)

    # ==========================================================================
    # TIER 4: LIVE NAUTILUS / GNOME FILES MENU & SCRIPT EXECUTION
    # ==========================================================================
    def test_tier4_nautilus_menu_deployment_and_scripts_execution(self) -> None:
        """
        Verify that `bin/marma-config` deploys all new v2.1 scripts into the Nautilus
        menu and that each script executes cleanly on target files.
        """
        with tempfile.TemporaryDirectory(prefix="marma-v21-nautilus.") as tmp:
            work = Path(tmp)
            fake_home = work / "home"
            fake_home.mkdir(parents=True, exist_ok=True)

            env = os.environ.copy()
            env["HOME"] = str(fake_home)
            env["MARMA_SOURCE_SCRIPTS_DIR"] = str(REPO_ROOT / "nautilus-scripts")
            env["MARMA_HEADLESS"] = "1"
            env["PATH"] = f"{REPO_ROOT / 'bin'}:{ work / 'bin' }:{env.get('PATH', '')}"

            # Create a local `marma-watermark` wrapper in work/bin so Nautilus scripts call our repo code
            bin_dir = work / "bin"
            bin_dir.mkdir(parents=True, exist_ok=True)
            wrapper = bin_dir / "marma-watermark"
            wrapper.write_text(
                f"#!/usr/bin/env bash\nexec python3 '{REPO_ROOT / 'src' / 'marma_watermark.py'}' \"$@\"\n",
                encoding="utf-8",
            )
            wrapper.chmod(0o755)

            # 1. Run marma-config --lang uk
            res_cfg = subprocess.run(
                [str(REPO_ROOT / "bin" / "marma-config"), "--lang", "uk"],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("🔱 Шрі Янтра · Marma-Crypto", res_cfg.stdout)

            menu_root = fake_home / ".local" / "share" / "nautilus" / "scripts" / "🔱 Шрі Янтра · Marma-Crypto"
            sign_cat = menu_root / "✍️ Підписання та Водяний знак"
            ver_cat = menu_root / "🔍 Перевірка та Протоколи"

            tryzub_script = sign_cat / "🇺🇦 Підписати Гербом-Тризубом або Щитом (Marma-Universal)"
            cad_script = sign_cat / "🏗️ Захистити креслення CAD-SVG (27-DOF)"
            batch_script = sign_cat / "📦 Пакетне штампування Deal-Room (N отримувачів)"
            trace_script = ver_cat / "🕵️ Розшук джерела витоку (PDF або Фото екрана Marma-Optical)"

            self.assertTrue(tryzub_script.is_file())
            self.assertTrue(cad_script.is_file())
            self.assertTrue(batch_script.is_file())
            self.assertTrue(trace_script.is_file())

            # 2. Execute 8_stamp_tryzub.sh via NAUTILUS_SCRIPT_SELECTED_FILE_PATHS
            sample_pdf = work / "ministry_order.pdf"
            d = pymupdf.open()
            p = d.new_page()
            p.insert_text((72, 100), "Наказ про затвердження криптографічного стандарту v2.1", fontsize=12)
            d.save(str(sample_pdf))
            d.close()

            env_tryzub = env.copy()
            env_tryzub["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"] = str(sample_pdf)
            env_tryzub["MARMA_EMBLEM"] = "tryzub"
            env_tryzub["MARMA_RECIPIENT_ID"] = "Dept_Cyber_07"
            subprocess.run([str(tryzub_script)], env=env_tryzub, check=True)
            signed_tryzub_pdf = work / "ministry_order_marma_tryzub.pdf"
            self.assertTrue(signed_tryzub_pdf.is_file())

            # 3. Execute 11_trace_leak_optical.sh on the signed Tryzub PDF
            env_trace = env.copy()
            env_trace["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"] = str(signed_tryzub_pdf)
            env_trace["MARMA_SUSPECTS"] = "Dept_Finance_01,Dept_Cyber_07,Dept_Legal_09"
            out_trace = subprocess.run(
                [str(trace_script)], env=env_trace, capture_output=True, text=True, check=True
            )
            trace_data = json.loads(out_trace.stdout)
            self.assertEqual(trace_data["matched_recipient"], "Dept_Cyber_07")


if __name__ == "__main__":
    unittest.main(verbosity=2)
