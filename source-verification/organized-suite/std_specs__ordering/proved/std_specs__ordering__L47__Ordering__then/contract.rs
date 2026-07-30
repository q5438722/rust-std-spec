pub assume_specification[ Ordering::then ](ordering: Ordering, other: Ordering) -> (result:
    Ordering)
    ensures
        result == if ordering is Equal {
            other
        } else {
            ordering
        },
;
