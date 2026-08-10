"""
Hidden pyrophosphorylation page.

This module adds a self-contained, *unlisted* page to the Sitetack webserver that
runs ONLY the pyrophosphorylation models that are in development (the four models
in the PyroPhos_prediction project folder):

    1. Without labels          - trained on raw sequence, no known sites encoded
    2. With phos labels        - known phosphorylation sites encoded in the input
    3. With pyrophos labels    - known pyrophosphorylation sites encoded in the input
    4. With both               - known phosphorylation AND pyrophosphorylation sites encoded

The prediction logic is identical to the main site (see ``sitetack.app.predict``):
each sequence is broken into fixed-length kmers centered on the target residues,
one-hot encoded against a model-specific alphabet, and scored by the model's CNN.

The page is not linked anywhere and is served under an unguessable path
(``PYROPHOS_PATH_TOKEN``) so it is not discoverable by the public, while still
being shareable with collaborators via the direct URL.
"""

import os
import importlib.resources
from pathlib import Path
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict

from fastapi import FastAPI
from pydantic.main import BaseModel
from pydantic.class_validators import validator
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from sitetack.app.alphabet import Alphabet
from sitetack.app.fasta import Fasta
from sitetack.app.model import Model
from sitetack.app.predict import (
    Predict,
    SitePrediction,
    SequencePrediction,
    SequencePredictions,
)


# ---------------------------------------------------------------------------
# Unguessable URL for the hidden page.
#
# The page is served at   /pyrophos-<PYROPHOS_PATH_TOKEN>/
# Change it any time by setting the PYROPHOS_PATH_TOKEN environment variable
# (e.g. in the .env file used by docker-compose). Rotating the token instantly
# revokes every old link.
# ---------------------------------------------------------------------------
PYROPHOS_PATH_TOKEN = os.environ.get("PYROPHOS_PATH_TOKEN", "4ed5bf104a2ef7761ce550e8")
PYROPHOS_PREFIX = f"/pyrophos-{PYROPHOS_PATH_TOKEN}"


# ---------------------------------------------------------------------------
# Model configuration.
#
# NOTE: The alphabet strings and target amino acids below MUST exactly match how
# each model was trained (indices come from enumerate(alphabet), so both the
# membership AND the order matter -- a mismatch silently produces meaningless
# probabilities). These values are taken directly from the training pipeline that
# produced the deployed Trial* models, PyroPhos_prediction/Processing_kmers.ipynb:
#     alphabet_without_labels = "ARNDCEQGHILKMFPSTWYV@&-UX"
#     alphabet_with_labels    = "ARNDCEQGHILKMFPSTWYV@&$%-UX"
# Label symbols mark KNOWN sites, encoded in place of the residue:
#     '@' = known phospho-serine     '&' = known phospho-threonine
#     '$' = known pyrophospho-serine '%' = known pyrophospho-threonine
# The alphabet is chosen by the no-labels / with-labels axis (NOT by model
# family): the two no-labels models share the first string, the two with-labels
# models share the second. (In the "no labels" string @ & are present but only
# actually used by the phos-primed model; the padding/U/X indices differ between
# the two strings, which is exactly why each model must use its own.)
# ---------------------------------------------------------------------------

# Residues that pyrophosphorylation is scored on: pre-phosphorylated Ser/Thr.
# From Processing_kmers.ipynb / Model_training.ipynb: PR='S', PR2='T'.
PYROPHOS_AMINO_ACIDS: List[str] = ["S", "T"]

_ALPHABET_NO_LABELS = "ARNDCEQGHILKMFPSTWYV@&-UX"
_ALPHABET_WITH_LABELS = "ARNDCEQGHILKMFPSTWYV@&$%-UX"


@dataclass(frozen=True)
class PyrophosModelMetadata:
    """Describes one of the four in-development pyrophosphorylation models."""

    name: str                 # display name shown in the dropdown
    description: str          # help text shown under the dropdown
    h5_filename: str         # file inside sitetack/models_pyrophos/
    alphabet: str            # one-hot alphabet, must match how the model was trained
    amino_acids: List[str] = field(default_factory=lambda: list(PYROPHOS_AMINO_ACIDS))


