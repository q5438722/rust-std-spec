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



trait T18_ArrayAdditionalSpecFns<A5_T, > where Self: T16_View, Self: T16_View<A17_V = D13_Seq<A5_T, >>,  {
}

trait T19_SliceAdditionalSpecFns<A5_T, > where Self: T16_View, Self: T16_View<A17_V = D13_Seq<A5_T, >>,  {
}

trait T16_View {
    type A17_V : ;
}

trait T3_ToOwned {
    type A20_Owned : T21_Borrow<Self, >;
}

trait T22_Clone where Self: Sized,  {
}

trait T23_Copy where Self: T22_Clone,  {
}

trait T24_Tuple {
}

trait T26_FnOnce<A25_Args, > where A25_Args: Tuple,  {
    type A27_Output : ;
}

trait T28_FnMut<A25_Args, > where Self: T26_FnOnce<A25_Args, >, A25_Args: Tuple,  {
}

trait T29_Fn<A25_Args, > where Self: T28_FnMut<A25_Args, >, A25_Args: Tuple,  {
}

trait T7_Allocator {
}

trait T21_Borrow<A30_Borrowed, > where A30_Borrowed : ?Sized,  {
}

trait T31_CowObservation<A5_T, > where  {
}

struct D1_Global(
);

struct D4_Cow<A2_B, >(
    Box<A2_B, >,
) where A2_B: T3_ToOwned, A2_B : ?Sized, ;

struct D8_Vec<A5_T, A6_A, >(
    Box<A5_T, >,
    Box<A6_A, >,
) where A6_A: T7_Allocator, ;

struct D9_ISet<A6_A, >(
    Box<A6_A, >,
    C<0, (Box<(A6_A, ), >, Box<bool, >, ), >,
) where ;

struct D10_Provenance(
);

struct D11_PtrData<A5_T, >(
    Box<A5_T, >,
    <A5_T as std::ptr::Pointee>::Metadata,
) where A5_T : ?Sized, ;

struct D12_SeqInner<A6_A, >(
    Box<A6_A, >,
) where ;

struct D13_Seq<A6_A, >(
    Box<A6_A, >,
    D12_SeqInner<A6_A, >,
) where ;

struct D14_String(
);

struct D15_CowContents<A5_T, >(
    Box<A5_T, >,
) where ;

impl<A5_T, const A32_N: usize, > T16_View for Arr<A5_T, A32_N, > where  {
    type A17_V = D13_Seq<A5_T, >;
}

impl<A5_T, const A32_N: usize, > T18_ArrayAdditionalSpecFns<A5_T, > for Arr<A5_T, A32_N, > where  {
}

impl<A5_T, > T16_View for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A17_V = D11_PtrData<A5_T, >;
}

impl<A5_T, > T16_View for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
    type A17_V = D11_PtrData<A5_T, >;
}

impl<A5_T, > T16_View for [A5_T] where  {
    type A17_V = D13_Seq<A5_T, >;
}

impl<A5_T, > T19_SliceAdditionalSpecFns<A5_T, > for [A5_T] where  {
}

impl T16_View for str {
    type A17_V = D13_Seq<char, >;
}

impl T16_View for D14_String {
    type A17_V = D13_Seq<char, >;
}

impl<A6_A, > T16_View for C<2, (Box<A6_A, >, ), > where A6_A: T16_View, A6_A : ?Sized,  {
    type A17_V = <A6_A as T16_View>::A17_V;
}

impl<A6_A, > T16_View for C<4, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T16_View, A6_A : ?Sized,  {
    type A17_V = <A6_A as T16_View>::A17_V;
}

impl<A6_A, > T16_View for C<5, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T16_View,  {
    type A17_V = <A6_A as T16_View>::A17_V;
}

impl<A6_A, > T16_View for C<6, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T16_View,  {
    type A17_V = <A6_A as T16_View>::A17_V;
}

impl<A5_T, A6_A, > T16_View for D8_Vec<A5_T, A6_A, > where A6_A: T7_Allocator,  {
    type A17_V = D13_Seq<A5_T, >;
}

impl T16_View for () {
    type A17_V = ();
}

impl T16_View for bool {
    type A17_V = bool;
}

impl T16_View for usize {
    type A17_V = usize;
}

impl T16_View for char {
    type A17_V = char;
}

impl<A5_T, > T16_View for D4_Cow<A5_T, > where A5_T: T16_View, A5_T: T22_Clone,  {
    type A17_V = <A5_T as T16_View>::A17_V;
}

impl T16_View for D4_Cow<str, > {
    type A17_V = D13_Seq<char, >;
}

impl<A5_T, > T16_View for D4_Cow<[A5_T], > where A5_T: T16_View, A5_T: T22_Clone,  {
    type A17_V = D13_Seq<A5_T, >;
}

impl<A5_T, > T21_Borrow<A5_T, > for A5_T where A5_T : ?Sized,  {
}

impl<A5_T, > T21_Borrow<A5_T, > for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T21_Borrow<A5_T, > for C<3, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A32_N: usize, > T21_Borrow<[A5_T], > for Arr<A5_T, A32_N, > where  {
}

impl<A2_B, > T21_Borrow<A2_B, > for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A6_A, > T21_Borrow<A5_T, > for C<4, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T21_Borrow<A5_T, > for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T21_Borrow<[A5_T], > for D8_Vec<A5_T, A6_A, > where A6_A: T7_Allocator,  {
}

impl T21_Borrow<str, > for D14_String {
}

