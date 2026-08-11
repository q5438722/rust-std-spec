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



trait T56_ArrayAdditionalSpecFns<A5_T, > where Self: T55_View, Self: T55_View<A3_V = D17_Seq<A5_T, >>,  {
}

trait T57_SliceAdditionalSpecFns<A5_T, > where Self: T55_View, Self: T55_View<A3_V = D17_Seq<A5_T, >>,  {
}

trait T58_SliceIndex<A5_T, > where A5_T : ?Sized,  {
    type A33_Output : ?Sized;
}

trait T55_View {
    type A3_V : ;
}

trait T59_Clone where Self: Sized,  {
}

trait T60_Copy where Self: T59_Clone,  {
}

trait T62_PartialEq<A61_Rhs, > where A61_Rhs : ?Sized,  {
}

trait T63_Eq where Self: T62_PartialEq<Self, >,  {
}

trait T64_PartialOrd<A61_Rhs, > where Self: T62_PartialEq<A61_Rhs, >, A61_Rhs : ?Sized,  {
}

trait T65_Ord where Self: T63_Eq, Self: T64_PartialOrd<Self, >,  {
}

trait T66_Tuple {
}

trait T32_FnOnce<A67_Args, > where A67_Args: Tuple,  {
    type A33_Output : ;
}

trait T31_FnMut<A67_Args, > where Self: T32_FnOnce<A67_Args, >, A67_Args: Tuple,  {
}

trait T68_Fn<A67_Args, > where Self: T31_FnMut<A67_Args, >, A67_Args: Tuple,  {
}

trait T69_Allocator {
}

trait T70_Debug {
}

trait T71_Hash {
}

trait T72_Default where Self: Sized,  {
}

trait T73_Step where Self: Sized, Self: T59_Clone, Self: T64_PartialOrd<Self, >,  {
}

trait T74_OptionAdditionalFns<A5_T, > where Self: Sized,  {
}

trait T75_ResultAdditionalSpecFns<A5_T, A6_E, > where  {
}

struct D1_Global(
);

struct D2_Ordering(
);

struct D4_Option<A3_V, >(
    Box<A3_V, >,
) where ;

struct D7_Result<A5_T, A6_E, >(
    Box<A5_T, >,
    Box<A6_E, >,
) where ;

struct D8_MaybeUninit<A5_T, >(
    Box<A5_T, >,
) where ;

struct D10_Range<A9_Idx, >(
    Box<A9_Idx, >,
    A9_Idx,
) where ;

struct D11_Bound<A5_T, >(
    Box<A5_T, >,
) where ;

struct D13_ISet<A12_A, >(
    Box<A12_A, >,
    C<0, (Box<(A12_A, ), >, Box<bool, >, ), >,
) where ;

struct D14_Provenance(
);

struct D15_PtrData<A5_T, >(
    Box<A5_T, >,
    <A5_T as std::ptr::Pointee>::Metadata,
) where A5_T : ?Sized, ;

struct D16_SeqInner<A12_A, >(
    Box<A12_A, >,
) where ;

struct D17_Seq<A12_A, >(
    Box<A12_A, >,
    D16_SeqInner<A12_A, >,
) where ;

struct D18_IterMut<A5_T, >(
    Box<A5_T, >,
) where ;

struct D19_Chunks<A5_T, >(
    Box<A5_T, >,
) where ;

struct D20_ChunksExact<A5_T, >(
    Box<A5_T, >,
) where ;

struct D21_ChunksMut<A5_T, >(
    Box<A5_T, >,
) where ;

struct D22_ChunksExactMut<A5_T, >(
    Box<A5_T, >,
) where ;

struct D23_RChunks<A5_T, >(
    Box<A5_T, >,
) where ;

struct D24_RChunksExact<A5_T, >(
    Box<A5_T, >,
) where ;

struct D25_RChunksMut<A5_T, >(
    Box<A5_T, >,
) where ;

struct D26_RChunksExactMut<A5_T, >(
    Box<A5_T, >,
) where ;

struct D27_Windows<A5_T, >(
    Box<A5_T, >,
) where ;

struct D29_ArrayWindows<A5_T, const A28_N: usize, >(
    Box<A5_T, >,
) where ;

struct D34_Split<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D35_SplitMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D36_SplitInclusive<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D37_SplitInclusiveMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D38_SplitN<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D39_SplitNMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D40_RSplit<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D41_RSplitMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D42_RSplitN<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D43_RSplitNMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >, A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, ;

