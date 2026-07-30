pub assume_specification<T, const N: usize>[ alloc::boxed::box_assume_init_into_vec_unsafe ](
    vals: alloc::boxed::Box<core::mem::MaybeUninit<[T; N]>>,
) -> (result: alloc::vec::Vec<T>)
    requires
        vals.mem_contents() is Init,
    ensures
        vals.mem_contents() matches MemContents::Init(array) && result@ == array@,
;
