#![feature(negative_impls)]
#![feature(with_negative_coherence)]
#![feature(box_patterns)]
#![feature(ptr_metadata)]
#![feature(never_type)]
#![feature(allocator_api)]
#![feature(unboxed_closures)]
#![feature(fn_traits)]
#![feature(tuple_trait)]
#![feature(f16)]
#![feature(f128)]
#![allow(non_camel_case_types)]
#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_assignments)]
#![allow(unreachable_patterns)]
#![allow(unused_parens)]
#![allow(unused_braces)]
#![allow(dead_code)]
#![allow(unreachable_code)]
#![allow(unconditional_recursion)]
#![allow(unused_mut)]
#![allow(unused_labels)]
use std::marker::PhantomData;
use std::marker::Tuple;
use std::rc::Rc;
use std::sync::Arc;
use std::alloc::Allocator;
use std::alloc::Global;
use std::mem::ManuallyDrop;
use std::ptr::Pointee;
use std::ptr::Thin;
fn op<A, B>(a: A) -> B { panic!() }
fn static_ref<T>(t: T) -> &'static T { panic!() }
fn tracked_new<T>(t: T) -> Tracked<T> { panic!() }
fn tracked_exec_borrow<'a, T>(t: &'a T) -> &'a Tracked<T> { panic!() }
fn clone<T>(t: &T) -> T { panic!() }
fn rc_new<T>(t: T) -> std::rc::Rc<T> { panic!() }
fn arc_new<T>(t: T) -> std::sync::Arc<T> { panic!() }
fn box_new<T>(t: T) -> Box<T> { panic!() }
struct Tracked<A> { a: PhantomData<A> }
impl<A> Tracked<A> {
    pub fn get(self) -> A { panic!() }
    pub fn borrow(&self) -> &A { panic!() }
    pub fn borrow_mut(&mut self) -> &mut A { panic!() }
}
struct Ghost<A> { a: PhantomData<A> }
impl<A> Clone for Ghost<A> { fn clone(&self) -> Self { panic!() } }
impl<A> Copy for Ghost<A> { }
impl<A: Copy> Clone for Tracked<A> { fn clone(&self) -> Self { panic!() } }
impl<A: Copy> Copy for Tracked<A> { }
#[derive(Clone, Copy)] struct int;
#[derive(Clone, Copy)] struct nat;
#[derive(Clone, Copy)] struct real;
struct FnSpec<Args, Output> { x: PhantomData<(Args, Output)> }
struct InvariantBlockGuard;
fn open_atomic_invariant_begin<'a, X, V>(_inv: &'a X) -> (InvariantBlockGuard, V) { panic!(); }
fn open_local_invariant_begin<'a, X, V>(_inv: &'a X) -> (InvariantBlockGuard, V) { panic!(); }
fn open_invariant_end<V>(_guard: InvariantBlockGuard, _v: V) { panic!() }
fn index<'a, V, Idx, Output>(v: &'a V, index: Idx) -> &'a Output { panic!() }
trait IndexSet{
fn index_set<Idx, V>(&mut self, index: Idx, val: V) { panic!() }
}
impl<A:?Sized> IndexSet for A {}
struct C<const N: usize, A: ?Sized>(Box<A>);
struct Arr<A: ?Sized, const N: usize>(Box<A>);
struct Dyn<const N: usize, A>(Box<A>, [bool]);
fn use_type_invariant<A>(a: A) -> A { a }

