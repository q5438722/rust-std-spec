#![feature(const_index)]
#![feature(const_trait_impl)]
#![allow(dead_code)]
#![allow(unused_imports)]

use vstd::prelude::*;

verus! {

pub open spec fn ascii_lower_byte(b: u8) -> int {
    if b >= 65 && b <= 90 {
        b as int + 32
    } else {
        b as int
    }
}

pub open spec fn ascii_equal_at(lhs: Seq<u8>, rhs: Seq<u8>, i: int) -> bool {
    ascii_lower_byte(lhs[i]) == ascii_lower_byte(rhs[i])
}

pub open spec fn ascii_slices_equal(lhs: Seq<u8>, rhs: Seq<u8>) -> bool {
    lhs.len() == rhs.len()
        && forall|i: int| 0 <= i < lhs.len() ==> ascii_equal_at(lhs, rhs, i)
}

proof fn lemma_ascii_contract_form(lhs: Seq<u8>, rhs: Seq<u8>)
    ensures
        (forall|i: int| 0 <= i < lhs.len() ==> ascii_equal_at(lhs, rhs, i))
        <==>
        (forall|i: int| i >= 0 && lhs.len() > i ==>
            (if lhs[i] >= 65 && 90 >= lhs[i] {
                lhs[i] as int + 32
            } else {
                lhs[i] as int
            }) == (if rhs[i] >= 65 && 90 >= rhs[i] {
                rhs[i] as int + 32
            } else {
                rhs[i] as int
            })),
{
    let left = forall|i: int| 0 <= i < lhs.len() ==> ascii_equal_at(lhs, rhs, i);
    let right = forall|i: int| i >= 0 && lhs.len() > i ==>
        (if lhs[i] >= 65 && 90 >= lhs[i] {
            lhs[i] as int + 32
        } else {
            lhs[i] as int
        }) == (if rhs[i] >= 65 && 90 >= rhs[i] {
            rhs[i] as int + 32
        } else {
            rhs[i] as int
        });
    if left {
        assert forall|i: int| i >= 0 && lhs.len() > i implies
            (if lhs[i] >= 65 && 90 >= lhs[i] {
                lhs[i] as int + 32
            } else {
                lhs[i] as int
            }) == (if rhs[i] >= 65 && 90 >= rhs[i] {
                rhs[i] as int + 32
            } else {
                rhs[i] as int
            }) by {
            assert(ascii_equal_at(lhs, rhs, i));
            reveal(ascii_equal_at);
            reveal(ascii_lower_byte);
        }
    }
    if right {
        assert forall|i: int| 0 <= i < lhs.len()
            implies ascii_equal_at(lhs, rhs, i) by {
            reveal(ascii_equal_at);
            reveal(ascii_lower_byte);
        }
    }
}

pub assume_specification[ u8::eq_ignore_ascii_case ](
    lhs: &u8,
    rhs: &u8,
) -> (result: bool)
    ensures
        result == (ascii_lower_byte(*lhs) == ascii_lower_byte(*rhs)),
;

pub assume_specification<T, const N: usize>[ <[T]>::as_chunks::<N> ](
    slice: &[T],
) -> (ret: (&[[T; N]], &[T]))
    requires
        N != 0,
    ensures
        ret.0@.len() == slice@.len() / (N as nat),
        ret.1@.len() == slice@.len() % (N as nat),
        ret.1@.len() < N,
        slice@.len() == ret.0@.len() * (N as nat) + ret.1@.len(),
        forall|i: int| 0 <= i < ret.0@.len() ==>
            (#[trigger] ret.0@[i])@ == slice@.subrange(
                i * (N as int),
                (i + 1) * (N as int),
            ),
        forall|i: int, j: int|
            0 <= i < ret.0@.len() && 0 <= j < N ==>
                #[trigger] ret.0@[i]@[j] == slice@[i * (N as int) + j],
        ret.1@ == slice@.subrange(
            ((slice@.len() / (N as nat)) * (N as nat)) as int,
            slice@.len() as int,
        ),
;

pub assume_specification<T, const N: usize>[ <[T]>::last_chunk::<N> ](
    slice: &[T],
) -> (ret: Option<&[T; N]>)
    ensures
        slice@.len() < N ==> ret.is_none(),
        N <= slice@.len() ==> ret.is_some()
            && ret.unwrap()@ == slice@.subrange(
                slice@.len() as int - N as int,
                slice@.len() as int,
            ),
        N <= slice@.len() ==> forall|j: int| 0 <= j < N ==>
            #[trigger] ret.unwrap()@[j]
                == slice@[slice@.len() as int - N as int + j],
;

const fn source_eq_ignore_ascii_inner<const L: usize>(
    lhs: &[u8; L],
    rhs: &[u8; L],
) -> (result: bool)
    ensures
        result == (forall|j: int| 0 <= j < L ==> (
            ascii_lower_byte(lhs@[j]) == ascii_lower_byte(rhs@[j])
        )),
{
    let mut equal_ascii = true;
    let mut j = 0usize;
    while j < L
        invariant
            j <= L,
            equal_ascii == (forall|k: int| 0 <= k < j ==> (
                ascii_lower_byte(lhs@[k]) == ascii_lower_byte(rhs@[k])
            )),
        decreases
            L - j,
    {
        let ghost old_equal = equal_ascii;
        let lhs_byte = &lhs[j];
        let rhs_byte = &rhs[j];
        let byte_equal = lhs_byte.eq_ignore_ascii_case(rhs_byte);
        proof {
            assert(*lhs_byte == lhs@[j as int]);
            assert(*rhs_byte == rhs@[j as int]);
        }
        // Verus does not model boolean `&=`; the erased executable keeps it.
        #[cfg(verus_keep_ghost)]
        {
            equal_ascii = equal_ascii && byte_equal;
        }
        #[cfg(not(verus_keep_ghost))]
        {
            equal_ascii &= byte_equal;
        }
        proof {
            assert(byte_equal == (
                ascii_lower_byte(lhs@[j as int]) == ascii_lower_byte(rhs@[j as int])
            ));
            if equal_ascii {
                assert(old_equal);
                assert(byte_equal);
                assert forall|k: int| 0 <= k < j + 1 implies (
                    ascii_lower_byte(lhs@[k]) == ascii_lower_byte(rhs@[k])
                ) by {
                    if k < j {
                    } else {
                        assert(k == j);
                    }
                }
            } else {
                assert(!(forall|k: int| 0 <= k < j + 1 ==> (
                    ascii_lower_byte(lhs@[k]) == ascii_lower_byte(rhs@[k])
                ))) by {
                    if !old_equal {
                        assert(!(forall|k: int| 0 <= k < j ==> (
                            ascii_lower_byte(lhs@[k]) == ascii_lower_byte(rhs@[k])
                        )));
                        let k = choose|k: int| 0 <= k < j && (
                            ascii_lower_byte(lhs@[k]) != ascii_lower_byte(rhs@[k])
                        );
                        assert(0 <= k < j + 1);
                    } else {
                        assert(!byte_equal);
                        assert(0 <= j < j + 1);
                        assert(ascii_lower_byte(lhs@[j as int])
                            != ascii_lower_byte(rhs@[j as int]));
                    }
                }
            }
            assert(equal_ascii == (forall|k: int| 0 <= k < j + 1 ==> (
                ascii_lower_byte(lhs@[k]) == ascii_lower_byte(rhs@[k])
            )));
        }
        j += 1;
    }
    equal_ascii
}

const fn source_eq_ignore_ascii_case_simple(
    slice: &[u8],
    other: &[u8],
) -> (result: bool)
    requires
        slice@.len() == other@.len(),
    ensures
        result == (forall|i: int| 0 <= i < slice@.len() ==>
            ascii_equal_at(slice@, other@, i)),
{
    let mut a = slice;
    let mut b = other;

    // Mechanical lowering of the two simultaneous slice patterns.
    while a.len() != 0 && b.len() != 0
        invariant
            slice@.len() == other@.len(),
            a@.len() == b@.len(),
            a@.len() <= slice@.len(),
            a@ == slice@.subrange(
                slice@.len() as int - a@.len() as int,
                slice@.len() as int,
            ),
            b@ == other@.subrange(
                slice@.len() as int - a@.len() as int,
                other@.len() as int,
            ),
            forall|i: int|
                0 <= i < slice@.len() - a@.len() ==>
                    ascii_equal_at(slice@, other@, i),
        decreases
            a@.len(),
    {
        proof {
            vstd::slice::axiom_spec_len(a);
            vstd::slice::axiom_spec_len(b);
        }
        let a_len = a.len();
        let b_len = b.len();
        let first_a = &a[0];
        let first_b = &b[0];
        let rest_a = &a[1..a_len];
        let rest_b = &b[1..b_len];
        let ghost offset = slice@.len() as int - a@.len() as int;
        proof {
            assert(a@.len() > 0);
            assert(b@.len() > 0);
            assert(0 <= offset <= slice@.len());
            assert(0 <= offset <= other@.len());
            assert(*first_a == a@[0]);
            assert(*first_b == b@[0]);
            vstd::seq::lemma_seq_subrange_index(
                slice@,
                offset,
                slice@.len() as int,
                0,
            );
            vstd::seq::lemma_seq_subrange_index(
                other@,
                offset,
                other@.len() as int,
                0,
            );
            assert(a@[0] == slice@[offset]);
            assert(b@[0] == other@[offset]);
            assert(rest_a@ == a@.subrange(1, a@.len() as int));
            assert(rest_b@ == b@.subrange(1, b@.len() as int));
            vstd::seq::lemma_seq_subrange_len(a@, 1, a@.len() as int);
            vstd::seq::lemma_seq_subrange_len(b@, 1, b@.len() as int);
            vstd::seq::lemma_seq_subrange_composition(
                slice@,
                offset,
                slice@.len() as int,
                1,
                a@.len() as int,
            );
            vstd::seq::lemma_seq_subrange_composition(
                other@,
                offset,
                other@.len() as int,
                1,
                b@.len() as int,
            );
            assert(rest_a@ == slice@.subrange(offset + 1, slice@.len() as int));
            assert(rest_b@ == other@.subrange(offset + 1, other@.len() as int));
        }

        if first_a.eq_ignore_ascii_case(first_b) {
            proof {
                assert(ascii_equal_at(slice@, other@, offset));
                assert forall|i: int|
                    0 <= i < slice@.len() - rest_a@.len()
                    implies ascii_equal_at(slice@, other@, i) by {
                    if i < offset {
                    } else {
                        assert(i == offset);
                    }
                }
            }
            a = rest_a;
            b = rest_b;
        } else {
            proof {
                assert(!ascii_equal_at(slice@, other@, offset));
                assert(!(forall|i: int| 0 <= i < slice@.len() ==>
                    ascii_equal_at(slice@, other@, i)));
            }
            return false;
        }
    }

    proof {
        assert(a@.len() == 0);
        assert(forall|i: int| 0 <= i < slice@.len() ==>
            ascii_equal_at(slice@, other@, i));
    }
    true
}

#[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
const fn source_eq_ignore_ascii_case_chunks<const N: usize>(
    slice: &[u8],
    other: &[u8],
) -> (result: bool)
    requires
        N == 16,
        slice@.len() == other@.len(),
        slice@.len() >= N,
    ensures
        result == (forall|i: int| 0 <= i < slice@.len() ==>
            ascii_equal_at(slice@, other@, i)),
{
    let (self_chunks, self_rem) = slice.as_chunks::<N>();
    let (other_chunks, _) = other.as_chunks::<N>();
    proof {
        vstd::slice::axiom_spec_len(self_chunks);
        vstd::slice::axiom_spec_len(other_chunks);
        assert(self_chunks@.len() == other_chunks@.len());
        assert(self_rem@.len() == slice@.len() % (N as nat));
    }

    let mut i = 0usize;
    while i < self_chunks.len() && i < other_chunks.len()
        invariant
            N == 16,
            slice@.len() == other@.len(),
            i <= self_chunks@.len(),
            i <= other_chunks@.len(),
            self_chunks@.len() == other_chunks@.len(),
            self_rem@.len() < N,
            slice@.len()
                == self_chunks@.len() * (N as nat) + self_rem@.len(),
            forall|c: int, j: int|
                0 <= c < self_chunks@.len() && 0 <= j < N ==>
                    #[trigger] self_chunks@[c]@[j]
                        == slice@[c * (N as int) + j],
            forall|c: int, j: int|
                0 <= c < other_chunks@.len() && 0 <= j < N ==>
                    #[trigger] other_chunks@[c]@[j]
                        == other@[c * (N as int) + j],
            forall|k: int| 0 <= k < (i as int) * 16 ==>
                ascii_equal_at(slice@, other@, k),
        decreases
            self_chunks@.len() - i,
    {
        proof {
            assert(i < self_chunks@.len());
            assert(i < other_chunks@.len());
            assert(N as int == 16);
            assert((i as int + 1) * (N as int) <= slice@.len());
            assert((i as int + 1) * (N as int) <= other@.len());
        }
        if !source_eq_ignore_ascii_inner(&self_chunks[i], &other_chunks[i]) {
            proof {
                assert(!(forall|j: int| 0 <= j < N ==> (
                    ascii_lower_byte(self_chunks@[i as int]@[j])
                        == ascii_lower_byte(other_chunks@[i as int]@[j])
                )));
                let j = choose|j: int| 0 <= j < N && (
                    ascii_lower_byte(self_chunks@[i as int]@[j])
                        != ascii_lower_byte(other_chunks@[i as int]@[j])
                );
                let k = (i as int) * 16 + j;
                assert(self_chunks@[i as int]@[j] == slice@[k]);
                assert(other_chunks@[i as int]@[j] == other@[k]);
                assert(0 <= k < slice@.len());
                assert(!ascii_equal_at(slice@, other@, k));
                assert(!(forall|q: int| 0 <= q < slice@.len() ==>
                    ascii_equal_at(slice@, other@, q)));
            }
            return false;
        }
        proof {
            assert forall|k: int| 0 <= k < (i as int + 1) * 16
                implies ascii_equal_at(slice@, other@, k) by {
                if k < (i as int) * 16 {
                } else {
                    let j = k - (i as int) * 16;
                    assert(0 <= j < N);
                    assert(self_chunks@[i as int]@[j] == slice@[k]);
                    assert(other_chunks@[i as int]@[j] == other@[k]);
                }
            }
        }
        i += 1;
    }

    proof {
        assert(i == self_chunks@.len());
        assert(i == other_chunks@.len());
    }

    #[cfg(verus_keep_ghost)]
    {
        proof {
            assert(slice@.len() >= N);
        }
    }
    #[cfg(not(verus_keep_ghost))]
    {
        debug_assert!(slice.len() >= N);
    }

    if !self_rem.is_empty() {
        let a_last = slice.last_chunk::<N>();
        let b_last = other.last_chunk::<N>();
        if let (Some(a_rem), Some(b_rem)) = (a_last, b_last) {
            if !source_eq_ignore_ascii_inner(a_rem, b_rem) {
                proof {
                    assert(!(forall|j: int| 0 <= j < N ==> (
                        ascii_lower_byte(a_rem@[j]) == ascii_lower_byte(b_rem@[j])
                    )));
                    let j = choose|j: int| 0 <= j < N && (
                        ascii_lower_byte(a_rem@[j]) != ascii_lower_byte(b_rem@[j])
                    );
                    let k = slice@.len() as int - N as int + j;
                    assert(a_rem@[j] == slice@[k]);
                    assert(b_rem@[j] == other@[k]);
                    assert(0 <= k < slice@.len());
                    assert(!ascii_equal_at(slice@, other@, k));
                    assert(!(forall|q: int| 0 <= q < slice@.len() ==>
                        ascii_equal_at(slice@, other@, q)));
                }
                return false;
            }
            proof {
                assert forall|k: int|
                    slice@.len() as int - N as int <= k < slice@.len()
                    implies ascii_equal_at(slice@, other@, k) by {
                    let j = k - (slice@.len() as int - N as int);
                    assert(0 <= j < N);
                    assert(a_rem@[j] == slice@[k]);
                    assert(b_rem@[j] == other@[k]);
                }
            }
        }
        proof {
            assert(a_last.is_some());
            assert(b_last.is_some());
            assert(forall|k: int|
                slice@.len() as int - N as int <= k < slice@.len()
                ==> ascii_equal_at(slice@, other@, k));
        }
    }

    proof {
        assert forall|k: int| 0 <= k < slice@.len()
            implies ascii_equal_at(slice@, other@, k) by {
            if k < (self_chunks@.len() as int) * 16 {
            } else if self_rem@.len() == 0 {
                assert(false);
            } else {
                assert(slice@.len() as int - N as int <= k);
            }
        }
    }
    true
}

#[must_use]
#[inline]
pub const fn source_eq_ignore_ascii_case(
    slice: &[u8],
    other: &[u8],
) -> (result: bool)
    ensures
        result == (
            slice@.len() == other@.len()
            && forall|i: int| i >= 0 && slice@.len() > i ==>
                (if slice@[i] >= 65 && 90 >= slice@[i] {
                    slice@[i] as int + 32
                } else {
                    slice@[i] as int
                }) == (if other@[i] >= 65 && 90 >= other@[i] {
                    other@[i] as int + 32
                } else {
                    other@[i] as int
                })
        ),
{
    if slice.len() != other.len() {
        return false;
    }

    #[cfg(all(target_arch = "x86_64", target_feature = "sse2"))]
    {
        const CHUNK_SIZE: usize = 16;
        if slice.len() >= CHUNK_SIZE {
            let result =
                source_eq_ignore_ascii_case_chunks::<CHUNK_SIZE>(slice, other);
            proof {
                lemma_ascii_contract_form(slice@, other@);
            }
            return result;
        }
    }

    let result = source_eq_ignore_ascii_case_simple(slice, other);
    proof {
        lemma_ascii_contract_form(slice@, other@);
    }
    result
}

}

fn main() {}