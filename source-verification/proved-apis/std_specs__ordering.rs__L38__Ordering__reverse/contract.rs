pub assume_specification[ Ordering::reverse ](ordering: Ordering) -> (result: Ordering)
    ensures
        result == match ordering {
            Ordering::Less => Ordering::Greater,
            Ordering::Equal => Ordering::Equal,
            Ordering::Greater => Ordering::Less,
        },
;
