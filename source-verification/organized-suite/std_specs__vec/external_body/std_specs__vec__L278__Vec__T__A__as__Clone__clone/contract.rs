pub assume_specification<T: Clone, A: Allocator + Clone>[ <Vec<T, A> as Clone>::clone ](
    vec: &Vec<T, A>,
) -> (res: Vec<T, A>)
    ensures
        res.len() == vec.len(),
        forall|i| #![all_triggers] 0 <= i < vec.len() ==> cloned::<T>(vec[i], res[i]),
        vec_clone_trigger(*vec, res),
        vec@ =~= res@ ==> vec@ == res@,
;
