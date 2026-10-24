// Independent JavaScript implementation of the word<->lattice map, used for cross-runtime
// verification of the Python implementation (paper_v3/eval/pdf_layer.py).
// word_to_delta(w) = round((18*w - 9207) * 1e-9, 9) ; delta_to_word(d) = round((d*1e9 + 9207)/18)
const toDelta = (w) => Number((((18 * w) - 9207) / 1e9).toFixed(9));
const toWord = (d) => Math.round((Math.round(d * 1e9) + 9207) / 18);
const out = { deltas: [], words: [] };
for (let w = 0; w < 1024; w++) {
  const d = toDelta(w);
  out.deltas.push(d);
  out.words.push(toWord(d));
}
process.stdout.write(JSON.stringify(out));
