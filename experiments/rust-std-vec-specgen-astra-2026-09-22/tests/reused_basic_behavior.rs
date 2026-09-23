#![feature(allocator_api)]

use std::alloc::{AllocError, Allocator, Global, Layout};
use std::cell::Cell;
use std::ops::Deref;
use std::ptr::NonNull;

use reused_default::default as source_default;
use reused_deref::deref as source_deref;
use reused_is_empty::is_empty as source_is_empty;

struct Element<'a> {
    value: &'a i32,
}

struct LocalAllocator<'a> {
    calls: &'a Cell<usize>,
}

unsafe impl Allocator for LocalAllocator<'_> {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        self.calls.set(self.calls.get() + 1);
        Global.allocate(layout)
    }

    unsafe fn deallocate(&self, ptr: NonNull<u8>, layout: Layout) {
        self.calls.set(self.calls.get() + 1);
        unsafe { Global.deallocate(ptr, layout) }
    }
}

fn exact_signatures<T, A: Allocator>() {
    let _: fn() -> Vec<T> = source_default::<T>;
    let _: fn() -> Vec<T> = <Vec<T> as Default>::default;
    let _: for<'a> fn(&'a Vec<T, A>) -> bool = source_is_empty::<T, A>;
    let _: for<'a> fn(&'a Vec<T, A>) -> bool = Vec::<T, A>::is_empty;
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a [T] = source_deref::<T, A>;
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a [T] = <Vec<T, A> as Deref>::deref;
}

fn source_with_borrowed_element<'a>(value: &'a i32) -> Vec<Element<'a>> {
    let mut result = source_default();
    result.push(Element { value });
    result
}

fn observe<T, A: Allocator>(vec: &Vec<T, A>) -> &[T] {
    let actual: &[T] = source_deref(vec);
    let official: &<Vec<T, A> as Deref>::Target = <Vec<T, A> as Deref>::deref(vec);
    assert_eq!(actual.len(), vec.len());
    assert_eq!(actual.len(), official.len());
    assert_eq!(actual.as_ptr(), vec.as_ptr());
    assert_eq!(actual.as_ptr(), official.as_ptr());
    assert_eq!(source_is_empty(vec), Vec::is_empty(vec));
    assert_eq!(source_is_empty(vec), actual.len() == 0);
    actual
}

#[test]
fn default_has_no_element_trait_or_static_bound() {
    let value = 17;
    exact_signatures::<Element<'_>, Global>();
    let actual: Vec<Element<'_>> = source_default();
    let official: Vec<Element<'_>> = Default::default();
    assert!(actual.is_empty());
    assert!(official.is_empty());
    assert_eq!(actual.capacity(), 0);
    assert_eq!(official.capacity(), 0);
    let borrowed = source_with_borrowed_element(&value);
    assert_eq!(*observe(&borrowed)[0].value, value);
}

#[test]
fn empty_includes_reserved_capacity() {
    for capacity in [0, 19] {
        let vec = Vec::<i32>::with_capacity(capacity);
        assert!(source_is_empty(&vec));
        assert_eq!(observe(&vec), &[]);
        assert!(vec.capacity() >= capacity);
    }
}

#[test]
fn full_prefix_keeps_singletons_repetitions_and_order() {
    for values in [&[41][..], &[5, -3, 5, 9, -3][..]] {
        let mut vec = Vec::with_capacity(values.len() + 11);
        vec.extend_from_slice(values);
        assert!(vec.capacity() > vec.len());
        assert!(!source_is_empty(&vec));
        assert_eq!(observe(&vec), values);
    }
}

#[test]
fn shared_slice_supports_nonstatic_elements_without_traits() {
    let first = 8;
    let second = -2;
    let values = [&first, &second, &first];
    let mut vec = Vec::with_capacity(9);
    for value in values {
        vec.push(Element { value });
    }
    let slice = observe(&vec);
    for (element, expected) in slice.iter().zip(values) {
        assert!(std::ptr::eq(element.value, expected));
    }
    assert_eq!(slice.len(), values.len());
}

#[test]
fn receivers_accept_a_nonclone_borrowing_allocator() {
    let calls = Cell::new(0);
    let first = 6;
    let second = 12;
    exact_signatures::<Element<'_>, LocalAllocator<'_>>();
    let mut vec = Vec::with_capacity_in(13, LocalAllocator { calls: &calls });
    let before = calls.get();
    assert!(source_is_empty(&vec));
    assert!(observe(&vec).is_empty());
    for value in [&first, &second, &first] {
        vec.push(Element { value });
    }
    let slice = observe(&vec);
    assert_eq!(slice.len(), 3);
    for (element, value) in slice.iter().zip([&first, &second, &first]) {
        assert!(std::ptr::eq(element.value, value));
    }
    assert!(!source_is_empty(&vec));
    assert_eq!(calls.get(), before);
    assert!(std::ptr::eq(vec.allocator().calls, &calls));
    drop(vec);
    assert_eq!(calls.get(), before + 1);
}

#[test]
fn zero_sized_capacity_is_not_confused_with_length() {
    struct Zst;
    let mut actual = source_default::<Zst>();
    let official = <Vec<Zst> as Default>::default();
    assert_eq!(actual.capacity(), official.capacity());
    assert_eq!(actual.capacity(), usize::MAX);
    assert!(source_is_empty(&actual));
    assert_eq!(observe(&actual).len(), 0);
    for _ in 0..4 {
        actual.push(Zst);
    }
    assert!(!source_is_empty(&actual));
    assert_eq!(observe(&actual).len(), 4);
    assert_eq!(actual.capacity(), usize::MAX);
    let calls = Cell::new(0);
    let mut allocated = Vec::new_in(LocalAllocator { calls: &calls });
    assert!(source_is_empty(&allocated));
    allocated.push(Zst);
    allocated.push(Zst);
    assert_eq!(observe(&allocated).len(), 2);
    assert!(!source_is_empty(&allocated));
    assert_eq!(calls.get(), 0);
}

#[test]
fn receiver_borrow_can_end_before_mutation() {
    let mut vec = vec![2, 7, 2];
    {
        let actual = source_deref(&vec);
        let official = <Vec<i32> as Deref>::deref(&vec);
        assert_eq!(actual, official);
        assert_eq!(actual, &[2, 7, 2]);
    }
    vec.push(-5);
    assert_eq!(source_deref(&vec), &[2, 7, 2, -5]);
}
