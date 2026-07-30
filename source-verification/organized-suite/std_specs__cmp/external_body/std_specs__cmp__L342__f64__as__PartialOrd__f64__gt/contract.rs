pub assume_specification[ <f64 as PartialOrd<f64>>::gt ](x: &f64, y: &f64) -> (o: bool)
    ensures
        gt_ensures::<f64>(*x, *y, o),
;
