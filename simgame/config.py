"""Defines some common accessor functions."""

import os
from pathlib import Path


def get_model_dir() -> Path:
    if "MODEL_DIR" not in os.environ:
        raise KeyError("Set the MODEL_DIR environment variable")
    return Path(os.environ["MODEL_DIR"]).resolve() / "maniskill"
