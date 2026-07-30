pub assume_specification[ <f32 as PartialOrd<f32>>::le ](x: &f32, y: &f32) -> (o: bool)
    ensures
        le_ensures::<f32>(*x, *y, o),
;
