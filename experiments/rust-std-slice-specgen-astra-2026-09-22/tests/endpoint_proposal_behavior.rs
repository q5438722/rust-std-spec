// Compare authority originals, the ADOPTED current proof bodies, and public methods.
// Expectations follow the unchanged slice docs and element positions, not adopted code.
include!(env!("SLICE_ENDPOINTS_SOURCE"));

fn first_bindings<T>() -> [for<'a> fn(&'a [T]) -> Option<&'a T>; 3] {
    [original::first::<T>, adopted::first::<T>, <[T]>::first]
}

fn last_bindings<T>() -> [for<'a> fn(&'a [T]) -> Option<&'a T>; 3] {
    [original::last::<T>, adopted::last::<T>, <[T]>::last]
}

fn check_places<T>(input: &[T], first: Option<&T>, last: Option<&T>) {
    for (bindings, expected) in [(first_bindings::<T>(), first), (last_bindings::<T>(), last)] {
        for endpoint in bindings {
            match (endpoint(input), expected) {
                (None, None) => {}
                (Some(actual), Some(place)) => {
                    // ZST addresses cannot identify positions; the generic source/MIR
                    // projection argument is required, not pointer-equality testing.
                    if core::mem::size_of::<T>() != 0 {
                        assert!(core::ptr::eq(actual, place));
                    }
                }
                _ => panic!("endpoint variant differs from the documented expectation"),
            }
        }
    }
}

#[test]
fn empty_slices() {
    let input: [u8; 0] = [];
    check_places(&input, None, None);
}

#[test]
fn singleton_selects_the_only_place() {
    let input = [17];
    check_places(&input, Some(&input[0]), Some(&input[0]));
    assert_eq!(input, [17]);
}

#[test]
fn documented_example_and_exact_generic_signatures() {
    let input = [10, 40, 30];
    check_places(&input, Some(&input[0]), Some(&input[2]));
    for first in first_bindings::<i32>() {
        assert_eq!(first(&input), Some(&10));
    }
    for last in last_bindings::<i32>() {
        assert_eq!(last(&input), Some(&30));
    }
    assert_eq!(input, [10, 40, 30]);
}

#[test]
fn ordered_multiple_elements_are_not_reordered() {
    for input in [[1, 2, 3, 4], [4, 3, 2, 1], [90, 0, 255, 7]] {
        let before = input;
        check_places(&input, Some(&input[0]), Some(&input[3]));
        assert_eq!(input, before);
    }
}

#[test]
fn equal_values_do_not_substitute_for_endpoint_places() {
    let input = [7, 7, 7, 7];
    check_places(&input, Some(&input[0]), Some(&input[3]));
    assert!(!core::ptr::eq(&input[0], &input[3]));
    assert_eq!(input, [7, 7, 7, 7]);
}

#[test]
fn subslices_return_places_in_the_original_allocation() {
    let input = [91, 10, 40, 30, 92];
    let address = input.as_ptr();
    for (slice, first, last) in [
        (&input[1..4], Some(&input[1]), Some(&input[3])),
        (&input[2..3], Some(&input[2]), Some(&input[2])),
        (&input[..], Some(&input[0]), Some(&input[4])),
        (&input[..0], None, None),
        (&input[2..2], None, None),
        (&input[5..], None, None),
    ] {
        check_places(slice, first, last);
        assert_eq!(input, [91, 10, 40, 30, 92]);
        assert!(core::ptr::eq(input.as_ptr(), address));
    }
}

#[test]
fn zero_sized_elements_check_variants_not_position_by_address() {
    struct Zst;
    let empty: [Zst; 0] = [];
    let singleton = [Zst];
    let multiple = [Zst, Zst, Zst];
    check_places(&empty, None, None);
    check_places(&singleton, Some(&singleton[0]), Some(&singleton[0]));
    check_places(&multiple, Some(&multiple[0]), Some(&multiple[2]));
}

#[test]
fn maximum_length_legal_zero_sized_slice() {
    let input: &[()] = &[(); usize::MAX];
    assert_eq!(input.len(), usize::MAX);
    check_places(input, Some(&()), Some(&()));
}

