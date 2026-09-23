#![allow(dead_code)]

mod source {
    include!(env!("SLICE_DEFAULT_SOURCE"));
}

struct NoTraits(String);
struct Borrowed<'a>(&'a str);
struct ZeroSized;
enum Uninhabited {}

fn check<'a, T: 'a>() {
    let shared: fn() -> &'a [T] = <&'a [T] as core::default::Default>::default;
    let shared_copy: fn() -> &'a [T] = source::default_shared::<T>;
    let mutable: fn() -> &'a mut [T] = <&'a mut [T] as core::default::Default>::default;
    let mutable_copy: fn() -> &'a mut [T] = source::default_mut::<T>;
    for value in [shared(), shared_copy()] {
        assert_eq!(value.len(), 0);
        assert!(value.is_empty());
        assert!(value.iter().next().is_none());
    }
    for value in [mutable(), mutable_copy()] {
        assert_eq!(value.len(), 0);
        assert!(value.is_empty());
        assert!(value.iter_mut().next().is_none());
    }
}

#[test]
fn no_arguments_and_exact_shared_return() {
    let source: fn() -> &'static [u8] = source::default_shared::<u8>;
    let actual: fn() -> &'static [u8] = <&[u8] as core::default::Default>::default;
    assert_eq!(source(), &[]);
    assert_eq!(actual(), &[]);
}

#[test]
fn no_arguments_and_exact_mutable_return() {
    let source: fn() -> &'static mut [u8] = source::default_mut::<u8>;
    let actual: fn() -> &'static mut [u8] = <&mut [u8] as core::default::Default>::default;
    let from_source: &mut [u8] = source();
    let from_actual: &mut [u8] = actual();
    assert!(from_source.is_empty());
    assert!(from_actual.is_empty());
}

#[test]
fn non_copy_non_default_elements() {
    check::<NoTraits>();
}

#[test]
fn non_static_elements_and_reference_lifetimes() {
    fn scoped<'a>(text: &'a str) {
        let _element = Borrowed(text);
        check::<'a, Borrowed<'a>>();
    }
    let text = String::from("local");
    scoped(&text);
}

#[test]
fn zero_sized_non_copy_elements() {
    assert_eq!(core::mem::size_of::<ZeroSized>(), 0);
    check::<ZeroSized>();
}

#[test]
fn no_element_needs_to_exist() {
    check::<Uninhabited>();
}

#[test]
fn simultaneous_mutable_defaults_are_legal() {
    let first: &mut [NoTraits] = Default::default();
    let second: &mut [NoTraits] = Default::default();
    let reborrowed: &mut [NoTraits] = &mut *first;
    assert!(reborrowed.is_empty());
    assert!(second.is_empty());
    assert!(first.is_empty());
}
