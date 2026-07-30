pub assume_specification[ <f32 as core::ops::Add>::add ](x: f32, y: f32) -> (o: f32)
    ensures
        add_ensures::<f32>(x, y, o),
;
