#![allow(dead_code, unexpected_cfgs)]

use vstd::prelude::*;
use vstd::seq_lib::*;

#[cfg(verus_keep_ghost)]
macro_rules! assert {
    ($condition:expr, $message:expr $(,)?) => {
        proof! {
            assert($condition);
        }
    };
}

verus! {

proof fn lemma_subrange_of_prefix<T>(
    values: Seq<T>,
    prefix_end: int,
    start: int,
    end: int,
)
    requires
        0 <= start <= end <= prefix_end <= values.len(),
    ensures
        values.subrange(0, prefix_end).subrange(start, end)
            == values.subrange(start, end),
{
    assert_seqs_equal!(
        values.subrange(0, prefix_end).subrange(start, end)
            == values.subrange(start, end)
    );
}

pub assume_specification<T>[ <[T]>::split_at_unchecked ](
    slice: &[T],
    mid: usize,
) -> (ret: (&[T], &[T]))
    requires
        mid <= slice.len(),
    ensures
        ret.0@ == slice@.subrange(0, mid as int),
        ret.1@ == slice@.subrange(mid as int, slice@.len() as int),
;

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

pub const fn source_core_slice_as_chunks<T, const N: usize>(
    slice: &[T],
) -> (ret: (&[[T; N]], &[T]))
    requires
        N != 0,
    ensures
        {
            let chunks = choose|candidate: Seq<[T; N]>| {
                &&& candidate.len() == slice@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == slice@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            };
            &&& ret.0@ == chunks
            &&& ret.0@.len() == slice@.len() / (N as nat)
            &&& ret.1@.len() == slice@.len() % (N as nat)
            &&& slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len()
            &&& forall|i: int| 0 <= i < ret.0@.len() ==>
                (#[trigger] ret.0@[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                )
            &&& ret.1@ == slice@.subrange(
                ((slice@.len() / (N as nat)) * (N as nat)) as int,
                slice@.len() as int,
            )
        },
{
    assert!(N != 0, "chunk size must be non-zero");
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
    }
    let len_rounded_down = slice.len() / N * N;
    let ghost quotient = slice@.len() / (N as nat);
    proof {
        assert(
            len_rounded_down as int
                == (slice@.len() / (N as nat)) * (N as nat)
        );
        assert(
            len_rounded_down as nat == quotient * (N as nat)
        );
        assert(len_rounded_down <= slice.len());
    }
    let (multiple_of_n, remainder) =
        unsafe { slice.split_at_unchecked(len_rounded_down) };
    proof {
        vstd::arithmetic::div_mod::lemma_mod_multiples_basic(
            slice@.len() as int / N as int,
            N as int,
        );
        assert(multiple_of_n@.len() == len_rounded_down as nat);
        assert(multiple_of_n@.len() % (N as nat) == 0);
    }
    let array_slice = unsafe { multiple_of_n.as_chunks_unchecked() };
    proof {
        vstd::arithmetic::div_mod::lemma_div_by_multiple(
            slice@.len() as int / N as int,
            N as int,
        );
        assert(
            array_slice@.len() == quotient
        );
        assert(
            len_rounded_down as nat
                == array_slice@.len() * (N as nat)
        );
        assert forall|i: int| 0 <= i < array_slice@.len() implies
            (#[trigger] array_slice@[i])@ == slice@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ) by {
            assert(0 < N as int);
            assert(0 <= i);
            assert(i + 1 <= array_slice@.len());
            assert(array_slice@.len() == quotient);
            assert(
                len_rounded_down as int
                    == (array_slice@.len() as int) * (N as int)
            );
            vstd::arithmetic::mul::lemma_mul_nonnegative(
                i,
                N as int,
            );
            vstd::arithmetic::mul::lemma_mul_left_inequality(
                N as int,
                i + 1,
                array_slice@.len() as int,
            );
            vstd::arithmetic::mul::lemma_mul_left_inequality(
                N as int,
                i,
                i + 1,
            );
            vstd::arithmetic::mul::lemma_mul_is_commutative(
                N as int,
                i,
            );
            vstd::arithmetic::mul::lemma_mul_is_commutative(
                N as int,
                i + 1,
            );
            vstd::arithmetic::mul::lemma_mul_is_commutative(
                N as int,
                array_slice@.len() as int,
            );
            assert(0 <= i * (N as int));
            assert(i * (N as int) <= (i + 1) * (N as int));
            assert(
                (i + 1) * (N as int) <= len_rounded_down as int
            );
            assert(len_rounded_down as int <= slice@.len());
            lemma_subrange_of_prefix(
                slice@,
                len_rounded_down as int,
                i * (N as int),
                (i + 1) * (N as int),
            );
        };
        assert(
            exists|candidate: Seq<[T; N]>| {
                &&& candidate.len() == slice@.len() / (N as nat)
                &&& forall|i: int| 0 <= i < candidate.len() ==>
                    (#[trigger] candidate[i])@ == slice@.subrange(
                        i * (N as int),
                        (i + 1) * (N as int),
                    )
            }
        ) by {
            let candidate = array_slice@;
            assert(candidate.len() == slice@.len() / (N as nat));
            assert forall|i: int| 0 <= i < candidate.len() implies
                (#[trigger] candidate[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                ) by {
                assert(candidate[i] == array_slice@[i]);
            };
        };
        let chunks = choose|candidate: Seq<[T; N]>| {
            &&& candidate.len() == slice@.len() / (N as nat)
            &&& forall|i: int| 0 <= i < candidate.len() ==>
                (#[trigger] candidate[i])@ == slice@.subrange(
                    i * (N as int),
                    (i + 1) * (N as int),
                )
        };
        assert(chunks.len() == slice@.len() / (N as nat));
        assert forall|i: int| 0 <= i < chunks.len() implies
            (#[trigger] chunks[i])@ == slice@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ) by {
            assert(chunks[i]@ == slice@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ));
        };
        assert_seqs_equal!(array_slice@ == chunks, i => {
            assert(array_slice@[i]@ == chunks[i]@);
            assert(array_slice@[i] =~= chunks[i]);
            assert(array_slice@[i] == chunks[i]);
        });
    }
    (array_slice, remainder)
}

} // verus!

fn main() {}