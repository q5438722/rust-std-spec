// Compare authority patterns, adopted current proofs and public methods.
include!(env!("SLICE_MUTABLE_SPLITS_SOURCE"));

fn first_bindings<T>() -> [for<'a> fn(&'a mut [T]) -> Option<(&'a mut T, &'a mut [T])>; 3] {
    [original::split_first_mut::<T>, adopted::split_first_mut::<T>, <[T]>::split_first_mut]
}

fn last_bindings<T>() -> [for<'a> fn(&'a mut [T]) -> Option<(&'a mut T, &'a mut [T])>; 3] {
    [original::split_last_mut::<T>, adopted::split_last_mut::<T>, <[T]>::split_last_mut]
}

fn check_writes(initial: &[i32], range: core::ops::Range<usize>, first: bool) {
    let bindings = if first { first_bindings::<i32>() } else { last_bindings::<i32>() };
    for split in bindings {
        for remainder_first in [false, true] {
            let mut input = initial.to_vec();
            let mut expected = initial.to_vec();
            let base = input.as_mut_ptr();
            match split(&mut input[range.clone()]) {
                None => assert!(range.is_empty()),
                Some((element, remainder)) => {
                    assert!(!range.is_empty());
                    let index = if first { range.start } else { range.end - 1 };
                    let rest = if first { range.start + 1..range.end } else { range.start..range.end - 1 };
                    assert_eq!(*element, initial[index]);
                    assert_eq!(remainder, &initial[rest.clone()]);
                    assert_eq!(element as *mut i32, base.wrapping_add(index));
                    assert_eq!(remainder.as_mut_ptr(), base.wrapping_add(rest.start));
                    for round in 0..3 {
                        let written = 1000 + round * 100;
                        if !remainder_first {
                            *element = written;
                        }
                        for (offset, value) in remainder.iter_mut().enumerate() {
                            *value = -written - offset as i32;
                            expected[rest.start + offset] = *value;
                        }
                        if remainder_first {
                            *element = written;
                        }
                        expected[index] = written;
                        assert_eq!(*element, written);
                        assert_eq!(remainder, &expected[rest.clone()]);
                        for offset in 0..remainder.len() {
                            *element += 1;
                            remainder[offset] -= 7;
                            expected[index] += 1;
                            expected[rest.start + offset] -= 7;
                            assert_eq!(*element, expected[index]);
                            assert_eq!(remainder[offset], expected[rest.start + offset]);
                        }
                        assert_eq!(*element, expected[index]);
                        assert_eq!(remainder, &expected[rest.clone()]);
                    }
                }
            }
            assert_eq!(input, expected);
            assert_eq!(&input[..range.start], &initial[..range.start]);
            assert_eq!(&input[range.end..], &initial[range.end..]);
        }
    }
}

#[test]
fn empty_slices_and_empty_subranges_preserve_the_complete_frame() {
    for first in [true, false] {
        check_writes(&[], 0..0, first);
        for range in [0..0, 2..2, 5..5] {
            check_writes(&[91, 10, 40, 30, 92], range, first);
        }
    }
}

#[test]
fn singleton_empty_remainders_keep_first_one_past_and_last_start_origins() {
    for first in [true, false] {
        check_writes(&[17], 0..1, first);
        check_writes(&[91, 17, 92], 1..2, first);
        let bindings = if first { first_bindings::<u32>() } else { last_bindings::<u32>() };
        for split in bindings {
            let mut input = [17];
            let base = input.as_mut_ptr();
            let (element, remainder) = split(&mut input).unwrap();
            assert_eq!(*element, 17);
            assert!(remainder.is_empty());
            assert_eq!(element as *mut u32, base);
            assert_eq!(remainder.as_mut_ptr(), base.wrapping_add(usize::from(first)));
            assert_ne!(base, base.wrapping_add(1));
            *element = 71;
            assert!(remainder.is_empty());
            *element = 72;
            assert_eq!(input, [72]);
        }
    }
}

#[test]
fn pairs_keep_element_then_remainder_order_and_allow_both_write_orders() {
    for first in [true, false] {
        check_writes(&[10, 20], 0..2, first);
        check_writes(&[91, 10, 20, 92], 1..3, first);
    }
}

