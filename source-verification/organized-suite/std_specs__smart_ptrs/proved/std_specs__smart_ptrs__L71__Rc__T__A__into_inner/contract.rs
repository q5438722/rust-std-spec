pub assume_specification<T, A: Allocator>[ Rc::<T, A>::into_inner ](v: Rc<T, A>) -> (result: Option<
    T,
>)
    ensures
        result matches Some(t) ==> t == *v,
;
