# Pyrophosphorylation models (in development)

The hidden pyrophosphorylation page (`sitetack/app/pyrophos.py`) loads **twelve**
models from this directory: four label variants × three motif cohorts. Every
submission is scored by all three cohorts of the selected label variant, so the
page can show how splitting by the CK2 motif changes each site.

All twelve are committed via Git LFS, alongside a `.model_card.json` each.

## Layout

| Label variant (dropdown) | general | `__ck2` | `__other` |
|---|---|---|---|
| Without labels | `pyrophos_no_labels.h5` | `pyrophos_no_labels__ck2.h5` | `pyrophos_no_labels__other.h5` |
| With phos labels | `pyrophos_with_phos_labels.h5` | `…__ck2.h5` | `…__other.h5` |
| With pyrophos labels | `pyrophos_with_labels.h5` | `…__ck2.h5` | `…__other.h5` |
| With both | `pyrophos_with_phos_labels_with_labels.h5` | `…__ck2.h5` | `…__other.h5` |

The general models keep their original bare filenames, so an older deployment
that only knows about four files still resolves them.

## Cohorts

- **general** — trained on all 308 curated human sites.
- **ck2** — trained only on the 207 sites whose +3 residue is E/D/S/T, against
  negatives drawn from the *same* motif class. Because the negatives are motif-
  matched, this model cannot score well merely by detecting the motif.
- **other** — trained on the remaining 101 sites, against non-CK2 negatives.
  Built from far less data; it is the least reliable of the three.

`pyrophos.is_ck2_motif` implements the +3 rule and mirrors `pyrophos.motif` in
the training repo. The `routed` score returned per site is the cohort model
matching that site's own motif class.

## Held-out test AUC (10 trials each, mean ± std)

| Label variant | general | ck2 | other | routed bulk |
|---|---|---|---|---|
| Without labels | 0.8730 ± 0.045 | 0.8970 ± 0.030 | 0.7840 ± 0.124 | 0.8607 ± 0.039 |
| With phos labels | 0.8786 ± 0.047 | 0.9079 ± 0.032 | 0.7912 ± 0.149 | 0.8677 ± 0.039 |
| With pyrophos labels | 0.9021 ± 0.035 | 0.9206 ± 0.032 | 0.7965 ± 0.109 | 0.8818 ± 0.035 |
| With both | 0.9047 ± 0.035 | 0.9250 ± 0.035 | 0.8185 ± 0.108 | 0.8717 ± 0.087 |

Read those with care:

- The **CK2 model beats the general model** in every label variant.
- The **non-CK2 model is weak and high-variance** — 101 positives is not much.
- The **routed combination lands below the general model** every time, because
  routing sends every non-CK2 site through the weaker specialist. The three
  tracks are shown side by side on the page precisely so this is visible rather
  than hidden inside one number.

Numbers are means across ten trials, not the exported trial's own score (which
is a maximum over ten and biased upward).

## Provenance

Trained by [`pyrophos-dev`](https://github.com/clair-gutierrez/pyrophos-dev)
(`PyroPhos_prediction/pyrophos-dev`) against `_master_pyrosites_processed.xlsx`.
Each `.model_card.json` records the alphabet, window length, target residues,
architecture, training seed and metrics for its `.h5`.

To regenerate and redeploy:

```sh
cd pyrophos-dev
uv run pyrophos train                                   # general -> runs/
uv run pyrophos train --cohorts ck2 other --runs-dir runs_cohorts
uv run pyrophos export                                  # -> models/
uv run pyrophos export --runs-dir runs_cohorts
uv run pyrophos deploy ../sitetack
```

## Alphabets (confirmed — do not change unless retraining)

Chosen by the pyrophos-labels axis only; the cohort does not affect encoding.

| Label variant | Alphabet |
|---|---|
| Without labels, With phos labels | `ARNDCEQGHILKMFPSTWYV@&-UX` |
| With pyrophos labels, With both | `ARNDCEQGHILKMFPSTWYV@&$%-UX` |

Target residues: **S, T**. Label symbols encode KNOWN sites in place of the
residue: `@` phospho-Ser, `&` phospho-Thr, `$` pyrophospho-Ser, `%`
pyrophospho-Thr.

The one-hot index comes from `enumerate(alphabet)` and feeds an `Embedding`
sized 256, so a mismatched alphabet does **not** raise — it silently produces
meaningless probabilities. `tests/app/test_pyrophos.py` checks every model card's
declared alphabet against the string used to encode for it.

## Git LFS

`*.h5` is tracked by Git LFS (see `.gitattributes`). Confirm with
`git lfs ls-files` before pushing.
