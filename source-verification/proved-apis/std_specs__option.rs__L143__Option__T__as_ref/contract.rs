pub assume_specification<T>[ Option::<T>::as_ref ](option: &Option<T>) -> (a: Option<&T>)
    ensures
        a is Some <==> option is Some,
        a is Some ==> option->0 == a->0,
    no_unwind
;
