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



trait T20_ArrayAdditionalSpecFns<A5_T, > where Self: T18_View, Self: T18_View<A19_V = D15_Seq<A5_T, >>,  {
}

trait T21_SliceAdditionalSpecFns<A5_T, > where Self: T18_View, Self: T18_View<A19_V = D15_Seq<A5_T, >>,  {
}

trait T18_View {
    type A19_V : ;
}

trait T3_ToOwned {
    type A22_Owned : T23_Borrow<Self, >;
}

trait T24_Clone where Self: Sized,  {
}

trait T25_Copy where Self: T24_Clone,  {
}

trait T26_From<A5_T, > where Self: Sized,  {
}

trait T27_FromSpec<A5_T, > where Self: Sized, Self: T26_From<A5_T, >,  {
}

trait T28_Tuple {
}

trait T30_FnOnce<A29_Args, > where A29_Args: Tuple,  {
    type A31_Output : ;
}

trait T32_FnMut<A29_Args, > where Self: T30_FnOnce<A29_Args, >, A29_Args: Tuple,  {
}

trait T33_Fn<A29_Args, > where Self: T32_FnMut<A29_Args, >, A29_Args: Tuple,  {
}

trait T7_Allocator {
}

trait T23_Borrow<A34_Borrowed, > where A34_Borrowed : ?Sized,  {
}

trait T9_ZeroablePrimitive where Self: Sized, Self: T25_Copy,  {
}

trait T35_ZeroablePrimitiveSpec where Self: Sized, Self: T25_Copy, Self: T9_ZeroablePrimitive,  {
}

trait T36_CowObservation<A5_T, > where  {
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

struct D10_NonZero<A5_T, >(
    Box<A5_T, >,
) where A5_T: T9_ZeroablePrimitive, ;

struct D11_ISet<A6_A, >(
    Box<A6_A, >,
    C<0, (Box<(A6_A, ), >, Box<bool, >, ), >,
) where ;

struct D12_Provenance(
);

struct D13_PtrData<A5_T, >(
    Box<A5_T, >,
    <A5_T as std::ptr::Pointee>::Metadata,
) where A5_T : ?Sized, ;

struct D14_SeqInner<A6_A, >(
    Box<A6_A, >,
) where ;

struct D15_Seq<A6_A, >(
    Box<A6_A, >,
    D14_SeqInner<A6_A, >,
) where ;

struct D16_String(
);

struct D17_CowContents<A5_T, >(
    Box<A5_T, >,
) where ;

impl<A5_T, const A37_N: usize, > T18_View for Arr<A5_T, A37_N, > where  {
    type A19_V = D15_Seq<A5_T, >;
}

impl<A5_T, const A37_N: usize, > T20_ArrayAdditionalSpecFns<A5_T, > for Arr<A5_T, A37_N, > where  {
}

impl<A5_T, > T18_View for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A19_V = D13_PtrData<A5_T, >;
}

impl<A5_T, > T18_View for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
    type A19_V = D13_PtrData<A5_T, >;
}

impl<A5_T, > T18_View for [A5_T] where  {
    type A19_V = D15_Seq<A5_T, >;
}

impl<A5_T, > T21_SliceAdditionalSpecFns<A5_T, > for [A5_T] where  {
}

impl T18_View for str {
    type A19_V = D15_Seq<char, >;
}

impl T18_View for D16_String {
    type A19_V = D15_Seq<char, >;
}

impl<A6_A, > T18_View for C<2, (Box<A6_A, >, ), > where A6_A: T18_View, A6_A : ?Sized,  {
    type A19_V = <A6_A as T18_View>::A19_V;
}

impl<A6_A, > T18_View for C<4, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T18_View, A6_A : ?Sized,  {
    type A19_V = <A6_A as T18_View>::A19_V;
}

impl<A6_A, > T18_View for C<5, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T18_View,  {
    type A19_V = <A6_A as T18_View>::A19_V;
}

