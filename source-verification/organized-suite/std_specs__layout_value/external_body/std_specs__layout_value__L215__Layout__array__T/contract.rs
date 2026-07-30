pub assume_specification<T>[ Layout::array::<T> ](length: usize) -> (result: Result<
    Layout,
    LayoutError,
>)
    ensures
        ({
            let size = size_of_as_usize::<T>() as nat * length as nat;
            size <= usize::MAX as nat && valid_layout(size as usize, align_of_as_usize::<T>())
        }) ==> (result matches Ok(layout) && layout@ == (LayoutView {
            size: (size_of_as_usize::<T>() as nat * length as nat) as usize,
            align: align_of_as_usize::<T>(),
        })),
        ({
            let size = size_of_as_usize::<T>() as nat * length as nat;
            size > usize::MAX as nat || !valid_layout(size as usize, align_of_as_usize::<T>())
        }) ==> result is Err,
;
