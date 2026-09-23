// Compare authority patterns, approved current bodies and public methods.
// Expectations use the unchanged docs and explicit input ranges.
include!(env!("SLICE_SPLITS_SOURCE"));

fn first_bindings<T>() -> [for<'a> fn(&'a [T]) -> Option<(&'a T, &'a [T])>; 3] {
    [original::split_first::<T>, adopted::split_first::<T>, <[T]>::split_first]
}

fn last_bindings<T>() -> [for<'a> fn(&'a [T]) -> Option<(&'a T, &'a [T])>; 3] {
    [original::split_last::<T>, adopted::split_last::<T>, <[T]>::split_last]
}

fn check_places<T>(
    input: &[T],
    first: Option<(&T, &[T])>,
    last: Option<(&T, &[T])>,
) {
    for (bindings, expected) in [(first_bindings::<T>(), first), (last_bindings::<T>(), last)] {
        for split in bindings {
            match (split(input), expected) {
                (None, None) => {}
                (Some((element, remainder)), Some((place, rest))) => {
                    assert_eq!(remainder.len(), rest.len());
                    // ZST origins follow the source/MIR argument, not address equality.
                    if core::mem::size_of::<T>() != 0 {
                        assert!(core::ptr::eq(element, place));
                        assert!(core::ptr::eq(remainder.as_ptr(), rest.as_ptr()));
                        for (actual, expected) in remainder.iter().zip(rest) {
                            assert!(core::ptr::eq(actual, expected));
                        }
                    }
                }
                _ => panic!("split variant differs from the documented expectation"),
            }
        }
    }
}

#[test]
fn empty_slices_return_none() {
    let input: [u8; 0] = [];
    check_places(&input, None, None);
}

#[test]
fn singleton_empty_remainders_keep_their_distinct_origins() {
    let input = [17u32];
    check_places(&input, Some((&input[0], &input[1..1])), Some((&input[0], &input[0..0])));
    assert_ne!(input[1..1].as_ptr(), input[0..0].as_ptr());
    assert_eq!(input, [17]);
}

#[test]
fn two_elements_keep_element_then_remainder_order() {
    let input = [10, 20];
    check_places(&input, Some((&input[0], &input[1..2])), Some((&input[1], &input[0..1])));
    for split in first_bindings::<i32>() {
        assert_eq!(split(&input), Some((&10, &[20][..])));
    }
    for split in last_bindings::<i32>() {
        assert_eq!(split(&input), Some((&20, &[10][..])));
    }
}

#[test]
fn documented_example_and_exact_generic_signatures() {
    let input = [0, 1, 2];
    check_places(&input, Some((&input[0], &input[1..3])), Some((&input[2], &input[0..2])));
    for split in first_bindings::<i32>() {
        assert_eq!(split(&input), Some((&0, &[1, 2][..])));
    }
    for split in last_bindings::<i32>() {
        assert_eq!(split(&input), Some((&2, &[0, 1][..])));
    }
    assert_eq!(input, [0, 1, 2]);
}

#[test]
fn complete_ordered_remainders_are_neither_shortened_nor_reordered() {
    for input in [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [90, 0, 255, 7, 12]] {
        let before = input;
        check_places(&input, Some((&input[0], &input[1..5])), Some((&input[4], &input[0..4])));
        for split in first_bindings::<i32>() {
            assert_eq!(split(&input), Some((&before[0], &before[1..5])));
        }
        for split in last_bindings::<i32>() {
            assert_eq!(split(&input), Some((&before[4], &before[0..4])));
        }
        assert_eq!(input, before);
    }
}

#[test]
fn repeated_values_do_not_substitute_for_places() {
    let input = [7, 7, 7, 7];
    check_places(&input, Some((&input[0], &input[1..4])), Some((&input[3], &input[0..3])));
    assert_eq!(input, [7, 7, 7, 7]);
}

#[test]
fn subslices_keep_the_original_allocation_and_frame() {
    let input = [91, 10, 40, 30, 92];
    let before = input;
    check_places(&input[1..4], Some((&input[1], &input[2..4])), Some((&input[3], &input[1..3])));
    check_places(&input[2..3], Some((&input[2], &input[3..3])), Some((&input[2], &input[2..2])));
    for empty in [&input[..0], &input[2..2], &input[5..]] {
        check_places(empty, None, None);
    }
    assert_eq!(input, before);
}

#[test]
fn zero_sized_elements_preserve_variants_and_remainder_lengths() {
    struct Zst;
    let empty: [Zst; 0] = [];
    let singleton = [Zst];
    let multiple = [Zst, Zst, Zst];
    check_places(&empty, None, None);
    check_places(
        &singleton, Some((&singleton[0], &singleton[1..1])),
        Some((&singleton[0], &singleton[0..0])),
    );
    check_places(
        &multiple, Some((&multiple[0], &multiple[1..3])),
        Some((&multiple[2], &multiple[0..2])),
    );
}

#[test]
fn maximum_length_legal_zero_sized_slice() {
    let input: &[()] = &[(); usize::MAX];
    assert_eq!(input.len(), usize::MAX);
    check_places(
        input, Some((&input[0], &input[1..])),
        Some((&input[usize::MAX - 1], &input[..usize::MAX - 1])),
    );
}

