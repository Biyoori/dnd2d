import importlib
import os

FEAT_REGISTRY = {}

FEAT_FOLDER = "feats"

for filename in os.listdir(FEAT_FOLDER):
    if filename.endswith(".py") and filename is not "__init__.py":
        feat_name = filename[:-3]
        FEAT_REGISTRY[feat_name.capitalize()] = f"{FEAT_FOLDER}.{feat_name}"

def get_feat(feat_name: str):
    if feat_name in FEAT_REGISTRY:
        module_name = FEAT_REGISTRY[feat_name]
        module = importlib.import_module(module_name)
        return getattr(module, f"{feat_name.lower()}")
    raise ValueError(f"Feat '{feat_name}' not found.")