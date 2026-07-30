pub assume_specification<T: Clone, A: Allocator + Clone>[ <VecDeque<T, A> as Clone>::clone ](
    v: &VecDeque<T, A>,
) -> (res: VecDeque<T, A>)
    ensures
        res.len() == v.len(),
        forall|i| #![all_triggers] 0 <= i < v.len() ==> cloned::<T>(v[i], res[i]),
        vec_dequeue_clone_trigger(*v, res),
        v@ =~= res@ ==> v@ == res@,
;
