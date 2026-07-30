pub assume_specification[ <f32 as core::ops::Div>::div ](x: f32, y: f32) -> (o: f32)
    ensures
        div_ensures::<f32>(x, y, o),
;