#[test]
fn original_documentation_examples_and_exact_generic_signatures() {
    for split in first_bindings::<i32>() {
        let x = &mut [0, 1, 2];
        if let Some((first, elements)) = split(x) {
            assert_eq!(*first, 0);
            assert_eq!(elements, &[1, 2]);
            *first = 3;
            elements[0] = 4;
            elements[1] = 5;
        } else {
            panic!("nonempty documentation input");
        }
        assert_eq!(x, &[3, 4, 5]);
    }
    for split in last_bindings::<i32>() {
        let x = &mut [0, 1, 2];
        if let Some((last, elements)) = split(x) {
            assert_eq!(*last, 2);
            assert_eq!(elements, &[0, 1]);
            *last = 3;
            elements[0] = 4;
            elements[1] = 5;
        } else {
            panic!("nonempty documentation input");
        }
        assert_eq!(x, &[4, 5, 3]);
    }
}

#[test]
fn complete_ordered_remainders_are_neither_shortened_nor_reordered() {
    for initial in [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [90, 0, 255, -7, 12]] {
        for first in [true, false] {
            check_writes(&initial, 0..5, first);
            check_writes(&initial, 1..4, first);
        }
    }
}

#[test]
fn repeated_contents_do_not_substitute_for_the_returned_places() {
    for first in [true, false] {
        check_writes(&[7, 7, 7, 7, 7], 0..5, first);
        check_writes(&[7, 7, 7, 7, 7], 1..4, first);
    }
}

#[test]
fn every_receiver_subrange_preserves_both_surroundings() {
    let initial = [91, 10, 40, 30, 92];
    for start in 0..=initial.len() {
        for end in start..=initial.len() {
            for first in [true, false] {
                check_writes(&initial, start..end, first);
            }
        }
    }
}

#[test]
fn both_outputs_remain_live_during_reborrows_and_interleaved_writes() {
    for first in [true, false] {
        let bindings = if first { first_bindings::<i32>() } else { last_bindings::<i32>() };
        for split in bindings {
            for remainder_first in [true, false] {
                let mut input = [91, 10, 40, 30, 92];
                let (element, remainder) = split(&mut input[1..4]).unwrap();
                assert_eq!(*element, if first { 10 } else { 30 });
                assert_eq!(remainder, if first { &[40, 30] } else { &[10, 40] });
                for step in 0..4 {
                    let element_borrow = &mut *element;
                    let remainder_borrow = &mut remainder[..];
                    if remainder_first {
                        remainder_borrow[0] = 100 + step;
                        *element_borrow = 200 + step;
                    } else {
                        *element_borrow = 200 + step;
                        remainder_borrow[0] = 100 + step;
                    }
                    remainder_borrow[1] = 300 + step;
                    *element_borrow += 1;
                    remainder[0] += 1;
                    *element += 1;
                    remainder[1] += 1;
                    assert_eq!(*element, 202 + step);
                    assert_eq!(remainder, &[101 + step, 301 + step]);
                }
                assert_eq!(input, if first { [91, 205, 104, 304, 92] } else { [91, 104, 304, 205, 92] });
            }
        }
    }
}

#[test]
fn sequential_calls_observe_the_entire_previous_writeback() {
    for first in [true, false] {
        let bindings = if first { first_bindings::<i32>() } else { last_bindings::<i32>() };
        for split in bindings {
            let mut input = [91, 10, 40, 30, 92];
            {
                let (element, remainder) = split(&mut input[1..4]).unwrap();
                *element = 61;
                remainder.copy_from_slice(&[62, 63]);
                *element = 64;
                assert_eq!(remainder, &[62, 63]);
            }
            let once = if first { [91, 64, 62, 63, 92] } else { [91, 62, 63, 64, 92] };
            assert_eq!(input, once);
            let (element, remainder) = split(&mut input[1..4]).unwrap();
            assert_eq!(*element, 64);
            assert_eq!(remainder, &[62, 63]);
            remainder[1] = 73;
            *element = 74;
            remainder[0] = 72;
            assert_eq!(*element, 74);
            assert_eq!(input, if first { [91, 74, 72, 73, 92] } else { [91, 72, 73, 74, 92] });
        }
    }
}

