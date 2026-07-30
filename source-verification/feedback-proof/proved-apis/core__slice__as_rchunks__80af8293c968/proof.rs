#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;
use vstd::seq_lib::*;

#[cfg(verus_keep_ghost)]
macro_rules! panic {
    ($($arg:tt)*) => {
        vstd::vpanic!($($arg)*)
    };
}

verus! {

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks_unchecked::<N> ](
    slice: &[T],
) -> (chunks: &[[T; N]])
    requires
        N != 0,
        slice@.len() % (N as nat) == 0,
    ensures
        chunks@.len() == slice@.len() / (N as nat),
        forall|i: int| 0 <= i < chunks@.len() ==>
            (#[trigger] chunks@[i])@ == slice@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ),
;

pub fn source_core_slice_as_rchunks<T, const N: usize>(
    slice: &[T],
) -> (ret: (&[T], &[[T; N]]))
    requires
        N != 0,
    ensures
        ret.0@ == slice@.subrange(
            0,
            (slice@.len() % (N as nat)) as int,
        ),
        ret.1@ == Seq::new(
            slice@.len() / (N as nat),
            |i: int| choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    (slice@.len() % (N as nat)) as int + i * (N as int),
                    (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
                ),
        ),
        forall|i: int| i >= 0 && ret.1@.len() > i ==>
            (#[trigger] ret.1@[i])@ == slice@.subrange(
                (slice@.len() % (N as nat)) as int + i * (N as int),
                (slice@.len() % (N as nat)) as int + (i + 1) * (N as int),
            ),
{
    if !(N != 0) {
        panic!("chunk size must be non-zero");
    }
    let len = slice.len() / N;
    proof {
        vstd::arithmetic::div_mod::lemma_fundamental_div_mod(
            slice@.len() as int,
            N as int,
        );
        vstd::arithmetic::div_mod::lemma_mod_division_less_than_divisor(
            slice@.len() as int,
            N as int,
        );
        assert(
            (slice@.len() / (N as nat)) * (N as nat) <= slice@.len()
        ) by (nonlinear_arith);
        assert(len as nat == slice@.len() / (N as nat));
    }
    let split_index = slice.len() - len * N;
    proof {
        let q = slice@.len() / (N as nat);
        let r = slice@.len() % (N as nat);
        vstd::arithmetic::div_mod::lemma_fundamental_div_mod(
            slice@.len() as int,
            N as int,
        );
        assert(slice@.len() == (N as nat) * q + r);
        assert(
            q as int == (slice@.len() as int) / (N as int)
        );
        assert(
            r as int == (slice@.len() as int) % (N as int)
        );
        assert(
            slice@.len() as int
                == (N as int) * (q as int) + (r as int)
        );
        assert(len as nat == q);
        assert(len * N <= slice.len());
        assert((len * N) as int == (len as int) * (N as int));
        assert(
            split_index as int
                == (slice.len() as int) - ((len * N) as int)
        );
        assert(slice.len() as int == slice@.len() as int);
        assert(len as int == q as int);
        assert(
            (N as int) * (q as int) == (q as int) * (N as int)
        ) by (nonlinear_arith);
        assert(
            slice@.len() as int
                == (q as int) * (N as int) + (r as int)
        );
        assert(split_index as int == r as int);
    }
    let (remainder, multiple_of_n) = slice.split_at(split_index);
    proof {
        let q = slice@.len() / (N as nat);
        let r = slice@.len() % (N as nat);
        vstd::arithmetic::div_mod::lemma_fundamental_div_mod(
            slice@.len() as int,
            N as int,
        );
        assert(slice@.len() == (N as nat) * q + r);
        assert(split_index as nat == r);
        assert(remainder@ == slice@.subrange(
            0,
            (slice@.len() % (N as nat)) as int,
        ));
        assert(multiple_of_n@ == slice@.subrange(
            (slice@.len() % (N as nat)) as int,
            slice@.len() as int,
        ));
        vstd::seq::lemma_seq_subrange_len(
            slice@,
            r as int,
            slice@.len() as int,
        );
        assert(
            multiple_of_n@.len() as int
                == (slice@.len() as int) - (r as int)
        );
        assert(q as int == (slice@.len() as int) / (N as int));
        assert(r as int == (slice@.len() as int) % (N as int));
        assert(
            slice@.len() as int
                == (N as int) * (q as int) + (r as int)
        );
        assert(
            (N as int) * (q as int) == (q as int) * (N as int)
        ) by (nonlinear_arith);
        assert(
            (slice@.len() as int) - (r as int)
                == (q as int) * (N as int)
        );
        assert(
            multiple_of_n@.len() as int
                == (q as int) * (N as int)
        );
        assert(
            (q * (N as nat)) as int == (q as int) * (N as int)
        );
        assert(multiple_of_n@.len() == q * (N as nat));
        vstd::arithmetic::div_mod::lemma_mod_multiples_basic(
            q as int,
            N as int,
        );
        assert(multiple_of_n@.len() % (N as nat) == 0);
    }
    let array_slice = unsafe { multiple_of_n.as_chunks_unchecked() };
    proof {
        let q = slice@.len() / (N as nat);
        let r = slice@.len() % (N as nat);
        assert(multiple_of_n@.len() == q * (N as nat));
        assert(array_slice@.len() == q) by {
            vstd::arithmetic::div_mod::lemma_div_by_multiple(
                len as int,
                N as int,
            );
        }
        assert forall|i: int| 0 <= i < array_slice@.len() implies
            (#[trigger] array_slice@[i])@ == slice@.subrange(
                r as int + i * (N as int),
                r as int + (i + 1) * (N as int),
            ) by {
            assert(array_slice@[i]@ == multiple_of_n@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ));
            assert(0 <= i);
            assert(i < array_slice@.len());
            assert(array_slice@.len() == q);
            assert(i + 1 <= q as int);
            assert(
                (q * (N as nat)) as int == (q as int) * (N as int)
            );
            assert(
                multiple_of_n@.len() as int == (q as int) * (N as int)
            );
            assert(N as int > 0);
            vstd::arithmetic::mul::lemma_mul_nonnegative(i, N as int);
            vstd::arithmetic::mul::lemma_mul_inequality(
                i,
                i + 1,
                N as int,
            );
            vstd::arithmetic::mul::lemma_mul_inequality(
                i + 1,
                q as int,
                N as int,
            );
            assert(
                0 <= i * (N as int)
                    <= (i + 1) * (N as int)
                    <= multiple_of_n@.len() as int
            );
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                r as int,
                slice@.len() as int,
                i * (N as int),
                (i + 1) * (N as int),
            );
        };
        let expected = Seq::new(
            q,
            |i: int| choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    r as int + i * (N as int),
                    r as int + (i + 1) * (N as int),
                ),
        );
        assert_seqs_equal!(array_slice@ == expected, i => {
            let actual = array_slice@[i];
            assert(exists|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    r as int + i * (N as int),
                    r as int + (i + 1) * (N as int),
                )
            ) by {
                let chunk = actual;
            };
            let chosen = choose|chunk: [T; N]|
                chunk@ == slice@.subrange(
                    r as int + i * (N as int),
                    r as int + (i + 1) * (N as int),
                );
            assert(actual@ == chosen@);
            assert(actual =~= chosen);
        });
    }
    (remainder, array_slice)
}

} // verus!

fn main() {}