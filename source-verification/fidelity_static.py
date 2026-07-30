#!/usr/bin/env python3
"""Static fidelity checks for every copied source proof."""

from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
import sys

from tree_sitter import Language, Parser
import tree_sitter_verus


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
sys.path.insert(0, str(WORKSPACE))

from run_rust_std_spec_feedback import assume_to_synthetic
from spec_determinism.extract.extractor import extract_spec


PARSER = Parser(Language(tree_sitter_verus.language()))


def normalize(value: str) -> str:
    value = re.sub(r"//.*", "", value)
    value = re.sub(r"/\*.*?\*/", "", value, flags=re.DOTALL)
    return re.sub(r"\s+", "", value).strip("()")


def function_nodes(source: bytes):
    tree = PARSER.parse(source)
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.type == "function_item":
            name = node.child_by_field_name("name")
            body = node.child_by_field_name("body")
            yield {
                "node": node,
                "name": source[name.start_byte : name.end_byte].decode() if name else "",
                "body": (
                    source[body.start_byte : body.end_byte].decode(errors="replace")
                    if body
                    else ""
                ),
                "text": source[node.start_byte : node.end_byte].decode(errors="replace"),
            }
        stack.extend(reversed(node.named_children))


def select_source_function(proof: str, api_path: str) -> dict | None:
    functions = [
        item
        for item in function_nodes(proof.encode())
        if item["name"].startswith("source_")
    ]
    if not functions:
        return None
    tokens = [
        token.lower()
        for token in re.split(r"::|[^A-Za-z0-9]+", api_path)
        if token
    ]
    method = tokens[-1]

    def score(item):
        name = item["name"].lower()
        return (
            20 * int(method in name)
            + sum(2 for token in tokens[-4:-1] if token in name)
            - len(name) / 1000
        )

    return max(functions, key=score)


