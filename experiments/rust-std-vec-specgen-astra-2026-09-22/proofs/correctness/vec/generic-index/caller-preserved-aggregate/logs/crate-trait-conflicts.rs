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



trait T19_ArrayAdditionalSpecFns<A5_T, > where Self: T17_View, Self: T17_View<A18_V = D14_Seq<A5_T, >>,  {
}

trait T20_SliceAdditionalSpecFns<A5_T, > where Self: T17_View, Self: T17_View<A18_V = D14_Seq<A5_T, >>,  {
}

trait T21_SliceIndex<A5_T, > where A5_T : ?Sized,  {
    type A22_Output : ?Sized;
}

trait T23_SliceIndexSpec<A5_T, > where Self: T21_SliceIndex<A5_T, >, A5_T : ?Sized,  {
}

trait T24_StringSliceAdditionalSpecFns {
}

trait T17_View {
    type A18_V : ;
}

trait T3_ToOwned {
    type A25_Owned : T26_Borrow<Self, >;
}

trait T27_Clone where Self: Sized,  {
}

trait T28_Copy where Self: T27_Clone,  {
}

trait T29_Tuple {
}

trait T31_FnOnce<A30_Args, > where A30_Args: Tuple,  {
    type A22_Output : ;
}

trait T32_FnMut<A30_Args, > where Self: T31_FnOnce<A30_Args, >, A30_Args: Tuple,  {
}

trait T33_Fn<A30_Args, > where Self: T32_FnMut<A30_Args, >, A30_Args: Tuple,  {
}

trait T34_Deref {
    type A35_Target : ?Sized;
}

trait T37_Index<A36_Idx, > where A36_Idx : ?Sized,  {
    type A22_Output : ?Sized;
}

trait T38_Integer where Self: T28_Copy,  {
}

trait T8_Allocator {
}

trait T26_Borrow<A39_Borrowed, > where A39_Borrowed : ?Sized,  {
}

trait T40_IndexSpec<A36_Idx, > where Self: T37_Index<A36_Idx, >, A36_Idx : ?Sized,  {
}

trait T41_RangeBounds<A5_T, > where A5_T : ?Sized,  {
}

trait T42_RangeBoundsSpec<A5_T, > where Self: T41_RangeBounds<A5_T, >, A5_T : ?Sized,  {
}

trait T43_CowObservation<A5_T, > where  {
}

struct D1_Global(
);

struct D4_Cow<A2_B, >(
    Box<A2_B, >,
) where A2_B: T3_ToOwned, A2_B : ?Sized, ;

struct D6_Bound<A5_T, >(
    Box<A5_T, >,
) where ;

struct D9_Vec<A5_T, A7_A, >(
    Box<A5_T, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

struct D10_ISet<A7_A, >(
    Box<A7_A, >,
    C<0, (Box<(A7_A, ), >, Box<bool, >, ), >,
) where ;

struct D11_Provenance(
);

struct D12_PtrData<A5_T, >(
    Box<A5_T, >,
    <A5_T as std::ptr::Pointee>::Metadata,
) where A5_T : ?Sized, ;

struct D13_SeqInner<A7_A, >(
    Box<A7_A, >,
) where ;

struct D14_Seq<A7_A, >(
    Box<A7_A, >,
    D13_SeqInner<A7_A, >,
) where ;

struct D15_String(
);

struct D16_CowContents<A5_T, >(
    Box<A5_T, >,
) where ;

impl<A5_T, const A44_N: usize, > T17_View for Arr<A5_T, A44_N, > where  {
    type A18_V = D14_Seq<A5_T, >;
}

impl<A5_T, const A44_N: usize, > T19_ArrayAdditionalSpecFns<A5_T, > for Arr<A5_T, A44_N, > where  {
}

impl<A5_T, > T17_View for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A18_V = D12_PtrData<A5_T, >;
}

impl<A5_T, > T17_View for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
    type A18_V = D12_PtrData<A5_T, >;
}

impl<A5_T, > T17_View for [A5_T] where  {
    type A18_V = D14_Seq<A5_T, >;
}

impl<A5_T, > T20_SliceAdditionalSpecFns<A5_T, > for [A5_T] where  {
}

impl T17_View for str {
    type A18_V = D14_Seq<char, >;
}

impl T24_StringSliceAdditionalSpecFns for str {
}

impl T17_View for D15_String {
    type A18_V = D14_Seq<char, >;
}

impl T23_SliceIndexSpec<str, > for (Box<D6_Bound<usize, >, >, Box<D6_Bound<usize, >, >, ) {
}

impl<A45_I, > T40_IndexSpec<A45_I, > for str where A45_I: T23_SliceIndexSpec<str, >,  {
}

