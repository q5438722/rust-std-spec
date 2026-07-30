pub assume_specification[ <f32 as PartialOrd<f32>>::lt ](x: &f32, y: &f32) -> (o: bool)
    ensures
        lt_ensures::<f32>(*x, *y, o),
;