impl<A6_A, > T18_View for C<6, (Box<A6_A, >, Box<D1_Global, >, ), > where A6_A: T18_View,  {
    type A19_V = <A6_A as T18_View>::A19_V;
}

impl<A5_T, A6_A, > T18_View for D8_Vec<A5_T, A6_A, > where A6_A: T7_Allocator,  {
    type A19_V = D15_Seq<A5_T, >;
}

impl T18_View for () {
    type A19_V = ();
}

impl T18_View for bool {
    type A19_V = bool;
}

impl T18_View for u8 {
    type A19_V = u8;
}

impl T18_View for u16 {
    type A19_V = u16;
}

impl T18_View for u32 {
    type A19_V = u32;
}

impl T18_View for u64 {
    type A19_V = u64;
}

impl T18_View for u128 {
    type A19_V = u128;
}

impl T18_View for usize {
    type A19_V = usize;
}

impl T18_View for i8 {
    type A19_V = i8;
}

impl T18_View for i16 {
    type A19_V = i16;
}

impl T18_View for i32 {
    type A19_V = i32;
}

impl T18_View for i64 {
    type A19_V = i64;
}

impl T18_View for i128 {
    type A19_V = i128;
}

impl T18_View for isize {
    type A19_V = isize;
}

impl T18_View for char {
    type A19_V = char;
}

impl<A38_A0, A39_A1, > T18_View for (Box<A38_A0, >, Box<A39_A1, >, ) where A38_A0: T18_View, A39_A1: T18_View,  {
    type A19_V = (Box<<A38_A0 as T18_View>::A19_V, >, Box<<A39_A1 as T18_View>::A19_V, >, );
}

impl<A5_T, > T18_View for D4_Cow<A5_T, > where A5_T: T18_View, A5_T: T24_Clone,  {
    type A19_V = <A5_T as T18_View>::A19_V;
}

impl T18_View for D4_Cow<str, > {
    type A19_V = D15_Seq<char, >;
}

impl<A5_T, > T18_View for D4_Cow<[A5_T], > where A5_T: T18_View, A5_T: T24_Clone,  {
    type A19_V = D15_Seq<A5_T, >;
}

impl T27_FromSpec<u8, > for u16 {
}

impl T27_FromSpec<u8, > for u32 {
}

impl T27_FromSpec<u8, > for u64 {
}

impl T27_FromSpec<u8, > for usize {
}

impl T27_FromSpec<u8, > for u128 {
}

impl T27_FromSpec<u16, > for u32 {
}

impl T27_FromSpec<u16, > for u64 {
}

impl T27_FromSpec<u16, > for usize {
}

impl T27_FromSpec<u16, > for u128 {
}

impl T27_FromSpec<u32, > for u64 {
}

impl T27_FromSpec<u32, > for u128 {
}

impl T27_FromSpec<u64, > for u128 {
}

impl T27_FromSpec<i8, > for i16 {
}

impl T27_FromSpec<i8, > for i32 {
}

impl T27_FromSpec<i8, > for i64 {
}

impl T27_FromSpec<i8, > for isize {
}

impl T27_FromSpec<i8, > for i128 {
}

impl T27_FromSpec<i16, > for i32 {
}

impl T27_FromSpec<i16, > for i64 {
}

impl T27_FromSpec<i16, > for isize {
}

impl T27_FromSpec<i16, > for i128 {
}

impl T27_FromSpec<i32, > for i64 {
}

impl T27_FromSpec<i32, > for i128 {
}

impl T27_FromSpec<i64, > for i128 {
}

impl T35_ZeroablePrimitiveSpec for char {
}

impl T35_ZeroablePrimitiveSpec for u8 {
}

impl T35_ZeroablePrimitiveSpec for u16 {
}

impl T35_ZeroablePrimitiveSpec for u32 {
}

impl T35_ZeroablePrimitiveSpec for u64 {
}

impl T35_ZeroablePrimitiveSpec for usize {
}

impl T35_ZeroablePrimitiveSpec for i8 {
}

impl T35_ZeroablePrimitiveSpec for i16 {
}

