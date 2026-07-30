use vstd::prelude::*;
use vstd::std_specs::ops::*;

verus! {

pub uninterp spec fn f64_mul_add_ensures(x: f64, a: f64, b: f64, o: f64) -> bool;

pub assume_specification[f64::mul_add](x: f64, a: f64, b: f64) -> (o: f64)
    ensures
        f64_mul_add_ensures(x, a, b, o),
;

pub axiom fn axiom_f64_mul_add_one_is_add(x: f64, y: f64, o: f64)
    requires
        f64_mul_add_ensures(x, 1.0f64, y, o),
    ensures
        add_ensures::<f64>(x, y, o),
;

pub fn source_f64_add(x: f64, y: f64) -> (o: f64)
    ensures
        add_ensures::<f64>(x, y, o),
{
    let o = x.mul_add(1.0f64, y);
    proof {
        axiom_f64_mul_add_one_is_add(x, y, o);
    }
    o
}

} // verus!

fn main() {}