impl<A5_T, A6_A, > T21_Borrow<A5_T, > for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T22_Clone for C<4, (Box<A5_T, >, Box<A6_A, >, ), > where A5_T: T22_Clone, A6_A: T7_Allocator, A6_A: T22_Clone,  {
}

impl<A5_T, A6_A, > T22_Clone for C<4, (Box<[A5_T], >, Box<A6_A, >, ), > where A5_T: T22_Clone, A6_A: T7_Allocator, A6_A: T22_Clone,  {
}

impl T22_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T22_Clone for usize {
}

impl T22_Clone for bool {
}

impl T22_Clone for char {
}

impl<A5_T, > T22_Clone for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T22_Clone for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T22_Clone for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A32_N: usize, > T22_Clone for Arr<A5_T, A32_N, > where A5_T: T22_Clone,  {
}

impl T22_Clone for D1_Global {
}

impl<A2_B, > T22_Clone for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A6_A, > T22_Clone for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A: T22_Clone, A5_T : ?Sized,  {
}

impl T22_Clone for D14_String {
}

impl<A5_T, A6_A, > T22_Clone for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A: T22_Clone, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T22_Clone for D8_Vec<A5_T, A6_A, > where A5_T: T22_Clone, A6_A: T7_Allocator, A6_A: T22_Clone,  {
}

impl<A6_A, > T22_Clone for C<7, (Box<A6_A, >, ), > where  {
}

impl<A6_A, > T22_Clone for C<8, (Box<A6_A, >, ), > where A6_A: T23_Copy,  {
}

impl T22_Clone for int {
}

impl T22_Clone for nat {
}

impl T23_Copy for usize {
}

impl T23_Copy for bool {
}

impl T23_Copy for char {
}

impl<A5_T, > T23_Copy for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T23_Copy for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T23_Copy for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A32_N: usize, > T23_Copy for Arr<A5_T, A32_N, > where A5_T: T23_Copy,  {
}

impl T23_Copy for D1_Global {
}

impl<A6_A, > T23_Copy for C<7, (Box<A6_A, >, ), > where  {
}

impl<A6_A, > T23_Copy for C<8, (Box<A6_A, >, ), > where A6_A: T23_Copy,  {
}

impl T23_Copy for int {
}

impl T23_Copy for nat {
}

impl<A6_A, A33_F, > T29_Fn<A6_A, > for C<2, (Box<A33_F, >, ), > where A6_A: Tuple, A33_F: T29_Fn<A6_A, >, A33_F : ?Sized,  {
}

impl<A25_Args, A33_F, A6_A, > T29_Fn<A25_Args, > for C<4, (Box<A33_F, >, Box<A6_A, >, ), > where A25_Args: Tuple, A33_F: T29_Fn<A25_Args, >, A6_A: T7_Allocator, A33_F : ?Sized,  {
}

impl<A6_A, A33_F, > T28_FnMut<A6_A, > for C<2, (Box<A33_F, >, ), > where A6_A: Tuple, A33_F: T29_Fn<A6_A, >, A33_F : ?Sized,  {
}

impl<A6_A, A33_F, > T28_FnMut<A6_A, > for C<3, (Box<A33_F, >, ), > where A6_A: Tuple, A33_F: T28_FnMut<A6_A, >, A33_F : ?Sized,  {
}

impl<A25_Args, A33_F, A6_A, > T28_FnMut<A25_Args, > for C<4, (Box<A33_F, >, Box<A6_A, >, ), > where A25_Args: Tuple, A33_F: T28_FnMut<A25_Args, >, A6_A: T7_Allocator, A33_F : ?Sized,  {
}

impl<A6_A, A33_F, > T26_FnOnce<A6_A, > for C<2, (Box<A33_F, >, ), > where A6_A: Tuple, A33_F: T29_Fn<A6_A, >, A33_F : ?Sized,  {
    type A27_Output = <A33_F as T26_FnOnce<A6_A, >>::A27_Output;
}

impl<A6_A, A33_F, > T26_FnOnce<A6_A, > for C<3, (Box<A33_F, >, ), > where A6_A: Tuple, A33_F: T28_FnMut<A6_A, >, A33_F : ?Sized,  {
    type A27_Output = <A33_F as T26_FnOnce<A6_A, >>::A27_Output;
}

impl<A25_Args, A33_F, A6_A, > T26_FnOnce<A25_Args, > for C<4, (Box<A33_F, >, Box<A6_A, >, ), > where A25_Args: Tuple, A33_F: T26_FnOnce<A25_Args, >, A6_A: T7_Allocator, A33_F : ?Sized,  {
    type A27_Output = <A33_F as T26_FnOnce<A25_Args, >>::A27_Output;
}

impl<A6_A, > T7_Allocator for C<2, (Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A : ?Sized,  {
}

impl<A6_A, > T7_Allocator for C<3, (Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A : ?Sized,  {
}

impl T7_Allocator for D1_Global {
}

impl<A5_T, A6_A, > T7_Allocator for C<4, (Box<A5_T, >, Box<A6_A, >, ), > where A5_T: T7_Allocator, A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T7_Allocator for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A5_T: T7_Allocator, A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T7_Allocator for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A5_T: T7_Allocator, A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, > T3_ToOwned for A5_T where A5_T: T22_Clone,  {
    type A20_Owned = A5_T;
}

impl<A5_T, > T3_ToOwned for [A5_T] where A5_T: T22_Clone,  {
    type A20_Owned = D8_Vec<A5_T, D1_Global, >;
}

impl T3_ToOwned for str {
    type A20_Owned = D14_String;
}

impl<A5_T, > T31_CowObservation<A5_T, > for D4_Cow<[A5_T], > where A5_T: T22_Clone,  {
}
