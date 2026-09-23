mod source {
    include!(env!("SLICE_SINGLETON_SOURCE"));
}

struct NoTraits(String);
struct Borrowed<'a>(&'a str);
struct ZeroSized;

#[repr(align(64))]
struct AlignedZeroSized;

struct DropTracked<'a> {
    drops: &'a core::cell::Cell<usize>,
    value: String,
}

impl Drop for DropTracked<'_> {
    fn drop(&mut self) {
        self.drops.set(self.drops.get() + 1);
    }
}

fn shared_bindings<T>() -> [for<'a> fn(&'a T) -> &'a [T]; 2] {
    [source::from_ref::<T>, core::slice::from_ref::<T>]
}

fn mutable_bindings<T>() -> [for<'a> fn(&'a mut T) -> &'a mut [T]; 2] {
    [source::from_mut::<T>, core::slice::from_mut::<T>]
}

fn check_shared<T>(input: &T) {
    for from_ref in shared_bindings::<T>() {
        let view: &[T] = from_ref(input);
        assert_eq!(view.len(), 1);
        assert!(core::ptr::eq(view.as_ptr(), input));
        assert!(core::ptr::eq(&view[0], input));
    }
}

fn check_mutable<T>(input: &mut T) {
    for from_mut in mutable_bindings::<T>() {
        let address = core::ptr::from_mut(&mut *input);
        let view: &mut [T] = from_mut(input);
        assert_eq!(view.len(), 1);
        assert_eq!(view.as_mut_ptr(), address);
        assert!(core::ptr::eq(&view[0], address));
    }
}

#[test]
fn one_argument_and_exact_shared_slice_result() {
    let input = 37u8;
    check_shared(&input);
    for from_ref in shared_bindings::<u8>() {
        let view: &[u8] = from_ref(&input);
        assert_eq!(view, &[37]);
    }
}

#[test]
fn one_argument_and_exact_mutable_slice_result() {
    let mut input = 37u8;
    check_mutable(&mut input);
    for from_mut in mutable_bindings::<u8>() {
        let view: &mut [u8] = from_mut(&mut input);
        assert_eq!(view, &[37]);
    }
}

#[test]
fn shared_element_content_and_address_without_copy() {
    let input = NoTraits(String::from("original allocation"));
    let allocation = input.0.as_ptr();
    check_shared(&input);
    for from_ref in shared_bindings::<NoTraits>() {
        let view = from_ref(&input);
        assert_eq!(view[0].0, "original allocation");
        assert_eq!(view[0].0.as_ptr(), allocation);
        assert!(core::ptr::eq(&view[0], &input));
    }
}

#[test]
fn mutable_writes_reach_original_input() {
    for from_mut in mutable_bindings::<u32>() {
        let mut input = 17;
        let address = core::ptr::from_mut(&mut input);
        let view = from_mut(&mut input);
        assert_eq!(view.len(), 1);
        assert_eq!(view.as_mut_ptr(), address);
        view[0] = 91;
        assert_eq!(input, 91);
    }
}

#[test]
fn non_copy_non_default_non_eq_elements() {
    let mut input = NoTraits(String::from("non-Copy"));
    check_shared(&input);
    check_mutable(&mut input);
    for from_mut in mutable_bindings::<NoTraits>() {
        let view = from_mut(&mut input);
        view[0].0.push('!');
    }
    assert_eq!(input.0, "non-Copy!!");
}

#[test]
fn borrowed_elements_and_inputs_need_not_be_static() {
    let first = String::from("first local");
    let second = String::from("second local");
    for from_ref in shared_bindings::<Borrowed<'_>>() {
        let input = Borrowed(&first);
        let view = from_ref(&input);
        assert_eq!(view.len(), 1);
        assert!(core::ptr::eq(&view[0], &input));
        assert_eq!(view[0].0, first.as_str());
    }
    for from_mut in mutable_bindings::<Borrowed<'_>>() {
        let mut input = Borrowed(&first);
        let view = from_mut(&mut input);
        assert_eq!(view.len(), 1);
        view[0].0 = &second;
        assert_eq!(input.0, second.as_str());
    }
}

#[test]
fn zero_sized_non_copy_elements_still_have_length_one() {
    assert_eq!(core::mem::size_of::<ZeroSized>(), 0);
    let mut input = ZeroSized;
    check_shared(&input);
    check_mutable(&mut input);
}

