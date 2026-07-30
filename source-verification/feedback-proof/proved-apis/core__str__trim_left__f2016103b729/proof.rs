#![allow(dead_code)]

use vstd::prelude::*;

verus! {

pub assume_specification[ str::trim_start ](s: &str) -> (res: &str)
    ensures
        exists|start: int|
            start >= 0
            && s@.len() >= start
            && res@ == s@.subrange(start, s@.len() as int)
            && (forall|i: int| i >= 0 && start > i ==> (
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
            ))
            && (s@.len() > start ==> !(
                (s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat)
                    || s@[start] as nat == 0x0020
                    || s@[start] as nat == 0x0085
                    || s@[start] as nat == 0x00a0
                    || s@[start] as nat == 0x1680
                    || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat)
                    || s@[start] as nat == 0x2028
                    || s@[start] as nat == 0x2029
                    || s@[start] as nat == 0x202f
                    || s@[start] as nat == 0x205f
                    || s@[start] as nat == 0x3000
            )),
;

#[allow(deprecated)]
pub fn source_core_str_trim_left(s: &str) -> (res: &str)
    ensures
        exists|start: int|
            start >= 0
            && s@.len() >= start
            && res@ == s@.subrange(start, s@.len() as int)
            && (forall|i: int| i >= 0 && start > i ==> (
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
            ))
            && (s@.len() > start ==> !(
                (s@[start] as nat >= 0x0009 && 0x000d >= s@[start] as nat)
                    || s@[start] as nat == 0x0020
                    || s@[start] as nat == 0x0085
                    || s@[start] as nat == 0x00a0
                    || s@[start] as nat == 0x1680
                    || (s@[start] as nat >= 0x2000 && 0x200a >= s@[start] as nat)
                    || s@[start] as nat == 0x2028
                    || s@[start] as nat == 0x2029
                    || s@[start] as nat == 0x202f
                    || s@[start] as nat == 0x205f
                    || s@[start] as nat == 0x3000
            )),
{
    s.trim_start()
}

} // verus!

fn main() {}