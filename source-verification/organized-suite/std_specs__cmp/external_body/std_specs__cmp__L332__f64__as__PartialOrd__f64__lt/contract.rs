pub assume_specification[ <f64 as PartialOrd<f64>>::lt ](x: &f64, y: &f64) -> (o: bool)
    ensures
        lt_ensures::<f64>(*x, *y, o),
;
