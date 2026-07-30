pub assume_specification<T>[ Layout::new::<T> ]() -> (result: Layout)
    ensures
        result@ == (LayoutView { size: size_of_as_usize::<T>(), align: align_of_as_usize::<T>() }),
;