struct D44_ChunkBy<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where ;

struct D45_ChunkByMut<A5_T, A30_P, >(
    Box<A5_T, >,
    Box<A30_P, >,
) where ;

struct D46_Utf8Chunks(
);

struct D47_EscapeAscii(
);

struct D48_GetDisjointMutError(
);

struct D49_Range<A9_Idx, >(
    Box<A9_Idx, >,
) where ;

struct D50_ComparatorObservation<A5_T, >(
    Box<A5_T, >,
    D17_Seq<A5_T, >,
) where ;

struct D51_SliceIteratorView<A5_T, >(
    Box<A5_T, >,
    bool,
) where ;

struct D52_SliceRawMutability(
);

struct D53_SliceRawDomain(
    D52_SliceRawMutability,
);

struct D54_MaybeUninitSliceRelation<A5_T, >(
    Box<A5_T, >,
    D17_Seq<A5_T, >,
) where ;

impl<A5_T, const A28_N: usize, > T55_View for Arr<A5_T, A28_N, > where  {
    type A3_V = D17_Seq<A5_T, >;
}

impl<A5_T, const A28_N: usize, > T56_ArrayAdditionalSpecFns<A5_T, > for Arr<A5_T, A28_N, > where  {
}

impl<A5_T, > T55_View for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
    type A3_V = D15_PtrData<A5_T, >;
}

impl<A5_T, > T55_View for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
    type A3_V = D15_PtrData<A5_T, >;
}

impl<A5_T, > T55_View for [A5_T] where  {
    type A3_V = D17_Seq<A5_T, >;
}

impl<A5_T, > T57_SliceAdditionalSpecFns<A5_T, > for [A5_T] where  {
}

impl T55_View for str {
    type A3_V = D17_Seq<char, >;
}

impl<A12_A, > T55_View for C<2, (Box<A12_A, >, ), > where A12_A: T55_View, A12_A : ?Sized,  {
    type A3_V = <A12_A as T55_View>::A3_V;
}

impl<A12_A, > T55_View for C<4, (Box<A12_A, >, Box<D1_Global, >, ), > where A12_A: T55_View, A12_A : ?Sized,  {
    type A3_V = <A12_A as T55_View>::A3_V;
}

impl<A12_A, > T55_View for C<5, (Box<A12_A, >, Box<D1_Global, >, ), > where A12_A: T55_View,  {
    type A3_V = <A12_A as T55_View>::A3_V;
}

impl<A12_A, > T55_View for C<6, (Box<A12_A, >, Box<D1_Global, >, ), > where A12_A: T55_View,  {
    type A3_V = <A12_A as T55_View>::A3_V;
}

impl<A5_T, > T55_View for D4_Option<A5_T, > where  {
    type A3_V = D4_Option<A5_T, >;
}

impl T55_View for () {
    type A3_V = ();
}

impl T55_View for bool {
    type A3_V = bool;
}

impl T55_View for u8 {
    type A3_V = u8;
}

impl T55_View for usize {
    type A3_V = usize;
}

impl T55_View for char {
    type A3_V = char;
}

impl<A76_A0, > T55_View for (Box<A76_A0, >, ) where A76_A0: T55_View,  {
    type A3_V = (Box<<A76_A0 as T55_View>::A3_V, >, );
}

impl<A76_A0, A77_A1, > T55_View for (Box<A76_A0, >, Box<A77_A1, >, ) where A76_A0: T55_View, A77_A1: T55_View,  {
    type A3_V = (Box<<A76_A0 as T55_View>::A3_V, >, Box<<A77_A1 as T55_View>::A3_V, >, );
}

impl<A5_T, > T74_OptionAdditionalFns<A5_T, > for D4_Option<A5_T, > where  {
}

impl<A5_T, A6_E, > T75_ResultAdditionalSpecFns<A5_T, A6_E, > for D7_Result<A5_T, A6_E, > where  {
}

impl<A5_T, A12_A, > T59_Clone for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T59_Clone, A12_A: T69_Allocator, A12_A: T59_Clone,  {
}

impl<A5_T, A12_A, > T59_Clone for C<4, (Box<[A5_T], >, Box<A12_A, >, ), > where A5_T: T59_Clone, A12_A: T69_Allocator, A12_A: T59_Clone,  {
}

impl T59_Clone for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T59_Clone for D8_MaybeUninit<A5_T, > where A5_T: T60_Copy,  {
}

impl T59_Clone for usize {
}

impl T59_Clone for u8 {
}

