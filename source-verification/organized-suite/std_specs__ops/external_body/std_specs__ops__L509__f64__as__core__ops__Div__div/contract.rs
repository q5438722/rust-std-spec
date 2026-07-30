pub assume_specification[ <f64 as core::ops::Div>::div ](x: f64, y: f64) -> (o: f64)
    ensures
        div_ensures::<f64>(x, y, o),
;