class PyrophosModelKind(Enum):
    """The four pyrophosphorylation models, in the order requested."""

    NO_LABELS = PyrophosModelMetadata(
        name="Without labels",
        description=(
            "Predicts pyrophosphorylation from sequence alone; no known "
            "modification sites are encoded in the input."
        ),
        h5_filename="pyrophos_no_labels.h5",
        alphabet=_ALPHABET_NO_LABELS,
    )
    WITH_PHOS_LABELS = PyrophosModelMetadata(
        name="With phos labels",
        description=(
            "Encodes known phosphorylation sites in the input. Mark known "
            "phospho sites with '@' (phospho-serine) and '&' (phospho-threonine) "
            "in the submitted sequence."
        ),
        h5_filename="pyrophos_with_phos_labels.h5",
        # No-labels model of the phos-primed family: uses the no-labels alphabet
        # (which already contains @ & for the encoded phospho sites).
        alphabet=_ALPHABET_NO_LABELS,
    )
    WITH_PYROPHOS_LABELS = PyrophosModelMetadata(
        name="With pyrophos labels",
        description=(
            "Encodes known pyrophosphorylation sites in the input. Mark known "
            "pyrophos sites with '$' (pyrophospho-serine) and '%' "
            "(pyrophospho-threonine) in the submitted sequence."
        ),
        h5_filename="pyrophos_with_labels.h5",
        alphabet=_ALPHABET_WITH_LABELS,
    )
    WITH_BOTH = PyrophosModelMetadata(
        name="With both",
        description=(
            "Encodes both known phosphorylation and pyrophosphorylation sites. "
            "Mark phospho sites with '@' (Ser) / '&' (Thr) and pyrophos sites "
            "with '$' (Ser) / '%' (Thr) in the submitted sequence."
        ),
        h5_filename="pyrophos_with_phos_labels_with_labels.h5",
        alphabet=_ALPHABET_WITH_LABELS,
    )


# ---------------------------------------------------------------------------
# Motif cohorts.
#
# Each label variant above ships three models: one trained on every curated site
# ("general"), one on sites matching the CK2 consensus, and one on the rest. A
# submission is scored by all three so the tracks can be compared directly --
# see COHORTS below for what each is good for.
#
# Cohort files are the label variant's filename with a "__<cohort>" suffix; the
# general model keeps the original bare name.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CohortMetadata:
    """One of the three models run for every submission."""

    key: str           # identifier used in the JSON response
    name: str          # column heading in the UI
    description: str
    suffix: str        # appended to the label variant's filename stem


class CohortKind(Enum):
    GENERAL = CohortMetadata(
        key="general",
        name="General",
        description="Trained on every curated pyrophosphorylation site.",
        suffix="",
    )
    CK2 = CohortMetadata(
        key="ck2",
        name="CK2 motif",
        description=(
            "Trained only on sites whose +3 residue is E/D/S/T, against "
            "negatives from the same motif class."
        ),
        suffix="__ck2",
    )
    OTHER = CohortMetadata(
        key="other",
        name="Non-CK2",
        description=(
            "Trained only on sites that do not match the CK2 +3 motif. Built "
            "from 101 sites, so it is the least reliable of the three."
        ),
        suffix="__other",
    )


#: Residues at +3 that make a site CK2-like, including the label forms of S/T.
#: Mirrors pyrophos.motif.CK2_PLUS3_RESIDUES in the training repo.
CK2_PLUS3_RESIDUES = frozenset({"E", "D", "S", "T", "@", "&", "$", "%"})
PLUS3_OFFSET = 3


def is_ck2_motif(sequence: str, site: int) -> bool:
    """Whether the 1-based ``site`` matches the CK2 +3 consensus.

    A site whose +3 runs past the C-terminus is not CK2-like: there is no
    residue to satisfy the motif.
    """
    index = site - 1 + PLUS3_OFFSET
    return 0 <= index < len(sequence) and sequence[index] in CK2_PLUS3_RESIDUES


