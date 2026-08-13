#[allow(unused_imports)]
use vstd::prelude::*;
#[allow(unused_imports)]
use vstd::seq::*;
#[allow(unused_imports)]
use vstd::view::*;

verus! {

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExChunksExact<'a, T: 'a>(core::slice::ChunksExact<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::reject_recursive_types(T)]
pub struct ExRChunksExact<'a, T: 'a>(core::slice::RChunksExact<'a, T>);

pub ghost struct SliceIteratorView<T> {
    pub source: Seq<T>,
    pub remaining: Seq<T>,
    pub yielded_prefix: Seq<T>,
    pub remainder: Seq<T>,
    pub chunk_size: int,
    pub reverse: bool,
}

pub uninterp spec fn slice_iterator_view<I, T>(iter: I) -> SliceIteratorView<T>;

pub open spec fn slice_iterator_well_formed<T>(view: SliceIteratorView<T>) -> bool {
    0 <= view.chunk_size && view.remainder.len() <= view.source.len()
}

pub broadcast axiom fn axiom_slice_iterator_view_well_formed<I, T>(iter: I)
    ensures
        slice_iterator_well_formed(#[trigger] slice_iterator_view::<I, T>(iter)),
;

pub open spec fn slice_chunk_partition<T>(view: SliceIteratorView<T>) -> bool {
    slice_iterator_well_formed(view)
        && view.chunk_size > 0
        && (view.remainder.len() as int) < view.chunk_size
        && (view.remaining.len() as int) % view.chunk_size == 0
        && (view.yielded_prefix.len() as int) % view.chunk_size == 0
        && if view.reverse {
            view.remainder + view.remaining + view.yielded_prefix == view.source
        } else {
            view.yielded_prefix + view.remaining + view.remainder == view.source
        }
}

pub open spec fn slice_split_off_first_result<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    value: T,
) -> bool {
    source.len() != 0
        && value == source[0]
        && remaining == source.subrange(1, source.len() as int)
}

pub open spec fn slice_split_off_last_result<T>(
    source: Seq<T>,
    remaining: Seq<T>,
    value: T,
) -> bool {
    source.len() != 0
        && value == source[(source.len() - 1) as int]
        && remaining == source.subrange(0, (source.len() - 1) as int)
}

pub open spec fn ascii_is_uppercase(byte: u8) -> bool {
    0x41 <= (byte as int) && (byte as int) <= 0x5a
}

pub open spec fn ascii_is_lowercase(byte: u8) -> bool {
    0x61 <= (byte as int) && (byte as int) <= 0x7a
}

pub open spec fn ascii_lower_byte(byte: u8) -> u8 {
    if ascii_is_uppercase(byte) {
        ((byte as int) + 0x20) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_upper_byte(byte: u8) -> u8 {
    if ascii_is_lowercase(byte) {
        ((byte as int) - 0x20) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_is_whitespace(byte: u8) -> bool {
    byte == 0x09u8
        || byte == 0x0au8
        || byte == 0x0bu8
        || byte == 0x0cu8
        || byte == 0x0du8
        || byte == 0x20u8
}

pub open spec fn ascii_lower_seq(seq: Seq<u8>) -> Seq<u8> {
    Seq::new(seq.len(), |i: int| ascii_lower_byte(seq[i]))
}

pub open spec fn ascii_upper_seq(seq: Seq<u8>) -> Seq<u8> {
    Seq::new(seq.len(), |i: int| ascii_upper_byte(seq[i]))
}

pub open spec fn ascii_trim_start_boundary(seq: Seq<u8>, i: int) -> bool {
    0 <= i <= seq.len()
        && (forall|j: int| 0 <= j < i ==> #[trigger] ascii_is_whitespace(seq[j]))
        && (i < seq.len() ==> !ascii_is_whitespace(seq[i]))
}

pub open spec fn ascii_trim_end_boundary(seq: Seq<u8>, i: int) -> bool {
    0 <= i <= seq.len()
        && (forall|j: int| i <= j < seq.len() ==> #[trigger] ascii_is_whitespace(seq[j]))
        && (0 < i ==> !ascii_is_whitespace(seq[i - 1]))
}

pub open spec fn ascii_trim_start_index(seq: Seq<u8>) -> int {
    choose|i: int| #[trigger] ascii_trim_start_boundary(seq, i)
}

pub open spec fn ascii_trim_end_index(seq: Seq<u8>) -> int {
    choose|i: int| #[trigger] ascii_trim_end_boundary(seq, i)
}

pub open spec fn ascii_trim_start_result(seq: Seq<u8>, ret: &[u8]) -> bool {
    0 <= ascii_trim_start_index(seq) <= seq.len()
        && ret@ == seq.subrange(ascii_trim_start_index(seq), seq.len() as int)
        && (forall|i: int| 0 <= i < ascii_trim_start_index(seq)
            ==> ascii_is_whitespace(seq[i]))
        && (ascii_trim_start_index(seq) < seq.len()
            ==> !ascii_is_whitespace(seq[ascii_trim_start_index(seq)]))
}

pub open spec fn ascii_trim_end_result(seq: Seq<u8>, ret: &[u8]) -> bool {
    0 <= ascii_trim_end_index(seq) <= seq.len()
        && ret@ == seq.subrange(0, ascii_trim_end_index(seq))
        && (forall|i: int| ascii_trim_end_index(seq) <= i < seq.len()
            ==> ascii_is_whitespace(seq[i]))
        && (0 < ascii_trim_end_index(seq)
            ==> !ascii_is_whitespace(seq[ascii_trim_end_index(seq) - 1]))
}

} // verus!
