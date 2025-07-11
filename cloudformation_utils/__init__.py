import re
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional

import yaml
from yaml import MappingNode, ScalarNode, SequenceNode

try:
    from ._version import version as __version__
except ImportError:
    # Version file not generated yet (development mode)
    __version__ = "unknown"

__all__ = [
    "__version__",
    "cloudformation_yaml_loads",
    "process_script",
    "process_script_decorated",
]

# the "var " prefix is to support javascript as well
VAR_DECL_RE = re.compile(
    r'^((\s*var\s+)|(\s*const\s+))?CF_([^\s=]+)[\s="\']*([^#"\'\`;]*)(?:["\'\s\`;]*)(//)?(#optional)?'
)
EMBED_DECL_RE = re.compile(
    r"^(.*?=\s*)?(.*?)(?:(?:\`?#|//)CF([^#\`]*))[\"\`\s]*(#optional)?"
)
IN_PLACE_RE = re.compile(r"^([^\$]*?)\$CF{([^}\|]*)(\|[^}]*)?}(#optional)?(.*)")


def _descalar(target: Any) -> Any:
    if (
        isinstance(target, ScalarNode)
        or isinstance(target, SequenceNode)
        or isinstance(target, MappingNode)
    ):
        if target.tag in INTRISINC_FUNCS:
            return INTRISINC_FUNCS[target.tag](None, "", target)
        else:
            return _descalar(target.value)
    elif isinstance(target, list):
        ret = []
        for nxt in target:
            ret.append(_descalar(nxt))
        return ret
    else:
        return target


def _decode_parameter_name(name: str) -> str:
    return re.sub("__", "::", name)


def _base64_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Base64": _descalar(node.value)}


def _findinmap_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::FindInMap": _descalar(node.value)}


def _getatt_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::GetAtt": _descalar(node.value)}


def _getazs_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::GetAZs": _descalar(node.value)}


def _importvalue_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::ImportValue": _descalar(node.value)}


def _join_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Join": _descalar(node.value)}


def _select_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Select": _descalar(node.value)}


def _split_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Split": _descalar(node.value)}


def _sub_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Sub": _descalar(node.value)}


def _ref_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Ref": _descalar(node.value)}


def _and_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::And": _descalar(node.value)}


def _equals_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Equals": _descalar(node.value)}


def _if_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::If": _descalar(node.value)}


def _not_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Not": _descalar(node.value)}


def _or_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Or": _descalar(node.value)}


def _importfile_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::ImportFile": _descalar(node.value)}


def _importyaml_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::ImportYaml": _descalar(node.value)}


def _merge_ctor(loader: Any, tag_suffix: str, node: Any) -> Dict[str, Any]:
    return {"Fn::Merge": _descalar(node.value)}


INTRISINC_FUNCS = {
    "!Base64": _base64_ctor,
    "!FindInMap": _findinmap_ctor,
    "!GetAtt": _getatt_ctor,
    "!GetAZs": _getazs_ctor,
    "!ImportValue": _importvalue_ctor,
    "!Join": _join_ctor,
    "!Select": _select_ctor,
    "!Split": _split_ctor,
    "!Sub": _sub_ctor,
    "!Ref": _ref_ctor,
    "!And": _and_ctor,
    "!Equals": _equals_ctor,
    "!If": _if_ctor,
    "!Not": _not_ctor,
    "!Or": _or_ctor,
    "!ImportFile": _importfile_ctor,
    "!ImportYaml": _importyaml_ctor,
    "!Merge": _merge_ctor,
}


def cloudformation_yaml_loads(content: str) -> Any:
    for name in INTRISINC_FUNCS:
        yaml.add_multi_constructor(name, INTRISINC_FUNCS[name], Loader=yaml.SafeLoader)

    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader: Any, node: Any) -> Any:
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
    )

    return yaml.load(content, OrderedLoader)


def process_script_decorated(filename: str) -> List[Any]:
    return process_script(filename, ref_decorator=source_and_optional_ref_decorator)


def process_script(
    filename: str, ref_decorator: Optional[Callable] = None
) -> List[Any]:
    arr: List[Any] = []
    with open(filename) as fd:
        line_no = 1
        for line in fd:
            next_arr = _do_replace(line, line_no, filename, ref_decorator=ref_decorator)
            arr = arr + next_arr
            line_no += 1
    return arr


def _apply_source(
    data: Any,
    filename: str,
    line_no: int,
    is_optional: bool,
    default_val: str,
    ref_decorator: Optional[Callable] = None,
) -> None:
    if isinstance(data, OrderedDict):
        if "Ref" in data and ref_decorator:
            ref_decorator(data, filename, line_no, is_optional, default_val)
        for k, val in list(data.items()):
            _apply_source(
                k,
                filename,
                line_no,
                is_optional,
                default_val,
                ref_decorator=ref_decorator,
            )
            _apply_source(
                val,
                filename,
                line_no,
                is_optional,
                default_val,
                ref_decorator=ref_decorator,
            )


def source_and_optional_ref_decorator(
    ref: Dict[str, Any],
    filename: str,
    line_no: int,
    is_optional: bool,
    default_val: str,
) -> None:
    ref["__source"] = filename
    ref["__source_line"] = str(line_no)
    if is_optional:
        ref["__optional"] = "true"
        ref["__default"] = default_val


def _do_replace(
    line: str, line_no: int, filename: str, ref_decorator: Optional[Callable] = None
) -> List[Any]:
    arr: List[Any] = []
    result = VAR_DECL_RE.match(line)
    if result:
        js_prefix = result.group(1)
        encoded_varname = result.group(4)
        var_name = _decode_parameter_name(encoded_varname)
        ref = OrderedDict()
        ref["Ref"] = var_name
        if ref_decorator:
            ref_decorator(
                ref,
                filename,
                line_no,
                str(result.group(7)) == "#optional",
                str(result.group(5)).strip(" \"'"),
            )
        arr.append(line[0 : result.end(4)] + "='")
        arr.append(ref)
        if js_prefix:
            arr.append("';\n")
        else:
            arr.append("'\n")
    else:
        result = EMBED_DECL_RE.match(line)
        if result:
            prefix = result.group(1)
            if not prefix:
                prefix = result.group(2)
                default_val = ""
            else:
                default_val = str(result.group(2)).strip(" \"'")
            arr.append(prefix + "'")
            for entry in cloudformation_yaml_loads("[" + result.group(3) + "]"):
                _apply_source(
                    entry,
                    filename,
                    line_no,
                    str(result.group(4)) == "#optional",
                    default_val,
                    ref_decorator=ref_decorator,
                )
                arr.append(entry)
            if filename.endswith(".ps1"):
                arr.append("'\r\n")
            else:
                arr.append("'\n")
        else:
            result = IN_PLACE_RE.match(line)
            if result:
                arr.append(result.group(1))
                var_name = _decode_parameter_name(result.group(2))
                ref = OrderedDict()
                ref["Ref"] = var_name
                if ref_decorator:
                    ref_decorator(
                        ref,
                        filename,
                        line_no,
                        str(result.group(4)) == "#optional",
                        str(result.group(3)[1:] if result.group(3) else ""),
                    )
                arr.append(ref)
                arr = arr + _do_replace(result.group(5), line_no, filename)
            else:
                arr.append(line)
    return arr
