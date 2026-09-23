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



trait T17_ArrayAdditionalSpecFns<A4_T, > where Self: T15_View, Self: T15_View<A16_V = D14_Seq<A4_T, >>,  {
}

trait T18_SliceAdditionalSpecFns<A4_T, > where Self: T15_View, Self: T15_View<A16_V = D14_Seq<A4_T, >>,  {
}

trait T19_SliceIndex<A4_T, > where A4_T : ?Sized,  {
    type A20_Output : ?Sized;
}

trait T21_SliceIndexSpec<A4_T, > where Self: T19_SliceIndex<A4_T, >, A4_T : ?Sized,  {
}

trait T22_StringSliceAdditionalSpecFns {
}

trait T15_View {
    type A16_V : ;
}

trait T23_Clone where Self: Sized,  {
}

trait T24_Copy where Self: T23_Clone,  {
}

trait T25_Tuple {
}

trait T27_FnOnce<A26_Args, > where A26_Args: Tuple,  {
    type A20_Output : ;
}

trait T28_FnMut<A26_Args, > where Self: T27_FnOnce<A26_Args, >, A26_Args: Tuple,  {
}

trait T29_Fn<A26_Args, > where Self: T28_FnMut<A26_Args, >, A26_Args: Tuple,  {
}

trait T30_Deref {
    type A31_Target : ?Sized;
}

trait T32_Index<A2_Idx, > where A2_Idx : ?Sized,  {
    type A20_Output : ?Sized;
}

trait T33_Integer where Self: T24_Copy,  {
}

trait T8_Allocator {
}

trait T34_IndexSpec<A2_Idx, > where Self: T32_Index<A2_Idx, >, A2_Idx : ?Sized,  {
}

trait T35_RangeBounds<A4_T, > where A4_T : ?Sized,  {
}

trait T36_RangeBoundsSpec<A4_T, > where Self: T35_RangeBounds<A4_T, >, A4_T : ?Sized,  {
}

struct D1_Global(
);

struct D3_Range<A2_Idx, >(
    Box<A2_Idx, >,
    A2_Idx,
) where ;

struct D5_Bound<A4_T, >(
    Box<A4_T, >,
) where ;

struct D6_RangeFull(
);

struct D9_Vec<A4_T, A7_A, >(
    Box<A4_T, >,
    Box<A7_A, >,
) where A7_A: T8_Allocator, ;

struct D10_ISet<A7_A, >(
    Box<A7_A, >,
    C<0, (Box<(A7_A, ), >, Box<bool, >, ), >,
) where ;

struct D11_Provenance(
);

struct D12_PtrData<A4_T, >(
    Box<A4_T, >,
    <A4_T as std::ptr::Pointee>::Metadata,
) where A4_T : ?Sized, ;

struct D13_SeqInner<A7_A, >(
    Box<A7_A, >,
) where ;

struct D14_Seq<A7_A, >(
    Box<A7_A, >,
    D13_SeqInner<A7_A, >,
) where ;

impl<A4_T, const A37_N: usize, > T15_View for Arr<A4_T, A37_N, > where  {
    type A16_V = D14_Seq<A4_T, >;
}

impl<A4_T, const A37_N: usize, > T17_ArrayAdditionalSpecFns<A4_T, > for Arr<A4_T, A37_N, > where  {
}

impl<A4_T, > T15_View for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
    type A16_V = D12_PtrData<A4_T, >;
}

impl<A4_T, > T15_View for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
    type A16_V = D12_PtrData<A4_T, >;
}

impl<A4_T, > T15_View for [A4_T] where  {
    type A16_V = D14_Seq<A4_T, >;
}

impl<A4_T, > T18_SliceAdditionalSpecFns<A4_T, > for [A4_T] where  {
}

impl T15_View for str {
    type A16_V = D14_Seq<char, >;
}

impl T22_StringSliceAdditionalSpecFns for str {
}

impl T21_SliceIndexSpec<str, > for (Box<D5_Bound<usize, >, >, Box<D5_Bound<usize, >, >, ) {
}

impl T21_SliceIndexSpec<str, > for D3_Range<usize, > {
}

