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



trait T15_ArrayAdditionalSpecFns<A2_T, > where Self: T13_View, Self: T13_View<A14_V = D12_Seq<A2_T, >>,  {
}

trait T16_SliceAdditionalSpecFns<A2_T, > where Self: T13_View, Self: T13_View<A14_V = D12_Seq<A2_T, >>,  {
}

trait T13_View {
    type A14_V : ;
}

trait T17_Clone where Self: Sized,  {
}

trait T18_Copy where Self: T17_Clone,  {
}

trait T19_From<A2_T, > where Self: Sized,  {
}

trait T20_FromSpec<A2_T, > where Self: Sized, Self: T19_From<A2_T, >,  {
}

trait T21_Tuple {
}

trait T23_FnOnce<A22_Args, > where A22_Args: Tuple,  {
    type A24_Output : ;
}

trait T25_FnMut<A22_Args, > where Self: T23_FnOnce<A22_Args, >, A22_Args: Tuple,  {
}

trait T26_Fn<A22_Args, > where Self: T25_FnMut<A22_Args, >, A22_Args: Tuple,  {
}

trait T4_Allocator {
}

trait T6_ZeroablePrimitive where Self: Sized, Self: T18_Copy,  {
}

trait T27_ZeroablePrimitiveSpec where Self: Sized, Self: T18_Copy, Self: T6_ZeroablePrimitive,  {
}

struct D1_Global(
);

struct D5_Vec<A2_T, A3_A, >(
    Box<A2_T, >,
    Box<A3_A, >,
) where A3_A: T4_Allocator, ;

struct D7_NonZero<A2_T, >(
    Box<A2_T, >,
) where A2_T: T6_ZeroablePrimitive, ;

struct D8_ISet<A3_A, >(
    Box<A3_A, >,
    C<0, (Box<(A3_A, ), >, Box<bool, >, ), >,
) where ;

struct D9_Provenance(
);

struct D10_PtrData<A2_T, >(
    Box<A2_T, >,
    <A2_T as std::ptr::Pointee>::Metadata,
) where A2_T : ?Sized, ;

struct D11_SeqInner<A3_A, >(
    Box<A3_A, >,
) where ;

struct D12_Seq<A3_A, >(
    Box<A3_A, >,
    D11_SeqInner<A3_A, >,
) where ;

impl<A2_T, const A28_N: usize, > T13_View for Arr<A2_T, A28_N, > where  {
    type A14_V = D12_Seq<A2_T, >;
}

impl<A2_T, const A28_N: usize, > T15_ArrayAdditionalSpecFns<A2_T, > for Arr<A2_T, A28_N, > where  {
}

impl<A2_T, > T13_View for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
    type A14_V = D10_PtrData<A2_T, >;
}

impl<A2_T, > T13_View for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
    type A14_V = D10_PtrData<A2_T, >;
}

impl<A2_T, > T13_View for [A2_T] where  {
    type A14_V = D12_Seq<A2_T, >;
}

impl<A2_T, > T16_SliceAdditionalSpecFns<A2_T, > for [A2_T] where  {
}

impl<A3_A, > T13_View for C<2, (Box<A3_A, >, ), > where A3_A: T13_View, A3_A : ?Sized,  {
    type A14_V = <A3_A as T13_View>::A14_V;
}

impl<A3_A, > T13_View for C<4, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T13_View, A3_A : ?Sized,  {
    type A14_V = <A3_A as T13_View>::A14_V;
}

impl<A3_A, > T13_View for C<5, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T13_View,  {
    type A14_V = <A3_A as T13_View>::A14_V;
}

impl<A3_A, > T13_View for C<6, (Box<A3_A, >, Box<D1_Global, >, ), > where A3_A: T13_View,  {
    type A14_V = <A3_A as T13_View>::A14_V;
}

impl<A2_T, A3_A, > T13_View for D5_Vec<A2_T, A3_A, > where A3_A: T4_Allocator,  {
    type A14_V = D12_Seq<A2_T, >;
}

impl T13_View for () {
    type A14_V = ();
}

impl T13_View for bool {
    type A14_V = bool;
}

impl T13_View for u8 {
    type A14_V = u8;
}

impl T13_View for u16 {
    type A14_V = u16;
}

impl T13_View for u32 {
    type A14_V = u32;
}

