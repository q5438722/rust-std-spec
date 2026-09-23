use std::borrow::Cow;
use std::ptr;

extern crate vec_specs as _;

struct Token<'a> {
    ordinal: u32,
    text: &'a str,
}

impl Clone for Token<'_> {
    fn clone(&self) -> Self {
        panic!("Cow::from must not clone an element");
    }
}

struct Zst;

impl Clone for Zst {
    fn clone(&self) -> Self {
        panic!("Cow::from must not clone a zero-sized element");
    }
}

fn exact_signatures<'a, T: Clone, const N: usize>(_: &'a [T]) {
    let _: fn(&'a [T]) -> Cow<'a, [T]> = from_slice::from_slice::<T>;
    let _: fn(&'a [T; N]) -> Cow<'a, [T]> = from_array::from_array::<T, N>;
    let _: fn(Vec<T>) -> Cow<'a, [T]> = from_vec::from_vec::<T>;
    let _: fn(&'a Vec<T>) -> Cow<'a, [T]> = from_vec_ref::from_vec_ref::<T>;

    let _: fn(&'a [T]) -> Cow<'a, [T]> = <Cow<'a, [T]> as From<&'a [T]>>::from;
    let _: fn(&'a [T; N]) -> Cow<'a, [T]> = <Cow<'a, [T]> as From<&'a [T; N]>>::from;
    let _: fn(Vec<T>) -> Cow<'a, [T]> = <Cow<'a, [T]> as From<Vec<T>>>::from;
    let _: fn(&'a Vec<T>) -> Cow<'a, [T]> = <Cow<'a, [T]> as From<&'a Vec<T>>>::from;
}

// Address/capacity checks supplement the Seq contracts; they are not a memory proof.
fn borrowed_storage<T: Clone>(result: &Cow<'_, [T]>, original: &[T]) {
    let Cow::Borrowed(payload) = result else {
        panic!("a borrowed input became Owned");
    };
    assert_eq!(payload.len(), original.len());
    assert!(ptr::eq(payload.as_ptr(), original.as_ptr()));
    for index in 0..original.len() {
        assert!(ptr::eq(&payload[index], &original[index]));
    }
}

fn check_slice<'a, T: Clone>(source: &'a [T], inspect: impl Fn(&[T])) {
    exact_signatures::<T, 0>(source);
    let conversions: [fn(&'a [T]) -> Cow<'a, [T]>; 2] = [
        from_slice::from_slice,
        <Cow<'a, [T]> as From<&'a [T]>>::from,
    ];
    for convert in conversions {
        let result = convert(source);
        borrowed_storage(&result, source);
        inspect(&result);
    }
}

fn check_array<'a, T: Clone, const N: usize>(source: &'a [T; N], inspect: impl Fn(&[T])) {
    exact_signatures::<T, N>(source);
    let conversions: [fn(&'a [T; N]) -> Cow<'a, [T]>; 2] = [
        from_array::from_array,
        <Cow<'a, [T]> as From<&'a [T; N]>>::from,
    ];
    for convert in conversions {
        let result = convert(source);
        borrowed_storage(&result, source);
        inspect(&result);
    }
}

fn check_vec_ref<'a, T: Clone>(source: &'a Vec<T>, inspect: impl Fn(&[T])) {
    exact_signatures::<T, 0>(source);
    let conversions: [fn(&'a Vec<T>) -> Cow<'a, [T]>; 2] = [
        from_vec_ref::from_vec_ref,
        <Cow<'a, [T]> as From<&'a Vec<T>>>::from,
    ];
    for convert in conversions {
        let result = convert(source);
        borrowed_storage(&result, source);
        inspect(&result);
    }
}

fn check_owned<'a, T: Clone>(
    source: Vec<T>,
    convert: fn(Vec<T>) -> Cow<'a, [T]>,
    inspect: impl Fn(&[T]),
) {
    exact_signatures::<T, 0>(&source);
    let length = source.len();
    let capacity = source.capacity();
    let allocation = source.as_ptr();
    let result = convert(source);
    let Cow::Owned(payload) = result else {
        panic!("a moved Vec became Borrowed");
    };
    assert_eq!(payload.len(), length);
    assert_eq!(payload.capacity(), capacity);
    assert!(ptr::eq(payload.as_ptr(), allocation));
    inspect(&payload);
}

fn tokens(text: &str) -> [Token<'_>; 4] {
    [
        Token { ordinal: 9, text },
        Token { ordinal: 1, text },
        Token { ordinal: 9, text },
        Token { ordinal: 4, text },
    ]
}

fn token_contents(actual: &[Token<'_>], text: &str) {
    assert_eq!(actual.len(), 4);
    for (index, ordinal) in [9, 1, 9, 4].into_iter().enumerate() {
        assert_eq!(actual[index].ordinal, ordinal);
        assert_eq!(actual[index].text, text);
    }
}

#[test]
fn slices_preserve_variant_storage_and_every_element() {
    let text = String::from("non-static, Clone but not Copy/Eq/PartialEq/View");
    let data = tokens(&text);
    check_slice(&data[..0], |items| assert!(items.is_empty()));
    check_slice(&data, |items| token_contents(items, &text));
    check_slice(&data[1..3], |items| {
        assert_eq!(items.len(), 2);
        assert_eq!(items[0].ordinal, 1);
        assert_eq!(items[1].ordinal, 9);
        for item in items {
            assert_eq!(item.text, text);
        }
    });
}

#[test]
fn arrays_include_zero_and_nonzero_const_lengths() {
    let text = String::from("borrowed array elements");
    let empty: [Token<'_>; 0] = [];
    check_array(&empty, |items| assert!(items.is_empty()));
    let data = tokens(&text);
    check_array(&data, |items| token_contents(items, &text));
}

#[test]
fn vec_references_include_empty_reserved_and_nonempty_storage() {
    let text = String::from("borrowed Vec elements");
    for capacity in [0, 19] {
        let data: Vec<Token<'_>> = Vec::with_capacity(capacity);
        let original_capacity = data.capacity();
        check_vec_ref(&data, |items| assert!(items.is_empty()));
        assert_eq!(data.capacity(), original_capacity);
    }
    let mut data = Vec::with_capacity(23);
    data.extend(tokens(&text));
    check_vec_ref(&data, |items| token_contents(items, &text));
    token_contents(&data, &text);
}

#[test]
fn moved_vecs_reuse_allocation_and_capacity_without_cloning() {
    let text = String::from("owned Vec with borrowed elements");
    for capacity in [0, 19] {
        check_owned(
            Vec::<Token<'_>>::with_capacity(capacity),
            from_vec::from_vec,
            |items| assert!(items.is_empty()),
        );
        check_owned(
            Vec::<Token<'_>>::with_capacity(capacity),
            <Cow<'_, [Token<'_>]> as From<Vec<Token<'_>>>>::from,
            |items| assert!(items.is_empty()),
        );
    }
    let make_vec = || {
        let mut data = Vec::with_capacity(23);
        data.extend(tokens(&text));
        data
    };
    check_owned(make_vec(), from_vec::from_vec, |items| token_contents(items, &text));
    check_owned(
        make_vec(),
        <Cow<'_, [Token<'_>]> as From<Vec<Token<'_>>>>::from,
        |items| token_contents(items, &text),
    );
}

#[test]
fn zero_sized_clone_only_elements_work_for_all_four_conversions() {
    assert_eq!(std::mem::size_of::<Zst>(), 0);
    let empty: [Zst; 0] = [];
    let data = [Zst, Zst, Zst];
    for slice in [&empty[..], &data[..]] {
        check_slice(slice, |items| assert_eq!(items.len(), slice.len()));
    }
    check_array(&empty, |items| assert!(items.is_empty()));
    check_array(&data, |items| assert_eq!(items.len(), 3));
    check_vec_ref(&Vec::<Zst>::new(), |items| assert!(items.is_empty()));
    check_vec_ref(&vec![Zst, Zst, Zst], |items| assert_eq!(items.len(), 3));
    check_owned(Vec::<Zst>::new(), from_vec::from_vec, |items| assert!(items.is_empty()));
    check_owned(
        Vec::<Zst>::new(),
        <Cow<'_, [Zst]> as From<Vec<Zst>>>::from,
        |items| assert!(items.is_empty()),
    );
    check_owned(vec![Zst, Zst, Zst], from_vec::from_vec, |items| assert_eq!(items.len(), 3));
    check_owned(
        vec![Zst, Zst, Zst],
        <Cow<'_, [Zst]> as From<Vec<Zst>>>::from,
        |items| assert_eq!(items.len(), 3),
    );
}

#[test]
fn owned_results_outlive_vec_binding_but_not_borrowed_elements() {
    fn local<'a>(text: &'a str) {
        let copy: Cow<'a, [Token<'a>]> = {
            let source = Vec::from(tokens(text));
            from_vec::from_vec(source)
        };
        let original: Cow<'a, [Token<'a>]> = {
            let source = Vec::from(tokens(text));
            <Cow<'a, [Token<'a>]> as From<Vec<Token<'a>>>>::from(source)
        };
        assert!(matches!(copy, Cow::Owned(_)));
        assert!(matches!(original, Cow::Owned(_)));
        token_contents(&copy, text);
        token_contents(&original, text);
    }
    let text = String::from("this element lifetime is not static");
    local(&text);
}
