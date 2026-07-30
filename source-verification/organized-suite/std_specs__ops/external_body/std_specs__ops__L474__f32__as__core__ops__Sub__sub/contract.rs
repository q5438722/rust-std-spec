pub assume_specification[ <f32 as core::ops::Sub>::sub ](x: f32, y: f32) -> (o: f32)
    ensures
        sub_ensures::<f32>(x, y, o),
;
