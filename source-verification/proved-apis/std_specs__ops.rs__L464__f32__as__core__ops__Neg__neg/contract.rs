pub assume_specification[ <f32 as core::ops::Neg>::neg ](x: f32) -> (o: f32)
    ensures
        neg_ensures::<f32>(x, o),
;
