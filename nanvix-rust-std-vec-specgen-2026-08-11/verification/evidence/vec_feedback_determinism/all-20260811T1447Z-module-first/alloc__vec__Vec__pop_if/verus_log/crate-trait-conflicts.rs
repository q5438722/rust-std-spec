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



trait T20_ArrayAdditionalSpecFns<A4_T, > where Self: T19_View, Self: T19_View<A2_V = D15_Seq<A4_T, >>,  {
}

trait T21_SliceAdditionalSpecFns<A4_T, > where Self: T19_View, Self: T19_View<A2_V = D15_Seq<A4_T, >>,  {
}

trait T19_View {
    type A2_V : ;
}

trait T22_DeepView {
    type A2_V : ;
}

trait T23_Clone where Self: Sized,  {
}

trait T24_Copy where Self: T23_Clone,  {
}

trait T26_PartialEq<A25_Rhs, > where A25_Rhs : ?Sized,  {
}

trait T27_Tuple {
}

trait T29_FnOnce<A28_Args, > where A28_Args: Tuple,  {
    type A30_Output : ;
}

trait T31_FnMut<A28_Args, > where Self: T29_FnOnce<A28_Args, >, A28_Args: Tuple,  {
}

trait T32_Fn<A28_Args, > where Self: T31_FnMut<A28_Args, >, A28_Args: Tuple,  {
}

trait T8_Allocator {
}

trait T33_Debug {
}

trait T34_OptionAdditionalFns<A4_T, > where Self: Sized,  {
}

trait T35_RangeBounds<A4_T, > where A4_T : ?Sized,  {
}

trait T36_VecAdditionalSpecFns<A4_T, > where Self: T19_View, Self: T19_View<A2_V = D15_Seq<A4_T, >>,  {
}

trait T37_CapacitySpec {
}

struct D1_Global(
);

struct D3_Option<A2_V, >(
    Box<A2_V, >,
) where ;

struct D5_MaybeUninit<A4_T, >(
    Box<A4_T, >,
) where ;

struct D6_Bound<A4_T, >(
    Box<A4_T, >,
) where ;

