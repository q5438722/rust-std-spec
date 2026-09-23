#![feature(allocator_api)]

use std::alloc::{AllocError, Allocator, Global, Layout};
use std::cell::Cell;
use std::ptr::NonNull;

struct Token<'a> {
    value: &'a i32,
    drops: &'a Cell<usize>,
}

impl Drop for Token<'_> {
    fn drop(&mut self) {
        self.drops.set(self.drops.get() + 1);
    }
}

struct Zst;

#[derive(Default)]
struct Counts {
    allocations: Cell<usize>,
    deallocations: Cell<usize>,
    allocator_drops: Cell<usize>,
}

struct TrackingAllocator<'a> {
    counts: &'a Counts,
    identity: Box<u8>,
}

unsafe impl Allocator for TrackingAllocator<'_> {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        self.counts.allocations.set(self.counts.allocations.get() + 1);
        Global.allocate(layout)
    }

    unsafe fn deallocate(&self, pointer: NonNull<u8>, layout: Layout) {
        self.counts.deallocations.set(self.counts.deallocations.get() + 1);
        unsafe { Global.deallocate(pointer, layout) };
    }
}

impl Drop for TrackingAllocator<'_> {
    fn drop(&mut self) {
        self.counts.allocator_drops.set(self.counts.allocator_drops.get() + 1);
    }
}

fn convert_array<T, const N: usize>(s: [T; N], source_body: bool) -> Vec<T> {
    if source_body {
        owned_from_array::from_array(s)
    } else {
        <Vec<T> as From<[T; N]>>::from(s)
    }
}

fn convert_boxed<T, A: Allocator>(s: Box<[T], A>, source_body: bool) -> Vec<T, A> {
    if source_body {
        owned_from_boxed_slice::from_boxed_slice(s)
    } else {
        <Vec<T, A> as From<Box<[T], A>>>::from(s)
    }
}

fn exact_signatures<T, A: Allocator, const N: usize>() {
    let _: fn([T; N]) -> Vec<T> = owned_from_array::from_array::<T, N>;
    let _: fn([T; N]) -> Vec<T> = <Vec<T> as From<[T; N]>>::from;
    let _: fn(Box<[T], A>) -> Vec<T, A> =
        owned_from_boxed_slice::from_boxed_slice::<T, A>;
    let _: fn(Box<[T], A>) -> Vec<T, A> = <Vec<T, A> as From<Box<[T], A>>>::from;
}

#[test]
fn exact_function_types() {
    exact_signatures::<i32, Global, 0>();
    exact_signatures::<Zst, Global, 1>();
    exact_signatures::<Token<'_>, TrackingAllocator<'_>, 7>();
}

#[test]
fn arrays_preserve_all_elements() {
    for source_body in [true, false] {
        assert_eq!(convert_array::<i32, 0>([], source_body).as_slice(), &[]);
        assert_eq!(convert_array([41], source_body).as_slice(), &[41]);
        assert_eq!(convert_array([8, 3, 8, 1], source_body).as_slice(), &[8, 3, 8, 1]);
    }
}

#[test]
fn boxed_slices_preserve_all_elements() {
    for source_body in [true, false] {
        let empty: Box<[i32]> = Box::new([]);
        assert_eq!(convert_boxed(empty, source_body).as_slice(), &[]);
        let one: Box<[i32]> = Box::new([41]);
        assert_eq!(convert_boxed(one, source_body).as_slice(), &[41]);
        let several: Box<[i32]> = Box::new([8, 3, 8, 1]);
        assert_eq!(convert_boxed(several, source_body).as_slice(), &[8, 3, 8, 1]);
    }
}

