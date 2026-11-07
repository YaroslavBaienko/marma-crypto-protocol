r"""
Marma-Crypto v2.3.0 — Universal Geometric Vector Watermarking, Optical Traitor Tracing & Subhash Kak Synthesis Suite
====================================================================================================================
Modules:
- `universal_qim`: Generalized 27-DOF Keyed Dithered QIM over arbitrary 2D contours
  (`sri-yantra`, `tryzub` Ukrainian Trident, `corporate-shield`, `cad-polygon`)
- `optical_ecc`: [32, 16, d_min=8] Polar-Sector Optical Error-Correcting Ring for
  smartphone screen-photo / print-camera leak attribution
- `api_server`: Zero-dependency HTTP REST microservice & high-throughput Deal-Room batch sealer
- `kak_synthesis_v23`: Subhash Kak 40-Paper Corpus Synthesis Engine (`v2.3.0`):
  * 54-Marma Nonlinear Incidence Determinant & 7 Coupled Ordinate Verifier (`VEDI-L10-0245`, `0250`, `0251`, `0252`)
  * Prime-Reciprocal Decimal Sequence (`d`-Sequence) QIM Schedule over Fermat prime $q = 257$ (`VEDI-L10-0256`)
  * Recursive Threshold 23-Bit Extended Leak Attribution ($8,388,608$ recipients, $0.0\text{ nm}$ extra RMSE, `VEDI-L10-0258`)
  * Hierarchical Dual-Layer Augmented Watermarking (`Public Keyless + Forensic Keyed`, `VEDI-L10-0253`)
  * Pythagorean-Triple Unit-Circle Angular Phase Coding (`VEDI-L10-0260`), Nārāyaṇa Universal Prefix Code (`VEDI-L10-0261`),
    Kaṭapayādi Sanskrit Seed Digest (`VEDI-L10-0235`), and Yamātārājabhānasalagām De Bruijn Register (`VEDI-L10-0239`)
  * 40-Document Subhash Kak Corpus Cross-Validation & Cross-Verification Engine (`VEDI-L10-0223` .. `VEDI-L10-0262`)
"""

from .api_server import (
    API_VERSION,
    MarmaDealRoomServer,
    batch_seal_dealroom,
    dispatch_api_request,
    stamp_pdf_universal_v21,
    trace_leak_any_medium,
    verify_pdf_universal_v21,
)
from .kak_synthesis_v23 import (
    COUPLED_TRIPLE_LINE_MARMAS_19,
    EXACT_TRIPLE_LINE_MARMAS_29,
    KAK_40_CORPUS_MAP,
    MARMA_V23_PROTOCOL_ID,
    MARMA_V23_VERSION,
    MAX_RECIPIENTS_V23,
    OUTER_CIRCLE_CONTACT_MARMAS_6,
    PPT_CODEBOOK_64,
    SHARED_ORDINATE_IDENTITIES_7,
    compute_cyclic_autocorrelation,
    cross_validate_kak_corpus_v23,
    decode_narayana_universal_v23,
    decode_ppt_unit_circle_v23,
    decode_recursive_23bit_recipient_v23,
    derive_dsequence_qim_schedule_v23,
    derive_recipient_23bit_token,
    encode_narayana_universal_v23,
    encode_ppt_unit_circle_v23,
    encode_recursive_23bit_recipient_v23,
    evaluate_kak_mathematical_invariants_v23,
    generate_prime_d_sequence,
    generate_prime_remainder_orbit,
    generate_primitive_pythagorean_triples_v23,
    katapayadi_seed_digest_v23,
    narayana_sequence_v23,
    stamp_augmented_dual_layer_v23,
    verify_augmented_dual_layer_v23,
    verify_sri_yantra_marma_concurrency_v23,
    yamatarajabhanasalagam_debruijn_v23,
)
from .optical_ecc import (
    compute_doc_tag6,
    decode_optical_codeword32_soft,
    draw_optical_lotus_ring_pdf,
    encode_optical_codeword32,
    extract_canary_from_raster_image,
    render_optical_seal_png,
)
from .universal_qim import (
    CANONICAL_CAD_POLYGON_CONTOURS,
    CANONICAL_CORPORATE_SHIELD_CONTOURS,
    CANONICAL_TRYZUB_CONTOURS,
    SUPPORTED_EMBLEMS,
    build_perturbed_emblem_v21,
    demodulate_arbitrary_2d_vertices,
    get_canonical_emblem_contours,
    modulate_arbitrary_2d_vertices,
    recover_256bit_from_emblem_v21,
    stamp_universal_svg_drawing,
    verify_emblem_coordinates_v21,
    verify_universal_svg_drawing,
)

__version__ = API_VERSION

__all__ = [
    "API_VERSION",
    "__version__",
    "SUPPORTED_EMBLEMS",
    "CANONICAL_TRYZUB_CONTOURS",
    "CANONICAL_CORPORATE_SHIELD_CONTOURS",
    "CANONICAL_CAD_POLYGON_CONTOURS",
    "get_canonical_emblem_contours",
    "build_perturbed_emblem_v21",
    "recover_256bit_from_emblem_v21",
    "verify_emblem_coordinates_v21",
    "modulate_arbitrary_2d_vertices",
    "demodulate_arbitrary_2d_vertices",
    "stamp_universal_svg_drawing",
    "verify_universal_svg_drawing",
    "compute_doc_tag6",
    "encode_optical_codeword32",
    "decode_optical_codeword32_soft",
    "draw_optical_lotus_ring_pdf",
    "render_optical_seal_png",
    "extract_canary_from_raster_image",
    "stamp_pdf_universal_v21",
    "verify_pdf_universal_v21",
    "batch_seal_dealroom",
    "trace_leak_any_medium",
    "dispatch_api_request",
    "MarmaDealRoomServer",
    "COUPLED_TRIPLE_LINE_MARMAS_19",
    "EXACT_TRIPLE_LINE_MARMAS_29",
    "KAK_40_CORPUS_MAP",
    "MARMA_V23_PROTOCOL_ID",
    "MARMA_V23_VERSION",
    "MAX_RECIPIENTS_V23",
    "OUTER_CIRCLE_CONTACT_MARMAS_6",
    "PPT_CODEBOOK_64",
    "SHARED_ORDINATE_IDENTITIES_7",
    "compute_cyclic_autocorrelation",
    "cross_validate_kak_corpus_v23",
    "decode_narayana_universal_v23",
    "decode_ppt_unit_circle_v23",
    "decode_recursive_23bit_recipient_v23",
    "derive_dsequence_qim_schedule_v23",
    "derive_recipient_23bit_token",
    "encode_narayana_universal_v23",
    "encode_ppt_unit_circle_v23",
    "encode_recursive_23bit_recipient_v23",
    "evaluate_kak_mathematical_invariants_v23",
    "generate_prime_d_sequence",
    "generate_prime_remainder_orbit",
    "generate_primitive_pythagorean_triples_v23",
    "katapayadi_seed_digest_v23",
    "narayana_sequence_v23",
    "stamp_augmented_dual_layer_v23",
    "verify_augmented_dual_layer_v23",
    "verify_sri_yantra_marma_concurrency_v23",
    "yamatarajabhanasalagam_debruijn_v23",
]
