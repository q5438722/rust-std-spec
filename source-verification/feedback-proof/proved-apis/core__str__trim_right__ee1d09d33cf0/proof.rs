#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification[ str::trim_end ](s: &str) -> (res: &str)
    ensures
        s@.len() >= res@.len(),
        res@ == s@.subrange(0, res@.len() as int),
        forall|i: int| i >= res@.len() as int && s@.len() > i ==> (
            (s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat)
                || s@[i] as nat == 0x0020
                || s@[i] as nat == 0x0085
                || s@[i] as nat == 0x00a0
                || s@[i] as nat == 0x1680
                || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat)
                || s@[i] as nat == 0x2028
                || s@[i] as nat == 0x2029
                || s@[i] as nat == 0x202f
                || s@[i] as nat == 0x205f
                || s@[i] as nat == 0x3000
        ),
        res@.len() > 0 ==> !(
            (res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat)
                || res@.last() as nat == 0x0020
                || res@.last() as nat == 0x0085
                || res@.last() as nat == 0x00a0
                || res@.last() as nat == 0x1680
                || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat)
                || res@.last() as nat == 0x2028
                || res@.last() as nat == 0x2029
                || res@.last() as nat == 0x202f
                || res@.last() as nat == 0x205f
                || res@.last() as nat == 0x3000
        ),
;

pub fn source_core_str_trim_right(s: &str) -> (res: &str)
    ensures
        s@.len() >= res@.len(),
        res@ == s@.subrange(0, res@.len() as int),
        forall|i: int| i >= res@.len() as int && s@.len() > i ==> (
            (s@[i] as nat >= 0x0009 && 0x000d >= s@[i] as nat)
                || s@[i] as nat == 0x0020
                || s@[i] as nat == 0x0085
                || s@[i] as nat == 0x00a0
                || s@[i] as nat == 0x1680
                || (s@[i] as nat >= 0x2000 && 0x200a >= s@[i] as nat)
                || s@[i] as nat == 0x2028
                || s@[i] as nat == 0x2029
                || s@[i] as nat == 0x202f
                || s@[i] as nat == 0x205f
                || s@[i] as nat == 0x3000
        ),
        res@.len() > 0 ==> !(
            (res@.last() as nat >= 0x0009 && 0x000d >= res@.last() as nat)
                || res@.last() as nat == 0x0020
                || res@.last() as nat == 0x0085
                || res@.last() as nat == 0x00a0
                || res@.last() as nat == 0x1680
                || (res@.last() as nat >= 0x2000 && 0x200a >= res@.last() as nat)
                || res@.last() as nat == 0x2028
                || res@.last() as nat == 0x2029
                || res@.last() as nat == 0x202f
                || res@.last() as nat == 0x205f
                || res@.last() as nat == 0x3000
        ),
{
    let res = s.trim_end();
    assert(s@.len() >= res@.len());
    assert(res@ == s@.subrange(0, res@.len() as int));
    res
}

} // verus!

fn main() {}