impl T13_View for u64 {
    type A14_V = u64;
}

impl T13_View for u128 {
    type A14_V = u128;
}

impl T13_View for usize {
    type A14_V = usize;
}

impl T13_View for i8 {
    type A14_V = i8;
}

impl T13_View for i16 {
    type A14_V = i16;
}

impl T13_View for i32 {
    type A14_V = i32;
}

impl T13_View for i64 {
    type A14_V = i64;
}

impl T13_View for i128 {
    type A14_V = i128;
}

impl T13_View for isize {
    type A14_V = isize;
}

impl T20_FromSpec<u8, > for u16 {
}

impl T20_FromSpec<u8, > for u32 {
}

impl T20_FromSpec<u8, > for u64 {
}

impl T20_FromSpec<u8, > for usize {
}

impl T20_FromSpec<u8, > for u128 {
}

impl T20_FromSpec<u16, > for u32 {
}

impl T20_FromSpec<u16, > for u64 {
}

impl T20_FromSpec<u16, > for usize {
}

impl T20_FromSpec<u16, > for u128 {
}

impl T20_FromSpec<u32, > for u64 {
}

impl T20_FromSpec<u32, > for u128 {
}

impl T20_FromSpec<u64, > for u128 {
}

impl T20_FromSpec<i8, > for i16 {
}

impl T20_FromSpec<i8, > for i32 {
}

impl T20_FromSpec<i8, > for i64 {
}

impl T20_FromSpec<i8, > for isize {
}

impl T20_FromSpec<i8, > for i128 {
}

impl T20_FromSpec<i16, > for i32 {
}

impl T20_FromSpec<i16, > for i64 {
}

impl T20_FromSpec<i16, > for isize {
}

impl T20_FromSpec<i16, > for i128 {
}

impl T20_FromSpec<i32, > for i64 {
}

impl T20_FromSpec<i32, > for i128 {
}

impl T20_FromSpec<i64, > for i128 {
}

impl T27_ZeroablePrimitiveSpec for u8 {
}

impl T27_ZeroablePrimitiveSpec for u16 {
}

impl T27_ZeroablePrimitiveSpec for u32 {
}

impl T27_ZeroablePrimitiveSpec for u64 {
}

impl T27_ZeroablePrimitiveSpec for usize {
}

impl T27_ZeroablePrimitiveSpec for i8 {
}

impl T27_ZeroablePrimitiveSpec for i16 {
}

impl T27_ZeroablePrimitiveSpec for i32 {
}

impl T27_ZeroablePrimitiveSpec for i64 {
}

impl T27_ZeroablePrimitiveSpec for isize {
}

impl<A2_T, > T13_View for D7_NonZero<A2_T, > where A2_T: T6_ZeroablePrimitive,  {
    type A14_V = A2_T;
}

impl<A2_T, > T20_FromSpec<D7_NonZero<A2_T, >, > for A2_T where A2_T: T6_ZeroablePrimitive,  {
}

impl T6_ZeroablePrimitive for u8 {
}

impl T6_ZeroablePrimitive for u16 {
}

impl T6_ZeroablePrimitive for u32 {
}

impl T6_ZeroablePrimitive for u64 {
}

impl T6_ZeroablePrimitive for u128 {
}

impl T6_ZeroablePrimitive for usize {
}

impl T6_ZeroablePrimitive for i8 {
}

impl T6_ZeroablePrimitive for i16 {
}

impl T6_ZeroablePrimitive for i32 {
}

impl T6_ZeroablePrimitive for i64 {
}

impl T6_ZeroablePrimitive for i128 {
}

impl T6_ZeroablePrimitive for isize {
}

impl<A2_T, A3_A, > T17_Clone for C<4, (Box<A2_T, >, Box<A3_A, >, ), > where A2_T: T17_Clone, A3_A: T4_Allocator, A3_A: T17_Clone,  {
}

impl<A2_T, A3_A, > T17_Clone for C<4, (Box<[A2_T], >, Box<A3_A, >, ), > where A2_T: T17_Clone, A3_A: T4_Allocator, A3_A: T17_Clone,  {
}

impl<A2_T, > T17_Clone for D7_NonZero<A2_T, > where A2_T: T6_ZeroablePrimitive,  {
}

impl T17_Clone for usize {
}

