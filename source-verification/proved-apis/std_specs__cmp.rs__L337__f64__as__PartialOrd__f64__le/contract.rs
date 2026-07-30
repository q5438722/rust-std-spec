pub assume_specification[ <f64 as PartialOrd<f64>>::le ](x: &f64, y: &f64) -> (o: bool)
    ensures
        le_ensures::<f64>(*x, *y, o),
;
