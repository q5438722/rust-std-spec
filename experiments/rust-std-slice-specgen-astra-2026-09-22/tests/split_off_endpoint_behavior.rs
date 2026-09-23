// Compare authority originals, adopted current formal bodies, and public APIs.
include!(env!("SLICE_SPLIT_OFF_ENDPOINTS_SOURCE"));

type SplitOff<T> = for<'a, 'b> fn(&'b mut &'a [T]) -> Option<&'a T>;

fn first_bindings<T>() -> [SplitOff<T>; 3] {
    [
        original::split_off_first::<T>,
        adopted::split_off_first::<T>,
        <[T]>::split_off_first,
    ]
}

fn last_bindings<T>() -> [SplitOff<T>; 3] {
    [
        original::split_off_last::<T>,
        adopted::split_off_last::<T>,
        <[T]>::split_off_last,
    ]
}

fn bindings<T>() -> [(SplitOff<T>, bool); 6] {
    let [original_first, adopted_first, public_first] = first_bindings::<T>();
    let [original_last, adopted_last, public_last] = last_bindings::<T>();
    [
        (original_first, false),
        (adopted_first, false),
        (public_first, false),
        (original_last, true),
        (adopted_last, true),
        (public_last, true),
    ]
}

fn check_step<'a, T>(
    split: SplitOff<T>,
    slot: &mut &'a [T],
    expected: Option<&'a T>,
    remainder: &'a [T],
) -> Option<&'a T> {
    let actual = split(slot);
    assert_eq!(slot.len(), remainder.len());
    // ZST address equality cannot establish element or empty-remainder origins.
    if core::mem::size_of::<T>() != 0 {
        assert!(core::ptr::eq(slot.as_ptr(), remainder.as_ptr()));
        for (value, expected) in slot.iter().zip(remainder) {
            assert!(core::ptr::eq(value, expected));
        }
    }
    match (actual, expected) {
        (None, None) => {}
        (Some(value), Some(expected)) => {
            if core::mem::size_of::<T>() != 0 {
                assert!(core::ptr::eq(value, expected));
            }
        }
        _ => panic!("returned variant differs from the documented expectation"),
    }
    actual
}

fn check_values<T: core::fmt::Debug + PartialEq>(input: &[T]) {
    for (split, last) in bindings::<T>() {
        let mut slot = input;
        let (expected, remainder) = if input.is_empty() {
            (None, input)
        } else if last {
            (Some(&input[input.len() - 1]), &input[..input.len() - 1])
        } else {
            (Some(&input[0]), &input[1..])
        };
        assert_eq!(check_step(split, &mut slot, expected, remainder), expected);
        assert_eq!(slot, remainder);
    }
}

#[test]
fn empty_slices_leave_slots_unchanged() {
    let empty: [u32; 0] = [];
    check_values(&empty);
    let input = [91, 92, 93];
    for offset in 0..=input.len() {
        check_values(&input[offset..offset]);
    }
    assert_eq!(input, [91, 92, 93]);
}

#[test]
fn singleton_empty_remainders_keep_distinct_origins() {
    let input = [17u32];
    for split in first_bindings::<u32>() {
        let mut slot = &input[..];
        assert_eq!(check_step(split, &mut slot, Some(&input[0]), &input[1..1]), Some(&17));
        assert_eq!(slot, &[]);
    }
    for split in last_bindings::<u32>() {
        let mut slot = &input[..];
        assert_eq!(check_step(split, &mut slot, Some(&input[0]), &input[0..0]), Some(&17));
        assert_eq!(slot, &[]);
    }
    assert_ne!(input[1..1].as_ptr(), input[0..0].as_ptr());
    assert_eq!(input, [17]);
}

#[test]
fn two_elements_update_the_complete_slot() {
    let input = [10, 20];
    check_values(&input);
    assert_eq!(input, [10, 20]);
}

#[test]
fn documented_character_examples() {
    let input = ['a', 'b', 'c'];
    for split in first_bindings::<char>() {
        let mut slot = &input[..];
        let first = split(&mut slot).unwrap();
        assert_eq!(slot, &['b', 'c']);
        assert_eq!(*first, 'a');
    }
    for split in last_bindings::<char>() {
        let mut slot = &input[..];
        let last = split(&mut slot).unwrap();
        assert_eq!(slot, &['a', 'b']);
        assert_eq!(*last, 'c');
    }
    check_values(&input);
    assert_eq!(input, ['a', 'b', 'c']);
}