#[test]
fn unconstrained_non_copy_elements_keep_all_values() {
    struct Opaque {
        number: u32,
        text: String,
    }
    let empty: [Opaque; 0] = [];
    let singleton = [Opaque { number: 17, text: String::from("only") }];
    let input = [
        Opaque { number: 10, text: String::from("first") },
        Opaque { number: 40, text: String::from("middle") },
        Opaque { number: 30, text: String::from("last") },
    ];
    check_places(&empty, None, None);
    check_places(
        &singleton, Some((&singleton[0], &singleton[1..1])),
        Some((&singleton[0], &singleton[0..0])),
    );
    check_places(&input, Some((&input[0], &input[1..3])), Some((&input[2], &input[0..2])));
    for split in first_bindings::<Opaque>() {
        let (first, rest) = split(&input).unwrap();
        assert_eq!((first.number, first.text.as_str()), (10, "first"));
        assert_eq!(rest.iter().map(|x| (x.number, x.text.as_str())).collect::<Vec<_>>(),
                   [(40, "middle"), (30, "last")]);
    }
    for split in last_bindings::<Opaque>() {
        let (last, rest) = split(&input).unwrap();
        assert_eq!((last.number, last.text.as_str()), (30, "last"));
        assert_eq!(rest.iter().map(|x| (x.number, x.text.as_str())).collect::<Vec<_>>(),
                   [(10, "first"), (40, "middle")]);
    }
    assert_eq!((singleton[0].number, singleton[0].text.as_str()), (17, "only"));
    assert_eq!(input.iter().map(|x| (x.number, x.text.as_str())).collect::<Vec<_>>(),
               [(10, "first"), (40, "middle"), (30, "last")]);
}

#[test]
fn non_static_elements_borrow_local_owners() {
    struct Borrowed<'a>(&'a str);
    let owners = [String::from("local first"), String::from("local middle"), String::from("local last")];
    let input = [Borrowed(&owners[0]), Borrowed(&owners[1]), Borrowed(&owners[2])];
    check_places(&input, Some((&input[0], &input[1..3])), Some((&input[2], &input[0..2])));
    for split in first_bindings::<Borrowed<'_>>() {
        let (first, rest) = split(&input).unwrap();
        assert_eq!(first.0, "local first");
        assert_eq!(rest.iter().map(|x| x.0).collect::<Vec<_>>(), ["local middle", "local last"]);
    }
    for split in last_bindings::<Borrowed<'_>>() {
        let (last, rest) = split(&input).unwrap();
        assert_eq!(last.0, "local last");
        assert_eq!(rest.iter().map(|x| x.0).collect::<Vec<_>>(), ["local first", "local middle"]);
    }
    assert_eq!(owners, ["local first", "local middle", "local last"]);
}

#[test]
fn legal_empty_uninhabited_elements() {
    enum Never {}
    let input: [Never; 0] = [];
    check_places(&input, None, None);
    const RESULTS: [Option<(&Never, &[Never])>; 6] = [
        original::split_first(&[]), adopted::split_first(&[]), <[Never]>::split_first(&[]),
        original::split_last(&[]), adopted::split_last(&[]), <[Never]>::split_last(&[]),
    ];
    for result in RESULTS {
        assert!(result.is_none());
    }
}

#[test]
fn observations_do_not_write_move_or_drop_elements() {
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
            check_places(&input, Some((&input[0], &input[1..3])), Some((&input[2], &input[0..2])));
            assert_eq!(drops.get(), 0);
            for (element, expected) in input.iter().zip([10, 40, 30]) {
                assert_eq!(element.value.get(), expected);
            }
        }
    }
    assert_eq!(drops.get(), 3);
}

#[test]
fn split_first_calls_remain_stable_const() {
    const RESULTS: [Option<(&i32, &[i32])>; 12] = [
        original::split_first(&[]), adopted::split_first(&[]), <[i32]>::split_first(&[]),
        original::split_first(&[17]), adopted::split_first(&[17]), <[i32]>::split_first(&[17]),
        original::split_first(&[10, 20]), adopted::split_first(&[10, 20]), <[i32]>::split_first(&[10, 20]),
        original::split_first(&[0, 1, 2]), adopted::split_first(&[0, 1, 2]),
        <[i32]>::split_first(&[0, 1, 2]),
    ];
    assert_eq!(RESULTS, [
        None, None, None,
        Some((&17, &[][..])), Some((&17, &[][..])), Some((&17, &[][..])),
        Some((&10, &[20][..])), Some((&10, &[20][..])), Some((&10, &[20][..])),
        Some((&0, &[1, 2][..])), Some((&0, &[1, 2][..])), Some((&0, &[1, 2][..])),
    ]);
}

#[test]
fn split_last_calls_remain_stable_const() {
    const RESULTS: [Option<(&i32, &[i32])>; 12] = [
        original::split_last(&[]), adopted::split_last(&[]), <[i32]>::split_last(&[]),
        original::split_last(&[17]), adopted::split_last(&[17]), <[i32]>::split_last(&[17]),
        original::split_last(&[10, 20]), adopted::split_last(&[10, 20]), <[i32]>::split_last(&[10, 20]),
        original::split_last(&[0, 1, 2]), adopted::split_last(&[0, 1, 2]),
        <[i32]>::split_last(&[0, 1, 2]),
    ];
    assert_eq!(RESULTS, [
        None, None, None,
        Some((&17, &[][..])), Some((&17, &[][..])), Some((&17, &[][..])),
        Some((&20, &[10][..])), Some((&20, &[10][..])), Some((&20, &[10][..])),
        Some((&2, &[0, 1][..])), Some((&2, &[0, 1][..])), Some((&2, &[0, 1][..])),
    ]);
}
