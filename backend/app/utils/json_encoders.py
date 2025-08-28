import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that converts NumPy types to native Python types
    so they can be serialized to JSON.
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # Let the base class default method raise the TypeError for other types
        return json.JSONEncoder.default(self, obj)