#[test]
fn complete_ordered_remainders_are_not_shortened_or_reordered() {
    for input in [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [90, 0, 255, 7, 12]] {
        let before = input;
        check_values(&input);
        assert_eq!(input, before);
    }
}

#[test]
fn repeated_values_do_not_substitute_for_places() {
    let input = [7, 7, 7, 7];
    check_values(&input);
    assert_eq!(input, [7, 7, 7, 7]);
}

#[test]
fn outer_subslice_frames_and_underlying_input_are_unchanged() {
    let input = [91, 10, 40, 30, 92];
    let before = input;
    check_values(&input[1..4]);
    check_values(&input[2..3]);
    check_values(&input[1..3]);
    for offset in 0..=input.len() {
        check_values(&input[offset..offset]);
    }
    assert_eq!(input, before);
}

#[test]
fn repeated_first_calls_keep_all_earlier_results_live() {
    let input = [10, 40, 30, 20, 50];
    for split in first_bindings::<i32>() {
        let mut slot = &input[..];
        let mut retained = Vec::new();
        for index in 0..input.len() {
            retained.push(check_step(
                split, &mut slot, Some(&input[index]), &input[index + 1..],
            ).unwrap());
            assert_eq!(slot, &input[index + 1..]);
            assert_eq!(
                retained.iter().map(|value| **value).collect::<Vec<_>>(),
                input[..=index].to_vec(),
            );
        }
        for _ in 0..3 {
            assert_eq!(check_step(split, &mut slot, None, &input[input.len()..]), None);
        }
        assert_eq!(retained.iter().map(|value| **value).collect::<Vec<_>>(), input);
    }
    assert_eq!(input, [10, 40, 30, 20, 50]);
}

#[test]
fn repeated_last_calls_keep_all_earlier_results_live() {
    let input = [10, 40, 30, 20, 50];
    for split in last_bindings::<i32>() {
        let mut slot = &input[..];
        let mut retained = Vec::new();
        for index in (0..input.len()).rev() {
            retained.push(check_step(
                split, &mut slot, Some(&input[index]), &input[..index],
            ).unwrap());
            assert_eq!(slot, &input[..index]);
            assert_eq!(
                retained.iter().map(|value| **value).collect::<Vec<_>>(),
                input[index..].iter().rev().copied().collect::<Vec<_>>(),
            );
        }
        for _ in 0..3 {
            assert_eq!(check_step(split, &mut slot, None, &input[..0]), None);
        }
        assert_eq!(
            retained.iter().map(|value| **value).collect::<Vec<_>>(),
            [50, 20, 30, 40, 10],
        );
    }
    assert_eq!(input, [10, 40, 30, 20, 50]);
}

#[test]
fn alternating_calls_preserve_every_return_and_whole_remainder() {
    let input = [91, 10, 40, 30, 20, 50, 92];
    let first = first_bindings::<i32>();
    let last = last_bindings::<i32>();
    for (first, last) in [
        (first[0], last[0]), (first[1], last[1]),
        (first[2], last[2]),
    ] {
        for schedule in [[false, true, false, true, false], [true, false, true, false, true]] {
            let mut slot = &input[1..6];
            let (mut low, mut high) = (1, 6);
            let mut retained = Vec::new();
            let mut expected = Vec::new();
            for from_last in schedule {
                let (split, index) = if from_last {
                    high -= 1;
                    (last, high)
                } else {
                    let index = low;
                    low += 1;
                    (first, index)
                };
                retained.push(check_step(
                    split, &mut slot, Some(&input[index]), &input[low..high],
                ).unwrap());
                expected.push(input[index]);
                assert_eq!(slot, &input[low..high]);
                assert_eq!(retained.iter().map(|value| **value).collect::<Vec<_>>(), expected);
                assert_eq!(input, [91, 10, 40, 30, 20, 50, 92]);
            }
            assert_eq!(check_step(first, &mut slot, None, &input[low..high]), None);
            assert_eq!(check_step(last, &mut slot, None, &input[low..high]), None);
            assert_eq!(retained.iter().map(|value| **value).collect::<Vec<_>>(), expected);
        }
    }
}

