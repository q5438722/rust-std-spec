pub assume_specification<T, I: SliceIndex<[T]>, A: Allocator>[Vec::<T, A>::index](
    vec: &Vec<T, A>,
    i: I,
) -> (r: &<Vec<T, A> as Index<I>>::Output)
    ensures
        exists|s: &[T]| #[trigger] s@ == vec@ && call_ensures(<I as SliceIndex<[T]>>::index, (i, s), r),
;