impl T21_SliceIndexSpec<str, > for D6_RangeFull {
}

impl<A38_I, > T34_IndexSpec<A38_I, > for str where A38_I: T21_SliceIndexSpec<str, >,  {
}

impl<A7_A, > T15_View for C<2, (Box<A7_A, >, ), > where A7_A: T15_View, A7_A : ?Sized,  {
    type A16_V = <A7_A as T15_View>::A16_V;
}

impl<A7_A, > T15_View for C<4, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T15_View, A7_A : ?Sized,  {
    type A16_V = <A7_A as T15_View>::A16_V;
}

impl<A7_A, > T15_View for C<5, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T15_View,  {
    type A16_V = <A7_A as T15_View>::A16_V;
}

impl<A7_A, > T15_View for C<6, (Box<A7_A, >, Box<D1_Global, >, ), > where A7_A: T15_View,  {
    type A16_V = <A7_A as T15_View>::A16_V;
}

impl<A4_T, A7_A, > T15_View for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator,  {
    type A16_V = D14_Seq<A4_T, >;
}

impl T15_View for () {
    type A16_V = ();
}

impl T15_View for bool {
    type A16_V = bool;
}

impl T15_View for u8 {
    type A16_V = u8;
}

impl T15_View for u32 {
    type A16_V = u32;
}

impl T15_View for usize {
    type A16_V = usize;
}

impl T15_View for i32 {
    type A16_V = i32;
}

impl T15_View for char {
    type A16_V = char;
}

impl<A39_A0, A40_A1, > T15_View for (Box<A39_A0, >, Box<A40_A1, >, ) where A39_A0: T15_View, A40_A1: T15_View,  {
    type A16_V = (Box<<A39_A0 as T15_View>::A16_V, >, Box<<A40_A1 as T15_View>::A16_V, >, );
}

impl<A4_T, > T36_RangeBoundsSpec<A4_T, > for D3_Range<A4_T, > where  {
}

impl<A4_T, > T36_RangeBoundsSpec<A4_T, > for D6_RangeFull where A4_T : ?Sized,  {
}

impl<A4_T, > T36_RangeBoundsSpec<A4_T, > for (Box<D5_Bound<A4_T, >, >, Box<D5_Bound<A4_T, >, >, ) where  {
}

impl<A4_T, > T36_RangeBoundsSpec<A4_T, > for (Box<D5_Bound<C<2, (Box<A4_T, >, ), >, >, >, Box<D5_Bound<C<2, (Box<A4_T, >, ), >, >, >, ) where A4_T : ?Sized,  {
}

impl<A4_T, > T36_RangeBoundsSpec<A4_T, > for D3_Range<C<2, (Box<A4_T, >, ), >, > where  {
}

impl<A4_T, > T21_SliceIndexSpec<[A4_T], > for usize where  {
}

impl<A4_T, > T21_SliceIndexSpec<[A4_T], > for D3_Range<usize, > where  {
}

impl<A4_T, > T21_SliceIndexSpec<[A4_T], > for D6_RangeFull where  {
}

impl<A4_T, A38_I, > T34_IndexSpec<A38_I, > for [A4_T] where A38_I: T19_SliceIndex<[A4_T], >,  {
}

impl<A4_T, A38_I, const A37_N: usize, > T34_IndexSpec<A38_I, > for Arr<A4_T, A37_N, > where [A4_T]: T32_Index<A38_I, >,  {
}

impl<A4_T, A38_I, A7_A, > T34_IndexSpec<A38_I, > for D9_Vec<A4_T, A7_A, > where A38_I: T19_SliceIndex<[A4_T], >, A7_A: T8_Allocator,  {
}

impl<A4_T, A7_A, > T23_Clone for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl<A4_T, A7_A, > T23_Clone for C<4, (Box<[A4_T], >, Box<A7_A, >, ), > where A4_T: T23_Clone, A7_A: T8_Allocator, A7_A: T23_Clone,  {
}

impl T23_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T23_Clone for usize {
}

impl T23_Clone for u8 {
}

impl T23_Clone for u32 {
}

impl T23_Clone for i32 {
}

