// Compare authority patterns, adopted current proofs and public methods.
// Expectations follow the docs and complete write-back/frame observations.
include!(env!("SLICE_MUTABLE_ENDPOINTS_SOURCE"));

fn first_bindings<T>() -> [for<'a> fn(&'a mut [T]) -> Option<&'a mut T>; 3] {
    [original::first_mut::<T>, adopted::first_mut::<T>, <[T]>::first_mut]
}

fn last_bindings<T>() -> [for<'a> fn(&'a mut [T]) -> Option<&'a mut T>; 3] {
    [original::last_mut::<T>, adopted::last_mut::<T>, <[T]>::last_mut]
}

fn check_write(initial: &[i32], range: core::ops::Range<usize>, first: bool, written: i32) {
    let position = if range.is_empty() {
        None
    } else if first {
        Some(range.start)
    } else {
        Some(range.end - 1)
    };
    let bindings = if first { first_bindings::<i32>() } else { last_bindings::<i32>() };
    for endpoint in bindings {
        let mut input = initial.to_vec();
        let mut expected = initial.to_vec();
        if let Some(index) = position {
            expected[index] = written;
        }
        match (endpoint(&mut input[range.clone()]), position) {
            (None, None) => {}
            (Some(element), Some(index)) => {
                assert_eq!(*element, initial[index]);
                *element = written;
                assert_eq!(*element, written);
            }
            _ => panic!("endpoint variant differs from the documented expectation"),
        }
        assert_eq!(input, expected);
        assert_eq!(&input[..range.start], &initial[..range.start]);
        assert_eq!(&input[range.end..], &initial[range.end..]);
    }
}

#[test]
fn empty_slices_and_empty_subranges_preserve_the_complete_frame() {
    for first in [true, false] {
        check_write(&[], 0..0, first, 71);
        for range in [0..0, 2..2, 5..5] {
            check_write(&[91, 10, 40, 30, 92], range, first, 71);
        }
    }
}

#[test]
fn singleton_returns_and_writes_the_only_element() {
    for first in [true, false] {
        check_write(&[17], 0..1, first, 71);
        check_write(&[91, 17, 92], 1..2, first, 71);
    }
}

#[test]
fn two_elements_select_distinct_write_back_positions() {
    for first in [true, false] {
        check_write(&[10, 20], 0..2, first, 71);
        check_write(&[91, 10, 20, 92], 1..3, first, 71);
    }
}

#[test]
fn documented_examples_and_exact_generic_signatures() {
    for endpoint in first_bindings::<i32>() {
        let mut input = [0, 1, 2];
        let first = endpoint(&mut input).expect("nonempty documented input");
        assert_eq!(*first, 0);
        *first = 5;
        assert_eq!(input, [5, 1, 2]);
    }
    for endpoint in last_bindings::<i32>() {
        let mut input = [0, 1, 2];
        let last = endpoint(&mut input).expect("nonempty documented input");
        assert_eq!(*last, 2);
        *last = 10;
        assert_eq!(input, [0, 1, 10]);
    }
}

#[test]
fn ordered_inputs_are_not_reordered_or_partially_updated() {
    for initial in [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [90, 0, 255, -7, 12]] {
        for first in [true, false] {
            check_write(&initial, 0..5, first, -12345);
            check_write(&initial, 1..4, first, -12345);
        }
    }
}

#[test]
fn repeated_values_do_not_substitute_for_selected_places() {
    for first in [true, false] {
        check_write(&[7, 7, 7, 7, 7], 0..5, first, 99);
        check_write(&[7, 7, 7, 7, 7], 1..4, first, 99);
    }
}

#[test]
fn every_subrange_preserves_all_other_elements_and_the_outside_frame() {
    let input = [91, 10, 40, 30, 92];
    for start in 0..=input.len() {
        for end in start..=input.len() {
            for first in [true, false] {
                check_write(&input, start..end, first, -12345);
            }
        }
    }
}

#[test]
fn returned_references_allow_legal_reborrowing_and_sequential_writes() {
    for first in [true, false] {
        let bindings = if first { first_bindings::<i32>() } else { last_bindings::<i32>() };
        for endpoint in bindings {
            let mut input = [91, 10, 40, 30, 92];
            let position = if first { 1 } else { 3 };
            let before = input[position];
            {
                let element = endpoint(&mut input[1..4]).unwrap();
                assert_eq!(*element, before);
                let reborrow: &mut i32 = &mut *element;
                *reborrow = 51;
                assert_eq!(*element, 51);
                *element = 61;
            }
            let mut expected = [91, 10, 40, 30, 92];
            expected[position] = 61;
            assert_eq!(input, expected);
            let element = endpoint(&mut input[1..4]).unwrap();
            assert_eq!(*element, 61);
            *element = 71;
            expected[position] = 71;
            assert_eq!(input, expected);
        }
    }
}