struct FnProof<'a, P, M, N, A, O>(PhantomData<P>, PhantomData<M>, PhantomData<N>, PhantomData<&'a fn(A) -> O>);
struct FOpts<const B: u8, C, const D: u8, const E: u8, const G: u8>(PhantomData<C>);
trait ProofFnOnce {}
trait ProofFnMut: ProofFnOnce {}
trait ProofFn: ProofFnMut {}
struct ProofFnConfirm;
trait ConfirmCopy<const D: u8, F> {}
trait ConfirmUsage<A, O, const B: u8, F> {}
impl<const B: u8, C, const E: u8, const G: u8> Clone for FOpts<B, C, 4, E, G> { fn clone(&self) -> Self { panic!() } }
impl<const B: u8, C, const E: u8, const G: u8> Copy for FOpts<B, C, 4, E, G> {}
impl<const B: u8, C, const D: u8, const E: u8, const G: u8> ProofFnOnce for FOpts<B, C, D, E, G> {}
impl<C, const D: u8, const E: u8, const G: u8> ProofFnMut for FOpts<2, C, D, E, G> {}
impl<C, const D: u8, const E: u8, const G: u8> ProofFnMut for FOpts<3, C, D, E, G> {}
impl<C, const D: u8, const E: u8, const G: u8> ProofFn for FOpts<3, C, D, E, G> {}
impl<'a, P: Copy, M, N, A, O> Clone for FnProof<'a, P, M, N, A, O> { fn clone(&self) -> Self { panic!() } }
impl<'a, P: Copy, M, N, A, O> Copy for FnProof<'a, P, M, N, A, O> {}
impl<'a, P: ProofFnOnce, M, N, A: Tuple, O> FnOnce<A> for FnProof<'a, P, M, N, A, O> {
    type Output = O;
    extern "rust-call" fn call_once(self, _: A) -> <Self as FnOnce<A>>::Output { panic!() }
}
impl<'a, P: ProofFnMut, M, N, A: Tuple, O> FnMut<A> for FnProof<'a, P, M, N, A, O> {
    extern "rust-call" fn call_mut(&mut self, _: A) -> <Self as FnOnce<A>>::Output { panic!() }
}
impl<'a, P: ProofFn, M, N, A: Tuple, O> Fn<A> for FnProof<'a, P, M, N, A, O> {
    extern "rust-call" fn call(&self, _: A) -> <Self as FnOnce<A>>::Output { panic!() }
}
impl<F: Copy> ConfirmCopy<4, F> for ProofFnConfirm {}
impl<F> ConfirmCopy<0, F> for ProofFnConfirm {}
impl<A: Tuple, O, F: FnOnce<A, Output = O>> ConfirmUsage<A, O, 1, F> for ProofFnConfirm {}
impl<A: Tuple, O, F: FnMut<A, Output = O>> ConfirmUsage<A, O, 2, F> for ProofFnConfirm {}
impl<A: Tuple, O, F: Fn<A, Output = O>> ConfirmUsage<A, O, 3, F> for ProofFnConfirm {}
pub fn closure_to_fn_proof<'a, const B: u8, const D: u8, const E: u8, const G: u8, M, N, A, O, F: 'a>(_f: F) -> FnProof<'a, FOpts<B, (), D, E, G>, M, N, A, O>
where ProofFnConfirm: ConfirmUsage<A, O, B, F>, ProofFnConfirm: ConfirmCopy<D, F>, M: Tuple, A: Tuple,
{ panic!() }

fn main() {}



trait T7_Tuple {
}

trait T9_FnOnce<A8_Args, > where A8_Args: Tuple,  {
    type A10_Output : ;
}

trait T11_FnMut<A8_Args, > where Self: T9_FnOnce<A8_Args, >, A8_Args: Tuple,  {
}

trait T12_Fn<A8_Args, > where Self: T11_FnMut<A8_Args, >, A8_Args: Tuple,  {
}

trait T3_Allocator {
}

trait T13_Iterator {
    type A14_Item : ;
}

trait T15_ExactSizeIterator where Self: T13_Iterator,  {
}

trait T16_IteratorSpec where Self: T13_Iterator,  {
}

trait T17_ExactSizeIteratorSpec where Self: T13_Iterator, Self: T15_ExactSizeIterator,  {
}

trait T18_Iterator {
    type A14_Item : ;
}

struct D4_IntoIter<A1_T, A2_A, >(
    Box<A1_T, >,
    Box<A2_A, >,
) where A2_A: T3_Allocator, ;

struct D5_SeqInner<A2_A, >(
    Box<A2_A, >,
) where ;

struct D6_Seq<A2_A, >(
    Box<A2_A, >,
    D5_SeqInner<A2_A, >,
) where ;

impl<A19_I, > T16_IteratorSpec for C<3, (Box<A19_I, >, ), > where A19_I: T13_Iterator,  {
}

impl<A1_T, A2_A, > T16_IteratorSpec for D4_IntoIter<A1_T, A2_A, > where A2_A: T3_Allocator,  {
}

impl<A2_A, A20_F, > T12_Fn<A2_A, > for C<2, (Box<A20_F, >, ), > where A2_A: Tuple, A20_F: T12_Fn<A2_A, >, A20_F : ?Sized,  {
}

impl<A8_Args, A20_F, A2_A, > T12_Fn<A8_Args, > for C<4, (Box<A20_F, >, Box<A2_A, >, ), > where A8_Args: Tuple, A20_F: T12_Fn<A8_Args, >, A2_A: T3_Allocator, A20_F : ?Sized,  {
}

