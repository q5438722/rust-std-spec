pub assume_specification<T: core::clone::Clone, A: Allocator>[ Vec::<T, A>::extend_from_slice ](
    vec: &mut Vec<T, A>,
    other: &[T],
)
    ensures
        final(vec)@.len() == old(vec)@.len() + other@.len(),
        forall|i: int|
            #![trigger final(vec)@[i]]
            0 <= i < final(vec)@.len() ==> if i < old(vec)@.len() {
                final(vec)@[i] == old(vec)@[i]
            } else {
                cloned::<T>(other@[i - old(vec)@.len()], final(vec)@[i])
            },
;
