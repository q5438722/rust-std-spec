pub assume_specification<
    'a,
    T,
    const N: usize,
>[ <&'a [T; N] as core::iter::IntoIterator>::into_iter ](s: &'a [T; N]) -> (iter: core::slice::Iter<
    'a,
    T,
>)
    ensures
        iter == spec_array_iter(s),
        IteratorSpec::decrease(&iter) is Some,
        IteratorSpec::initial_value_relation(&iter, &iter),
;