impl T35_ZeroablePrimitiveSpec for i32 {
}

impl T35_ZeroablePrimitiveSpec for i64 {
}

impl T35_ZeroablePrimitiveSpec for isize {
}

impl<A5_T, > T18_View for D10_NonZero<A5_T, > where A5_T: T9_ZeroablePrimitive,  {
    type A19_V = A5_T;
}

impl<A5_T, > T27_FromSpec<D10_NonZero<A5_T, >, > for A5_T where A5_T: T9_ZeroablePrimitive,  {
}

impl T9_ZeroablePrimitive for u8 {
}

impl T9_ZeroablePrimitive for u16 {
}

impl T9_ZeroablePrimitive for u32 {
}

impl T9_ZeroablePrimitive for u64 {
}

impl T9_ZeroablePrimitive for u128 {
}

impl T9_ZeroablePrimitive for usize {
}

impl T9_ZeroablePrimitive for i8 {
}

impl T9_ZeroablePrimitive for i16 {
}

impl T9_ZeroablePrimitive for i32 {
}

impl T9_ZeroablePrimitive for i64 {
}

impl T9_ZeroablePrimitive for i128 {
}

impl T9_ZeroablePrimitive for isize {
}

impl T9_ZeroablePrimitive for char {
}

impl<A5_T, > T23_Borrow<A5_T, > for A5_T where A5_T : ?Sized,  {
}

impl<A5_T, > T23_Borrow<A5_T, > for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T23_Borrow<A5_T, > for C<3, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A37_N: usize, > T23_Borrow<[A5_T], > for Arr<A5_T, A37_N, > where  {
}

impl<A2_B, > T23_Borrow<A2_B, > for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A6_A, > T23_Borrow<A5_T, > for C<4, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T23_Borrow<A5_T, > for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T23_Borrow<[A5_T], > for D8_Vec<A5_T, A6_A, > where A6_A: T7_Allocator,  {
}

impl T23_Borrow<str, > for D16_String {
}

impl<A5_T, A6_A, > T23_Borrow<A5_T, > for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T24_Clone for C<4, (Box<A5_T, >, Box<A6_A, >, ), > where A5_T: T24_Clone, A6_A: T7_Allocator, A6_A: T24_Clone,  {
}

impl<A5_T, A6_A, > T24_Clone for C<4, (Box<[A5_T], >, Box<A6_A, >, ), > where A5_T: T24_Clone, A6_A: T7_Allocator, A6_A: T24_Clone,  {
}

impl T24_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T24_Clone for D10_NonZero<A5_T, > where A5_T: T9_ZeroablePrimitive,  {
}

impl T24_Clone for usize {
}

impl T24_Clone for u8 {
}

impl T24_Clone for u16 {
}

impl T24_Clone for u32 {
}

impl T24_Clone for u64 {
}

impl T24_Clone for u128 {
}

impl T24_Clone for isize {
}

impl T24_Clone for i8 {
}

impl T24_Clone for i16 {
}

impl T24_Clone for i32 {
}

impl T24_Clone for i64 {
}

impl T24_Clone for i128 {
}

impl T24_Clone for bool {
}

impl T24_Clone for char {
}

impl<A5_T, > T24_Clone for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T24_Clone for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T24_Clone for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A37_N: usize, > T24_Clone for Arr<A5_T, A37_N, > where A5_T: T24_Clone,  {
}

impl T24_Clone for D1_Global {
}

impl<A2_B, > T24_Clone for D4_Cow<A2_B, > where A2_B: T3_ToOwned, A2_B : ?Sized,  {
}

impl<A5_T, A6_A, > T24_Clone for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A: T24_Clone, A5_T : ?Sized,  {
}

impl T24_Clone for D16_String {
}

impl<A5_T, A6_A, > T24_Clone for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A: T24_Clone, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T24_Clone for D8_Vec<A5_T, A6_A, > where A5_T: T24_Clone, A6_A: T7_Allocator, A6_A: T24_Clone,  {
}

impl<A6_A, > T24_Clone for C<7, (Box<A6_A, >, ), > where  {
}

