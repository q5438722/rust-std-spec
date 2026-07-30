pub assume_specification[ <f32 as PartialEq<f32>>::eq ](x: &f32, y: &f32) -> (o: bool)
    ensures
        eq_ensures::<f32>(*x, *y, o),
;
