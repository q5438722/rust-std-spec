pub assume_specification[ <f32 as PartialOrd<f32>>::ge ](x: &f32, y: &f32) -> (o: bool)
    ensures
        ge_ensures::<f32>(*x, *y, o),
;
