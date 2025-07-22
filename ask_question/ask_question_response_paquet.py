"""
    File in charge of returning the user response under the form of a packet rather than an dictionnary
"""

from typing import Union, List, Any, Dict, get_type_hints, TypeVar, Type, Iterable, Generic

_KT = TypeVar("_KT")
VT = TypeVar("VT")


class AQFlexibleDictionary(Generic[_KT, VT]):
    """ Class in charge of emulating the functionalities of a dictionary as well as a C type structure 
    Class in charge of emulating the functionalities of a dictionary as well as a C type structure.

    Provides dictionary-like behavior with attribute access, default values from type hints,
    recursive dictionary wrapping, and support for serialization and merging.
    """

    def __init__(self, **kwargs) -> None:
        """
        Initialize a new AQFlexibleDictionary instance.

        Args:
            **kwargs: Key-value pairs to initialize the dictionary.

        Notes:
            Class attributes with type hints will be used as defaults if not overridden by kwargs.
        """
        # Store the name of the class
        self._class_name: str = self.__class__.__name__

        # initialise the reference dictionnary
        self._data: Dict[str, Any] = {}

        # Use type hints (if any) for default values
        defaults = {
            k: getattr(self.__class__, k)
            for k in get_type_hints(self.__class__)
            if hasattr(self.__class__, k)
        }

        # Load defaults first
        for key, value in defaults.items():
            self._data[key] = self._wrap(value)

        # Override with explicit kwargs
        for key, value in kwargs.items():
            self._data[key] = self._wrap(value)

    def _wrap(self, value):
        """
        Wraps nested dictionaries into AQFlexibleDictionary instances.

        Args:
            value: Any value, possibly a dict.

        Returns:
            The original value or an AQFlexibleDictionary if value is a dict.
        """
        if isinstance(value, Dict) and not isinstance(value, AQFlexibleDictionary):
            return self.__class__(**value)
        return value

    def __getattr__(self, name):
        """
        Fallback for attribute access when not found on the instance.

        Args:
            name: Attribute name.

        Returns:
            The corresponding value from internal data.

        Raises:
            AttributeError: If the key does not exist.
        """
        try:
            return self._data[name]
        except KeyError as e:
            raise AttributeError(
                f"'{self._class_name}' object has no attribute '{name}'"
            ) from e

    def __setattr__(self, name, value):
        """
        Sets an attribute or dictionary item.

        Args:
            name: Attribute name.
            value: Value to assign.
        """
        if name in self.__dict__ or name.startswith('_'):
            # Let Python handle internal attributes normally
            super().__setattr__(name, value)
        else:
            self._data[name] = self._wrap(value)

    def __getitem__(self, key):
        """
        Retrieve a value by key.

        Args:
            key: Key to access.

        Returns:
            Corresponding value from the internal data.
        """
        return self._data[key]

    def __setitem__(self, key, value):
        """
        Set a value by key.

        Args:
            key: Key to assign to.
            value: Value to store.
        """
        self._data[key] = self._wrap(value)

    def __delitem__(self, key):
        """
        Delete a key from the dictionary.

        Args:
            key: Key to remove.
        """
        del self._data[key]

    def __delattr__(self, key):
        """
        Delete an attribute from the dictionary.

        Args:
            key: Key to remove.
        """
        del self._data[key]

    def __contains__(self, key):
        """
        Check if a key exists in the dictionary.

        Args:
            key: The key to check.

        Returns:
            True if key exists, False otherwise.
        """
        return key in self._data

    def __iter__(self):
        """
        Return iterator over dictionary keys.

        Returns:
            Iterator over keys.
        """
        return iter(self._data)

    def __len__(self):
        """
        Return the number of stored keys.

        Returns:
            The number of items.
        """
        return len(self._data)

    def __eq__(self, other):
        """
        Equality comparison.

        Args:
            other: Another AQFlexibleDictionary or dict.

        Returns:
            True if contents are equal, False otherwise.
        """
        if isinstance(other, AQFlexibleDictionary):
            return self._data == other._data
        if isinstance(other, dict):
            return self.to_dict() == other
        return NotImplemented

    def __copy__(self):
        """
        Create a shallow copy of the dictionary.

        Returns:
            A new AQFlexibleDictionary with the same content.
        """
        return self.copy()

    def __repr__(self):
        """
        Return the official string representation.

        Returns:
            A developer-friendly string of the internal data.
        """
        return f"{self._class_name}({self._data})"

    def __reversed__(self):
        """
        Return reversed iterator over keys.

        Returns:
            A reversed iterator of keys.
        """
        return reversed(list(self._data))

    def __or__(self, other):
        """
        Merge two dictionaries using the | operator.

        Args:
            other: Another dictionary.

        Returns:
            A new merged AQFlexibleDictionary.
        """
        if isinstance(other, dict):
            merged = self.to_dict()
            merged.update(other)
            return self.__class__(**merged)
        return NotImplemented

    def __ior__(self, other):
        """
        In-place merge using |= operator.

        Args:
            other: A dictionary to merge.

        Returns:
            The updated AQFlexibleDictionary.
        """
        if isinstance(other, dict):
            self.update(other)
            return self
        return NotImplemented

    def __getstate__(self):
        """
        Support for pickling.

        Returns:
            Internal state as a plain dictionary.
        """
        return self.to_dict()

    def __setstate__(self, state: Dict):
        """
        Restore from pickled state.

        Args:
            state: Dictionary representing internal data.
        """
        object.__setattr__(self, "_data", {})
        for key, value in state.items():
            self._data[key] = self._wrap(value)

    def __str__(self):
        """
        Return string version of the internal dictionary.

        Returns:
            A stringified dictionary.
        """
        return str(self.to_dict())

    def __json__(self):
        """
        JSON serializer hook.

        Returns:
            A dictionary suitable for JSON serialization.
        """
        return self.to_dict()

    def items(self):
        """
        Return key-value pairs.

        Returns:
            dict_items of internal data.
        """
        return self._data.items()

    def keys(self):
        """
        Return keys of the dictionary.

        Returns:
            dict_keys of internal data.
        """
        return self._data.keys()

    def values(self):
        """
        Return values of the dictionary.

        Returns:
            dict_values of internal data.
        """
        return self._data.values()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to a standard Python dictionary.

        Returns:
            A dict with all nested AQFlexibleDictionaries unwrapped.
        """
        # Optionally convert back to plain dict
        def unwrap(val):
            if isinstance(val, AQFlexibleDictionary):
                return val.to_dict()
            return val
        return {k: unwrap(v) for k, v in self._data.items()}

    def copy(self) -> "AQFlexibleDictionary":
        """
        Shallow copy of this object.

        Returns:
            A new AQFlexibleDictionary instance.
        """
        return self.__class__(**self.to_dict())

    def pop(self, key, default=None):
        """
        Remove and return item by key.

        Args:
            key: The key to pop.
            default: Value to return if key is missing.

        Returns:
            The value associated with the key, or default.
        """
        return self._data.pop(key, default)

    def get(self, key, default=None):
        """
        Return value for key if present.

        Args:
            key: Key to look for.
            default: Value to return if key is missing.

        Returns:
            The value or default.
        """
        return self._data.get(key, default)

    def setdefault(self, key, default=None):
        """
        Insert key with default if not already present.

        Args:
            key: Key to insert.
            default: Value to use if key is not found.

        Returns:
            The value associated with the key.
        """
        return self._data.setdefault(key, self._wrap(default))

    def update(self, other=(), **kwargs):
        """
        Update internal data with another dict or iterable.

        Args:
            other: Dictionary or iterable of key-value pairs.
            **kwargs: Additional key-value pairs to update.
        """
        if isinstance(other, dict):
            items = other.items()
        else:
            items = other  # assume iterable of pairs
        for k, v in items:
            self._data[k] = self._wrap(v)
        for k, v in kwargs.items():
            self._data[k] = self._wrap(v)

    def clear(self):
        """
        Remove all items from the dictionary.
        """
        self._data.clear()

    @classmethod
    def fromkeys(cls: Type["AQFlexibleDictionary"], iterable: Iterable[str], value: Any = None):
        """
        Create new instance from keys and a shared default value.

        Args:
            iterable: Iterable of keys.
            value: Value assigned to each key.

        Returns:
            A new AQFlexibleDictionary instance.
        """
        return cls(**{k: value for k in iterable})


class AskQuestionResponse(AQFlexibleDictionary[str, Any]):
    """
    Specialized response container for CLI or GUI question prompts.

    Includes fields such as `question`, `answer_type`, and `user_answer`.
    Supports both dictionary-style and attribute-style access.
    """
    tui: bool = False
    allow_blanks: bool = False
    message: str = ""
    question: Union[str, None] = ""
    answer_type: str = ""
    answer_found: bool = False
    raw_user_answer: str = ""
    user_answer: Union[str, int, float,  None, bool, List[Any]] = ""