def pyrophos_models_directory() -> Path:
    """Directory that holds the four pyrophosphorylation .h5 model files."""
    return Model.get_directory_from_module("sitetack.models_pyrophos")


def get_h5_file(
    model: PyrophosModelKind, cohort: CohortKind = CohortKind.GENERAL
) -> Path:
    """Resolve the .h5 file for a (label variant, cohort) pair."""
    stem = model.value.h5_filename[: -len(".h5")]
    path = pyrophos_models_directory() / f"{stem}{cohort.value.suffix}.h5"
    if not path.exists():
        raise FileNotFoundError(
            f"Pyrophosphorylation model file not found: {path}. "
            f"Copy the trained model into sitetack/models_pyrophos/ (see the "
            f"README there)."
        )
    return path


def get_alphabet(model: PyrophosModelKind) -> Alphabet:
    """Alphabet used to one-hot encode inputs for a pyrophosphorylation model."""
    return Alphabet(str=model.value.alphabet)


def predict_on_fasta(
    fasta_text: str,
    model: PyrophosModelKind,
    cohort: CohortKind = CohortKind.GENERAL,
) -> SequencePredictions:
    """
    Predict pyrophosphorylation probabilities for every target site in the fasta
    text. Mirrors ``Predict.on_fasta`` but uses the pyrophos model configuration.
    """
    meta = model.value
    alphabet = get_alphabet(model)
    h5_file = get_h5_file(model, cohort)
    sequences = Fasta.read_sequences_from_text(fasta_text)

    sequence_predictions = []
    for sequence in sequences:
        kmers = [
            kmer
            for amino_acid in meta.amino_acids
            for kmer in sequence.get_kmers(Predict.KMER_LENGTH, amino_acid)
        ]
        probabilities = Predict.on_kmers(kmers, alphabet, h5_file)
        site_predictions = [
            SitePrediction(kmer.site, kmer.amino_acid, probability)
            for kmer, probability in zip(kmers, probabilities)
        ]
        sequence_predictions.append(
            SequencePrediction(sequence.sequence_name, sequence.sequence, site_predictions)
        )
    return SequencePredictions(sequence_predictions)


def predict_all_cohorts(fasta_text: str, model: PyrophosModelKind) -> Dict:
    """Score a submission with all three cohort models and merge the results.

    Returns one entry per sequence, each carrying every target site once with a
    score from each cohort plus the site's CK2 motif call:

        {"sequences": [
            {"sequence_name": ..., "sequence": ...,
             "sites": [{"site": 12, "amino_acid": "S", "is_ck2_motif": true,
                        "scores": {"general": 0.8, "ck2": 0.9, "other": 0.3},
                        "routed": 0.9}, ...]}]}

    ``routed`` is the score from the cohort matching the site's own motif class
    -- the CK2 model for CK2-motif sites, the non-CK2 model otherwise. It is a
    convenience: every underlying score is present, so the caller can aggregate
    differently without re-submitting.
    """
    by_cohort = {
        cohort.value.key: predict_on_fasta(fasta_text, model, cohort) for cohort in CohortKind
    }

    general = by_cohort[CohortKind.GENERAL.value.key]
    sequences = []
    for index, sequence_prediction in enumerate(general.sequence_predictions):
        sequence = sequence_prediction.sequence
        sites = []
        for site_index, site_prediction in enumerate(sequence_prediction.site_predictions):
            scores = {
                key: predictions.sequence_predictions[index]
                .site_predictions[site_index]
                .probability
                for key, predictions in by_cohort.items()
            }
            ck2_motif = is_ck2_motif(sequence, site_prediction.site)
            sites.append(
                {
                    "site": site_prediction.site,
                    "amino_acid": site_prediction.amino_acid,
                    "is_ck2_motif": ck2_motif,
                    "scores": scores,
                    "routed": scores[
                        CohortKind.CK2.value.key if ck2_motif else CohortKind.OTHER.value.key
                    ],
                }
            )
        sites.sort(key=lambda entry: entry["site"])
        sequences.append(
            {
                "sequence_name": sequence_prediction.sequence_name,
                "sequence": sequence,
                "sites": sites,
            }
        )

    return {
        "cohorts": [
            {
                "key": cohort.value.key,
                "name": cohort.value.name,
                "description": cohort.value.description,
            }
            for cohort in CohortKind
        ],
        "sequences": sequences,
    }