#[test]
fn aligned_zero_sized_elements_preserve_address() {
    assert_eq!(core::mem::size_of::<AlignedZeroSized>(), 0);
    assert_eq!(core::mem::align_of::<AlignedZeroSized>(), 64);
    let mut input = AlignedZeroSized;
    check_shared(&input);
    check_mutable(&mut input);
    for from_ref in shared_bindings::<AlignedZeroSized>() {
        assert_eq!(from_ref(&input).as_ptr() as usize % 64, 0);
    }
}

#[test]
fn shared_views_observe_interior_mutation_without_copy() {
    for from_ref in shared_bindings::<core::cell::Cell<u32>>() {
        let input = core::cell::Cell::new(3);
        let view = from_ref(&input);
        view[0].set(7);
        assert_eq!(input.get(), 7);
        input.set(11);
        assert_eq!(view[0].get(), 11);
    }
}

#[test]
fn droppable_elements_are_neither_copied_nor_dropped() {
    let drops = core::cell::Cell::new(0);
    let mut input = DropTracked {
        drops: &drops,
        value: String::from("owned"),
    };
    check_shared(&input);
    check_mutable(&mut input);
    for from_ref in shared_bindings::<DropTracked<'_>>() {
        assert_eq!(from_ref(&input)[0].value, "owned");
        assert_eq!(drops.get(), 0);
    }
    for from_mut in mutable_bindings::<DropTracked<'_>>() {
        from_mut(&mut input)[0].value.push('!');
        assert_eq!(drops.get(), 0);
    }
    assert_eq!(input.value, "owned!!");
    drop(input);
    assert_eq!(drops.get(), 1);
}

#[test]
fn references_to_unsized_values_are_sized_elements() {
    let text = String::from("borrowed str");
    let mut reference: &str = &text;
    check_shared(&reference);
    check_mutable(&mut reference);
    let data = [1u8, 2, 3];
    let mut reference: &[u8] = &data;
    check_shared(&reference);
    check_mutable(&mut reference);
}

#[test]
fn arrays_including_empty_arrays_are_single_elements() {
    let mut input = [2u8, 4, 6];
    check_shared(&input);
    check_mutable(&mut input);
    for from_mut in mutable_bindings::<[u8; 3]>() {
        let view = from_mut(&mut input);
        assert_eq!(view.len(), 1);
        assert_eq!(view[0], [2, 4, 6]);
        view[0][1] = 9;
        assert_eq!(input, [2, 9, 6]);
        input[1] = 4;
    }
    let mut empty: [NoTraits; 0] = [];
    check_shared(&empty);
    check_mutable(&mut empty);
}

#[test]
fn mutable_reborrows_are_legal() {
    for from_mut in mutable_bindings::<u8>() {
        let mut input = 1;
        let view = from_mut(&mut input);
        {
            let element: &mut u8 = &mut view[0];
            *element = 2;
        }
        view[0] += 3;
        assert_eq!(input, 5);
    }
}

#[test]
fn shared_views_can_overlap_and_accept_mutable_input() {
    for from_ref in shared_bindings::<u8>() {
        let mut input = 5;
        {
            let view = from_ref(&mut input);
            assert_eq!(view, &[5]);
        }
        let first = from_ref(&input);
        let second = from_ref(&input);
        assert!(core::ptr::eq(first, second));
        assert_eq!(first, &[5]);
        assert_eq!(second, &[5]);
        input = 8;
        assert_eq!(input, 8);
    }
}

#[test]
fn shared_calls_are_stable_const() {
    const INPUT: u16 = 41;
    const SOURCE: &[u16] = source::from_ref(&INPUT);
    const PUBLIC: &[u16] = core::slice::from_ref(&INPUT);
    assert_eq!(SOURCE.len(), 1);
    assert_eq!(PUBLIC.len(), 1);
    assert_eq!(SOURCE[0], 41);
    assert_eq!(PUBLIC[0], 41);
}

#[test]
fn mutable_calls_are_stable_const() {
    const SOURCE: (usize, u16) = {
        let mut input = 41;
        let view = source::from_mut(&mut input);
        let length = view.len();
        view[0] += 1;
        (length, input)
    };
    const PUBLIC: (usize, u16) = {
        let mut input = 41;
        let view = core::slice::from_mut(&mut input);
        let length = view.len();
        view[0] += 1;
        (length, input)
    };
    assert_eq!(SOURCE, (1, 42));
    assert_eq!(PUBLIC, (1, 42));
}