impl T17_Clone for u8 {
}

impl T17_Clone for u16 {
}

impl T17_Clone for u32 {
}

impl T17_Clone for u64 {
}

impl T17_Clone for u128 {
}

impl T17_Clone for isize {
}

impl T17_Clone for i8 {
}

impl T17_Clone for i16 {
}

impl T17_Clone for i32 {
}

impl T17_Clone for i64 {
}

impl T17_Clone for i128 {
}

impl T17_Clone for bool {
}

impl<A2_T, > T17_Clone for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T17_Clone for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T17_Clone for C<2, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, const A28_N: usize, > T17_Clone for Arr<A2_T, A28_N, > where A2_T: T17_Clone,  {
}

impl T17_Clone for D1_Global {
}

impl<A2_T, A3_A, > T17_Clone for C<5, (Box<A2_T, >, Box<A3_A, >, ), > where A3_A: T4_Allocator, A3_A: T17_Clone, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T17_Clone for C<6, (Box<A2_T, >, Box<A3_A, >, ), > where A3_A: T4_Allocator, A3_A: T17_Clone, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T17_Clone for D5_Vec<A2_T, A3_A, > where A2_T: T17_Clone, A3_A: T4_Allocator, A3_A: T17_Clone,  {
}

impl<A3_A, > T17_Clone for C<7, (Box<A3_A, >, ), > where  {
}

impl<A3_A, > T17_Clone for C<8, (Box<A3_A, >, ), > where A3_A: T18_Copy,  {
}

impl T17_Clone for int {
}

impl T17_Clone for nat {
}

impl<A2_T, > T19_From<D7_NonZero<A2_T, >, > for A2_T where A2_T: T6_ZeroablePrimitive,  {
}

impl<A2_T, > T19_From<A2_T, > for A2_T where  {
}