#[test]
fn unconstrained_non_copy_elements_can_be_replaced_through_both_outputs() {
    struct Opaque(String);
    let labels = ["outside left", "first", "middle", "last", "outside right"];
    for first in [true, false] {
        let bindings = if first { first_bindings::<Opaque>() } else { last_bindings::<Opaque>() };
        for split in bindings {
            let mut empty: [Opaque; 0] = [];
            assert!(split(&mut empty).is_none());
            let mut singleton = [Opaque(String::from("only"))];
            let (element, remainder) = split(&mut singleton).unwrap();
            assert_eq!(element.0, "only");
            assert_eq!(remainder.len(), 0);
            *element = Opaque(String::from("replacement"));
            assert_eq!(singleton[0].0, "replacement");
            let mut input = labels.map(|value| Opaque(String::from(value)));
            let (element, remainder) = split(&mut input[1..4]).unwrap();
            assert_eq!(element.0, if first { "first" } else { "last" });
            let rest = if first { ["middle", "last"] } else { ["first", "middle"] };
            assert_eq!(remainder.iter().map(|x| x.0.as_str()).collect::<Vec<_>>(), rest);
            *element = Opaque(String::from("selected"));
            remainder[0] = Opaque(String::from("rest zero"));
            element.0.push_str(" again");
            remainder[1] = Opaque(String::from("rest one"));
            assert_eq!(element.0, "selected again");
            let middle = if first { ["selected again", "rest zero", "rest one"] }
                         else { ["rest zero", "rest one", "selected again"] };
            assert_eq!(input.each_ref().map(|x| x.0.as_str()),
                       [labels[0], middle[0], middle[1], middle[2], labels[4]]);
        }
    }
}

#[test]
fn non_static_elements_can_independently_borrow_local_replacements() {
    struct Borrowed<'a>(&'a str);
    let labels = ["outside left", "first", "middle", "last", "outside right"];
    let owners = labels.map(String::from);
    let replacements = ["selected", "remainder zero", "remainder one"].map(String::from);
    for first in [true, false] {
        let bindings = if first { first_bindings::<Borrowed<'_>>() } else { last_bindings::<Borrowed<'_>>() };
        for split in bindings {
            let mut input = owners.each_ref().map(|owner| Borrowed(owner.as_str()));
            let (element, remainder) = split(&mut input[1..4]).unwrap();
            assert_eq!(element.0, if first { "first" } else { "last" });
            assert_eq!(remainder.iter().map(|x| x.0).collect::<Vec<_>>(),
                       if first { ["middle", "last"] } else { ["first", "middle"] });
            remainder[0] = Borrowed(&replacements[1]);
            *element = Borrowed(&replacements[0]);
            remainder[1] = Borrowed(&replacements[2]);
            assert_eq!(element.0, "selected");
            assert_eq!(remainder[0].0, "remainder zero");
            let middle = if first { ["selected", "remainder zero", "remainder one"] }
                         else { ["remainder zero", "remainder one", "selected"] };
            assert_eq!(input.each_ref().map(|x| x.0),
                       [labels[0], middle[0], middle[1], middle[2], labels[4]]);
            assert_eq!(owners, labels);
        }
    }
}

#[test]
fn obtaining_and_writing_both_borrows_neither_clones_nor_adds_drops() {
    use core::cell::Cell;
    struct Tracked<'a> {
        value: i32,
        drops: &'a Cell<usize>,
        clones: &'a Cell<usize>,
    }
    impl Clone for Tracked<'_> {
        fn clone(&self) -> Self {
            self.clones.set(self.clones.get() + 1);
            Self { value: self.value, drops: self.drops, clones: self.clones }
        }
    }
    impl Drop for Tracked<'_> {
        fn drop(&mut self) {
            self.drops.set(self.drops.get() + 1);
        }
    }
    let drops = Cell::new(0);
    let clones = Cell::new(0);
    for first in [true, false] {
        let bindings = if first { first_bindings::<Tracked<'_>>() } else { last_bindings::<Tracked<'_>>() };
        for split in bindings {
            drops.set(0);
            let mut input = [91, 10, 40, 30, 92].map(|value| Tracked { value, drops: &drops, clones: &clones });
            let (element, remainder) = split(&mut input[1..4]).unwrap();
            assert_eq!(element.value, if first { 10 } else { 30 });
            assert_eq!(remainder.iter().map(|x| x.value).collect::<Vec<_>>(),
                       if first { [40, 30] } else { [10, 40] });
            assert_eq!(drops.get(), 0);
            assert_eq!(clones.get(), 0);
            element.value = 71;
            remainder[0].value = 72;
            element.value = 74;
            remainder[1].value = 73;
            assert_eq!(element.value, 74);
            assert_eq!(input.each_ref().map(|x| x.value),
                       if first { [91, 74, 72, 73, 92] } else { [91, 72, 73, 74, 92] });
            assert_eq!(drops.get(), 0);
            assert_eq!(clones.get(), 0);
            drop(input);
            assert_eq!(drops.get(), 5);
        }
    }
}

