#!/usr/bin/env python3
"""Materialize conservative source-surrogate fidelity verdicts."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


# Kept as historical audit data. The current verdict is derived from the
# exhaustive per-record surrogate audit instead of this earlier manual list.
LEGACY_DOWNGRADE = {
    # net
    "std_specs__net.rs__L213__Ipv4Addr__from_octets",
    "std_specs__net.rs__L218__Ipv4Addr__octets",
    "std_specs__net.rs__L268__Ipv6Addr__from_octets",
    "std_specs__net.rs__L273__Ipv6Addr__octets",
    # duration + location
    "std_specs__duration.rs__L152__Duration__new",
    "std_specs__duration.rs__L159__Duration__from_secs",
    "std_specs__duration.rs__L164__Duration__from_millis",
    "std_specs__duration.rs__L169__Duration__from_micros",
    "std_specs__duration.rs__L174__Duration__from_nanos",
    "std_specs__duration.rs__L179__Duration__from_nanos_u128",
    "std_specs__duration.rs__L186__Duration__from_hours",
    "std_specs__duration.rs__L193__Duration__from_mins",
    "std_specs__duration.rs__L200__Duration__is_zero",
    "std_specs__duration.rs__L210__Duration__as_secs_f32",
    "std_specs__duration.rs__L215__Duration__as_secs_f64",
    "std_specs__duration.rs__L220__Duration__subsec_millis",
    "std_specs__duration.rs__L225__Duration__subsec_micros",
    "std_specs__duration.rs__L235__Duration__as_millis",
    "std_specs__duration.rs__L240__Duration__as_micros",
    "std_specs__duration.rs__L245__Duration__as_nanos",
    "std_specs__duration.rs__L250__Duration__abs_diff",
    "std_specs__duration.rs__L259__Duration__checked_add",
    "std_specs__duration.rs__L268__Duration__saturating_add",
    "std_specs__duration.rs__L278__Duration__checked_sub",
    "std_specs__duration.rs__L286__Duration__saturating_sub",
    "std_specs__duration.rs__L296__Duration__checked_mul",
    "std_specs__duration.rs__L305__Duration__saturating_mul",
    "std_specs__duration.rs__L314__Duration__checked_div",
    "std_specs__duration.rs__L322__Duration__mul_f64",
    "std_specs__duration.rs__L329__Duration__mul_f32",
    "std_specs__duration.rs__L336__Duration__div_f64",
    "std_specs__duration.rs__L343__Duration__div_f32",
    "std_specs__duration.rs__L350__Duration__from_secs_f32",
    "std_specs__duration.rs__L357__Duration__from_secs_f64",
    "std_specs__duration.rs__L364__Duration__try_from_secs_f32",
    "std_specs__duration.rs__L379__Duration__try_from_secs_f64",
    "std_specs__duration.rs__L394__Duration__div_duration_f32",
    "std_specs__duration.rs__L403__Duration__div_duration_f64",
    "std_specs__location.rs__L26__Location__file",
    # vecdeque / btree / capacity
    "std_specs__vecdeque.rs__L80__VecDeque__T__A__len",
    "std_specs__vecdeque.rs__L86__VecDeque__T__new",
    "std_specs__vecdeque.rs__L98__VecDeque__T__with_capacity",
    "std_specs__vecdeque.rs__L103__VecDeque__T__A__reserve",
    "std_specs__vecdeque.rs__L111__VecDeque__T__A__reserve_exact",
    "std_specs__vecdeque.rs__L119__VecDeque__T__A__try_reserve_exact",
    "std_specs__vecdeque.rs__L127__VecDeque__T__A__push_back",
    "std_specs__vecdeque.rs__L135__VecDeque__T__A__push_front",
    "std_specs__vecdeque.rs__L143__VecDeque__T__A__pop_back",
    "std_specs__vecdeque.rs__L160__VecDeque__T__A__pop_front",
    "std_specs__vecdeque.rs__L237__VecDeque__T__A__get",
    "std_specs__vecdeque.rs__L263__VecDeque__T__A__rotate_left",
    "std_specs__vecdeque.rs__L276__VecDeque__T__A__rotate_right",
    "std_specs__vecdeque.rs__L288__VecDeque__T__A__swap",
    "std_specs__vecdeque.rs__L303__VecDeque__T__A__append",
    "std_specs__vecdeque.rs__L312__VecDeque__T__A__insert",
    "std_specs__vecdeque.rs__L323__VecDeque__T__A__remove",
    "std_specs__vecdeque.rs__L341__VecDeque__T__A__clear",
    "std_specs__vecdeque.rs__L346__VecDeque__T__A__split_off",
    "std_specs__vecdeque.rs__L374__VecDeque__T__A__truncate",
    "std_specs__btree.rs__L461__BTreeMap__Key__Value__A__contains_key__Q",
    "std_specs__btree.rs__L562__BTreeMap__Key__Value__A__remove__Q",
    "std_specs__btree.rs__L567__BTreeMap__Key__Value__A__remove__Q",
    "std_specs__capacity.rs__L42__Vec__T__A__reserve_exact",
    "std_specs__capacity.rs__L60__Vec__T__A__shrink_to_fit",
    "std_specs__capacity.rs__L82__String__with_capacity",
    "std_specs__capacity.rs__L94__String__reserve_exact",
    "std_specs__capacity.rs__L114__String__shrink_to_fit",
    "std_specs__capacity.rs__L168__BinaryHeap__T__with_capacity",
    "std_specs__capacity.rs__L175__BinaryHeap__T__A__reserve",
    "std_specs__capacity.rs__L184__BinaryHeap__T__A__reserve_exact",
    "std_specs__capacity.rs__L211__BinaryHeap__T__A__shrink_to_fit",
    # cmp / ops / bits
    "std_specs__cmp.rs__L252__bool__as__PartialEq__bool__ne",
    "std_specs__cmp.rs__L279__f32__as__PartialEq__f32__eq",
    "std_specs__cmp.rs__L285__f32__as__PartialEq__f32__ne",
    "std_specs__cmp.rs__L290__f32__as__PartialOrd__f32__partial_cmp",
    "std_specs__cmp.rs__L295__f32__as__PartialOrd__f32__lt",
    "std_specs__cmp.rs__L300__f32__as__PartialOrd__f32__le",
    "std_specs__cmp.rs__L305__f32__as__PartialOrd__f32__gt",
    "std_specs__cmp.rs__L310__f32__as__PartialOrd__f32__ge",
    "std_specs__cmp.rs__L316__f64__as__PartialEq__f64__eq",
    "std_specs__cmp.rs__L322__f64__as__PartialEq__f64__ne",
    "std_specs__cmp.rs__L327__f64__as__PartialOrd__f64__partial_cmp",
    "std_specs__cmp.rs__L332__f64__as__PartialOrd__f64__lt",
    "std_specs__cmp.rs__L337__f64__as__PartialOrd__f64__le",
    "std_specs__cmp.rs__L342__f64__as__PartialOrd__f64__gt",
    "std_specs__cmp.rs__L347__f64__as__PartialOrd__f64__ge",
    "std_specs__cmp.rs__L375__a__A__as__PartialEq__B__ne",
    "std_specs__cmp.rs__L404__a__A__as__PartialOrd__B__lt",
    "std_specs__cmp.rs__L412__a__A__as__PartialOrd__B__le",
    "std_specs__cmp.rs__L420__a__A__as__PartialOrd__B__gt",
    "std_specs__cmp.rs__L428__a__A__as__PartialOrd__B__ge",
    "std_specs__ops.rs__L464__f32__as__core__ops__Neg__neg",
    "std_specs__ops.rs__L469__f32__as__core__ops__Add__add",
    "std_specs__ops.rs__L474__f32__as__core__ops__Sub__sub",
    "std_specs__ops.rs__L479__f32__as__core__ops__Mul__mul",
    "std_specs__ops.rs__L484__f32__as__core__ops__Div__div",
    "std_specs__ops.rs__L489__f64__as__core__ops__Neg__neg",
    "std_specs__ops.rs__L494__f64__as__core__ops__Add__add",
    "std_specs__ops.rs__L499__f64__as__core__ops__Sub__sub",
    "std_specs__ops.rs__L504__f64__as__core__ops__Mul__mul",
    "std_specs__ops.rs__L509__f64__as__core__ops__Div__div",
    "std_specs__bits.rs__L48__u8__trailing_zeros",
    "std_specs__bits.rs__L60__u8__leading_zeros",
    "std_specs__bits.rs__L218__u16__trailing_zeros",
    "std_specs__bits.rs__L230__u16__leading_zeros",
    "std_specs__bits.rs__L394__u32__trailing_zeros",
    "std_specs__bits.rs__L406__u32__leading_zeros",
    "std_specs__bits.rs__L571__u64__trailing_zeros",
    "std_specs__bits.rs__L583__u64__leading_zeros",
    # vec / smart pointers / MaybeUninit
    "std_specs__vec.rs__L93__Vec__T__A__len",
    "std_specs__vec.rs__L110__Vec__T__A__new_in",
    "std_specs__vec.rs__L115__Vec__T__with_capacity",
    "std_specs__vec.rs__L120__Vec__T__A__with_capacity_in",
    "std_specs__vec.rs__L125__Vec__T__A__reserve",
    "std_specs__vec.rs__L154__Vec__T__A__append",
    "std_specs__vec.rs__L184__Vec__T__A__index",
    "std_specs__vec.rs__L192__Vec__T__A__swap_remove",
    "std_specs__vec.rs__L236__Vec__T__A__as_slice",
    "std_specs__vec.rs__L242__Vec__T__A__as_mut_slice",
    "std_specs__vec.rs__L263__Vec__T__A__split_off",
    "std_specs__vec.rs__L300__Vec__T__A__truncate",
    "std_specs__vec.rs__L343__Vec__T__A1__as__PartialEq__Vec__U__A2__eq",
    "std_specs__vec.rs__L409__alloc__vec__from_elem",
    "std_specs__vec.rs__L457__a__Vec__T__A__as__core__iter__IntoIterator__into_iter",
    "std_specs__alloc.rs__L26__alloc__intrinsics__write_box_via_move",
    "std_specs__alloc.rs__L36__alloc__boxed__Box__T__new_uninit",
    "std_specs__smart_ptrs.rs__L12__T__into_vec",
    "std_specs__smart_ptrs.rs__L29__Rc__T__new",
    "std_specs__smart_ptrs.rs__L34__Rc__T__as__core__default__Default__default",
    "std_specs__smart_ptrs.rs__L41__Arc__T__new",
    "std_specs__smart_ptrs.rs__L46__Arc__T__as__core__default__Default__default",
    "std_specs__smart_ptrs.rs__L53__Box__T__A__as__Clone__clone",
    "std_specs__smart_ptrs.rs__L60__Rc__T__A__try_unwrap",
    "std_specs__maybe_uninit.rs__L39__MaybeUninit__T__assume_init",
    "std_specs__maybe_uninit.rs__L45__MaybeUninit__T__assume_init_ref",
    "std_specs__maybe_uninit.rs__L51__MaybeUninit__T__assume_init_mut",
    # hash / ffi / collection / nonzero / manuallydrop
    "std_specs__hash.rs__L625__HashMap__Key__Value__new",
    "std_specs__hash.rs__L634__HashMap__K__V__S__as__core__default__Default__default",
    "std_specs__hash.rs__L643__HashMap__Key__Value__with_capacity",
    "std_specs__hash.rs__L659__HashMap__Key__Value__S__A__insert",
    "std_specs__hash.rs__L836__HashMap__Key__Value__S__A__remove__Q",
    "std_specs__hash.rs__L1007__HashSet__Key__new",
    "std_specs__hash.rs__L1012__HashSet__T__S__as__core__default__Default__default",
    "std_specs__hash.rs__L1020__HashSet__Key__with_capacity",
    "std_specs__hash.rs__L1449__OccupiedEntry__insert",
    "std_specs__hash.rs__L1460__OccupiedEntry__remove",
    "std_specs__hash.rs__L1491__VacantEntry__insert",
    "std_specs__ffi.rs__L159__CStr__count_bytes",
    "std_specs__ffi.rs__L164__CStr__is_empty",
    "std_specs__ffi.rs__L179__CStr__from_bytes_with_nul",
    "std_specs__ffi.rs__L189__CStr__from_bytes_until_nul",
    "std_specs__ffi.rs__L225__CString__as_bytes",
    "std_specs__ffi.rs__L231__CString__as_bytes_with_nul",
    "std_specs__ffi.rs__L237__CString__as_c_str",
    "std_specs__ffi.rs__L243__CString__into_bytes",
    "std_specs__ffi.rs__L249__CString__into_bytes_with_nul",
    "std_specs__ffi.rs__L255__CString__into_boxed_c_str",
    "std_specs__collections_extra.rs__L46__BinaryHeap__T__new",
    "std_specs__collections_extra.rs__L51__BinaryHeap__T__A__len",
    "std_specs__collections_extra.rs__L78__BinaryHeap__T__A__append",
    "std_specs__collections_extra.rs__L87__BinaryHeap__T__A__pop",
    "std_specs__collections_extra.rs__L103__BinaryHeap__T__A__peek",
    "std_specs__collections_extra.rs__L118__BinaryHeap__T__A__into_vec",
    "std_specs__collections_extra.rs__L125__BinaryHeap__T__A__into_sorted_vec",
    "std_specs__collections_extra.rs__L132__LinkedList__T__new",
    "std_specs__collections_extra.rs__L144__LinkedList__T__A__is_empty",
    "std_specs__nonzero.rs__L70__NonZero__T__new",
    "std_specs__nonzero.rs__L82__NonZero__T__new_unchecked",
    "std_specs__nonzero.rs__L98__NonZero__T__get",
    "std_specs__manually_drop.rs__L30__ManuallyDrop__T__new",
    "std_specs__manually_drop.rs__L35__ManuallyDrop__T__into_inner",
    "std_specs__manually_drop.rs__L40__ManuallyDrop__T__as__Clone__clone",
    # option / result / range
    "std_specs__option.rs__L160__Option__T__unwrap",
    "std_specs__option.rs__L193__Option__T__expect",
    "std_specs__option.rs__L372__Option__as_slice",
    "std_specs__option.rs__L381__Option__as_mut_slice",
    "std_specs__option.rs__L395__Option__insert",
    "std_specs__option.rs__L402__Option__get_or_insert",
    "std_specs__result.rs__L177__Result__T__E__unwrap",
    "std_specs__result.rs__L196__Result__T__E__unwrap_err",
    "std_specs__result.rs__L215__Result__T__E__expect",
    "std_specs__range.rs__L74__Range__Idx__contains",
    "std_specs__range.rs__L82__RangeInclusive__Idx__contains",
    "std_specs__range.rs__L339__RangeInclusive__T__as__RangeBounds__T__start_bound",
    # slice / string / raw pointer
    "slice.rs__L83__T__len",
    "string.rs__L100__str__as_bytes",
    "string.rs__L136__str__from_utf8_unchecked",
    "std_specs__slice.rs__L56__Range__usize__as__SliceIndex__T__index",
    "std_specs__slice.rs__L92__core__hint__unreachable_unchecked",
    "std_specs__slice.rs__L213__T__copy_from_slice",
    "std_specs__slice.rs__L243__T__copy_within__R",
    "raw_ptr.rs__L198__mut__T__as__PartialEq__mut__T__eq",
    "raw_ptr.rs__L221__const__T__as__PartialEq__const__T__eq",
    "string.rs__L351__String__as__PartialEq__eq",
    "string.rs__L357__String__new",
    # layout / misc
    "layout.rs__L77__core__mem__size_of__V",
    "layout.rs__L85__core__mem__align_of__V",
    "std_specs__layout_value.rs__L50__Layout__from_size_align",
    "std_specs__layout_value.rs__L62__Layout__from_size_align_unchecked",
    "std_specs__layout_value.rs__L80__Layout__new__T",
    "std_specs__layout_value.rs__L93__Layout__align_to",
    "std_specs__layout_value.rs__L107__Layout__pad_to_align",
    "std_specs__layout_value.rs__L113__Layout__extend",
    "std_specs__layout_value.rs__L143__Layout__extend_packed",
    "std_specs__layout_value.rs__L161__Layout__repeat",
    "std_specs__layout_value.rs__L197__Layout__repeat_packed",
    "std_specs__layout_value.rs__L215__Layout__array__T",
    "std_specs__clone.rs__L44__T__N__as__Clone__clone",
    "std_specs__core.rs__L132__core__mem__swap__T",
    "std_specs__ordering.rs__L8__Ordering__is_eq",
    "std_specs__ordering.rs__L13__Ordering__is_ne",
    "std_specs__ordering.rs__L18__Ordering__is_lt",
    "std_specs__ordering.rs__L23__Ordering__is_gt",
    "std_specs__ordering.rs__L28__Ordering__is_le",
    "std_specs__ordering.rs__L33__Ordering__is_ge",
    "std_specs__convert.rs__L109__T__as__TryFrom__U__try_from",
}


def main() -> None:
    proved_root = ROOT / "proved-apis"
    all_ids = {
        path.parent.name
        for path in proved_root.glob("*/metadata.json")
    }
    audit_path = ROOT / "surrogate-audit" / "records.csv"
    with audit_path.open() as stream:
        audit_rows = list(csv.DictReader(stream))
    retained = sorted(
        row["id"]
        for row in audit_rows
        if row["strict_verdict"] == "strict_faithful_admissible"
    )
    retained_set = set(retained)
    assert retained_set <= all_ids
    assert len(retained) == 168, len(retained)
    downgraded = sorted(all_ids - retained_set)
    assert len(downgraded) == 238, len(downgraded)
    payload = {
        "policy": (
            "Conservative source-surrogate fidelity: retain only local surrogate "
            "functions whose executable bodies are exact copies or mechanical "
            "desugarings and whose proof artifacts are admissible. Alternate "
            "implementations, target-critical axioms, wrong mappings, unresolved "
            "source bodies, and blocked records use external-body fallback."
        ),
        "proof_scope": (
            "These are Verus proofs of local source_* surrogate functions, not direct "
            "proofs of the original external Rust std symbols."
        ),
        "counts": {
            "original_verified": len(all_ids),
            "retained_verified": len(retained),
            "downgraded": len(downgraded),
        },
        "retained": retained,
        "downgraded": downgraded,
    }
    (ROOT / "fidelity-verdicts.json").write_text(json.dumps(payload, indent=2) + "\n")
    (ROOT / "FIDELITY-FINAL.md").write_text(
        "# Final strict implementation-fidelity verdict\n\n"
        f"- Original passing proof records: **{len(all_ids)}**\n"
        f"- Retained as strict-faithful admissible local surrogates: **{len(retained)}**\n"
        f"- Passing artifacts downgraded to external-body fallback: **{len(downgraded)}**\n\n"
        "No original Rust std symbol is directly proved. The retained artifacts "
        "verify local `source_*` functions whose executable bodies were audited as "
        "exact or mechanically desugared and whose proofs are admissible. See "
        "`surrogate-audit/SUMMARY.md`.\n"
    )
    print(json.dumps(payload["counts"], indent=2))


if __name__ == "__main__":
    main()