impl<A7_A, > T17_View for C<2, (Box<A7_A, >, ), > where A7_A: T17_View, A7_A : ?Sized,  {
    type A18_V = <A7_A as T17_View>::A18_V;
}

impl<A7_A, > T17_View for C<4, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T17_View, A7_A : ?Sized,  {
    type A18_V = <A7_A as T17_View>::A18_V;
}

impl<A7_A, > T17_View for C<5, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T17_View,  {
    type A18_V = <A7_A as T17_View>::A18_V;
}

impl<A7_A, > T17_View for C<6, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T17_View,  {
    type A18_V = <A7_A as T17_View>::A18_V;
}

impl<A5_T, A7_A, > T17_View for D9_Vec<A5_T, A7_A, > where A7_A: T8_Allocator,  {
    type A18_V = D14_Seq<A5_T, >;
}

impl T17_View for () {
    type A18_V = ();
}

impl T17_View for bool {
    type A18_V = bool;
}

impl T17_View for u8 {
    type A18_V = u8;
}

impl T17_View for u32 {
    type A18_V = u32;
}

impl T17_View for usize {
    type A18_V = usize;
}

impl T17_View for i32 {
    type A18_V = i32;
}

impl T17_View for char {
    type A18_V = char;
}

impl<A46_A0, A47_A1, > T17_View for (Box<A46_A0, >, Box<A47_A1, >, ) where A46_A0: T17_View, A47_A1: T17_View,  {
    type A18_V = (Box<<A46_A0 as T17_View>::A18_V, >, Box<<A47_A1 as T17_View>::A18_V, >, );
}

impl<A5_T, > T17_View for D4_Cow<A5_T, > where A5_T: T17_View, A5_T: T27_Clone,  {
    type A18_V = <A5_T as T17_View>::A18_V;
}

impl T17_View for D4_Cow<str, > {
    type A18_V = D14_Seq<char, >;
}

impl<A5_T, > T17_View for D4_Cow<[A5_T], > where A5_T: T17_View, A5_T: T27_Clone,  {
    type A18_V = D14_Seq<A5_T, >;
}

impl<A5_T, > T42_RangeBoundsSpec<A5_T, > for (Box<D6_Bound<A5_T, >, >, Box<D6_Bound<A5_T, >, >, ) where  {
}

impl<A5_T, > T42_RangeBoundsSpec<A5_T, > for (Box<D6_Bound<C<2, (Box<A5_T, >, ), >, >, >, Box<D6_Bound<C<2, (Box<A5_T, >, ), >, >, >, ) where A5_T : ?Sized,  {
}

impl<A5_T, > T23_SliceIndexSpec<[A5_T], > for usize where  {
}

impl<A5_T, A45_I, > T40_IndexSpec<A45_I, > for [A5_T] where A45_I: T21_SliceIndex<[A5_T], >,  {
}

impl<A5_T, A45_I, const A44_N: usize, > T40_IndexSpec<A45_I, > for Arr<A5_T, A44_N, > where [A5_T]: T37_Index<A45_I, >,  {
}

impl<A5_T, A45_I, A7_A, > T40_IndexSpec<A45_I, > for D9_Vec<A5_T, A7_A, > where A45_I: T21_SliceIndex<[A5_T], >, A7_A: T8_Allocator,  {
}

impl<A5_T, > T26_Borrow<A5_T, > for A5_T where A5_T : ?Sized,  {
}

impl<A5_T, > T26_Borrow<A5_T, > for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T26_Borrow<A5_T, > for C<3, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A44_N: usize, > T26_Borrow<[A5_T], > for Arr<A5_T, A44_N, > where  {
}

impl<A2_B, > T26_Borrow<A2_B, > for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A7_A, > T26_Borrow<A5_T, > for C<4, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T26_Borrow<A5_T, > for C<5, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T26_Borrow<[A5_T], > for D9_Vec<A5_T, A7_A, > where A7_A: T8_Allocator,  {
}

impl T26_Borrow<str, > for D15_String {
}

impl<A5_T, A7_A, > T26_Borrow<A5_T, > for C<6, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T27_Clone for C<4, (Box<A5_T, >, Box<A7_A, >, ), > where A5_T: T27_Clone, A7_A: T8_Allocator, A7_A: T27_Clone,  {
}

impl<A5_T, A7_A, > T27_Clone for C<4, (Box<[A5_T], >, Box<A7_A, >, ), > where A5_T: T27_Clone, A7_A: T8_Allocator, A7_A: T27_Clone,  {
}

impl T27_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T27_Clone for usize {
}

