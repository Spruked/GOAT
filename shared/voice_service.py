import sys
import os
import tempfile
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Phonatory_Output_Module'))

import os
from phonitory_output_module import PhonatoryOutputModule

_pom = None

def get_pom():
    global _pom
    if _pom is None:
        _pom = PhonatoryOutputModule()
    return _pom

def generate_voice(text, voice="cali", style="default"):
    pom = get_pom()
    # Create a temporary file for the output
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_path = temp_file.name
    
    # Use phonate which saves to file
    output_path = pom.phonate(text, out_path=temp_path, pitch_factor=1.0)  # Adjust params as needed
    return output_path