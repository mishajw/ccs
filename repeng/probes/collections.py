from typing import Literal

from repeng.activations.probe_preparations import ProbeArrays
from repeng.probes.base import BaseProbe
from repeng.probes.contrast_consistent_search import CcsTrainingConfig, train_ccs_probe
from repeng.probes.linear_artificial_tomography import (
    LatTrainingConfig,
    train_lat_probe,
)
from repeng.probes.logistic_regression import train_lr_probe, train_paired_lr_probe
from repeng.probes.mean_mass_probe import train_mmp_probe

ProbeId = Literal["ccs", "lat", "mmp", "mmp-iid", "lr", "lr-paired"]


def train_probe(probe_id: ProbeId, probe_arrays: ProbeArrays) -> BaseProbe | None:
    if probe_id == "ccs":
        if probe_arrays.paired is None:
            return None
        return train_ccs_probe(
            probe_arrays.paired,
            CcsTrainingConfig(),
        )
    elif probe_id == "lat":
        return train_lat_probe(
            probe_arrays.activations,
            LatTrainingConfig(),
        )
    elif probe_id == "mmp":
        return train_mmp_probe(
            probe_arrays.labeled,
            use_iid=False,
        )
    elif probe_id == "mmp-iid":
        return train_mmp_probe(
            probe_arrays.labeled,
            use_iid=True,
        )
    elif probe_id == "lr":
        return train_lr_probe(
            probe_arrays.labeled,
        )
    elif probe_id == "lr-paired":
        if probe_arrays.labeled_paired is None:
            return None
        return train_paired_lr_probe(
            probe_arrays.labeled_paired,
        )
    else:
        raise ValueError(f"Unknown probe_id: {probe_id}")
