use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

pub uninterp spec fn f32_mul_add_ensures(x: f32, a: f32, b: f32, o: f32) -> bool;

pub assume_specification[f32::mul_add](x: f32, a: f32, b: f32) -> (o: f32)
    ensures
        f32_mul_add_ensures(x, a, b, o),
;

pub axiom fn axiom_f32_mul_add_one_is_add(x: f32, y: f32, o: f32)
    requires
        f32_mul_add_ensures(x, 1.0f32, y, o),
    ensures
        add_ensures::<f32>(x, y, o),
;

pub fn source_f32_add(x: f32, y: f32) -> (o: f32)
    ensures
        add_ensures::<f32>(x, y, o),
{
    let o = x.mul_add(1.0f32, y);
    proof {
        axiom_f32_mul_add_one_is_add(x, y, o);
    }
    o
}

} // verus!

fn main() {}