#![feature(allocator_api, sliceindex_wrappers)]

use core::index::{Clamp, Last};
use core::range;
use std::alloc::{AllocError, Allocator, Global, Layout};
use std::cell::Cell;
use std::ops::{Bound::*, Index};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::ptr::NonNull;
use std::slice::SliceIndex;
use vec_index_source::index_source;
use vec_specs::vec::index::index_source as aggregate_index;

fn exact_signature<T, I: SliceIndex<[T]>, A: Allocator>() {
    let _: for<'a> fn(&'a Vec<T, A>, I) -> &'a I::Output = index_source::<T, I, A>;
    let _: for<'a> fn(&'a Vec<T, A>, I) -> &'a I::Output = aggregate_index::<T, I, A>;
    let _: for<'a> fn(&'a Vec<T, A>, I) -> &'a I::Output =
        <Vec<T, A> as Index<I>>::index;
}

fn element<I: SliceIndex<[i32], Output = i32>>(
    vec: &Vec<i32>, make: impl Fn() -> I, expected: i32,
) {
    let source = index_source(vec, make());
    let aggregate = aggregate_index(vec, make());
    let standard = Index::index(vec, make());
    assert_eq!(*source, expected);
    assert_eq!(source, standard);
    assert_eq!(aggregate, standard);
    assert!(std::ptr::eq(source, standard));
}

fn slice<I: SliceIndex<[i32], Output = [i32]>>(
    vec: &Vec<i32>, make: impl Fn() -> I, expected: &[i32],
) {
    let source = index_source(vec, make());
    let aggregate = aggregate_index(vec, make());
    let standard = Index::index(vec, make());
    assert_eq!(source, expected);
    assert_eq!(source, standard);
    assert_eq!(aggregate, standard);
    assert!(std::ptr::eq(source, standard));
}

#[test]
fn generic_signature_and_legacy_indices() {
    exact_signature::<String, usize, Global>();
    exact_signature::<String, std::ops::Range<usize>, Global>();
    let vec = vec![8, 3, 8, 1, 8];
    element(&vec, || 0, 8);
    element(&vec, || 4, 8);
    slice(&vec, || 1..5, &[3, 8, 1, 8]);
    slice(&vec, || ..5, &[8, 3, 8, 1, 8]);
    slice(&vec, || 1.., &[3, 8, 1, 8]);
    slice(&vec, || .., &[8, 3, 8, 1, 8]);
    slice(&vec, || 1..=3, &[3, 8, 1]);
    slice(&vec, || ..=3, &[8, 3, 8, 1]);
    slice(&vec, || 2..2, &[]);
    slice(&vec, || 5..5, &[]);
    slice(&vec, || 5.., &[]);
    slice(&vec, || 2..=1, &[]);
}

#[test]
fn new_ranges_and_all_bound_forms() {
    let vec = vec![8, 3, 8, 1, 8];
    slice(&vec, || range::Range { start: 1, end: 5 }, &[3, 8, 1, 8]);
    slice(&vec, || range::RangeFrom { start: 1 }, &[3, 8, 1, 8]);
    slice(&vec, || range::RangeInclusive { start: 1, last: 3 }, &[3, 8, 1]);
    slice(&vec, || range::RangeToInclusive { last: 3 }, &[8, 3, 8, 1]);
    slice(&vec, || (Included(1), Included(3)), &[3, 8, 1]);
    slice(&vec, || (Included(1), Excluded(3)), &[3, 8]);
    slice(&vec, || (Included(1), Unbounded), &[3, 8, 1, 8]);
    slice(&vec, || (Excluded(1), Included(3)), &[8, 1]);
    slice(&vec, || (Excluded(1), Excluded(3)), &[8]);
    slice(&vec, || (Excluded(1), Unbounded), &[8, 1, 8]);
    slice(&vec, || (Unbounded, Included(3)), &[8, 3, 8, 1]);
    slice(&vec, || (Unbounded, Excluded(3)), &[8, 3, 8]);
    slice(&vec, || (Unbounded, Unbounded), &[8, 3, 8, 1, 8]);
    slice(&vec, || (Included(5), Excluded(5)), &[]);
}

