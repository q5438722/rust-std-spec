pub assume_specification<T: PointeeSized>[ <core::marker::PhantomData<
    T,
> as core::default::Default>::default ]() -> (r: core::marker::PhantomData<T>)
    ensures
        r == core::marker::PhantomData::<T>,
;
