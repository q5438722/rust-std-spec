pub assume_specification[ <f64 as PartialEq<f64>>::eq ](x: &f64, y: &f64) -> (o: bool)
    ensures
        eq_ensures::<f64>(*x, *y, o),
;