impl T59_Clone for bool {
}

impl T59_Clone for char {
}

impl<A5_T, > T59_Clone for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T59_Clone for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T59_Clone for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl T59_Clone for D2_Ordering {
}

impl<A9_Idx, > T59_Clone for D10_Range<A9_Idx, > where A9_Idx: T59_Clone,  {
}

impl<A5_T, > T59_Clone for D11_Bound<A5_T, > where A5_T: T59_Clone,  {
}

impl<A5_T, const A28_N: usize, > T59_Clone for Arr<A5_T, A28_N, > where A5_T: T59_Clone,  {
}

impl<A5_T, A6_E, > T59_Clone for D7_Result<A5_T, A6_E, > where A5_T: T59_Clone, A6_E: T59_Clone,  {
}

impl T59_Clone for D1_Global {
}

impl<A5_T, A12_A, > T59_Clone for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A12_A: T69_Allocator, A12_A: T59_Clone, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T59_Clone for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A12_A: T69_Allocator, A12_A: T59_Clone, A5_T : ?Sized,  {
}

impl<A12_A, > T59_Clone for C<7, (Box<A12_A, >, ), > where  {
}

impl<A12_A, > T59_Clone for C<8, (Box<A12_A, >, ), > where A12_A: T60_Copy,  {
}

impl T59_Clone for int {
}

impl T59_Clone for nat {
}

impl T62_PartialEq<str, > for str {
}

impl<A12_A, A78_B, > T62_PartialEq<C<2, (Box<A78_B, >, ), >, > for C<2, (Box<A12_A, >, ), > where A12_A: T62_PartialEq<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A12_A, A78_B, > T62_PartialEq<C<3, (Box<A78_B, >, ), >, > for C<2, (Box<A12_A, >, ), > where A12_A: T62_PartialEq<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<Arr<A79_U, A28_N, >, > for C<2, (Box<[A5_T], >, ), > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, > T62_PartialEq<C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), >, > for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T62_PartialEq<C<1, (Box<A5_T, >, ), >, > for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl T62_PartialEq<D2_Ordering, > for D2_Ordering {
}

impl T62_PartialEq<(), > for () {
}

impl T62_PartialEq<bool, > for bool {
}

impl T62_PartialEq<char, > for char {
}

impl T62_PartialEq<usize, > for usize {
}

impl T62_PartialEq<u8, > for u8 {
}

impl<A12_A, A78_B, > T62_PartialEq<C<3, (Box<A78_B, >, ), >, > for C<3, (Box<A12_A, >, ), > where A12_A: T62_PartialEq<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A12_A, A78_B, > T62_PartialEq<C<2, (Box<A78_B, >, ), >, > for C<3, (Box<A12_A, >, ), > where A12_A: T62_PartialEq<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<Arr<A79_U, A28_N, >, > for C<3, (Box<[A5_T], >, ), > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A9_Idx, > T62_PartialEq<D10_Range<A9_Idx, >, > for D10_Range<A9_Idx, > where A9_Idx: T62_PartialEq<A9_Idx, >,  {
}

impl<A5_T, > T62_PartialEq<D11_Bound<A5_T, >, > for D11_Bound<A5_T, > where A5_T: T62_PartialEq<A5_T, >,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<Arr<A79_U, A28_N, >, > for Arr<A5_T, A28_N, > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<[A79_U], > for Arr<A5_T, A28_N, > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<C<2, (Box<[A79_U], >, ), >, > for Arr<A5_T, A28_N, > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<C<3, (Box<[A79_U], >, ), >, > for Arr<A5_T, A28_N, > where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, A79_U, const A28_N: usize, > T62_PartialEq<Arr<A79_U, A28_N, >, > for [A5_T] where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, A79_U, > T62_PartialEq<[A79_U], > for [A5_T] where A5_T: T62_PartialEq<A79_U, >,  {
}

impl<A5_T, > T62_PartialEq<D4_Option<A5_T, >, > for D4_Option<A5_T, > where A5_T: T62_PartialEq<A5_T, >,  {
}

impl<A5_T, A6_E, > T62_PartialEq<D7_Result<A5_T, A6_E, >, > for D7_Result<A5_T, A6_E, > where A5_T: T62_PartialEq<A5_T, >, A6_E: T62_PartialEq<A6_E, >,  {
}

impl<A5_T, > T62_PartialEq<(Box<A5_T, >, ), > for (Box<A5_T, >, ) where A5_T: T62_PartialEq<A5_T, >,  {
}

