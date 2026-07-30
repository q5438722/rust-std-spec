pub assume_specification[ <f64 as core::ops::Mul>::mul ](x: f64, y: f64) -> (o: f64)
    ensures
        mul_ensures::<f64>(x, y, o),
;
