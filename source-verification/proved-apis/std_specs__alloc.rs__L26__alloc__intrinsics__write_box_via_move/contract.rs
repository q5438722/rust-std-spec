pub assume_specification<T>[ alloc::intrinsics::write_box_via_move ](
    _0: alloc::boxed::Box<core::mem::MaybeUninit<T>>,
    v: T,
) -> (result: alloc::boxed::Box<core::mem::MaybeUninit<T>>)
    ensures
        result.mem_contents() == MemContents::Init(v),
;