#[test]
fn exhausted_repeated_calls_preserve_the_empty_slot_origin() {
    let input = [10u32, 20, 30];
    for (split, last) in bindings::<u32>() {
        let mut slot = &input[..];
        let mut retained = Vec::new();
        for step in 0..input.len() {
            let index = if last { input.len() - 1 - step } else { step };
            let remainder = if last { &input[..index] } else { &input[index + 1..] };
            retained.push(check_step(split, &mut slot, Some(&input[index]), remainder).unwrap());
            assert_eq!(slot, remainder);
        }
        let empty = if last { &input[..0] } else { &input[input.len()..] };
        for _ in 0..3 {
            for (next, _) in bindings::<u32>() {
                assert_eq!(check_step(next, &mut slot, None, empty), None);
            }
        }
        let expected = if last { [30, 20, 10] } else { [10, 20, 30] };
        assert_eq!(retained.iter().map(|value| **value).collect::<Vec<_>>(), expected);
    }
    assert_eq!(input, [10, 20, 30]);
}

#[test]
fn first_result_survives_arbitrary_slot_reassignment() {
    let input = [10, 20, 30];
    let replacement = [-7, 80];
    for split in first_bindings::<i32>() {
        let mut slot = &input[..];
        let retained = check_step(split, &mut slot, Some(&input[0]), &input[1..]).unwrap();
        slot = &replacement[..];
        assert_eq!(*retained, 10);
        assert_eq!(slot, &replacement);
        let next = check_step(split, &mut slot, Some(&replacement[0]), &replacement[1..]).unwrap();
        slot = &input[1..1];
        assert_eq!((*retained, *next), (10, -7));
        assert_eq!(slot, &[]);
    }
    assert_eq!(input, [10, 20, 30]);
    assert_eq!(replacement, [-7, 80]);
}

#[test]
fn last_result_survives_arbitrary_slot_reassignment() {
    let input = [10, 20, 30];
    let replacement = [-7, 80];
    for split in last_bindings::<i32>() {
        let mut slot = &input[..];
        let retained = check_step(split, &mut slot, Some(&input[2]), &input[..2]).unwrap();
        slot = &replacement[..];
        assert_eq!(*retained, 30);
        assert_eq!(slot, &replacement);
        let next = check_step(split, &mut slot, Some(&replacement[1]), &replacement[..1]).unwrap();
        slot = &input[1..2];
        assert_eq!((*retained, *next), (30, 80));
        assert_eq!(slot, &[20]);
    }
    assert_eq!(input, [10, 20, 30]);
    assert_eq!(replacement, [-7, 80]);
}

#[test]
fn positive_lifetime_probe_result_outlives_the_outer_slot_and_borrow() {
    fn retain<'a, T>(input: &'a [T], split: SplitOff<T>) -> Option<&'a T> {
        let result;
        {
            let mut slot = input;
            result = split(&mut slot);
        }
        result
    }
    let input = [String::from("local first"), String::from("local last")];
    for (split, last) in bindings::<String>() {
        let result = retain(&input, split).unwrap();
        assert_eq!(result.as_str(), if last { "local last" } else { "local first" });
    }
    assert_eq!(input, ["local first", "local last"]);
}

#[test]
fn unconstrained_non_copy_elements_keep_all_values_and_frame() {
    struct Opaque {
        number: u32,
        text: String,
    }
    fn values(input: &[Opaque]) -> Vec<(u32, &str)> {
        input.iter().map(|value| (value.number, value.text.as_str())).collect()
    }
    let input = [
        Opaque { number: 91, text: String::from("outside left") },
        Opaque { number: 10, text: String::from("first") },
        Opaque { number: 40, text: String::from("middle") },
        Opaque { number: 30, text: String::from("last") },
        Opaque { number: 92, text: String::from("outside right") },
    ];
    for (split, last) in bindings::<Opaque>() {
        let mut slot = &input[1..4];
        let index = if last { 3 } else { 1 };
        let remainder = if last { &input[1..3] } else { &input[2..4] };
        let result = check_step(split, &mut slot, Some(&input[index]), remainder).unwrap();
        assert_eq!(
            (result.number, result.text.as_str()),
            if last { (30, "last") } else { (10, "first") },
        );
        assert_eq!(
            values(slot),
            if last { vec![(10, "first"), (40, "middle")] } else { vec![(40, "middle"), (30, "last")] },
        );
    }
    assert_eq!(values(&input), [
        (91, "outside left"), (10, "first"), (40, "middle"), (30, "last"), (92, "outside right"),
    ]);
}

