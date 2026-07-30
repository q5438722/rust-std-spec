pub assume_specification[ <f64 as core::ops::Neg>::neg ](x: f64) -> (o: f64)
    ensures
        neg_ensures::<f64>(x, o),
;