#[test]
fn unconstrained_non_copy_elements_keep_their_values() {
    struct Opaque {
        number: u32,
        text: String,
    }
    let empty: [Opaque; 0] = [];
    let singleton = [Opaque { number: 17, text: String::from("only") }];
    let multiple = [
        Opaque { number: 10, text: String::from("first") },
        Opaque { number: 40, text: String::from("middle") },
        Opaque { number: 30, text: String::from("last") },
    ];
    check_places(&empty, None, None);
    check_places(&singleton, Some(&singleton[0]), Some(&singleton[0]));
    check_places(&multiple, Some(&multiple[0]), Some(&multiple[2]));
    assert_eq!(singleton[0].number, 17);
    assert_eq!(singleton[0].text, "only");
    for (element, (number, text)) in multiple.iter().zip([
        (10, "first"), (40, "middle"), (30, "last"),
    ]) {
        assert_eq!(element.number, number);
        assert_eq!(element.text, text);
    }
}

#[test]
fn non_static_elements_borrow_local_owners() {
    struct Borrowed<'a>(&'a str);
    let left = String::from("local first");
    let right = String::from("local last");
    let input = [Borrowed(&left), Borrowed(&right)];
    check_places(&input, Some(&input[0]), Some(&input[1]));
    for first in first_bindings::<Borrowed<'_>>() {
        assert_eq!(first(&input).unwrap().0, "local first");
    }
    for last in last_bindings::<Borrowed<'_>>() {
        assert_eq!(last(&input).unwrap().0, "local last");
    }
    assert_eq!(left, "local first");
    assert_eq!(right, "local last");
}

#[test]
fn legal_empty_uninhabited_elements() {
    enum Never {}
    let input: [Never; 0] = [];
    check_places(&input, None, None);
    const ORIGINAL_FIRST: Option<&Never> = original::first(&[]);
    const ADOPTED_FIRST: Option<&Never> = adopted::first(&[]);
    const PUBLIC_FIRST: Option<&Never> = <[Never]>::first(&[]);
    const ORIGINAL_LAST: Option<&Never> = original::last(&[]);
    const ADOPTED_LAST: Option<&Never> = adopted::last(&[]);
    const PUBLIC_LAST: Option<&Never> = <[Never]>::last(&[]);
    for endpoint in [
        ORIGINAL_FIRST, ADOPTED_FIRST, PUBLIC_FIRST,
        ORIGINAL_LAST, ADOPTED_LAST, PUBLIC_LAST,
    ] {
        assert!(endpoint.is_none());
    }
}

#[test]
fn observations_do_not_write_or_drop_elements() {
    use core::cell::Cell;
    struct Observed<'a> {
        value: Cell<u32>,
        drops: &'a Cell<usize>,
    }
    impl Drop for Observed<'_> {
        fn drop(&mut self) {
            self.drops.set(self.drops.get() + 1);
        }
    }
    let drops = Cell::new(0);
    {
        let input = [
            Observed { value: Cell::new(10), drops: &drops },
            Observed { value: Cell::new(40), drops: &drops },
            Observed { value: Cell::new(30), drops: &drops },
        ];
        for _ in 0..3 {
            check_places(&input, Some(&input[0]), Some(&input[2]));
            assert_eq!(drops.get(), 0);
            for (element, expected) in input.iter().zip([10, 40, 30]) {
                assert_eq!(element.value.get(), expected);
            }
        }
    }
    assert_eq!(drops.get(), 3);
}

#[test]
fn first_calls_remain_stable_const() {
    const RESULTS: [Option<&i32>; 9] = [
        original::first(&[]), adopted::first(&[]), <[i32]>::first(&[]),
        original::first(&[17]), adopted::first(&[17]), <[i32]>::first(&[17]),
        original::first(&[10, 40, 30]), adopted::first(&[10, 40, 30]),
        <[i32]>::first(&[10, 40, 30]),
    ];
    assert_eq!(RESULTS, [
        None, None, None, Some(&17), Some(&17), Some(&17),
        Some(&10), Some(&10), Some(&10),
    ]);
}

#[test]
fn last_calls_remain_stable_const() {
    const RESULTS: [Option<&i32>; 9] = [
        original::last(&[]), adopted::last(&[]), <[i32]>::last(&[]),
        original::last(&[17]), adopted::last(&[17]), <[i32]>::last(&[17]),
        original::last(&[10, 40, 30]), adopted::last(&[10, 40, 30]),
        <[i32]>::last(&[10, 40, 30]),
    ];
    assert_eq!(RESULTS, [
        None, None, None, Some(&17), Some(&17), Some(&17),
        Some(&30), Some(&30), Some(&30),
    ]);
}