impl<A79_U, A5_T, > T62_PartialEq<(Box<A79_U, >, Box<A5_T, >, ), > for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T62_PartialEq<A79_U, >, A5_T: T62_PartialEq<A5_T, >,  {
}

impl<A5_T, A12_A, > T62_PartialEq<C<4, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T62_PartialEq<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T62_PartialEq<C<5, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T62_PartialEq<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T62_PartialEq<C<6, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T62_PartialEq<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl T62_PartialEq<int, > for int {
}

impl T62_PartialEq<nat, > for nat {
}

impl<A5_T, > T63_Eq for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T63_Eq for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl T63_Eq for D2_Ordering {
}

impl T63_Eq for () {
}

impl T63_Eq for bool {
}

impl T63_Eq for char {
}

impl T63_Eq for usize {
}

impl T63_Eq for u8 {
}

impl<A12_A, > T63_Eq for C<2, (Box<A12_A, >, ), > where A12_A: T63_Eq, A12_A : ?Sized,  {
}

impl<A12_A, > T63_Eq for C<3, (Box<A12_A, >, ), > where A12_A: T63_Eq, A12_A : ?Sized,  {
}

impl<A9_Idx, > T63_Eq for D10_Range<A9_Idx, > where A9_Idx: T63_Eq,  {
}

impl<A5_T, > T63_Eq for D11_Bound<A5_T, > where A5_T: T63_Eq,  {
}

impl<A5_T, const A28_N: usize, > T63_Eq for Arr<A5_T, A28_N, > where A5_T: T63_Eq,  {
}

impl<A5_T, > T63_Eq for D4_Option<A5_T, > where A5_T: T63_Eq,  {
}

impl<A5_T, A6_E, > T63_Eq for D7_Result<A5_T, A6_E, > where A5_T: T63_Eq, A6_E: T63_Eq,  {
}

impl<A5_T, > T63_Eq for [A5_T] where A5_T: T63_Eq,  {
}

impl T63_Eq for str {
}

impl<A5_T, > T63_Eq for (Box<A5_T, >, ) where A5_T: T63_Eq,  {
}

impl<A79_U, A5_T, > T63_Eq for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T63_Eq, A5_T: T63_Eq,  {
}

impl<A5_T, A12_A, > T63_Eq for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T63_Eq, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T63_Eq for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T63_Eq, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T63_Eq for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T63_Eq, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl T63_Eq for int {
}

impl T63_Eq for nat {
}

impl<A5_T, > T65_Ord for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T65_Ord for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl T65_Ord for D2_Ordering {
}

impl T65_Ord for () {
}

impl T65_Ord for bool {
}

impl T65_Ord for char {
}

impl T65_Ord for usize {
}

impl T65_Ord for u8 {
}

impl<A12_A, > T65_Ord for C<2, (Box<A12_A, >, ), > where A12_A: T65_Ord, A12_A : ?Sized,  {
}

impl<A12_A, > T65_Ord for C<3, (Box<A12_A, >, ), > where A12_A: T65_Ord, A12_A : ?Sized,  {
}

impl<A5_T, const A28_N: usize, > T65_Ord for Arr<A5_T, A28_N, > where A5_T: T65_Ord,  {
}

impl<A5_T, > T65_Ord for D4_Option<A5_T, > where A5_T: T65_Ord,  {
}

impl<A5_T, A6_E, > T65_Ord for D7_Result<A5_T, A6_E, > where A5_T: T65_Ord, A6_E: T65_Ord,  {
}

impl<A5_T, > T65_Ord for [A5_T] where A5_T: T65_Ord,  {
}

impl T65_Ord for str {
}

impl<A5_T, > T65_Ord for (Box<A5_T, >, ) where A5_T: T65_Ord,  {
}

impl<A79_U, A5_T, > T65_Ord for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T65_Ord, A5_T: T65_Ord,  {
}

impl<A5_T, A12_A, > T65_Ord for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T65_Ord, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T65_Ord for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T65_Ord, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T65_Ord for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T65_Ord, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl T65_Ord for int {
}

impl T65_Ord for nat {
}

impl<A12_A, A78_B, > T64_PartialOrd<C<2, (Box<A78_B, >, ), >, > for C<2, (Box<A12_A, >, ), > where A12_A: T64_PartialOrd<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A5_T, > T64_PartialOrd<C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), >, > for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T64_PartialOrd<C<1, (Box<A5_T, >, ), >, > for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl T64_PartialOrd<D2_Ordering, > for D2_Ordering {
}

