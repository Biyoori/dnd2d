import importlib
import os

FEAT_REGISTRY = {}

FEAT_FOLDER = "feats"

for filename in os.listdir(FEAT_FOLDER):
    if filename.endswith(".py") and filename is not "__init__.py":
        featName = filename[:-3]
        FEAT_REGISTRY[featName.capitalize()] = f"{FEAT_FOLDER}.{featName}"

def getFeat(featName):
    if featName in FEAT_REGISTRY:
        moduleName = FEAT_REGISTRY[featName]
        module = importlib.import_module(moduleName)
        return getattr(module, f"{featName.lower()}")
    raise ValueError(f"Feat '{featName}' not found.")