struct D9_Vec<A4_T, A7_A, >(
    Box<A4_T, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

struct D10_IntoIter<A4_T, A7_A, >(
    Box<A4_T, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

struct D11_ISet<A7_A, >(
    Box<A7_A, >,
    C<0, (Box<(A7_A, ), >, Box<bool, >, ), >,
) where ;

struct D12_Provenance(
);

struct D13_PtrData<A4_T, >(
    Box<A4_T, >,
    <A4_T as std::ptr::Pointee>::Metadata,
) where A4_T : ?Sized, ;

struct D14_SeqInner<A7_A, >(
    Box<A7_A, >,
) where ;

struct D15_Seq<A7_A, >(
    Box<A7_A, >,
    D14_SeqInner<A7_A, >,
) where ;

struct D16_Drain<A4_T, A7_A, >(
    Box<A4_T, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

struct D18_ExtractIf<A4_T, A17_F, A7_A, >(
    Box<A4_T, >,
    Box<A17_F, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

impl<A4_T, const A38_N: usize, > T19_View for Arr<A4_T, A38_N, > where  {
    type A2_V = D15_Seq<A4_T, >;
}

impl<A4_T, const A38_N: usize, > T22_DeepView for Arr<A4_T, A38_N, > where A4_T: T22_DeepView,  {
    type A2_V = D15_Seq<<A4_T as T22_DeepView>::A2_V, >;
}

impl<A4_T, const A38_N: usize, > T20_ArrayAdditionalSpecFns<A4_T, > for Arr<A4_T, A38_N, > where  {
}

impl<A4_T, > T19_View for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
    type A2_V = D13_PtrData<A4_T, >;
}

impl<A4_T, > T19_View for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
    type A2_V = D13_PtrData<A4_T, >;
}

impl<A4_T, > T19_View for [A4_T] where  {
    type A2_V = D15_Seq<A4_T, >;
}

impl<A4_T, > T22_DeepView for [A4_T] where A4_T: T22_DeepView,  {
    type A2_V = D15_Seq<<A4_T as T22_DeepView>::A2_V, >;
}

impl<A4_T, > T21_SliceAdditionalSpecFns<A4_T, > for [A4_T] where  {
}

impl<A7_A, > T19_View for C<2, (Box<A7_A, >, ), > where A7_A: T19_View, A7_A : ?Sized,  {
    type A2_V = <A7_A as T19_View>::A2_V;
}

impl<A7_A, > T22_DeepView for C<2, (Box<A7_A, >, ), > where A7_A: T22_DeepView, A7_A : ?Sized,  {
    type A2_V = <A7_A as T22_DeepView>::A2_V;
}

impl<A7_A, > T19_View for C<4, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T19_View, A7_A : ?Sized,  {
    type A2_V = <A7_A as T19_View>::A2_V;
}

impl<A7_A, > T22_DeepView for C<4, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T22_DeepView, A7_A : ?Sized,  {
    type A2_V = <A7_A as T22_DeepView>::A2_V;
}

impl<A7_A, > T19_View for C<5, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T19_View,  {
    type A2_V = <A7_A as T19_View>::A2_V;
}

impl<A7_A, > T22_DeepView for C<5, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T22_DeepView,  {
    type A2_V = <A7_A as T22_DeepView>::A2_V;
}

impl<A7_A, > T19_View for C<6, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T19_View,  {
    type A2_V = <A7_A as T19_View>::A2_V;
}

impl<A7_A, > T22_DeepView for C<6, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T22_DeepView,  {
    type A2_V = <A7_A as T22_DeepView>::A2_V;
}

impl<A4_T, A7_A, > T19_View for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator,  {
    type A2_V = D15_Seq<A4_T, >;
}

impl<A4_T, A7_A, > T22_DeepView for D9_Vec<A4_T, A7_A, > where A4_T: T22_DeepView, A7_A: T8_Allocator,  {
    type A2_V = D15_Seq<<A4_T as T22_DeepView>::A2_V, >;
}

impl<A4_T, > T19_View for D3_Option<A4_T, > where  {
    type A2_V = D3_Option<A4_T, >;
}

impl<A4_T, > T22_DeepView for D3_Option<A4_T, > where A4_T: T22_DeepView,  {
    type A2_V = D3_Option<<A4_T as T22_DeepView>::A2_V, >;
}

impl T19_View for () {
    type A2_V = ();
}

impl T22_DeepView for () {
    type A2_V = ();
}

impl T19_View for bool {
    type A2_V = bool;
}

impl T22_DeepView for bool {
    type A2_V = bool;
}

impl T19_View for usize {
    type A2_V = usize;
}

impl T22_DeepView for usize {
    type A2_V = usize;
}

impl<A39_A0, > T19_View for (Box<A39_A0, >, ) where A39_A0: T19_View,  {
    type A2_V = (Box<<A39_A0 as T19_View>::A2_V, >, );
}

impl<A39_A0, > T22_DeepView for (Box<A39_A0, >, ) where A39_A0: T22_DeepView,  {
    type A2_V = (Box<<A39_A0 as T22_DeepView>::A2_V, >, );
}

impl<A39_A0, A40_A1, > T19_View for (Box<A39_A0, >, Box<A40_A1, >, ) where A39_A0: T19_View, A40_A1: T19_View,  {
    type A2_V = (Box<<A39_A0 as T19_View>::A2_V, >, Box<<A40_A1 as T19_View>::A2_V, >, );
}

impl<A39_A0, A40_A1, > T22_DeepView for (Box<A39_A0, >, Box<A40_A1, >, ) where A39_A0: T22_DeepView, A40_A1: T22_DeepView,  {
    type A2_V = (Box<<A39_A0 as T22_DeepView>::A2_V, >, Box<<A40_A1 as T22_DeepView>::A2_V, >, );
}

impl<A4_T, > T34_OptionAdditionalFns<A4_T, > for D3_Option<A4_T, > where  {
}

impl<A4_T, A7_A, > T36_VecAdditionalSpecFns<A4_T, > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator,  {
}

impl<A4_T, A7_A, > T23_Clone for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl<A4_T, A7_A, > T23_Clone for C<4, (Box<[A4_T], >, Box<A7_A, >, ), > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl<A4_T, > T23_Clone for D5_MaybeUninit<A4_T, > where A4_T: T24_Copy,  {
}

impl T23_Clone for usize {
}

impl T23_Clone for bool {
}

impl<A4_T, > T23_Clone for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for C<2, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for D6_Bound<A4_T, > where A4_T: T23_Clone,  {
}

impl<A4_T, const A38_N: usize, > T23_Clone for Arr<A4_T, A38_N, > where A4_T: T23_Clone,  {
}

impl T23_Clone for D1_Global {
}

impl<A4_T, A7_A, > T23_Clone for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T23_Clone, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T23_Clone for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T23_Clone, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T23_Clone for D10_IntoIter<A4_T, A7_A, > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl<A4_T, A7_A, > T23_Clone for D9_Vec<A4_T, A7_A, > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl<A7_A, > T23_Clone for C<7, (Box<A7_A, >, ), > where  {
}

impl<A7_A, > T23_Clone for C<8, (Box<A7_A, >, ), > where A7_A: T24_Copy,  {
}

impl T23_Clone for int {
}

impl T23_Clone for nat {
}

impl<A7_A, A41_B, > T26_PartialEq<C<2, (Box<A41_B, >, ), >, > for C<2, (Box<A7_A, >, ), > where A7_A: T26_PartialEq<A41_B, >, A7_A : ?Sized, A41_B : ?Sized,  {
}

impl<A7_A, A41_B, > T26_PartialEq<C<3, (Box<A41_B, >, ), >, > for C<2, (Box<A7_A, >, ), > where A7_A: T26_PartialEq<A41_B, >, A7_A : ?Sized, A41_B : ?Sized,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<Arr<A42_U, A38_N, >, > for C<2, (Box<[A4_T], >, ), > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<D9_Vec<A42_U, A7_A, >, > for C<2, (Box<[A4_T], >, ), > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, > T26_PartialEq<C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), >, > for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T26_PartialEq<C<1, (Box<A4_T, >, ), >, > for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl T26_PartialEq<(), > for () {
}

impl T26_PartialEq<bool, > for bool {
}

impl T26_PartialEq<usize, > for usize {
}

impl<A7_A, A41_B, > T26_PartialEq<C<3, (Box<A41_B, >, ), >, > for C<3, (Box<A7_A, >, ), > where A7_A: T26_PartialEq<A41_B, >, A7_A : ?Sized, A41_B : ?Sized,  {
}

impl<A7_A, A41_B, > T26_PartialEq<C<2, (Box<A41_B, >, ), >, > for C<3, (Box<A7_A, >, ), > where A7_A: T26_PartialEq<A41_B, >, A7_A : ?Sized, A41_B : ?Sized,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<Arr<A42_U, A38_N, >, > for C<3, (Box<[A4_T], >, ), > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<D9_Vec<A42_U, A7_A, >, > for C<3, (Box<[A4_T], >, ), > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, > T26_PartialEq<D6_Bound<A4_T, >, > for D6_Bound<A4_T, > where A4_T: T26_PartialEq<A4_T, >,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<Arr<A42_U, A38_N, >, > for Arr<A4_T, A38_N, > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<[A42_U], > for Arr<A4_T, A38_N, > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<C<2, (Box<[A42_U], >, ), >, > for Arr<A4_T, A38_N, > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<C<3, (Box<[A42_U], >, ), >, > for Arr<A4_T, A38_N, > where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, const A38_N: usize, > T26_PartialEq<Arr<A42_U, A38_N, >, > for [A4_T] where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, > T26_PartialEq<[A42_U], > for [A4_T] where A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<D9_Vec<A42_U, A7_A, >, > for [A4_T] where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, > T26_PartialEq<D3_Option<A4_T, >, > for D3_Option<A4_T, > where A4_T: T26_PartialEq<A4_T, >,  {
}

impl<A4_T, > T26_PartialEq<(Box<A4_T, >, ), > for (Box<A4_T, >, ) where A4_T: T26_PartialEq<A4_T, >,  {
}

impl<A42_U, A4_T, > T26_PartialEq<(Box<A42_U, >, Box<A4_T, >, ), > for (Box<A42_U, >, Box<A4_T, >, ) where A42_U: T26_PartialEq<A42_U, >, A4_T: T26_PartialEq<A4_T, >,  {
}

impl<A4_T, A7_A, > T26_PartialEq<C<4, (Box<A4_T, >, Box<A7_A, >, ), >, > for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T26_PartialEq<A4_T, >, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A42_U, A40_A1, A43_A2, > T26_PartialEq<D9_Vec<A42_U, A43_A2, >, > for D9_Vec<A4_T, A40_A1, > where A40_A1: T8_Allocator, A43_A2: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<C<2, (Box<[A42_U], >, ), >, > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<C<3, (Box<[A42_U], >, ), >, > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, > T26_PartialEq<[A42_U], > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, const A38_N: usize, > T26_PartialEq<Arr<A42_U, A38_N, >, > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A42_U, A7_A, const A38_N: usize, > T26_PartialEq<C<2, (Box<Arr<A42_U, A38_N, >, >, ), >, > for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator, A4_T: T26_PartialEq<A42_U, >,  {
}

impl<A4_T, A7_A, > T26_PartialEq<C<5, (Box<A4_T, >, Box<A7_A, >, ), >, > for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T26_PartialEq<A4_T, >, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T26_PartialEq<C<6, (Box<A4_T, >, Box<A7_A, >, ), >, > for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T26_PartialEq<A4_T, >, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl T26_PartialEq<int, > for int {
}

impl T26_PartialEq<nat, > for nat {
}

impl<A4_T, > T24_Copy for D5_MaybeUninit<A4_T, > where A4_T: T24_Copy,  {
}

impl T24_Copy for usize {
}

impl T24_Copy for bool {
}

impl<A4_T, > T24_Copy for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T24_Copy for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T24_Copy for C<2, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T24_Copy for D6_Bound<A4_T, > where A4_T: T24_Copy,  {
}

impl<A4_T, const A38_N: usize, > T24_Copy for Arr<A4_T, A38_N, > where A4_T: T24_Copy,  {
}

impl<A4_T, > T24_Copy for D3_Option<A4_T, > where A4_T: T24_Copy,  {
}

impl T24_Copy for D1_Global {
}

impl<A7_A, > T24_Copy for C<7, (Box<A7_A, >, ), > where  {
}

impl<A7_A, > T24_Copy for C<8, (Box<A7_A, >, ), > where A7_A: T24_Copy,  {
}

impl T24_Copy for int {
}

impl T24_Copy for nat {
}

impl<A7_A, A17_F, > T32_Fn<A7_A, > for C<2, (Box<A17_F, >, ), > where A7_A: Tuple, A17_F: T32_Fn<A7_A, >, A17_F : ?Sized,  {
}

impl<A28_Args, A17_F, A7_A, > T32_Fn<A28_Args, > for C<4, (Box<A17_F, >, Box<A7_A, >, ), > where A28_Args: Tuple, A17_F: T32_Fn<A28_Args, >, A7_A: T8_Allocator, A17_F : ?Sized,  {
}

impl<A7_A, A17_F, > T31_FnMut<A7_A, > for C<2, (Box<A17_F, >, ), > where A7_A: Tuple, A17_F: T32_Fn<A7_A, >, A17_F : ?Sized,  {
}

impl<A7_A, A17_F, > T31_FnMut<A7_A, > for C<3, (Box<A17_F, >, ), > where A7_A: Tuple, A17_F: T31_FnMut<A7_A, >, A17_F : ?Sized,  {
}

impl<A28_Args, A17_F, A7_A, > T31_FnMut<A28_Args, > for C<4, (Box<A17_F, >, Box<A7_A, >, ), > where A28_Args: Tuple, A17_F: T31_FnMut<A28_Args, >, A7_A: T8_Allocator, A17_F : ?Sized,  {
}

impl<A7_A, A17_F, > T29_FnOnce<A7_A, > for C<2, (Box<A17_F, >, ), > where A7_A: Tuple, A17_F: T32_Fn<A7_A, >, A17_F : ?Sized,  {
    type A30_Output = <A17_F as T29_FnOnce<A7_A, >>::A30_Output;
}

impl<A7_A, A17_F, > T29_FnOnce<A7_A, > for C<3, (Box<A17_F, >, ), > where A7_A: Tuple, A17_F: T31_FnMut<A7_A, >, A17_F : ?Sized,  {
    type A30_Output = <A17_F as T29_FnOnce<A7_A, >>::A30_Output;
}

impl<A28_Args, A17_F, A7_A, > T29_FnOnce<A28_Args, > for C<4, (Box<A17_F, >, Box<A7_A, >, ), > where A28_Args: Tuple, A17_F: T29_FnOnce<A28_Args, >, A7_A: T8_Allocator, A17_F : ?Sized,  {
    type A30_Output = <A17_F as T29_FnOnce<A28_Args, >>::A30_Output;
}

impl<A4_T, > T35_RangeBounds<A4_T, > for (Box<D6_Bound<A4_T, >, >, Box<D6_Bound<A4_T, >, >, ) where  {
}

impl<A4_T, > T35_RangeBounds<A4_T, > for (Box<D6_Bound<C<2, (Box<A4_T, >, ), >, >, >, Box<D6_Bound<C<2, (Box<A4_T, >, ), >, >, >, ) where A4_T : ?Sized,  {
}

impl<A4_T, > T33_Debug for D5_MaybeUninit<A4_T, > where  {
}

impl<A4_T, > T33_Debug for D6_Bound<A4_T, > where A4_T: T33_Debug,  {
}

impl<A4_T, const A38_N: usize, > T33_Debug for Arr<A4_T, A38_N, > where A4_T: T33_Debug,  {
}

impl<A4_T, > T33_Debug for D3_Option<A4_T, > where A4_T: T33_Debug,  {
}

impl T33_Debug for usize {
}

impl<A4_T, > T33_Debug for C<2, (Box<A4_T, >, ), > where A4_T: T33_Debug, A4_T : ?Sized,  {
}

impl<A4_T, > T33_Debug for C<3, (Box<A4_T, >, ), > where A4_T: T33_Debug, A4_T : ?Sized,  {
}

impl T33_Debug for bool {
}

impl<A4_T, > T33_Debug for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T33_Debug for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A42_U, A4_T, > T33_Debug for (Box<A42_U, >, Box<A4_T, >, ) where A42_U: T33_Debug, A4_T: T33_Debug,  {
}

impl<A4_T, > T33_Debug for (Box<A4_T, >, ) where A4_T: T33_Debug,  {
}

impl<A4_T, > T33_Debug for [A4_T] where A4_T: T33_Debug,  {
}

impl T33_Debug for () {
}

impl T33_Debug for D1_Global {
}

impl<A4_T, A7_A, > T33_Debug for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T33_Debug, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T33_Debug for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T33_Debug, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T33_Debug for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T33_Debug, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T33_Debug for D10_IntoIter<A4_T, A7_A, > where A4_T: T33_Debug, A7_A: T8_Allocator,  {
}

impl<A4_T, A7_A, > T33_Debug for D9_Vec<A4_T, A7_A, > where A4_T: T33_Debug, A7_A: T8_Allocator,  {
}

impl<A7_A, > T33_Debug for C<8, (Box<A7_A, >, ), > where  {
}

impl<A7_A, > T8_Allocator for C<2, (Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A : ?Sized,  {
}

impl<A7_A, > T8_Allocator for C<3, (Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A : ?Sized,  {
}

impl T8_Allocator for D1_Global {
}

impl<A4_T, A7_A, > T8_Allocator for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T8_Allocator, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T8_Allocator for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T8_Allocator, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T8_Allocator for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T8_Allocator, A7_A: T8_Allocator, A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for D3_Option<A4_T, > where A4_T: T23_Clone,  {
}

impl<A4_T, A7_A, > T37_CapacitySpec for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator,  {
}

impl<A4_T, A17_F, A7_A, > T33_Debug for D18_ExtractIf<A4_T, A17_F, A7_A, > where A4_T: T33_Debug, A7_A: T8_Allocator,  {
}

impl<A4_T, A7_A, > T33_Debug for D16_Drain<A4_T, A7_A, > where A4_T: T33_Debug, A7_A: T8_Allocator,  {
}
