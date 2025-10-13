import ast
from copy import deepcopy
from typing import Dict, Any, Set, Optional, List

import ast

DELIMITER = "."

def filter_data_by_keys(
    data: Dict[str, Any] | List[Any],
    keys: Set[str],
    keychain: Optional[List[str]] = None,
    delimiter: str = DELIMITER,
    **kwargs: Any,
) -> Dict[str, Any] | List[Any]:
    if isinstance(data, Dict):
        new_data: Dict[str, Any] = dict()

        for key, value in data.items():
            new_keychain = deepcopy(keychain) if keychain is not None else []
            new_keychain.append(key)

            new_keychain_string = delimiter.join(new_keychain)

            if any([k.startswith(new_keychain_string) for k in keys]):
                if isinstance(value, Dict) or isinstance(value, List):
                    new_value = filter_data_by_keys(value, keys, new_keychain, delimiter, **kwargs)

                    if new_value not in [[], {}]:
                        new_data[key] = new_value
                else:
                    if new_keychain_string in keys:
                        new_data[key] = value

        return new_data

    elif isinstance(data, List):
        new_data_array = [
            (
                filter_data_by_keys(item, keys, keychain, delimiter, **kwargs)
                if isinstance(item, Dict) or isinstance(item, List)
                else item
            )
            for item in data
        ]

        new_data_array = [item for item in new_data_array if item != {}]

        return new_data_array

    else:
        raise TypeError(f"Unexpected data: {data}")


def filter_schema_by_keys(
    schema: Dict[str, Any],
    keys: Set[str],
    keychain: List[str] = None,
    delimiter: str = DELIMITER,
) -> Dict[str, Any]:
    if keychain is None:
        keychain = []

    schema_type = schema.get("type")
    filtered: Dict[str, Any] = dict(schema)  # copy all metadata
    current_path = delimiter.join(keychain) if keychain else ""

    keep_node = any(
        kp == current_path or kp.startswith(current_path + delimiter)
        for kp in keys
    )

    if schema_type == "object" and "properties" in schema:
        filtered_properties = {}
        for prop, subschema in schema["properties"].items():
            new_keychain = keychain + [prop]
            result = filter_schema_by_keys(subschema, keys, new_keychain, delimiter)
            if result:
                filtered_properties[prop] = result

        if filtered_properties:
            filtered["properties"] = filtered_properties
            if "required" in schema:
                filtered["required"] = [r for r in schema.get("required", []) if r in filtered_properties]
        elif not keep_node:
            return {}

    elif schema_type == "array" and "items" in schema:
        # Always include array if path matches or any children match
        new_keychain = keychain
        filtered_items = filter_schema_by_keys(schema["items"], keys, new_keychain, delimiter)
        if filtered_items:
            filtered["items"] = filtered_items
        elif not keep_node:
            return {}

    else:
        if not keep_node:
            return {}

    return filtered


class EnhancedJSONPathExtractor(ast.NodeVisitor):
    def __init__(self):
        self.paths = set()
        self.var_map = {}

    def visit_Assign(self, node):
        # Track variable assignments like: user = data["user"]
        if isinstance(node.value, ast.Subscript):
            path = self._extract_path(node.value)
            for target in node.targets:
                if isinstance(target, ast.Name) and path:
                    self.var_map[target.id] = path
        self.generic_visit(node)

    def visit_Subscript(self, node):
        path = self._extract_path(node)
        if path:
            self.paths.add(".".join(path))
        self.generic_visit(node)



    def visit_For(self, node):
        # Resolve the iterable expression to a path
        path = self._extract_path(node.iter)
        if path:
            #path.append("[]") # Mark as list access
            if isinstance(node.target, ast.Name):
                self.var_map[node.target.id] = path
        self.generic_visit(node)


    def _extract_path(self, node):
        path = []
        current = node

        while isinstance(current, ast.Subscript):
            key = self._get_key(current.slice)
            if key is None:
                return None
            path.insert(0, key)
            current = current.value

        if isinstance(current, ast.Name):
            var_name = current.id
            if var_name in self.var_map:
                # Prepend known variable path
                return self.var_map[var_name] + path
            else:
                return path
        return None

    def _get_key(self, slice_node):
        if isinstance(slice_node, ast.Constant):  # Python 3.8+
            return str(slice_node.value)
        elif isinstance(slice_node, ast.Str):  # Older versions
            return slice_node.s
        elif isinstance(slice_node, ast.Index):  # Python <3.9
            return self._get_key(slice_node.value)
        elif isinstance(slice_node, ast.Num):
            return "[]"  # Treat numeric index as list access
        elif isinstance(slice_node, ast.Constant) and isinstance(slice_node.value, int):
            return "[]"
        return None

def extract_json_paths(source_code):
    tree = ast.parse(source_code)
    extractor = EnhancedJSONPathExtractor()
    extractor.visit(tree)
    return sorted(extractor.paths)