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



trait T14_ArrayAdditionalSpecFns<A2_T, > where Self: T12_View, Self: T12_View<A13_V = D11_Seq<A2_T, >>,  {
}

trait T15_SliceAdditionalSpecFns<A2_T, > where Self: T12_View, Self: T12_View<A13_V = D11_Seq<A2_T, >>,  {
}

trait T16_SliceIndex<A2_T, > where A2_T : ?Sized,  {
    type A17_Output : ?Sized;
}

trait T18_SliceIndexSpec<A2_T, > where Self: T16_SliceIndex<A2_T, >, A2_T : ?Sized,  {
}

trait T19_StringSliceAdditionalSpecFns {
}

trait T12_View {
    type A13_V : ;
}

trait T20_Clone where Self: Sized,  {
}

trait T21_Copy where Self: T20_Clone,  {
}

trait T22_Tuple {
}

trait T24_FnOnce<A23_Args, > where A23_Args: Tuple,  {
    type A17_Output : ;
}

trait T25_FnMut<A23_Args, > where Self: T24_FnOnce<A23_Args, >, A23_Args: Tuple,  {
}

trait T26_Fn<A23_Args, > where Self: T25_FnMut<A23_Args, >, A23_Args: Tuple,  {
}

trait T27_Deref {
    type A28_Target : ?Sized;
}

trait T30_Index<A29_Idx, > where A29_Idx : ?Sized,  {
    type A17_Output : ?Sized;
}

trait T31_Integer where Self: T21_Copy,  {
}

trait T5_Allocator {
}

trait T32_IndexSpec<A29_Idx, > where Self: T30_Index<A29_Idx, >, A29_Idx : ?Sized,  {
}

trait T33_RangeBounds<A2_T, > where A2_T : ?Sized,  {
}

trait T34_RangeBoundsSpec<A2_T, > where Self: T33_RangeBounds<A2_T, >, A2_T : ?Sized,  {
}

struct D1_Global(
);

struct D3_Bound<A2_T, >(
    Box<A2_T, >,
) where ;

struct D6_Vec<A2_T, A4_A, >(
    Box<A2_T, >,
    Box<A4_A, >,
) where A4_A: T5_Allocator, ;

struct D7_ISet<A4_A, >(
    Box<A4_A, >,
    C<0, (Box<(A4_A, ), >, Box<bool, >, ), >,
) where ;

struct D8_Provenance(
);

struct D9_PtrData<A2_T, >(
    Box<A2_T, >,
    <A2_T as std::ptr::Pointee>::Metadata,
) where A2_T : ?Sized, ;

struct D10_SeqInner<A4_A, >(
    Box<A4_A, >,
) where ;

struct D11_Seq<A4_A, >(
    Box<A4_A, >,
    D10_SeqInner<A4_A, >,
) where ;

impl<A2_T, const A35_N: usize, > T12_View for Arr<A2_T, A35_N, > where  {
    type A13_V = D11_Seq<A2_T, >;
}

impl<A2_T, const A35_N: usize, > T14_ArrayAdditionalSpecFns<A2_T, > for Arr<A2_T, A35_N, > where  {
}

impl<A2_T, > T12_View for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
    type A13_V = D9_PtrData<A2_T, >;
}

impl<A2_T, > T12_View for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
    type A13_V = D9_PtrData<A2_T, >;
}

impl<A2_T, > T12_View for [A2_T] where  {
    type A13_V = D11_Seq<A2_T, >;
}

impl<A2_T, > T15_SliceAdditionalSpecFns<A2_T, > for [A2_T] where  {
}

impl T12_View for str {
    type A13_V = D11_Seq<char, >;
}

impl T19_StringSliceAdditionalSpecFns for str {
}

impl T18_SliceIndexSpec<str, > for (Box<D3_Bound<usize, >, >, Box<D3_Bound<usize, >, >, ) {
}

impl<A36_I, > T32_IndexSpec<A36_I, > for str where A36_I: T18_SliceIndexSpec<str, >,  {
}

impl<A4_A, > T12_View for C<2, (Box<A4_A, >, ), > where A4_A: T12_View, A4_A : ?Sized,  {
    type A13_V = <A4_A as T12_View>::A13_V;
}