impl<A2_A, A20_F, > T11_FnMut<A2_A, > for C<2, (Box<A20_F, >, ), > where A2_A: Tuple, A20_F: T12_Fn<A2_A, >, A20_F : ?Sized,  {
}

impl<A2_A, A20_F, > T11_FnMut<A2_A, > for C<3, (Box<A20_F, >, ), > where A2_A: Tuple, A20_F: T11_FnMut<A2_A, >, A20_F : ?Sized,  {
}

impl<A8_Args, A20_F, A2_A, > T11_FnMut<A8_Args, > for C<4, (Box<A20_F, >, Box<A2_A, >, ), > where A8_Args: Tuple, A20_F: T11_FnMut<A8_Args, >, A2_A: T3_Allocator, A20_F : ?Sized,  {
}

impl<A2_A, A20_F, > T9_FnOnce<A2_A, > for C<2, (Box<A20_F, >, ), > where A2_A: Tuple, A20_F: T12_Fn<A2_A, >, A20_F : ?Sized,  {
    type A10_Output = <A20_F as T9_FnOnce<A2_A, >>::A10_Output;
}

impl<A2_A, A20_F, > T9_FnOnce<A2_A, > for C<3, (Box<A20_F, >, ), > where A2_A: Tuple, A20_F: T11_FnMut<A2_A, >, A20_F : ?Sized,  {
    type A10_Output = <A20_F as T9_FnOnce<A2_A, >>::A10_Output;
}

impl<A8_Args, A20_F, A2_A, > T9_FnOnce<A8_Args, > for C<4, (Box<A20_F, >, Box<A2_A, >, ), > where A8_Args: Tuple, A20_F: T9_FnOnce<A8_Args, >, A2_A: T3_Allocator, A20_F : ?Sized,  {
    type A10_Output = <A20_F as T9_FnOnce<A8_Args, >>::A10_Output;
}

impl<A19_I, > T15_ExactSizeIterator for C<3, (Box<A19_I, >, ), > where A19_I: T15_ExactSizeIterator, A19_I : ?Sized,  {
}

impl<A19_I, A2_A, > T15_ExactSizeIterator for C<4, (Box<A19_I, >, Box<A2_A, >, ), > where A19_I: T15_ExactSizeIterator, A2_A: T3_Allocator, A19_I : ?Sized,  {
}

impl<A1_T, A2_A, > T15_ExactSizeIterator for D4_IntoIter<A1_T, A2_A, > where A2_A: T3_Allocator,  {
}

impl<A19_I, > T13_Iterator for C<3, (Box<A19_I, >, ), > where A19_I: T13_Iterator, A19_I : ?Sized,  {
    type A14_Item = <A19_I as T13_Iterator>::A14_Item;
}

impl<A19_I, A2_A, > T13_Iterator for C<4, (Box<A19_I, >, Box<A2_A, >, ), > where A19_I: T13_Iterator, A2_A: T3_Allocator, A19_I : ?Sized,  {
    type A14_Item = <A19_I as T13_Iterator>::A14_Item;
}

impl<A1_T, A2_A, > T13_Iterator for D4_IntoIter<A1_T, A2_A, > where A2_A: T3_Allocator,  {
    type A14_Item = A1_T;
}

impl<A2_A, > T3_Allocator for C<2, (Box<A2_A, >, ), > where A2_A: T3_Allocator, A2_A : ?Sized,  {
}

impl<A2_A, > T3_Allocator for C<3, (Box<A2_A, >, ), > where A2_A: T3_Allocator, A2_A : ?Sized,  {
}

impl<A1_T, A2_A, > T3_Allocator for C<4, (Box<A1_T, >, Box<A2_A, >, ), > where A1_T: T3_Allocator, A2_A: T3_Allocator, A1_T : ?Sized,  {
}

impl<A1_T, A2_A, > T3_Allocator for C<5, (Box<A1_T, >, Box<A2_A, >, ), > where A1_T: T3_Allocator, A2_A: T3_Allocator, A1_T : ?Sized,  {
}

impl<A1_T, A2_A, > T3_Allocator for C<6, (Box<A1_T, >, Box<A2_A, >, ), > where A1_T: T3_Allocator, A2_A: T3_Allocator, A1_T : ?Sized,  {
}

impl<A1_T, A2_A, > T18_Iterator for D4_IntoIter<A1_T, A2_A, > where A2_A: T3_Allocator,  {
    type A14_Item = A1_T;
}
