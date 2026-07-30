pub assume_specification[ <f64 as core::ops::Sub>::sub ](x: f64, y: f64) -> (o: f64)
    ensures
        sub_ensures::<f64>(x, y, o),
;
