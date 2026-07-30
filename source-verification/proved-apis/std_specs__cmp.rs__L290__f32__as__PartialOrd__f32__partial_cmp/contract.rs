pub assume_specification[ <f32 as PartialOrd<f32>>::partial_cmp ](x: &f32, y: &f32) -> (o: Option<Ordering>)
    ensures
        partial_cmp_ensures::<f32>(*x, *y, o),
;
