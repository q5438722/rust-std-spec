pub assume_specification[ <f64 as PartialOrd<f64>>::ge ](x: &f64, y: &f64) -> (o: bool)
    ensures
        ge_ensures::<f64>(*x, *y, o),
;
