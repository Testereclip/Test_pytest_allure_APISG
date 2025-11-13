# tests/conftest.py

import sys
import os

# Agrega el directorio raíz del proyecto al path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
