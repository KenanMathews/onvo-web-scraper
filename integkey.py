import os
import pickle

class IntegrationKeyManager:
    def __init__(self, filepath):
        self._filepath = filepath
        self._integration_key = None
        self._create_integration_key_file()

    @property
    def integration_key(self):
        return self._integration_key
    
    @integration_key.setter
    def integration_key(self, value):
        self._integration_key = value
        self._save_integration_key()

    def _create_integration_key_file(self):
        if not os.path.exists(self._filepath):
            with open(self._filepath, 'wb') as f:
                pickle.dump(None, f)

    def _save_integration_key(self):
        with open(self._filepath, 'wb') as f:
            pickle.dump(self._integration_key, f)
    
    def load_integration_key(self):
        try:
            with open(self._filepath, 'rb') as f:
                self._integration_key = pickle.load(f)
        except FileNotFoundError:
            print("Integration key file not found. Initializing with empty string.")
            self._integration_key = ""
        return self._integration_key
if __name__ == "__main__":
    manager = IntegrationKeyManager("integration_key.pkl")
    manager.load_integration_key()
    print("Integration Key:", manager.integration_key)
