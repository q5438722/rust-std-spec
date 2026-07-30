pub assume_specification[ <f64 as core::ops::Add>::add ](x: f64, y: f64) -> (o: f64)
    ensures
        add_ensures::<f64>(x, y, o),
;
