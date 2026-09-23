"""Inspect native observation support without changing or lowering a Cow model."""

import json
import sys
from dataclasses import asdict
from pathlib import Path

from specdet.adapters.verus import backend, type_context
from specdet.adapters.verus.native.extract import (
    function_spec_from_dict,
    function_spec_to_dict,
)
from specdet.adapters.verus.native.extract import extractor
from specdet.adapters.verus.native.view.registry import ViewRegistry


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = (
    ROOT / "proofs/completeness/cow/cow-engineer/analysis-runs"
    / "20260922T113813Z-1aa027dfd4/targets/e613e9e0b4d0c19df1723877"
    / "revisions/0/contract.json"
)


def main():
    contract = json.loads(CONTRACT.read_text())["payload"]
    native = contract["native"]
    sources = {
        native["source_file"]: native["source"],
        **{entry["file"]: entry["source"] for entry in native["type_sources"]},
    }
    function = function_spec_from_dict(native["function_spec"])
    before = function_spec_to_dict(function)
    syntax = type_context.parse_input_type(function.return_type, function)
    bound_views = type_context.bound_views(function, sources)
    registry = ViewRegistry.from_sources(
        native["source"],
        [entry["source"] for entry in native["type_sources"]],
        bound_views=bound_views,
    )
    resolution = registry.resolve(syntax)
    if function_spec_to_dict(function) != before:
        raise AssertionError("Native support inspection changed the source model")
    json.dump({
        "purpose": "component support inspection, not API completeness",
        "contract": str(CONTRACT.relative_to(ROOT)),
        "target": contract["target"]["qualified_name"],
        "loaded_modules": {
            "extractor": extractor.__file__,
            "type_context": type_context.__file__,
            "backend": backend.__file__,
        },
        "generics": function.generics_decl,
        "where": function.where_decl,
        "requires": function.requires,
        "ensures": function.ensures,
        "return_type": function.return_type.to_dict(),
        "helper_type_syntax": asdict(syntax),
        "source_bound_views": {
            name: asdict(view) for name, view in bound_views.items()
        },
        "scanned_view_impls": sorted(registry.scan.views),
        "accepted_views": sorted(registry.accepted_views),
        "registry_resolution": {
            "layer": resolution.layer,
            "view_type": resolution.view_type_text,
            "rationale": resolution.rationale,
            "needs": resolution.needs,
        },
        "registry_diagnostics": registry.diagnostics,
        "model_unchanged": True,
    }, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
