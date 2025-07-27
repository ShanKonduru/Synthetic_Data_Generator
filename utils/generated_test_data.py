# utils/generated_test_data.py
from typing import Any, Dict

class GeneratedTestData:
    """
    A wrapper class to hold the generated test data dictionary.
    Provides a .get_data() method to retrieve the dictionary.
    Also supports dictionary-like access (__getitem__, __contains__, etc.).
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def get_data(self) -> Dict[str, Any]:
        return self._data

    def __str__(self) -> str:
        return str(self._data)

    def __repr__(self) -> str:
        return f"GeneratedTestData({repr(self._data)})"

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def items(self):
        return self._data.items()

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()