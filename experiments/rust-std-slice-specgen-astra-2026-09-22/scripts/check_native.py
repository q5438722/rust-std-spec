"""Exercise source observers and slice Default constructors with Rust 1.96.

Select --group singleton to check only from_ref/from_mut and their array
delegates, or --group ascii-case for the in-place ASCII case conversions,
without bootstrap features. --output-root redirects the selected group's
target/ and logs/ directories; omitting --group preserves the original checks.
The existing groups {defaults,singleton,ascii-case} remain unchanged.
--group endpoints compares the authoritative first/last patterns, the exact
ADOPTED current source-proof bodies, and the real public slice methods.
Only the two conversions approved in issues/V-SLICE-PATTERN.md are accepted;
historical proposal files are not native inputs.
--group splits compares only the original split_first/split_last patterns,
the exact ADOPTED current proof bodies, and public methods. Historical isolated
proposals are retained but are not native inputs.
--group mutable-endpoints compares the authoritative first_mut/last_mut patterns,
the exact ADOPTED current proof bodies, and public methods. Historical isolated
proposals are retained but are not native inputs.
--group mutable-splits compares the authoritative mutable split patterns,
the exact ADOPTED current proof bodies, and public methods. Historical isolated
proposals are retained but are not native inputs.
--group split-off-endpoints compares the authority originals, the exact
ADOPTED current shared split-off proof bodies, and public APIs. Only the last
call/import changed; first is unchanged. The local split_last is extracted
from the adopted last proof's actual dependency. Historical isolated proposals
are retained but are not native inputs. Native acceptance does not establish
Verus support. Runtime is stable; public const calls are not.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(
    "/home/chentianyu/nanvix-rust-std-spec-survey/rust-1.96/"
    "library/core/src/slice/mod.rs"
)
FUNCTIONS = {
    "len": (116, 118),
    "is_empty": (136, 138),
    "first": (155, 157),
    "split_first": (198, 200),
    "split_last": (240, 242),
    "last": (281, 283),
}
DEFAULTS = {
    "default_shared": (5635, 5637, "&'a [T]"),
    "default_mut": (5644, 5646, "&'a mut [T]"),
}
SINGLETON_SLICE_SOURCE = SOURCE.with_name("raw.rs")
SINGLETON_ARRAY_SOURCE = SOURCE.parent.parent / "array/mod.rs"
ASCII_CASE_SOURCE = SOURCE.with_name("ascii.rs")
ENDPOINT_PROOFS = ROOT / "proofs/correctness/slice"
SPLIT_PROOFS = ROOT / "proofs/correctness/slice"
MUTABLE_ENDPOINT_PROOFS = ROOT / "proofs/correctness/slice"
MUTABLE_SPLIT_PROOFS = ROOT / "proofs/correctness/slice"
MUTABLE_SPLIT_VSTD = ROOT / "toolchain/upstream/source/vstd"
SPLIT_OFF_ENDPOINT_PROOFS = ROOT / "proofs/correctness/slice"


def endpoint_source():
    lines = SOURCE.read_text().splitlines(keepends=True)
    spans = []
    mappings = []
    originals = []
    adopted = []
    impl = "".join(lines[100:101])
    if impl != "impl<T> [T] {\n":
        raise ValueError(f"Source span changed: {SOURCE}:101")
    spans.append({
        "role": "authority", "kind": "generic-impl", "path": str(SOURCE),
        "start": 101, "end": 101, "text": impl,
    })
    spans.append({
        "role": "native-dependency", "kind": "slice-len", "path": str(SOURCE),
        "start": 102, "end": 118, "text": "".join(lines[101:118]),
    })
    comments = r"(?:[ \t]*//[^\n]*\n|\n)*"
    for name, start, pattern, expression, value in (
        ("first", 140, "[first, ..]", "Some(&slice[0])", 10),
        ("last", 266, "[.., last]", "Some(&slice[slice.len() - 1])", 30),
    ):
        documentation = (
            f"    /// Returns the {name} element of the slice, or `None` if it is empty.\n"
            "    ///\n"
            "    /// # Examples\n"
            "    ///\n"
            "    /// ```\n"
            "    /// let v = [10, 40, 30];\n"
            f"    /// assert_eq!(Some(&{value}), v.{name}());\n"
            "    ///\n"
            "    /// let w: &[i32] = &[];\n"
            f"    /// assert_eq!(None, w.{name}());\n"
            "    /// ```\n"
        )
        attributes = (
            '    #[stable(feature = "rust1", since = "1.0.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_first_last_not_mut", since = "1.56.0")]\n'
            "    #[inline]\n"
            "    #[must_use]\n"
        )
        function = (
            f"    pub const fn {name}(&self) -> Option<&T> {{\n"
            f"        if let {pattern} = self {{ Some({name}) }} else {{ None }}\n"
            "    }\n"
        )
        for kind, first, last, expected in (
            ("documentation", start, start + 10, documentation),
            ("attributes", start + 11, start + 14, attributes),
            ("function", start + 15, start + 17, function),
        ):
            text = "".join(lines[first - 1:last])
            if text != expected:
                raise ValueError(f"Source span changed: {SOURCE}:{first}-{last}")
            spans.append({
                "role": "authority", "name": name, "kind": kind,
                "path": str(SOURCE), "start": first, "end": last, "text": text,
            })
        lifted = re.sub(
            r"\bself\b", "slice",
            text.replace(f"fn {name}(&self)", f"fn {name}<T>(slice: &[T])", 1),
        )
        original_body = lifted.splitlines()[1][4:]
        originals.append(
            f"// {SOURCE}:{start}-{start + 17}\n"
            + documentation + "    #[inline]\n    #[must_use]\n" + lifted
        )
        mapping = {
            "api": f"<[T]>::{name}",
            "authority": {"path": str(SOURCE), "start": start, "end": start + 17},
            "original_body": original_body,
            "native_original": f"original::{name}",
            "native_adopted": f"adopted::{name}",
            "native_public": f"<[T]>::{name}",
            "lifting": (
                "Only self -> slice and explicit <T> are added to the original "
                "signature/body; std-only stability attributes are recorded, not compiled. "
                "The adopted current proof's named Verus return and ensures clause "
                "are erased, but its executable body is extracted without substitution."
            ),
        }
        path = ENDPOINT_PROOFS / f"{name}.rs"
        relative_contract = "../../../specs/slice/mod.rs"
        expected_body = f"    if slice.len() == 0 {{ None }} else {{ {expression} }}"
        proof = path.read_text()
        match = re.fullmatch(
            comments + r"use vstd::prelude::\*;\n"
            + rf'#\[path = "{re.escape(relative_contract)}"\]\nmod contracts;\n'
            + comments + r"verus! \{\n" + comments
            + rf"(?P<signature>pub const fn {name}<T>\(slice: &\[T\]\)"
            + r" -> \(result: Option<&T>\))\n"
            + rf"    ensures\n        contracts::{name}_post\(slice, result\),\n"
            + r"\{\n(?P<body>.*?)\n\}\n\}\n" + comments,
            proof, re.DOTALL,
        )
        if match is None or match["body"] != expected_body:
            raise ValueError(f"Endpoint current source drift: {path}")
        body_start = proof[:match.start("body")].count("\n") + 1
        spans.append({
            "role": "current", "name": name, "kind": "proof", "path": str(path),
            "start": 1, "end": len(proof.splitlines()), "text": proof,
        })
        mapping["current"] = {
            "path": str(path), "body_start": body_start, "body_end": body_start,
            "body": match["body"], "signature": match["signature"],
            "contract": str((path.parent / relative_contract).resolve()),
            "ensures": f"contracts::{name}_post(slice, result)",
        }
        signature = match["signature"].replace(
            "-> (result: Option<&T>)", "-> Option<&T>", 1,
        )
        adopted.append(
            f"// ADOPTED current source-proof input: {path}:{body_start}\n"
            + signature + " {\n" + match["body"] + "\n}\n"
        )
        mappings.append(mapping)
    return (
        "// ADOPTED first/last only; permission: issues/V-SLICE-PATTERN.md.\n"
        "pub mod original {\n" + "\n".join(originals) + "}\n\n"
        "pub mod adopted {\n" + "\n".join(adopted) + "}\n",
        spans, mappings,
    )


def endpoint_negative_cases():
    cases = {
        "wrong-receiver": (
            "fn bad() { let _ = API([1u8]); }", "E0308",
        ),
        "missing-receiver": (
            "fn bad() { let _ = API(); }", "E0061",
        ),
        "extra-argument": (
            "fn bad() { let _ = API(&[1u8], 2u8); }", "E0061",
        ),
        "wrong-element": (
            "fn bad() { let input = [1u16]; let _ = API(&input); }", "E0308",
        ),
        "mutable-result": (
            "fn bad() { let _: Option<&mut u8> = API(&[1u8]); }", "E0308",
        ),
        "owned-result": (
            "fn bad() { let _: Option<u8> = API(&[1u8]); }", "E0308",
        ),
        "write-through-result": (
            "fn bad() { let input = [1u8]; *API(&input).unwrap() = 2; }", "E0594",
        ),
        "local-escape": (
            "fn bad<'a>() -> Option<&'a u8> { let input = [1u8]; API(&input) }",
            "E0515",
        ),
        "short-lifetime": (
            "fn bad() { let view; { let input = [1u8]; view = API(&input); } "
            "let _ = view.unwrap(); }", "E0597",
        ),
        "static-escape": (
            "fn bad(input: &[u8]) -> Option<&'static u8> { API(input) }", None,
        ),
    }
    for label in ("original", "adopted", "public"):
        for api in ("first", "last"):
            binding = f"<[u8]>::{api}" if label == "public" else f"{label}::{api}::<u8>"
            for name, (text, code) in cases.items():
                expected = {"code": code}
                if code is None:
                    expected["message"] = "lifetime may not live long enough"
                yield f"{label}-{api}-{name}", text.replace("API", binding), expected


def split_source():
    lines = SOURCE.read_text().splitlines(keepends=True)
    spans, mappings, originals, adopted = [], [], [], []
    if lines[100] != "impl<T> [T] {\n":
        raise ValueError(f"Source span changed: {SOURCE}:101")
    for kind, start, end in (
        ("generic-impl", 101, 101), ("slice-len", 102, 118),
        ("split-at", 1913, 1957), ("split-at-unchecked", 1993, 2054),
        ("split-at-checked", 2114, 2161),
    ):
        spans.append({
            "role": "authority" if kind == "generic-impl" else "native-dependency",
            "kind": kind, "path": str(SOURCE), "start": start, "end": end,
            "text": "".join(lines[start - 1:end]),
        })
    for name, start, endpoint, remainder, pattern, value, rest, body in (
        (
            "split_first", 182, "first", "tail", "[first, tail @ ..]", 0, "[1, 2]",
            "    if slice.len() == 0 {\n"
            "        None\n"
            "    } else {\n"
            "        Some((&slice[0], slice.split_at(1).1))\n"
            "    }",
        ),
        (
            "split_last", 224, "last", "init", "[init @ .., last]", 2, "[0, 1]",
            "    if slice.len() == 0 {\n"
            "        None\n"
            "    } else {\n"
            "        let i = slice.len() - 1;\n"
            "        Some((&slice[i], slice.split_at(i).0))\n"
            "    }",
        ),
    ):
        documentation = (
            f"    /// Returns the {endpoint} and all the rest of the elements of the slice, "
            "or `None` if it is empty.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let x = &[0, 1, 2];\n    ///\n"
            f"    /// if let Some(({endpoint}, elements)) = x.{name}() {{\n"
            f"    ///     assert_eq!({endpoint}, &{value});\n"
            f"    ///     assert_eq!(elements, &{rest});\n"
            "    /// }\n    /// ```\n"
        )
        attributes = (
            '    #[stable(feature = "slice_splits", since = "1.5.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_first_last_not_mut", since = "1.56.0")]\n'
            "    #[inline]\n    #[must_use]\n"
        )
        function = (
            f"    pub const fn {name}(&self) -> Option<(&T, &[T])> {{\n"
            f"        if let {pattern} = self {{ Some(({endpoint}, {remainder})) }} else {{ None }}\n"
            "    }\n"
        )
        for kind, first, last, expected in (
            ("documentation", start, start + 11, documentation),
            ("attributes", start + 12, start + 15, attributes),
            ("function", start + 16, start + 18, function),
        ):
            text = "".join(lines[first - 1:last])
            if text != expected:
                raise ValueError(f"Source span changed: {SOURCE}:{first}-{last}")
            spans.append({
                "role": "authority", "name": name, "kind": kind, "path": str(SOURCE),
                "start": first, "end": last, "text": text,
            })
        original_body = (
            f"    if let {pattern} = slice {{ Some(({endpoint}, {remainder})) }} else {{ None }}"
        )
        signature = f"pub const fn {name}<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)"
        current = (
            'use vstd::prelude::*;\n#[path = "../../../specs/slice/mod.rs"]\n'
            "mod contracts;\n\nverus! {\n"
            f"// Rust 1.96 core/src/slice/mod.rs:{start}-{start + 18}; "
            f"body:{start + 16}-{start + 18}.\n"
            f"{signature}\n    ensures\n        contracts::{name}_post(slice, result),\n"
            "{\n" + body + "\n}\n}\n"
        )
        mapping = {
            "api": f"<[T]>::{name}",
            "authority": {"path": str(SOURCE), "start": start, "end": start + 18},
            "original_body": original_body,
            "native_original": f"original::{name}", "native_adopted": f"adopted::{name}",
            "native_public": f"<[T]>::{name}",
            "lifting": (
                "Only self -> slice and explicit <T> are added to the original. "
                "Only the named Verus return and ensures are erased from the exact "
                "ADOPTED current proof. No executable substitution is made during extraction."
            ),
        }
        path = SPLIT_PROOFS / f"{name}.rs"
        proof = path.read_text()
        if proof != current:
            raise ValueError(f"Split current source drift: {path}")
        body_start = proof[:proof.index(body)].count("\n") + 1
        spans.append({
            "role": "current", "name": name, "kind": "proof", "path": str(path),
            "start": 1, "end": len(proof.splitlines()), "text": proof,
        })
        mapping["current"] = {
            "path": str(path), "signature": signature, "body": body,
            "body_start": body_start, "body_end": body_start + len(body.splitlines()) - 1,
            "contract": str(SPLIT_PROOFS.parents[2] / "specs/slice/mod.rs"),
            "ensures": f"contracts::{name}_post(slice, result)",
        }
        native_signature = signature.replace(
            "-> (result: Option<(&T, &[T])>)", "-> Option<(&T, &[T])>", 1,
        )
        originals.append(
            f"// {SOURCE}:{start}-{start + 18}\n" + documentation
            + native_signature + " {\n" + original_body + "\n}\n"
        )
        adopted.append(
            f"// ADOPTED current source-proof input: {path}:{body_start}\n"
            + native_signature + " {\n" + mapping["current"]["body"] + "\n}\n"
        )
        mappings.append(mapping)
    return (
        "// ADOPTED split bodies; permission: issues/V-SLICE-PATTERN.md.\n"
        "pub mod original {\n" + "\n".join(originals) + "}\n\n"
        "pub mod adopted {\n" + "\n".join(adopted) + "}\n",
        spans, mappings,
    )


def split_negative_cases():
    cases = {
        "wrong-receiver": ("fn bad() { let _ = API([1u8]); }", "E0308"),
        "missing-receiver": ("fn bad() { let _ = API(); }", "E0061"),
        "extra-argument": ("fn bad() { let _ = API(&[1u8], 2u8); }", "E0061"),
        "wrong-element": ("fn bad() { let input = [1u16]; let _ = API(&input); }", "E0308"),
        "mutable-element": (
            "fn bad() { let _: Option<(&mut u8, &[u8])> = API(&[1u8]); }", "E0308",
        ),
        "mutable-remainder": (
            "fn bad() { let _: Option<(&u8, &mut [u8])> = API(&[1u8]); }", "E0308",
        ),
        "reversed-result": (
            "fn bad() { let _: Option<(&[u8], &u8)> = API(&[1u8]); }", "E0308",
        ),
        "owned-element": (
            "fn bad() { let _: Option<(u8, &[u8])> = API(&[1u8]); }", "E0308",
        ),
        "owned-remainder": (
            "fn bad() { let _: Option<(&u8, Vec<u8>)> = API(&[1u8]); }", "E0308",
        ),
        "missing-option": (
            "fn bad(input: &[u8]) -> (&u8, &[u8]) { API(input) }", "E0308",
        ),
        "write-element": (
            "fn bad() { let input = [1u8, 2]; *API(&input).unwrap().0 = 3; }", "E0594",
        ),
        "write-remainder": (
            "fn bad() { let input = [1u8, 2]; API(&input).unwrap().1[0] = 3; }", "E0594",
        ),
        "local-element": (
            "fn bad<'a>() -> &'a u8 { let input = [1u8]; API(&input).unwrap().0 }", "E0515",
        ),
        "local-remainder": (
            "fn bad<'a>() -> &'a [u8] { let input = [1u8]; API(&input).unwrap().1 }", "E0515",
        ),
        "short-element": (
            "fn bad() { let view; { let input = [1u8]; view = API(&input).unwrap().0; } "
            "let _ = *view; }", "E0597",
        ),
        "short-remainder": (
            "fn bad() { let view; { let input = [1u8]; view = API(&input).unwrap().1; } "
            "let _ = view.len(); }", "E0597",
        ),
        "static-element": (
            "fn bad(input: &[u8]) -> &'static u8 { API(input).unwrap().0 }", None,
        ),
        "static-remainder": (
            "fn bad(input: &[u8]) -> &'static [u8] { API(input).unwrap().1 }", None,
        ),
        "mutate-input-element-live": (
            "fn bad(input: &mut [u8]) { let result = API(input).unwrap(); "
            "input[0] = 2; let _ = *result.0; }", "E0506",
        ),
        "mutate-input-remainder-live": (
            "fn bad(input: &mut [u8]) { let result = API(input).unwrap(); "
            "input[0] = 2; let _ = result.1.len(); }", "E0506",
        ),
    }
    for label in ("original", "adopted", "public"):
        for api in ("split_first", "split_last"):
            binding = f"<[u8]>::{api}" if label == "public" else f"{label}::{api}::<u8>"
            for name, (text, code) in cases.items():
                expected = {"code": code}
                if code is None:
                    expected["message"] = "lifetime may not live long enough"
                yield f"{label}-{api}-{name}", text.replace("API", binding), expected


def mutable_endpoint_source():
    lines = SOURCE.read_text().splitlines(keepends=True)
    spans, mappings, originals, adopted = [], [], [], []
    for kind, start, end, expected in (
        ("generic-impl", 101, 101, "impl<T> [T] {\n"),
        (
            "slice-len", 102, 118,
            "    /// Returns the number of elements in the slice.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let a = [1, 2, 3];\n"
            "    /// assert_eq!(a.len(), 3);\n    /// ```\n"
            '    #[lang = "slice_len_fn"]\n'
            '    #[stable(feature = "rust1", since = "1.0.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_len", since = "1.39.0")]\n'
            "    #[rustc_no_implicit_autorefs]\n    #[inline]\n    #[must_use]\n"
            "    pub const fn len(&self) -> usize {\n"
            "        ptr::metadata(self)\n    }\n",
        ),
    ):
        text = "".join(lines[start - 1:end])
        if text != expected:
            raise ValueError(f"Source span changed: {SOURCE}:{start}-{end}")
        spans.append({
            "role": "authority" if kind == "generic-impl" else "native-dependency",
            "kind": kind, "path": str(SOURCE), "start": start, "end": end, "text": text,
        })
    contract = MUTABLE_ENDPOINT_PROOFS.parents[2] / "specs/slice/mutable_endpoints.rs"
    expected_contract = (
        "use vstd::prelude::*;\n\nverus! {\n\n"
        "// Inputs are the original slice and the caller's final optional element.\n"
        "// Outputs are the initial optional element and the entire returned slice.\n"
    )
    for name, index in (("first_mut", "0"), ("last_mut", "input_initial.len() - 1")):
        expected_contract += (
            f"pub open spec fn {name}_post<T>(\n"
            "    input_initial: Seq<T>,\n    caller_final: Option<T>,\n"
            "    observations: (Option<T>, Seq<T>),\n) -> bool {\n"
            "    match (observations.0, caller_final) {\n"
            "        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],\n"
            "        (Some(value), Some(written)) => {\n"
            "            &&& input_initial.len() > 0\n"
            f"            &&& value == input_initial[{index}]\n"
            f"            &&& observations.1 == input_initial.update({index}, written)\n"
            "        },\n        _ => false,\n    }\n}\n\n"
        )
    expected_contract += "}\n"
    pure_contract = contract.read_text()
    if pure_contract != expected_contract:
        raise ValueError(f"Mutable endpoint pure contract drift: {contract}")
    spans.append({
        "role": "contract", "kind": "pure-postconditions", "path": str(contract),
        "start": 1, "end": len(pure_contract.splitlines()), "text": pure_contract,
    })
    for name, start, endpoint, description, pattern, value, after, expected_body in (
        (
            "first_mut", 159, "first", "first element of", "[first, ..]", 5, "[5, 1, 2]",
            "    if slice.len() == 0 { None } else { Some(&mut slice[0]) }",
        ),
        (
            "last_mut", 285, "last", "last item in", "[.., last]", 10, "[0, 1, 10]",
            "    if slice.len() == 0 {\n"
            "        None\n    } else {\n"
            "        let i = slice.len() - 1;\n"
            "        Some(&mut slice[i])\n    }",
        ),
    ):
        documentation = (
            f"    /// Returns a mutable reference to the {description} the slice, "
            "or `None` if it is empty.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let x = &mut [0, 1, 2];\n    ///\n"
            f"    /// if let Some({endpoint}) = x.{name}() {{\n"
            f"    ///     *{endpoint} = {value};\n    /// }}\n"
            f"    /// assert_eq!(x, &{after});\n    ///\n"
            "    /// let y: &mut [i32] = &mut [];\n"
            f"    /// assert_eq!(None, y.{name}());\n    /// ```\n"
        )
        attributes = (
            '    #[stable(feature = "rust1", since = "1.0.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_first_last", since = "1.83.0")]\n'
            "    #[inline]\n    #[must_use]\n"
        )
        function = (
            f"    pub const fn {name}(&mut self) -> Option<&mut T> {{\n"
            f"        if let {pattern} = self {{ Some({endpoint}) }} else {{ None }}\n"
            "    }\n"
        )
        for kind, first, last, expected in (
            ("documentation", start, start + 14, documentation),
            ("attributes", start + 15, start + 18, attributes),
            ("function", start + 19, start + 21, function),
        ):
            text = "".join(lines[first - 1:last])
            if text != expected:
                raise ValueError(f"Source span changed: {SOURCE}:{first}-{last}")
            spans.append({
                "role": "authority", "name": name, "kind": kind, "path": str(SOURCE),
                "start": first, "end": last, "text": text,
            })
        lifted = re.sub(
            r"\bself\b", "slice",
            text.replace(f"fn {name}(&mut self)", f"fn {name}<T>(slice: &mut [T])", 1),
        )
        original_body = lifted.splitlines()[1][4:]
        originals.append(
            f"// {SOURCE}:{start}-{start + 21}\n" + documentation
            + "    #[inline]\n    #[must_use]\n" + lifted
        )
        signature = f"pub const fn {name}<T>(slice: &mut [T]) -> (result: Option<&mut T>)"
        ensures = (
            "    ensures\n"
            f"        contracts::{name}_post(\n"
            "            old(slice)@,\n"
            "            match result { None => None, Some(value) => Some(*final(value)) },\n"
            "            (match result { None => None, Some(value) => Some(*value) }, final(slice)@),\n"
            "        ),"
        )
        mapping = {
            "api": f"<[T]>::{name}",
            "authority": {"path": str(SOURCE), "start": start, "end": start + 21},
            "original_body": original_body,
            "native_original": f"original::{name}", "native_adopted": f"adopted::{name}",
            "native_public": f"<[T]>::{name}",
            "lifting": (
                "Authority functions only gain explicit <T> and self -> slice; "
                "stability attributes are retained as evidence, not compiled. "
                "The adopted current proof's named return and exact pure old/final "
                "mapping are erased; its executable body is extracted without "
                "substitution."
            ),
        }
        path = MUTABLE_ENDPOINT_PROOFS / f"{name}.rs"
        contract_import = "../../../specs/slice/mutable_endpoints.rs"
        prefix = (
            f'use vstd::prelude::*;\n#[path = "{contract_import}"]\n'
            "mod contracts;\n\nverus! {\n"
            f"// Rust 1.96 core/src/slice/mod.rs:{start}-{start + 21}; "
            f"body:{start + 19}-{start + 21}.\n"
        )
        proof = path.read_text()
        match = re.fullmatch(
            re.escape(prefix) + f"(?P<signature>{re.escape(signature)})\n"
            + f"(?P<ensures>{re.escape(ensures)})" + r"\n\{\n(?P<body>.*?)\n\}\n\}\n",
            proof, re.DOTALL,
        )
        if match is None or match["body"] != expected_body:
            raise ValueError(f"Mutable endpoint current source drift: {path}")
        body_start = proof[:match.start("body")].count("\n") + 1
        spans.append({
            "role": "current", "name": name, "kind": "proof", "path": str(path),
            "start": 1, "end": len(proof.splitlines()), "text": proof,
        })
        mapping["current"] = {
            "path": str(path), "signature": match["signature"], "body": match["body"],
            "body_start": body_start,
            "body_end": body_start + len(match["body"].splitlines()) - 1,
            "contract": str((path.parent / contract_import).resolve()),
            "ensures": match["ensures"],
        }
        native_signature = match["signature"].replace(
            "-> (result: Option<&mut T>)", "-> Option<&mut T>", 1,
        )
        adopted.append(
            f"// ADOPTED current source-proof input: {path}:{body_start}\n"
            + native_signature + " {\n" + match["body"] + "\n}\n"
        )
        mappings.append(mapping)
    return (
        "// ADOPTED first_mut/last_mut only; permission: issues/V-SLICE-PATTERN.md.\n"
        "pub mod original {\n" + "\n".join(originals) + "}\n\n"
        "pub mod adopted {\n" + "\n".join(adopted) + "}\n",
        spans, mappings,
    )


def mutable_endpoint_negative_cases():
    cases = {
        "wrong-receiver": ("fn bad() { let _ = API([1u8]); }", "E0308"),
        "missing-receiver": ("fn bad() { let _ = API(); }", "E0061"),
        "extra-argument": ("fn bad() { let _ = API(&mut [1u8], 2u8); }", "E0061"),
        "shared-receiver": ("fn bad(input: &[u8]) { let _ = API(input); }", "E0308"),
        "immutable-binding": (
            "fn bad() { let input = [1u8]; let _ = API(&mut input); }", "E0596",
        ),
        "wrong-element": (
            "fn bad() { let mut input = [1u16]; let _ = API(&mut input); }", "E0308",
        ),
        "owned-result": (
            "fn bad() { let _: Option<u8> = API(&mut [1u8]); }", "E0308",
        ),
        "slice-result": (
            "fn bad() { let _: Option<&mut [u8]> = API(&mut [1u8]); }", "E0308",
        ),
        "missing-option": (
            "fn bad(input: &mut [u8]) -> &mut u8 { API(input) }", "E0308",
        ),
        "shared-function-result": (
            "fn bad() { let _: for<'a> fn(&'a mut [u8]) -> Option<&'a u8> = API; }",
            "E0308",
        ),
        "shared-function-argument": (
            "fn bad() { let _: for<'a> fn(&'a [u8]) -> Option<&'a mut u8> = API; }",
            "E0308",
        ),
        "local-escape": (
            "fn bad<'a>() -> Option<&'a mut u8> { let mut input = [1u8]; "
            "API(&mut input) }", "E0515",
        ),
        "short-lifetime": (
            "fn bad() { let view; { let mut input = [1u8]; view = API(&mut input); } "
            "*view.unwrap() = 2; }", "E0597",
        ),
        "static-escape": (
            "fn bad(input: &mut [u8]) -> Option<&'static mut u8> { API(input) }", None,
        ),
        "conflicting-shared-access": (
            "fn bad(input: &mut [u8]) { let result = API(input).unwrap(); "
            "let shared: &[u8] = &*input; core::hint::black_box(shared); *result = 2; }",
            "E0502",
        ),
        "conflicting-mutable-access": (
            "fn bad(input: &mut [u8]) { let result = API(input).unwrap(); "
            "let other: &mut [u8] = &mut *input; core::hint::black_box(other); *result = 2; }",
            "E0499",
        ),
    }
    for label in ("original", "adopted", "public"):
        for api in ("first_mut", "last_mut"):
            binding = f"<[u8]>::{api}" if label == "public" else f"{label}::{api}::<u8>"
            for name, (text, code) in cases.items():
                expected = {"code": code}
                if code is None:
                    expected["message"] = "lifetime may not live long enough"
                yield f"{label}-{api}-{name}", text.replace("API", binding), expected


def mutable_split_source():
    spans, mappings, originals, adopted = [], [], [], []

    def retain(path, role, kind, start, end, *, expected=None, name=None):
        lines = path.read_text().splitlines(keepends=True)
        text = "".join(lines[start - 1:end])
        span = {
            "role": role, "kind": kind, "path": str(path),
            "start": start, "end": end, "text": text,
        }
        if name is not None:
            span["name"] = name
        spans.append(span)
        if len(lines) < end or (expected is not None and text != expected):
            raise ValueError(f"Source span changed: {path}:{start}-{end}")
        return text

    retain(SOURCE, "authority", "generic-impl", 101, 101, expected="impl<T> [T] {\n")
    retain(
        SOURCE, "native-dependency", "slice-len", 102, 118,
        expected=(
            "    /// Returns the number of elements in the slice.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let a = [1, 2, 3];\n"
            "    /// assert_eq!(a.len(), 3);\n    /// ```\n"
            '    #[lang = "slice_len_fn"]\n'
            '    #[stable(feature = "rust1", since = "1.0.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_len", since = "1.39.0")]\n'
            "    #[rustc_no_implicit_autorefs]\n    #[inline]\n    #[must_use]\n"
            "    pub const fn len(&self) -> usize {\n"
            "        ptr::metadata(self)\n    }\n"
        ),
    )
    for path, role, kind, start, end in (
        (SOURCE, "native-dependency", "split-at-mut", 1959, 1991),
        (SOURCE, "native-dependency", "split-at-mut-unchecked", 2056, 2112),
        (SOURCE, "native-dependency", "split-at-mut-checked", 2163, 2204),
        (SOURCE, "native-dependency", "as-mut-ptr", 730, 759),
        (SOURCE.with_name("raw.rs"), "native-dependency", "from-raw-parts-mut", 143, 196),
        (SOURCE.parent.parent / "ptr/docs/add.md", "native-dependency", "pointer-add", 1, 24),
        (MUTABLE_SPLIT_VSTD / "slice.rs", "vstd-contract", "slice-view", 13, 17),
        (MUTABLE_SPLIT_VSTD / "slice.rs", "vstd-contract", "slice-len", 71, 86),
        (MUTABLE_SPLIT_VSTD / "slice.rs", "vstd-contract", "slice-index-trait", 117, 169),
        (MUTABLE_SPLIT_VSTD / "slice.rs", "vstd-contract", "mutable-borrow-length", 218, 221),
        (
            MUTABLE_SPLIT_VSTD / "std_specs/slice.rs", "vstd-contract",
            "mutable-usize-index", 17, 46,
        ),
        (
            MUTABLE_SPLIT_VSTD / "std_specs/slice.rs", "vstd-contract",
            "split-at-mut", 525, 535,
        ),
        (
            MUTABLE_SPLIT_VSTD / "std_specs/slice.rs", "vstd-contract",
            "existing-split-first-mut", 554, 564,
        ),
    ):
        retain(path, role, kind, start, end)

    contract = MUTABLE_SPLIT_PROOFS.parents[2] / "specs/slice/mutable_splits_post.rs"
    expected_contract = "use vstd::prelude::*;\n\nverus! {\n\n"
    for name, index, remainder, reconstruction in (
        (
            "split_first_mut", "0", "1, input_initial.len() as int",
            "seq![written] + written_remainder",
        ),
        (
            "split_last_mut", "input_initial.len() - 1", "0, input_initial.len() - 1",
            "written_remainder + seq![written]",
        ),
    ):
        expected_contract += (
            f"pub open spec fn {name}_post<T>(\n"
            "    input_initial: Seq<T>,\n"
            "    caller_final: Option<(T, Seq<T>)>,\n"
            "    observations: (Option<(T, Seq<T>)>, Seq<T>),\n"
            ") -> bool {\n"
            "    match (observations.0, caller_final) {\n"
            "        (None, None) => input_initial.len() == 0 && observations.1 =~= seq![],\n"
            "        (Some((value, remainder)), Some((written, written_remainder))) => {\n"
            "            &&& input_initial.len() > 0\n"
            f"            &&& value == input_initial[{index}]\n"
            f"            &&& remainder == input_initial.subrange({remainder})\n"
            "            &&& written_remainder.len() == remainder.len()\n"
            f"            &&& observations.1 =~= {reconstruction}\n"
            "        },\n        _ => false,\n    }\n}\n\n"
        )
    expected_contract += "}\n"
    pure_contract = contract.read_text()
    if pure_contract != expected_contract:
        raise ValueError(f"Mutable split pure contract drift: {contract}")
    spans.append({
        "role": "contract", "kind": "pure-postconditions", "path": str(contract),
        "start": 1, "end": len(pure_contract.splitlines()), "text": pure_contract,
    })
    for name, start, endpoint, remainder, pattern, after, expected_body in (
        (
            "split_first_mut", 202, "first", "tail", "[first, tail @ ..]", "[3, 4, 5]",
            "    if slice.len() == 0 {\n"
            "        None\n    } else {\n"
            "        let (head, tail) = slice.split_at_mut(1);\n"
            "        proof {\n"
            "            vstd::slice::mut_ref_slice_len_eq(&tail);\n"
            "        }\n"
            "        Some((&mut head[0], tail))\n    }",
        ),
        (
            "split_last_mut", 244, "last", "init", "[init @ .., last]", "[4, 5, 3]",
            "    if slice.len() == 0 {\n"
            "        None\n    } else {\n"
            "        let i = slice.len() - 1;\n"
            "        let (init, last) = slice.split_at_mut(i);\n"
            "        proof {\n"
            "            vstd::slice::mut_ref_slice_len_eq(&init);\n"
            "        }\n"
            "        Some((&mut last[0], init))\n    }",
        ),
    ):
        documentation = (
            f"    /// Returns the {endpoint} and all the rest of the elements of the slice, "
            "or `None` if it is empty.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let x = &mut [0, 1, 2];\n    ///\n"
            f"    /// if let Some(({endpoint}, elements)) = x.{name}() {{\n"
            f"    ///     *{endpoint} = 3;\n"
            "    ///     elements[0] = 4;\n    ///     elements[1] = 5;\n    /// }\n"
            f"    /// assert_eq!(x, &{after});\n    /// ```\n"
        )
        attributes = (
            '    #[stable(feature = "slice_splits", since = "1.5.0")]\n'
            '    #[rustc_const_stable(feature = "const_slice_first_last", since = "1.83.0")]\n'
            "    #[inline]\n    #[must_use]\n"
        )
        function = (
            f"    pub const fn {name}(&mut self) -> Option<(&mut T, &mut [T])> {{\n"
            f"        if let {pattern} = self {{ Some(({endpoint}, {remainder})) }} else {{ None }}\n"
            "    }\n"
        )
        for kind, first, last, expected in (
            ("documentation", start, start + 13, documentation),
            ("attributes", start + 14, start + 17, attributes),
            ("function", start + 18, start + 20, function),
        ):
            text = retain(
                SOURCE, "authority", kind, first, last, expected=expected, name=name,
            )
        lifted = re.sub(
            r"\bself\b", "slice",
            text.replace(f"fn {name}(&mut self)", f"fn {name}<T>(slice: &mut [T])", 1),
        )
        original_body = lifted.splitlines()[1][4:]
        originals.append(
            f"// {SOURCE}:{start}-{start + 20}\n" + documentation
            + "    #[inline]\n    #[must_use]\n" + lifted
        )
        signature = (
            f"pub const fn {name}<T>(slice: &mut [T])"
            " -> (result: Option<(&mut T, &mut [T])>)"
        )
        ensures = (
            "    ensures\n"
            f"        contracts::{name}_post(\n"
            "            old(slice)@,\n"
            "            match result {\n"
            "                None => None,\n"
            "                Some((value, remainder)) => Some((*final(value), final(remainder)@)),\n"
            "            },\n"
            "            (\n"
            "                match result {\n"
            "                    None => None,\n"
            "                    Some((value, remainder)) => Some((*value, remainder@)),\n"
            "                },\n"
            "                final(slice)@,\n"
            "            ),\n"
            "        ),"
        )
        mapping = {
            "api": f"<[T]>::{name}",
            "authority": {"path": str(SOURCE), "start": start, "end": start + 20},
            "original_body": original_body,
            "native_original": f"original::{name}", "native_adopted": f"adopted::{name}",
            "native_public": f"<[T]>::{name}",
            "lifting": (
                "Authority functions only gain explicit <T> and self -> slice; "
                "stability attributes are recorded, not compiled. Current adopted "
                "proof imports, signatures, pure ensures "
                "and bodies must match exactly. Only named returns, ensures and the "
                "exact existing mutable borrow-length proof call are erased; "
                "other ghost additions are rejected, not silently erased. "
                "The exact current bodies were independently permitted in "
                "issues/V-SLICE-PATTERN.md; historical proposals are not inputs."
            ),
        }
        path = MUTABLE_SPLIT_PROOFS / f"{name}.rs"
        contract_import = "../../../specs/slice/mutable_splits_post.rs"
        proof = path.read_text()
        prefix = (
            f'use vstd::prelude::*;\n#[path = "{contract_import}"]\n'
            "mod contracts;\n\nverus! {\n"
            f"// Rust 1.96 core/src/slice/mod.rs:{start}-{start + 20}; "
            f"body:{start + 18}-{start + 20}.\n"
        )
        match = re.fullmatch(
            re.escape(prefix) + f"(?P<signature>{re.escape(signature)})\n"
            + f"(?P<ensures>{re.escape(ensures)})" + r"\n\{\n(?P<body>.*?)\n\}\n\}\n",
            proof, re.DOTALL,
        )
        if match is None or match["body"] != expected_body:
            raise ValueError(
                f"Mutable split current source drift (including unsupported ghost changes): {path}"
            )
        body_start = proof[:match.start("body")].count("\n") + 1
        spans.append({
            "role": "current", "name": name, "kind": "proof", "path": str(path),
            "start": 1, "end": len(proof.splitlines()), "text": proof,
        })
        length_proof = (
            "        proof {\n"
            f"            vstd::slice::mut_ref_slice_len_eq(&{remainder});\n"
            "        }\n"
        )
        native_body = match["body"].replace(length_proof, "", 1)
        mapping["current"] = {
            "path": str(path), "signature": match["signature"], "body": match["body"],
            "body_start": body_start,
            "body_end": body_start + len(match["body"].splitlines()) - 1,
            "contract": str((path.parent / contract_import).resolve()),
            "ensures": match["ensures"], "erased_proof": length_proof,
            "native_body": native_body,
        }
        native_signature = match["signature"].replace(
            "-> (result: Option<(&mut T, &mut [T])>)", "-> Option<(&mut T, &mut [T])>", 1,
        )
        adopted.append(
            f"// ADOPTED current source-proof input: {path}:{body_start}\n"
            + native_signature + " {\n" + native_body + "\n}\n"
        )
        mappings.append(mapping)
    return (
        "// ADOPTED mutable splits; permission: issues/V-SLICE-PATTERN.md.\n"
        "pub mod original {\n" + "\n".join(originals) + "}\n\n"
        "pub mod adopted {\n" + "\n".join(adopted) + "}\n",
        spans, mappings,
    )


def mutable_split_negative_cases():
    cases = {
        "wrong-receiver": ("fn bad() { let _ = API([1u8]); }", "E0308"),
        "missing-receiver": ("fn bad() { let _ = API(); }", "E0061"),
        "extra-argument": ("fn bad() { let _ = API(&mut [1u8], 2u8); }", "E0061"),
        "shared-receiver": ("fn bad(input: &[u8]) { let _ = API(input); }", "E0308"),
        "immutable-binding": (
            "fn bad() { let input = [1u8]; let _ = API(&mut input); }", "E0596",
        ),
        "wrong-element": (
            "fn bad() { let mut input = [1u16]; let _ = API(&mut input); }", "E0308",
        ),
        "wrong-result-element": (
            "fn bad() { let _: Option<(&mut u16, &mut [u8])> = API(&mut [1u8]); }", "E0308",
        ),
        "wrong-result-remainder": (
            "fn bad() { let _: Option<(&mut u8, &mut [u16])> = API(&mut [1u8]); }", "E0308",
        ),
        "reversed-result": (
            "fn bad() { let _: Option<(&mut [u8], &mut u8)> = API(&mut [1u8]); }", "E0308",
        ),
        "owned-element": (
            "fn bad() { let _: Option<(u8, &mut [u8])> = API(&mut [1u8]); }", "E0308",
        ),
        "owned-remainder": (
            "fn bad() { let _: Option<(&mut u8, Vec<u8>)> = API(&mut [1u8]); }", "E0308",
        ),
        "missing-option": (
            "fn bad(input: &mut [u8]) -> (&mut u8, &mut [u8]) { API(input) }", "E0308",
        ),
        "shared-function-argument": (
            "fn bad() { let _: for<'a> fn(&'a [u8]) -> "
            "Option<(&'a mut u8, &'a mut [u8])> = API; }", "E0308",
        ),
        "shared-function-element": (
            "fn bad() { let _: for<'a> fn(&'a mut [u8]) -> "
            "Option<(&'a u8, &'a mut [u8])> = API; }", "E0308",
        ),
        "shared-function-remainder": (
            "fn bad() { let _: for<'a> fn(&'a mut [u8]) -> "
            "Option<(&'a mut u8, &'a [u8])> = API; }", "E0308",
        ),
        "shared-function-results": (
            "fn bad() { let _: for<'a> fn(&'a mut [u8]) -> "
            "Option<(&'a u8, &'a [u8])> = API; }", "E0308",
        ),
    }
    for component, position, ty, write, first_write, second_write in (
        ("element", 0, "u8", "*view = 3", "*first = 3", "*second = 4"),
        ("remainder", 1, "[u8]", "view[0] = 3", "first[0] = 3", "second[0] = 4"),
    ):
        bind = f"let view = API(input).unwrap().{position}; "
        cases.update({
            f"local-{component}": (
                f"fn bad<'a>() -> &'a mut {ty} {{ let mut input = [1u8, 2]; "
                f"API(&mut input).unwrap().{position} }}", "E0515",
            ),
            f"short-{component}": (
                "fn bad() { let view; { let mut input = [1u8, 2]; "
                f"view = API(&mut input).unwrap().{position}; }} {write}; }}", "E0597",
            ),
            f"static-{component}": (
                f"fn bad(input: &mut [u8]) -> &'static mut {ty} "
                f"{{ API(input).unwrap().{position} }}", None,
            ),
            f"conflicting-shared-{component}": (
                "fn bad(input: &mut [u8]) { " + bind
                + f"core::hint::black_box(&*input); {write}; }}", "E0502",
            ),
            f"conflicting-mutable-{component}": (
                "fn bad(input: &mut [u8]) { " + bind
                + f"core::hint::black_box(&mut *input); {write}; }}", "E0499",
            ),
            f"duplicate-mutable-{component}": (
                "fn bad(input: &mut [u8]) { " + bind
                + "let first = &mut *view; let second = &mut *view; "
                + f"{first_write}; {second_write}; }}", "E0499",
            ),
            f"shared-then-mutable-{component}": (
                "fn bad(input: &mut [u8]) { " + bind
                + "let first = &*view; let second = &mut *view; "
                + f"core::hint::black_box(first); {second_write}; }}", "E0502",
            ),
            f"duplicate-moved-{component}": (
                "fn bad(input: &mut [u8]) { " + bind
                + f"let first = view; let second = view; {first_write}; {second_write}; }}",
                "E0382",
            ),
        })
    for name, select, borrows in (
        (
            "overlap-remainder-element-first", 1,
            "let element = &mut view[0]; let remainder = &mut view[..]; ",
        ),
        (
            "overlap-remainder-slice-first", 1,
            "let remainder = &mut view[..]; let element = API(&mut *view).unwrap().0; ",
        ),
        (
            "overlap-element-element-first", 0,
            "let element = &mut *view; let remainder = core::slice::from_mut(&mut *view); ",
        ),
        (
            "overlap-element-slice-first", 0,
            "let remainder = core::slice::from_mut(&mut *view); let element = &mut *view; ",
        ),
    ):
        cases[name] = (
            f"fn bad(input: &mut [u8]) {{ let view = API(input).unwrap().{select}; "
            + borrows + "*element = 3; remainder[0] = 4; }", "E0499",
        )
    for label in ("original", "adopted", "public"):
        for api in ("split_first_mut", "split_last_mut"):
            binding = f"<[u8]>::{api}" if label == "public" else f"{label}::{api}::<u8>"
            for name, (text, code) in cases.items():
                expected = {"code": code}
                if code is None:
                    expected["message"] = "lifetime may not live long enough"
                yield f"{label}-{api}-{name}", text.replace("API", binding), expected


def split_off_endpoint_source():
    spans, mappings, originals, adopted = [], [], [], []

    def retain(path, role, kind, start, end, *, expected=None, name=None):
        lines = path.read_text().splitlines(keepends=True)
        text = "".join(lines[start - 1:end])
        if len(lines) < end or (expected is not None and text != expected):
            raise ValueError(f"Source span changed: {path}:{start}-{end}")
        span = {
            "role": role, "kind": kind, "path": str(path),
            "start": start, "end": end, "text": text,
        }
        if name is not None:
            span["name"] = name
        spans.append(span)
        return text

    def ensures(name, module):
        return (
            "    ensures\n"
            f"        {module}::{name}_post(\n"
            "            (*old(slice))@,\n"
            "            (\n"
            "                match result {\n"
            "                    None => None,\n"
            "                    Some(value) => Some(*value),\n"
            "                },\n"
            "                (*final(slice))@,\n"
            "            ),\n"
            "        ),"
        )

    def extract(path, role, prefix, signature, postcondition, expected_body, contract_import):
        proof = path.read_text()
        match = re.fullmatch(
            re.escape(prefix) + f"(?P<signature>{re.escape(signature)})\n"
            + f"(?P<ensures>{re.escape(postcondition)})"
            + r"\n\{\n(?P<body>.*?)\n\}\n\}\n",
            proof, re.DOTALL,
        )
        if match is None or match["body"] != expected_body:
            raise ValueError(f"Split-off endpoint {role} source drift: {path}")
        body_start = proof[:match.start("body")].count("\n") + 1
        spans.append({
            "role": role, "kind": "proof", "path": str(path),
            "start": 1, "end": len(proof.splitlines()), "text": proof,
        })
        record = {
            "path": str(path), "signature": match["signature"], "body": match["body"],
            "body_start": body_start,
            "body_end": body_start + len(match["body"].splitlines()) - 1,
            "ensures": match["ensures"],
            "contract": str((path.parent / contract_import).resolve()),
        }
        native_signature = match["signature"].replace("-> (result: ", "-> ", 1).removesuffix(")")
        label = "ADOPTED current" if role == "current" else role.upper()
        native = (
            f"// {label} source-proof input: {path}:{body_start}\n"
            + native_signature + " {\n" + match["body"] + "\n}\n"
        )
        return native, record

    retain(SOURCE, "authority", "generic-impl", 101, 101, expected="impl<T> [T] {\n")
    for kind, start, end in (
        ("slice-len", 102, 118), ("split-first", 182, 200), ("split-last", 224, 242),
        ("split-at", 1913, 1957), ("split-at-unchecked", 1993, 2054),
        ("split-at-checked", 2114, 2161),
    ):
        retain(SOURCE, "native-dependency", kind, start, end)

    contract = SPLIT_OFF_ENDPOINT_PROOFS.parents[2] / "specs/slice/split_off_post.rs"
    public_contract = contract.with_name("split_off.rs")
    expected_contract = "use vstd::prelude::*;\n\nverus! {\n\n"
    expected_public = (
        'use vstd::prelude::*;\n\n#[path = "split_off_post.rs"]\npub mod post;\n\nverus! {\n\n'
    )
    endpoints = (
        ("first", 4993, "a", "['b', 'c']", "0", "1, input_initial.len() as int"),
        ("last", 5043, "c", "['a', 'b']", "input_initial.len() - 1", "0, input_initial.len() - 1"),
    )
    for endpoint, start, _, _, index, remainder in endpoints:
        name = f"split_off_{endpoint}"
        expected_contract += (
            f"pub open spec fn {name}_post<T>(\n"
            "    input_initial: Seq<T>,\n"
            "    observations: (Option<T>, Seq<T>),\n"
            ") -> bool {\n"
            "    match observations.0 {\n"
            "        None => input_initial.len() == 0 && observations.1 =~= input_initial,\n"
            "        Some(value) => {\n"
            "            &&& input_initial.len() > 0\n"
            f"            &&& value == input_initial[{index}]\n"
            f"            &&& observations.1 =~= input_initial.subrange({remainder})\n"
            "        },\n    }\n}\n\n"
        )
        expected_public += (
            f"// Rust 1.96 slice/mod.rs:{start}-{start + 22}; "
            "const use requires const_split_off_first_last.\n"
            f"pub assume_specification<'a, T>[ <[T]>::{name} ](\n"
            "    slice: &mut &'a [T],\n"
            ") -> (result: Option<&'a T>)\n"
            + ensures(name, "post") + "\n    no_unwind\n;\n\n"
        )
    for path, kind, expected in (
        (contract, "pure-postconditions", expected_contract + "}\n"),
        (public_contract, "public-declarations", expected_public + "}\n"),
    ):
        text = path.read_text()
        if text != expected:
            raise ValueError(f"Split-off endpoint {kind} drift: {path}")
        spans.append({
            "role": "contract", "kind": kind, "path": str(path),
            "start": 1, "end": len(text.splitlines()), "text": text,
        })

    dependency_import = "split_last.rs"
    dependency_native = ""
    for endpoint, start, value, rest, _, _ in endpoints:
        name = f"split_off_{endpoint}"
        documentation = (
            f"    /// Removes the {endpoint} element of the slice and returns a reference\n"
            "    /// to it.\n    ///\n"
            "    /// Returns `None` if the slice is empty.\n"
            "    ///\n    /// # Examples\n    ///\n    /// ```\n"
            "    /// let mut slice: &[_] = &['a', 'b', 'c'];\n"
            f"    /// let {endpoint} = slice.{name}().unwrap();\n    ///\n"
            f"    /// assert_eq!(slice, &{rest});\n"
            f"    /// assert_eq!({endpoint}, &'{value}');\n    /// ```\n"
        )
        attributes = (
            "    #[inline]\n"
            '    #[stable(feature = "slice_take", since = "1.87.0")]\n'
            '    #[rustc_const_unstable(feature = "const_split_off_first_last", issue = "138539")]\n'
        )
        function = (
            f"    pub const fn {name}<'a>(self: &mut &'a Self) -> Option<&'a T> {{\n"
            "        // FIXME(const-hack): Use `?` when available in const instead of `let-else`.\n"
            f"        let Some(({endpoint}, rem)) = self.split_{endpoint}() else {{ return None }};\n"
            "        *self = rem;\n"
            f"        Some({endpoint})\n"
            "    }\n"
        )
        for kind, first, last, expected in (
            ("documentation", start, start + 13, documentation),
            ("attributes", start + 14, start + 16, attributes),
            ("function", start + 17, start + 22, function),
        ):
            text = retain(SOURCE, "authority", kind, first, last, expected=expected, name=name)
        lifted = re.sub(
            r"\bself\b", "slice",
            text.replace(
                f"fn {name}<'a>(self: &mut &'a Self)",
                f"fn {name}<'a, T>(slice: &mut &'a [T])", 1,
            ),
        )
        lifted = "\n".join(line[4:] for line in lifted.splitlines()) + "\n"
        original_body = "\n".join(lifted.splitlines()[1:-1])
        originals.append(
            f"// Authority: {SOURCE}:{start}-{start + 22}\n"
            + documentation + "#[inline]\n" + lifted
        )
        signature = (
            f"pub const fn {name}<'a, T>(slice: &mut &'a [T]) -> (result: Option<&'a T>)"
        )
        contract_import = "../../../specs/slice/split_off_post.rs"
        local_import = (
            f'#[path = "{dependency_import}"]\nmod split_dependency;\n'
            if endpoint == "last" else ""
        )
        expected_body = (
            original_body.replace("slice.split_last()", "split_dependency::split_last(*slice)", 1)
            if endpoint == "last" else original_body
        )
        native, formal = extract(
            SPLIT_OFF_ENDPOINT_PROOFS / f"{name}.rs", "current",
            f'use vstd::prelude::*;\n#[path = "{contract_import}"]\n'
            "mod contracts;\n" + local_import + "\nverus! {\n"
            f"// Rust 1.96 core/src/slice/mod.rs:{start}-{start + 22}; "
            f"body:{start + 18}-{start + 21}.\n",
            signature, ensures(name, "contracts"), expected_body, contract_import,
        )
        adopted.append(native)
        mapping = {
            "api": f"<[T]>::{name}",
            "authority": {"path": str(SOURCE), "start": start, "end": start + 22},
            "original_body": original_body, "current": formal,
            "native_original": f"original::{name}", "native_adopted": f"adopted::{name}",
            "native_public": f"<[T]>::{name}",
            "runtime_stable_since": "1.87.0",
            "public_const": "UNSTABLE: const_split_off_first_last; rejected without feature",
            "lifting": (
                "Only the authority receiver is lifted (self -> slice, Self -> [T], explicit T); "
                "compiler-internal stability attributes are recorded, not compiled. "
                "Exact Verus wrappers/imports, named return and exact ghost ensures are erased. "
                "Every executable body is extracted unchanged from its own actual file. "
                "Return-state observations use (*old(slice))@, Option<T> and (*final(slice))@; "
                "there is no caller-final environment or mutable returned reference."
            ),
        }
        if endpoint == "last":
            dependency_contract = "../../../specs/slice/mod.rs"
            dependency_native, dependency = extract(
                Path(formal["path"]).parent / dependency_import, "dependency",
                f'use vstd::prelude::*;\n#[path = "{dependency_contract}"]\n'
                "mod contracts;\n\nverus! {\n"
                "// Rust 1.96 core/src/slice/mod.rs:224-242; body:240-242.\n",
                "pub const fn split_last<T>(slice: &[T]) -> (result: Option<(&T, &[T])>)",
                "    ensures\n        contracts::split_last_post(slice, result),",
                "    if slice.len() == 0 {\n"
                "        None\n"
                "    } else {\n"
                "        let i = slice.len() - 1;\n"
                "        Some((&slice[i], slice.split_at(i).0))\n"
                "    }",
                dependency_contract,
            )
            formal["dependency_import"] = dependency_import
            formal["dependency"] = dependency
        mappings.append(mapping)
    return (
        "// ADOPTED current split-off endpoints; only the last call/import changed.\n"
        "// Permission: issues/V-ASCII-CALL-BINDING.md"
        "#independent-split-off-permission-before-adoption.\n"
        "pub mod original {\n" + "\n".join(originals) + "}\n\n"
        "pub mod adopted {\nmod split_dependency {\n" + dependency_native + "}\n"
        + "\n".join(adopted) + "}\n",
        spans, mappings,
    )


def split_off_endpoint_negative_cases():
    slot = "let mut slice: &[u8] = &[1, 2]; "
    cases = {
        "wrong-receiver": ("fn bad() { let _ = API([1u8]); }", "E0308"),
        "missing-receiver": ("fn bad() { let _ = API(); }", "E0061"),
        "extra-argument": ("fn bad() { " + slot + "let _ = API(&mut slice, 2u8); }", "E0061"),
        "shared-slot": ("fn bad() { " + slot + "let _ = API(&slice); }", "E0308"),
        "direct-mutable-slice": (
            "fn bad(input: &mut [u8]) { let _ = API(input); }", "E0308",
        ),
        "immutable-slot": (
            "fn bad() { let slice: &[u8] = &[1, 2]; let _ = API(&mut slice); }", "E0596",
        ),
        "wrong-element": (
            "fn bad() { let mut slice: &[u16] = &[1, 2]; let _ = API(&mut slice); }", "E0308",
        ),
        "wrong-result-element": (
            "fn bad() { " + slot + "let _: Option<&u16> = API(&mut slice); }", "E0308",
        ),
        "mutable-result": (
            "fn bad() { " + slot + "let _: Option<&mut u8> = API(&mut slice); }", "E0308",
        ),
        "owned-result": (
            "fn bad() { " + slot + "let _: Option<u8> = API(&mut slice); }", "E0308",
        ),
        "slice-result": (
            "fn bad() { " + slot + "let _: Option<&[u8]> = API(&mut slice); }", "E0308",
        ),
        "missing-option": (
            "fn bad() { " + slot + "let _: &u8 = API(&mut slice); }", "E0308",
        ),
        "write-through-result": (
            "fn bad() { " + slot + "*API(&mut slice).unwrap() = 3; }", "E0594",
        ),
        "local-escape": (
            "fn bad<'a>() -> Option<&'a u8> { let input = [1u8, 2]; "
            "let mut slice = &input[..]; API(&mut slice) }", "E0515",
        ),
        "short-lifetime": (
            "fn bad() { let result; { let input = [1u8, 2]; let mut slice = &input[..]; "
            "result = API(&mut slice); } core::hint::black_box(result); }", "E0597",
        ),
        "static-escape": (
            "fn bad(input: &[u8]) -> Option<&'static u8> { "
            "let mut slice = input; API(&mut slice) }", None,
        ),
        "shared-function-argument": (
            "fn bad() { let _: for<'a, 'b> fn(&'b &'a [u8]) -> Option<&'a u8> = API; }",
            "E0308",
        ),
        "mutable-function-result": (
            "fn bad() { let _: for<'a, 'b> fn(&'b mut &'a [u8]) -> Option<&'a mut u8> = API; }",
            "E0308",
        ),
    }
    for label, apis in (
        ("original", ("split_off_first", "split_off_last")),
        ("adopted", ("split_off_first", "split_off_last")),
        ("public", ("split_off_first", "split_off_last")),
    ):
        for api in apis:
            binding = f"<[u8]>::{api}" if label == "public" else f"{label}::{api}::<u8>"
            for name, (text, code) in cases.items():
                expected = {"code": code}
                if code is None:
                    expected["message"] = "lifetime may not live long enough"
                yield f"{label}-{api}-{name}", text.replace("API", binding), expected
            if label == "public":
                yield (
                    f"public-{api}-const-without-feature",
                    "const BAD: Option<&u8> = { " + slot + f"{binding}(&mut slice) }};",
                    {
                        "code": None,
                        "message": (
                            f"`core::slice::<impl [T]>::{api}` is not yet stable as a const fn"
                        ),
                    },
                )


def ascii_case_source():
    lines = ASCII_CASE_SOURCE.read_text().splitlines()
    copies = []
    spans = []
    for direction, start, first, last, mapped_first, mapped_last in (
        ("upper", 161, "a", "z", "A", "Z"),
        ("lower", 183, "A", "Z", "a", "z"),
    ):
        name = f"make_ascii_{direction}case"
        documentation = (
            f"    /// Converts this slice to its ASCII {direction} case equivalent in-place.\n"
            "    ///\n"
            f"    /// ASCII letters '{first}' to '{last}' are mapped to '{mapped_first}' to '{mapped_last}',\n"
            "    /// but non-ASCII letters are unchanged.\n"
            "    ///\n"
            f"    /// To return a new {direction}cased value without modifying the existing one, use\n"
            f"    /// [`to_ascii_{direction}case`].\n"
            "    ///\n"
            f"    /// [`to_ascii_{direction}case`]: #method.to_ascii_{direction}case"
        )
        attributes = (
            '    #[stable(feature = "ascii_methods_on_intrinsics", since = "1.23.0")]\n'
            '    #[rustc_const_stable(feature = "const_make_ascii", since = "1.84.0")]\n'
            "    #[inline]"
        )
        function = (
            f"    pub const fn {name}(&mut self) {{\n"
            "        // FIXME(const-hack): We would like to simply iterate using `for` loops but this isn't currently allowed in constant expressions.\n"
            "        let mut i = 0;\n"
            "        while i < self.len() {\n"
            "            let byte = &mut self[i];\n"
            f"            byte.{name}();\n"
            "            i += 1;\n"
            "        }\n"
            "    }"
        )
        for kind, first_line, last_line, expected in (
            ("documentation", start, start + 8, documentation),
            ("attributes", start + 9, start + 11, attributes),
            ("function", start + 12, start + 20, function),
        ):
            text = "\n".join(lines[first_line - 1 : last_line])
            if text != expected:
                raise ValueError(
                    f"Source span changed: {ASCII_CASE_SOURCE}:{first_line}-{last_line}"
                )
            spans.append({
                "module": "slice", "name": name, "kind": kind,
                "path": str(ASCII_CASE_SOURCE),
                "start": first_line, "end": last_line, "text": text,
            })
        lifted = text.replace(
            f"fn {name}(&mut self)", f"fn {name}(slice: &mut [u8])", 1,
        )
        lifted = re.sub(r"\bself\b", "slice", lifted)
        copies.append(
            f"// {ASCII_CASE_SOURCE}:{start}-{start + 8}\n{documentation}\n"
            f"// {ASCII_CASE_SOURCE}:{start + 12}-{start + 20}\n"
            f"    #[inline]\n{lifted}\n"
        )
    return "\n".join(copies), spans


def ascii_case_negative_cases():
    cases = {
        "shared-receiver": (
            "fn bad() { let input: &[u8] = &[97]; API(input); }", "E0308",
        ),
        "wrong-element": (
            "fn bad() { let mut input = [97u16]; API(&mut input); }", "E0308",
        ),
        "wrong-result": (
            "fn bad() { let mut input = [97u8]; let _: usize = API(&mut input); }",
            "E0308",
        ),
        "extra-argument": (
            "fn bad() { let mut input = [97u8]; API(&mut input, 1u8); }", "E0061",
        ),
    }
    for label, binding in (("source", "source"), ("public", "<[u8]>")):
        for direction in ("uppercase", "lowercase"):
            for name, (text, code) in cases.items():
                yield (
                    f"{label}-{direction}-{name}",
                    text.replace("API", f"{binding}::make_ascii_{direction}"),
                    {"code": code},
                )


def singleton_source():
    blocks = {}
    spans = []
    for module, path, functions in (
        (
            "array", SINGLETON_ARRAY_SOURCE,
            (
                (166, 169, "pub const fn from_ref<T>(s: &T) -> &[T; 1] {"),
                (174, 177, "pub const fn from_mut<T>(s: &mut T) -> &mut [T; 1] {"),
            ),
        ),
        (
            "slice", SINGLETON_SLICE_SOURCE,
            (
                (203, 205, "pub const fn from_ref<T>(s: &T) -> &[T] {"),
                (211, 213, "pub const fn from_mut<T>(s: &mut T) -> &mut [T] {"),
            ),
        ),
    ):
        lines = path.read_text().splitlines()
        copies = []
        for start, end, signature in functions:
            text = "\n".join(lines[start - 1 : end])
            if not text.startswith(signature + "\n") or not text.endswith("\n}"):
                raise ValueError(f"Source span changed: {path}:{start}-{end}")
            spans.append({
                "module": module, "path": str(path),
                "start": start, "end": end, "text": text,
            })
            copies.append(f"// {path}:{start}-{end}\n{text}\n")
        blocks[module] = "\n".join(copies)
    return "mod array {\n" + blocks["array"] + "}\n\n" + blocks["slice"], spans


def singleton_negative_cases():
    cases = {
        "shared-missing-argument": (
            "fn bad() { let _ = API::from_ref::<u8>(); }", "E0061",
        ),
        "mutable-missing-argument": (
            "fn bad() { let _ = API::from_mut::<u8>(); }", "E0061",
        ),
        "shared-extra-argument": (
            "fn bad() { let value = 1u8; let _ = API::from_ref(&value, 2); }", "E0061",
        ),
        "mutable-extra-argument": (
            "fn bad() { let mut value = 1u8; let _ = API::from_mut(&mut value, 2); }",
            "E0061",
        ),
        "shared-value-argument": (
            "fn bad() { let _ = API::from_ref(1u8); }", "E0308",
        ),
        "mutable-value-argument": (
            "fn bad() { let _ = API::from_mut(1u8); }", "E0308",
        ),
        "shared-wrong-element": (
            "fn bad() { let _ = API::from_ref::<u8>(&1u16); }", "E0308",
        ),
        "mutable-wrong-element": (
            "fn bad() { let _ = API::from_mut::<u8>(&mut 1u16); }", "E0308",
        ),
        "shared-wrong-result": (
            "fn bad() { let _: usize = API::from_ref(&1u8); }", "E0308",
        ),
        "mutable-wrong-result": (
            "fn bad() { let _: usize = API::from_mut(&mut 1u8); }", "E0308",
        ),
        "shared-array-result": (
            "fn bad() { let _: &[u8; 1] = API::from_ref(&1u8); }", "E0308",
        ),
        "mutable-array-result": (
            "fn bad() { let _: &mut [u8; 1] = API::from_mut(&mut 1u8); }", "E0308",
        ),
        "shared-mutable-result": (
            "fn bad() { let _: &mut [u8] = API::from_ref(&1u8); }", "E0308",
        ),
        "mutable-shared-function-result": (
            "fn bad() { let _: for<'a> fn(&'a mut u8) -> &'a [u8] = "
            "API::from_mut::<u8>; }", "E0308",
        ),
        "mutable-shared-input": (
            "fn bad() { let value = 1u8; let _ = API::from_mut(&value); }", "E0308",
        ),
        "shared-write": (
            "fn bad() { let value = 1u8; let view = API::from_ref(&value); "
            "view[0] = 2; }", "E0594",
        ),
        "shared-local-escape": (
            "fn bad<'a>() -> &'a [u8] { let value = 1u8; API::from_ref(&value) }",
            "E0515",
        ),
        "mutable-local-escape": (
            "fn bad<'a>() -> &'a mut [u8] { let mut value = 1u8; "
            "API::from_mut(&mut value) }", "E0515",
        ),
        "shared-short-lifetime": (
            "fn bad() { let view; { let value = 1u8; view = API::from_ref(&value); } "
            "let _ = view[0]; }", "E0597",
        ),
        "mutable-short-lifetime": (
            "fn bad() { let view; { let mut value = 1u8; "
            "view = API::from_mut(&mut value); } view[0] = 2; }", "E0597",
        ),
        "shared-static-escape": (
            "fn bad(value: &u8) -> &'static [u8] { API::from_ref(value) }", None,
        ),
        "mutable-static-escape": (
            "fn bad(value: &mut u8) -> &'static mut [u8] { API::from_mut(value) }",
            None,
        ),
        "shared-unsized-str": (
            "fn bad() { let _ = API::from_ref::<str>; }", "E0277",
        ),
        "mutable-unsized-str": (
            "fn bad() { let _ = API::from_mut::<str>; }", "E0277",
        ),
        "shared-unsized-slice": (
            "fn bad() { let _ = API::from_ref::<[u8]>; }", "E0277",
        ),
        "mutable-unsized-slice": (
            "fn bad() { let _ = API::from_mut::<[u8]>; }", "E0277",
        ),
        "mutable-conflicting-mutable-borrow": (
            "fn bad() { let mut value = 1u8; let view = API::from_mut(&mut value); "
            "let _other = &mut value; view[0] = 2; }", "E0499",
        ),
        "mutable-conflicting-shared-borrow": (
            "fn bad() { let mut value = 1u8; let view = API::from_mut(&mut value); "
            "let _other = &value; view[0] = 2; }", "E0502",
        ),
        "mutable-conflicting-read": (
            "fn bad() { let mut value = 1u8; let view = API::from_mut(&mut value); "
            "let read = value; view[0] = read; }", "E0503",
        ),
        "mutable-conflicting-write": (
            "fn bad() { let mut value = 1u8; let view = API::from_mut(&mut value); "
            "value = 2; view[0] = 3; }", "E0506",
        ),
        "mutable-second-view": (
            "fn bad() { let mut value = 1u8; let view = API::from_mut(&mut value); "
            "let _other = API::from_mut(&mut value); view[0] = 2; }", "E0499",
        ),
        "shared-conflicting-write": (
            "fn bad() { let mut value = 1u8; let view = API::from_ref(&value); "
            "value = 2; let _ = view[0]; }", "E0506",
        ),
        "shared-conflicting-mutable-borrow": (
            "fn bad() { let mut value = 1u8; let view = API::from_ref(&value); "
            "let _other = &mut value; let _ = view[0]; }", "E0502",
        ),
    }
    for label, binding in (("source", "source"), ("public", "core::slice")):
        for name, (text, code) in cases.items():
            expected = {"code": code}
            if code is None:
                expected["message"] = "lifetime may not live long enough"
            yield f"{label}-{name}", text.replace("API::", binding + "::"), expected


def check_singleton_rejection(result, expected, log):
    try:
        diagnostics = [
            json.loads(line) for line in result.stderr.splitlines() if line.strip()
        ]
    except json.JSONDecodeError as error:
        raise AssertionError(f"Invalid rustc JSON diagnostics; see {log}") from error
    errors = []
    for item in diagnostics:
        if not isinstance(item, dict):
            raise AssertionError(f"Invalid rustc diagnostic object; see {log}")
        if item.get("level") != "error":
            continue
        if (
            item.get("code") is None and not item.get("spans")
            and re.fullmatch(
                r"aborting due to \d+ previous errors?(?:; \d+ warnings? emitted)?",
                item.get("message", ""),
            )
        ):
            continue
        errors.append({
            "code": (item.get("code") or {}).get("code"),
            "message": item.get("message"),
        })
    if (
        result.returncode != 1 or len(errors) != 1
        or any(errors[0].get(key) != value for key, value in expected.items())
    ):
        raise AssertionError(
            f"Expected rustc exit 1 and exactly one {expected} error; "
            f"got exit {result.returncode}, errors {errors}; see {log}"
        )
    return errors[0]


def check_singletons(output_root):
    output = output_root / "target/singleton/native"
    logs = output_root / "logs/singleton/native"
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    derived = output / "source_singletons.rs"
    binary = output / "singleton_behavior"
    environment = {
        **os.environ, "SLICE_SINGLETON_SOURCE": str(derived), "TMPDIR": str(output),
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands = []
    results = {"group": "singleton", "status": "failed", "negative_cases": []}

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log),
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "returncode": None,
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record["returncode"] = result.returncode
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(
                f"{name}: expected exit 0, got {result.returncode}; see {log}"
            )
        return result

    try:
        text, spans = singleton_source()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        derived.write_text(text)
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/singleton_behavior.rs", "-o", str(binary),
            ],
            "compile", success=True,
        )
        tested = run([str(binary), "--test-threads=1"], "behavior", success=True)
        summary = re.search(
            r"test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout,
        )
        if summary is None or int(summary[1]) == 0:
            raise AssertionError(
                f"Expected executed, nonempty singleton tests; see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = int(summary[1])
        print(tested.stdout.strip())
        for name, text, expected in singleton_negative_cases():
            probe = output / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rlib"
            log = logs / f"{name}.log"
            case = {"name": name, "expected": expected, "log": str(log), "passed": False}
            results["negative_cases"].append(case)
            try:
                probe.write_text(
                    '#![allow(dead_code, unused_variables, unused_assignments)]\n'
                    'mod source { include!(env!("SLICE_SINGLETON_SOURCE")); }\n'
                    + text + "\n"
                )
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        "--crate-name=singleton_rejection", "--error-format=json",
                        str(probe), "-o", str(rejected),
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                probe.unlink(missing_ok=True)
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"Singleton checks: {len(results['negative_cases'])} invalid signatures, "
            "lifetimes, unsized elements or conflicting borrows rejected."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        derived.unlink(missing_ok=True)
        binary.unlink(missing_ok=True)


def check_ascii_case(output_root):
    output = output_root / "target/ascii-case/native"
    logs = output_root / "logs/ascii-case/native"
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    derived = output / "source_ascii_case.rs"
    binary = output / "ascii_case_behavior"
    environment = {
        **os.environ, "SLICE_ASCII_CASE_SOURCE": str(derived), "TMPDIR": str(output),
        "RUSTUP_HOME": "/home/chentianyu/.rustup",
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands = []
    results = {"group": "ascii-case", "status": "failed", "negative_cases": []}
    temporaries = []

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log),
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "RUSTUP_HOME": environment["RUSTUP_HOME"], "returncode": None,
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record["returncode"] = result.returncode
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(
                f"{name}: expected exit 0, got {result.returncode}; see {log}"
            )
        return result

    try:
        text, spans = ascii_case_source()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        for path in (derived, binary):
            if path.exists():
                raise FileExistsError(f"Refusing to overwrite existing native artifact: {path}")
        temporaries.extend((derived, binary))
        derived.write_text(text)
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/ascii_case_behavior.rs", "-o", str(binary),
            ],
            "compile", success=True,
        )
        tested = run([str(binary), "--test-threads=1"], "behavior", success=True)
        summary = re.search(
            r"test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout,
        )
        if summary is None or int(summary[1]) != 17:
            raise AssertionError(
                f"Expected all 17 executed ASCII-case tests; see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = int(summary[1])
        print(tested.stdout.strip())
        for name, text, expected in ascii_case_negative_cases():
            probe = output / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rlib"
            log = logs / f"{name}.log"
            case = {"name": name, "expected": expected, "log": str(log), "passed": False}
            results["negative_cases"].append(case)
            for path in (probe, rejected):
                if path.exists():
                    raise FileExistsError(f"Refusing to overwrite existing native artifact: {path}")
            try:
                probe.write_text(
                    '#![allow(dead_code)]\n'
                    'mod source { include!(env!("SLICE_ASCII_CASE_SOURCE")); }\n'
                    + text + "\n"
                )
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        "--crate-name=ascii_case_rejection", "--error-format=json",
                        str(probe), "-o", str(rejected),
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                probe.unlink(missing_ok=True)
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"ASCII-case checks: {len(results['negative_cases'])} invalid receivers, "
            "element types, results or extra arguments rejected."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        for path in temporaries:
            path.unlink(missing_ok=True)


def check_endpoints(output_root):
    return check_pattern_comparison(output_root, splits=False)


def check_pattern_comparison(output_root, *, splits):
    if splits:
        group, stem, source_name = "splits", "split", "source_splits"
        source_environment = "SLICE_SPLITS_SOURCE"
        source_reader, negative_cases = split_source, split_negative_cases
        module, proof_role = "adopted", "current"
        apis, return_type = ("split_first", "split_last"), "Option<(&T, &[T])>"
        expected_tests, test_label = 15, "adopted split"
        source_status = (
            "ADOPTED current split_first/split_last source-proof bodies; "
            "permission: issues/V-SLICE-PATTERN.md"
        )
    else:
        group, stem, source_name = "endpoints", "endpoint", "source_endpoints"
        source_environment = "SLICE_ENDPOINTS_SOURCE"
        source_reader, negative_cases = endpoint_source, endpoint_negative_cases
        module, proof_role = "adopted", "current"
        apis, return_type = ("first", "last"), "Option<&T>"
        expected_tests, test_label = 14, "adopted endpoint"
        source_status = (
            "ADOPTED current first/last source-proof bodies; "
            "permission: issues/V-SLICE-PATTERN.md"
        )
    behavior_input = ROOT / f"tests/{'split_behavior' if splits else 'endpoint_proposal_behavior'}.rs"
    output = output_root / f"target/{group}/native"
    logs = output_root / f"logs/{group}/native"
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    derived = logs / f"{source_name}.rs"
    harness = logs / f"{stem}_behavior.rs"
    mir = logs / f"{stem}_behavior.mir"
    binary = output / f"{stem}_behavior"
    negatives = list(negative_cases())
    evidence = [
        derived, harness, mir, binary,
        *(logs / name for name in (
            "source-spans.json", "source-mappings.json", "dependencies.json",
            "commands.json", "results.json", "rustc-version.log", "compile.log",
            "behavior.log",
        )),
    ]
    for name, _, _ in negatives:
        evidence.extend((
            logs / f"{name}.log", output / f"rejection-{name}.rs",
            output / f"rejected-{name}.rlib",
        ))
    for path in evidence:
        if path.exists() or path.is_symlink():
            raise FileExistsError(
                f"Refusing to overwrite existing native evidence/artifact: {path}; "
                "use a fresh --output-root"
            )
    environment = {
        **os.environ, source_environment: str(derived),
        "TMPDIR": str(output), "RUSTUP_HOME": "/home/chentianyu/.rustup",
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands = []
    results = {
        "group": group, "status": "failed", "source_status": source_status,
        "positive_tests": 0, "negative_cases": [],
        "limits": (
            "Native observations and textual generic MIR are supplemental evidence, "
            "not an equivalence proof or completed API correctness proof. Pointer "
            "equality distinguishes non-ZST places only; ZST positions require the "
            "generic source/projection argument in issues/V-SLICE-PATTERN.md."
        ),
    }

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log),
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "RUSTUP_HOME": environment["RUSTUP_HOME"],
            "TMPDIR": environment["TMPDIR"],
            source_environment: str(derived), "returncode": None,
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record["returncode"] = result.returncode
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(
                f"{name}: expected exit 0, got {result.returncode}; see {log}"
            )
        return result

    try:
        text, spans, mappings = source_reader()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        (logs / "source-mappings.json").write_text(json.dumps(mappings, indent=2) + "\n")
        dependencies = {
            "authority": str(SOURCE),
            "proof_inputs": [
                mapping[proof_role]["path"] for mapping in mappings
            ],
            "unchanged_contracts": sorted({
                mapping[proof_role]["contract"] for mapping in mappings
            }),
            "contract_use": (
                "Only import paths and unchanged ensures clauses are checked here. "
                "Verus contracts/vstd are not compiled or assumed by these native tests."
            ),
            "native_operations": [
                "built-in slice patterns and shared usize indexing",
                "slice len (canonical lines 102-118 retained in source-spans.json)",
                "usize comparison and subtraction with overflow checks enabled",
                "core::option::Option and shared-reference construction",
            ],
            "behavior_input": str(behavior_input),
            "retained_inputs": [str(derived), str(harness)],
            "rust_toolchain": "rustc +1.96.0; RUSTC_BOOTSTRAP removed",
            "mir_use": "Textual evidence of generic branches/projections, not an equivalence proof.",
        }
        if splits:
            dependencies["native_operations"].append(
                "shared const split_at -> split_at_checked -> split_at_unchecked; "
                "canonical docs/bodies retained in source-spans.json"
            )
        (logs / "dependencies.json").write_text(json.dumps(dependencies, indent=2) + "\n")
        derived.write_text(text)
        harness.write_text(behavior_input.read_text())
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=link,mir={mir}", "-o", str(binary),
            ],
            "compile", success=True,
        )
        mir_text = mir.read_text()
        generic_functions = [
            f"{implementation}::{name}" for implementation in ("original", module)
            for name in apis
        ]
        if any(f"fn {name}(_1: &[T]) -> {return_type}" not in mir_text
               for name in generic_functions):
            raise AssertionError(f"Expected all four generic {test_label} functions in MIR: {mir}")
        results["mir"] = {
            "path": str(mir), "generic_functions": generic_functions,
            "overflow_checks": True, "source_inputs": [str(derived), str(harness)],
        }
        tested = run([str(binary), "--test-threads=1"], "behavior", success=True)
        summary = re.search(
            r"test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout,
        )
        if summary is None or int(summary[1]) != expected_tests:
            raise AssertionError(
                f"Expected all {expected_tests} executed {test_label} tests; "
                f"see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = int(summary[1])
        print(tested.stdout.strip())
        for name, text, expected in negatives:
            probe = output / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rlib"
            log = logs / f"{name}.log"
            source = (
                '#![allow(dead_code)]\n'
                f'include!(env!("{source_environment}"));\n' + text + "\n"
            )
            case = {
                "name": name, "source": source, "expected": expected,
                "log": str(log), "passed": False,
            }
            results["negative_cases"].append(case)
            try:
                probe.write_text(source)
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        f"--crate-name={'split' if splits else 'endpoint'}_rejection",
                        "--error-format=json",
                        str(probe), "-o", str(rejected),
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                probe.unlink(missing_ok=True)
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"{'ADOPTED split' if splits else 'ADOPTED endpoint'} checks: "
            f"{len(results['negative_cases'])} invalid "
            "receivers, arguments, returns, writes or lifetime escapes rejected; "
            "authority originals, actual current proofs and public methods compared."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        binary.unlink(missing_ok=True)


def check_mutable_endpoints(output_root):
    group = "mutable-endpoints"
    output_root = output_root.resolve()
    output = output_root / f"target/{group}/native"
    logs = output_root / f"logs/{group}/native"
    for directory in (output, logs):
        if not directory.resolve().is_relative_to(output_root):
            raise ValueError(f"Native output escapes --output-root through a symlink: {directory}")
    behavior_input = ROOT / "tests/mutable_endpoint_behavior.rs"
    derived = logs / "source_mutable_endpoints.rs"
    harness = logs / "mutable_endpoint_behavior.rs"
    metadata = logs / "mutable_endpoints.rmeta"
    mir = logs / "mutable_endpoints.mir"
    behavior_mir = logs / "mutable_endpoint_behavior.mir"
    binary = output / "mutable_endpoint_behavior"
    negatives = list(mutable_endpoint_negative_cases())
    evidence = [
        derived, harness, metadata, mir, behavior_mir, binary,
        *(logs / name for name in (
            "source-spans.json", "source-mappings.json", "dependencies.json",
            "commands.json", "results.json", "rustc-version.log",
            "compile-metadata-mir.log", "compile.log", "behavior.log",
        )),
    ]
    for name, _, _ in negatives:
        evidence.extend((
            logs / f"{name}.log", logs / f"rejection-{name}.rs",
            output / f"rejected-{name}.rmeta",
        ))
    for path in evidence:
        if path.exists() or path.is_symlink():
            raise FileExistsError(
                f"Refusing to overwrite existing native evidence/artifact: {path}; "
                "use a fresh --output-root"
            )
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    environment = {
        **os.environ, "SLICE_MUTABLE_ENDPOINTS_SOURCE": str(derived),
        "TMPDIR": str(output), "TMP": str(output), "TEMP": str(output),
        "RUSTUP_HOME": "/home/chentianyu/.rustup",
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands, temporaries = [], []
    results = {
        "group": group, "status": "failed", "positive_tests": 0, "negative_cases": [],
        "source_status": (
            "ADOPTED current first_mut/last_mut source-proof bodies; "
            "permission: issues/V-SLICE-PATTERN.md"
        ),
        "limits": (
            "Native tests, metadata and generic MIR are supplemental evidence, not "
            "an equivalence or API correctness proof. No source edits are performed. "
            "ZST positions are not inferred from addresses; their position argument "
            "depends on the generic source/projections, including at usize::MAX."
        ),
    }

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log), "returncode": None,
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "RUSTUP_HOME": environment["RUSTUP_HOME"],
            "PATH": environment.get("PATH"),
            "TMPDIR": environment["TMPDIR"], "TMP": environment["TMP"],
            "TEMP": environment["TEMP"],
            "SLICE_MUTABLE_ENDPOINTS_SOURCE": str(derived),
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record.update(
            returncode=result.returncode, stdout=result.stdout, stderr=result.stderr,
        )
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(
                f"{name}: expected exit 0, got {result.returncode}; see {log}"
            )
        return result

    try:
        if len(negatives) != 96 or len({name for name, _, _ in negatives}) != 96:
            raise AssertionError("Expected 96 distinct mutable endpoint compiler rejection targets")
        text, spans, mappings = mutable_endpoint_source()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        (logs / "source-mappings.json").write_text(json.dumps(mappings, indent=2) + "\n")
        dependencies = {
            "authority": str(SOURCE),
            "current_proof_inputs": [mapping["current"]["path"] for mapping in mappings],
            "unchanged_contracts": sorted({mapping["current"]["contract"] for mapping in mappings}),
            "contract_use": (
                "The pure predicates, imports and old/final postcondition bindings are "
                "pinned as read-only text. Verus/vstd are not compiled or assumed by "
                "the native tests."
            ),
            "native_operations": [
                "built-in slice patterns and mutable usize indexing",
                "slice len (canonical lines 102-118 retained in source-spans.json)",
                "usize comparison and subtraction with overflow checks enabled",
                "core::option::Option and exclusive reborrowing",
            ],
            "behavior_input": str(behavior_input),
            "retained_inputs": [str(derived), str(harness)],
            "rust_toolchain": "rustc +1.96.0; RUSTC_BOOTSTRAP removed",
            "mir_use": "Generic branch/projection evidence, not an equivalence proof.",
        }
        (logs / "dependencies.json").write_text(json.dumps(dependencies, indent=2) + "\n")
        derived.write_text(text)
        harness.write_text(behavior_input.read_text())
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=mutable_endpoints", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ],
            "compile-metadata-mir", success=True,
        )
        if not metadata.is_file() or metadata.stat().st_size == 0:
            raise AssertionError(f"Expected retained native metadata: {metadata}")
        generic_functions = [
            f"{implementation}::{name}" for implementation in ("original", "adopted")
            for name in ("first_mut", "last_mut")
        ]
        mir_text = mir.read_text()
        if any(
            f"fn {name}(_1: &mut [T]) -> Option<&mut T>" not in mir_text
            for name in generic_functions
        ):
            raise AssertionError(f"Expected all four generic mutable endpoint functions in MIR: {mir}")
        results["metadata"] = {"path": str(metadata), "generic_functions": generic_functions}
        results["mir"] = {
            "path": str(mir), "generic_functions": generic_functions,
            "overflow_checks": True, "source_inputs": [str(derived), str(harness)],
        }
        temporaries.append(binary)
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "--error-format=json", "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=link,mir={behavior_mir}", "-o", str(binary),
            ],
            "compile", success=True,
        )
        if not binary.is_file():
            raise AssertionError(f"Expected linked mutable endpoint test executable: {binary}")
        if not behavior_mir.is_file() or behavior_mir.stat().st_size == 0:
            raise AssertionError(f"Expected retained behavior MIR: {behavior_mir}")
        results["mir"]["behavior_path"] = str(behavior_mir)
        tested = run(
            [str(binary), "--test-threads=1", "--color=never"], "behavior", success=True,
        )
        expected_tests = 17
        summaries = re.findall(
            r"^test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout, re.MULTILINE,
        )
        if (
            summaries != [str(expected_tests)]
            or f"running {expected_tests} tests" not in tested.stdout.splitlines()
        ):
            raise AssertionError(
                f"Expected all {expected_tests} executed mutable endpoint tests; "
                f"see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = expected_tests
        print(tested.stdout.strip())
        for name, text, expected in negatives:
            probe = logs / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rmeta"
            log = logs / f"{name}.log"
            source = (
                '#![allow(dead_code)]\n'
                'include!(env!("SLICE_MUTABLE_ENDPOINTS_SOURCE"));\n' + text + "\n"
            )
            case = {
                "name": name, "source": source, "input": str(probe), "expected": expected,
                "log": str(log), "passed": False,
            }
            results["negative_cases"].append(case)
            probe.write_text(source)
            temporaries.append(rejected)
            try:
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        "--crate-name=mutable_endpoint_rejection", "--error-format=json",
                        str(probe), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                        f"--emit=metadata={rejected}",
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"Adopted mutable endpoints: {expected_tests} runtime tests and "
            f"{len(negatives)} exact compiler rejections passed."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        for path in temporaries:
            path.unlink(missing_ok=True)


def check_mutable_splits(output_root):
    group = "mutable-splits"
    output_root = output_root.resolve()
    output = output_root / f"target/{group}/native"
    logs = output_root / f"logs/{group}/native"
    for directory in (output, logs):
        if not directory.resolve().is_relative_to(output_root):
            raise ValueError(f"Native output escapes --output-root through a symlink: {directory}")
    behavior_input = ROOT / "tests/mutable_split_behavior.rs"
    derived = logs / "source_mutable_splits.rs"
    harness = logs / "mutable_split_behavior.rs"
    metadata = logs / "mutable_splits.rmeta"
    mir = logs / "mutable_splits.mir"
    behavior_mir = logs / "mutable_split_behavior.mir"
    binary = output / "mutable_split_behavior"
    negatives = list(mutable_split_negative_cases())
    evidence = [
        derived, harness, metadata, mir, behavior_mir, binary,
        *(logs / name for name in (
            "source-spans.json", "source-mappings.json", "dependencies.json",
            "commands.json", "results.json", "rustc-version.log",
            "compile-metadata-mir.log", "compile.log", "behavior.log",
        )),
    ]
    for name, _, _ in negatives:
        evidence.extend((
            logs / f"{name}.log", logs / f"rejection-{name}.rs",
            output / f"rejected-{name}.rmeta",
        ))
    for path in evidence:
        if path.exists() or path.is_symlink():
            raise FileExistsError(
                f"Refusing to overwrite existing native evidence/artifact: {path}; "
                "use a fresh --output-root"
            )
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    environment = {
        **os.environ, "SLICE_MUTABLE_SPLITS_SOURCE": str(derived),
        "TMPDIR": str(output), "TMP": str(output), "TEMP": str(output),
        "RUSTUP_HOME": "/home/chentianyu/.rustup",
        "PATH": str(ROOT / "toolchain/review-native/bin") + os.pathsep + os.environ.get("PATH", ""),
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands, temporaries = [], []
    results = {
        "group": group, "status": "failed", "positive_tests": 0, "negative_cases": [],
        "source_status": (
            "ADOPTED current split_first_mut/split_last_mut source proofs; "
            "exact permission: issues/V-SLICE-PATTERN.md"
        ),
        "limits": (
            "Native tests, metadata and generic/runtime/const MIR are supplemental "
            "evidence, not a source equivalence or API correctness proof. Neither "
            "current source proofs nor historical proposals are edited. ZST position/provenance "
            "cannot be established from address equality, including at usize::MAX."
        ),
    }

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log), "returncode": None,
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "RUSTUP_HOME": environment["RUSTUP_HOME"], "PATH": environment["PATH"],
            "TMPDIR": environment["TMPDIR"], "TMP": environment["TMP"],
            "TEMP": environment["TEMP"], "SLICE_MUTABLE_SPLITS_SOURCE": str(derived),
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record.update(
            returncode=result.returncode, stdout=result.stdout, stderr=result.stderr,
        )
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(
                f"{name}: expected exit 0, got {result.returncode}; see {log}"
            )
        return result

    try:
        if len(negatives) != 216 or len({name for name, _, _ in negatives}) != 216:
            raise AssertionError("Expected 216 distinct mutable split compiler rejection targets")
        text, spans, mappings = mutable_split_source()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        (logs / "source-mappings.json").write_text(json.dumps(mappings, indent=2) + "\n")
        dependencies = {
            "authority": str(SOURCE),
            "current_proof_inputs": [mapping["current"]["path"] for mapping in mappings],
            "unchanged_contracts": sorted({mapping["current"]["contract"] for mapping in mappings}),
            "contract_use": (
                "Exact pure candidates and old/final element/full-remainder/owner "
                "bindings are read-only extraction gates, not compiled assumptions. "
                "Source proofs import only mutable_splits_post.rs, never the public "
                "mutable_splits.rs binding. The selected vstd already binds "
                "split_first_mut; it is not registered again here."
            ),
            "native_dependencies": [span for span in spans if span["role"] == "native-dependency"],
            "vstd_contracts": [span for span in spans if span["role"] == "vstd-contract"],
            "vstd_use": (
                "View, length, mutable index/writeback, borrow-length, split_at_mut "
                "and the existing split_first_mut contracts are recorded, not "
                "compiled or assumed. Rust's checked/unchecked split and raw "
                "pointer delegates execute through the real standard library."
            ),
            "native_operations": [
                "original built-in mutable slice patterns",
                "adopted split_at_mut plus mutable usize indexing",
                "slice len, usize comparison/subtraction with overflow checks",
                "core::option::Option and exclusive disjoint reborrowing",
                "real public split_first_mut/split_last_mut with exact HRTB types",
            ],
            "behavior_input": str(behavior_input),
            "retained_inputs": [str(derived), str(harness)],
            "rejection_inputs": "Retained in logs/ as evidence; transient compiler outputs are removed.",
            "rust_toolchain": "rustc +1.96.0; RUSTC_BOOTSTRAP removed",
            "linker": str(ROOT / "toolchain/review-native/bin/cc"),
            "mir_use": "Generic and runtime/const evidence, not an equivalence proof.",
        }
        (logs / "dependencies.json").write_text(json.dumps(dependencies, indent=2) + "\n")
        derived.write_text(text)
        harness.write_text(behavior_input.read_text())
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=mutable_splits", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ],
            "compile-metadata-mir", success=True,
        )
        if not metadata.is_file() or metadata.stat().st_size == 0:
            raise AssertionError(f"Expected retained native metadata: {metadata}")
        generic_functions = [
            f"{implementation}::{name}" for implementation in ("original", "adopted")
            for name in ("split_first_mut", "split_last_mut")
        ]
        mir_text = mir.read_text()
        if any(
            f"fn {name}(_1: &mut [T]) -> Option<(&mut T, &mut [T])>" not in mir_text
            for name in generic_functions
        ):
            raise AssertionError(f"Expected all four generic mutable split functions in MIR: {mir}")
        results["metadata"] = {"path": str(metadata), "generic_functions": generic_functions}
        results["mir"] = {
            "path": str(mir), "generic_functions": generic_functions,
            "overflow_checks": True, "source_inputs": [str(derived), str(harness)],
        }
        temporaries.append(binary)
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "--error-format=json", "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=link,mir={behavior_mir}", "-o", str(binary),
            ],
            "compile", success=True,
        )
        if not binary.is_file():
            raise AssertionError(f"Expected linked mutable split test executable: {binary}")
        if not behavior_mir.is_file() or behavior_mir.stat().st_size == 0:
            raise AssertionError(f"Expected retained behavior MIR: {behavior_mir}")
        results["mir"]["behavior_path"] = str(behavior_mir)
        tested = run(
            [str(binary), "--test-threads=1", "--color=never"], "behavior", success=True,
        )
        expected_tests = 19
        summaries = re.findall(
            r"^test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout, re.MULTILINE,
        )
        if (
            summaries != [str(expected_tests)]
            or f"running {expected_tests} tests" not in tested.stdout.splitlines()
        ):
            raise AssertionError(
                f"Expected all {expected_tests} executed mutable split tests; see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = expected_tests
        print(tested.stdout.strip())
        for name, text, expected in negatives:
            probe = logs / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rmeta"
            log = logs / f"{name}.log"
            source = (
                '#![allow(dead_code)]\n'
                'include!(env!("SLICE_MUTABLE_SPLITS_SOURCE"));\n' + text + "\n"
            )
            case = {
                "name": name, "source": source, "input": str(probe), "expected": expected,
                "log": str(log), "passed": False,
            }
            results["negative_cases"].append(case)
            probe.write_text(source)
            temporaries.append(rejected)
            try:
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        "--crate-name=mutable_split_rejection", "--error-format=json",
                        str(probe), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                        f"--emit=metadata={rejected}",
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"Adopted mutable splits: {expected_tests} runtime tests and "
            f"{len(negatives)} exact compiler rejections passed."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        for path in temporaries:
            path.unlink(missing_ok=True)


def check_split_off_endpoints(output_root):
    group = "split-off-endpoints"
    output_root = output_root.resolve()
    output = output_root / f"target/{group}/native"
    logs = output_root / f"logs/{group}/native"
    for directory in (output, logs):
        if not directory.resolve().is_relative_to(output_root):
            raise ValueError(f"Native output escapes --output-root through a symlink: {directory}")
    behavior_input = ROOT / "tests/split_off_endpoint_behavior.rs"
    derived = logs / "source_split_off_endpoints.rs"
    harness = logs / "split_off_endpoint_behavior.rs"
    metadata = logs / "split_off_endpoints.rmeta"
    mir = logs / "split_off_endpoints.mir"
    behavior_mir = logs / "split_off_endpoint_behavior.mir"
    binary = output / "split_off_endpoint_behavior"
    linker = ROOT / "toolchain/review-native/bin/cc"
    negatives = list(split_off_endpoint_negative_cases())
    evidence = [
        derived, harness, metadata, mir, behavior_mir, binary,
        *(logs / name for name in (
            "source-spans.json", "source-mappings.json", "dependencies.json",
            "commands.json", "results.json", "rustc-version.log",
            "compile-metadata-mir.log", "compile.log", "behavior.log",
        )),
    ]
    for name, _, _ in negatives:
        evidence.extend((
            logs / f"{name}.log", logs / f"rejection-{name}.rs",
            output / f"rejected-{name}.rmeta",
        ))
    for path in evidence:
        if path.exists() or path.is_symlink():
            raise FileExistsError(
                f"Refusing to overwrite existing native evidence/artifact: {path}; "
                "use a fresh --output-root"
            )
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    environment = {
        **os.environ, "SLICE_SPLIT_OFF_ENDPOINTS_SOURCE": str(derived),
        "TMPDIR": str(output), "TMP": str(output), "TEMP": str(output),
        "RUSTUP_HOME": "/home/chentianyu/.rustup",
        "PATH": str(linker.parent) + os.pathsep + os.environ.get("PATH", ""),
    }
    environment.pop("RUSTC_BOOTSTRAP", None)
    commands, temporaries = [], []
    results = {
        "group": group, "status": "failed", "positive_tests": 0, "negative_cases": [],
        "source_status": (
            "ADOPTED current formal sources: first remains unchanged; only last's "
            "split_last call and local dependency import changed under independent permission."
        ),
        "formal_verification": "Not run. Native acceptance does not establish Verus support.",
        "limits": (
            "Native tests, metadata and MIR are supplemental evidence, not a source "
            "equivalence or API correctness proof or formal-verification result. "
            "Runtime calls are stable since 1.87.0, but real public const calls require "
            "const_split_off_first_last and must fail here. ZST position/provenance "
            "cannot be established from address equality."
        ),
    }

    def run(command, name, *, success=False):
        log = logs / f"{name}.log"
        record = {
            "command": command, "cwd": str(ROOT), "log": str(log), "returncode": None,
            "RUSTC_BOOTSTRAP": environment.get("RUSTC_BOOTSTRAP"),
            "RUSTUP_HOME": environment["RUSTUP_HOME"], "PATH": environment["PATH"],
            "TMPDIR": environment["TMPDIR"], "TMP": environment["TMP"],
            "TEMP": environment["TEMP"], "SLICE_SPLIT_OFF_ENDPOINTS_SOURCE": str(derived),
        }
        commands.append(record)
        try:
            result = subprocess.run(
                command, cwd=ROOT, env=environment, text=True, capture_output=True,
            )
        except OSError as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log.write_text(record["error"] + "\n")
            raise
        record.update(returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
        log.write_text(result.stdout + result.stderr)
        if success and result.returncode != 0:
            raise AssertionError(f"{name}: expected exit 0, got {result.returncode}; see {log}")
        return result

    try:
        if len(negatives) != 110 or len({name for name, _, _ in negatives}) != 110:
            raise AssertionError("Expected 110 distinct split-off endpoint compiler rejection targets")
        text, spans, mappings = split_off_endpoint_source()
        (logs / "source-spans.json").write_text(json.dumps(spans, indent=2) + "\n")
        (logs / "source-mappings.json").write_text(json.dumps(mappings, indent=2) + "\n")
        dependencies = {
            "authority": str(SOURCE),
            "current_proof_inputs": [mapping["current"]["path"] for mapping in mappings],
            "current_dependency_input": mappings[1]["current"]["dependency"]["path"],
            "authorization": (
                "issues/V-ASCII-CALL-BINDING.md"
                "#independent-split-off-permission-before-adoption"
            ),
            "unchanged_contracts": [
                span["path"] for span in spans if span["role"] == "contract"
            ],
            "contract_use": (
                "Exact pure predicates and separate public declarations are read-only "
                "extraction gates, not compiled assumptions. Both formal sources "
                "import split_off_post.rs, never the public "
                "split_off.rs binding. Only exact ghost ensures and Verus wrappers/"
                "named returns/imports are erased; no executable proof-body rewriting."
            ),
            "native_dependencies": [span for span in spans if span["role"] == "native-dependency"],
            "native_operations": [
                "original: shared split_first/split_last, then slot assignment",
                "adopted first: unchanged shared split_first call, then slot assignment",
                "adopted last only: actual local split_last, then unchanged slot assignment",
                "local split_last: length check, usize subtraction/index and split_at",
                "real public shared split_off_first/split_off_last; no mutable endpoints",
                "for<'a, 'b> fn(&'b mut &'a [T]) -> Option<&'a T>, with unconstrained T",
            ],
            "behavior_input": str(behavior_input),
            "retained_inputs": [str(derived), str(harness)],
            "rejection_inputs": "Retained in logs/; only named transient compiler outputs are removed.",
            "rust_toolchain": "rustc +1.96.0; RUSTC_BOOTSTRAP removed",
            "linker": str(linker),
            "mir_use": (
                "Generic and runtime evidence, not an equivalence proof. Local const bodies "
                "do not establish stable const availability of the real public APIs."
            ),
        }
        (logs / "dependencies.json").write_text(json.dumps(dependencies, indent=2) + "\n")
        derived.write_text(text)
        harness.write_text(behavior_input.read_text())
        version = run(["rustc", "+1.96.0", "-vV"], "rustc-version", success=True)
        if "release: 1.96.0" not in version.stdout.splitlines():
            raise AssertionError(f"Expected Rust 1.96.0; see {logs / 'rustc-version.log'}")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--crate-name=split_off_endpoints", "--error-format=json",
                str(derived), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                f"--emit=metadata={metadata},mir={mir}",
            ],
            "compile-metadata-mir", success=True,
        )
        if not metadata.is_file() or metadata.stat().st_size == 0:
            raise AssertionError(f"Expected retained native metadata: {metadata}")
        signatures = {
            f"{module}::{name}": "(_1: &mut &[T]) -> Option<&T>"
            for module, names in (
                ("original", ("split_off_first", "split_off_last")),
                ("adopted", ("split_off_first", "split_off_last")),
            )
            for name in names
        }
        # Rust 1.96 prints this unique dependency without its module path.
        signatures["split_last"] = "(_1: &[T]) -> Option<(&T, &[T])>"
        mir_text = mir.read_text()
        if any(f"fn {name}{signature}" not in mir_text for name, signature in signatures.items()):
            raise AssertionError(f"Expected all five generic split-off/dependency functions in MIR: {mir}")
        results["metadata"] = {"path": str(metadata), "generic_functions": list(signatures)}
        results["mir"] = {
            "path": str(mir), "generic_functions": list(signatures),
            "overflow_checks": True, "source_inputs": [str(derived), str(harness)],
        }
        temporaries.append(binary)
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test", str(harness),
                "--error-format=json", "-C", "overflow-checks=yes", "-C", "opt-level=0",
                "-C", f"linker={linker}",
                f"--emit=link,mir={behavior_mir}", "-o", str(binary),
            ],
            "compile", success=True,
        )
        if not binary.is_file() or binary.stat().st_size == 0:
            raise AssertionError(f"Expected linked split-off endpoint test executable: {binary}")
        if not behavior_mir.is_file() or behavior_mir.stat().st_size == 0:
            raise AssertionError(f"Expected retained behavior MIR: {behavior_mir}")
        results["mir"]["behavior_path"] = str(behavior_mir)
        tested = run(
            [str(binary), "--test-threads=1", "--color=never"], "behavior", success=True,
        )
        expected_tests = 20
        summaries = re.findall(
            r"^test result: ok\. (\d+) passed; 0 failed; 0 ignored; "
            r"0 measured; 0 filtered out;",
            tested.stdout, re.MULTILINE,
        )
        if (
            summaries != [str(expected_tests)]
            or f"running {expected_tests} tests" not in tested.stdout.splitlines()
        ):
            raise AssertionError(
                f"Expected all {expected_tests} executed split-off endpoint tests; "
                f"see {logs / 'behavior.log'}"
            )
        results["positive_tests"] = expected_tests
        print(tested.stdout.strip())
        for name, text, expected in negatives:
            probe = logs / f"rejection-{name}.rs"
            rejected = output / f"rejected-{name}.rmeta"
            log = logs / f"{name}.log"
            source = (
                '#![allow(dead_code)]\n'
                'include!(env!("SLICE_SPLIT_OFF_ENDPOINTS_SOURCE"));\n' + text + "\n"
            )
            case = {
                "name": name, "source": source, "input": str(probe), "expected": expected,
                "log": str(log), "passed": False,
            }
            results["negative_cases"].append(case)
            probe.write_text(source)
            temporaries.append(rejected)
            try:
                failed = run(
                    [
                        "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                        "--crate-name=split_off_endpoint_rejection", "--error-format=json",
                        str(probe), "-C", "overflow-checks=yes", "-C", "opt-level=0",
                        f"--emit=metadata={rejected}",
                    ],
                    name,
                )
                case["returncode"] = failed.returncode
                case["diagnostic"] = check_singleton_rejection(failed, expected, log)
                case["passed"] = True
            finally:
                rejected.unlink(missing_ok=True)
        results["status"] = "passed"
        print(
            f"Adopted split-off endpoints: {expected_tests} runtime tests and "
            f"{len(negatives)} exact compiler rejections passed; not a Verus result."
        )
    except Exception as error:
        results["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        (logs / "results.json").write_text(json.dumps(results, indent=2) + "\n")
        for path in temporaries:
            path.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root", type=Path, default=ROOT, metavar="DIR",
        help="Write target/ and logs/ beneath DIR instead of the project root.",
    )
    parser.add_argument(
        "--group", choices=(
            "defaults", "singleton", "ascii-case", "endpoints", "splits",
            "mutable-endpoints", "mutable-splits", "split-off-endpoints",
        ), default="defaults", metavar="GROUP",
        help=(
            "Run the original observers/Defaults checks (default), singletons, ASCII "
            "case conversions, or ADOPTED current first/last, split, or mutable "
            "endpoint, mutable split, or shared split-off endpoint comparisons."
        ),
    )
    args = parser.parse_args(argv)
    output_root = args.output_root.resolve()
    if args.group == "singleton":
        return check_singletons(output_root)
    if args.group == "ascii-case":
        return check_ascii_case(output_root)
    if args.group == "endpoints":
        return check_endpoints(output_root)
    if args.group == "splits":
        return check_pattern_comparison(output_root, splits=True)
    if args.group == "mutable-endpoints":
        return check_mutable_endpoints(output_root)
    if args.group == "mutable-splits":
        return check_mutable_splits(output_root)
    if args.group == "split-off-endpoints":
        return check_split_off_endpoints(output_root)
    output = output_root / "target/defaults/native"
    logs = output_root / "logs/defaults/native"
    output.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    lines = SOURCE.read_text().splitlines()
    copies = ["use core::ptr;\n"]
    for name, (start, end) in FUNCTIONS.items():
        text = "\n".join(line[4:] for line in lines[start - 1 : end])
        expected = f"pub const fn {name}(&self)"
        if not text.startswith(expected) or not text.endswith("\n}"):
            raise ValueError(f"Source span changed: {name} at {SOURCE}:{start}-{end}")
        text = text.replace(f"fn {name}(&self)", f"fn {name}<T>(slice: &[T])", 1)
        text = re.sub(r"\bself\b", "slice", text)
        copies.append(f"// {SOURCE}:{start}-{end}\n{text}\n")
    defaults = []
    for name, (start, end, result) in DEFAULTS.items():
        text = "\n".join(line[4:] for line in lines[start - 1 : end])
        expected = "fn default() -> Self"
        if not text.startswith(expected + " {") or not text.endswith("\n}"):
            raise ValueError(f"Source span changed: {name} at {SOURCE}:{start}-{end}")
        text = text.replace(expected, f"pub fn {name}<'a, T>() -> {result}", 1)
        defaults.append(f"// {SOURCE}:{start}-{end}\n{text}\n")
    derived = output / "source_observers.rs"
    derived_defaults = output / "source_defaults.rs"
    binary = output / "readonly_behavior"
    defaults_binary = output / "default_behavior"
    rejected = output / "rejected.rlib"
    probe = output / "default_rejection.rs"
    stable_environment = {
        **os.environ,
        "SLICE_NATIVE_SOURCE": str(derived),
        "SLICE_DEFAULT_SOURCE": str(derived_defaults),
    }
    stable_environment.pop("RUSTC_BOOTSTRAP", None)
    environment = {**stable_environment, "RUSTC_BOOTSTRAP": "1"}
    commands = []

    def run(command, name, env=environment):
        commands.append({
            "command": command,
            "RUSTC_BOOTSTRAP": env.get("RUSTC_BOOTSTRAP"),
        })
        result = subprocess.run(
            command, cwd=ROOT, env=env, text=True, capture_output=True
        )
        (logs / f"{name}.log").write_text(result.stdout + result.stderr)
        return result

    try:
        derived.write_text("\n".join(copies))
        derived_defaults.write_text("\n".join(defaults))
        run(["rustc", "+1.96.0", "-vV"], "rustc-version").check_returncode()
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/readonly_behavior.rs", "-o", str(binary),
            ],
            "compile",
        ).check_returncode()
        tested = run([str(binary), "--test-threads=1"], "behavior")
        tested.check_returncode()
        failed = run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                "--error-format=json", "tests/readonly_lifetime_rejection.rs",
                "-o", str(rejected),
            ],
            "lifetimes",
        )
        diagnostics = [
            json.loads(line) for line in failed.stderr.splitlines()
            if line.startswith("{")
        ]
        errors = [
            item for item in diagnostics
            if item.get("level") == "error" and item.get("code")
        ]
        if failed.returncode == 0 or len(errors) != 4 or any(
            item["code"]["code"] != "E0515" for item in errors
        ):
            raise AssertionError("Expected exactly four borrow-escape errors E0515")
        print(tested.stdout.strip())
        print("Lifetime checks: four invalid escapes rejected with E0515.")
        run(
            [
                "rustc", "+1.96.0", "--edition=2021", "--test",
                "tests/default_behavior.rs", "-o", str(defaults_binary),
            ],
            "defaults-compile", stable_environment,
        ).check_returncode()
        default_tested = run(
            [str(defaults_binary), "--test-threads=1"],
            "defaults-behavior", stable_environment,
        )
        default_tested.check_returncode()
        print(default_tested.stdout.strip())
        negative_cases = {
            "shared-arguments": (
                "fn bad() { let _ = <&[u8] as core::default::Default>::default(1); }",
                "E0061",
            ),
            "mutable-arguments": (
                "fn bad() { let _ = <&mut [u8] as core::default::Default>::default(1); }",
                "E0061",
            ),
            "shared-result": (
                "fn bad() { let _: usize = <&[u8] as core::default::Default>::default(); }",
                "E0308",
            ),
            "mutable-result": (
                "fn bad() { let _: usize = <&mut [u8] as core::default::Default>::default(); }",
                "E0308",
            ),
            "shared-mutability": (
                "fn bad() { let _: &mut [u8] = <&[u8] as core::default::Default>::default(); }",
                "E0308",
            ),
            "mutable-function-result": (
                "fn bad() { let _: fn() -> &'static [u8] = "
                "<&'static mut [u8] as core::default::Default>::default; }",
                "E0308",
            ),
            "shared-const-unstable": (
                "const BAD: &[u8] = <&[u8] as core::default::Default>::default();",
                "E0658",
            ),
            "mutable-const-unstable": (
                "const BAD: &mut [u8] = <&mut [u8] as core::default::Default>::default();",
                "E0658",
            ),
        }
        for name, (text, expected_code) in negative_cases.items():
            probe.write_text(text + "\n")
            failed = run(
                [
                    "rustc", "+1.96.0", "--edition=2021", "--crate-type=lib",
                    "--error-format=json", str(probe), "-o", str(rejected),
                ],
                f"defaults-{name}", stable_environment,
            )
            diagnostics = [
                json.loads(line) for line in failed.stderr.splitlines()
                if line.startswith("{")
            ]
            codes = [
                item["code"]["code"] for item in diagnostics
                if item.get("level") == "error" and item.get("code")
            ]
            if failed.returncode == 0 or codes != [expected_code]:
                raise AssertionError(
                    f"{name}: expected one {expected_code} error, got {codes}; "
                    f"see {logs / f'defaults-{name}.log'}"
                )
        print("Default checks: eight invalid signatures or const calls rejected.")
    finally:
        (logs / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        for temporary in (
            derived, derived_defaults, binary, defaults_binary, probe, rejected,
        ):
            temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
