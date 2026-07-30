pub assume_specification<T, A: Allocator>[ Rc::<T, A>::try_unwrap ](v: Rc<T, A>) -> (result: Result<
    T,
    Rc<T, A>,
>)
    ensures
        match result {
            Ok(t) => t == *v,
            Err(e) => e == v,
        },
;
