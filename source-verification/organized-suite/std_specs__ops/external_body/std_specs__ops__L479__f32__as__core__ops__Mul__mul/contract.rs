pub assume_specification[ <f32 as core::ops::Mul>::mul ](x: f32, y: f32) -> (o: f32)
    ensures
        mul_ensures::<f32>(x, y, o),
;
