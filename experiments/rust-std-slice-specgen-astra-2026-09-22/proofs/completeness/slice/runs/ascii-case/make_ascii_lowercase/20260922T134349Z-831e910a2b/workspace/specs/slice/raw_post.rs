use vstd::prelude::*;

verus! {

pub open spec fn singleton_post<T>(value: T, elements: Seq<T>) -> bool {
    elements =~= seq![value]
}

}
