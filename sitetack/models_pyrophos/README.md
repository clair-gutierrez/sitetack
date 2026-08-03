# Pyrophosphorylation models (in development)

The hidden pyrophosphorylation page (`sitetack/app/pyrophos.py`) loads its four
models from this directory. The four `.h5` files below are already in place
(committed via Git LFS) — a working default set selected as the **best-AUC fold**
from each model's 10-fold cross-validation.

| Dropdown option        | File in this folder                          | Default source (`PyroPhos_prediction/Trained_models_data/`)              | Val AUC |
|------------------------|----------------------------------------------|-------------------------------------------------------------------------|---------|
| Without labels         | `pyrophos_no_labels.h5`                      | `Trial2/_emb_CNN_no_labels_Trial2.h5`                                   | 0.9724  |
| With phos labels       | `pyrophos_with_phos_labels.h5`              | `Trial3_with_phos_labels/_emb_CNN_no_labels_Trial3_with_phos_labels.h5` | 0.9794  |
| With pyrophos labels   | `pyrophos_with_labels.h5`                   | `Trial7/_emb_CNN_with_labels_Trial7.h5`                                 | 0.9986  |
| With both              | `pyrophos_with_phos_labels_with_labels.h5`  | `Trial6_with_phos_labels/_emb_CNN_with_labels_Trial6_with_phos_labels.h5` | 0.9958 |

## Swapping in a different trial

To deploy a different fold, copy that trial's file over the matching name above.
The naming pattern in `Trained_models_data/` is:

- Base family:        `Trial<N>/_emb_CNN_{no,with}_labels_Trial<N>.h5`
- Phos-primed family: `Trial<N>_with_phos_labels/_emb_CNN_{no,with}_labels_Trial<N>_with_phos_labels.h5`

where `no_labels` = the pyrophos-labels-OFF model and `with_labels` = the
pyrophos-labels-ON model.

## Alphabets (confirmed — do not change unless retraining)

Taken directly from the training pipeline (`Processing_kmers.ipynb`). The one-hot
index comes from `enumerate(alphabet)`, so order and membership must match exactly:

| Model axis                       | Alphabet (in `app/pyrophos.py`)   |
|----------------------------------|-----------------------------------|
| no-labels (Without / With phos)  | `ARNDCEQGHILKMFPSTWYV@&-UX`        |
| with-labels (Pyrophos / Both)    | `ARNDCEQGHILKMFPSTWYV@&$%-UX`      |

Target residues: **S, T** (`PR='S'`, `PR2='T'`). Label symbols encode KNOWN sites
in place of the residue: `@` phospho-Ser, `&` phospho-Thr, `$` pyrophospho-Ser,
`%` pyrophospho-Thr.

## Git LFS

`*.h5` is tracked by Git LFS (see `.gitattributes`), so these files commit via LFS
like the rest of the models.
