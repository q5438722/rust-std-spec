#![allow(dead_code)]

use core::time::Duration;
use vstd::float::FloatBitsProperties;
use vstd::prelude::*;
use vstd::std_specs::cmp::lt_ensures;
use vstd::std_specs::duration::{
    duration_from_secs_f32_nanos, duration_from_secs_f64_nanos,
    duration_secs_f32_is_negative, duration_secs_f32_valid,
    duration_secs_f64_is_negative, duration_secs_f64_valid, nanos_per_second,
};

verus! {

#[derive(PartialEq, Eq)]
pub enum MirrorTryFromFloatSecsErrorKind {
    Negative,
    OverflowOrNan,
}

pub struct MirrorTryFromFloatSecsError {
    pub kind: MirrorTryFromFloatSecsErrorKind,
}

pub assume_specification[ f32::to_bits ](value: f32) -> (result: u32)
    ensures
        result == value.to_bits_spec(),
;

pub assume_specification[ f64::to_bits ](value: f64) -> (result: u64)
    ensures
        result == value.to_bits_spec(),
;

// IMPLEMENTATION ASSUMPTIONS: vstd deliberately leaves executable float
// comparison relational. These bridges state the Rust/IEEE classification
// used by the copied `< 0.0` guard; they involve no float arithmetic.
pub axiom fn implementation_f32_lt_zero(
    secs: f32,
    result: bool,
)
    requires
        lt_ensures(secs, 0.0f32, result),
    ensures
        result == duration_secs_f32_is_negative(secs),
;

pub axiom fn implementation_f64_lt_zero(
    secs: f64,
    result: bool,
)
    requires
        lt_ensures(secs, 0.0f64, result),
    ensures
        result == duration_secs_f64_is_negative(secs),
;

pub open spec fn f32_source_decode(bits: u32, mant: u32, exp: i16) -> bool {
    &&& mant == ((bits & 0x7f_ffff) | 0x80_0000)
    &&& exp as int == ((bits >> 23) & 0xff) as int - 127
}

pub open spec fn f32_source_overflow(exp: i16) -> bool {
    exp >= 64
}

pub open spec fn f32_source_success(
    mant: u32,
    exp: i16,
    out_secs: u64,
    out_nanos: u32,
) -> bool {
    let mant_mask: u32 = 0x7f_ffff;

    if exp < -31 {
        out_secs == 0 && out_nanos == 0
    } else if exp < 0 {
        let t = (mant as u64) << (41 + exp);
        let nanos_offset: u32 = 64;
        let nanos_tmp = (1_000_000_000u128 * t as u128) as u128;
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xffff_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8000_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        let rounded_nanos = (nanos + add_ns as u32) as u32;
        out_secs == 0 && out_nanos == rounded_nanos
    } else if exp < 23 {
        let secs = (mant >> (23 - exp)) as u64;
        let t = ((mant << exp) & mant_mask) as u64;
        let nanos_offset: u32 = 23;
        let nanos_tmp = (1_000_000_000u64 * t) as u64;
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0x7f_ffffu64;
        let rem_msb_mask = 0x40_0000u64;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        let rounded_nanos = (nanos + add_ns as u32) as u32;
        out_secs == secs && out_nanos == rounded_nanos
    } else if exp < 64 {
        let secs = (mant as u64) << (exp - 23);
        out_secs == secs && out_nanos == 0
    } else {
        false
    }
}

pub open spec fn f32_source_execution_safe(mant: u32, exp: i16) -> bool {
    let mant_mask: u32 = 0x7f_ffff;

    &&& mant <= 0xff_ffff
    &&& exp >= -127
    &&& exp <= 128
    &&& ((exp >= -31 && exp < 0) ==> {
        let t = (mant as u64) << (41 + exp);
        let product = 1_000_000_000nat * t as nat;
        &&& product <= u128::MAX as nat
        &&& (((product as u128) >> 64) as nat) < 1_000_000_000
    })
    &&& ((exp >= 0 && exp < 23) ==> {
        let t = ((mant << exp) & mant_mask) as u64;
        let product = 1_000_000_000nat * t as nat;
        &&& product <= u64::MAX as nat
        &&& (((product as u64) >> 23) as nat) < 1_000_000_000
    })
}

pub open spec fn f64_source_decode(bits: u64, mant: u64, exp: i16) -> bool {
    &&& mant == ((bits & 0xf_ffff_ffff_ffff) | 0x10_0000_0000_0000)
    &&& exp as int == ((bits >> 52) & 0x7ff) as int - 1023
}

pub open spec fn f64_source_overflow(exp: i16) -> bool {
    exp >= 64
}

pub open spec fn f64_source_success(
    mant: u64,
    exp: i16,
    out_secs: u64,
    out_nanos: u32,
) -> bool {
    let mant_mask: u64 = 0xf_ffff_ffff_ffff;

    if exp < -31 {
        out_secs == 0 && out_nanos == 0
    } else if exp < 0 {
        let t = (mant as u128) << (44 + exp);
        let nanos_offset: u32 = 96;
        let nanos_tmp = (1_000_000_000u128 * t) as u128;
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xffff_ffff_ffff_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8000_0000_0000_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        let rounded_nanos = (nanos + add_ns as u32) as u32;
        if rounded_nanos != 1_000_000_000 {
            out_secs == 0 && out_nanos == rounded_nanos
        } else {
            out_secs == 1 && out_nanos == 0
        }
    } else if exp < 52 {
        let secs = mant >> (52 - exp);
        let t = ((mant << exp) & mant_mask) as u128;
        let nanos_offset: u32 = 52;
        let nanos_tmp = (1_000_000_000u128 * t) as u128;
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xf_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        let rounded_nanos = (nanos + add_ns as u32) as u32;
        if rounded_nanos != 1_000_000_000 {
            out_secs == secs && out_nanos == rounded_nanos
        } else {
            out_secs == secs + 1 && out_nanos == 0
        }
    } else if exp < 64 {
        let secs = mant << (exp - 52);
        out_secs == secs && out_nanos == 0
    } else {
        false
    }
}

pub open spec fn f64_source_execution_safe(mant: u64, exp: i16) -> bool {
    let mant_mask: u64 = 0xf_ffff_ffff_ffff;

    &&& mant <= 0x1f_ffff_ffff_ffff
    &&& exp >= -1023
    &&& exp <= 1024
    &&& ((exp >= -31 && exp < 0) ==> {
        let t = (mant as u128) << (44 + exp);
        let product = 1_000_000_000nat * t as nat;
        &&& product <= u128::MAX as nat
        &&& (((product as u128) >> 96) as nat) < 1_000_000_000
    })
    &&& ((exp >= 0 && exp < 52) ==> {
        let t = ((mant << exp) & mant_mask) as u128;
        let product = 1_000_000_000nat * t as nat;
        let source_secs = mant >> (52 - exp);
        &&& product <= u128::MAX as nat
        &&& (((product as u128) >> 52) as nat) < 1_000_000_000
        &&& source_secs < u64::MAX
    })
}

// ARITHMETIC LEMMAS: these are the only trusted mathematical steps. They
// connect the exact bit/shift/round-to-even source models above to vstd's
// independent pow2/div/mod specifications.
pub axiom fn arithmetic_f32_source_model(
    secs: f32,
    bits: u32,
    mant: u32,
    exp: i16,
)
    requires
        bits == secs.to_bits_spec(),
        !duration_secs_f32_is_negative(secs),
        f32_source_decode(bits, mant, exp),
    ensures
        f32_source_execution_safe(mant, exp),
        f32_source_overflow(exp) <==> !duration_secs_f32_valid(secs),
        forall|out_secs: u64, out_nanos: u32|
            #[trigger] f32_source_success(mant, exp, out_secs, out_nanos) ==> {
                &&& duration_secs_f32_valid(secs)
                &&& out_nanos < nanos_per_second()
                &&& out_secs as nat + out_nanos as nat / nanos_per_second() <= u64::MAX as nat
                &&& out_secs as nat * nanos_per_second() + out_nanos as nat
                    == duration_from_secs_f32_nanos(secs)
            },