#[test]
fn last_and_every_clamp_implementation() {
    let vec = vec![8, 3, 8, 1, 8];
    element(&vec, || Last, 8);
    element(&vec, || Clamp(usize::MAX), 8);
    slice(&vec, || Clamp(1..99), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(range::Range { start: 1, end: 99 }), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(1..=99), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(range::RangeInclusive { start: 1, last: 99 }), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(1..), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(range::RangeFrom { start: 1 }), &[3, 8, 1, 8]);
    slice(&vec, || Clamp(..99), &[8, 3, 8, 1, 8]);
    slice(&vec, || Clamp(..=99), &[8, 3, 8, 1, 8]);
    slice(&vec, || Clamp(range::RangeToInclusive { last: 99 }), &[8, 3, 8, 1, 8]);
    slice(&vec, || Clamp(..), &[8, 3, 8, 1, 8]);
    slice(&vec, || Clamp(99..100), &[]);
    slice(&vec, || Clamp(99..), &[]);
}

#[test]
fn empty_vectors_and_exhausted_inclusive_ranges() {
    let empty = Vec::<i32>::new();
    slice(&empty, || 0..0, &[]);
    slice(&empty, || ..0, &[]);
    slice(&empty, || 0.., &[]);
    slice(&empty, || .., &[]);
    slice(&empty, || range::Range { start: 0, end: 0 }, &[]);
    slice(&empty, || range::RangeFrom { start: 0 }, &[]);
    slice(&empty, || (Unbounded, Unbounded), &[]);
    slice(&empty, || (Included(0), Excluded(0)), &[]);
    slice(&empty, || Clamp(9..10), &[]);
    slice(&empty, || Clamp(range::Range { start: 9, end: 10 }), &[]);
    slice(&empty, || Clamp(9..), &[]);
    slice(&empty, || Clamp(range::RangeFrom { start: 9 }), &[]);
    slice(&empty, || Clamp(..9), &[]);
    slice(&empty, || Clamp(..), &[]);
    let vec = vec![8, 3, 8];
    slice(&vec, || {
        let mut range = 1..=2;
        assert_eq!(range.next(), Some(1));
        assert_eq!(range.next(), Some(2));
        range
    }, &[]);
}

struct BorrowingAllocator<'a>(&'a Cell<usize>);

unsafe impl Allocator for BorrowingAllocator<'_> {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        self.0.set(self.0.get() + 1);
        Global.allocate(layout)
    }

    unsafe fn deallocate(&self, ptr: NonNull<u8>, layout: Layout) {
        unsafe { Global.deallocate(ptr, layout) }
    }
}

struct NoTraits<'a>(&'a str, usize);

#[test]
fn nonstatic_elements_and_nonclone_borrowing_allocator() {
    exact_signature::<NoTraits<'_>, usize, BorrowingAllocator<'_>>();
    exact_signature::<NoTraits<'_>, std::ops::Range<usize>, BorrowingAllocator<'_>>();
    let text = String::from("borrowed");
    let calls = Cell::new(0);
    let mut vec = Vec::new_in(BorrowingAllocator(&calls));
    vec.push(NoTraits(&text, 3));
    vec.push(NoTraits(&text, 1));
    vec.push(NoTraits(&text, 3));
    let source = index_source(&vec, 1);
    let standard = Index::index(&vec, 1);
    assert_eq!((source.0, source.1), ("borrowed", 1));
    assert!(std::ptr::eq(source, standard));
    let source = index_source(&vec, 0..3);
    let aggregate = aggregate_index(&vec, 0..3);
    let standard = Index::index(&vec, 0..3);
    for (i, expected) in [3, 1, 3].into_iter().enumerate() {
        assert_eq!((source[i].0, source[i].1), ("borrowed", expected));
        assert_eq!((aggregate[i].0, aggregate[i].1), (standard[i].0, standard[i].1));
    }
    assert_eq!(source.len(), 3);
    vec.push(NoTraits(&text, 2));
    assert_eq!(index_source(&vec, 3).1, 2);
    assert!(calls.get() > 0);
}