impl<A4_A, > T12_View for C<4, (Box<A4_A, >, Box<D1_Global, >, ), > where A4_A: T12_View, A4_A : ?Sized,  {
    type A13_V = <A4_A as T12_View>::A13_V;
}

impl<A4_A, > T12_View for C<5, (Box<A4_A, >, Box<D1_Global, >, ), > where A4_A: T12_View,  {
    type A13_V = <A4_A as T12_View>::A13_V;
}

impl<A4_A, > T12_View for C<6, (Box<A4_A, >, Box<D1_Global, >, ), > where A4_A: T12_View,  {
    type A13_V = <A4_A as T12_View>::A13_V;
}

impl<A2_T, A4_A, > T12_View for D6_Vec<A2_T, A4_A, > where A4_A: T5_Allocator,  {
    type A13_V = D11_Seq<A2_T, >;
}

impl T12_View for () {
    type A13_V = ();
}

impl T12_View for bool {
    type A13_V = bool;
}

impl T12_View for u8 {
    type A13_V = u8;
}

impl T12_View for u32 {
    type A13_V = u32;
}

impl T12_View for usize {
    type A13_V = usize;
}

impl T12_View for i32 {
    type A13_V = i32;
}

impl T12_View for char {
    type A13_V = char;
}

impl<A37_A0, A38_A1, > T12_View for (Box<A37_A0, >, Box<A38_A1, >, ) where A37_A0: T12_View, A38_A1: T12_View,  {
    type A13_V = (Box<<A37_A0 as T12_View>::A13_V, >, Box<<A38_A1 as T12_View>::A13_V, >, );
}

impl<A2_T, > T34_RangeBoundsSpec<A2_T, > for (Box<D3_Bound<A2_T, >, >, Box<D3_Bound<A2_T, >, >, ) where  {
}

impl<A2_T, > T34_RangeBoundsSpec<A2_T, > for (Box<D3_Bound<C<2, (Box<A2_T, >, ), >, >, >, Box<D3_Bound<C<2, (Box<A2_T, >, ), >, >, >, ) where A2_T : ?Sized,  {
}

impl<A2_T, > T18_SliceIndexSpec<[A2_T], > for usize where  {
}

impl<A2_T, A36_I, > T32_IndexSpec<A36_I, > for [A2_T] where A36_I: T16_SliceIndex<[A2_T], >,  {
}

impl<A2_T, A36_I, const A35_N: usize, > T32_IndexSpec<A36_I, > for Arr<A2_T, A35_N, > where [A2_T]: T30_Index<A36_I, >,  {
}

impl<A2_T, A36_I, A4_A, > T32_IndexSpec<A36_I, > for D6_Vec<A2_T, A4_A, > where A36_I: T16_SliceIndex<[A2_T], >, A4_A: T5_Allocator,  {
}

impl<A2_T, A4_A, > T20_Clone for C<4, (Box<A2_T, >, Box<A4_A, >, ), > where A2_T: T20_Clone, A4_A: T5_Allocator, A4_A: T20_Clone,  {
}

impl<A2_T, A4_A, > T20_Clone for C<4, (Box<[A2_T], >, Box<A4_A, >, ), > where A2_T: T20_Clone, A4_A: T5_Allocator, A4_A: T20_Clone,  {
}

impl T20_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T20_Clone for usize {
}

impl T20_Clone for u8 {
}

impl T20_Clone for u32 {
}

impl T20_Clone for i32 {
}

impl T20_Clone for bool {
}

impl T20_Clone for char {
}

impl<A2_T, > T20_Clone for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T20_Clone for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T20_Clone for C<2, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T20_Clone for D3_Bound<A2_T, > where A2_T: T20_Clone,  {
}

impl<A2_T, const A35_N: usize, > T20_Clone for Arr<A2_T, A35_N, > where A2_T: T20_Clone,  {
}

impl T20_Clone for D1_Global {
}

impl<A2_T, A4_A, > T20_Clone for C<5, (Box<A2_T, >, Box<A4_A, >, ), > where A4_A: T5_Allocator, A4_A: T20_Clone, A2_T : ?Sized,  {
}