#[test]
fn unconstrained_non_copy_elements_can_be_replaced_in_place() {
    struct Opaque(String);
    let initial = ["outside left", "first", "middle", "last", "outside right"];
    for first in [true, false] {
        let bindings = if first { first_bindings::<Opaque>() } else { last_bindings::<Opaque>() };
        for endpoint in bindings {
            let mut empty: [Opaque; 0] = [];
            assert!(endpoint(&mut empty).is_none());
            assert_eq!(empty.len(), 0);
            let mut singleton = [Opaque(String::from("only"))];
            let element = endpoint(&mut singleton).unwrap();
            assert_eq!(element.0, "only");
            *element = Opaque(String::from("replacement"));
            assert_eq!(singleton[0].0, "replacement");

            let mut input = initial.map(|value| Opaque(String::from(value)));
            let position = if first { 1 } else { 3 };
            let element = endpoint(&mut input[1..4]).unwrap();
            assert_eq!(element.0, initial[position]);
            *element = Opaque(String::from("replacement"));
            for (index, value) in input.iter().enumerate() {
                assert_eq!(value.0, if index == position { "replacement" } else { initial[index] });
            }
        }
    }
}

#[test]
fn non_static_elements_borrow_and_write_local_owners() {
    struct Borrowed<'a>(&'a str);
    let labels = ["outside left", "local first", "local middle", "local last", "outside right"];
    let owners = labels.map(String::from);
    let replacement = String::from("local replacement");
    for first in [true, false] {
        let bindings = if first {
            first_bindings::<Borrowed<'_>>()
        } else {
            last_bindings::<Borrowed<'_>>()
        };
        for endpoint in bindings {
            let mut input = owners.each_ref().map(|owner| Borrowed(owner.as_str()));
            let position = if first { 1 } else { 3 };
            let element = endpoint(&mut input[1..4]).unwrap();
            assert_eq!(element.0, owners[position]);
            *element = Borrowed(&replacement);
            for (index, value) in input.iter().enumerate() {
                let expected = if index == position { replacement.as_str() } else { &owners[index] };
                assert_eq!(value.0, expected);
            }
            for (owner, initial) in owners.iter().zip(labels) {
                assert_eq!(owner, initial);
            }
        }
    }
}

#[test]
fn obtaining_and_using_the_borrow_does_not_add_element_drops() {
    use core::cell::Cell;
    struct Tracked<'a> {
        value: i32,
        drops: &'a Cell<usize>,
    }
    impl Drop for Tracked<'_> {
        fn drop(&mut self) {
            self.drops.set(self.drops.get() + 1);
        }
    }
    let drops = Cell::new(0);
    for first in [true, false] {
        let bindings = if first { first_bindings::<Tracked<'_>>() } else { last_bindings::<Tracked<'_>>() };
        for endpoint in bindings {
            drops.set(0);
            let mut input = [91, 10, 40, 30, 92].map(|value| Tracked { value, drops: &drops });
            let position = if first { 1 } else { 3 };
            let element = endpoint(&mut input[1..4]).unwrap();
            assert_eq!(drops.get(), 0);
            assert_eq!(element.value, if first { 10 } else { 30 });
            element.value = 71;
            let mut expected = [91, 10, 40, 30, 92];
            expected[position] = 71;
            assert_eq!(input.each_ref().map(|element| element.value), expected);
            assert_eq!(drops.get(), 0);
            drop(input);
            assert_eq!(drops.get(), 5);
        }
    }
}

#[test]
fn zero_sized_elements_check_variants_and_writes_not_addresses() {
    struct Zst;
    assert_eq!(core::mem::size_of::<Zst>(), 0);
    for endpoint in first_bindings::<Zst>().into_iter().chain(last_bindings::<Zst>()) {
        let mut empty: [Zst; 0] = [];
        assert!(endpoint(&mut empty).is_none());
        let mut singleton = [Zst];
        let element = endpoint(&mut singleton).unwrap();
        assert!(matches!(*element, Zst));
        *element = Zst;
        assert!(matches!(singleton, [Zst]));
        for range in [0..0, 0..1, 1..4, 2..2, 0..5] {
            let mut input = [Zst, Zst, Zst, Zst, Zst];
            match endpoint(&mut input[range.clone()]) {
                None => assert!(range.is_empty()),
                Some(element) => {
                    assert!(!range.is_empty());
                    assert!(matches!(*element, Zst));
                    *element = Zst;
                }
            }
            assert_eq!(input.len(), 5);
            assert!(input.iter().all(|element| matches!(element, Zst)));
            assert!(input[..range.start].iter().all(|element| matches!(element, Zst)));
            assert!(input[range.end..].iter().all(|element| matches!(element, Zst)));
        }
    }
}