impl T27_Clone for u8 {
}

impl T27_Clone for u32 {
}

impl T27_Clone for i32 {
}

impl T27_Clone for bool {
}

impl T27_Clone for char {
}

impl<A5_T, > T27_Clone for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T27_Clone for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T27_Clone for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T27_Clone for D6_Bound<A5_T, > where A5_T: T27_Clone,  {
}

impl<A5_T, const A44_N: usize, > T27_Clone for Arr<A5_T, A44_N, > where A5_T: T27_Clone,  {
}

impl T27_Clone for D1_Global {
}

impl<A2_B, > T27_Clone for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A7_A, > T27_Clone for C<5, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T27_Clone, A5_T : ?Sized,  {
}

impl T27_Clone for D15_String {
}

impl<A5_T, A7_A, > T27_Clone for C<6, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T27_Clone, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T27_Clone for D9_Vec<A5_T, A7_A, > where A5_T: T27_Clone, A7_A: T8_Allocator, A7_A: T27_Clone,  {
}

impl<A7_A, > T27_Clone for C<7, (Box<A7_A, >, ), > where  {
}

impl<A7_A, > T27_Clone for C<8, (Box<A7_A, >, ), > where A7_A: T28_Copy,  {
}

impl T27_Clone for int {
}

impl T27_Clone for nat {
}

impl T28_Copy for usize {
}

impl T28_Copy for u8 {
}

impl T28_Copy for u32 {
}

impl T28_Copy for i32 {
}

impl T28_Copy for bool {
}

impl T28_Copy for char {
}

impl<A5_T, > T28_Copy for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T28_Copy for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T28_Copy for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T28_Copy for D6_Bound<A5_T, > where A5_T: T28_Copy,  {
}

impl<A5_T, const A44_N: usize, > T28_Copy for Arr<A5_T, A44_N, > where A5_T: T28_Copy,  {
}

impl T28_Copy for D1_Global {
}

impl<A7_A, > T28_Copy for C<7, (Box<A7_A, >, ), > where  {
}

impl<A7_A, > T28_Copy for C<8, (Box<A7_A, >, ), > where A7_A: T28_Copy,  {
}

impl T28_Copy for int {
}

impl T28_Copy for nat {
}

impl<A5_T, > T34_Deref for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A35_Target = A5_T;
}

impl<A5_T, > T34_Deref for C<3, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A35_Target = A5_T;
}

impl<A2_B, > T34_Deref for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
    type A35_Target = A2_B;
}

impl<A5_T, A7_A, > T34_Deref for C<4, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
    type A35_Target = A5_T;
}

impl<A5_T, A7_A, > T34_Deref for C<5, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
    type A35_Target = A5_T;
}

impl T34_Deref for D15_String {
    type A35_Target = str;
}