impl<A2_T, A4_A, > T20_Clone for C<6, (Box<A2_T, >, Box<A4_A, >, ), > where A4_A: T5_Allocator, A4_A: T20_Clone, A2_T : ?Sized,  {
}

impl<A2_T, A4_A, > T20_Clone for D6_Vec<A2_T, A4_A, > where A2_T: T20_Clone, A4_A: T5_Allocator, A4_A: T20_Clone,  {
}

impl<A4_A, > T20_Clone for C<7, (Box<A4_A, >, ), > where  {
}

impl<A4_A, > T20_Clone for C<8, (Box<A4_A, >, ), > where A4_A: T21_Copy,  {
}

impl T20_Clone for int {
}

impl T20_Clone for nat {
}

impl T21_Copy for usize {
}

impl T21_Copy for u8 {
}

impl T21_Copy for u32 {
}

impl T21_Copy for i32 {
}

impl T21_Copy for bool {
}

impl T21_Copy for char {
}

impl<A2_T, > T21_Copy for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T21_Copy for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T21_Copy for C<2, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T21_Copy for D3_Bound<A2_T, > where A2_T: T21_Copy,  {
}

impl<A2_T, const A35_N: usize, > T21_Copy for Arr<A2_T, A35_N, > where A2_T: T21_Copy,  {
}

impl T21_Copy for D1_Global {
}

impl<A4_A, > T21_Copy for C<7, (Box<A4_A, >, ), > where  {
}

impl<A4_A, > T21_Copy for C<8, (Box<A4_A, >, ), > where A4_A: T21_Copy,  {
}

impl T21_Copy for int {
}

impl T21_Copy for nat {
}

impl<A2_T, > T27_Deref for C<2, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
    type A28_Target = A2_T;
}

impl<A2_T, > T27_Deref for C<3, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
    type A28_Target = A2_T;
}

impl<A2_T, A4_A, > T27_Deref for C<4, (Box<A2_T, >, Box<A4_A, >, ), > where A4_A: T5_Allocator, A2_T : ?Sized,  {
    type A28_Target = A2_T;
}

impl<A2_T, A4_A, > T27_Deref for C<5, (Box<A2_T, >, Box<A4_A, >, ), > where A4_A: T5_Allocator, A2_T : ?Sized,  {
    type A28_Target = A2_T;
}

impl<A2_T, A4_A, > T27_Deref for C<6, (Box<A2_T, >, Box<A4_A, >, ), > where A4_A: T5_Allocator, A2_T : ?Sized,  {
    type A28_Target = A2_T;
}

impl<A2_T, A4_A, > T27_Deref for D6_Vec<A2_T, A4_A, > where A4_A: T5_Allocator,  {
    type A28_Target = [A2_T];
}

impl<A4_A, A39_F, > T26_Fn<A4_A, > for C<2, (Box<A39_F, >, ), > where A4_A: Tuple, A39_F: T26_Fn<A4_A, >, A39_F : ?Sized,  {
}

impl<A23_Args, A39_F, A4_A, > T26_Fn<A23_Args, > for C<4, (Box<A39_F, >, Box<A4_A, >, ), > where A23_Args: Tuple, A39_F: T26_Fn<A23_Args, >, A4_A: T5_Allocator, A39_F : ?Sized,  {
}

impl<A4_A, A39_F, > T25_FnMut<A4_A, > for C<2, (Box<A39_F, >, ), > where A4_A: Tuple, A39_F: T26_Fn<A4_A, >, A39_F : ?Sized,  {
}

impl<A4_A, A39_F, > T25_FnMut<A4_A, > for C<3, (Box<A39_F, >, ), > where A4_A: Tuple, A39_F: T25_FnMut<A4_A, >, A39_F : ?Sized,  {
}

impl<A23_Args, A39_F, A4_A, > T25_FnMut<A23_Args, > for C<4, (Box<A39_F, >, Box<A4_A, >, ), > where A23_Args: Tuple, A39_F: T25_FnMut<A23_Args, >, A4_A: T5_Allocator, A39_F : ?Sized,  {
}