#[test]
fn aligned_zero_sized_elements_need_no_address_based_position_claim() {
    #[repr(align(64))]
    struct Aligned;
    for endpoint in first_bindings::<Aligned>().into_iter().chain(last_bindings::<Aligned>()) {
        let mut input = [Aligned, Aligned, Aligned];
        assert!(endpoint(&mut input[1..1]).is_none());
        let element = endpoint(&mut input[1..2]).unwrap();
        assert!(matches!(*element, Aligned));
        assert_eq!(core::mem::size_of_val(element), 0);
        assert_eq!(core::mem::align_of_val(element), 64);
        *element = Aligned;
        assert!(matches!(input, [Aligned, Aligned, Aligned]));
    }
}

#[test]
fn maximum_length_legal_zero_sized_slice_allows_safe_writes() {
    for endpoint in first_bindings::<()>().into_iter().chain(last_bindings::<()>()) {
        // Vec's unit specialization constructs this legal slice without expanding
        // a usize::MAX array constant in rustc's textual MIR printer.
        let mut input = vec![(); usize::MAX];
        assert_eq!(input.len(), usize::MAX);
        let element = endpoint(&mut input).unwrap();
        assert_eq!(*element, ());
        *element = ();
        let element = endpoint(&mut input[1..usize::MAX - 1]).unwrap();
        assert_eq!(*element, ());
        *element = ();
        // Length and the sole inhabited unit value describe this entire sequence;
        // identical ZST addresses cannot establish which position was borrowed.
        assert_eq!(input.len(), usize::MAX);
        assert_eq!(core::mem::size_of_val(&input[..]), 0);
        assert_eq!(input[0], ());
        assert_eq!(input[usize::MAX - 1], ());
        assert_eq!(input[..1].len(), 1);
        assert_eq!(input[usize::MAX - 1..].len(), 1);
    }
}

#[test]
fn empty_uninhabited_elements_are_legal_at_runtime_and_in_const_calls() {
    enum Never {}
    for endpoint in first_bindings::<Never>().into_iter().chain(last_bindings::<Never>()) {
        let mut input: [Never; 0] = [];
        assert!(endpoint(&mut input).is_none());
        assert_eq!(input.len(), 0);
    }
    const EMPTY: [bool; 6] = [
        { let mut input: [Never; 0] = []; original::first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; adopted::first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; <[Never]>::first_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; original::last_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; adopted::last_mut(&mut input).is_none() },
        { let mut input: [Never; 0] = []; <[Never]>::last_mut(&mut input).is_none() },
    ];
    assert_eq!(EMPTY, [true; 6]);
}

macro_rules! const_writes {
    ($api:expr, $first:literal) => {{
        let mut empty: [i32; 0] = [];
        assert!(matches!($api(&mut empty), None));
        let mut singleton = [17];
        match $api(&mut singleton) {
            Some(element) => { assert!(*element == 17); *element = 71; }
            None => panic!("const singleton returned None"),
        }
        let mut pair = [10, 20];
        match $api(&mut pair) {
            Some(element) => {
                assert!(*element == if $first { 10 } else { 20 });
                *element = 51;
            }
            None => panic!("const pair returned None"),
        }
        let mut framed = [91, 10, 40, 30, 92];
        let (_, right) = framed.split_at_mut(1);
        let (middle, _) = right.split_at_mut(3);
        match $api(middle) {
            Some(element) => {
                assert!(*element == if $first { 10 } else { 30 });
                *element = 61;
            }
            None => panic!("const subrange returned None"),
        }
        (singleton, pair, framed)
    }};
}

#[test]
fn first_mut_calls_and_writes_remain_stable_const() {
    const RESULTS: [([i32; 1], [i32; 2], [i32; 5]); 3] = [
        const_writes!(original::first_mut, true),
        const_writes!(adopted::first_mut, true),
        const_writes!(<[i32]>::first_mut, true),
    ];
    for result in RESULTS {
        assert_eq!(result, ([71], [51, 20], [91, 61, 40, 30, 92]));
    }
}

#[test]
fn last_mut_calls_and_writes_remain_stable_const() {
    const RESULTS: [([i32; 1], [i32; 2], [i32; 5]); 3] = [
        const_writes!(original::last_mut, false),
        const_writes!(adopted::last_mut, false),
        const_writes!(<[i32]>::last_mut, false),
    ];
    for result in RESULTS {
        assert_eq!(result, ([71], [10, 51], [91, 10, 40, 61, 92]));
    }
}
