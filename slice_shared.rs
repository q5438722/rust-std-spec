use core::slice::{EscapeAscii, GetDisjointMutError};

use vstd::prelude::*;

verus! {

pub open spec fn uppercase_byte(byte: u8) -> u8 {
    if b'a' <= byte <= b'z' {
        (byte - 32) as u8
    } else {
        byte
    }
}

pub open spec fn lowercase_byte(byte: u8) -> u8 {
    if b'A' <= byte <= b'Z' {
        (byte + 32) as u8
    } else {
        byte
    }
}

pub open spec fn ascii_whitespace(byte: u8) -> bool {
    byte == 9 || byte == 10 || byte == 12 || byte == 13 || byte == 32
}

#[verifier::external_type_specification]
pub struct ExGetDisjointMutError(GetDisjointMutError);

#[verifier::external_type_specification]
#[verifier::external_body]
pub struct ExEscapeAscii<'a>(EscapeAscii<'a>);

} // verus!
pub mod ascii_model {
    pub mod state {
        use super::values;
        use vstd::prelude::*;
        verus! {

pub type Parts = (Seq<u8>, Seq<u8>, Seq<u8>);

pub open spec fn contents(parts: Parts) -> Seq<u8> {
    parts.0 + values::escaped(parts.1) + parts.2
}

pub open spec fn initial(bytes: Seq<u8>) -> Parts {
    (Seq::empty(), bytes, Seq::empty())
}

pub open spec fn front_parts(p: Parts) -> Parts {
    if p.0.len() > 0 {
        (p.0.drop_first(), p.1, p.2)
    } else if p.1.len() > 0 {
        (values::escape_byte(p.1[0]).drop_first(), p.1.drop_first(), p.2)
    } else {
        (
            Seq::empty(),
            p.1,
            if p.2.len() == 0 {
                p.2
            } else {
                p.2.drop_first()
            },
        )
    }
}

pub open spec fn back_parts(p: Parts) -> Parts {
    if p.2.len() > 0 {
        (p.0, p.1, p.2.drop_last())
    } else if p.1.len() > 0 {
        (p.0, p.1.drop_last(), values::escape_byte(p.1.last()).drop_last())
    } else {
        (
            if p.0.len() == 0 {
                p.0
            } else {
                p.0.drop_last()
            },
            p.1,
            Seq::empty(),
        )
    }
}

} // verus!
    }
    pub mod values {
        use vstd::prelude::*;
        verus! {

pub open spec fn is_ascii(bytes: Seq<u8>) -> bool {
    forall|i: int| 0 <= i < bytes.len() ==> #[trigger] bytes[i] < 128
}

pub open spec fn hex_digit(n: int) -> u8 {
    if n < 10 {
        (48 + n) as u8
    } else {
        (87 + n) as u8
    }
}

pub open spec fn escape_byte(b: u8) -> Seq<u8> {
    if b == 9 {
        seq![92u8, 116u8]
    } else if b == 13 {
        seq![92u8, 114u8]
    } else if b == 10 {
        seq![92u8, 110u8]
    } else if b == 92 {
        seq![92u8, 92u8]
    } else if b == 39 {
        seq![92u8, 39u8]
    } else if b == 34 {
        seq![92u8, 34u8]
    } else if 32 <= b <= 126 {
        seq![b]
    } else {
        seq![92u8, 120u8, hex_digit(b as int / 16), hex_digit(b as int % 16)]
    }
}

pub open spec fn escaped(bytes: Seq<u8>) -> Seq<u8> {
    bytes.flat_map(|b: u8| escape_byte(b))
}

pub open spec fn hint_from_parts(front: Seq<u8>, outer: Seq<u8>, back: Seq<u8>) -> (
    usize,
    Option<usize>,
) {
    let buffered = front.len() + back.len();
    (
        if buffered <= usize::MAX {
            buffered as usize
        } else {
            usize::MAX
        },
        if outer.len() == 0 && buffered <= usize::MAX {
            Some(buffered as usize)
        } else {
            None
        },
    )
}

} // verus!
    }
    pub mod parts {
        use super::state;
        use core::slice::EscapeAscii;
        use vstd::prelude::*;

