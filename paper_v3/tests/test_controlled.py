#!/usr/bin/env python3
"""Controlled, cross-verified, cross-validated test suite for the PDF seal.

Covered functionality
  - word <-> lattice map (bijection, truncation behaviour, KAT)
  - cross-runtime verification against an independent JavaScript implementation
  - cross-verification against the production signer (src/marma_watermark.py)
  - profile P1 (paper stamp) and P2 (42 mm round product stamp): round-trip, geometry,
    truncation, single-coordinate edit, flattening, wrong-profile rejection
  - reserved-zone templates: no text overlap for P1/P2 (and overlap on the default template)
  - corpus integrity (sha256 manifest) and the physical print-scan results
  - determinism / known-answer vectors
Run:  python3 paper_v3/tests/test_controlled.py -v
"""
from __future__ import annotations
import hashlib, json, math, random, shutil, statistics, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL = ROOT / "paper_v3" / "eval"
sys.path.insert(0, str(EVAL))
sys.path.insert(0, str(ROOT / "src"))
import pymupdf as fitz
import pdf_layer as pl
import profiles as pf
import harness
import build_corpus as bc

CORPUS = EVAL / "corpus"
MANIFEST = CORPUS / "corpus_manifest.json"
MM = 72.0 / 25.4


def payload(seed: int) -> list[int]:
    return harness.payload_words(hashlib.sha256(f"controlled::{seed}".encode()).digest(), seed % 1024)


def native_docs(n=6):
    return sorted(CORPUS.glob("typst_*_native.pdf"))[:n]


def stamp(profile, src, words, seed, name):
    out = Path(tempfile.mkdtemp()) / f"{name}.pdf"
    pf.stamp(src, out, profile, words, seed=seed)
    return out


def text_rects(path):
    doc = fitz.open(str(path))
    try:
        return [fitz.Rect(b[:4]) for b in doc[0].get_text("blocks")]
    finally:
        doc.close()


def overlap_area(path):
    m = pf.marker_bbox(path)
    if m is None: return 0.0
    area = 0.0
    for r in text_rects(path):
        inter = fitz.Rect(m) & r
        if not inter.is_empty:
            area += abs(inter.width * inter.height)
    return area


class TestWordMap(unittest.TestCase):
    def test_bijection_all_1024(self):
        ds = [pl.word_to_delta(w) for w in range(1024)]
        self.assertEqual(len(set(ds)), 1024)
        for w, d in enumerate(ds):
            self.assertEqual(pl.delta_to_word(d), w)

    def test_kat_values(self):
        expect = {0: -0.000009207, 1: -0.000009189, 511: -0.000000009,
                  512: 0.000000009, 1023: 0.000009207}
        for w, v in expect.items():
            self.assertAlmostEqual(pl.word_to_delta(w), v, places=15)
            self.assertEqual(pl.delta_to_word(v), w)

    def test_trunc8_exact_trunc7_breaks(self):
        rng = random.Random(2026)
        ok8 = ok7 = 0
        N = 512
        for _ in range(N):
            w = rng.randrange(1024)
            # re-serialisation rounds the stored coordinate itself (no extra analog noise):
            ok8 += pl.delta_to_word(round(pl.word_to_delta(w), 8)) == w
            ok7 += pl.delta_to_word(round(pl.word_to_delta(w), 7)) == w
        self.assertEqual(ok8, N)
        self.assertLess(ok7, N * 0.25, f"expected the 7-decimal cliff, got {ok7}/{N} survivors")

    def test_cross_runtime_javascript(self):
        js = ROOT / "paper_v3" / "tests" / "crosscheck_wordmap.js"
        out = subprocess.run(["node", str(js)], capture_output=True, text=True, check=True)
        ref = json.loads(out.stdout)
        self.assertEqual(len(ref["deltas"]), 1024)
        for w, (d_js, w_js) in enumerate(zip(ref["deltas"], ref["words"])):
            self.assertAlmostEqual(d_js, pl.word_to_delta(w), places=15)
            self.assertEqual(w_js, w)
            self.assertEqual(pl.delta_to_word(d_js), w)

    def test_cross_verification_production_signer(self):
        try:
            import marma_watermark as mw
        except Exception as e:  # pragma: no cover
            self.skipTest(f"production signer import failed: {e}")
        for w in range(1024):
            self.assertEqual(mw.word10_to_delta(w), pl.word_to_delta(w))
            self.assertEqual(mw.delta_to_word10(pl.word_to_delta(w)), w)


class TestProfiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MANIFEST.exists():
            raise unittest.SkipTest("corpus missing; run build_corpus.py first")
        cls.words = payload(11)
        cls.docs = native_docs(6)
        cls.tmp = Path(tempfile.mkdtemp(prefix="controlled_profiles_"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _stamp(self, p, src, seed):
        out = self.tmp / f"{p.id}_{src.stem}_{seed}.pdf"
        pf.stamp(src, out, p, self.words, seed=seed)
        return out

    def test_p1_roundtrip(self):
        for src in self.docs:
            for seed in (0, 1):
                out = self._stamp(pf.P1, src, seed)
                self.assertEqual(pf.extract_words(out, pf.P1, seed=seed), self.words)

    def test_p2_roundtrip(self):
        for src in self.docs:
            for seed in (0, 1):
                out = self._stamp(pf.P2, src, seed)
                self.assertEqual(pf.extract_words(out, pf.P2, seed=seed), self.words)

    def test_p2_geometry_and_size(self):
        src = self.docs[0]
        out = self._stamp(pf.P2, src, 0)
        self.assertTrue(pf.geometry_ok(out, pf.P2))
        r = pf.marker_bbox(out)
        self.assertLessEqual(max(r.width, r.height), 42.0 * MM + 1e-6)
        page = fitz.open(str(out))[0]
        self.assertTrue(page.rect.contains(r))

    def test_wrong_profile_rejected(self):
        a = self._stamp(pf.P1, self.docs[0], 0)
        b = self._stamp(pf.P2, self.docs[0], 0)
        self.assertNotEqual(pf.extract_words(a, pf.P2, seed=0), self.words)
        self.assertNotEqual(pf.extract_words(b, pf.P1, seed=0), self.words)

    def test_geometry_invariant_breaks_on_centre_edit(self):
        out = self._stamp(pf.P1, self.docs[0], 0)
        self.assertTrue(pf.geometry_ok(out, pf.P1))
        edited = self.tmp / "centre_edit.pdf"
        self.assertTrue(pl.attack_edit_coord(out, edited, occurrence=1, delta=0.5))
        self.assertFalse(pf.geometry_ok(edited, pf.P1))
        self.assertNotEqual(pf.extract_words(edited, pf.P1, seed=0), self.words)

    def test_truncation_and_edit_detection_p1_p2(self):
        for p in (pf.P1, pf.P2):
            out = self._stamp(p, self.docs[0], 0)
            t8 = self.tmp / f"{p.id}_t8.pdf"; self.assertTrue(pl.attack_truncate(out, t8, 8))
            self.assertEqual(pf.extract_words(t8, p, seed=0), self.words)
            t7 = self.tmp / f"{p.id}_t7.pdf"; self.assertTrue(pl.attack_truncate(out, t7, 7))
            self.assertNotEqual(pf.extract_words(t7, p, seed=0), self.words)
            ed = self.tmp / f"{p.id}_ed.pdf"; self.assertTrue(pl.attack_edit_coord(out, ed, 6, 1e-4))
            words_ed = pf.extract_words(ed, p, seed=0)
            self.assertIsNotNone(words_ed)
            self.assertEqual(sum(1 for a, b in zip(words_ed, self.words) if a != b), 1)
            fl = self.tmp / f"{p.id}_flat.pdf"; pl.flatten(out, fl)
            self.assertIsNone(pf.extract_words(fl, p, seed=0))

    def test_profiles_json(self):
        meta = pf.to_json()
        self.assertEqual([x["id"] for x in meta["profiles"]], ["v1-geometric", "v2-round42"])
        self.assertIn("absolute", meta["deltas"])

    def test_determinism(self):
        a = self._stamp(pf.P2, self.docs[0], 3)
        b = self._stamp(pf.P2, self.docs[0], 3)
        wa, wb = pf.extract_words(a, pf.P2, seed=3), pf.extract_words(b, pf.P2, seed=3)
        self.assertEqual(wa, wb)
        self.assertEqual(hashlib.sha256(json.dumps(wa).encode()).hexdigest(),
                         hashlib.sha256(json.dumps(wb).encode()).hexdigest())


class TestReservedZone(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MANIFEST.exists():
            raise unittest.SkipTest("corpus missing")
        cls.tmp = Path(tempfile.mkdtemp(prefix="controlled_reserved_"))
        cls.reserved = []
        for i in range(2):
            p = cls.tmp / f"typst_{i:02d}_native.pdf"
            bc.gen_pdf("typst", i, p, random.Random(100 + i), reserved=True)
            if p.exists(): cls.reserved.append(p)
        cls.words = payload(21)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def _stamp(self, p, src):
        out = self.tmp / f"{p.id}_reserved_{src.stem}.pdf"
        pf.stamp(src, out, p, self.words, seed=0)
        return out

    def test_reserved_zone_generated(self):
        self.assertEqual(len(self.reserved), 2)

    def test_p1_no_text_overlap(self):
        for src in self.reserved:
            out = self._stamp(pf.P1, src)
            self.assertEqual(overlap_area(out), 0.0, f"P1 overlaps text on {src.name}")

    def test_p2_no_text_overlap(self):
        for src in self.reserved:
            out = self._stamp(pf.P2, src)
            self.assertEqual(overlap_area(out), 0.0, f"P2 overlaps text on {src.name}")

    def test_default_template_overlaps_justifying_reserved_zone(self):
        src = CORPUS / "typst_00_native.pdf"
        if not src.exists(): self.skipTest("corpus missing")
        out = self._stamp(pf.P1, src)
        self.assertGreater(overlap_area(out), 0.0)


class TestCorpusAndArtifacts(unittest.TestCase):
    def test_corpus_manifest_hashes(self):
        if not MANIFEST.exists(): self.skipTest("corpus missing")
        man = json.loads(MANIFEST.read_text())
        self.assertEqual(len(man), 180)
        for m in man:
            f = CORPUS / m["path"]
            self.assertTrue(f.exists(), m["path"])
            self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(), m["sha256"], m["path"])

    def test_physical_printscan_results(self):
        res = json.loads((EVAL / "printscan" / "results.json").read_text())
        self.assertEqual(len(res), 5)
        for r in res:
            self.assertEqual(r["digital_control"], "valid")
            self.assertEqual(r["state"], "absent")

    def test_profiles_manifest(self):
        p = EVAL / "profiles.json"
        if not p.exists(): self.skipTest("profiles.json missing")
        self.assertEqual(json.loads(p.read_text())["profiles"][1]["scale"], 0.45)


class TestCrossValidationMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not MANIFEST.exists(): raise unittest.SkipTest("corpus missing")
        cls.docs = native_docs(3)
        cls.tmp = Path(tempfile.mkdtemp(prefix="controlled_matrix_"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_matrix_exact_and_attacks(self):
        n = exact = detect = absent = 0
        for p in (pf.P1, pf.P2):
            for di, src in enumerate(self.docs):
                for seed in range(3):
                    words = payload(100 + di * 10 + seed)
                    out = self.tmp / f"{p.id}_{di}_{seed}.pdf"
                    pf.stamp(src, out, p, words, seed=seed)
                    n += 1
                    exact += pf.extract_words(out, p, seed=seed) == words
                    t7 = self.tmp / f"{p.id}_{di}_{seed}_t7.pdf"
                    pl.attack_truncate(out, t7, 7)
                    detect += pf.extract_words(t7, p, seed=seed) != words
                    fl = self.tmp / f"{p.id}_{di}_{seed}_flat.pdf"
                    pl.flatten(out, fl)
                    absent += pf.extract_words(fl, p, seed=seed) is None
        self.assertEqual(exact, n)
        self.assertEqual(detect, n)
        self.assertEqual(absent, n)

    def test_unmodified_document_has_no_carrier(self):
        self.assertIsNone(pf.extract_words(self.docs[0], pf.P1))
        self.assertIsNone(pf.extract_words(self.docs[0], pf.P2))


class TestHarnessAndCarriers(unittest.TestCase):
    """Slot-level carrier/method API used by the experiments (same word map and attacks)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="controlled_harness_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_carriers_make_and_render(self):
        for kind in ("sri-yantra", "generic-18gon", "grid"):
            c = harness.make_carrier(kind, seed=4)
            self.assertEqual(len(c.slots), 27)
            out = self.tmp / f"{kind}.svg"
            harness.render_svg(c, out)
            self.assertTrue(out.exists() and out.stat().st_size > 100)

    def test_qim_embed_extract_keyed_and_unkeyed(self):
        for keyed in (False, True):
            c = harness.make_carrier("sri-yantra", seed=5)
            payload_bytes = b"\x11" * 32
            m, info = harness.embed_qim(c, payload_bytes, canary=7, keyed=keyed, key=b"k" * 32)
            self.assertEqual(info["payload_bits"], 266)
            rec = harness.extract_qim(m, c, keyed=keyed, key=b"k" * 32)
            self.assertEqual(rec["words"], harness.payload_words(payload_bytes, 7))

    def test_scalar_qim_rdh_lsb_ss(self):
        c = harness.make_carrier("generic-18gon", seed=6)
        m, info = harness.embed_scalar_qim(c, b"\x22" * 32, canary=3)
        self.assertEqual(info["payload_bits"], 266)
        for fn in (harness.embed_lsb, harness.embed_ss):
            m, info = fn(c)
            self.assertIn("capacity", info)
        m, info = harness.embed_de_rdh(c, max_diff_nano=5000)
        self.assertIn("capacity", info)

    def test_metrics_and_attacks(self):
        c = harness.make_carrier("sri-yantra", seed=7)
        d = harness.translate(c, 0.5)
        self.assertGreater(harness.rmse(c, d), 0)
        self.assertLess(harness.psnr_geom(harness.rmse(c, d)), 200)
        self.assertLess(harness.rmse(c, harness.truncate(c, 8)), 1e-8)
        self.assertNotEqual(harness.edit_vertex(c, 0, 1e-4).slots, c.slots)
        self.assertNotEqual(harness.scale(c, 2.0).slots, c.slots)
        w, n = harness.match_words([1, 2, 3], [1, 5, 3])
        self.assertEqual((w, n), (1, 3))

    def test_run_methods(self):
        for method in ("qim", "qim-unkeyed"):
            r = harness.run(seed=11, carrier_kind="sri-yantra", method=method, keyed=True)
            self.assertTrue(r["exact"])
            self.assertTrue(r["detect_trunc7"])
        for method in ("ss", "lsb", "de"):
            r = harness.run(seed=12, carrier_kind="sri-yantra", method=method, keyed=True)
            self.assertIn("capacity", r)


class TestPdfLayerAPI(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="controlled_pdflayer_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_carrier_variants_roundtrip(self):
        src = CORPUS / "typst_00_native.pdf"
        if not src.exists(): self.skipTest("corpus missing")
        slots = pl._canonical("sri-yantra", seed=0)
        deltas = [pl.word_to_delta(w) for w in payload(31)]
        for kind in ("sri-yantra", "generic-polyline", "grid"):
            out = self.tmp / f"{kind}.pdf"
            pl.stamp(src, out, kind, deltas, seed=0)
            rec = pl.extract(out, kind, seed=0)
            self.assertIsNotNone(rec)
            self.assertEqual(rec, payload(31))

    def test_extract_slots_and_geometry(self):
        src = CORPUS / "typst_00_native.pdf"
        if not src.exists(): self.skipTest("corpus missing")
        slots = pl._canonical("sri-yantra", seed=0)
        deltas = [pl.word_to_delta(w) for w in payload(32)]
        out = self.tmp / "s.pdf"; pl.stamp(src, out, "sri-yantra", deltas, seed=0)
        raw = pl.extract_slots(out, "sri-yantra", seed=0)
        self.assertEqual(len(raw), 27)
        self.assertTrue(pl.geometry_ok(out, "sri-yantra", seed=0))
        self.assertTrue(pl.invariant_ok(out, "sri-yantra", seed=0))
        self.assertIsNone(pl.extract_slots(src, "sri-yantra", seed=0))

    def test_unknown_carrier_rejected(self):
        src = CORPUS / "typst_00_native.pdf"
        if not src.exists(): self.skipTest("corpus missing")
        with self.assertRaises(ValueError):
            pl.stamp(src, self.tmp / "x.pdf", "unknown", [0.0] * 27)


class TestProductionProfile(unittest.TestCase):
    """P2 profile wired into the production signer wrapper (src/marma_seal_profiles.py)."""

    SECRET = "Sovereign-Vedic-Geometry-Key-108"

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="controlled_prodprofile_"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        import marma_seal_profiles as sp
        self.sp = sp

    def _sign(self, profile, payload="profiled production seal"):
        out = self.tmp / f"{profile}.svg"
        res = self.sp.sign_seal_svg(payload, self.SECRET, out, profile_id=profile)
        return out, res

    def test_v1_legacy_unchanged(self):
        out, res = self._sign("v1-geometric")
        v = self.sp.verify_seal_svg(out.read_text(), payload="profiled production seal",
                                    secret_key=self.SECRET)
        self.assertTrue(v["verified"], v.get("reason"))
        self.assertEqual(res["profile"], "v1-geometric")

    def test_v2_round42_verified_and_profile_persisted(self):
        out, res = self._sign("v2-round42")
        svg = out.read_text()
        self.assertIn('data-profile="v2-round42"', svg)
        self.assertIn('width="42mm"', svg)
        self.assertGreaterEqual(svg.count("<circle"), 5)
        self.assertEqual(res["profile_mm"], 42.0)
        v = self.sp.verify_seal_svg(svg, expected_profile="v2-round42",
                                    payload="profiled production seal", secret_key=self.SECRET)
        self.assertTrue(v["verified"], v.get("reason"))
        self.assertEqual(v["profile"], "v2-round42")
        self.assertEqual(v["profile_mm"], 42.0)

    def test_wrong_profile_fails_closed(self):
        out, _ = self._sign("v2-round42")
        v = self.sp.verify_seal_svg(out.read_text(), expected_profile="v1-geometric",
                                    payload="profiled production seal", secret_key=self.SECRET)
        self.assertFalse(v["verified"])
        v2 = self.sp.verify_seal_svg(out.read_text(), profile_id="v1-geometric",
                                     payload="profiled production seal", secret_key=self.SECRET)
        self.assertFalse(v2["verified"])

    def test_unknown_profile_fails_closed(self):
        out, _ = self._sign("v2-round42")
        svg = out.read_text().replace('data-profile="v2-round42"', 'data-profile="evil-profile"', 1)
        v = self.sp.verify_seal_svg(svg, payload="profiled production seal", secret_key=self.SECRET)
        self.assertFalse(v["verified"])
        self.assertIn("unknown seal profile", v["reason"])

    def test_tampered_geometry_fails(self):
        out, _ = self._sign("v2-round42")
        svg = out.read_text()
        m = __import__("re").search(r'data-lx="([0-9.]+)"', svg)
        self.assertIsNotNone(m)
        changed = svg.replace(m.group(0), f'data-lx="{float(m.group(1)) + 1e-3:.9f}"', 1)
        v = self.sp.verify_seal_svg(changed, payload="profiled production seal", secret_key=self.SECRET)
        self.assertFalse(v["verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
