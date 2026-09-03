pub assume_specification<T, const N: usize>[ <[T]>::as_chunks::<N> ](
    slice: &[T],
) -> (ret: (&[[T; N]], &[T]))
    requires
        N != 0,
    ensures
        slice_array_chunks_partition::<T, N>(slice@, ret.0@, ret.1@),
        ret.0@.len() == slice@.len() / (N as nat),
        ret.1@.len() == slice@.len() % (N as nat),
        forall|chunk: int| 0 <= chunk < ret.0@.len() ==> array_value_view::<T, N>(
            ret.0@[chunk],
        ) == slice@.subrange(chunk * (N as int), (chunk + 1) * (N as int)),
        ret.1@ == slice@.subrange((ret.0@.len() * (N as nat)) as int, slice@.len() as int),
;