        verus! {

// The private-field projection is interpreted by source/outer.rs::parts:
// front alive bytes, current outer Iter bytes, and back alive bytes.
// Its API equations are proved in the independently approved corresponding
// implementation; no representation axiom or new executable accessor is added.
#[verifier::prophetic]
pub uninterp spec fn view(iter: EscapeAscii<'_>) -> state::Parts;

} // verus!
    }
}

pub mod splits_model {
    use core::slice::{
        RSplit, RSplitMut, RSplitN, RSplitNMut, Split, SplitInclusive, SplitInclusiveMut, SplitMut,
        SplitN, SplitNMut,
    };
    use vstd::prelude::*;

    verus! {

pub trait SplitState<T, P> {
    spec fn state(&self) -> State<T, P>;
}

pub trait SplitFuture<T> {
    #[verifier::prophetic]
    spec fn field_final(&self) -> Seq<T>;
}

} // verus!
    macro_rules! split_type {
        ($external:ident, $ty:ident) => {
            verus! {
        #[verifier::external_type_specification]
        #[verifier::external_body]
        #[verifier::accept_recursive_types(T)]
        #[verifier::reject_recursive_types(P)]
        pub struct $external<'a, T: 'a, P: FnMut(&T) -> bool>($ty<'a, T, P>);

        impl<'a, T, P: FnMut(&T) -> bool> SplitState<T, P> for $ty<'a, T, P> {
            uninterp spec fn state(&self) -> State<T, P>;
        }
    }
        };
    }

    split_type!(ExSplit, Split);
    split_type!(ExSplitMut, SplitMut);
    split_type!(ExSplitInclusive, SplitInclusive);
    split_type!(ExSplitInclusiveMut, SplitInclusiveMut);
    split_type!(ExRSplit, RSplit);
    split_type!(ExRSplitMut, RSplitMut);
    split_type!(ExSplitN, SplitN);
    split_type!(ExSplitNMut, SplitNMut);
    split_type!(ExRSplitN, RSplitN);
    split_type!(ExRSplitNMut, RSplitNMut);

    macro_rules! mutable_field {
        ($ty:ident) => {
            verus! {
        impl<'a, T, P: FnMut(&T) -> bool> SplitFuture<T> for $ty<'a, T, P> {
            #[verifier::prophetic]
            uninterp spec fn field_final(&self) -> Seq<T>;
        }
    }
        };
    }

    mutable_field!(SplitMut);
    mutable_field!(SplitInclusiveMut);
    mutable_field!(RSplitMut);
    mutable_field!(SplitNMut);
    mutable_field!(RSplitNMut);

    verus! {

pub ghost struct State<T, P> {
    pub v: Seq<T>,
    pub pred: P,
    pub finished: bool,
    pub count: Option<usize>,
}

} // verus!
}

pub mod chunk_by_model {
    use core::slice::{ChunkBy, ChunkByMut};
    use vstd::prelude::*;