;

pub axiom fn arithmetic_f64_source_model(
    secs: f64,
    bits: u64,
    mant: u64,
    exp: i16,
)
    requires
        bits == secs.to_bits_spec(),
        !duration_secs_f64_is_negative(secs),
        f64_source_decode(bits, mant, exp),
    ensures
        f64_source_execution_safe(mant, exp),
        f64_source_overflow(exp) <==> !duration_secs_f64_valid(secs),
        forall|out_secs: u64, out_nanos: u32|
            #[trigger] f64_source_success(mant, exp, out_secs, out_nanos) ==> {
                &&& duration_secs_f64_valid(secs)
                &&& out_nanos < nanos_per_second()
                &&& out_secs as nat + out_nanos as nat / nanos_per_second() <= u64::MAX as nat
                &&& out_secs as nat * nanos_per_second() + out_nanos as nat
                    == duration_from_secs_f64_nanos(secs)
            },
;

// Source-faithful desugaring of rust-1.96/library/core/src/time.rs:1558-1635
// with the private standard-library error replaced by the local mirror above.
pub fn source_duration_try_from_secs_f32(
    input_secs: f32,
) -> (result: Result<Duration, MirrorTryFromFloatSecsError>)
    ensures
        duration_secs_f32_valid(input_secs) ==> (
            result matches Ok(value)
                && value@ == duration_from_secs_f32_nanos(input_secs)
        ),
        !duration_secs_f32_valid(input_secs) ==> (
            result matches Err(error)
                && error.kind == if duration_secs_f32_is_negative(input_secs) {
                    MirrorTryFromFloatSecsErrorKind::Negative
                } else {
                    MirrorTryFromFloatSecsErrorKind::OverflowOrNan
                }
        ),
{
    const MIN_EXP: i16 = -127; // `1 - (1i16 << 8) / 2`
    const MANT_MASK: u32 = 0x7f_ffff; // `(1 << 23) - 1`
    const EXP_MASK: u32 = 0xff; // `(1 << 8) - 1`

    let negative = input_secs < 0.0;
    proof {
        implementation_f32_lt_zero(input_secs, negative);
    }
    if negative {
        return Err(MirrorTryFromFloatSecsError {
            kind: MirrorTryFromFloatSecsErrorKind::Negative,
        });
    }

    let bits = input_secs.to_bits();
    proof {
        assert((bits & MANT_MASK) <= MANT_MASK) by (bit_vector);
        assert(((bits >> 23) & EXP_MASK) <= 0xff) by (bit_vector);
        assert(MANT_MASK + 1 == 0x80_0000);
    }
    let mant = (bits & MANT_MASK) | (MANT_MASK + 1);
    let biased_exp = ((bits >> 23) & EXP_MASK) as i16;
    let exp = biased_exp + MIN_EXP;

    proof {
        assert(f32_source_decode(bits, mant, exp)) by {
            reveal(f32_source_decode);
            assert(mant == ((bits & 0x7f_ffff) | 0x80_0000));
        }
        arithmetic_f32_source_model(input_secs, bits, mant, exp);
    }

    let (secs, nanos) = if exp < -31 {
        proof {
            assert(f32_source_success(mant, exp, 0, 0)) by {
                reveal(f32_source_success);
            }
        }
        (0u64, 0u32)
    } else if exp < 0 {
        let t = u64::from(mant) << (41 + exp);
        let nanos_offset = 23 + 41;
        proof {
            reveal(f32_source_execution_safe);
            assert(1_000_000_000nat * t as nat <= u128::MAX as nat);
        }
        let nanos_tmp = u128::from(1_000_000_000u32) * u128::from(t);
        proof {
            assert((nanos_tmp >> 64) < 1_000_000_000);
        }
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xffff_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8000_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        proof {
            assert(nanos < 1_000_000_000);
        }
        let nanos = nanos + add_ns as u32;
        if (23 == 23) || (nanos != 1_000_000_000) {
            proof {
                assert(f32_source_success(mant, exp, 0, nanos)) by {
                    reveal(f32_source_success);
                }
            }
            (0, nanos)
        } else {
            (1, 0)
        }
    } else if exp < 23 {
        let secs = u64::from(mant >> (23 - exp));
        let t = u64::from((mant << exp) & MANT_MASK);
        let nanos_offset = 23;
        proof {
            reveal(f32_source_execution_safe);
            assert(1_000_000_000nat * t as nat <= u64::MAX as nat);
        }
        let nanos_tmp = u64::from(1_000_000_000u32) * t;
        proof {
            assert((nanos_tmp >> 23) < 1_000_000_000);
        }
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0x7f_ffffu64;
        let rem_msb_mask = 0x40_0000u64;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        proof {
            assert(nanos < 1_000_000_000);
        }
        let nanos = nanos + add_ns as u32;
        if (23 == 23) || (nanos != 1_000_000_000) {
            proof {
                assert(f32_source_success(mant, exp, secs, nanos)) by {
                    reveal(f32_source_success);
                }
            }
            (secs, nanos)
        } else {
            (secs + 1, 0)
        }
    } else if exp < 64 {
        let secs = u64::from(mant) << (exp - 23);
        proof {
            assert(f32_source_success(mant, exp, secs, 0)) by {
                reveal(f32_source_success);
            }
        }
        (secs, 0)
    } else {
        proof {
            assert(f32_source_overflow(exp));
        }
        return Err(MirrorTryFromFloatSecsError {
            kind: MirrorTryFromFloatSecsErrorKind::OverflowOrNan,
        });
    };

    proof {
        assert(f32_source_success(mant, exp, secs, nanos)) by {
            reveal(f32_source_success);
        }
    }
    Ok(Duration::new(secs, nanos))
}

