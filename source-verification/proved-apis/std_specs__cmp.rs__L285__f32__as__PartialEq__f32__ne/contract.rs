pub assume_specification[ <f32 as PartialEq<f32>>::ne ](x: &f32, y: &f32) -> (o: bool)
    ensures
        ne_ensures::<f32>(*x, *y, o),
;
