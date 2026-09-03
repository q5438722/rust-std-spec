pub assume_specification<T, const N: usize>[ <[T]>::as_rchunks_mut::<N> ](
    slice: &mut [T],
) -> (ret: (&mut [T], &mut [[T; N]]))
    requires
        N != 0,
    ensures
        slice_array_rchunks_partition::<T, N>(old(slice)@, ret.0@, ret.1@),
        ret.1@.len() == old(slice)@.len() / (N as nat),
        ret.0@.len() == old(slice)@.len() % (N as nat),
        ret.0@ == old(slice)@.subrange(0, ret.0@.len() as int),
        forall|chunk: int| 0 <= chunk < ret.1@.len() ==> array_value_view::<T, N>(
            ret.1@[chunk],
        ) == old(slice)@.subrange(
            ret.0@.len() as int + chunk * (N as int),
            ret.0@.len() as int + (chunk + 1) * (N as int),
        ),
        final(ret.1)@.len() == ret.1@.len(),
        final(ret.0)@.len() == ret.0@.len(),
        final(slice)@ == final(ret.0)@ + flatten_array_chunks::<T, N>(final(ret.1)@),
        final(ret.0)@ == final(slice)@.subrange(0, final(ret.0)@.len() as int),
        forall|chunk: int| 0 <= chunk < final(ret.1)@.len() ==> array_value_view::<T, N>(
            final(ret.1)@[chunk],
        ) == final(slice)@.subrange(
            final(ret.0)@.len() as int + chunk * (N as int),
            final(ret.0)@.len() as int + (chunk + 1) * (N as int),
        ),
;
