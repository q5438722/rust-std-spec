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



trait T13_ArrayAdditionalSpecFns<A2_T, > where Self: T11_View, Self: T11_View<A12_V = D10_Seq<A2_T, >>,  {
}

trait T14_SliceAdditionalSpecFns<A2_T, > where Self: T11_View, Self: T11_View<A12_V = D10_Seq<A2_T, >>,  {
}

trait T11_View {
    type A12_V : ;
}

trait T15_Tuple {
}

trait T17_FnOnce<A16_Args, > where A16_Args: Tuple,  {
    type A18_Output : ;
}

trait T19_FnMut<A16_Args, > where Self: T17_FnOnce<A16_Args, >, A16_Args: Tuple,  {
}

trait T20_Fn<A16_Args, > where Self: T19_FnMut<A16_Args, >, A16_Args: Tuple,  {
}

trait T4_Allocator {
}

struct D1_Global(
);

struct D5_Vec<A2_T, A3_A, >(
    Box<A2_T, >,
    Box<A3_A, >,
) where A3_A: T4_Allocator, ;

struct D6_ISet<A3_A, >(
    Box<A3_A, >,
    C<0, (Box<(A3_A, ), >, Box<bool, >, ), >,
) where ;

struct D7_Provenance(
);

struct D8_PtrData<A2_T, >(
    Box<A2_T, >,
    <A2_T as std::ptr::Pointee>::Metadata,
) where A2_T : ?Sized, ;

struct D9_SeqInner<A3_A, >(
    Box<A3_A, >,
) where ;

struct D10_Seq<A3_A, >(
    Box<A3_A, >,
    D9_SeqInner<A3_A, >,
) where ;

impl<A2_T, const A21_N: usize, > T11_View for Arr<A2_T, A21_N, > where  {
    type A12_V = D10_Seq<A2_T, >;
}

impl<A2_T, const A21_N: usize, > T13_ArrayAdditionalSpecFns<A2_T, > for Arr<A2_T, A21_N, > where  {
}

impl<A2_T, > T11_View for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
    type A12_V = D8_PtrData<A2_T, >;
}

impl<A2_T, > T11_View for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
    type A12_V = D8_PtrData<A2_T, >;
}

impl<A2_T, > T11_View for [A2_T] where  {
    type A12_V = D10_Seq<A2_T, >;
}

impl<A2_T, > T14_SliceAdditionalSpecFns<A2_T, > for [A2_T] where  {
}

impl<A3_A, > T11_View for C<2, (Box<A3_A, >, ), > where A3_A: T11_View, A3_A : ?Sized,  {
    type A12_V = <A3_A as T11_View>::A12_V;
}

impl<A3_A, > T11_View for C<4, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T11_View, A3_A : ?Sized,  {
    type A12_V = <A3_A as T11_View>::A12_V;
}

impl<A3_A, > T11_View for C<5, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T11_View,  {
    type A12_V = <A3_A as T11_View>::A12_V;
}

impl<A3_A, > T11_View for C<6, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T11_View,  {
    type A12_V = <A3_A as T11_View>::A12_V;
}

impl<A2_T, A3_A, > T11_View for D5_Vec<A2_T, A3_A, > where A3_A: T4_Allocator,  {
    type A12_V = D10_Seq<A2_T, >;
}

impl T11_View for () {
    type A12_V = ();
}

impl T11_View for bool {
    type A12_V = bool;
}

impl T11_View for usize {
    type A12_V = usize;
}

impl<A3_A, A22_F, > T20_Fn<A3_A, > for C<2, (Box<A22_F, >, ), > where A3_A: Tuple, A22_F: T20_Fn<A3_A, >, A22_F : ?Sized,  {
}

impl<A16_Args, A22_F, A3_A, > T20_Fn<A16_Args, > for C<4, (Box<A22_F, >, Box<A3_A, >, ), > where A16_Args: Tuple, A22_F: T20_Fn<A16_Args, >, A3_A: T4_Allocator, A22_F : ?Sized,  {
}

impl<A3_A, A22_F, > T19_FnMut<A3_A, > for C<2, (Box<A22_F, >, ), > where A3_A: Tuple, A22_F: T20_Fn<A3_A, >, A22_F : ?Sized,  {
}

impl<A3_A, A22_F, > T19_FnMut<A3_A, > for C<3, (Box<A22_F, >, ), > where A3_A: Tuple, A22_F: T19_FnMut<A3_A, >, A22_F : ?Sized,  {
}

impl<A16_Args, A22_F, A3_A, > T19_FnMut<A16_Args, > for C<4, (Box<A22_F, >, Box<A3_A, >, ), > where A16_Args: Tuple, A22_F: T19_FnMut<A16_Args, >, A3_A: T4_Allocator, A22_F : ?Sized,  {
}

impl<A3_A, A22_F, > T17_FnOnce<A3_A, > for C<2, (Box<A22_F, >, ), > where A3_A: Tuple, A22_F: T20_Fn<A3_A, >, A22_F : ?Sized,  {
    type A18_Output = <A22_F as T17_FnOnce<A3_A, >>::A18_Output;
}

impl<A3_A, A22_F, > T17_FnOnce<A3_A, > for C<3, (Box<A22_F, >, ), > where A3_A: Tuple, A22_F: T19_FnMut<A3_A, >, A22_F : ?Sized,  {
    type A18_Output = <A22_F as T17_FnOnce<A3_A, >>::A18_Output;
}

impl<A16_Args, A22_F, A3_A, > T17_FnOnce<A16_Args, > for C<4, (Box<A22_F, >, Box<A3_A, >, ), > where A16_Args: Tuple, A22_F: T17_FnOnce<A16_Args, >, A3_A: T4_Allocator, A22_F : ?Sized,  {
    type A18_Output = <A22_F as T17_FnOnce<A16_Args, >>::A18_Output;
}

impl<A3_A, > T4_Allocator for C<2, (Box<A3_A, >, ), > where A3_A: T4_Allocator, A3_A : ?Sized,  {
}

impl<A3_A, > T4_Allocator for C<3, (Box<A3_A, >, ), > where A3_A: T4_Allocator, A3_A : ?Sized,  {
}

impl T4_Allocator for D1_Global {
}

impl<A2_T, A3_A, > T4_Allocator for C<4, (Box<A2_T, >, Box<A3_A, >, ), > where A2_T: T4_Allocator, A3_A: T4_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T4_Allocator for C<5, (Box<A2_T, >, Box<A3_A, >, ), > where A2_T: T4_Allocator, A3_A: T4_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T4_Allocator for C<6, (Box<A2_T, >, Box<A3_A, >, ), > where A2_T: T4_Allocator, A3_A: T4_Allocator, A2_T : ?Sized,  {
}
