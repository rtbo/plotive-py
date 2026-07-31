from collections.abc import Mapping


class PvMapping(Mapping):
    def __len__(self) -> int:
        return len(self.__dict__)

    def __iter__(self):
        return iter_camel_case_keys(self.__dict__)

    def __getitem__(self, key: str) -> object:
        return get_by_camel_or_snake(self.__dict__, key)


def snake_to_camel(key: str) -> str:
    """Convert a snake_case key to camelCase."""
    if "_" not in key:
        return key
    parts = key.split("_")
    head = parts[0]
    tail = "".join(part[:1].upper() + part[1:] for part in parts[1:] if part)
    return head + tail


def camel_to_snake(key: str) -> str:
    """Convert a camelCase key to snake_case."""
    if "_" in key:
        return key
    chars: list[str] = []
    for char in key:
        if char.isupper():
            chars.append("_")
            chars.append(char.lower())
        else:
            chars.append(char)
    return "".join(chars)


def iter_camel_case_keys(mapping: Mapping[str, object]):
    """Iterate over mapping keys transformed to camelCase."""
    for key in mapping:
        yield snake_to_camel(key)


def get_by_camel_or_snake(mapping: Mapping[str, object], key: str) -> object:
    """Get a value by camelCase or snake_case key."""
    if key in mapping:
        return mapping[key]
    snake_key = camel_to_snake(key)
    if snake_key in mapping:
        return mapping[snake_key]
    raise KeyError(key)