#[test]
fn nonclone_borrowed_elements_move_once() {
    let first = 17;
    let second = 4;
    for source_body in [true, false] {
        for boxed in [false, true] {
            let drops = Cell::new(0);
            let input = [
                Token { value: &first, drops: &drops },
                Token { value: &second, drops: &drops },
                Token { value: &first, drops: &drops },
            ];
            let result = if boxed {
                let input: Box<[Token<'_>]> = Box::new(input);
                convert_boxed(input, source_body)
            } else {
                convert_array(input, source_body)
            };
            assert_eq!(drops.get(), 0);
            assert_eq!(result.iter().map(|item| *item.value).collect::<Vec<_>>(), [17, 4, 17]);
            assert!(std::ptr::eq(result[0].value, &first));
            assert!(std::ptr::eq(result[1].value, &second));
            drop(result);
            assert_eq!(drops.get(), 3);
        }
    }
}

#[test]
fn zero_sized_elements() {
    assert_eq!(std::mem::size_of::<Zst>(), 0);
    for source_body in [true, false] {
        assert_eq!(convert_array::<Zst, 0>([], source_body).len(), 0);
        assert_eq!(convert_array([Zst, Zst, Zst], source_body).len(), 3);
        let empty: Box<[Zst]> = Box::new([]);
        assert_eq!(convert_boxed(empty, source_body).len(), 0);
        let several: Box<[Zst]> = Box::new([Zst, Zst, Zst]);
        assert_eq!(convert_boxed(several, source_body).len(), 3);
    }
}

#[test]
fn boxed_storage_and_allocator_are_transferred() {
    for source_body in [true, false] {
        let counts = Counts::default();
        let allocator = TrackingAllocator { counts: &counts, identity: Box::new(37) };
        let mut input = Vec::new_in(allocator);
        input.extend([9, 2, 9, 5]);
        let input = input.into_boxed_slice();
        let pointer = input.as_ptr();
        let identity = &*Box::allocator(&input).identity as *const u8;
        let allocations = counts.allocations.get();
        let deallocations = counts.deallocations.get();
        assert!(allocations > 0);

        let result = convert_boxed(input, source_body);
        assert_eq!(result.as_slice(), &[9, 2, 9, 5]);
        assert_eq!(result.as_ptr(), pointer);
        assert_eq!(result.capacity(), 4);
        assert!(std::ptr::eq(result.allocator().counts, &counts));
        assert_eq!(&*result.allocator().identity as *const u8, identity);
        assert_eq!(counts.allocations.get(), allocations);
        assert_eq!(counts.deallocations.get(), deallocations);
        assert_eq!(counts.allocator_drops.get(), 0);

        drop(result);
        assert_eq!(counts.deallocations.get(), deallocations + 1);
        assert_eq!(counts.allocator_drops.get(), 1);
    }
}

#[test]
fn custom_allocator_empty_and_zst() {
    for source_body in [true, false] {
        let counts = Counts::default();
        let allocator = TrackingAllocator { counts: &counts, identity: Box::new(23) };
        let empty = Vec::<i32, _>::new_in(allocator).into_boxed_slice();
        let identity = &*Box::allocator(&empty).identity as *const u8;
        let result = convert_boxed(empty, source_body);
        assert!(result.is_empty());
        assert_eq!(&*result.allocator().identity as *const u8, identity);
        assert!(std::ptr::eq(result.allocator().counts, &counts));
        assert_eq!(counts.allocations.get(), 0);
        drop(result);
        assert_eq!(counts.deallocations.get(), 0);
        assert_eq!(counts.allocator_drops.get(), 1);

        let counts = Counts::default();
        let allocator = TrackingAllocator { counts: &counts, identity: Box::new(29) };
        let mut input = Vec::new_in(allocator);
        input.extend([Zst, Zst, Zst]);
        let input = input.into_boxed_slice();
        let identity = &*Box::allocator(&input).identity as *const u8;
        let result = convert_boxed(input, source_body);
        assert_eq!(result.len(), 3);
        assert_eq!(&*result.allocator().identity as *const u8, identity);
        assert!(std::ptr::eq(result.allocator().counts, &counts));
        assert_eq!(counts.allocations.get(), 0);
        drop(result);
        assert_eq!(counts.deallocations.get(), 0);
        assert_eq!(counts.allocator_drops.get(), 1);
    }
}