impl<A2_T, > T19_From<A2_T, > for C<4, (Box<A2_T, >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, > T19_From<C<2, (Box<[A2_T], >, ), >, > for C<4, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, > T19_From<C<3, (Box<[A2_T], >, ), >, > for C<4, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, const A28_N: usize, > T19_From<Arr<A2_T, A28_N, >, > for C<4, (Box<[A2_T], >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, A3_A, > T19_From<D5_Vec<A2_T, A3_A, >, > for C<4, (Box<[A2_T], >, Box<A3_A, >, ), > where A3_A: T4_Allocator,  {
}

impl<A2_T, > T19_From<A2_T, > for C<6, (Box<A2_T, >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, const A28_N: usize, > T19_From<Arr<A2_T, A28_N, >, > for C<6, (Box<[A2_T], >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, > T19_From<C<2, (Box<[A2_T], >, ), >, > for C<6, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, > T19_From<C<3, (Box<[A2_T], >, ), >, > for C<6, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, A3_A, > T19_From<C<4, (Box<A2_T, >, Box<A3_A, >, ), >, > for C<6, (Box<A2_T, >, Box<A3_A, >, ), > where A3_A: T4_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T19_From<D5_Vec<A2_T, A3_A, >, > for C<6, (Box<[A2_T], >, Box<A3_A, >, ), > where A3_A: T4_Allocator, A3_A: T17_Clone,  {
}

impl<A2_T, > T19_From<A2_T, > for C<5, (Box<A2_T, >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, const A28_N: usize, > T19_From<Arr<A2_T, A28_N, >, > for C<5, (Box<[A2_T], >, Box<D1_Global, >, ), > where  {
}

impl<A2_T, > T19_From<C<2, (Box<[A2_T], >, ), >, > for C<5, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, > T19_From<C<3, (Box<[A2_T], >, ), >, > for C<5, (Box<[A2_T], >, Box<D1_Global, >, ), > where A2_T: T17_Clone,  {
}

impl<A2_T, A3_A, > T19_From<C<4, (Box<A2_T, >, Box<A3_A, >, ), >, > for C<5, (Box<A2_T, >, Box<A3_A, >, ), > where A3_A: T4_Allocator, A2_T : ?Sized,  {
}

impl<A2_T, A3_A, > T19_From<D5_Vec<A2_T, A3_A, >, > for C<5, (Box<[A2_T], >, Box<A3_A, >, ), > where A3_A: T4_Allocator,  {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<u16, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<u32, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<u64, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<u128, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<usize, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<u32, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<u64, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<u128, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<usize, > {
}

impl T19_From<D7_NonZero<u32, >, > for D7_NonZero<u64, > {
}

impl T19_From<D7_NonZero<u32, >, > for D7_NonZero<u128, > {
}

impl T19_From<D7_NonZero<u64, >, > for D7_NonZero<u128, > {
}

impl T19_From<D7_NonZero<i8, >, > for D7_NonZero<i16, > {
}

impl T19_From<D7_NonZero<i8, >, > for D7_NonZero<i32, > {
}

impl T19_From<D7_NonZero<i8, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<i8, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<i8, >, > for D7_NonZero<isize, > {
}

impl T19_From<D7_NonZero<i16, >, > for D7_NonZero<i32, > {
}

impl T19_From<D7_NonZero<i16, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<i16, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<i16, >, > for D7_NonZero<isize, > {
}

impl T19_From<D7_NonZero<i32, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<i32, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<i64, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<i16, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<i32, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<u8, >, > for D7_NonZero<isize, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<i32, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<u16, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<u32, >, > for D7_NonZero<i64, > {
}

impl T19_From<D7_NonZero<u32, >, > for D7_NonZero<i128, > {
}

impl T19_From<D7_NonZero<u64, >, > for D7_NonZero<i128, > {
}

impl T19_From<bool, > for usize {
}

impl T19_From<u8, > for usize {
}

impl T19_From<u16, > for usize {
}

impl T19_From<bool, > for u8 {
}

impl T19_From<bool, > for u16 {
}

impl T19_From<u8, > for u16 {
}

impl T19_From<bool, > for u32 {
}

impl T19_From<u8, > for u32 {
}

impl T19_From<u16, > for u32 {
}

impl T19_From<bool, > for u64 {
}

impl T19_From<u8, > for u64 {
}

impl T19_From<u16, > for u64 {
}

impl T19_From<u32, > for u64 {
}

impl T19_From<bool, > for u128 {
}

impl T19_From<u8, > for u128 {
}

impl T19_From<u16, > for u128 {
}

impl T19_From<u32, > for u128 {
}

impl T19_From<u64, > for u128 {
}

impl T19_From<bool, > for i8 {
}

impl T19_From<bool, > for i16 {
}

impl T19_From<i8, > for i16 {
}

impl T19_From<u8, > for i16 {
}

impl T19_From<bool, > for i32 {
}

impl T19_From<i8, > for i32 {
}

impl T19_From<i16, > for i32 {
}

impl T19_From<u8, > for i32 {
}

impl T19_From<u16, > for i32 {
}

impl T19_From<bool, > for i64 {
}

impl T19_From<i8, > for i64 {
}

impl T19_From<i16, > for i64 {
}

impl T19_From<i32, > for i64 {
}

impl T19_From<u8, > for i64 {
}

impl T19_From<u16, > for i64 {
}

impl T19_From<u32, > for i64 {
}

impl T19_From<bool, > for i128 {
}

impl T19_From<i8, > for i128 {
}

impl T19_From<i16, > for i128 {
}

impl T19_From<i32, > for i128 {
}

impl T19_From<i64, > for i128 {
}

impl T19_From<u8, > for i128 {
}

impl T19_From<u16, > for i128 {
}

impl T19_From<u32, > for i128 {
}

impl T19_From<u64, > for i128 {
}

impl T19_From<bool, > for isize {
}

impl T19_From<i8, > for isize {
}

impl T19_From<u8, > for isize {
}

impl T19_From<i16, > for isize {
}

impl<A2_T, > T19_From<C<2, (Box<[A2_T], >, ), >, > for D5_Vec<A2_T, D1_Global, > where A2_T: T17_Clone,  {
}

impl<A2_T, > T19_From<C<3, (Box<[A2_T], >, ), >, > for D5_Vec<A2_T, D1_Global, > where A2_T: T17_Clone,  {
}

impl<A2_T, const A28_N: usize, > T19_From<C<2, (Box<Arr<A2_T, A28_N, >, >, ), >, > for D5_Vec<A2_T, D1_Global, > where A2_T: T17_Clone,  {
}

impl<A2_T, const A28_N: usize, > T19_From<C<3, (Box<Arr<A2_T, A28_N, >, >, ), >, > for D5_Vec<A2_T, D1_Global, > where A2_T: T17_Clone,  {
}

impl<A2_T, const A28_N: usize, > T19_From<Arr<A2_T, A28_N, >, > for D5_Vec<A2_T, D1_Global, > where  {
}

impl<A2_T, A3_A, > T19_From<C<4, (Box<[A2_T], >, Box<A3_A, >, ), >, > for D5_Vec<A2_T, A3_A, > where A3_A: T4_Allocator,  {
}

impl<A2_T, > T18_Copy for D7_NonZero<A2_T, > where A2_T: T6_ZeroablePrimitive,  {
}

impl T18_Copy for usize {
}

impl T18_Copy for u8 {
}

impl T18_Copy for u16 {
}

impl T18_Copy for u32 {
}

impl T18_Copy for u64 {
}

impl T18_Copy for u128 {
}

impl T18_Copy for isize {
}

impl T18_Copy for i8 {
}

impl T18_Copy for i16 {
}

impl T18_Copy for i32 {
}

impl T18_Copy for i64 {
}

impl T18_Copy for i128 {
}

impl T18_Copy for bool {
}

impl<A2_T, > T18_Copy for C<10, (Box<C<1, (Box<A2_T, >, ), >, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T18_Copy for C<1, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, > T18_Copy for C<2, (Box<A2_T, >, ), > where A2_T : ?Sized,  {
}

impl<A2_T, const A28_N: usize, > T18_Copy for Arr<A2_T, A28_N, > where A2_T: T18_Copy,  {
}

impl T18_Copy for D1_Global {
}

impl<A3_A, > T18_Copy for C<7, (Box<A3_A, >, ), > where  {
}

impl<A3_A, > T18_Copy for C<8, (Box<A3_A, >, ), > where A3_A: T18_Copy,  {
}

impl T18_Copy for int {
}

impl T18_Copy for nat {
}

impl<A3_A, A29_F, > T26_Fn<A3_A, > for C<2, (Box<A29_F, >, ), > where A3_A: Tuple, A29_F: T26_Fn<A3_A, >, A29_F : ?Sized,  {
}

impl<A22_Args, A29_F, A3_A, > T26_Fn<A22_Args, > for C<4, (Box<A29_F, >, Box<A3_A, >, ), > where A22_Args: Tuple, A29_F: T26_Fn<A22_Args, >, A3_A: T4_Allocator, A29_F : ?Sized,  {
}

impl<A3_A, A29_F, > T25_FnMut<A3_A, > for C<2, (Box<A29_F, >, ), > where A3_A: Tuple, A29_F: T26_Fn<A3_A, >, A29_F : ?Sized,  {
}

impl<A3_A, A29_F, > T25_FnMut<A3_A, > for C<3, (Box<A29_F, >, ), > where A3_A: Tuple, A29_F: T25_FnMut<A3_A, >, A29_F : ?Sized,  {
}

impl<A22_Args, A29_F, A3_A, > T25_FnMut<A22_Args, > for C<4, (Box<A29_F, >, Box<A3_A, >, ), > where A22_Args: Tuple, A29_F: T25_FnMut<A22_Args, >, A3_A: T4_Allocator, A29_F : ?Sized,  {
}

impl<A3_A, A29_F, > T23_FnOnce<A3_A, > for C<2, (Box<A29_F, >, ), > where A3_A: Tuple, A29_F: T26_Fn<A3_A, >, A29_F : ?Sized,  {
    type A24_Output = <A29_F as T23_FnOnce<A3_A, >>::A24_Output;
}

impl<A3_A, A29_F, > T23_FnOnce<A3_A, > for C<3, (Box<A29_F, >, ), > where A3_A: Tuple, A29_F: T25_FnMut<A3_A, >, A29_F : ?Sized,  {
    type A24_Output = <A29_F as T23_FnOnce<A3_A, >>::A24_Output;
}

impl<A22_Args, A29_F, A3_A, > T23_FnOnce<A22_Args, > for C<4, (Box<A29_F, >, Box<A3_A, >, ), > where A22_Args: Tuple, A29_F: T23_FnOnce<A22_Args, >, A3_A: T4_Allocator, A29_F : ?Sized,  {
    type A24_Output = <A29_F as T23_FnOnce<A22_Args, >>::A24_Output;
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