def models_to_dict() -> Dict[str, Dict]:
    """Serialize the four label variants for the frontend dropdown."""
    d: Dict[str, Dict] = {}
    for kind in PyrophosModelKind:
        value = asdict(kind.value)
        # The frontend only needs display fields; drop server-side internals.
        d[kind.name] = {"name": value["name"], "description": value["description"]}
    return d


def cohorts_to_dict() -> List[Dict]:
    """Serialize the three cohort models for the frontend legend."""
    return [
        {
            "key": cohort.value.key,
            "name": cohort.value.name,
            "description": cohort.value.description,
        }
        for cohort in CohortKind
    ]


# ---------------------------------------------------------------------------
# Request model + routes
# ---------------------------------------------------------------------------
class PyrophosRequest(BaseModel):
    model: str
    text: str

    @validator("model", always=True)
    def model_must_be_valid(cls, value):
        if value not in PyrophosModelKind.__members__:
            raise ValueError("Invalid pyrophosphorylation model")
        return value

    @validator("text", pre=False, always=True)
    def validate_text(cls, value, values):
        model_name = values.get("model")
        if model_name:
            model = PyrophosModelKind[model_name]
            alphabet = get_alphabet(model)
            is_valid, error_message = Fasta.validate_fasta_text(value, alphabet=alphabet)
            if not is_valid:
                raise ValueError(error_message)
        return value


async def _get_form():
    with importlib.resources.path("sitetack.frontend_pyrophos", "index.html") as import_path:
        filepath = Path(import_path)
    with open(filepath, "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


async def _get_models():
    # Deliberately the bare {NAME: {...}} mapping, NOT wrapped in a envelope.
    # A cached copy of an older script.js iterates this response's top-level
    # keys to build the dropdown, so adding a sibling key here silently breaks
    # every browser holding that cache: the dropdown fills with the envelope's
    # own keys and submitting posts "models" as the model name. Cohorts are
    # served separately by _get_cohorts for exactly this reason.
    return models_to_dict()


async def _get_cohorts():
    return cohorts_to_dict()


async def _submit_data(request: PyrophosRequest):
    model = PyrophosModelKind[request.model]
    return predict_all_cohorts(request.text, model)


def register(app: FastAPI) -> None:
    """
    Attach the hidden pyrophosphorylation page to the main app.

    Every route lives under the unguessable ``PYROPHOS_PREFIX`` and nothing on
    the public site links to it. Registering routes directly on the app (rather
    than via an APIRouter) keeps this compatible with the repo's pinned
    FastAPI 0.9 / Starlette 0.11 stack.
    """
    # Static assets (script.js, style.css) under the same unguessable prefix.
    with importlib.resources.path("sitetack.frontend_pyrophos", "") as frontend_path:
        app.mount(
            f"{PYROPHOS_PREFIX}/frontend",
            StaticFiles(directory=str(frontend_path)),
            name="frontend_pyrophos",
        )

    app.add_api_route(f"{PYROPHOS_PREFIX}/", _get_form, methods=["GET"])
    app.add_api_route(f"{PYROPHOS_PREFIX}/models", _get_models, methods=["GET"])
    app.add_api_route(f"{PYROPHOS_PREFIX}/cohorts", _get_cohorts, methods=["GET"])
    app.add_api_route(f"{PYROPHOS_PREFIX}/submit/", _submit_data, methods=["POST"])