impl<A5_T, A7_A, > T34_Deref for C<6, (Box<A5_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A5_T : ?Sized,  {
    type A35_Target = A5_T;
}

impl<A5_T, A7_A, > T34_Deref for D9_Vec<A5_T, A7_A, > where A7_A: T8_Allocator,  {
    type A35_Target = [A5_T];
}

impl<A7_A, A48_F, > T33_Fn<A7_A, > for C<2, (Box<A48_F, >, ), > where A7_A: Tuple, A48_F: T33_Fn<A7_A, >, A48_F : ?Sized,  {
}

impl<A30_Args, A48_F, A7_A, > T33_Fn<A30_Args, > for C<4, (Box<A48_F, >, Box<A7_A, >, ), > where A30_Args: Tuple, A48_F: T33_Fn<A30_Args, >, A7_A: T8_Allocator, A48_F : ?Sized,  {
}

impl<A7_A, A48_F, > T32_FnMut<A7_A, > for C<2, (Box<A48_F, >, ), > where A7_A: Tuple, A48_F: T33_Fn<A7_A, >, A48_F : ?Sized,  {
}

impl<A7_A, A48_F, > T32_FnMut<A7_A, > for C<3, (Box<A48_F, >, ), > where A7_A: Tuple, A48_F: T32_FnMut<A7_A, >, A48_F : ?Sized,  {
}

impl<A30_Args, A48_F, A7_A, > T32_FnMut<A30_Args, > for C<4, (Box<A48_F, >, Box<A7_A, >, ), > where A30_Args: Tuple, A48_F: T32_FnMut<A30_Args, >, A7_A: T8_Allocator, A48_F : ?Sized,  {
}

impl<A7_A, A48_F, > T31_FnOnce<A7_A, > for C<2, (Box<A48_F, >, ), > where A7_A: Tuple, A48_F: T33_Fn<A7_A, >, A48_F : ?Sized,  {
    type A22_Output = <A48_F as T31_FnOnce<A7_A, >>::A22_Output;
}

impl<A7_A, A48_F, > T31_FnOnce<A7_A, > for C<3, (Box<A48_F, >, ), > where A7_A: Tuple, A48_F: T32_FnMut<A7_A, >, A48_F : ?Sized,  {
    type A22_Output = <A48_F as T31_FnOnce<A7_A, >>::A22_Output;
}

impl<A30_Args, A48_F, A7_A, > T31_FnOnce<A30_Args, > for C<4, (Box<A48_F, >, Box<A7_A, >, ), > where A30_Args: Tuple, A48_F: T31_FnOnce<A30_Args, >, A7_A: T8_Allocator, A48_F : ?Sized,  {
    type A22_Output = <A48_F as T31_FnOnce<A30_Args, >>::A22_Output;
}

impl<A5_T, A45_I, const A44_N: usize, > T37_Index<A45_I, > for Arr<A5_T, A44_N, > where [A5_T]: T37_Index<A45_I, >,  {
    type A22_Output = <[A5_T] as T37_Index<A45_I, >>::A22_Output;
}

impl<A5_T, A45_I, > T37_Index<A45_I, > for [A5_T] where A45_I: T21_SliceIndex<[A5_T], >,  {
    type A22_Output = <A45_I as T21_SliceIndex<[A5_T], >>::A22_Output;
}

impl<A45_I, > T37_Index<A45_I, > for str where A45_I: T21_SliceIndex<str, >,  {
    type A22_Output = <A45_I as T21_SliceIndex<str, >>::A22_Output;
}

impl<A45_I, > T37_Index<A45_I, > for D15_String where A45_I: T21_SliceIndex<str, >,  {
    type A22_Output = <A45_I as T21_SliceIndex<str, >>::A22_Output;
}

impl<A5_T, A45_I, A7_A, > T37_Index<A45_I, > for D9_Vec<A5_T, A7_A, > where A45_I: T21_SliceIndex<[A5_T], >, A7_A: T8_Allocator,  {
    type A22_Output = <A45_I as T21_SliceIndex<[A5_T], >>::A22_Output;
}

impl<A5_T, > T41_RangeBounds<A5_T, > for (Box<D6_Bound<A5_T, >, >, Box<D6_Bound<A5_T, >, >, ) where  {
}

impl<A5_T, > T41_RangeBounds<A5_T, > for (Box<D6_Bound<C<2, (Box<A5_T, >, ), >, >, >, Box<D6_Bound<C<2, (Box<A5_T, >, ), >, >, >, ) where A5_T : ?Sized,  {
}

impl<A5_T, > T21_SliceIndex<[A5_T], > for usize where  {
    type A22_Output = A5_T;
}

impl<A5_T, > T21_SliceIndex<[A5_T], > for (Box<D6_Bound<usize, >, >, Box<D6_Bound<usize, >, >, ) where  {
    type A22_Output = [A5_T];
}

impl T21_SliceIndex<str, > for (Box<D6_Bound<usize, >, >, Box<D6_Bound<usize, >, >, ) {
    type A22_Output = str;
}

impl<A7_A, > T8_Allocator for C<2, (Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A : ?Sized,  {
}

impl<A7_A, > T8_Allocator for C<3, (Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A : ?Sized,  {
}

impl T8_Allocator for D1_Global {
}

impl<A5_T, A7_A, > T8_Allocator for C<4, (Box<A5_T, >, Box<A7_A, >, ), > where A5_T: T8_Allocator, A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T8_Allocator for C<5, (Box<A5_T, >, Box<A7_A, >, ), > where A5_T: T8_Allocator, A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A7_A, > T8_Allocator for C<6, (Box<A5_T, >, Box<A7_A, >, ), > where A5_T: T8_Allocator, A7_A: T8_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, > T3_ToOwned for A5_T where A5_T: T27_Clone,  {
    type A25_Owned = A5_T;
}

impl<A5_T, > T3_ToOwned for [A5_T] where A5_T: T27_Clone,  {
    type A25_Owned = D9_Vec<A5_T, D1_Global, >;
}

impl T3_ToOwned for str {
    type A25_Owned = D15_String;
}

impl T38_Integer for u8 {
}

impl T38_Integer for u32 {
}

impl T38_Integer for usize {
}

impl T38_Integer for i32 {
}

impl T38_Integer for int {
}

impl T38_Integer for nat {
}

impl T38_Integer for char {
}

impl<A5_T, > T43_CowObservation<A5_T, > for D4_Cow<[A5_T], > where A5_T: T27_Clone,  {
}