#[test]
fn replacement_drops_are_exactly_the_callers_explicit_replacements() {
    use core::cell::Cell;
    struct Tracked<'a>(i32, &'a Cell<usize>);
    impl Drop for Tracked<'_> {
        fn drop(&mut self) { self.1.set(self.1.get() + 1); }
    }
    let drops = Cell::new(0);
    for first in [true, false] {
        let bindings = if first { first_bindings::<Tracked<'_>>() } else { last_bindings::<Tracked<'_>>() };
        for split in bindings {
            drops.set(0);
            let mut input = [10, 20, 30].map(|value| Tracked(value, &drops));
            let (element, remainder) = split(&mut input).unwrap();
            assert_eq!(drops.get(), 0);
            *element = Tracked(71, &drops);
            assert_eq!(drops.get(), 1);
            remainder[0] = Tracked(72, &drops);
            assert_eq!(drops.get(), 2);
            *element = Tracked(74, &drops);
            assert_eq!(drops.get(), 3);
            remainder[1] = Tracked(73, &drops);
            assert_eq!(drops.get(), 4);
            assert_eq!(element.0, 74);
            assert_eq!(input.each_ref().map(|x| x.0), if first { [74, 72, 73] } else { [72, 73, 74] });
            drop(input);
            assert_eq!(drops.get(), 7);
        }
    }
}

#[test]
fn zero_sized_elements_check_values_extents_and_writes_not_addresses() {
    struct Zst;
    for split in first_bindings::<Zst>().into_iter().chain(last_bindings::<Zst>()) {
        let mut empty: [Zst; 0] = [];
        assert!(split(&mut empty).is_none());
        for range in [0..0, 0..1, 1..4, 2..2, 0..5] {
            let mut input = [Zst, Zst, Zst, Zst, Zst];
            match split(&mut input[range.clone()]) {
                None => assert!(range.is_empty()),
                Some((element, remainder)) => {
                    assert_eq!(remainder.len(), range.len() - 1);
                    assert!(matches!(*element, Zst));
                    assert!(remainder.iter().all(|value| matches!(value, Zst)));
                    *element = Zst;
                    for value in remainder.iter_mut() {
                        *value = Zst;
                        *element = Zst;
                    }
                    assert!(matches!(*element, Zst));
                    assert_eq!(remainder.len(), range.len() - 1);
                }
            }
            assert_eq!(input.len(), 5);
            assert!(input.iter().all(|value| matches!(value, Zst)));
            assert_eq!(input[..range.start].len(), range.start);
            assert_eq!(input[range.end..].len(), 5 - range.end);
        }
    }
}

#[test]
fn aligned_zero_sized_outputs_allow_simultaneous_independent_writes() {
    #[repr(align(64))]
    struct Aligned;
    for split in first_bindings::<Aligned>().into_iter().chain(last_bindings::<Aligned>()) {
        let mut input = [Aligned, Aligned, Aligned];
        assert!(split(&mut input[1..1]).is_none());
        let (element, remainder) = split(&mut input).unwrap();
        assert_eq!(core::mem::size_of_val(element), 0);
        assert_eq!(core::mem::align_of_val(element), 64);
        assert_eq!(remainder.len(), 2);
        assert_eq!(core::mem::size_of_val(remainder), 0);
        assert_eq!(core::mem::align_of_val(remainder), 64);
        remainder[0] = Aligned;
        *element = Aligned;
        remainder[1] = Aligned;
        assert!(matches!(*element, Aligned));
        assert!(matches!(input, [Aligned, Aligned, Aligned]));
    }
}