impl<A6_A, > T24_Clone for C<8, (Box<A6_A, >, ), > where A6_A: T25_Copy,  {
}

impl T24_Clone for int {
}

impl T24_Clone for nat {
}

impl<A5_T, > T26_From<D10_NonZero<A5_T, >, > for A5_T where A5_T: T9_ZeroablePrimitive,  {
}

impl<A5_T, > T26_From<A5_T, > for A5_T where  {
}

impl<A5_T, > T26_From<A5_T, > for C<4, (Box<A5_T, >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, > T26_From<C<2, (Box<[A5_T], >, ), >, > for C<4, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<C<3, (Box<[A5_T], >, ), >, > for C<4, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<D4_Cow<[A5_T], >, > for C<4, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl T26_From<C<2, (Box<str, >, ), >, > for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<C<3, (Box<str, >, ), >, > for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<D4_Cow<str, >, > for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A6_A, > T26_From<C<4, (Box<str, >, Box<A6_A, >, ), >, > for C<4, (Box<[u8], >, Box<A6_A, >, ), > where A6_A: T7_Allocator,  {
}

impl<A5_T, const A37_N: usize, > T26_From<Arr<A5_T, A37_N, >, > for C<4, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl T26_From<D16_String, > for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, A6_A, > T26_From<D8_Vec<A5_T, A6_A, >, > for C<4, (Box<[A5_T], >, Box<A6_A, >, ), > where A6_A: T7_Allocator,  {
}

impl<A5_T, > T26_From<A5_T, > for C<6, (Box<A5_T, >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, const A37_N: usize, > T26_From<Arr<A5_T, A37_N, >, > for C<6, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, > T26_From<C<2, (Box<[A5_T], >, ), >, > for C<6, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<C<3, (Box<[A5_T], >, ), >, > for C<6, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl T26_From<C<2, (Box<str, >, ), >, > for C<6, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<C<3, (Box<str, >, ), >, > for C<6, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<D16_String, > for C<6, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, A6_A, > T26_From<C<4, (Box<A5_T, >, Box<A6_A, >, ), >, > for C<6, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T26_From<D8_Vec<A5_T, A6_A, >, > for C<6, (Box<[A5_T], >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A6_A: T24_Clone,  {
}

impl<A2_B, > T26_From<D4_Cow<A2_B, >, > for C<6, (Box<A2_B, >, Box<D1_Global, >, ), > where A2_B: T3_ToOwned, C<6, (Box<A2_B, >, Box<D1_Global, >, ), >: T26_From<C<2, (Box<A2_B, >, ), >, >, C<6, (Box<A2_B, >, Box<D1_Global, >, ), >: T26_From<<A2_B as T3_ToOwned>::A22_Owned, >, A2_B : ?Sized,  {
}

impl T26_From<C<6, (Box<str, >, Box<D1_Global, >, ), >, > for C<6, (Box<[u8], >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T26_From<A5_T, > for C<5, (Box<A5_T, >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, const A37_N: usize, > T26_From<Arr<A5_T, A37_N, >, > for C<5, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, > T26_From<C<2, (Box<[A5_T], >, ), >, > for C<5, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<C<3, (Box<[A5_T], >, ), >, > for C<5, (Box<[A5_T], >, Box<D1_Global, >, ), > where A5_T: T24_Clone,  {
}

impl T26_From<C<2, (Box<str, >, ), >, > for C<5, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<C<3, (Box<str, >, ), >, > for C<5, (Box<str, >, Box<D1_Global, >, ), > {
}

impl T26_From<D16_String, > for C<5, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, A6_A, > T26_From<C<4, (Box<A5_T, >, Box<A6_A, >, ), >, > for C<5, (Box<A5_T, >, Box<A6_A, >, ), > where A6_A: T7_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A6_A, > T26_From<D8_Vec<A5_T, A6_A, >, > for C<5, (Box<[A5_T], >, Box<A6_A, >, ), > where A6_A: T7_Allocator,  {
}

impl<A2_B, > T26_From<D4_Cow<A2_B, >, > for C<5, (Box<A2_B, >, Box<D1_Global, >, ), > where A2_B: T3_ToOwned, C<5, (Box<A2_B, >, Box<D1_Global, >, ), >: T26_From<C<2, (Box<A2_B, >, ), >, >, C<5, (Box<A2_B, >, Box<D1_Global, >, ), >: T26_From<<A2_B as T3_ToOwned>::A22_Owned, >, A2_B : ?Sized,  {
}

impl T26_From<C<5, (Box<str, >, Box<D1_Global, >, ), >, > for C<5, (Box<[u8], >, Box<D1_Global, >, ), > {
}

impl T26_From<C<2, (Box<str, >, ), >, > for D4_Cow<str, > {
}

impl T26_From<D16_String, > for D4_Cow<str, > {
}

impl T26_From<C<2, (Box<D16_String, >, ), >, > for D4_Cow<str, > {
}

impl<A5_T, > T26_From<C<2, (Box<[A5_T], >, ), >, > for D4_Cow<[A5_T], > where A5_T: T24_Clone,  {
}

impl<A5_T, const A37_N: usize, > T26_From<C<2, (Box<Arr<A5_T, A37_N, >, >, ), >, > for D4_Cow<[A5_T], > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<D8_Vec<A5_T, D1_Global, >, > for D4_Cow<[A5_T], > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<C<2, (Box<D8_Vec<A5_T, D1_Global, >, >, ), >, > for D4_Cow<[A5_T], > where A5_T: T24_Clone,  {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<u16, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<u32, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<u64, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<u128, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<usize, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<u32, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<u64, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<u128, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<usize, > {
}

impl T26_From<D10_NonZero<u32, >, > for D10_NonZero<u64, > {
}

impl T26_From<D10_NonZero<u32, >, > for D10_NonZero<u128, > {
}

impl T26_From<D10_NonZero<u64, >, > for D10_NonZero<u128, > {
}

impl T26_From<D10_NonZero<i8, >, > for D10_NonZero<i16, > {
}

impl T26_From<D10_NonZero<i8, >, > for D10_NonZero<i32, > {
}

impl T26_From<D10_NonZero<i8, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<i8, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<i8, >, > for D10_NonZero<isize, > {
}

impl T26_From<D10_NonZero<i16, >, > for D10_NonZero<i32, > {
}

impl T26_From<D10_NonZero<i16, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<i16, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<i16, >, > for D10_NonZero<isize, > {
}

impl T26_From<D10_NonZero<i32, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<i32, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<i64, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<i16, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<i32, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<u8, >, > for D10_NonZero<isize, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<i32, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<u16, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<u32, >, > for D10_NonZero<i64, > {
}

impl T26_From<D10_NonZero<u32, >, > for D10_NonZero<i128, > {
}

impl T26_From<D10_NonZero<u64, >, > for D10_NonZero<i128, > {
}

impl T26_From<bool, > for usize {
}

impl T26_From<u8, > for usize {
}

impl T26_From<u16, > for usize {
}

impl<A5_T, > T26_From<(Box<A5_T, >, Box<A5_T, >, ), > for Arr<A5_T, 2, > where  {
}

impl T26_From<bool, > for u8 {
}

impl T26_From<bool, > for u16 {
}

impl T26_From<u8, > for u16 {
}

impl T26_From<bool, > for u32 {
}

impl T26_From<u8, > for u32 {
}

impl T26_From<u16, > for u32 {
}

impl T26_From<char, > for u32 {
}

impl T26_From<bool, > for u64 {
}

impl T26_From<u8, > for u64 {
}

impl T26_From<u16, > for u64 {
}

impl T26_From<u32, > for u64 {
}

impl T26_From<char, > for u64 {
}

impl T26_From<bool, > for u128 {
}

impl T26_From<u8, > for u128 {
}

impl T26_From<u16, > for u128 {
}

impl T26_From<u32, > for u128 {
}

impl T26_From<u64, > for u128 {
}

impl T26_From<char, > for u128 {
}

impl T26_From<bool, > for i8 {
}

impl T26_From<bool, > for i16 {
}

impl T26_From<i8, > for i16 {
}

impl T26_From<u8, > for i16 {
}

impl T26_From<bool, > for i32 {
}

impl T26_From<i8, > for i32 {
}

impl T26_From<i16, > for i32 {
}

impl T26_From<u8, > for i32 {
}

impl T26_From<u16, > for i32 {
}

impl T26_From<bool, > for i64 {
}

impl T26_From<i8, > for i64 {
}

impl T26_From<i16, > for i64 {
}

impl T26_From<i32, > for i64 {
}

impl T26_From<u8, > for i64 {
}

impl T26_From<u16, > for i64 {
}

impl T26_From<u32, > for i64 {
}

impl T26_From<bool, > for i128 {
}

impl T26_From<i8, > for i128 {
}

impl T26_From<i16, > for i128 {
}

impl T26_From<i32, > for i128 {
}

impl T26_From<i64, > for i128 {
}

impl T26_From<u8, > for i128 {
}

impl T26_From<u16, > for i128 {
}

impl T26_From<u32, > for i128 {
}

impl T26_From<u64, > for i128 {
}

impl T26_From<bool, > for isize {
}

impl T26_From<i8, > for isize {
}

impl T26_From<u8, > for isize {
}

impl T26_From<i16, > for isize {
}

impl T26_From<u8, > for char {
}

impl<A5_T, > T26_From<Arr<A5_T, 2, >, > for (Box<A5_T, >, Box<A5_T, >, ) where  {
}

impl T26_From<D16_String, > for D8_Vec<u8, D1_Global, > {
}

impl<A5_T, > T26_From<C<2, (Box<[A5_T], >, ), >, > for D8_Vec<A5_T, D1_Global, > where A5_T: T24_Clone,  {
}

impl<A5_T, > T26_From<C<3, (Box<[A5_T], >, ), >, > for D8_Vec<A5_T, D1_Global, > where A5_T: T24_Clone,  {
}

impl<A5_T, const A37_N: usize, > T26_From<C<2, (Box<Arr<A5_T, A37_N, >, >, ), >, > for D8_Vec<A5_T, D1_Global, > where A5_T: T24_Clone,  {
}

impl<A5_T, const A37_N: usize, > T26_From<C<3, (Box<Arr<A5_T, A37_N, >, >, ), >, > for D8_Vec<A5_T, D1_Global, > where A5_T: T24_Clone,  {
}

impl<A5_T, const A37_N: usize, > T26_From<Arr<A5_T, A37_N, >, > for D8_Vec<A5_T, D1_Global, > where  {
}

impl<A5_T, > T26_From<D4_Cow<[A5_T], >, > for D8_Vec<A5_T, D1_Global, > where [A5_T]: T3_ToOwned<A22_Owned = D8_Vec<A5_T, D1_Global, >>, [A5_T]: T3_ToOwned,  {
}

impl<A5_T, A6_A, > T26_From<C<4, (Box<[A5_T], >, Box<A6_A, >, ), >, > for D8_Vec<A5_T, A6_A, > where A6_A: T7_Allocator,  {
}

impl T26_From<C<2, (Box<str, >, ), >, > for D8_Vec<u8, D1_Global, > {
}

impl T26_From<C<2, (Box<str, >, ), >, > for D16_String {
}

impl T26_From<C<3, (Box<str, >, ), >, > for D16_String {
}

impl T26_From<C<2, (Box<D16_String, >, ), >, > for D16_String {
}

impl T26_From<C<4, (Box<str, >, Box<D1_Global, >, ), >, > for D16_String {
}

impl T26_From<D4_Cow<str, >, > for D16_String {
}

impl T26_From<char, > for D16_String {
}

impl<A5_T, > T25_Copy for D10_NonZero<A5_T, > where A5_T: T9_ZeroablePrimitive,  {
}

impl T25_Copy for usize {
}

impl T25_Copy for u8 {
}

impl T25_Copy for u16 {
}

impl T25_Copy for u32 {
}

impl T25_Copy for u64 {
}

impl T25_Copy for u128 {
}

impl T25_Copy for isize {
}

impl T25_Copy for i8 {
}

impl T25_Copy for i16 {
}

impl T25_Copy for i32 {
}

impl T25_Copy for i64 {
}

impl T25_Copy for i128 {
}

impl T25_Copy for bool {
}

impl T25_Copy for char {
}

impl<A5_T, > T25_Copy for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T25_Copy for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T25_Copy for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, const A37_N: usize, > T25_Copy for Arr<A5_T, A37_N, > where A5_T: T25_Copy,  {
}

impl T25_Copy for D1_Global {
}

impl<A6_A, > T25_Copy for C<7, (Box<A6_A, >, ), > where  {
}

impl<A6_A, > T25_Copy for C<8, (Box<A6_A, >, ), > where A6_A: T25_Copy,  {
}

impl T25_Copy for int {
}

impl T25_Copy for nat {
}

impl<A6_A, A40_F, > T33_Fn<A6_A, > for C<2, (Box<A40_F, >, ), > where A6_A: Tuple, A40_F: T33_Fn<A6_A, >, A40_F : ?Sized,  {
}

impl<A29_Args, A40_F, A6_A, > T33_Fn<A29_Args, > for C<4, (Box<A40_F, >, Box<A6_A, >, ), > where A29_Args: Tuple, A40_F: T33_Fn<A29_Args, >, A6_A: T7_Allocator, A40_F : ?Sized,  {
}

impl<A6_A, A40_F, > T32_FnMut<A6_A, > for C<2, (Box<A40_F, >, ), > where A6_A: Tuple, A40_F: T33_Fn<A6_A, >, A40_F : ?Sized,  {
}

impl<A6_A, A40_F, > T32_FnMut<A6_A, > for C<3, (Box<A40_F, >, ), > where A6_A: Tuple, A40_F: T32_FnMut<A6_A, >, A40_F : ?Sized,  {
}

impl<A29_Args, A40_F, A6_A, > T32_FnMut<A29_Args, > for C<4, (Box<A40_F, >, Box<A6_A, >, ), > where A29_Args: Tuple, A40_F: T32_FnMut<A29_Args, >, A6_A: T7_Allocator, A40_F : ?Sized,  {
}

impl<A6_A, A40_F, > T30_FnOnce<A6_A, > for C<2, (Box<A40_F, >, ), > where A6_A: Tuple, A40_F: T33_Fn<A6_A, >, A40_F : ?Sized,  {
    type A31_Output = <A40_F as T30_FnOnce<A6_A, >>::A31_Output;
}

impl<A6_A, A40_F, > T30_FnOnce<A6_A, > for C<3, (Box<A40_F, >, ), > where A6_A: Tuple, A40_F: T32_FnMut<A6_A, >, A40_F : ?Sized,  {
    type A31_Output = <A40_F as T30_FnOnce<A6_A, >>::A31_Output;
}

impl<A29_Args, A40_F, A6_A, > T30_FnOnce<A29_Args, > for C<4, (Box<A40_F, >, Box<A6_A, >, ), > where A29_Args: Tuple, A40_F: T30_FnOnce<A29_Args, >, A6_A: T7_Allocator, A40_F : ?Sized,  {
    type A31_Output = <A40_F as T30_FnOnce<A29_Args, >>::A31_Output;
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

impl<A5_T, > T3_ToOwned for A5_T where A5_T: T24_Clone,  {
    type A22_Owned = A5_T;
}

impl<A5_T, > T3_ToOwned for [A5_T] where A5_T: T24_Clone,  {
    type A22_Owned = D8_Vec<A5_T, D1_Global, >;
}

impl T3_ToOwned for str {
    type A22_Owned = D16_String;
}

impl<A5_T, > T36_CowObservation<A5_T, > for D4_Cow<[A5_T], > where A5_T: T24_Clone,  {
}
