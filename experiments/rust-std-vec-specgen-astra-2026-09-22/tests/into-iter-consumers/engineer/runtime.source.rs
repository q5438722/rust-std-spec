#![feature(allocator_api)]

extern crate into_iter_count;
extern crate into_iter_last_native;

use std::alloc::{AllocError, Allocator, Global, Layout};
use std::cell::Cell;
use std::collections::VecDeque;
use std::ptr::NonNull;
use std::vec::IntoIter;

fn count<T, A: Allocator>(iter: IntoIter<T, A>, source: bool) -> usize {
    if source {
        <IntoIter<T, A> as into_iter_count::source::Iterator>::count(iter)
    } else {
        <IntoIter<T, A> as Iterator>::count(iter)
    }
}

fn last<T, A: Allocator>(iter: IntoIter<T, A>, source: bool) -> Option<T> {
    if source {
        <IntoIter<T, A> as into_iter_last_native::source::Iterator>::last(iter)
    } else {
        <IntoIter<T, A> as Iterator>::last(iter)
    }
}

fn signatures<T, A: Allocator>() {
    let _: fn(IntoIter<T, A>) -> usize =
        <IntoIter<T, A> as into_iter_count::source::Iterator>::count;
    let _: fn(IntoIter<T, A>) -> usize = <IntoIter<T, A> as Iterator>::count;
    let _: fn(IntoIter<T, A>) -> Option<T> =
        <IntoIter<T, A> as into_iter_last_native::source::Iterator>::last;
    let _: fn(IntoIter<T, A>) -> Option<T> = <IntoIter<T, A> as Iterator>::last;
}

#[test]
fn exact_generic_function_types() {
    signatures::<(), Global>();
}

fn advanced(values: &[i32], steps: &[bool]) -> (IntoIter<i32>, VecDeque<i32>) {
    let mut iter = values.to_vec().into_iter();
    let mut expected: VecDeque<_> = values.iter().copied().collect();
    for &back in steps {
        if back {
            assert_eq!(iter.next_back(), expected.pop_back());
        } else {
            assert_eq!(iter.next(), expected.pop_front());
        }
    }
    (iter, expected)
}

#[test]
fn current_remaining_empty_singleton_duplicates_and_both_ends() {
    let inputs: &[&[i32]] = &[&[], &[7], &[9, 2, 9, 4, 2]];
    let steps: &[&[bool]] = &[
        &[], &[false], &[true], &[false, false], &[true, true],
        &[false, true, false], &[true, false, true, false],
        &[false, true, false, true, false, true, false],
    ];
    for source in [false, true] {
        for values in inputs {
            for steps in steps {
                let (iter, expected) = advanced(values, steps);
                assert_eq!(count(iter, source), expected.len());
                let (iter, mut expected) = advanced(values, steps);
                assert_eq!(last(iter, source), expected.pop_back());
            }
        }
    }
}

struct Zst;

#[test]
fn zero_sized_elements_without_clone_or_eq() {
    for source in [false, true] {
        for n in 0_usize..5 {
            let mut values = Vec::new();
            for _ in 0..n {
                values.push(Zst);
            }
            let mut iter = values.into_iter();
            let _ = iter.next();
            let _ = iter.next_back();
            assert_eq!(count(iter, source), n.saturating_sub(2));

            let mut values = Vec::new();
            for _ in 0..n {
                values.push(Zst);
            }
            let mut iter = values.into_iter();
            let _ = iter.next_back();
            let _ = iter.next();
            assert_eq!(last(iter, source).is_some(), n > 2);
        }
    }
}

struct Borrowed<'a> {
    value: &'a str,
}

struct BorrowingAllocator<'a> {
    allocations: &'a Cell<usize>,
    deallocations: &'a Cell<usize>,
    drops: &'a Cell<usize>,
    token: Box<u8>,
}

unsafe impl Allocator for BorrowingAllocator<'_> {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        let block = Global.allocate(layout)?;
        self.allocations.set(self.allocations.get() + 1);
        Ok(block)
    }

    unsafe fn deallocate(&self, pointer: NonNull<u8>, layout: Layout) {
        self.deallocations.set(self.deallocations.get() + 1);
        unsafe { Global.deallocate(pointer, layout) };
    }
}

impl Drop for BorrowingAllocator<'_> {
    fn drop(&mut self) {
        assert_eq!(*self.token, 31);
        self.drops.set(self.drops.get() + 1);
    }
}

#[test]
fn nonstatic_elements_and_nonclone_borrowing_allocator() {
    let text = String::from("local element");
    for source in [false, true] {
        for return_last in [false, true] {
            let allocations = Cell::new(0);
            let deallocations = Cell::new(0);
            let drops = Cell::new(0);
            let allocator = BorrowingAllocator {
                allocations: &allocations,
                deallocations: &deallocations,
                drops: &drops,
                token: Box::new(31),
            };
            signatures::<Borrowed<'_>, BorrowingAllocator<'_>>();
            let mut values = Vec::new_in(allocator);
            for _ in 0..4 {
                values.push(Borrowed { value: &text });
            }
            let mut iter = values.into_iter();
            let front = iter.next().unwrap();
            let back = iter.next_back().unwrap();
            if return_last {
                let result = last(iter, source).unwrap();
                assert!(std::ptr::eq(result.value, text.as_str()));
            } else {
                assert_eq!(count(iter, source), 2);
            }
            assert_eq!(front.value, "local element");
            assert_eq!(back.value, "local element");
            assert!(allocations.get() > 0);
            assert_eq!(allocations.get(), deallocations.get());
            assert_eq!(drops.get(), 1);
        }
    }
}

struct DropProbe<'a> {
    id: usize,
    drops: &'a [Cell<usize>; 5],
}

impl Drop for DropProbe<'_> {
    fn drop(&mut self) {
        self.drops[self.id].set(self.drops[self.id].get() + 1);
        assert_eq!(self.drops[self.id].get(), 1);
    }
}

#[test]
fn count_drops_only_the_remaining_elements() {
    for source in [false, true] {
        let drops = std::array::from_fn(|_| Cell::new(0));
        let mut values = Vec::new();
        for id in 0..5 {
            values.push(DropProbe { id, drops: &drops });
        }
        let mut iter = values.into_iter();
        let front = iter.next().unwrap();
        let back = iter.next_back().unwrap();
        assert_eq!(count(iter, source), 3);
        assert_eq!(drops.each_ref().map(Cell::get), [0, 1, 1, 1, 0]);
        drop(front);
        drop(back);
        assert_eq!(drops.each_ref().map(Cell::get), [1, 1, 1, 1, 1]);
    }
}

#[test]
fn last_does_not_drop_the_returned_or_previously_moved_elements() {
    for source in [false, true] {
        let drops = std::array::from_fn(|_| Cell::new(0));
        let mut values = Vec::new();
        for id in 0..5 {
            values.push(DropProbe { id, drops: &drops });
        }
        let mut iter = values.into_iter();
        let front = iter.next().unwrap();
        let back = iter.next_back().unwrap();
        let returned = last(iter, source).unwrap();
        assert_eq!(returned.id, 3);
        assert_eq!(drops.each_ref().map(Cell::get), [0, 1, 1, 0, 0]);
        drop(returned);
        assert_eq!(drops.each_ref().map(Cell::get), [0, 1, 1, 1, 0]);
        drop(front);
        drop(back);
        assert_eq!(drops.each_ref().map(Cell::get), [1, 1, 1, 1, 1]);
    }
}
