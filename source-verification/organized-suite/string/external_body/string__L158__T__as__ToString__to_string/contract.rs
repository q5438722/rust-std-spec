pub assume_specification<T: core::fmt::Display + ?Sized>[ <T as ToString>::to_string ](
    t: &T,
) -> (res: String)
    ensures
        to_string_from_display_ensures::<T>(t, res),
;
