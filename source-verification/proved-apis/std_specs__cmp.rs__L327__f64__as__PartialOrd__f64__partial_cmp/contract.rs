pub assume_specification[ <f64 as PartialOrd<f64>>::partial_cmp ](x: &f64, y: &f64) -> (o: Option<Ordering>)
    ensures
        partial_cmp_ensures::<f64>(*x, *y, o),
;
