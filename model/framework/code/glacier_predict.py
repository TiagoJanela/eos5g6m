"""GLACIER inference helper: SMILES -> 512-d multimodal embedding.

Loads the vendored Glacier model (student encoders + Finsler fusion) from the
bundled checkpoint and returns the 512-d fused embedding per molecule. All three
modalities (graph via chemprop, SMILES via a local tokenizer, RDKit
physicochemical descriptors) are derived internally from SMILES; no network
access and no teacher model are needed at inference. Invalid SMILES yield an
all-NaN row so the output stays aligned with the input, one row per molecule.
"""
import os
import sys

import numpy as np
import torch
from rdkit import Chem

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_HERE, "glacier_src")          # vendored model code + tokenizer
_CKPT = os.path.join(_HERE, "..", "..", "checkpoints")  # config.json + model.safetensors (eosvc)

EMB_DIM = 512  # GLACIER fused embedding dimension (config.json: fusion_dim / output_dim)
# The descriptor branch was trained on a fixed-length RDKit descriptor vector.
# rdkit must be pinned (see install.yml) so Descriptors.descList has this many
# entries; a different rdkit version silently changes the count and otherwise
# fails deep inside the model with an opaque shape error.
_EXPECTED_N_DESCRIPTORS = 217

# The vendored GLACIER code uses flat imports (`from encoders import ...`,
# `from data.dataloader import ...`), so its directory must be on sys.path.
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

_model = None


def _load_model():
    """Load and cache the Glacier model on CPU in eval mode."""
    global _model
    if _model is None:
        # Fail fast with a clear message if the rdkit descriptor count does not
        # match what the checkpoint expects (usually an rdkit version mismatch).
        from rdkit.Chem import Descriptors
        import rdkit

        n_desc = len(Descriptors.descList)
        if n_desc != _EXPECTED_N_DESCRIPTORS:
            raise RuntimeError(
                f"RDKit produces {n_desc} descriptors but GLACIER's descriptor "
                f"branch expects {_EXPECTED_N_DESCRIPTORS}. Pin the rdkit version "
                f"from install.yml (installed: {rdkit.__version__})."
            )

        from glacier_student import Glacier

        torch.set_num_threads(max(1, os.cpu_count() or 1))
        model = Glacier.from_pretrained(_CKPT)
        model.eval()
        _model = model
    return _model


def predict(smiles_list):
    """Return an (N, 512) float32 array of GLACIER embeddings.

    Invalid / unparseable SMILES produce an all-NaN row at the same position.
    """
    model = _load_model()
    from data.dataloader import SmilesMoleculeDataset, build_dataloader

    valid_idx, valid_smiles = [], []
    for i, smi in enumerate(smiles_list):
        if smi is not None and Chem.MolFromSmiles(smi) is not None:
            valid_idx.append(i)
            valid_smiles.append(smi)

    out = np.full((len(smiles_list), EMB_DIM), np.nan, dtype=np.float32)
    if valid_smiles:
        dataset = SmilesMoleculeDataset(smiles=valid_smiles)
        # shuffle=False is essential: the loader defaults to shuffle=True, which
        # would misalign embeddings to input SMILES.
        dataloader = build_dataloader(dataset, batch_size=64, shuffle=False)
        rows = []
        with torch.no_grad():
            for batch in dataloader:
                rows.append(model(batch).cpu().numpy().astype(np.float32))
        emb = np.concatenate(rows, axis=0)
        for row, i in enumerate(valid_idx):
            out[i] = emb[row]
    return out
