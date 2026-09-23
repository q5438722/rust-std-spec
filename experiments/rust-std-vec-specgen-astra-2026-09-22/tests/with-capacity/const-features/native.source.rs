use source_with_capacity::with_capacity as source;

struct Element<'a> {
    value: &'a i32,
}

fn exact_signatures<T>() {
    let _: fn(usize) -> Vec<T> = Vec::<T>::with_capacity;
    let _: fn(usize) -> Vec<T> = source::<T>;
}

fn fill_borrowed<'a>(construct: fn(usize) -> Vec<Element<'a>>, values: &'a [i32]) {
    for requested in [0, 1, 37] {
        let mut vec = construct(requested);
        assert_eq!(vec.len(), 0);
        assert!(vec.as_slice().is_empty());
        assert!(vec.capacity() >= requested);
        let capacity = vec.capacity();
        let pointer = vec.as_ptr();
        for index in 0..requested {
            vec.push(Element { value: &values[index % values.len()] });
            assert_eq!(vec.capacity(), capacity);
            assert_eq!(vec.as_ptr(), pointer);
        }
        assert_eq!(vec.len(), requested);
        for (index, element) in vec.iter().enumerate() {
            assert!(std::ptr::eq(element.value, &values[index % values.len()]));
            assert_eq!(*element.value, values[index % values.len()]);
        }
    }
}

fn capacity_overflow<T>(construct: fn(usize) -> Vec<T>, requested: usize) {
    match std::panic::catch_unwind(|| construct(requested)) {
        Ok(_) => panic!("a byte-overflowing request returned normally"),
        Err(payload) => {
            let message = payload.downcast_ref::<&str>().expect("literal capacity overflow panic");
            assert_eq!(*message, "capacity overflow");
        }
    }
}

#[test]
fn precise_generic_signatures_and_zero_request() {
    exact_signatures::<Element<'_>>();
    for construct in [Vec::<u32>::with_capacity, source::<u32>] {
        let vec = construct(0);
        assert_eq!(vec.len(), 0);
        assert_eq!(vec.capacity(), 0);
        assert!(vec.as_slice().is_empty());
    }
}

#[test]
fn requested_capacity_keeps_borrowed_elements_in_order() {
    let values = [17, -3, 17, 5];
    fill_borrowed(Vec::with_capacity, &values);
    fill_borrowed(source, &values);
}

#[test]
fn zst_capacity_is_maximum_even_for_maximum_request() {
    #[repr(align(64))]
    struct Zst;

    exact_signatures::<Zst>();
    assert_eq!(std::mem::size_of::<Zst>(), 0);
    for construct in [Vec::<Zst>::with_capacity, source::<Zst>] {
        for requested in [0, 1, 37, usize::MAX] {
            let mut vec = construct(requested);
            assert_eq!(vec.len(), 0);
            assert_eq!(vec.capacity(), usize::MAX);
            for _ in 0..7 {
                vec.push(Zst);
            }
            assert_eq!(vec.len(), 7);
            assert_eq!(vec.capacity(), usize::MAX);
        }
    }
}

#[test]
fn byte_limit_is_not_an_element_count_limit() {
    let requested = isize::MAX as usize / std::mem::size_of::<u16>() + 1;
    assert!(requested <= isize::MAX as usize);
    assert!(requested.checked_mul(std::mem::size_of::<u16>()).unwrap() > isize::MAX as usize);
    for construct in [Vec::<u16>::with_capacity, source::<u16>] {
        capacity_overflow(construct, requested);
    }
    for construct in [Vec::<u8>::with_capacity, source::<u8>] {
        capacity_overflow(construct, isize::MAX as usize + 1);
    }
}

#[test]
fn multiplication_overflow_is_rejected_before_allocation() {
    assert!(usize::MAX.checked_mul(std::mem::size_of::<u16>()).is_none());
    for construct in [Vec::<u16>::with_capacity, source::<u16>] {
        capacity_overflow(construct, usize::MAX);
    }
}
