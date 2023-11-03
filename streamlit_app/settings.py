from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# images
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'logo.png'

# model
MODEL_DIR = ROOT
# PREDICTION_MODEL = MODEL_DIR / 'model/modelv150.pkl'
PREDICTION_MODEL = MODEL_DIR / 'model/model_A.pkl'
PREDICTION_MODEL_CCSR = MODEL_DIR / 'model/pipeline_obj_updated.pkl'

#model_A_object
MODEL_A_OBJECT = ROOT
CCSR_ORDINAL_MAPPING = MODEL_A_OBJECT / 'model_A_object/ccsr_ordinal_mapping.json'
COUNTY_ORDINAL_MAPPING = MODEL_A_OBJECT / 'model_A_object/county_ordinal_mapping.json'
FACILITY_ORDINAL_MAPPING = MODEL_A_OBJECT / 'model_A_object/facility_ordinal_mapping.json'

# css stylesheet
CSS = MODEL_DIR/ 'css/style.css'

# javascipt file
JS = MODEL_DIR/ 'js/main.js'