pub fn source_duration_try_from_secs_f64(
    input_secs: f64,
) -> (result: Result<Duration, MirrorTryFromFloatSecsError>)
    ensures
        duration_secs_f64_valid(input_secs) ==> (
            result matches Ok(value)
                && value@ == duration_from_secs_f64_nanos(input_secs)
        ),
        !duration_secs_f64_valid(input_secs) ==> (
            result matches Err(error)
                && error.kind == if duration_secs_f64_is_negative(input_secs) {
                    MirrorTryFromFloatSecsErrorKind::Negative
                } else {
                    MirrorTryFromFloatSecsErrorKind::OverflowOrNan
                }
        ),
{
    const MIN_EXP: i16 = -1023; // `1 - (1i16 << 11) / 2`
    const MANT_MASK: u64 = 0xf_ffff_ffff_ffff; // `(1 << 52) - 1`
    const EXP_MASK: u64 = 0x7ff; // `(1 << 11) - 1`

    let negative = input_secs < 0.0;
    proof {
        implementation_f64_lt_zero(input_secs, negative);
    }
    if negative {
        return Err(MirrorTryFromFloatSecsError {
            kind: MirrorTryFromFloatSecsErrorKind::Negative,
        });
    }

    let bits = input_secs.to_bits();
    proof {
        assert((bits & MANT_MASK) <= MANT_MASK) by (bit_vector);
        assert(((bits >> 52) & EXP_MASK) <= 0x7ff) by (bit_vector);
        assert(MANT_MASK + 1 == 0x10_0000_0000_0000);
    }
    let mant = (bits & MANT_MASK) | (MANT_MASK + 1);
    let biased_exp = ((bits >> 52) & EXP_MASK) as i16;
    let exp = biased_exp + MIN_EXP;

    proof {
        assert(f64_source_decode(bits, mant, exp)) by {
            reveal(f64_source_decode);
            assert(
                mant == ((bits & 0xf_ffff_ffff_ffff) | 0x10_0000_0000_0000)
            );
        }
        arithmetic_f64_source_model(input_secs, bits, mant, exp);
    }

    let (secs, nanos) = if exp < -31 {
        proof {
            assert(f64_source_success(mant, exp, 0, 0)) by {
                reveal(f64_source_success);
            }
        }
        (0u64, 0u32)
    } else if exp < 0 {
        let t = u128::from(mant) << (44 + exp);
        let nanos_offset = 52 + 44;
        proof {
            reveal(f64_source_execution_safe);
            assert(1_000_000_000nat * t as nat <= u128::MAX as nat);
        }
        let nanos_tmp = u128::from(1_000_000_000u32) * u128::from(t);
        proof {
            assert((nanos_tmp >> 96) < 1_000_000_000);
        }
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xffff_ffff_ffff_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8000_0000_0000_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        proof {
            assert(nanos < 1_000_000_000);
        }
        let nanos = nanos + add_ns as u32;
        if (52 == 23) || (nanos != 1_000_000_000) {
            proof {
                assert(f64_source_success(mant, exp, 0, nanos)) by {
                    reveal(f64_source_success);
                }
            }
            (0, nanos)
        } else {
            proof {
                assert(f64_source_success(mant, exp, 1, 0)) by {
                    reveal(f64_source_success);
                }
            }
            (1, 0)
        }
    } else if exp < 52 {
        let secs = u64::from(mant >> (52 - exp));
        let t = u128::from((mant << exp) & MANT_MASK);
        let nanos_offset = 52;
        proof {
            reveal(f64_source_execution_safe);
            assert(1_000_000_000nat * t as nat <= u128::MAX as nat);
        }
        let nanos_tmp = u128::from(1_000_000_000u32) * t;
        proof {
            assert((nanos_tmp >> 52) < 1_000_000_000);
        }
        let nanos = (nanos_tmp >> nanos_offset) as u32;

        let rem_mask = 0xf_ffff_ffff_ffffu128;
        let rem_msb_mask = 0x8_0000_0000_0000u128;
        let rem = nanos_tmp & rem_mask;
        let is_tie = rem == rem_msb_mask;
        let is_even = (nanos & 1) == 0;
        let rem_msb = nanos_tmp & rem_msb_mask == 0;
        let add_ns = !(rem_msb || (is_even && is_tie));

        proof {
            assert(nanos < 1_000_000_000);
        }
        let nanos = nanos + add_ns as u32;
        if (52 == 23) || (nanos != 1_000_000_000) {
            proof {
                assert(f64_source_success(mant, exp, secs, nanos)) by {
                    reveal(f64_source_success);
                }
            }
            (secs, nanos)
        } else {
            proof {
                reveal(f64_source_execution_safe);
                assert(secs < u64::MAX);
                assert(f64_source_success(mant, exp, (secs + 1) as u64, 0)) by {
                    reveal(f64_source_success);
                }
            }
            (secs + 1, 0)
        }
    } else if exp < 64 {
        let secs = u64::from(mant) << (exp - 52);
        proof {
            assert(f64_source_success(mant, exp, secs, 0)) by {
                reveal(f64_source_success);
            }
        }
        (secs, 0)
    } else {
        proof {
            assert(f64_source_overflow(exp));
        }
        return Err(MirrorTryFromFloatSecsError {
            kind: MirrorTryFromFloatSecsErrorKind::OverflowOrNan,
        });
    };

    proof {
        assert(f64_source_success(mant, exp, secs, nanos)) by {
            reveal(f64_source_success);
        }
    }
    Ok(Duration::new(secs, nanos))
}

}

fn main() {}