#[test]
fn zero_sized_elements() {
    struct Zst;
    let mut vec = Vec::new();
    for _ in 0..4 {
        vec.push(Zst);
    }
    let _: &Zst = index_source(&vec, 0);
    let _: &Zst = aggregate_index(&vec, 3);
    let _: &Zst = Index::index(&vec, 3);
    assert_eq!(index_source(&vec, 0..4).len(), 4);
    assert_eq!(aggregate_index(&vec, 1..3).len(), 2);
    assert_eq!(Index::index(&vec, 1..3).len(), 2);
    assert!(index_source(&vec, 4..4).is_empty());
}

fn panic_message(payload: Box<dyn std::any::Any + Send>) -> String {
    if let Some(message) = payload.downcast_ref::<&str>() {
        (*message).to_owned()
    } else if let Some(message) = payload.downcast_ref::<String>() {
        message.clone()
    } else {
        panic!("unexpected non-string panic payload");
    }
}

fn panics<I: SliceIndex<[i32]>>(vec: &Vec<i32>, make: impl Fn() -> I) {
    let source = catch_unwind(AssertUnwindSafe(|| { let _ = index_source(vec, make()); }));
    let aggregate = catch_unwind(AssertUnwindSafe(|| { let _ = aggregate_index(vec, make()); }));
    let standard = catch_unwind(AssertUnwindSafe(|| { let _ = Index::index(vec, make()); }));
    let expected = panic_message(standard.expect_err("standard indexing must panic"));
    assert_eq!(panic_message(source.expect_err("source indexing must panic")), expected);
    assert_eq!(panic_message(aggregate.expect_err("aggregate indexing must panic")), expected);
}

#[test]
fn panic_reports_index_call_site() {
    thread_local! {
        static LOCATION: std::cell::RefCell<Option<(String, u32)>> = const {
            std::cell::RefCell::new(None)
        };
    }
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(|info| {
        LOCATION.with_borrow_mut(|saved| {
            *saved = info.location().map(|location| (location.file().to_owned(), location.line()));
        });
    }));
    let vec = vec![8];
    let source_site = (file!().to_owned(), line!() + 1);
    let source = catch_unwind(|| { let _ = index_source(&vec, 1); });
    let source_location = LOCATION.take();
    let aggregate_site = (file!().to_owned(), line!() + 1);
    let aggregate = catch_unwind(|| { let _ = aggregate_index(&vec, 1); });
    let aggregate_location = LOCATION.take();
    let standard_site = (file!().to_owned(), line!() + 1);
    let standard = catch_unwind(|| { let _ = Index::index(&vec, 1); });
    let standard_location = LOCATION.take();
    std::panic::set_hook(previous);
    assert!(source.is_err() && aggregate.is_err() && standard.is_err());
    assert_eq!(standard_location, Some(standard_site));
    assert_eq!(source_location, Some(source_site));
    assert_eq!(aggregate_location, Some(aggregate_site));
}

#[test]
fn safe_out_of_bounds_reversed_and_overflow_cases() {
    let vec = vec![8, 3, 8, 1, 8];
    panics(&vec, || 5);
    panics(&vec, || usize::MAX);
    panics(&vec, || 0..6);
    panics(&vec, || 4..1);
    panics(&vec, || 6..6);
    panics(&vec, || 6..);
    panics(&vec, || ..6);
    panics(&vec, || 3..=1);
    panics(&vec, || 0..=5);
    panics(&vec, || ..=5);
    panics(&vec, || 0..=usize::MAX);
    panics(&vec, || ..=usize::MAX);
    panics(&vec, || range::Range { start: 4, end: 1 });
    panics(&vec, || range::RangeFrom { start: 6 });
    panics(&vec, || range::RangeInclusive { start: 0, last: usize::MAX });
    panics(&vec, || range::RangeToInclusive { last: usize::MAX });
    panics(&vec, || (Excluded(usize::MAX), Unbounded));
    panics(&vec, || (Unbounded, Included(usize::MAX)));
    panics(&vec, || (Included(4), Excluded(1)));
    panics(&vec, || Clamp(4..1));
    panics(&vec, || Clamp(range::Range { start: 4, end: 1 }));
    let empty = Vec::<i32>::new();
    panics(&empty, || 0);
    panics(&empty, || Last);
    panics(&empty, || Clamp(0));
    panics(&empty, || ..=0);
    panics(&empty, || Clamp(..=0));
    panics(&empty, || {
        let mut range = 0..=0;
        assert_eq!(range.next(), Some(0));
        range
    });
}
