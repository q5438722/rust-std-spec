#![allow(dead_code)]

use core::alloc::{Layout, LayoutError};
use vstd::layout::valid_layout;
use vstd::prelude::*;
use vstd::std_specs::layout_value::{
    axiom_layout_view_valid, max_usize, round_up_to, LayoutView,
};

verus! {

proof fn align_is_positive(size: usize, align: usize)
    requires
        valid_layout(size, align),
    ensures
        align > 0,
{
    reveal(vstd::arithmetic::power2::is_pow2);
}

pub axiom fn round_up_preserves_layout(size: usize, align: usize)
    requires
        valid_layout(size, align),
    ensures
        round_up_to(size as nat, align as nat) <= usize::MAX as nat,
        valid_layout(round_up_to(size as nat, align as nat) as usize, align)
;

pub axiom fn rounded_prefix_plus_layout_fits(
    size: usize,
    size_align: usize,
    next_size: usize,
    next_align: usize,
)
    requires
        valid_layout(size, size_align),
        valid_layout(next_size, next_align),
    ensures
        round_up_to(size as nat, next_align as nat) + next_size as nat <= usize::MAX as nat
;

fn round_up_checked(
    size: usize,
    align: usize,
) -> (result: Option<usize>)
    requires
        align > 0,
    ensures
        round_up_to(size as nat, align as nat) <= usize::MAX as nat ==>
            (result matches Some(value)
                && value as nat == round_up_to(size as nat, align as nat)),
        round_up_to(size as nat, align as nat) > usize::MAX as nat ==> result is None,
{
    let remainder = size % align;
    if remainder == 0 {
        Some(size)
    } else {
        size.checked_add(align - remainder)
    }
}

fn source_layout_align_to(
    layout: &Layout,
    align: usize,
) -> (result: Result<Layout, LayoutError>)
    ensures
        valid_layout(0, align)
            && valid_layout(layout@.size, max_usize(layout@.align, align)) ==>
            (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: layout@.size,
            align: max_usize(layout@.align, align),
        })),
        (!valid_layout(0, align)
            || !valid_layout(layout@.size, max_usize(layout@.align, align))) ==> result is Err,
{
    proof {
        axiom_layout_view_valid(layout);
    }
    let new_align = if layout.align() >= align {
        layout.align()
    } else {
        align
    };
    match Layout::from_size_align(0, align) {
        Err(error) => Err(error),
        Ok(_) => Layout::from_size_align(layout.size(), new_align),
    }
}

fn source_layout_pad_to_align(layout: &Layout) -> (result: Layout)
    ensures
        result@.align == layout@.align,
        result@.size as nat == round_up_to(layout@.size as nat, layout@.align as nat),
{
    proof {
        axiom_layout_view_valid(layout);
    }
    let size = layout.size();
    let align = layout.align();
    proof {
        align_is_positive(size, align);
        round_up_preserves_layout(size, align);
    }
    match round_up_checked(size, align) {
        Some(rounded) => match Layout::from_size_align(rounded, align) {
            Ok(result) => result,
            Err(_) => {
                assert(false);
                *layout
            },
        },
        None => {
            assert(false);
            *layout
        },
    }
}

