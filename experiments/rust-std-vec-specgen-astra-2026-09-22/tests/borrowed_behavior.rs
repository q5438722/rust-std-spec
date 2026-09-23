#![feature(allocator_api)]

use std::alloc::{AllocError, Allocator, Global, Layout};
use std::ptr::{self, NonNull};

struct LocalAllocator<'a>(&'a str);

unsafe impl Allocator for LocalAllocator<'_> {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, AllocError> {
        Global.allocate(layout)
    }

    unsafe fn deallocate(&self, ptr: NonNull<u8>, layout: Layout) {
        unsafe { Global.deallocate(ptr, layout) }
    }
}

struct Token<'a> {
    ordinal: u32,
    text: &'a str,
}

fn exact_signatures<T, A: Allocator>() {
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a Vec<T, A> = as_ref_vec::as_ref_vec::<T, A>;
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a [T] = as_ref_slice::as_ref_slice::<T, A>;
    let _: for<'a> fn(&'a mut Vec<T, A>) -> &'a mut Vec<T, A> = as_mut_vec::as_mut_vec::<T, A>;
    let _: for<'a> fn(&'a mut Vec<T, A>) -> &'a mut [T] = as_mut_slice::as_mut_slice::<T, A>;
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a Vec<T, A> = <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref;
    let _: for<'a> fn(&'a Vec<T, A>) -> &'a [T] = <Vec<T, A> as AsRef<[T]>>::as_ref;
    let _: for<'a> fn(&'a mut Vec<T, A>) -> &'a mut Vec<T, A> =
        <Vec<T, A> as AsMut<Vec<T, A>>>::as_mut;
    let _: for<'a> fn(&'a mut Vec<T, A>) -> &'a mut [T] =
        <Vec<T, A> as AsMut<[T]>>::as_mut;
}

fn shared_contents<T, A: Allocator>(vec: &Vec<T, A>) {
    exact_signatures::<T, A>();
    let vector_conversions: [for<'a> fn(&'a Vec<T, A>) -> &'a Vec<T, A>; 2] =
        [as_ref_vec::as_ref_vec, <Vec<T, A> as AsRef<Vec<T, A>>>::as_ref];
    for convert in vector_conversions {
        let result = convert(vec);
        assert!(ptr::eq(result, vec));
        assert_eq!(result.capacity(), vec.capacity());
        assert!(ptr::eq(result.allocator(), vec.allocator()));
    }
    let slice_conversions: [for<'a> fn(&'a Vec<T, A>) -> &'a [T]; 2] =
        [as_ref_slice::as_ref_slice, <Vec<T, A> as AsRef<[T]>>::as_ref];
    for convert in slice_conversions {
        let result = convert(vec);
        assert_eq!(result.len(), vec.len());
        assert!(ptr::eq(result.as_ptr(), vec.as_ptr()));
        for (actual, expected) in result.iter().zip(vec.iter()) {
            assert!(ptr::eq(actual, expected));
        }
    }
}

#[test]
fn empty_and_reserved_empty_vectors() {
    let label = String::from("local allocator");
    let mut vec: Vec<Token<'_>, _> = Vec::new_in(LocalAllocator(&label));
    shared_contents(&vec);
    vec.reserve(7);
    shared_contents(&vec);
    assert_eq!(vec.allocator().0, label);
}

#[test]
fn non_clone_elements_keep_all_contents_and_order() {
    let label = String::from("borrowed, not static");
    let mut vec = Vec::new_in(LocalAllocator(&label));
    vec.extend([
        Token { ordinal: 9, text: &label },
        Token { ordinal: 1, text: &label },
        Token { ordinal: 9, text: &label },
        Token { ordinal: 4, text: &label },
    ]);
    shared_contents(&vec);
    let result = as_ref_slice::as_ref_slice(&vec);
    assert_eq!(result.iter().map(|item| item.ordinal).collect::<Vec<_>>(), [9, 1, 9, 4]);
    assert!(result.iter().all(|item| item.text == label));
}

#[test]
fn zero_sized_non_clone_elements() {
    struct Zst;
    let label = String::from("zst allocator");
    let mut vec = Vec::new_in(LocalAllocator(&label));
    shared_contents(&vec);
    vec.extend([Zst, Zst, Zst]);
    shared_contents(&vec);
    as_mut_vec::as_mut_vec(&mut vec).push(Zst);
    assert_eq!(as_mut_slice::as_mut_slice(&mut vec).len(), 4);
    <Vec<Zst, _> as AsMut<Vec<Zst, _>>>::as_mut(&mut vec).push(Zst);
    assert_eq!(<Vec<Zst, _> as AsMut<[Zst]>>::as_mut(&mut vec).len(), 5);
}

#[test]
fn mutable_vector_allows_length_capacity_and_order_changes() {
    let label = String::from("mutable vector");
    let mut vec = Vec::new_in(LocalAllocator(&label));
    {
        let result = as_mut_vec::as_mut_vec(&mut vec);
        result.push(Token { ordinal: 10, text: &label });
        result.push(Token { ordinal: 20, text: &label });
        result.reserve(128);
        result.swap(0, 1);
    }
    assert_eq!(vec.iter().map(|item| item.ordinal).collect::<Vec<_>>(), [20, 10]);
    assert!(vec.capacity() >= 130);
    {
        let result = <Vec<Token<'_>, _> as AsMut<Vec<Token<'_>, _>>>::as_mut(&mut vec);
        result.clear();
        result.push(Token { ordinal: 30, text: &label });
    }
    assert_eq!(vec.len(), 1);
    assert_eq!(vec[0].ordinal, 30);
    assert_eq!(vec.allocator().0, label);
}

#[test]
fn mutable_slice_writes_back_without_freezing_caller() {
    let label = String::from("mutable slice");
    let mut vec = Vec::new_in(LocalAllocator(&label));
    vec.extend([
        Token { ordinal: 3, text: &label },
        Token { ordinal: 4, text: &label },
        Token { ordinal: 5, text: &label },
    ]);
    let capacity = vec.capacity();
    {
        let result = as_mut_slice::as_mut_slice(&mut vec);
        result[1] = Token { ordinal: 40, text: &label };
        result.swap(0, 2);
    }
    assert_eq!(vec.iter().map(|item| item.ordinal).collect::<Vec<_>>(), [5, 40, 3]);
    {
        let result = <Vec<Token<'_>, _> as AsMut<[Token<'_>]>>::as_mut(&mut vec);
        result[0] = Token { ordinal: 50, text: &label };
    }
    assert_eq!(vec.iter().map(|item| item.ordinal).collect::<Vec<_>>(), [50, 40, 3]);
    assert_eq!(vec.capacity(), capacity);
}
