pub assume_specification<T, I>[ <[T]>::get::<I> ](slice: &[T], i: I) -> (b: Option<
    &<I as SliceIndex<[T]>>::Output,
>) where I: SliceIndex<[T]>
    returns
        spec_slice_get(slice, i),
;