#[test]
fn legal_maximum_length_zero_sized_slices_allow_both_output_writes() {
    for split in first_bindings::<()>().into_iter().chain(last_bindings::<()>()) {
        // Unit Vec construction avoids enormous array constants in textual MIR.
        let mut input = vec![(); usize::MAX];
        for range in [0..usize::MAX, 1..usize::MAX - 1] {
            let (element, remainder) = split(&mut input[range.clone()]).unwrap();
            assert_eq!(*element, ());
            assert_eq!(remainder.len(), range.len() - 1);
            let last = remainder.len() - 1;
            assert_eq!(remainder[0], ());
            assert_eq!(remainder[last], ());
            remainder[0] = ();
            *element = ();
            remainder[last] = ();
            *element = ();
            assert_eq!(remainder.len(), range.len() - 1);
            assert_eq!(*element, ());
        }
        // Length and the sole unit value describe this sequence, not ZST addresses.
        assert_eq!(input.len(), usize::MAX);
        assert_eq!(core::mem::size_of_val(&input[..]), 0);
        assert_eq!(input[0], ());
        assert_eq!(input[usize::MAX - 1], ());
        assert_eq!(input[..1].len(), 1);
        assert_eq!(input[usize::MAX - 1..].len(), 1);
    }
}

#[test]
fn empty_uninhabited_elements_are_legal_in_runtime_and_const_calls() {
    enum Never {}
    for split in first_bindings::<Never>().into_iter().chain(last_bindings::<Never>()) {
        let mut input: [Never; 0] = [];
        assert!(split(&mut input).is_none());
        assert_eq!(input.len(), 0);
    }
    const EMPTY: [bool; 6] = [
        { let mut input: [Never; 0] = []; original::split_first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; adopted::split_first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; <[Never]>::split_first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; original::split_last_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; adopted::split_last_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; <[Never]>::split_last_mut(&mut input).is_none() },
    ];
    assert_eq!(EMPTY, [true; 6]);
}

macro_rules! const_writes {
    ($api:expr, $first:literal) => {{
        let mut empty: [i32; 0] = [];
        assert!(matches!($api(&mut empty), None));
        let mut singleton = [17];
        match $api(&mut singleton) {
            Some((element, remainder)) => {
                assert!(*element == 17);
                assert!(remainder.len() == 0);
                *element = 71;
            }
            None => panic!("const singleton returned None"),
        }
        let mut pair = [10, 20];
        match $api(&mut pair) {
            Some((element, remainder)) => {
                assert!(*element == if $first { 10 } else { 20 });
                assert!(remainder.len() == 1);
                assert!(remainder[0] == if $first { 20 } else { 10 });
                remainder[0] = 52;
                *element = 50;
                remainder[0] = 53;
                *element = 51;
            }
            None => panic!("const pair returned None"),
        }
        let mut framed = [91, 10, 40, 30, 92];
        let (_, right) = framed.split_at_mut(1);
        let (middle, _) = right.split_at_mut(3);
        match $api(middle) {
            Some((element, remainder)) => {
                assert!(*element == if $first { 10 } else { 30 });
                assert!(remainder.len() == 2);
                assert!(remainder[0] == if $first { 40 } else { 10 });
                assert!(remainder[1] == if $first { 30 } else { 40 });
                *element = 61;
                remainder[0] = 62;
                remainder[1] = 63;
                *element = 64;
                remainder[1] = 65;
                assert!(*element == 64);
            }
            None => panic!("const receiver subrange returned None"),
        }
        (singleton, pair, framed)
    }};
}

#[test]
fn split_first_mut_const_calls_mutate_both_outputs_in_tuple_order() {
    const RESULTS: [([i32; 1], [i32; 2], [i32; 5]); 3] = [
        const_writes!(original::split_first_mut, true),
        const_writes!(adopted::split_first_mut, true),
        const_writes!(<[i32]>::split_first_mut, true),
    ];
    for result in RESULTS {
        assert_eq!(result, ([71], [51, 53], [91, 64, 62, 65, 92]));
    }
}

#[test]
fn split_last_mut_const_calls_mutate_both_outputs_in_tuple_order() {
    const RESULTS: [([i32; 1], [i32; 2], [i32; 5]); 3] = [
        const_writes!(original::split_last_mut, false),
        const_writes!(adopted::split_last_mut, false),
        const_writes!(<[i32]>::split_last_mut, false),
    ];
    for result in RESULTS {
        assert_eq!(result, ([71], [53, 51], [91, 62, 65, 64, 92]));
    }
}