impl<A4_A, A39_F, > T24_FnOnce<A4_A, > for C<2, (Box<A39_F, >, ), > where A4_A: Tuple, A39_F: T26_Fn<A4_A, >, A39_F : ?Sized,  {
    type A17_Output = <A39_F as T24_FnOnce<A4_A, >>::A17_Output;
}

impl<A4_A, A39_F, > T24_FnOnce<A4_A, > for C<3, (Box<A39_F, >, ), > where A4_A: Tuple, A39_F: T25_FnMut<A4_A, >, A39_F : ?Sized,  {
    type A17_Output = <A39_F as T24_FnOnce<A4_A, >>::A17_Output;
}

impl<A23_Args, A39_F, A4_A, > T24_FnOnce<A23_Args, > for C<4, (Box<A39_F, >, Box<A4_A, >, ), > where A23_Args: Tuple, A39_F: T24_FnOnce<A23_Args, >, A4_A: T5_Allocator, A39_F : ?Sized,  {
    type A17_Output = <A39_F as T24_FnOnce<A23_Args, >>::A17_Output;
}

impl<A2_T, A36_I, const A35_N: usize, > T30_Index<A36_I, > for Arr<A2_T, A35_N, > where [A2_T]: T30_Index<A36_I, >,  {
    type A17_Output = <[A2_T] as T30_Index<A36_I, >>::A17_Output;
}

impl<A2_T, A36_I, > T30_Index<A36_I, > for [A2_T] where A36_I: T16_SliceIndex<[A2_T], >,  {
    type A17_Output = <A36_I as T16_SliceIndex<[A2_T], >>::A17_Output;
}

impl<A36_I, > T30_Index<A36_I, > for str where A36_I: T16_SliceIndex<str, >,  {
    type A17_Output = <A36_I as T16_SliceIndex<str, >>::A17_Output;
}

impl<A2_T, A36_I, A4_A, > T30_Index<A36_I, > for D6_Vec<A2_T, A4_A, > where A36_I: T16_SliceIndex<[A2_T], >, A4_A: T5_Allocator,  {
    type A17_Output = <A36_I as T16_SliceIndex<[A2_T], >>::A17_Output;
}

impl<A2_T, > T33_RangeBounds<A2_T, > for (Box<D3_Bound<A2_T, >, >, Box<D3_Bound<A2_T, >, >, ) where  {
}

impl<A2_T, > T33_RangeBounds<A2_T, > for (Box<D3_Bound<C<2, (Box<A2_T, >, ), >, >, >, Box<D3_Bound<C<2, (Box<A2_T, >, ), >, >, >, ) where A2_T : ?Sized,  {
}

impl<A2_T, > T16_SliceIndex<[A2_T], > for usize where  {
    type A17_Output = A2_T;
}

impl<A2_T, > T16_SliceIndex<[A2_T], > for (Box<D3_Bound<usize, >, >, Box<D3_Bound<usize, >, >, ) where  {
    type A17_Output = [A2_T];
}

impl T16_SliceIndex<str, > for (Box<D3_Bound<usize, >, >, Box<D3_Bound<usize, >, >, ) {
    type A17_Output = str;
}

impl<A4_A, > T5_Allocator for C<2, (Box<A4_A, >, ), > where A4_A: T5_Allocator, A4_A : ?Sized,  {
}

impl<A4_A, > T5_Allocator for C<3, (Box<A4_A, >, ), > where A4_A: T5_Allocator, A4_A : ?Sized,  {
}

impl T5_Allocator for D1_Global {
}

impl<A2_T, A4_A, > T5_Allocator for C<4, (Box<A2_T, >, Box<A4_A, >, ), > where A2_T: T5_Allocator, A4_A: T5_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A4_A, > T5_Allocator for C<5, (Box<A2_T, >, Box<A4_A, >, ), > where A2_T: T5_Allocator, A4_A: T5_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A4_A, > T5_Allocator for C<6, (Box<A2_T, >, Box<A4_A, >, ), > where A2_T: T5_Allocator, A4_A: T5_Allocator, A2_T : ?Sized,  {
}

impl T31_Integer for u8 {
}

impl T31_Integer for u32 {
}

impl T31_Integer for usize {
}

impl T31_Integer for i32 {
}

impl T31_Integer for int {
}

impl T31_Integer for nat {
}

impl T31_Integer for char {
}