impl T64_PartialOrd<(), > for () {
}

impl T64_PartialOrd<bool, > for bool {
}

impl T64_PartialOrd<char, > for char {
}

impl T64_PartialOrd<usize, > for usize {
}

impl T64_PartialOrd<u8, > for u8 {
}

impl<A12_A, A78_B, > T64_PartialOrd<C<3, (Box<A78_B, >, ), >, > for C<3, (Box<A12_A, >, ), > where A12_A: T64_PartialOrd<A78_B, >, A12_A : ?Sized, A78_B : ?Sized,  {
}

impl<A5_T, const A28_N: usize, > T64_PartialOrd<Arr<A5_T, A28_N, >, > for Arr<A5_T, A28_N, > where A5_T: T64_PartialOrd<A5_T, >,  {
}

impl<A5_T, > T64_PartialOrd<D4_Option<A5_T, >, > for D4_Option<A5_T, > where A5_T: T64_PartialOrd<A5_T, >,  {
}

impl<A5_T, A6_E, > T64_PartialOrd<D7_Result<A5_T, A6_E, >, > for D7_Result<A5_T, A6_E, > where A5_T: T64_PartialOrd<A5_T, >, A6_E: T64_PartialOrd<A6_E, >,  {
}

impl<A5_T, > T64_PartialOrd<[A5_T], > for [A5_T] where A5_T: T64_PartialOrd<A5_T, >,  {
}

impl T64_PartialOrd<str, > for str {
}

impl<A5_T, > T64_PartialOrd<(Box<A5_T, >, ), > for (Box<A5_T, >, ) where A5_T: T64_PartialOrd<A5_T, >,  {
}

impl<A79_U, A5_T, > T64_PartialOrd<(Box<A79_U, >, Box<A5_T, >, ), > for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T64_PartialOrd<A79_U, >, A5_T: T64_PartialOrd<A5_T, >,  {
}

impl<A5_T, A12_A, > T64_PartialOrd<C<4, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T64_PartialOrd<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T64_PartialOrd<C<5, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T64_PartialOrd<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T64_PartialOrd<C<6, (Box<A5_T, >, Box<A12_A, >, ), >, > for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T64_PartialOrd<A5_T, >, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl T64_PartialOrd<int, > for int {
}

impl T64_PartialOrd<nat, > for nat {
}

impl<A5_T, > T72_Default for C<4, (Box<A5_T, >, Box<D1_Global, >, ), > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for C<4, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl T72_Default for C<4, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T72_Default for C<2, (Box<[A5_T], >, ), > where  {
}

impl T72_Default for C<2, (Box<str, >, ), > {
}

impl T72_Default for () {
}

impl T72_Default for bool {
}

impl T72_Default for char {
}

impl T72_Default for usize {
}

impl T72_Default for u8 {
}

impl<A9_Idx, > T72_Default for D10_Range<A9_Idx, > where A9_Idx: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 32, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 31, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 30, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 29, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 28, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 27, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 26, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 25, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 24, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 23, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 22, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 21, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 20, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 19, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 18, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 17, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 16, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 15, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 14, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 13, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 12, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 11, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 10, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 9, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 8, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 7, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 6, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 5, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 4, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 3, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 2, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 1, > where A5_T: T72_Default,  {
}

impl<A5_T, > T72_Default for Arr<A5_T, 0, > where  {
}

impl<A5_T, > T72_Default for C<3, (Box<[A5_T], >, ), > where  {
}

impl T72_Default for C<3, (Box<str, >, ), > {
}

impl<A5_T, > T72_Default for D4_Option<A5_T, > where  {
}

impl<A5_T, > T72_Default for (Box<A5_T, >, ) where A5_T: T72_Default,  {
}

impl<A79_U, A5_T, > T72_Default for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T72_Default, A5_T: T72_Default,  {
}

impl T72_Default for D1_Global {
}

impl<A5_T, > T72_Default for C<5, (Box<A5_T, >, Box<D1_Global, >, ), > where A5_T: T72_Default,  {
}

impl T72_Default for C<5, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T72_Default for C<5, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, > T72_Default for C<6, (Box<A5_T, >, Box<D1_Global, >, ), > where A5_T: T72_Default,  {
}

impl T72_Default for C<6, (Box<str, >, Box<D1_Global, >, ), > {
}

impl<A5_T, > T72_Default for C<6, (Box<[A5_T], >, Box<D1_Global, >, ), > where  {
}

