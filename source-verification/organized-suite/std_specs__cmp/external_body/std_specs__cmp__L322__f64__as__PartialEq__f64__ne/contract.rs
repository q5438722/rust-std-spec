pub assume_specification[ <f64 as PartialEq<f64>>::ne ](x: &f64, y: &f64) -> (o: bool)
    ensures
        ne_ensures::<f64>(*x, *y, o),
;