#[test]
fn non_static_elements_borrow_local_owners() {
    struct Borrowed<'a>(&'a str);
    let owners = [String::from("local first"), String::from("local middle"), String::from("local last")];
    let input = [Borrowed(&owners[0]), Borrowed(&owners[1]), Borrowed(&owners[2])];
    for (split, last) in bindings::<Borrowed<'_>>() {
        let mut slot = &input[..];
        let index = if last { 2 } else { 0 };
        let remainder = if last { &input[..2] } else { &input[1..] };
        let retained = check_step(split, &mut slot, Some(&input[index]), remainder).unwrap();
        assert_eq!(
            slot.iter().map(|value| value.0).collect::<Vec<_>>(),
            if last { vec!["local first", "local middle"] } else { vec!["local middle", "local last"] },
        );
        slot = &input[1..2];
        assert_eq!(slot[0].0, "local middle");
        assert_eq!(retained.0, if last { "local last" } else { "local first" });
    }
    assert_eq!(input.iter().map(|value| value.0).collect::<Vec<_>>(), [
        "local first", "local middle", "local last",
    ]);
    assert_eq!(owners, ["local first", "local middle", "local last"]);
}

#[test]
fn zero_sized_elements_use_variants_and_lengths_not_addresses() {
    struct Zst;
    let empty: [Zst; 0] = [];
    let singleton = [Zst];
    let multiple = [Zst, Zst, Zst, Zst];
    for input in [&empty[..], &singleton[..], &multiple[..]] {
        for (split, last) in bindings::<Zst>() {
            let mut slot = input;
            let mut retained = Vec::new();
            for step in 0..input.len() {
                let index = if last { input.len() - 1 - step } else { step };
                let remainder = if last { &input[..index] } else { &input[index + 1..] };
                retained.push(check_step(split, &mut slot, Some(&input[index]), remainder).unwrap());
                assert_eq!(slot.len(), input.len() - step - 1);
            }
            let empty = if last { &input[..0] } else { &input[input.len()..] };
            assert!(check_step(split, &mut slot, None, empty).is_none());
            assert!(check_step(split, &mut slot, None, empty).is_none());
            assert_eq!(retained.len(), input.len());
        }
    }
}

#[test]
fn maximum_length_legal_zero_sized_slice() {
    let input: &[()] = &[(); usize::MAX];
    for (split, last) in bindings::<()>() {
        let mut slot = input;
        for removed in 1..=2 {
            let index = if last { input.len() - removed } else { removed - 1 };
            let remainder = if last { &input[..index] } else { &input[removed..] };
            assert!(check_step(split, &mut slot, Some(&input[index]), remainder).is_some());
            assert_eq!(slot.len(), usize::MAX - removed);
        }
    }
    assert_eq!(input.len(), usize::MAX);
}

#[test]
fn legal_empty_uninhabited_elements() {
    enum Never {}
    let input: [Never; 0] = [];
    for (split, _) in bindings::<Never>() {
        let mut slot = &input[..];
        assert!(check_step(split, &mut slot, None, &input).is_none());
        assert!(check_step(split, &mut slot, None, &input).is_none());
        assert_eq!(slot.len(), 0);
    }
    assert_eq!(input.len(), 0);
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
        for (split, last) in bindings::<Observed<'_>>() {
            let mut slot = &input[..];
            let index = if last { 2 } else { 0 };
            let remainder = if last { &input[..2] } else { &input[1..] };
            let retained = check_step(split, &mut slot, Some(&input[index]), remainder).unwrap();
            let remaining = if last { &input[..1] } else { &input[2..] };
            let next = check_step(split, &mut slot, Some(&input[1]), remaining).unwrap();
            assert_eq!(slot.iter().map(|value| value.value.get()).collect::<Vec<_>>(),
                       if last { vec![10] } else { vec![30] });
            slot = &input[..0];
            assert_eq!(slot.len(), 0);
            assert_eq!(retained.value.get(), if last { 30 } else { 10 });
            assert_eq!(next.value.get(), 40);
            assert_eq!(drops.get(), 0);
            assert_eq!(input.iter().map(|value| value.value.get()).collect::<Vec<_>>(), [10, 40, 30]);
        }
    }
    assert_eq!(drops.get(), 3);
}