impl<A5_T, > T60_Copy for D8_MaybeUninit<A5_T, > where A5_T: T60_Copy,  {
}

impl T60_Copy for D2_Ordering {
}

impl T60_Copy for usize {
}

impl T60_Copy for u8 {
}

impl T60_Copy for bool {
}

impl T60_Copy for char {
}

impl<A5_T, > T60_Copy for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T60_Copy for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T60_Copy for C<2, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T60_Copy for D11_Bound<A5_T, > where A5_T: T60_Copy,  {
}

impl<A5_T, const A28_N: usize, > T60_Copy for Arr<A5_T, A28_N, > where A5_T: T60_Copy,  {
}

impl<A5_T, > T60_Copy for D4_Option<A5_T, > where A5_T: T60_Copy,  {
}

impl<A5_T, A6_E, > T60_Copy for D7_Result<A5_T, A6_E, > where A5_T: T60_Copy, A6_E: T60_Copy,  {
}

impl T60_Copy for D1_Global {
}

impl<A12_A, > T60_Copy for C<7, (Box<A12_A, >, ), > where  {
}

impl<A12_A, > T60_Copy for C<8, (Box<A12_A, >, ), > where A12_A: T60_Copy,  {
}

impl T60_Copy for int {
}

impl T60_Copy for nat {
}

impl<A12_A, A80_F, > T68_Fn<A12_A, > for C<2, (Box<A80_F, >, ), > where A12_A: Tuple, A80_F: T68_Fn<A12_A, >, A80_F : ?Sized,  {
}

impl<A67_Args, A80_F, A12_A, > T68_Fn<A67_Args, > for C<4, (Box<A80_F, >, Box<A12_A, >, ), > where A67_Args: Tuple, A80_F: T68_Fn<A67_Args, >, A12_A: T69_Allocator, A80_F : ?Sized,  {
}

impl<A12_A, A80_F, > T31_FnMut<A12_A, > for C<2, (Box<A80_F, >, ), > where A12_A: Tuple, A80_F: T68_Fn<A12_A, >, A80_F : ?Sized,  {
}

impl<A12_A, A80_F, > T31_FnMut<A12_A, > for C<3, (Box<A80_F, >, ), > where A12_A: Tuple, A80_F: T31_FnMut<A12_A, >, A80_F : ?Sized,  {
}

impl<A67_Args, A80_F, A12_A, > T31_FnMut<A67_Args, > for C<4, (Box<A80_F, >, Box<A12_A, >, ), > where A67_Args: Tuple, A80_F: T31_FnMut<A67_Args, >, A12_A: T69_Allocator, A80_F : ?Sized,  {
}

impl<A12_A, A80_F, > T32_FnOnce<A12_A, > for C<2, (Box<A80_F, >, ), > where A12_A: Tuple, A80_F: T68_Fn<A12_A, >, A80_F : ?Sized,  {
    type A33_Output = <A80_F as T32_FnOnce<A12_A, >>::A33_Output;
}

impl<A12_A, A80_F, > T32_FnOnce<A12_A, > for C<3, (Box<A80_F, >, ), > where A12_A: Tuple, A80_F: T31_FnMut<A12_A, >, A80_F : ?Sized,  {
    type A33_Output = <A80_F as T32_FnOnce<A12_A, >>::A33_Output;
}

impl<A67_Args, A80_F, A12_A, > T32_FnOnce<A67_Args, > for C<4, (Box<A80_F, >, Box<A12_A, >, ), > where A67_Args: Tuple, A80_F: T32_FnOnce<A67_Args, >, A12_A: T69_Allocator, A80_F : ?Sized,  {
    type A33_Output = <A80_F as T32_FnOnce<A67_Args, >>::A33_Output;
}

impl T73_Step for u8 {
}

impl T73_Step for usize {
}

impl T73_Step for char {
}

impl<A5_T, > T70_Debug for D8_MaybeUninit<A5_T, > where  {
}

impl T70_Debug for D2_Ordering {
}

impl<A9_Idx, > T70_Debug for D10_Range<A9_Idx, > where A9_Idx: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D11_Bound<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, const A28_N: usize, > T70_Debug for Arr<A5_T, A28_N, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D4_Option<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, A6_E, > T70_Debug for D7_Result<A5_T, A6_E, > where A5_T: T70_Debug, A6_E: T70_Debug,  {
}

impl T70_Debug for u8 {
}

impl T70_Debug for usize {
}