    verus! {

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExChunkBy<'a, T: 'a, P>(ChunkBy<'a, T, P>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
#[verifier::reject_recursive_types(P)]
pub struct ExChunkByMut<'a, T: 'a, P>(ChunkByMut<'a, T, P>);

pub trait ChunkByState<T, P> {
    spec fn state(&self) -> Current<T, P>;
}

impl<'a, T, P> ChunkByState<T, P> for ChunkBy<'a, T, P> {
    uninterp spec fn state(&self) -> Current<T, P>;
}

impl<'a, T, P> ChunkByState<T, P> for ChunkByMut<'a, T, P> {
    uninterp spec fn state(&self) -> Current<T, P>;
}

pub trait ChunkByFuture<T> {
    #[verifier::prophetic]
    spec fn future_slice(&self) -> Seq<T>;
}

impl<'a, T, P> ChunkByFuture<T> for ChunkByMut<'a, T, P> {
    #[verifier::prophetic]
    uninterp spec fn future_slice(&self) -> Seq<T>;
}

pub ghost struct Current<T, P> {
    pub slice: Seq<T>,
    pub predicate: P,
}

} // verus!
}

pub mod chunks_model {
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;
    verus! {

pub ghost struct State<T> {
    pub v: Seq<T>,
    pub rem: Seq<T>,
    pub width: usize,
}

pub trait ChunkState<T> {
    spec fn state(&self) -> State<T>;
}

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExChunksExact<'a, T: 'a>(ChunksExact<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExRChunks<'a, T: 'a>(RChunks<'a, T>);

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExRChunksExact<'a, T: 'a>(RChunksExact<'a, T>);

impl<'a, T> ChunkState<T> for ChunksExact<'a, T> {
    uninterp spec fn state(&self) -> State<T>;
}

impl<'a, T> ChunkState<T> for RChunksExact<'a, T> {
    uninterp spec fn state(&self) -> State<T>;
}

} // verus!
}

pub mod arrays_model {
    use core::slice::*;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;
    verus! {

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExArrayWindows<'a, T: 'a, const N: usize>(ArrayWindows<'a, T, N>);

} // verus!
}

pub mod windows_model {
    use core::slice::Windows;
    use vstd::prelude::*;
    use vstd::std_specs::iter::IteratorSpec;

    verus! {

#[verifier::external_type_specification]
#[verifier::external_body]
#[verifier::accept_recursive_types(T)]
pub struct ExWindows<'a, T: 'a>(Windows<'a, T>);

pub trait WindowsView<T> {
    spec fn view(&self) -> State<T>;
}

// The source interpretation is (self.v@, self.size.get()), not the original slice.
impl<'a, T> WindowsView<T> for Windows<'a, T> {
    uninterp spec fn view(&self) -> State<T>;
}

pub ghost struct State<T> {
    pub v: Seq<T>,
    pub width: usize,
}

pub open spec fn valid<T>(s: State<T>) -> bool {
    s.width > 0 && s.v.len() <= usize::MAX
}

pub open spec fn window_values<T>(values: Seq<T>, width: usize) -> Seq<Seq<T>>
    recommends
        width > 0,
{
    Seq::new(
        if width <= values.len() {
            (values.len() - width + 1) as nat
        } else {
            0
        },
        |i: int| values.subrange(i, i + width),
    )
}

pub open spec fn values<T>(s: State<T>) -> Seq<Seq<T>> {
    window_values(s.v, s.width)
}

pub open spec fn item_values<'a, T>(items: Seq<&'a [T]>) -> Seq<Seq<T>> {
    Seq::new(items.len(), |i: int| items[i]@)
}

pub open spec fn option_values<T>(item: Option<&[T]>) -> Option<Seq<T>> {
    match item {
        None => None,
        Some(slice) => Some(slice@),
    }
}

pub open spec fn matches_items<'a, T>(s: State<T>, items: Seq<&'a [T]>) -> bool {
    valid(s) && item_values(items) == values(s)
}

pub open spec fn slice_contents<T>(slice: &[T], contents: Seq<T>) -> bool {
    slice@ == contents
}

pub open spec fn content_ref<'a, T>(contents: Seq<T>) -> &'a [T] {
    choose|slice: &'a [T]| #[trigger] slice_contents(slice, contents)
}

pub open spec fn references<'a, T>(contents: Seq<Seq<T>>) -> Seq<&'a [T]> {
    Seq::new(contents.len(), |i: int| content_ref(contents[i]))
}

pub open spec fn remaining<'a, T>(s: State<T>) -> Seq<&'a [T]> {
    references(values(s))
}

} // verus!
}
