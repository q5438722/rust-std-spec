pub assume_specification[ <f32 as PartialOrd<f32>>::gt ](x: &f32, y: &f32) -> (o: bool)
    ensures
        gt_ensures::<f32>(*x, *y, o),
;
