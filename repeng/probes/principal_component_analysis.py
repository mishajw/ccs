"""
Implementation of PCA based probes.

Grouped PCA probe is equivalent to CRC-TPC described in
<https://arxiv.org/abs/2212.03827>.
"""

import numpy as np
from jaxtyping import Float, Int64
from sklearn.decomposition import PCA

from repeng.probes.base import DotProductProbe
from repeng.probes.normalization import normalize_by_group


def train_pca_probe(
    *,
    activations: Float[np.ndarray, "n d"],  # noqa: F722
    answer_types: Int64[np.ndarray, "n d"] | None,  # noqa: F722
) -> DotProductProbe:
    if answer_types is not None:
        activations = normalize_by_group(activations, answer_types)
    activations = activations - activations.mean(axis=0)
    pca = PCA(n_components=1)
    pca.fit_transform(activations)
    probe = pca.components_.squeeze(0)
    probe = probe / np.linalg.norm(probe)
    return DotProductProbe(probe=probe)


def train_grouped_pca_probe(
    *,
    activations: Float[np.ndarray, "n d"],  # noqa: F722
    groups: Float[np.ndarray, "n"],  # noqa: F821
    answer_types: Int64[np.ndarray, "n d"] | None,  # noqa: F722
) -> DotProductProbe:
    activations = normalize_by_group(activations, groups)
    return train_pca_probe(activations=activations, answer_types=answer_types)
