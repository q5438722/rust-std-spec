#![feature(ptr_metadata)]

mod source {
    include!(env!("SLICE_NATIVE_SOURCE"));
}

fn check<T>(input: &[T], length: usize) {
    let len: for<'a> fn(&'a [T]) -> usize = source::len::<T>;
    let is_empty: for<'a> fn(&'a [T]) -> bool = source::is_empty::<T>;
    let first: for<'a> fn(&'a [T]) -> Option<&'a T> = source::first::<T>;
    let last: for<'a> fn(&'a [T]) -> Option<&'a T> = source::last::<T>;
    let split_first: for<'a> fn(&'a [T]) -> Option<(&'a T, &'a [T])> =
        source::split_first::<T>;
    let split_last: for<'a> fn(&'a [T]) -> Option<(&'a T, &'a [T])> =
        source::split_last::<T>;

    assert_eq!(len(input), length);
    assert_eq!(is_empty(input), length == 0);
    if length == 0 {
        assert!(first(input).is_none());
        assert!(last(input).is_none());
        assert!(split_first(input).is_none());
        assert!(split_last(input).is_none());
    } else {
        assert!(core::ptr::eq(first(input).unwrap(), &input[0]));
        assert!(core::ptr::eq(last(input).unwrap(), &input[length - 1]));
        let (head, tail) = split_first(input).unwrap();
        assert!(core::ptr::eq(head, &input[0]));
        assert!(core::ptr::eq(tail, &input[1..]));
        let (end, init) = split_last(input).unwrap();
        assert!(core::ptr::eq(end, &input[length - 1]));
        assert!(core::ptr::eq(init, &input[..length - 1]));
    }
}

#[test]
fn empty() {
    check::<u8>(&[], 0);
}

#[test]
fn singleton() {
    check(&[17], 1);
}

#[test]
fn ordered_elements() {
    check(&[10, 40, 30], 3);
    assert_eq!(source::split_first(&[0, 1, 2]), Some((&0, &[1, 2][..])));
    assert_eq!(source::split_last(&[0, 1, 2]), Some((&2, &[0, 1][..])));
}

#[test]
fn zero_sized_elements() {
    check::<()>(&[], 0);
    check(&[()], 1);
    check(&[(); 5], 5);
}

#[test]
fn non_copy_elements() {
    check::<String>(&[], 0);
    check(&[String::from("only")], 1);
    check(
        &[
            String::from("first"),
            String::from("middle"),
            String::from("last"),
        ],
        3,
    );
}

#[test]
fn non_static_elements() {
    struct Borrowed<'a>(&'a str);
    let text = String::from("borrowed");
    let input = [Borrowed(&text), Borrowed(&text)];
    check(&input, 2);
    assert_eq!(source::first(&input).unwrap().0, "borrowed");
}

#[test]
fn all_six_remain_const() {
    const INPUT: &[u8] = &[10, 40, 30];
    const LEN: usize = source::len(INPUT);
    const EMPTY: bool = source::is_empty(INPUT);
    const FIRST: Option<&u8> = source::first(INPUT);
    const LAST: Option<&u8> = source::last(INPUT);
    const SPLIT_FIRST: Option<(&u8, &[u8])> = source::split_first(INPUT);
    const SPLIT_LAST: Option<(&u8, &[u8])> = source::split_last(INPUT);
    const EMPTY_INPUT: &[u8] = &[];
    const EMPTY_LEN: usize = source::len(EMPTY_INPUT);
    const EMPTY_BOOL: bool = source::is_empty(EMPTY_INPUT);
    const EMPTY_FIRST: Option<&u8> = source::first(EMPTY_INPUT);
    const EMPTY_LAST: Option<&u8> = source::last(EMPTY_INPUT);
    const EMPTY_SPLIT_FIRST: Option<(&u8, &[u8])> = source::split_first(EMPTY_INPUT);
    const EMPTY_SPLIT_LAST: Option<(&u8, &[u8])> = source::split_last(EMPTY_INPUT);
    assert_eq!(LEN, 3);
    assert!(!EMPTY);
    assert_eq!(FIRST, Some(&10));
    assert_eq!(LAST, Some(&30));
    assert_eq!(SPLIT_FIRST, Some((&10, &[40, 30][..])));
    assert_eq!(SPLIT_LAST, Some((&30, &[10, 40][..])));
    assert_eq!(EMPTY_LEN, 0);
    assert!(EMPTY_BOOL);
    assert!(EMPTY_FIRST.is_none());
    assert!(EMPTY_LAST.is_none());
    assert!(EMPTY_SPLIT_FIRST.is_none());
    assert!(EMPTY_SPLIT_LAST.is_none());
}
