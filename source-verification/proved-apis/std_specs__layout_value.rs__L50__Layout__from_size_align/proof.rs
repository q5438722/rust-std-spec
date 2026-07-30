#![allow(dead_code)]

use core::alloc::{Layout as AllocDesc, LayoutError};
use vstd::layout::valid_layout;
use vstd::prelude::*;
use vstd::std_specs::layout_value::*;

verus! {

proof fn power_of_two_max_size(align: usize)
    requires
        align > 0,
        align & ((align - 1) as usize) == 0,
    ensures
        isize::MAX as usize % align == align - 1,
        align <= isize::MAX as usize + 1,
{
    assert(usize::BITS == 32 || usize::BITS == 64) by (bit_vector);
    if usize::BITS == 32 {
        assert(0x7fff_ffffusize % align == align - 1) by (bit_vector)
            requires
                usize::BITS == 32,
                align > 0,
                align & ((align - 1) as usize) == 0,
        ;
        assert(isize::MAX as usize == 0x7fff_ffffusize);
    } else {
        assert((0x7fff_ffff_ffff_ffffu64 as usize) % align == align - 1) by (bit_vector)
            requires
                usize::BITS == 64,
                align > 0,
                align & ((align - 1) as usize) == 0,
        ;
        assert(isize::MAX as usize == 0x7fff_ffff_ffff_ffffu64 as usize);
    }
    vstd::arithmetic::div_mod::lemma_mod_decreases(
        isize::MAX as usize as nat,
        align as nat,
    );
}

fn source_usize_is_power_of_two(value: usize) -> (result: bool)
    ensures
        result == vstd::arithmetic::power2::is_pow2(value as int),
        result ==> value > 0 && value & ((value - 1) as usize) == 0,
    decreases value,
{
    reveal(vstd::arithmetic::power2::is_pow2);
    if value == 0 {
        false
    } else if value == 1 {
        proof {
            assert(value > 0 && value & ((value - 1) as usize) == 0) by (bit_vector)
                requires value == 1,
            ;
        }
        true
    } else if value % 2 != 0 {
        false
    } else {
        let result = source_usize_is_power_of_two(value / 2);
        proof {
            if result {
                assert(value & ((value - 1) as usize) == 0) by (bit_vector)
                    requires
                        value > 1,
                        value % 2 == 0,
                        value / 2 > 0,
                        (value / 2) & (((value / 2) - 1) as usize) == 0,
                ;
                assert(value > 0 && value & ((value - 1) as usize) == 0);
            }
        }
        result
    }
}

fn source_layout_is_size_align_valid(size: usize, align: usize) -> (result: bool)
    ensures
        result == valid_layout(size, align),
{
    if source_usize_is_power_of_two(align) {
        proof {
            reveal(vstd::arithmetic::power2::is_pow2);
            assert(align > 0);
            power_of_two_max_size(align);
        }
        size <= isize::MAX as usize + 1 - align
    } else {
        false
    }
}

fn layout_error_value() -> LayoutError {
    proof {
        assert(!valid_layout(0, 0)) by {
            reveal(vstd::arithmetic::power2::is_pow2);
        }
    }
    match AllocDesc::new::<()>().align_to(0) {
        Err(error) => error,
        Ok(_) => {
            proof {
                assert(false);
            }
            vstd::pervasive::unreached()
        },
    }
}

fn source_layout_from_size_align(
    size: usize,
    align: usize,
) -> (result: Result<AllocDesc, LayoutError>)
    ensures
        valid_layout(size, align) ==> (result matches Ok(layout) && layout@ == (LayoutView {
            size,
            align,
        })),
        !valid_layout(size, align) ==> result is Err,
{
    if source_layout_is_size_align_valid(size, align) {
        unsafe { Ok(AllocDesc::from_size_align_unchecked(size, align)) }
    } else {
        Err(layout_error_value())
    }
}

} // verus!

fn main() {}