fn source_layout_repeat_packed(
    layout: &Layout,
    n: usize,
) -> (result: Result<Layout, LayoutError>)
    ensures
        ({
            let size = layout@.size as nat * n as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: (layout@.size as nat * n as nat) as usize,
            align: layout@.align,
        })),
        ({
            let size = layout@.size as nat * n as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
{
    proof {
        axiom_layout_view_valid(layout);
    }
    match layout.size().checked_mul(n) {
        Some(size) => Layout::from_size_align(size, layout.align()),
        None => Layout::from_size_align(usize::MAX, 1),
    }
}

fn source_layout_extend_packed(
    layout: &Layout,
    next: Layout,
) -> (result: Result<Layout, LayoutError>)
    ensures
        ({
            let size = layout@.size as nat + next@.size as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> (result matches Ok(new_layout) && new_layout@ == (LayoutView {
            size: (layout@.size as nat + next@.size as nat) as usize,
            align: layout@.align,
        })),
        ({
            let size = layout@.size as nat + next@.size as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
{
    proof {
        axiom_layout_view_valid(layout);
        axiom_layout_view_valid(&next);
    }
    match layout.size().checked_add(next.size()) {
        Some(size) => Layout::from_size_align(size, layout.align()),
        None => Layout::from_size_align(usize::MAX, 1),
    }
}

fn source_layout_extend(
    layout: &Layout,
    next: Layout,
) -> (result: Result<(Layout, usize), LayoutError>)
    ensures
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size <= usize::MAX as nat
                && valid_layout(size as usize, max_usize(layout@.align, next@.align))
        }) ==> ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: max_usize(layout@.align, next@.align),
            }) && pair.1 as nat == offset
        }),
        ({
            let offset = round_up_to(layout@.size as nat, next@.align as nat);
            let size = offset + next@.size as nat;
            size > usize::MAX as nat
                || !valid_layout(size as usize, max_usize(layout@.align, next@.align))
        }) ==> result is Err,
{
    proof {
        axiom_layout_view_valid(layout);
        axiom_layout_view_valid(&next);
    }
    let size = layout.size();
    let align = layout.align();
    let next_size = next.size();
    let next_align = next.align();
    proof {
        align_is_positive(next_size, next_align);
        rounded_prefix_plus_layout_fits(size, align, next_size, next_align);
    }
    let new_align = if align >= next_align {
        align
    } else {
        next_align
    };
    match round_up_checked(size, next_align) {
        Some(offset) => match offset.checked_add(next_size) {
            Some(new_size) => match Layout::from_size_align(new_size, new_align) {
                Ok(result) => Ok((result, offset)),
                Err(error) => Err(error),
            },
            None => {
                assert(false);
                match Layout::from_size_align(usize::MAX, 1) {
                    Err(error) => Err(error),
                    Ok(value) => Ok((value, 0)),
                }
            },
        },
        None => {
            assert(false);
            match Layout::from_size_align(usize::MAX, 1) {
                Err(error) => Err(error),
                Ok(value) => Ok((value, 0)),
            }
        },
    }
}

fn source_layout_repeat(
    layout: &Layout,
    n: usize,
) -> (result: Result<(Layout, usize), LayoutError>)
    ensures
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size <= usize::MAX as nat && valid_layout(size as usize, layout@.align)
        }) ==> ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            result matches Ok(pair) && pair.0@ == (LayoutView {
                size: size as usize,
                align: layout@.align,
            }) && pair.1 as nat == stride
        }),
        ({
            let stride = round_up_to(layout@.size as nat, layout@.align as nat);
            let size = if n == 0 {
                0
            } else {
                stride * (n as nat - 1) + layout@.size as nat
            };
            size > usize::MAX as nat || !valid_layout(size as usize, layout@.align)
        }) ==> result is Err,
{
    let padded = source_layout_pad_to_align(layout);
    let result = if let Some(k) = n.checked_sub(1) {
        match source_layout_repeat_packed(&padded, k) {
            Err(error) => Err(error),
            Ok(repeated) => source_layout_extend_packed(&repeated, *layout),
        }
    } else {
        source_layout_repeat_packed(layout, 0)
    };
    match result {
        Ok(value) => Ok((value, padded.size())),
        Err(error) => Err(error),
    }
}

fn source_layout_array<T>(
    length: usize,
) -> (result: Result<Layout, LayoutError>)
    ensures
        ({
            let size = vstd::layout::size_of_as_usize::<T>() as nat * length as nat;
            size <= usize::MAX as nat
                && valid_layout(size as usize, vstd::layout::align_of_as_usize::<T>())
        }) ==> (result matches Ok(layout) && layout@ == (LayoutView {
            size: (vstd::layout::size_of_as_usize::<T>() as nat * length as nat) as usize,
            align: vstd::layout::align_of_as_usize::<T>(),
        })),
        ({
            let size = vstd::layout::size_of_as_usize::<T>() as nat * length as nat;
            size > usize::MAX as nat
                || !valid_layout(size as usize, vstd::layout::align_of_as_usize::<T>())
        }) ==> result is Err,
{
    let element = Layout::new::<T>();
    source_layout_repeat_packed(&element, length)
}

} // verus!

fn main() {}