impl T23_Clone for bool {
}

impl T23_Clone for char {
}

impl<A4_T, > T23_Clone for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T23_Clone for C<2, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl T23_Clone for D6_RangeFull {
}

impl<A2_Idx, > T23_Clone for D3_Range<A2_Idx, > where A2_Idx: T23_Clone,  {
}

impl<A4_T, > T23_Clone for D5_Bound<A4_T, > where A4_T: T23_Clone,  {
}

impl<A4_T, const A37_N: usize, > T23_Clone for Arr<A4_T, A37_N, > where A4_T: T23_Clone,  {
}

impl T23_Clone for D1_Global {
}

impl<A4_T, A7_A, > T23_Clone for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T23_Clone, A4_T : ?Sized,  {
}

impl<A4_T, A7_A, > T23_Clone for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A7_A: T23_Clone, A4_T : ?Sized,  {
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

impl T24_Copy for usize {
}

impl T24_Copy for u8 {
}

impl T24_Copy for u32 {
}

impl T24_Copy for i32 {
}

impl T24_Copy for bool {
}

impl T24_Copy for char {
}

impl<A4_T, > T24_Copy for C<10, (Box<C<1, (Box<A4_T, >, ), >, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T24_Copy for C<1, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl<A4_T, > T24_Copy for C<2, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
}

impl T24_Copy for D6_RangeFull {
}

impl<A4_T, > T24_Copy for D5_Bound<A4_T, > where A4_T: T24_Copy,  {
}

impl<A4_T, const A37_N: usize, > T24_Copy for Arr<A4_T, A37_N, > where A4_T: T24_Copy,  {
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

impl<A4_T, > T30_Deref for C<2, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
    type A31_Target = A4_T;
}

impl<A4_T, > T30_Deref for C<3, (Box<A4_T, >, ), > where A4_T : ?Sized,  {
    type A31_Target = A4_T;
}

impl<A4_T, A7_A, > T30_Deref for C<4, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A4_T : ?Sized,  {
    type A31_Target = A4_T;
}

impl<A4_T, A7_A, > T30_Deref for C<5, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A4_T : ?Sized,  {
    type A31_Target = A4_T;
}

impl<A4_T, A7_A, > T30_Deref for C<6, (Box<A4_T, >, Box<A7_A, >, ), > where A7_A: T8_Allocator, A4_T : ?Sized,  {
    type A31_Target = A4_T;
}

impl<A4_T, A7_A, > T30_Deref for D9_Vec<A4_T, A7_A, > where A7_A: T8_Allocator,  {
    type A31_Target = [A4_T];
}

impl<A7_A, A41_F, > T29_Fn<A7_A, > for C<2, (Box<A41_F, >, ), > where A7_A: Tuple, A41_F: T29_Fn<A7_A, >, A41_F : ?Sized,  {
}

impl<A26_Args, A41_F, A7_A, > T29_Fn<A26_Args, > for C<4, (Box<A41_F, >, Box<A7_A, >, ), > where A26_Args: Tuple, A41_F: T29_Fn<A26_Args, >, A7_A: T8_Allocator, A41_F : ?Sized,  {
}

impl<A7_A, A41_F, > T28_FnMut<A7_A, > for C<2, (Box<A41_F, >, ), > where A7_A: Tuple, A41_F: T29_Fn<A7_A, >, A41_F : ?Sized,  {
}

impl<A7_A, A41_F, > T28_FnMut<A7_A, > for C<3, (Box<A41_F, >, ), > where A7_A: Tuple, A41_F: T28_FnMut<A7_A, >, A41_F : ?Sized,  {
}

impl<A26_Args, A41_F, A7_A, > T28_FnMut<A26_Args, > for C<4, (Box<A41_F, >, Box<A7_A, >, ), > where A26_Args: Tuple, A41_F: T28_FnMut<A26_Args, >, A7_A: T8_Allocator, A41_F : ?Sized,  {
}

impl<A7_A, A41_F, > T27_FnOnce<A7_A, > for C<2, (Box<A41_F, >, ), > where A7_A: Tuple, A41_F: T29_Fn<A7_A, >, A41_F : ?Sized,  {
    type A20_Output = <A41_F as T27_FnOnce<A7_A, >>::A20_Output;
}

impl<A7_A, A41_F, > T27_FnOnce<A7_A, > for C<3, (Box<A41_F, >, ), > where A7_A: Tuple, A41_F: T28_FnMut<A7_A, >, A41_F : ?Sized,  {
    type A20_Output = <A41_F as T27_FnOnce<A7_A, >>::A20_Output;
}

impl<A26_Args, A41_F, A7_A, > T27_FnOnce<A26_Args, > for C<4, (Box<A41_F, >, Box<A7_A, >, ), > where A26_Args: Tuple, A41_F: T27_FnOnce<A26_Args, >, A7_A: T8_Allocator, A41_F : ?Sized,  {
    type A20_Output = <A41_F as T27_FnOnce<A26_Args, >>::A20_Output;
}

impl<A4_T, A38_I, const A37_N: usize, > T32_Index<A38_I, > for Arr<A4_T, A37_N, > where [A4_T]: T32_Index<A38_I, >,  {
    type A20_Output = <[A4_T] as T32_Index<A38_I, >>::A20_Output;
}

impl<A4_T, A38_I, > T32_Index<A38_I, > for [A4_T] where A38_I: T19_SliceIndex<[A4_T], >,  {
    type A20_Output = <A38_I as T19_SliceIndex<[A4_T], >>::A20_Output;
}

impl<A38_I, > T32_Index<A38_I, > for str where A38_I: T19_SliceIndex<str, >,  {
    type A20_Output = <A38_I as T19_SliceIndex<str, >>::A20_Output;
}

impl<A4_T, A38_I, A7_A, > T32_Index<A38_I, > for D9_Vec<A4_T, A7_A, > where A38_I: T19_SliceIndex<[A4_T], >, A7_A: T8_Allocator,  {
    type A20_Output = <A38_I as T19_SliceIndex<[A4_T], >>::A20_Output;
}

impl<A4_T, > T35_RangeBounds<A4_T, > for D6_RangeFull where A4_T : ?Sized,  {
}

impl<A4_T, > T35_RangeBounds<A4_T, > for D3_Range<A4_T, > where  {
}

impl<A4_T, > T35_RangeBounds<A4_T, > for D3_Range<C<2, (Box<A4_T, >, ), >, > where  {
}

impl<A4_T, > T35_RangeBounds<A4_T, > for (Box<D5_Bound<A4_T, >, >, Box<D5_Bound<A4_T, >, >, ) where  {
}

impl<A4_T, > T35_RangeBounds<A4_T, > for (Box<D5_Bound<C<2, (Box<A4_T, >, ), >, >, >, Box<D5_Bound<C<2, (Box<A4_T, >, ), >, >, >, ) where A4_T : ?Sized,  {
}

impl<A4_T, > T19_SliceIndex<[A4_T], > for D6_RangeFull where  {
    type A20_Output = [A4_T];
}

impl T19_SliceIndex<str, > for D6_RangeFull {
    type A20_Output = str;
}

impl<A4_T, > T19_SliceIndex<[A4_T], > for usize where  {
    type A20_Output = A4_T;
}

impl<A4_T, > T19_SliceIndex<[A4_T], > for D3_Range<usize, > where  {
    type A20_Output = [A4_T];
}

impl T19_SliceIndex<str, > for D3_Range<usize, > {
    type A20_Output = str;
}

impl<A4_T, > T19_SliceIndex<[A4_T], > for (Box<D5_Bound<usize, >, >, Box<D5_Bound<usize, >, >, ) where  {
    type A20_Output = [A4_T];
}

impl T19_SliceIndex<str, > for (Box<D5_Bound<usize, >, >, Box<D5_Bound<usize, >, >, ) {
    type A20_Output = str;
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

impl T33_Integer for u8 {
}

impl T33_Integer for u32 {
}

impl T33_Integer for usize {
}

impl T33_Integer for i32 {
}

impl T33_Integer for int {
}

impl T33_Integer for nat {
}

impl T33_Integer for char {
}