impl<A5_T, > T70_Debug for C<2, (Box<A5_T, >, ), > where A5_T: T70_Debug, A5_T : ?Sized,  {
}

impl<A5_T, > T70_Debug for C<3, (Box<A5_T, >, ), > where A5_T: T70_Debug, A5_T : ?Sized,  {
}

impl T70_Debug for bool {
}

impl T70_Debug for str {
}

impl T70_Debug for char {
}

impl<A5_T, > T70_Debug for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T70_Debug for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A79_U, A5_T, > T70_Debug for (Box<A79_U, >, Box<A5_T, >, ) where A79_U: T70_Debug, A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for (Box<A5_T, >, ) where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for [A5_T] where A5_T: T70_Debug,  {
}

impl T70_Debug for () {
}

impl T70_Debug for D1_Global {
}

impl<A5_T, A12_A, > T70_Debug for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T70_Debug, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T70_Debug for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T70_Debug, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T70_Debug for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T70_Debug, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A12_A, > T70_Debug for C<8, (Box<A12_A, >, ), > where  {
}

impl T71_Hash for D2_Ordering {
}

impl<A9_Idx, > T71_Hash for D10_Range<A9_Idx, > where A9_Idx: T71_Hash,  {
}

impl<A5_T, > T71_Hash for D11_Bound<A5_T, > where A5_T: T71_Hash,  {
}

impl<A5_T, const A28_N: usize, > T71_Hash for Arr<A5_T, A28_N, > where A5_T: T71_Hash,  {
}

impl<A5_T, > T71_Hash for D4_Option<A5_T, > where A5_T: T71_Hash,  {
}

impl<A5_T, A6_E, > T71_Hash for D7_Result<A5_T, A6_E, > where A5_T: T71_Hash, A6_E: T71_Hash,  {
}

impl T71_Hash for u8 {
}

impl T71_Hash for usize {
}

impl T71_Hash for bool {
}

impl T71_Hash for char {
}

impl T71_Hash for str {
}

impl T71_Hash for () {
}

impl<A5_T, > T71_Hash for (Box<A5_T, >, ) where A5_T: T71_Hash,  {
}

impl<A5_T, A78_B, > T71_Hash for (Box<A5_T, >, Box<A78_B, >, ) where A5_T: T71_Hash, A78_B: T71_Hash,  {
}

impl<A5_T, > T71_Hash for [A5_T] where A5_T: T71_Hash,  {
}

impl<A5_T, > T71_Hash for C<2, (Box<A5_T, >, ), > where A5_T: T71_Hash, A5_T : ?Sized,  {
}

impl<A5_T, > T71_Hash for C<3, (Box<A5_T, >, ), > where A5_T: T71_Hash, A5_T : ?Sized,  {
}

