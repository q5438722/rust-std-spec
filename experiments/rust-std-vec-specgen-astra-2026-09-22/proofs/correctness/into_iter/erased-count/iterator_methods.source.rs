use vstd::prelude::*;

verus! {

#[verifier::external_trait_specification]
pub trait ExIteratorConsumers {
    type ExternalTraitSpecificationFor: core::iter::Iterator;
    type Item;

    fn count(self) -> usize where Self: Sized;
    fn last(self) -> Option<Self::Item> where Self: Sized;
}

}
