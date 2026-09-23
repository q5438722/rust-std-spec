use vstd::prelude::*;

verus! {

pub open spec fn default_post<T>(result: &[T]) -> bool {
    result@ =~= Seq::<T>::empty()
}

}
