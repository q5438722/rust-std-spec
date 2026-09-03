pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks::<N> ](
    slice: &[T],
) -> (ret: (&[T], &[[T; N]]))
    requires
        N != 0,
    ensures
        slice_array_rchunks_partition::<T, N>(slice@, ret.0@, ret.1@),
        ret.1@.len() == slice@.len() / (N as nat),
        ret.0@.len() == slice@.len() % (N as nat),
        ret.0@ == slice@.subrange(0, ret.0@.len() as int),
        forall|chunk: int| 0 <= chunk < ret.1@.len() ==> array_value_view::<T, N>(
            ret.1@[chunk],
        ) == slice@.subrange(
            ret.0@.len() as int + chunk * (N as int),
            ret.0@.len() as int + (chunk + 1) * (N as int),
        ),
;