def remove_proof_blocks(body: str) -> str:
    result = body
    while True:
        match = re.search(r"\bproof\s*\{", result)
        if not match:
            return result
        start = match.start()
        opening = result.find("{", match.start())
        depth = 0
        end = None
        for index in range(opening, len(result)):
            if result[index] == "{":
                depth += 1
            elif result[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            return result
        result = result[:start] + result[end:]


def calls(body: str) -> set[str]:
    return set(
        re.findall(
            r"(?:(?:[A-Za-z_][A-Za-z0-9_]*::)+|\.)([A-Za-z_][A-Za-z0-9_]*)\s*(?:::<[^>]*>)?\s*\(",
            body,
        )
    )


def keywords(body: str) -> Counter:
    return Counter(
        re.findall(r"\b(?:if|else|match|while|loop|for|return|unsafe)\b", body)
    )


def main() -> None:
    results = []
    for proof_dir in sorted(path for path in (ROOT / "proved-apis").iterdir() if path.is_dir()):
        proof_path = proof_dir / "proof.rs"
        contract_path = proof_dir / "contract.rs"
        source_path = proof_dir / "rust_source.rs"
        metadata_path = proof_dir / "metadata.json"
        if not all(path.is_file() for path in (proof_path, contract_path, metadata_path)):
            continue
        proof = proof_path.read_text(errors="replace")
        contract = contract_path.read_text(errors="replace")
        rust_source = source_path.read_text(errors="replace") if source_path.is_file() else ""
        metadata = json.loads(metadata_path.read_text())
        api_path = metadata.get("api_path", "")
        source_fn = select_source_function(proof, api_path)
        flags = []
        extra_requires: list[str] = []
        missing_requires: list[str] = []
        contract_requires: list[str] = []
        proof_requires: list[str] = []
        if source_fn is None:
            flags.append("missing_source_function")
        else:
            try:
                synthetic = assume_to_synthetic(contract)
                contract_spec = extract_spec(
                    synthetic,
                    "__rust_std_candidate",
                    type_sources=[synthetic],
                )
                proof_spec = extract_spec(
                    proof,
                    source_fn["name"],
                    type_sources=[proof],
                )
                contract_requires = list(contract_spec.requires)
                proof_requires = list(proof_spec.requires)
                contract_normalized = {normalize(value) for value in contract_requires}
                proof_normalized = {normalize(value) for value in proof_requires}
                extra_requires = sorted(proof_normalized - contract_normalized)
                missing_requires = sorted(contract_normalized - proof_normalized)
                if extra_requires:
                    flags.append("extra_requires")
                if len(proof_spec.params) != len(contract_spec.params):
                    flags.append("parameter_count_mismatch")
            except Exception as error:
                flags.append(f"spec_extract_error:{type(error).__name__}")

            body = source_fn["body"]
            compact = normalize(body)
            raw_target = normalize(metadata.get("raw_target", ""))
            normalized_api = normalize(api_path)
            if raw_target and raw_target in compact:
                flags.append("exact_target_call")
            if normalized_api and normalized_api in compact:
                flags.append("exact_api_call")
            target_method = api_path.rsplit("::", 1)[-1]
            if re.search(rf"(?:\.|::){re.escape(target_method)}\s*\(", body):
                flags.append("same_named_call")

        if re.search(r"\bassume\s*\(|\badmit\s*\(|external_body", proof):
            flags.append("forbidden_trust_construct")
        assume_targets = [
            normalize(value)
            for value in re.findall(
                r"assume_specification(?:<[^>]*>)?\s*\[(.*?)\]",
                proof,
                flags=re.DOTALL,
            )
        ]
        raw_target = normalize(metadata.get("raw_target", ""))
        if raw_target and raw_target in assume_targets:
            flags.append("target_assume_specification")
        axiom_count = len(re.findall(r"\b(?:broadcast\s+)?axiom\s+fn\b", proof))
        if axiom_count:
            flags.append("contains_axiom")

        similarity = None
        source_calls: list[str] = []
        proof_calls: list[str] = []
        source_keywords = {}
        proof_keywords = {}
        if source_fn is not None and rust_source.strip():
            clean_proof_body = remove_proof_blocks(source_fn["body"])
            similarity = SequenceMatcher(
                None,
                normalize(rust_source),
                normalize(clean_proof_body),
            ).ratio()
            source_calls = sorted(calls(rust_source))
            proof_calls = sorted(calls(clean_proof_body))
            source_keywords = dict(keywords(rust_source))
            proof_keywords = dict(keywords(clean_proof_body))
            if similarity < 0.15:
                flags.append("very_low_source_similarity")
            if source_keywords != proof_keywords:
                flags.append("control_flow_shape_changed")

        results.append(
            {
                "id": proof_dir.name,
                "api_path": api_path,
                "proof_function": source_fn["name"] if source_fn else None,
                "trust_level": metadata.get("trust_level"),
                "flags": sorted(set(flags)),
                "contract_requires": contract_requires,
                "proof_requires": proof_requires,
                "extra_requires": extra_requires,
                "missing_requires": missing_requires,
                "axiom_count": axiom_count,
                "assume_specification_targets": assume_targets,
                "similarity": similarity,
                "source_calls": source_calls,
                "proof_calls": proof_calls,
                "source_keywords": source_keywords,
                "proof_keywords": proof_keywords,
            }
        )

    flag_counts = Counter(flag for result in results for flag in result["flags"])
    high_risk_flags = {
        "missing_source_function",
        "extra_requires",
        "parameter_count_mismatch",
        "exact_target_call",
        "exact_api_call",
        "forbidden_trust_construct",
        "target_assume_specification",
    }
    high_risk = [
        result
        for result in results
        if any(flag in high_risk_flags or flag.startswith("spec_extract_error") for flag in result["flags"])
    ]
    payload = {
        "counts": {
            "proofs": len(results),
            "high_risk": len(high_risk),
            "with_axioms": sum(result["axiom_count"] > 0 for result in results),
            "with_assume_specification": sum(
                bool(result["assume_specification_targets"]) for result in results
            ),
        },
        "flag_counts": dict(flag_counts),
        "high_risk_ids": [result["id"] for result in high_risk],
        "results": results,
    }
    (ROOT / "fidelity-static.json").write_text(json.dumps(payload, indent=2) + "\n")
    lines = [
        "# Static proof fidelity audit",
        "",
        f"- Proofs: **{len(results)}**",
        f"- High-risk static findings: **{len(high_risk)}**",
        f"- Proofs containing explicit axioms: **{payload['counts']['with_axioms']}**",
        f"- Proofs containing lower `assume_specification`: **{payload['counts']['with_assume_specification']}**",
        "",
        "## Flag counts",
        "",
    ]
    lines.extend(f"- `{key}`: {value}" for key, value in flag_counts.most_common())
    lines.extend(["", "## High-risk targets", ""])
    lines.extend(
        f"- `{result['id']}` — {', '.join(result['flags'])}"
        for result in high_risk
    )
    (ROOT / "FIDELITY-STATIC.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(payload["counts"], indent=2))
    print(json.dumps(dict(flag_counts), indent=2))


if __name__ == "__main__":
    main()