impl<A5_T, > T71_Hash for C<10, (Box<C<1, (Box<A5_T, >, ), >, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, > T71_Hash for C<1, (Box<A5_T, >, ), > where A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T71_Hash for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T71_Hash, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T71_Hash for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T71_Hash, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T71_Hash for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T71_Hash, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, > T58_SliceIndex<[A5_T], > for usize where  {
    type A33_Output = A5_T;
}

impl<A5_T, > T58_SliceIndex<[A5_T], > for D10_Range<usize, > where  {
    type A33_Output = [A5_T];
}

impl T58_SliceIndex<str, > for D10_Range<usize, > {
    type A33_Output = str;
}

impl<A5_T, > T58_SliceIndex<[A5_T], > for (Box<D11_Bound<usize, >, >, Box<D11_Bound<usize, >, >, ) where  {
    type A33_Output = [A5_T];
}

impl T58_SliceIndex<str, > for (Box<D11_Bound<usize, >, >, Box<D11_Bound<usize, >, >, ) {
    type A33_Output = str;
}

impl<A12_A, > T69_Allocator for C<2, (Box<A12_A, >, ), > where A12_A: T69_Allocator, A12_A : ?Sized,  {
}

impl<A12_A, > T69_Allocator for C<3, (Box<A12_A, >, ), > where A12_A: T69_Allocator, A12_A : ?Sized,  {
}

impl T69_Allocator for D1_Global {
}

impl<A5_T, A12_A, > T69_Allocator for C<4, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T69_Allocator, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T69_Allocator for C<5, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T69_Allocator, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, A12_A, > T69_Allocator for C<6, (Box<A5_T, >, Box<A12_A, >, ), > where A5_T: T69_Allocator, A12_A: T69_Allocator, A5_T : ?Sized,  {
}

impl<A5_T, > T59_Clone for D4_Option<A5_T, > where A5_T: T59_Clone,  {
}

impl<A9_Idx, > T59_Clone for D49_Range<A9_Idx, > where A9_Idx: T59_Clone,  {
}

impl T59_Clone for D47_EscapeAscii {
}

impl<A5_T, A30_P, > T59_Clone for D34_Split<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A30_P: T59_Clone, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T59_Clone for D36_SplitInclusive<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A30_P: T59_Clone, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T59_Clone for D40_RSplit<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A30_P: T59_Clone, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, > T59_Clone for D27_Windows<A5_T, > where  {
}

impl<A5_T, > T59_Clone for D19_Chunks<A5_T, > where  {
}

impl<A5_T, > T59_Clone for D20_ChunksExact<A5_T, > where  {
}

impl<A5_T, const A28_N: usize, > T59_Clone for D29_ArrayWindows<A5_T, A28_N, > where  {
}

impl<A5_T, > T59_Clone for D23_RChunks<A5_T, > where  {
}

impl<A5_T, > T59_Clone for D24_RChunksExact<A5_T, > where  {
}

impl<A5_T, A30_P, > T59_Clone for D44_ChunkBy<A5_T, A30_P, > where A30_P: T59_Clone,  {
}

impl T59_Clone for D48_GetDisjointMutError {
}

impl T59_Clone for D46_Utf8Chunks {
}

impl<A9_Idx, > T62_PartialEq<D49_Range<A9_Idx, >, > for D49_Range<A9_Idx, > where A9_Idx: T62_PartialEq<A9_Idx, >,  {
}

impl T62_PartialEq<D48_GetDisjointMutError, > for D48_GetDisjointMutError {
}

impl<A9_Idx, > T63_Eq for D49_Range<A9_Idx, > where A9_Idx: T63_Eq,  {
}

impl T63_Eq for D48_GetDisjointMutError {
}

impl<A9_Idx, > T72_Default for D49_Range<A9_Idx, > where A9_Idx: T72_Default,  {
}

impl<A5_T, > T72_Default for D18_IterMut<A5_T, > where  {
}

impl<A9_Idx, > T60_Copy for D49_Range<A9_Idx, > where A9_Idx: T60_Copy,  {
}

impl<A9_Idx, > T70_Debug for D49_Range<A9_Idx, > where A9_Idx: T70_Debug,  {
}

impl T70_Debug for D47_EscapeAscii {
}

impl<A5_T, > T70_Debug for D18_IterMut<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, A30_P, > T70_Debug for D34_Split<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D36_SplitInclusive<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D35_SplitMut<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D37_SplitInclusiveMut<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D40_RSplit<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D41_RSplitMut<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D38_SplitN<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D42_RSplitN<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D39_SplitNMut<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, A30_P, > T70_Debug for D43_RSplitNMut<A5_T, A30_P, > where A30_P: T32_FnOnce<(Box<C<2, (Box<A5_T, >, ), >, >, ), A33_Output = bool>, A5_T: T70_Debug, A30_P: T31_FnMut<(Box<C<2, (Box<A5_T, >, ), >, >, ), >,  {
}

impl<A5_T, > T70_Debug for D27_Windows<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D19_Chunks<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D21_ChunksMut<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D20_ChunksExact<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D22_ChunksExactMut<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, const A28_N: usize, > T70_Debug for D29_ArrayWindows<A5_T, A28_N, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D23_RChunks<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D25_RChunksMut<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D24_RChunksExact<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, > T70_Debug for D26_RChunksExactMut<A5_T, > where A5_T: T70_Debug,  {
}

impl<A5_T, A30_P, > T70_Debug for D44_ChunkBy<A5_T, A30_P, > where A5_T: T70_Debug,  {
}

impl<A5_T, A30_P, > T70_Debug for D45_ChunkByMut<A5_T, A30_P, > where A5_T: T70_Debug,  {
}

impl T70_Debug for D48_GetDisjointMutError {
}

impl T70_Debug for D46_Utf8Chunks {
}

impl<A9_Idx, > T71_Hash for D49_Range<A9_Idx, > where A9_Idx: T71_Hash,  {
}

impl<A5_T, > T58_SliceIndex<[A5_T], > for D49_Range<usize, > where  {
    type A33_Output = [A5_T];
}

impl T58_SliceIndex<str, > for D49_Range<usize, > {
    type A33_Output = str;
}
