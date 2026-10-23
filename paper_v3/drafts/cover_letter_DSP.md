# Cover letter — Digital Signal Processing (transfer from Signal Processing)

Dear Editors,

Please consider the transferred manuscript **“Fragile Authentication of PDF Signatures via
Bit-Exact Quantization Index Modulation on Vector Geometry”** (transferred from
*Signal Processing*, manuscript SIGPRO-D-26-04464) for publication in *Digital Signal
Processing*.

**Why this journal.** The paper is a watermarking/signal-processing study, not a cryptography
protocol paper: it asks how a fragile payload can be carried by the geometry of a visible mark,
how exact (bit-for-bit) recovery can be achieved with dithered quantization index modulation, and
what capacity–distortion trade-off results on a fixed 27-degree-of-freedom carrier. Those are core
DSP questions, and the manuscript is now written for that readership.

**What changed on transfer.** The transferred file was the earlier submission. Before completing
this submission I have revised it substantially:
- a new title and abstract framed for the DSP/watermarking readership (the earlier title carried a
  protocol/legal framing that belonged to a different community);
- a rebuilt, verified bibliography (every citation resolves to a DOI, standard or book; the earlier
  draft contained references that could not be verified, and they were removed);
- a new PDF-level evaluation on a 180-file corpus from three document generators (LibreOffice,
  Typst, Chromium print) in native, flattened and print-scan-simulated variants, with a carrier
  ablation and same-carrier baselines;
- optical/screen-photo and API material moved out of this paper into a companion manuscript.

**What the paper claims and does not claim.** It reports exact recovery of a 266-bit payload,
fragility to coordinate edits and re-serialisation, fail-closed behaviour under flattening, and a
capacity–distortion comparison in which capacity-limited baselines are reported as such. It does not
claim cryptographic security from a watermarking argument, and it explicitly complements rather than
replaces PAdES/eIDAS signatures.

**Declarations.** The manuscript is not under consideration elsewhere; the preprint is archived on
Zenodo (concept DOI 10.5281/zenodo.23429017) and SSRN (10.2139/ssrn.7631458); a Ukrainian patent
application (a 2026 06266) covers the sealing method. I am happy to provide the evaluation harness
and corpus manifest for reproducibility.

Thank you for considering the transfer.

Sincerely,
Yaroslav V. Baienko
