pub assume_specification<T: ?Sized>[ Layout::for_value::<T> ](value: &T) -> (result: Layout)
    ensures
        result@ == (LayoutView {
            size: size_of_val_as_usize(value),
            align: align_of_val_as_usize(value),
        }),
;
