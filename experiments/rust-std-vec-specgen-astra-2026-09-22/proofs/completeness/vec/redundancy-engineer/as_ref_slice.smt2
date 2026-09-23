(declare-sort FuelId 0)
(declare-sort Poly 0)
(declare-sort Type 0)
(declare-sort Dcr 0)
(declare-sort %%Function%% 0)
(declare-sort Height 0)
(declare-sort alloc!alloc.Global. 0)
(declare-sort vstd!raw_ptr.Provenance. 0)
(declare-datatypes ((vstd!raw_ptr.PtrData. 0)) (((vstd!raw_ptr.PtrData./PtrData (vstd!raw_ptr.PtrData./PtrData/?addr Int) (vstd!raw_ptr.PtrData./PtrData/?provenance vstd!raw_ptr.Provenance.) (vstd!raw_ptr.PtrData./PtrData/?metadata Poly)))))
(declare-datatypes ((tuple%0. 0)) (((tuple%0./tuple%0))))
(declare-fun fuel_bool (FuelId) Bool)
(declare-fun fuel_bool_default (FuelId) Bool)
(declare-fun fuel_defaults () Bool)
(declare-fun mut_ref_update_current% (Poly Poly) Poly)
(declare-fun mut_ref_current% (Poly) Poly)
(declare-fun mut_ref_future% (Poly) Poly)
(declare-fun has_type (Poly Type) Bool)
(declare-fun MUTREF (Dcr Type) Type)
(declare-fun sized (Dcr) Bool)
(declare-fun DST (Dcr) Dcr)
(declare-fun REF (Dcr) Dcr)
(declare-fun BOX (Dcr Type Dcr) Dcr)
(declare-fun RC (Dcr Type Dcr) Dcr)
(declare-fun ARC (Dcr Type Dcr) Dcr)
(declare-fun GHOST (Dcr) Dcr)
(declare-fun TRACKED (Dcr) Dcr)
(declare-fun NEVER (Dcr) Dcr)
(declare-fun CONST_PTR (Dcr) Dcr)
(declare-fun $ () Dcr)
(declare-fun CONST_INT (Int) Type)
(declare-fun const_int (Type) Int)
(declare-fun CONST_BOOL (Bool) Type)
(declare-fun const_bool (Type) Bool)
(declare-fun BOOL () Type)
(declare-fun B (Bool) Poly)
(declare-fun REAL () Type)
(declare-fun R (Real) Poly)
(declare-fun as_type (Poly Type) Poly)
(declare-fun mk_fun (%%Function%%) %%Function%%)
(declare-fun %B (Poly) Bool)
(declare-fun I (Int) Poly)
(declare-fun %I (Poly) Int)
(declare-fun %R (Poly) Real)
(declare-fun INT () Type)
(declare-fun NAT () Type)
(declare-fun USIZE () Type)
(declare-fun ISIZE () Type)
(declare-fun UINT (Int) Type)
(declare-fun SINT (Int) Type)
(declare-fun FLOAT (Int) Type)
(declare-fun CHAR () Type)
(declare-fun ext_eq (Bool Type Poly Poly) Bool)
(declare-fun SZ () Int)
(declare-fun uHi (Int) Int)
(declare-fun iLo (Int) Int)
(declare-fun iHi (Int) Int)
(declare-fun nClip (Int) Int)
(declare-fun uClip (Int Int) Int)
(declare-fun iClip (Int Int) Int)
(declare-fun charClip (Int) Int)
(declare-fun uInv (Int Int) Bool)
(declare-fun iInv (Int Int) Bool)
(declare-fun charInv (Int) Bool)
(declare-fun Add (Int Int) Int)
(declare-fun Sub (Int Int) Int)
(declare-fun Mul (Int Int) Int)
(declare-fun EucDiv (Int Int) Int)
(declare-fun EucMod (Int Int) Int)
(declare-fun RAdd (Real Real) Real)
(declare-fun RSub (Real Real) Real)
(declare-fun RMul (Real Real) Real)
(declare-fun RDiv (Real Real) Real)
(declare-fun bitxor (Poly Poly) Int)
(declare-fun bitor (Poly Poly) Int)
(declare-fun bitand (Poly Poly) Int)
(declare-fun bitshr (Poly Poly) Int)
(declare-fun singular_mod (Int Int) Int)
(declare-fun check_decrease_height (Poly Poly Bool) Bool)
(declare-fun height (Poly) Height)
(declare-fun height_lt (Height Height) Bool)
(declare-fun fuel%vstd!group_vstd_default. () FuelId)
(declare-fun fuel%vstd!std_specs.nonzero.group_nonzero_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.vec.group_vec_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.range.group_range_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.hash.group_hash_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.btree.group_btree_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.
             ()
             FuelId)
(declare-fun fuel%vstd!std_specs.iter.group_iter_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.fmt.group_fmt_axioms. () FuelId)
(declare-fun fuel%vstd!std_specs.control_flow.group_control_flow_axioms.
             ()
             FuelId)
(declare-fun fuel%vstd!std_specs.bits.group_bits_axioms. () FuelId)
(declare-fun fuel%vstd!string.group_string_axioms. () FuelId)
(declare-fun fuel%vstd!slice.group_slice_axioms. () FuelId)
(declare-fun fuel%vstd!set_lib.group_set_lib_default. () FuelId)
(declare-fun fuel%vstd!set.group_set_lemmas. () FuelId)
(declare-fun fuel%vstd!seq_lib.group_seq_lib_default. () FuelId)
(declare-fun fuel%vstd!seq_lib.group_filter_ensures. () FuelId)
(declare-fun fuel%vstd!seq.group_seq_lemmas. () FuelId)
(declare-fun fuel%vstd!raw_ptr.group_raw_ptr_axioms. () FuelId)
(declare-fun fuel%vstd!mut_ref.group_mut_ref_axioms. () FuelId)
(declare-fun fuel%vstd!multiset.group_multiset_axioms. () FuelId)
(declare-fun fuel%vstd!map.group_map_lemmas. () FuelId)
(declare-fun fuel%vstd!layout.group_layout_axioms. () FuelId)
(declare-fun fuel%vstd!layout.group_align_properties. () FuelId)
(declare-fun fuel%vstd!laws_eq.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_11_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_10_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_9_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_8_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_7_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_6_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_5_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_4_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_3_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_2_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.tuple_1_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.isize_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.usize_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.i128_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.u128_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.i64_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.u64_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.i32_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.u32_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.i16_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.u16_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.i8_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.u8_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_eq.bool_laws.group_laws_eq. () FuelId)
(declare-fun fuel%vstd!laws_cmp.group_laws_cmp. () FuelId)
(declare-fun fuel%vstd!iset.group_iset_lemmas. () FuelId)
(declare-fun fuel%vstd!imap.group_imap_lemmas. () FuelId)
(declare-fun fuel%vstd!function.group_function_axioms. () FuelId)
(declare-fun fuel%vstd!array.group_array_axioms. () FuelId)
(declare-fun fuel%lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.
             ()
             FuelId)
(declare-fun fuel%vstd!view.impl&%30.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%18.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%16.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%6.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%4.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%2.view. () FuelId)
(declare-fun fuel%vstd!view.impl&%0.view. () FuelId)
(declare-fun fuel%vstd!slice.lemma_slice_index_decreases. () FuelId)
(declare-fun fuel%vstd!slice.axiom_slice_decreases_to_seq. () FuelId)
(declare-fun fuel%vstd!slice.axiom_slice_has_resolved. () FuelId)
(declare-fun fuel%vstd!slice.axiom_slice_ext_equal. () FuelId)
(declare-fun fuel%vstd!slice.len%returns_clause_autospec. () FuelId)
(declare-fun fuel%vstd!slice.axiom_spec_len. () FuelId)
(declare-fun fuel%vstd!slice.impl&%2.spec_index. () FuelId)
(declare-fun fuel%vstd!seq.lemma_seq_ext_equal_deep. () FuelId)
(declare-fun fuel%vstd!seq.lemma_seq_ext_equal. () FuelId)
(declare-fun fuel%vstd!seq.lemma_seq_index_decreases. () FuelId)
(declare-fun fuel%vstd!seq.impl&%2.spec_index. () FuelId)
(declare-fun fuel%vstd!raw_ptr.ptrs_mut_eq_sized. () FuelId)
(declare-fun fuel%vstd!raw_ptr.ptrs_mut_eq. () FuelId)
(declare-fun fuel%vstd!raw_ptr.impl&%3.view. () FuelId)
(declare-fun fuel%vstd!function.axiom_fn_mut_call_ensures. () FuelId)
(declare-fun fuel%vstd!function.axiom_fn_mut_call_requires. () FuelId)
(declare-fun fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view. () FuelId)
(declare-fun fuel%vstd!std_specs.vec.axiom_vec_has_resolved. () FuelId)
(declare-fun fuel%vstd!std_specs.vec.axiom_spec_len. () FuelId)
(declare-fun pointee_metadata% (Dcr) Type)
(declare-fun TYPE%tuple%0. () Type)
(declare-fun pointee_metadata%% (Dcr) Dcr)
(declare-fun $slice () Dcr)
(declare-fun Poly%alloc!alloc.Global. (alloc!alloc.Global.) Poly)
(declare-fun %Poly%alloc!alloc.Global. (Poly) alloc!alloc.Global.)
(declare-fun TYPE%alloc!alloc.Global. () Type)
(declare-fun Poly%vstd!raw_ptr.Provenance. (vstd!raw_ptr.Provenance.) Poly)
(declare-fun %Poly%vstd!raw_ptr.Provenance. (Poly) vstd!raw_ptr.Provenance.)
(declare-fun TYPE%vstd!raw_ptr.Provenance. () Type)
(declare-fun Poly%vstd!raw_ptr.PtrData. (vstd!raw_ptr.PtrData.) Poly)
(declare-fun %Poly%vstd!raw_ptr.PtrData. (Poly) vstd!raw_ptr.PtrData.)
(declare-fun TYPE%vstd!raw_ptr.PtrData. (Dcr Type) Type)
(declare-fun vstd!raw_ptr.PtrData./PtrData/addr (vstd!raw_ptr.PtrData.) Int)
(declare-fun vstd!raw_ptr.PtrData./PtrData/provenance
             (vstd!raw_ptr.PtrData.)
             vstd!raw_ptr.Provenance.)
(declare-fun vstd!raw_ptr.PtrData./PtrData/metadata
             (vstd!raw_ptr.PtrData.)
             Poly)
(declare-fun Poly%tuple%0. (tuple%0.) Poly)
(declare-fun %Poly%tuple%0. (Poly) tuple%0.)
(declare-fun tr_bound%vstd!slice.SliceAdditionalSpecFns.
             (Dcr Type Dcr Type)
             Bool)
(declare-fun proj%vstd!view.View./V (Dcr Type) Type)
(declare-fun TYPE%vstd!seq.Seq. (Dcr Type) Type)
(declare-fun proj%%vstd!view.View./V (Dcr Type) Dcr)
(declare-fun tr_bound%vstd!view.View. (Dcr Type) Bool)
(declare-fun tr_bound%core!marker.Tuple. (Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.FnOnce. (Dcr Type Dcr Type) Bool)
(declare-fun proj%%core!ops.function.FnOnce./Output (Dcr Type Dcr Type) Dcr)
(declare-fun tr_bound%core!ops.function.FnMut. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.Fn. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!alloc.Allocator. (Dcr Type) Bool)
(declare-fun PTR (Dcr Type) Type)
(declare-fun SLICE (Dcr Type) Type)
(declare-fun TYPE%alloc!vec.Vec. (Dcr Type Dcr Type) Type)
(declare-fun proj%core!ops.function.FnOnce./Output (Dcr Type Dcr Type) Type)
(declare-fun vstd!seq.Seq.len.? (Dcr Type Poly) Int)
(declare-fun req%vstd!seq.Seq.index. (Dcr Type Poly Poly) Bool)
(declare-fun %%global_location_label%%0 () Bool)
(declare-fun vstd!seq.Seq.index.? (Dcr Type Poly Poly) Poly)
(declare-fun req%vstd!seq.impl&%2.spec_index. (Dcr Type Poly Poly) Bool)
(declare-fun %%global_location_label%%1 () Bool)
(declare-fun vstd!seq.impl&%2.spec_index.? (Dcr Type Poly Poly) Poly)
(declare-fun closure_req (Type Dcr Type Poly Poly) Bool)
(declare-fun closure_ens (Type Dcr Type Poly Poly Poly) Bool)
(declare-fun vstd!slice.spec_slice_len.? (Dcr Type Poly) Int)
(declare-fun vstd!view.View.view.? (Dcr Type Poly) Poly)
(declare-fun vstd!slice.len%returns_clause_autospec.? (Dcr Type Poly) Int)
(declare-fun req%vstd!slice.SliceAdditionalSpecFns.spec_index.
             (Dcr Type Dcr Type Poly Poly)
             Bool)
(declare-fun %%global_location_label%%2 () Bool)
(declare-fun vstd!slice.SliceAdditionalSpecFns.spec_index.?
             (Dcr Type Dcr Type Poly Poly)
             Poly)
(declare-fun has_resolved (Dcr Type Poly) Bool)
(declare-fun vstd!raw_ptr.view_reverse_for_eq.? (Dcr Type Poly) Poly)
(declare-fun vstd!raw_ptr.view_reverse_for_eq_sized.? (Dcr Type Poly Poly) Poly)
(declare-fun vstd!std_specs.vec.spec_vec_len.? (Dcr Type Dcr Type Poly) Int)
(declare-fun ens%alloc!vec.impl&%29.as_ref. (Dcr Type Dcr Type Poly Poly) Bool)
(declare-fun ens%alloc!vec.impl&%31.as_ref. (Dcr Type Dcr Type Poly Poly) Bool)
(declare-fun ens%alloc!vec.impl&%30.as_mut. (Dcr Type Dcr Type Poly Poly) Bool)
(declare-fun ens%alloc!vec.impl&%32.as_mut. (Dcr Type Dcr Type Poly Poly) Bool)
(declare-fun lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
             (Dcr Type Poly Poly)
             Bool)
(declare-fun ens%lib!vec.borrowed.__specdet_6576671712930c59306307a6.
             (Dcr
              Type
              Dcr
              Type
              Bool
              Int
              Bool
              Int
              Int
              Bool
              Int
              Bool
              Int
              Int
              Bool
              Int
              Bool
              Int
              Int
              Bool
              Poly
              Poly
              Poly)
             Bool)
(declare-fun T&. () Dcr)
(declare-fun A&. () Dcr)
(declare-fun A& () Type)
(declare-fun k_vec_leneq! () Int)
(declare-fun k_vec_lenrng_lo! () Int)
(declare-fun k_vec_lenrng_hi! () Int)
(declare-fun k_r1_leneq! () Int)
(declare-fun k_r1_lenrng_lo! () Int)
(declare-fun k_r1_lenrng_hi! () Int)
(declare-fun k_r2_leneq! () Int)
(declare-fun k_r2_lenrng_lo! () Int)
(declare-fun k_r2_lenrng_hi! () Int)
(declare-fun T& () Type)
(declare-fun vec! () Poly)
(declare-fun r1! () Poly)
(declare-fun r2! () Poly)
(declare-fun %%location_label%%0 () Bool)
(declare-fun %%switch_label%%0 () Bool)
(declare-fun g_neq_tuple! () Bool)
(declare-fun %%switch_label%%1 () Bool)
(declare-fun g_r2_lenrng! () Bool)
(declare-fun %%switch_label%%2 () Bool)
(declare-fun g_r2_leneq! () Bool)
(declare-fun %%switch_label%%3 () Bool)
(declare-fun g_r1_lenrng! () Bool)
(declare-fun %%switch_label%%4 () Bool)
(declare-fun g_r1_leneq! () Bool)
(declare-fun %%switch_label%%5 () Bool)
(declare-fun g_vec_lenrng! () Bool)
(declare-fun %%switch_label%%6 () Bool)
(declare-fun g_vec_leneq! () Bool)
(assert (=> fuel_defaults
    (forall ((id FuelId))
      (! (= (fuel_bool id) (fuel_bool_default id))
         :pattern ((fuel_bool id))
         :skolemid skolem_prelude_fuel_defaults
         :qid prelude_fuel_defaults))))
(assert (forall ((m Poly) (arg Poly))
  (! (= (mut_ref_current% (mut_ref_update_current% m arg)) arg)
     :pattern ((mut_ref_update_current% m arg))
     :skolemid skolem_prelude_mut_ref_update_current_current
     :qid prelude_mut_ref_update_current_current)))
(assert (forall ((m Poly) (arg Poly))
  (! (= (mut_ref_future% (mut_ref_update_current% m arg)) (mut_ref_future% m))
     :pattern ((mut_ref_update_current% m arg))
     :skolemid skolem_prelude_mut_ref_update_current_future
     :qid prelude_mut_ref_update_current_future)))
(assert (forall ((m Poly) (d Dcr) (t Type))
  (! (=> (has_type m (MUTREF d t)) (has_type (mut_ref_current% m) t))
     :pattern ((has_type m (MUTREF d t)) (mut_ref_current% m))
     :skolemid skolem_prelude_mut_ref_current_has_type
     :qid prelude_mut_ref_current_has_type)))
(assert (forall ((m Poly) (d Dcr) (t Type))
  (! (=> (has_type m (MUTREF d t)) (has_type (mut_ref_future% m) t))
     :pattern ((has_type m (MUTREF d t)) (mut_ref_future% m))
     :skolemid skolem_prelude_mut_ref_future_has_type
     :qid prelude_mut_ref_future_has_type)))
(assert (forall ((m Poly) (d Dcr) (t Type) (arg Poly))
  (! (=> (and (has_type m (MUTREF d t)) (has_type arg t))
         (has_type (mut_ref_update_current% m arg) (MUTREF d t)))
     :pattern ((has_type m (MUTREF d t)) (mut_ref_update_current% m arg))
     :skolemid skolem_prelude_mut_ref_update_has_type
     :qid prelude_mut_ref_update_has_type)))
(assert (forall ((d Dcr))
  (! (=> (sized d) (sized (DST d)))
     :pattern ((sized (DST d)))
     :skolemid skolem_prelude_sized_decorate_struct_inherit
     :qid prelude_sized_decorate_struct_inherit)))
(assert (forall ((d Dcr))
  (! (sized (REF d))
     :pattern ((sized (REF d)))
     :skolemid skolem_prelude_sized_decorate_ref
     :qid prelude_sized_decorate_ref)))
(assert (forall ((d Dcr) (t Type) (d2 Dcr))
  (! (sized (BOX d t d2))
     :pattern ((sized (BOX d t d2)))
     :skolemid skolem_prelude_sized_decorate_box
     :qid prelude_sized_decorate_box)))
(assert (forall ((d Dcr) (t Type) (d2 Dcr))
  (! (sized (RC d t d2))
     :pattern ((sized (RC d t d2)))
     :skolemid skolem_prelude_sized_decorate_rc
     :qid prelude_sized_decorate_rc)))
(assert (forall ((d Dcr) (t Type) (d2 Dcr))
  (! (sized (ARC d t d2))
     :pattern ((sized (ARC d t d2)))
     :skolemid skolem_prelude_sized_decorate_arc
     :qid prelude_sized_decorate_arc)))
(assert (forall ((d Dcr))
  (! (sized (GHOST d))
     :pattern ((sized (GHOST d)))
     :skolemid skolem_prelude_sized_decorate_ghost
     :qid prelude_sized_decorate_ghost)))
(assert (forall ((d Dcr))
  (! (sized (TRACKED d))
     :pattern ((sized (TRACKED d)))
     :skolemid skolem_prelude_sized_decorate_tracked
     :qid prelude_sized_decorate_tracked)))
(assert (forall ((d Dcr))
  (! (sized (NEVER d))
     :pattern ((sized (NEVER d)))
     :skolemid skolem_prelude_sized_decorate_never
     :qid prelude_sized_decorate_never)))
(assert (forall ((d Dcr))
  (! (sized (CONST_PTR d))
     :pattern ((sized (CONST_PTR d)))
     :skolemid skolem_prelude_sized_decorate_const_ptr
     :qid prelude_sized_decorate_const_ptr)))
(assert (sized $))
(assert (forall ((i Int))
  (! (= i (const_int (CONST_INT i)))
     :pattern ((CONST_INT i))
     :skolemid skolem_prelude_type_id_const_int
     :qid prelude_type_id_const_int)))
(assert (forall ((b Bool))
  (! (= b (const_bool (CONST_BOOL b)))
     :pattern ((CONST_BOOL b))
     :skolemid skolem_prelude_type_id_const_bool
     :qid prelude_type_id_const_bool)))
(assert (forall ((b Bool))
  (! (has_type (B b) BOOL)
     :pattern ((has_type (B b) BOOL))
     :skolemid skolem_prelude_has_type_bool
     :qid prelude_has_type_bool)))
(assert (forall ((r Real))
  (! (has_type (R r) REAL)
     :pattern ((has_type (R r) REAL))
     :skolemid skolem_prelude_has_type_real
     :qid prelude_has_type_real)))
(assert (forall ((x Poly) (t Type))
  (! (and (has_type (as_type x t) t) (=> (has_type x t) (= x (as_type x t))))
     :pattern ((as_type x t))
     :skolemid skolem_prelude_as_type
     :qid prelude_as_type)))
(assert (forall ((x %%Function%%))
  (! (= (mk_fun x) x)
     :pattern ((mk_fun x))
     :skolemid skolem_prelude_mk_fun
     :qid prelude_mk_fun)))
(assert (forall ((x Bool))
  (! (= x (%B (B x)))
     :pattern ((B x))
     :skolemid skolem_prelude_unbox_box_bool
     :qid prelude_unbox_box_bool)))
(assert (forall ((x Int))
  (! (= x (%I (I x)))
     :pattern ((I x))
     :skolemid skolem_prelude_unbox_box_int
     :qid prelude_unbox_box_int)))
(assert (forall ((x Real))
  (! (= x (%R (R x)))
     :pattern ((R x))
     :skolemid skolem_prelude_unbox_box_real
     :qid prelude_unbox_box_real)))
(assert (forall ((x Poly))
  (! (=> (has_type x BOOL) (= x (B (%B x))))
     :pattern ((has_type x BOOL))
     :skolemid skolem_prelude_box_unbox_bool
     :qid prelude_box_unbox_bool)))
(assert (forall ((x Poly))
  (! (=> (has_type x INT) (= x (I (%I x))))
     :pattern ((has_type x INT))
     :skolemid skolem_prelude_box_unbox_int
     :qid prelude_box_unbox_int)))
(assert (forall ((x Poly))
  (! (=> (has_type x NAT) (= x (I (%I x))))
     :pattern ((has_type x NAT))
     :skolemid skolem_prelude_box_unbox_nat
     :qid prelude_box_unbox_nat)))
(assert (forall ((x Poly))
  (! (=> (has_type x USIZE) (= x (I (%I x))))
     :pattern ((has_type x USIZE))
     :skolemid skolem_prelude_box_unbox_usize
     :qid prelude_box_unbox_usize)))
(assert (forall ((x Poly))
  (! (=> (has_type x ISIZE) (= x (I (%I x))))
     :pattern ((has_type x ISIZE))
     :skolemid skolem_prelude_box_unbox_isize
     :qid prelude_box_unbox_isize)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (UINT bits)) (= x (I (%I x))))
     :pattern ((has_type x (UINT bits)))
     :skolemid skolem_prelude_box_unbox_uint
     :qid prelude_box_unbox_uint)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (SINT bits)) (= x (I (%I x))))
     :pattern ((has_type x (SINT bits)))
     :skolemid skolem_prelude_box_unbox_sint
     :qid prelude_box_unbox_sint)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (FLOAT bits)) (= x (I (%I x))))
     :pattern ((has_type x (FLOAT bits)))
     :skolemid skolem_prelude_box_unbox_float
     :qid prelude_box_unbox_float)))
(assert (forall ((x Poly))
  (! (=> (has_type x CHAR) (= x (I (%I x))))
     :pattern ((has_type x CHAR))
     :skolemid skolem_prelude_box_unbox_char
     :qid prelude_box_unbox_char)))
(assert (forall ((x Poly))
  (! (=> (has_type x REAL) (= x (R (%R x))))
     :pattern ((has_type x REAL))
     :skolemid skolem_prelude_box_unbox_real
     :qid prelude_box_unbox_real)))
(assert (forall ((deep Bool) (t Type) (x Poly) (y Poly))
  (! (= (= x y) (ext_eq deep t x y))
     :pattern ((ext_eq deep t x y))
     :skolemid skolem_prelude_ext_eq
     :qid prelude_ext_eq)))
(assert (or (= SZ 32) (= SZ 64)))
(assert (= (uHi 8) 256))
(assert (= (uHi 16) 65536))
(assert (= (uHi 32) 4294967296))
(assert (= (uHi 64) 18446744073709551616))
(assert (= (uHi 128) (+ 1 340282366920938463463374607431768211455)))
(assert (= (iLo 8) (- 128)))
(assert (= (iLo 16) (- 32768)))
(assert (= (iLo 32) (- 2147483648)))
(assert (= (iLo 64) (- 9223372036854775808)))
(assert (= (iLo 128) (- 170141183460469231731687303715884105728)))
(assert (= (iHi 8) 128))
(assert (= (iHi 16) 32768))
(assert (= (iHi 32) 2147483648))
(assert (= (iHi 64) 9223372036854775808))
(assert (= (iHi 128) 170141183460469231731687303715884105728))
(assert (forall ((i Int))
  (! (and (<= 0 (nClip i)) (=> (<= 0 i) (= i (nClip i))))
     :pattern ((nClip i))
     :skolemid skolem_prelude_nat_clip
     :qid prelude_nat_clip)))
(assert (forall ((bits Int) (i Int))
  (! (let ((a!1 (=> (and (<= 0 i) (< i (uHi bits))) (= i (uClip bits i)))))
       (and (<= 0 (uClip bits i)) (< (uClip bits i) (uHi bits)) a!1))
     :pattern ((uClip bits i))
     :skolemid skolem_prelude_u_clip
     :qid prelude_u_clip)))
(assert (forall ((bits Int) (i Int))
  (! (let ((a!1 (=> (and (<= (iLo bits) i) (< i (iHi bits)))
                    (= i (iClip bits i)))))
       (and (<= (iLo bits) (iClip bits i)) (< (iClip bits i) (iHi bits)) a!1))
     :pattern ((iClip bits i))
     :skolemid skolem_prelude_i_clip
     :qid prelude_i_clip)))
(assert (forall ((i Int))
  (! (let ((a!1 (or (and (<= 0 (charClip i)) (<= (charClip i) 55295))
                    (and (<= 57344 (charClip i)) (<= (charClip i) 1114111))))
           (a!2 (=> (or (and (<= 0 i) (<= i 55295))
                        (and (<= 57344 i) (<= i 1114111)))
                    (= i (charClip i)))))
       (and a!1 a!2))
     :pattern ((charClip i))
     :skolemid skolem_prelude_char_clip
     :qid prelude_char_clip)))
(assert (forall ((bits Int) (i Int))
  (! (= (uInv bits i) (and (<= 0 i) (< i (uHi bits))))
     :pattern ((uInv bits i))
     :skolemid skolem_prelude_u_inv
     :qid prelude_u_inv)))
(assert (forall ((bits Int) (i Int))
  (! (= (iInv bits i) (and (<= (iLo bits) i) (< i (iHi bits))))
     :pattern ((iInv bits i))
     :skolemid skolem_prelude_i_inv
     :qid prelude_i_inv)))
(assert (forall ((i Int))
  (! (= (charInv i)
        (or (and (<= 0 i) (<= i 55295)) (and (<= 57344 i) (<= i 1114111))))
     :pattern ((charInv i))
     :skolemid skolem_prelude_char_inv
     :qid prelude_char_inv)))
(assert (forall ((x Int))
  (! (has_type (I x) INT)
     :pattern ((has_type (I x) INT))
     :skolemid skolem_prelude_has_type_int
     :qid prelude_has_type_int)))
(assert (forall ((x Int))
  (! (=> (<= 0 x) (has_type (I x) NAT))
     :pattern ((has_type (I x) NAT))
     :skolemid skolem_prelude_has_type_nat
     :qid prelude_has_type_nat)))
(assert (forall ((x Int))
  (! (=> (uInv SZ x) (has_type (I x) USIZE))
     :pattern ((has_type (I x) USIZE))
     :skolemid skolem_prelude_has_type_usize
     :qid prelude_has_type_usize)))
(assert (forall ((x Int))
  (! (=> (iInv SZ x) (has_type (I x) ISIZE))
     :pattern ((has_type (I x) ISIZE))
     :skolemid skolem_prelude_has_type_isize
     :qid prelude_has_type_isize)))
(assert (forall ((bits Int) (x Int))
  (! (=> (uInv bits x) (has_type (I x) (UINT bits)))
     :pattern ((has_type (I x) (UINT bits)))
     :skolemid skolem_prelude_has_type_uint
     :qid prelude_has_type_uint)))
(assert (forall ((bits Int) (x Int))
  (! (=> (iInv bits x) (has_type (I x) (SINT bits)))
     :pattern ((has_type (I x) (SINT bits)))
     :skolemid skolem_prelude_has_type_sint
     :qid prelude_has_type_sint)))
(assert (forall ((bits Int) (x Int))
  (! (=> (uInv bits x) (has_type (I x) (FLOAT bits)))
     :pattern ((has_type (I x) (FLOAT bits)))
     :skolemid skolem_prelude_has_type_float
     :qid prelude_has_type_float)))
(assert (forall ((x Int))
  (! (=> (charInv x) (has_type (I x) CHAR))
     :pattern ((has_type (I x) CHAR))
     :skolemid skolem_prelude_has_type_char
     :qid prelude_has_type_char)))
(assert (forall ((x Poly))
  (! (=> (has_type x NAT) (<= 0 (%I x)))
     :pattern ((has_type x NAT))
     :skolemid skolem_prelude_unbox_int
     :qid prelude_unbox_int)))
(assert (forall ((x Poly))
  (! (=> (has_type x USIZE) (uInv SZ (%I x)))
     :pattern ((has_type x USIZE))
     :skolemid skolem_prelude_unbox_usize
     :qid prelude_unbox_usize)))
(assert (forall ((x Poly))
  (! (=> (has_type x CHAR) (charInv (%I x)))
     :pattern ((has_type x CHAR))
     :skolemid skolem_prelude_unbox_char
     :qid prelude_unbox_char)))
(assert (forall ((x Poly))
  (! (=> (has_type x ISIZE) (iInv SZ (%I x)))
     :pattern ((has_type x ISIZE))
     :skolemid skolem_prelude_unbox_isize
     :qid prelude_unbox_isize)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (UINT bits)) (uInv bits (%I x)))
     :pattern ((has_type x (UINT bits)))
     :skolemid skolem_prelude_unbox_uint
     :qid prelude_unbox_uint)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (SINT bits)) (iInv bits (%I x)))
     :pattern ((has_type x (SINT bits)))
     :skolemid skolem_prelude_unbox_sint
     :qid prelude_unbox_sint)))
(assert (forall ((bits Int) (x Poly))
  (! (=> (has_type x (FLOAT bits)) (uInv bits (%I x)))
     :pattern ((has_type x (FLOAT bits)))
     :skolemid skolem_prelude_unbox_float
     :qid prelude_unbox_float)))
(assert (forall ((x Int) (y Int))
  (! (= (Add x y) (+ x y))
     :pattern ((Add x y))
     :skolemid skolem_prelude_add
     :qid prelude_add)))
(assert (forall ((x Int) (y Int))
  (! (= (Sub x y) (- x y))
     :pattern ((Sub x y))
     :skolemid skolem_prelude_sub
     :qid prelude_sub)))
(assert (forall ((x Int) (y Int))
  (! (= (Mul x y) (* x y))
     :pattern ((Mul x y))
     :skolemid skolem_prelude_mul
     :qid prelude_mul)))
(assert (forall ((x Int) (y Int))
  (! (= (EucDiv x y) (div x y))
     :pattern ((EucDiv x y))
     :skolemid skolem_prelude_eucdiv
     :qid prelude_eucdiv)))
(assert (forall ((x Int) (y Int))
  (! (= (EucMod x y) (mod x y))
     :pattern ((EucMod x y))
     :skolemid skolem_prelude_eucmod
     :qid prelude_eucmod)))
(assert (forall ((x Real) (y Real))
  (! (= (RAdd x y) (+ x y))
     :pattern ((RAdd x y))
     :skolemid skolem_prelude_radd
     :qid prelude_radd)))
(assert (forall ((x Real) (y Real))
  (! (= (RSub x y) (- x y))
     :pattern ((RSub x y))
     :skolemid skolem_prelude_rsub
     :qid prelude_rsub)))
(assert (forall ((x Real) (y Real))
  (! (= (RMul x y) (* x y))
     :pattern ((RMul x y))
     :skolemid skolem_prelude_rmul
     :qid prelude_rmul)))
(assert (forall ((x Real) (y Real))
  (! (= (RDiv x y) (/ x y))
     :pattern ((RDiv x y))
     :skolemid skolem_prelude_rdiv
     :qid prelude_rdiv)))
(assert (forall ((x Int) (y Int))
  (! (=> (and (<= 0 x) (<= 0 y)) (<= 0 (Mul x y)))
     :pattern ((Mul x y))
     :skolemid skolem_prelude_mul_nats
     :qid prelude_mul_nats)))
(assert (forall ((x Int) (y Int))
  (! (=> (and (<= 0 x) (< 0 y)) (and (<= 0 (EucDiv x y)) (<= (EucDiv x y) x)))
     :pattern ((EucDiv x y))
     :skolemid skolem_prelude_div_unsigned_in_bounds
     :qid prelude_div_unsigned_in_bounds)))
(assert (forall ((x Int) (y Int))
  (! (=> (and (<= 0 x) (< 0 y)) (and (<= 0 (EucMod x y)) (< (EucMod x y) y)))
     :pattern ((EucMod x y))
     :skolemid skolem_prelude_mod_unsigned_in_bounds
     :qid prelude_mod_unsigned_in_bounds)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (uInv bits (%I x)) (uInv bits (%I y))) (uInv bits (bitxor x y)))
     :pattern ((uClip bits (bitxor x y)))
     :skolemid skolem_prelude_bit_xor_u_inv
     :qid prelude_bit_xor_u_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (iInv bits (%I x)) (iInv bits (%I y))) (iInv bits (bitxor x y)))
     :pattern ((iClip bits (bitxor x y)))
     :skolemid skolem_prelude_bit_xor_i_inv
     :qid prelude_bit_xor_i_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (uInv bits (%I x)) (uInv bits (%I y))) (uInv bits (bitor x y)))
     :pattern ((uClip bits (bitor x y)))
     :skolemid skolem_prelude_bit_or_u_inv
     :qid prelude_bit_or_u_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (iInv bits (%I x)) (iInv bits (%I y))) (iInv bits (bitor x y)))
     :pattern ((iClip bits (bitor x y)))
     :skolemid skolem_prelude_bit_or_i_inv
     :qid prelude_bit_or_i_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (uInv bits (%I x)) (uInv bits (%I y))) (uInv bits (bitand x y)))
     :pattern ((uClip bits (bitand x y)))
     :skolemid skolem_prelude_bit_and_u_inv
     :qid prelude_bit_and_u_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (iInv bits (%I x)) (iInv bits (%I y))) (iInv bits (bitand x y)))
     :pattern ((iClip bits (bitand x y)))
     :skolemid skolem_prelude_bit_and_i_inv
     :qid prelude_bit_and_i_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (uInv bits (%I x)) (<= 0 (%I y))) (uInv bits (bitshr x y)))
     :pattern ((uClip bits (bitshr x y)))
     :skolemid skolem_prelude_bit_shr_u_inv
     :qid prelude_bit_shr_u_inv)))
(assert (forall ((x Poly) (y Poly) (bits Int))
  (! (=> (and (iInv bits (%I x)) (<= 0 (%I y))) (iInv bits (bitshr x y)))
     :pattern ((iClip bits (bitshr x y)))
     :skolemid skolem_prelude_bit_shr_i_inv
     :qid prelude_bit_shr_i_inv)))
(assert (forall ((x Int) (y Int))
  (! (=> (not (= y 0)) (= (EucMod x y) (singular_mod x y)))
     :pattern ((singular_mod x y))
     :skolemid skolem_prelude_singularmod
     :qid prelude_singularmod)))
(assert (forall ((cur Poly) (prev Poly) (otherwise Bool))
  (! (let ((a!1 (or (height_lt (height cur) (height prev))
                    (and (= (height cur) (height prev)) otherwise))))
       (= (check_decrease_height cur prev otherwise) a!1))
     :pattern ((check_decrease_height cur prev otherwise))
     :skolemid skolem_prelude_check_decrease_height
     :qid prelude_check_decrease_height)))
(assert (forall ((cur Int) (prev Int))
  (! (= (height_lt (height (I cur)) (height (I prev)))
        (and (<= 0 cur) (< cur prev)))
     :pattern ((height_lt (height (I cur)) (height (I prev))))
     :skolemid skolem_prelude_check_decrease_int_height
     :qid prelude_check_decrease_int_height)))
(assert (forall ((x Height) (y Height))
  (! (= (height_lt x y) (and ((_ partial-order 0) x y) (not (= x y))))
     :pattern ((height_lt x y))
     :skolemid skolem_prelude_height_lt
     :qid prelude_height_lt)))
(assert (distinct fuel%vstd!std_specs.vec.axiom_spec_len.
          fuel%vstd!std_specs.vec.axiom_vec_has_resolved.
          fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view.
          fuel%vstd!function.axiom_fn_mut_call_requires.
          fuel%vstd!function.axiom_fn_mut_call_ensures.
          fuel%vstd!raw_ptr.impl&%3.view.
          fuel%vstd!raw_ptr.ptrs_mut_eq.
          fuel%vstd!raw_ptr.ptrs_mut_eq_sized.
          fuel%vstd!seq.impl&%2.spec_index.
          fuel%vstd!seq.lemma_seq_index_decreases.
          fuel%vstd!seq.lemma_seq_ext_equal.
          fuel%vstd!seq.lemma_seq_ext_equal_deep.
          fuel%vstd!slice.impl&%2.spec_index.
          fuel%vstd!slice.axiom_spec_len.
          fuel%vstd!slice.len%returns_clause_autospec.
          fuel%vstd!slice.axiom_slice_ext_equal.
          fuel%vstd!slice.axiom_slice_has_resolved.
          fuel%vstd!slice.axiom_slice_decreases_to_seq.
          fuel%vstd!slice.lemma_slice_index_decreases.
          fuel%vstd!view.impl&%0.view.
          fuel%vstd!view.impl&%2.view.
          fuel%vstd!view.impl&%4.view.
          fuel%vstd!view.impl&%6.view.
          fuel%vstd!view.impl&%16.view.
          fuel%vstd!view.impl&%18.view.
          fuel%vstd!view.impl&%30.view.
          fuel%lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.
          fuel%vstd!array.group_array_axioms.
          fuel%vstd!function.group_function_axioms.
          fuel%vstd!imap.group_imap_lemmas.
          fuel%vstd!iset.group_iset_lemmas.
          fuel%vstd!laws_cmp.group_laws_cmp.
          fuel%vstd!laws_eq.bool_laws.group_laws_eq.
          fuel%vstd!laws_eq.u8_laws.group_laws_eq.
          fuel%vstd!laws_eq.i8_laws.group_laws_eq.
          fuel%vstd!laws_eq.u16_laws.group_laws_eq.
          fuel%vstd!laws_eq.i16_laws.group_laws_eq.
          fuel%vstd!laws_eq.u32_laws.group_laws_eq.
          fuel%vstd!laws_eq.i32_laws.group_laws_eq.
          fuel%vstd!laws_eq.u64_laws.group_laws_eq.
          fuel%vstd!laws_eq.i64_laws.group_laws_eq.
          fuel%vstd!laws_eq.u128_laws.group_laws_eq.
          fuel%vstd!laws_eq.i128_laws.group_laws_eq.
          fuel%vstd!laws_eq.usize_laws.group_laws_eq.
          fuel%vstd!laws_eq.isize_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_1_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_2_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_3_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_4_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_5_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_6_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_7_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_8_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_9_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_10_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_11_laws.group_laws_eq.
          fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq.
          fuel%vstd!laws_eq.group_laws_eq.
          fuel%vstd!layout.group_align_properties.
          fuel%vstd!layout.group_layout_axioms.
          fuel%vstd!map.group_map_lemmas.
          fuel%vstd!multiset.group_multiset_axioms.
          fuel%vstd!mut_ref.group_mut_ref_axioms.
          fuel%vstd!raw_ptr.group_raw_ptr_axioms.
          fuel%vstd!seq.group_seq_lemmas.
          fuel%vstd!seq_lib.group_filter_ensures.
          fuel%vstd!seq_lib.group_seq_lib_default.
          fuel%vstd!set.group_set_lemmas.
          fuel%vstd!set_lib.group_set_lib_default.
          fuel%vstd!slice.group_slice_axioms.
          fuel%vstd!string.group_string_axioms.
          fuel%vstd!std_specs.bits.group_bits_axioms.
          fuel%vstd!std_specs.control_flow.group_control_flow_axioms.
          fuel%vstd!std_specs.fmt.group_fmt_axioms.
          fuel%vstd!std_specs.iter.group_iter_axioms.
          fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.
          fuel%vstd!std_specs.btree.group_btree_axioms.
          fuel%vstd!std_specs.hash.group_hash_axioms.
          fuel%vstd!std_specs.range.group_range_axioms.
          fuel%vstd!std_specs.vec.group_vec_axioms.
          fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms.
          fuel%vstd!std_specs.nonzero.group_nonzero_axioms.
          fuel%vstd!group_vstd_default.))
(assert (=> (fuel_bool_default fuel%vstd!function.group_function_axioms.)
    (and (fuel_bool_default fuel%vstd!function.axiom_fn_mut_call_requires.)
         (fuel_bool_default fuel%vstd!function.axiom_fn_mut_call_ensures.))))
(assert (=> (fuel_bool_default fuel%vstd!laws_eq.group_laws_eq.)
    (and (fuel_bool_default fuel%vstd!laws_eq.bool_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.u8_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.i8_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.u16_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.i16_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.u32_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.i32_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.u64_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.i64_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.u128_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.i128_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.usize_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.isize_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_1_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_2_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_3_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_4_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_5_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_6_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_7_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_8_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_9_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_10_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_11_laws.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq.))))
(assert (=> (fuel_bool_default fuel%vstd!layout.group_layout_axioms.)
    (fuel_bool_default fuel%vstd!layout.group_align_properties.)))
(assert (=> (fuel_bool_default fuel%vstd!raw_ptr.group_raw_ptr_axioms.)
    (and (fuel_bool_default fuel%vstd!raw_ptr.ptrs_mut_eq.)
         (fuel_bool_default fuel%vstd!raw_ptr.ptrs_mut_eq_sized.))))
(assert (=> (fuel_bool_default fuel%vstd!seq.group_seq_lemmas.)
    (and (fuel_bool_default fuel%vstd!seq.lemma_seq_index_decreases.)
         (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal.)
         (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal_deep.))))
(assert (=> (fuel_bool_default fuel%vstd!seq_lib.group_seq_lib_default.)
    (fuel_bool_default fuel%vstd!seq_lib.group_filter_ensures.)))
(assert (=> (fuel_bool_default fuel%vstd!slice.group_slice_axioms.)
    (and (fuel_bool_default fuel%vstd!slice.axiom_spec_len.)
         (fuel_bool_default fuel%vstd!slice.axiom_slice_ext_equal.)
         (fuel_bool_default fuel%vstd!slice.axiom_slice_has_resolved.)
         (fuel_bool_default fuel%vstd!slice.axiom_slice_decreases_to_seq.)
         (fuel_bool_default fuel%vstd!slice.lemma_slice_index_decreases.))))
(assert (=> (fuel_bool_default fuel%vstd!std_specs.vec.group_vec_axioms.)
    (and (fuel_bool_default fuel%vstd!std_specs.vec.axiom_spec_len.)
         (fuel_bool_default fuel%vstd!std_specs.vec.axiom_vec_has_resolved.)
         (fuel_bool_default
           fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view.))))
(assert (fuel_bool_default fuel%vstd!group_vstd_default.))
(assert (=> (fuel_bool_default fuel%vstd!group_vstd_default.)
    (and (fuel_bool_default fuel%vstd!seq.group_seq_lemmas.)
         (fuel_bool_default fuel%vstd!seq_lib.group_seq_lib_default.)
         (fuel_bool_default fuel%vstd!map.group_map_lemmas.)
         (fuel_bool_default fuel%vstd!set.group_set_lemmas.)
         (fuel_bool_default fuel%vstd!imap.group_imap_lemmas.)
         (fuel_bool_default fuel%vstd!iset.group_iset_lemmas.)
         (fuel_bool_default fuel%vstd!set_lib.group_set_lib_default.)
         (fuel_bool_default fuel%vstd!multiset.group_multiset_axioms.)
         (fuel_bool_default fuel%vstd!function.group_function_axioms.)
         (fuel_bool_default fuel%vstd!laws_eq.group_laws_eq.)
         (fuel_bool_default fuel%vstd!laws_cmp.group_laws_cmp.)
         (fuel_bool_default fuel%vstd!slice.group_slice_axioms.)
         (fuel_bool_default fuel%vstd!array.group_array_axioms.)
         (fuel_bool_default fuel%vstd!string.group_string_axioms.)
         (fuel_bool_default fuel%vstd!raw_ptr.group_raw_ptr_axioms.)
         (fuel_bool_default fuel%vstd!layout.group_layout_axioms.)
         (fuel_bool_default fuel%vstd!mut_ref.group_mut_ref_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.range.group_range_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.bits.group_bits_axioms.)
         (fuel_bool_default
           fuel%vstd!std_specs.control_flow.group_control_flow_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.fmt.group_fmt_axioms.)
         (fuel_bool_default
           fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.iter.group_iter_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.vec.group_vec_axioms.)
         (fuel_bool_default
           fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.hash.group_hash_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.btree.group_btree_axioms.)
         (fuel_bool_default fuel%vstd!std_specs.nonzero.group_nonzero_axioms.))))
(assert (forall ((d Dcr))
  (! (=> (sized d) (= (pointee_metadata% d) TYPE%tuple%0.))
     :pattern ((pointee_metadata% d))
     :skolemid skolem_prelude_project_pointee_metadata_sized
     :qid prelude_project_pointee_metadata_sized)))
(assert (forall ((d Dcr))
  (! (=> (sized d) (= (pointee_metadata%% d) $))
     :pattern ((pointee_metadata%% d))
     :skolemid skolem_prelude_project_pointee_metadata_decoration_sized
     :qid prelude_project_pointee_metadata_decoration_sized)))
(assert (= (pointee_metadata% $slice) USIZE))
(assert (= (pointee_metadata%% $slice) $))
(assert (forall ((d Dcr))
  (! (= (pointee_metadata% (DST d)) (pointee_metadata% d))
     :pattern ((pointee_metadata% (DST d)))
     :skolemid skolem_prelude_project_pointee_metadata_decorate_struct_inherit
     :qid prelude_project_pointee_metadata_decorate_struct_inherit)))
(assert (forall ((d Dcr))
  (! (= (pointee_metadata%% (DST d)) (pointee_metadata%% d))
     :pattern ((pointee_metadata%% (DST d)))
     :skolemid skolem_prelude_project_pointee_metadata_decoration_decorate_struct_inherit
     :qid prelude_project_pointee_metadata_decoration_decorate_struct_inherit)))
(assert (forall ((x alloc!alloc.Global.))
  (! (= x (%Poly%alloc!alloc.Global. (Poly%alloc!alloc.Global. x)))
     :pattern ((Poly%alloc!alloc.Global. x))
     :skolemid skolem_internal_alloc__alloc__Global_box_axiom_definition
     :qid internal_alloc__alloc__Global_box_axiom_definition)))
(assert (forall ((x Poly))
  (! (=> (has_type x TYPE%alloc!alloc.Global.)
         (= x (Poly%alloc!alloc.Global. (%Poly%alloc!alloc.Global. x))))
     :pattern ((has_type x TYPE%alloc!alloc.Global.))
     :skolemid skolem_internal_alloc__alloc__Global_unbox_axiom_definition
     :qid internal_alloc__alloc__Global_unbox_axiom_definition)))
(assert (forall ((x alloc!alloc.Global.))
  (! (has_type (Poly%alloc!alloc.Global. x) TYPE%alloc!alloc.Global.)
     :pattern ((has_type (Poly%alloc!alloc.Global. x) TYPE%alloc!alloc.Global.))
     :skolemid skolem_internal_alloc__alloc__Global_has_type_always_definition
     :qid internal_alloc__alloc__Global_has_type_always_definition)))
(assert (forall ((x vstd!raw_ptr.Provenance.))
  (! (= x (%Poly%vstd!raw_ptr.Provenance. (Poly%vstd!raw_ptr.Provenance. x)))
     :pattern ((Poly%vstd!raw_ptr.Provenance. x))
     :skolemid skolem_internal_vstd__raw_ptr__Provenance_box_axiom_definition
     :qid internal_vstd__raw_ptr__Provenance_box_axiom_definition)))
(assert (forall ((x Poly))
  (! (=> (has_type x TYPE%vstd!raw_ptr.Provenance.)
         (= x
            (Poly%vstd!raw_ptr.Provenance. (%Poly%vstd!raw_ptr.Provenance. x))))
     :pattern ((has_type x TYPE%vstd!raw_ptr.Provenance.))
     :skolemid skolem_internal_vstd__raw_ptr__Provenance_unbox_axiom_definition
     :qid internal_vstd__raw_ptr__Provenance_unbox_axiom_definition)))
(assert (forall ((x vstd!raw_ptr.Provenance.))
  (! (has_type (Poly%vstd!raw_ptr.Provenance. x) TYPE%vstd!raw_ptr.Provenance.)
     :pattern ((has_type (Poly%vstd!raw_ptr.Provenance. x)
                         TYPE%vstd!raw_ptr.Provenance.))
     :skolemid skolem_internal_vstd__raw_ptr__Provenance_has_type_always_definition
     :qid internal_vstd__raw_ptr__Provenance_has_type_always_definition)))
(assert (forall ((x vstd!raw_ptr.PtrData.))
  (! (= x (%Poly%vstd!raw_ptr.PtrData. (Poly%vstd!raw_ptr.PtrData. x)))
     :pattern ((Poly%vstd!raw_ptr.PtrData. x))
     :skolemid skolem_internal_vstd__raw_ptr__PtrData_box_axiom_definition
     :qid internal_vstd__raw_ptr__PtrData_box_axiom_definition)))
(assert (forall ((T&. Dcr) (T& Type) (x Poly))
  (! (=> (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
         (= x (Poly%vstd!raw_ptr.PtrData. (%Poly%vstd!raw_ptr.PtrData. x))))
     :pattern ((has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
     :skolemid skolem_internal_vstd__raw_ptr__PtrData_unbox_axiom_definition
     :qid internal_vstd__raw_ptr__PtrData_unbox_axiom_definition)))
(assert (forall ((T&. Dcr)
         (T& Type)
         (_addr! Int)
         (_provenance! vstd!raw_ptr.Provenance.)
         (_metadata! Poly))
  (! (=> (and (uInv SZ _addr!) (has_type _metadata! (pointee_metadata% T&.)))
         (has_type (Poly%vstd!raw_ptr.PtrData.
                     (vstd!raw_ptr.PtrData./PtrData
                       _addr!
                       _provenance!
                       _metadata!))
                   (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
     :pattern ((has_type (Poly%vstd!raw_ptr.PtrData.
                           (vstd!raw_ptr.PtrData./PtrData
                             _addr!
                             _provenance!
                             _metadata!))
                         (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData_constructor_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData_constructor_definition)))
(assert (forall ((x vstd!raw_ptr.PtrData.))
  (! (= (vstd!raw_ptr.PtrData./PtrData/addr x)
        (vstd!raw_ptr.PtrData./PtrData/?addr x))
     :pattern ((vstd!raw_ptr.PtrData./PtrData/addr x))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/addr_accessor_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData/addr_accessor_definition)))
(assert (forall ((T&. Dcr) (T& Type) (x Poly))
  (! (=> (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
         (uInv SZ
               (vstd!raw_ptr.PtrData./PtrData/addr
                 (%Poly%vstd!raw_ptr.PtrData. x))))
     :pattern ((vstd!raw_ptr.PtrData./PtrData/addr
                 (%Poly%vstd!raw_ptr.PtrData. x))
               (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/addr_invariant_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData/addr_invariant_definition)))
(assert (forall ((x vstd!raw_ptr.PtrData.))
  (! (= (vstd!raw_ptr.PtrData./PtrData/provenance x)
        (vstd!raw_ptr.PtrData./PtrData/?provenance x))
     :pattern ((vstd!raw_ptr.PtrData./PtrData/provenance x))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/provenance_accessor_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData/provenance_accessor_definition)))
(assert (forall ((x vstd!raw_ptr.PtrData.))
  (! (= (vstd!raw_ptr.PtrData./PtrData/metadata x)
        (vstd!raw_ptr.PtrData./PtrData/?metadata x))
     :pattern ((vstd!raw_ptr.PtrData./PtrData/metadata x))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/metadata_accessor_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData/metadata_accessor_definition)))
(assert (forall ((T&. Dcr) (T& Type) (x Poly))
  (! (=> (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
         (has_type (vstd!raw_ptr.PtrData./PtrData/metadata
                     (%Poly%vstd!raw_ptr.PtrData. x))
                   (pointee_metadata% T&.)))
     :pattern ((vstd!raw_ptr.PtrData./PtrData/metadata
                 (%Poly%vstd!raw_ptr.PtrData. x))
               (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
     :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/metadata_invariant_definition
     :qid internal_vstd!raw_ptr.PtrData./PtrData/metadata_invariant_definition)))
(assert (forall ((x tuple%0.))
  (! (= x (%Poly%tuple%0. (Poly%tuple%0. x)))
     :pattern ((Poly%tuple%0. x))
     :skolemid skolem_internal_crate__tuple__0_box_axiom_definition
     :qid internal_crate__tuple__0_box_axiom_definition)))
(assert (forall ((x Poly))
  (! (=> (has_type x TYPE%tuple%0.) (= x (Poly%tuple%0. (%Poly%tuple%0. x))))
     :pattern ((has_type x TYPE%tuple%0.))
     :skolemid skolem_internal_crate__tuple__0_unbox_axiom_definition
     :qid internal_crate__tuple__0_unbox_axiom_definition)))
(assert (forall ((x tuple%0.))
  (! (has_type (Poly%tuple%0. x) TYPE%tuple%0.)
     :pattern ((has_type (Poly%tuple%0. x) TYPE%tuple%0.))
     :skolemid skolem_internal_crate__tuple__0_has_type_always_definition
     :qid internal_crate__tuple__0_has_type_always_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type))
  (! (=> (tr_bound%vstd!slice.SliceAdditionalSpecFns. Self%&. Self%& T&. T&)
         (and (tr_bound%vstd!view.View. Self%&. Self%&)
              (= $ (proj%%vstd!view.View./V Self%&. Self%&))
              (= (TYPE%vstd!seq.Seq. T&. T&)
                 (proj%vstd!view.View./V Self%&. Self%&))
              (sized T&.)))
     :pattern ((tr_bound%vstd!slice.SliceAdditionalSpecFns.
                 Self%&.
                 Self%&
                 T&.
                 T&))
     :skolemid skolem_internal_vstd__slice__SliceAdditionalSpecFns_trait_type_bounds_definition
     :qid internal_vstd__slice__SliceAdditionalSpecFns_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type))
  (! (=> (tr_bound%vstd!view.View. Self%&. Self%&)
         (sized (proj%%vstd!view.View./V Self%&. Self%&)))
     :pattern ((tr_bound%vstd!view.View. Self%&. Self%&))
     :skolemid skolem_internal_vstd__view__View_trait_type_bounds_definition
     :qid internal_vstd__view__View_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type))
  (! true
     :pattern ((tr_bound%core!marker.Tuple. Self%&. Self%&))
     :skolemid skolem_internal_core__marker__Tuple_trait_type_bounds_definition
     :qid internal_core__marker__Tuple_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type))
  (! (=> (tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&)
         (and (sized Args&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (sized (proj%%core!ops.function.FnOnce./Output
                       Self%&.
                       Self%&
                       Args&.
                       Args&))))
     :pattern ((tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&))
     :skolemid skolem_internal_core__ops__function__FnOnce_trait_type_bounds_definition
     :qid internal_core__ops__function__FnOnce_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type))
  (! (=> (tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&)
         (and (tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&)
              (sized Args&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)))
     :pattern ((tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&))
     :skolemid skolem_internal_core__ops__function__FnMut_trait_type_bounds_definition
     :qid internal_core__ops__function__FnMut_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type))
  (! (=> (tr_bound%core!ops.function.Fn. Self%&. Self%& Args&. Args&)
         (and (tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&)
              (sized Args&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)))
     :pattern ((tr_bound%core!ops.function.Fn. Self%&. Self%& Args&. Args&))
     :skolemid skolem_internal_core__ops__function__Fn_trait_type_bounds_definition
     :qid internal_core__ops__function__Fn_trait_type_bounds_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type))
  (! true
     :pattern ((tr_bound%core!alloc.Allocator. Self%&. Self%&))
     :skolemid skolem_internal_core__alloc__Allocator_trait_type_bounds_definition
     :qid internal_core__alloc__Allocator_trait_type_bounds_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (= (proj%%vstd!view.View./V $ (PTR T&. T&)) $)
     :pattern ((proj%%vstd!view.View./V $ (PTR T&. T&)))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_true_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (= (proj%vstd!view.View./V $ (PTR T&. T&))
        (TYPE%vstd!raw_ptr.PtrData. T&. T&))
     :pattern ((proj%vstd!view.View./V $ (PTR T&. T&)))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_false_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (= (proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)) $)
     :pattern ((proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_true_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (= (proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&))
        (TYPE%vstd!raw_ptr.PtrData. T&. T&))
     :pattern ((proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_false_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (=> (sized T&.) (= (proj%%vstd!view.View./V $slice (SLICE T&. T&)) $))
     :pattern ((proj%%vstd!view.View./V $slice (SLICE T&. T&)))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_true_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (=> (sized T&.)
         (= (proj%vstd!view.View./V $slice (SLICE T&. T&))
            (TYPE%vstd!seq.Seq. T&. T&)))
     :pattern ((proj%vstd!view.View./V $slice (SLICE T&. T&)))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (= (proj%%vstd!view.View./V (REF A&.) A&)
            (proj%%vstd!view.View./V A&. A&)))
     :pattern ((proj%%vstd!view.View./V (REF A&.) A&))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (= (proj%vstd!view.View./V (REF A&.) A&)
            (proj%vstd!view.View./V A&. A&)))
     :pattern ((proj%vstd!view.View./V (REF A&.) A&))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (= (proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%%vstd!view.View./V A&. A&)))
     :pattern ((proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (= (proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%vstd!view.View./V A&. A&)))
     :pattern ((proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (= (proj%%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%%vstd!view.View./V A&. A&)))
     :pattern ((proj%%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (= (proj%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%vstd!view.View./V A&. A&)))
     :pattern ((proj%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (= (proj%%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%%vstd!view.View./V A&. A&)))
     :pattern ((proj%%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (= (proj%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&)
            (proj%vstd!view.View./V A&. A&)))
     :pattern ((proj%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_false_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized T&.) (sized A&.) (tr_bound%core!alloc.Allocator. A&. A&))
         (= (proj%%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)) $))
     :pattern ((proj%%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
     :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_true_definition
     :qid internal_proj____vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_true_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized T&.) (sized A&.) (tr_bound%core!alloc.Allocator. A&. A&))
         (= (proj%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&))
            (TYPE%vstd!seq.Seq. T&. T&)))
     :pattern ((proj%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
     :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_false_definition
     :qid internal_proj__vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_false_definition)))
(assert (= (proj%%vstd!view.View./V $ TYPE%tuple%0.) $))
(assert (= (proj%vstd!view.View./V $ TYPE%tuple%0.) TYPE%tuple%0.))
(assert (= (proj%%vstd!view.View./V $ BOOL) $))
(assert (= (proj%vstd!view.View./V $ BOOL) BOOL))
(assert (= (proj%%vstd!view.View./V $ USIZE) $))
(assert (= (proj%vstd!view.View./V $ USIZE) USIZE))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.Fn. F&. F& A&. A&))
         (= (proj%%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&)
            (proj%%core!ops.function.FnOnce./Output F&. F& A&. A&)))
     :pattern ((proj%%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&))
     :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_true_definition
     :qid internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.Fn. F&. F& A&. A&))
         (= (proj%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&)
            (proj%core!ops.function.FnOnce./Output F&. F& A&. A&)))
     :pattern ((proj%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&))
     :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_false_definition
     :qid internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.FnMut. F&. F& A&. A&))
         (= (proj%%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&)
            (proj%%core!ops.function.FnOnce./Output F&. F& A&. A&)))
     :pattern ((proj%%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&))
     :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_true_definition
     :qid internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_true_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.FnMut. F&. F& A&. A&))
         (= (proj%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&)
            (proj%core!ops.function.FnOnce./Output F&. F& A&. A&)))
     :pattern ((proj%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&))
     :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_false_definition
     :qid internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_false_definition)))
(assert (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized Args&.)
              (sized A&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (= (proj%%core!ops.function.FnOnce./Output
              (BOX A&. A& F&.)
              F&
              Args&.
              Args&)
            (proj%%core!ops.function.FnOnce./Output F&. F& Args&. Args&)))
     :pattern ((proj%%core!ops.function.FnOnce./Output
                 (BOX A&. A& F&.)
                 F&
                 Args&.
                 Args&))
     :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_true_definition
     :qid internal_proj____core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_true_definition)))
(assert (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized Args&.)
              (sized A&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (= (proj%core!ops.function.FnOnce./Output
              (BOX A&. A& F&.)
              F&
              Args&.
              Args&)
            (proj%core!ops.function.FnOnce./Output F&. F& Args&. Args&)))
     :pattern ((proj%core!ops.function.FnOnce./Output
                 (BOX A&. A& F&.)
                 F&
                 Args&.
                 Args&))
     :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_false_definition
     :qid internal_proj__core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_false_definition)))
(assert (forall ((A&. Dcr) (A& Type) (self! Poly))
  (! (=> (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
         (<= 0 (vstd!seq.Seq.len.? A&. A& self!)))
     :pattern ((vstd!seq.Seq.len.? A&. A& self!))
     :skolemid skolem_internal_vstd!seq.Seq.len.?_pre_post_definition
     :qid internal_vstd!seq.Seq.len.?_pre_post_definition)))
(assert (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly))
  (! (let ((a!1 (=> %%global_location_label%%0
                    (and (<= 0 (%I i!))
                         (< (%I i!) (vstd!seq.Seq.len.? A&. A& self!))))))
       (= (req%vstd!seq.Seq.index. A&. A& self! i!) a!1))
     :pattern ((req%vstd!seq.Seq.index. A&. A& self! i!))
     :skolemid skolem_internal_req__vstd!seq.Seq.index._definition
     :qid internal_req__vstd!seq.Seq.index._definition)))
(assert (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly))
  (! (=> (and (has_type self! (TYPE%vstd!seq.Seq. A&. A&)) (has_type i! INT))
         (has_type (vstd!seq.Seq.index.? A&. A& self! i!) A&))
     :pattern ((vstd!seq.Seq.index.? A&. A& self! i!))
     :skolemid skolem_internal_vstd!seq.Seq.index.?_pre_post_definition
     :qid internal_vstd!seq.Seq.index.?_pre_post_definition)))
(assert (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly))
  (! (let ((a!1 (=> %%global_location_label%%1
                    (and (<= 0 (%I i!))
                         (< (%I i!) (vstd!seq.Seq.len.? A&. A& self!))))))
       (= (req%vstd!seq.impl&%2.spec_index. A&. A& self! i!) a!1))
     :pattern ((req%vstd!seq.impl&%2.spec_index. A&. A& self! i!))
     :skolemid skolem_internal_req__vstd!seq.impl&__2.spec_index._definition
     :qid internal_req__vstd!seq.impl&__2.spec_index._definition)))
(assert (fuel_bool_default fuel%vstd!seq.impl&%2.spec_index.))
(assert (=> (fuel_bool fuel%vstd!seq.impl&%2.spec_index.)
    (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly))
      (! (= (vstd!seq.impl&%2.spec_index.? A&. A& self! i!)
            (vstd!seq.Seq.index.? A&. A& self! i!))
         :pattern ((vstd!seq.impl&%2.spec_index.? A&. A& self! i!))
         :skolemid skolem_internal_vstd!seq.impl&__2.spec_index.?_definition
         :qid internal_vstd!seq.impl&__2.spec_index.?_definition))))
(assert (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly))
  (! (=> (and (has_type self! (TYPE%vstd!seq.Seq. A&. A&)) (has_type i! INT))
         (has_type (vstd!seq.impl&%2.spec_index.? A&. A& self! i!) A&))
     :pattern ((vstd!seq.impl&%2.spec_index.? A&. A& self! i!))
     :skolemid skolem_internal_vstd!seq.impl&__2.spec_index.?_pre_post_definition
     :qid internal_vstd!seq.impl&__2.spec_index.?_pre_post_definition)))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (s! Poly) (i! Poly))
             (! (let ((a!1 (=> (and (sized A&.)
                                    (<= 0 (%I i!))
                                    (< (%I i!) (vstd!seq.Seq.len.? A&. A& s!)))
                               (height_lt (height (vstd!seq.Seq.index.?
                                                    A&.
                                                    A&
                                                    s!
                                                    i!))
                                          (height s!)))))
                  (=> (and (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
                           (has_type i! INT))
                      a!1))
                :pattern ((height (vstd!seq.Seq.index.? A&. A& s! i!)))
                :skolemid skolem_user_vstd__seq__lemma_seq_index_decreases_0
                :qid user_vstd__seq__lemma_seq_index_decreases_0))))
  (=> (fuel_bool fuel%vstd!seq.lemma_seq_index_decreases.) a!1)))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly))
             (! (let ((a!1 (and (= (vstd!seq.Seq.len.? A&. A& s1!)
                                   (vstd!seq.Seq.len.? A&. A& s2!))
                                (forall ((i$ Poly))
                                  (! (let ((a!1 (=> (and (<= 0 (%I i$))
                                                         (< (%I i$)
                                                            (vstd!seq.Seq.len.?
                                                              A&.
                                                              A&
                                                              s1!)))
                                                    (= (vstd!seq.Seq.index.?
                                                         A&.
                                                         A&
                                                         s1!
                                                         i$)
                                                       (vstd!seq.Seq.index.?
                                                         A&.
                                                         A&
                                                         s2!
                                                         i$)))))
                                       (=> (has_type i$ INT) a!1))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 A&.
                                                 A&
                                                 s1!
                                                 i$))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 A&.
                                                 A&
                                                 s2!
                                                 i$))
                                     :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_0
                                     :qid user_vstd__seq__lemma_seq_ext_equal_0)))))
                (let ((a!2 (=> (sized A&.)
                               (= (ext_eq false
                                          (TYPE%vstd!seq.Seq. A&. A&)
                                          s1!
                                          s2!)
                                  a!1))))
                  (=> (and (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
                           (has_type s2! (TYPE%vstd!seq.Seq. A&. A&)))
                      a!2)))
                :pattern ((ext_eq false (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
                :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_1
                :qid user_vstd__seq__lemma_seq_ext_equal_1))))
  (=> (fuel_bool fuel%vstd!seq.lemma_seq_ext_equal.) a!1)))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly))
             (! (let ((a!1 (and (= (vstd!seq.Seq.len.? A&. A& s1!)
                                   (vstd!seq.Seq.len.? A&. A& s2!))
                                (forall ((i$ Poly))
                                  (! (let ((a!1 (=> (and (<= 0 (%I i$))
                                                         (< (%I i$)
                                                            (vstd!seq.Seq.len.?
                                                              A&.
                                                              A&
                                                              s1!)))
                                                    (ext_eq true
                                                            A&
                                                            (vstd!seq.Seq.index.?
                                                              A&.
                                                              A&
                                                              s1!
                                                              i$)
                                                            (vstd!seq.Seq.index.?
                                                              A&.
                                                              A&
                                                              s2!
                                                              i$)))))
                                       (=> (has_type i$ INT) a!1))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 A&.
                                                 A&
                                                 s1!
                                                 i$))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 A&.
                                                 A&
                                                 s2!
                                                 i$))
                                     :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_0
                                     :qid user_vstd__seq__lemma_seq_ext_equal_deep_0)))))
                (let ((a!2 (=> (sized A&.)
                               (= (ext_eq true
                                          (TYPE%vstd!seq.Seq. A&. A&)
                                          s1!
                                          s2!)
                                  a!1))))
                  (=> (and (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
                           (has_type s2! (TYPE%vstd!seq.Seq. A&. A&)))
                      a!2)))
                :pattern ((ext_eq true (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
                :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_1
                :qid user_vstd__seq__lemma_seq_ext_equal_deep_1))))
  (=> (fuel_bool fuel%vstd!seq.lemma_seq_ext_equal_deep.) a!1)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.FnMut. F&. F& A&. A&))
         (tr_bound%core!ops.function.FnOnce. $ (MUTREF F&. F&) A&. A&))
     :pattern ((tr_bound%core!ops.function.FnOnce. $ (MUTREF F&. F&) A&. A&))
     :skolemid skolem_internal_core__ops__function__impls__impl&__4_trait_impl_definition
     :qid internal_core__ops__function__impls__impl&__4_trait_impl_definition)))
(assert (let ((a!1 (forall ((Args&. Dcr)
                    (Args& Type)
                    (F&. Dcr)
                    (F& Type)
                    (f! Poly)
                    (args! Poly))
             (! (let ((a!1 (=> (and (sized Args&.)
                                    (sized F&.)
                                    (tr_bound%core!marker.Tuple. Args&. Args&)
                                    (tr_bound%core!ops.function.FnMut.
                                      F&.
                                      F&
                                      Args&.
                                      Args&)
                                    (closure_req F&
                                                 Args&.
                                                 Args&
                                                 (mut_ref_current% f!)
                                                 args!))
                               (closure_req (MUTREF F&. F&)
                                            Args&.
                                            Args&
                                            f!
                                            args!))))
                  (=> (and (has_type f! (MUTREF F&. F&)) (has_type args! Args&))
                      a!1))
                :pattern ((closure_req (MUTREF F&. F&) Args&. Args& f! args!))
                :skolemid skolem_user_vstd__function__axiom_fn_mut_call_requires_0
                :qid user_vstd__function__axiom_fn_mut_call_requires_0))))
  (=> (fuel_bool fuel%vstd!function.axiom_fn_mut_call_requires.) a!1)))
(assert (let ((a!1 (forall ((Args&. Dcr)
                    (Args& Type)
                    (F&. Dcr)
                    (F& Type)
                    (f! Poly)
                    (args! Poly)
                    (output! Poly))
             (! (let ((a!1 (=> (and (sized Args&.)
                                    (sized F&.)
                                    (tr_bound%core!marker.Tuple. Args&. Args&)
                                    (tr_bound%core!ops.function.FnMut.
                                      F&.
                                      F&
                                      Args&.
                                      Args&)
                                    (closure_ens (MUTREF F&. F&)
                                                 Args&.
                                                 Args&
                                                 f!
                                                 args!
                                                 output!))
                               (and (closure_ens F&
                                                 Args&.
                                                 Args&
                                                 (mut_ref_current% f!)
                                                 args!
                                                 output!)
                                    (= (mut_ref_current% f!)
                                       (mut_ref_future% f!))))))
                  (=> (and (has_type f! (MUTREF F&. F&))
                           (has_type args! Args&)
                           (has_type output!
                                     (proj%core!ops.function.FnOnce./Output
                                       F&.
                                       F&
                                       Args&.
                                       Args&)))
                      a!1))
                :pattern ((closure_ens (MUTREF F&. F&)
                                       Args&.
                                       Args&
                                       f!
                                       args!
                                       output!))
                :skolemid skolem_user_vstd__function__axiom_fn_mut_call_ensures_0
                :qid user_vstd__function__axiom_fn_mut_call_ensures_0))))
  (=> (fuel_bool fuel%vstd!function.axiom_fn_mut_call_ensures.) a!1)))
(assert (forall ((T&. Dcr) (T& Type) (slice! Poly))
  (! (=> (has_type slice! (SLICE T&. T&))
         (uInv SZ (vstd!slice.spec_slice_len.? T&. T& slice!)))
     :pattern ((vstd!slice.spec_slice_len.? T&. T& slice!))
     :skolemid skolem_internal_vstd!slice.spec_slice_len.?_pre_post_definition
     :qid internal_vstd!slice.spec_slice_len.?_pre_post_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (self! Poly))
  (! (=> (has_type self! Self%&)
         (has_type (vstd!view.View.view.? Self%&. Self%& self!)
                   (proj%vstd!view.View./V Self%&. Self%&)))
     :pattern ((vstd!view.View.view.? Self%&. Self%& self!))
     :skolemid skolem_internal_vstd!view.View.view.?_pre_post_definition
     :qid internal_vstd!view.View.view.?_pre_post_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (=> (sized T&.) (tr_bound%vstd!view.View. $slice (SLICE T&. T&)))
     :pattern ((tr_bound%vstd!view.View. $slice (SLICE T&. T&)))
     :skolemid skolem_internal_vstd__slice__impl&__0_trait_impl_definition
     :qid internal_vstd__slice__impl&__0_trait_impl_definition)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (slice! Poly))
             (! (let ((a!1 (= (vstd!slice.spec_slice_len.? T&. T& slice!)
                              (vstd!seq.Seq.len.?
                                T&.
                                T&
                                (vstd!view.View.view.?
                                  $slice
                                  (SLICE T&. T&)
                                  slice!)))))
                  (=> (has_type slice! (SLICE T&. T&)) (=> (sized T&.) a!1)))
                :pattern ((vstd!slice.spec_slice_len.? T&. T& slice!))
                :skolemid skolem_user_vstd__slice__axiom_spec_len_0
                :qid user_vstd__slice__axiom_spec_len_0))))
  (=> (fuel_bool fuel%vstd!slice.axiom_spec_len.) a!1)))
(assert (fuel_bool_default fuel%vstd!slice.len%returns_clause_autospec.))
(assert (=> (fuel_bool fuel%vstd!slice.len%returns_clause_autospec.)
    (forall ((T&. Dcr) (T& Type) (slice! Poly))
      (! (= (vstd!slice.len%returns_clause_autospec.? T&. T& slice!)
            (vstd!slice.spec_slice_len.? T&. T& slice!))
         :pattern ((vstd!slice.len%returns_clause_autospec.? T&. T& slice!))
         :skolemid skolem_internal_vstd!slice.len__returns_clause_autospec.?_definition
         :qid internal_vstd!slice.len__returns_clause_autospec.?_definition))))
(assert (forall ((T&. Dcr) (T& Type) (slice! Poly))
  (! (=> (has_type slice! (SLICE T&. T&))
         (uInv SZ (vstd!slice.len%returns_clause_autospec.? T&. T& slice!)))
     :pattern ((vstd!slice.len%returns_clause_autospec.? T&. T& slice!))
     :skolemid skolem_internal_vstd!slice.len__returns_clause_autospec.?_pre_post_definition
     :qid internal_vstd!slice.len__returns_clause_autospec.?_pre_post_definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly))
  (! (let ((a!1 (and (<= 0 (%I i!))
                     (< (%I i!)
                        (vstd!seq.Seq.len.?
                          T&.
                          T&
                          (vstd!view.View.view.? Self%&. Self%& self!))))))
       (= (req%vstd!slice.SliceAdditionalSpecFns.spec_index.
            Self%&.
            Self%&
            T&.
            T&
            self!
            i!)
          (=> %%global_location_label%%2 a!1)))
     :pattern ((req%vstd!slice.SliceAdditionalSpecFns.spec_index.
                 Self%&.
                 Self%&
                 T&.
                 T&
                 self!
                 i!))
     :skolemid skolem_internal_req__vstd!slice.SliceAdditionalSpecFns.spec_index._definition
     :qid internal_req__vstd!slice.SliceAdditionalSpecFns.spec_index._definition)))
(assert (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly))
  (! (=> (and (has_type self! Self%&) (has_type i! INT))
         (has_type (vstd!slice.SliceAdditionalSpecFns.spec_index.?
                     Self%&.
                     Self%&
                     T&.
                     T&
                     self!
                     i!)
                   T&))
     :pattern ((vstd!slice.SliceAdditionalSpecFns.spec_index.?
                 Self%&.
                 Self%&
                 T&.
                 T&
                 self!
                 i!))
     :skolemid skolem_internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_pre_post_definition
     :qid internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_pre_post_definition)))
(assert (fuel_bool_default fuel%vstd!slice.impl&%2.spec_index.))
(assert (=> (fuel_bool fuel%vstd!slice.impl&%2.spec_index.)
    (forall ((T&. Dcr) (T& Type) (self! Poly) (i! Poly))
      (! (let ((a!1 (= (vstd!slice.SliceAdditionalSpecFns.spec_index.?
                         $slice
                         (SLICE T&. T&)
                         T&.
                         T&
                         self!
                         i!)
                       (vstd!seq.Seq.index.?
                         T&.
                         T&
                         (vstd!view.View.view.? $slice (SLICE T&. T&) self!)
                         i!))))
           (=> (sized T&.) a!1))
         :pattern ((vstd!slice.SliceAdditionalSpecFns.spec_index.?
                     $slice
                     (SLICE T&. T&)
                     T&.
                     T&
                     self!
                     i!))
         :skolemid skolem_internal_vstd!slice.impl&__2.spec_index.?_definition
         :qid internal_vstd!slice.impl&__2.spec_index.?_definition))))
(assert (forall ((T&. Dcr) (T& Type))
  (! (=> (sized T&.)
         (tr_bound%vstd!slice.SliceAdditionalSpecFns.
           $slice
           (SLICE T&. T&)
           T&.
           T&))
     :pattern ((tr_bound%vstd!slice.SliceAdditionalSpecFns.
                 $slice
                 (SLICE T&. T&)
                 T&.
                 T&))
     :skolemid skolem_internal_vstd__slice__impl&__2_trait_impl_definition
     :qid internal_vstd__slice__impl&__2_trait_impl_definition)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (a1! Poly) (a2! Poly))
             (! (let ((a!1 (and (= (vstd!slice.len%returns_clause_autospec.?
                                     T&.
                                     T&
                                     a1!)
                                   (vstd!slice.len%returns_clause_autospec.?
                                     T&.
                                     T&
                                     a2!))
                                (forall ((i$ Poly))
                                  (! (let ((a!1 (= (vstd!seq.Seq.index.?
                                                     T&.
                                                     T&
                                                     (vstd!view.View.view.?
                                                       $slice
                                                       (SLICE T&. T&)
                                                       a1!)
                                                     i$)
                                                   (vstd!seq.Seq.index.?
                                                     T&.
                                                     T&
                                                     (vstd!view.View.view.?
                                                       $slice
                                                       (SLICE T&. T&)
                                                       a2!)
                                                     i$))))
                                     (let ((a!2 (=> (and (<= 0 (%I i$))
                                                         (< (%I i$)
                                                            (vstd!slice.len%returns_clause_autospec.?
                                                              T&.
                                                              T&
                                                              a1!)))
                                                    a!1)))
                                       (=> (has_type i$ INT) a!2)))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 T&.
                                                 T&
                                                 (vstd!view.View.view.?
                                                   $slice
                                                   (SLICE T&. T&)
                                                   a1!)
                                                 i$))
                                     :pattern ((vstd!seq.Seq.index.?
                                                 T&.
                                                 T&
                                                 (vstd!view.View.view.?
                                                   $slice
                                                   (SLICE T&. T&)
                                                   a2!)
                                                 i$))
                                     :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_0
                                     :qid user_vstd__slice__axiom_slice_ext_equal_0)))))
                (let ((a!2 (=> (sized T&.)
                               (= (ext_eq false (SLICE T&. T&) a1! a2!) a!1))))
                  (=> (and (has_type a1! (SLICE T&. T&))
                           (has_type a2! (SLICE T&. T&)))
                      a!2)))
                :pattern ((ext_eq false (SLICE T&. T&) a1! a2!))
                :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_1
                :qid user_vstd__slice__axiom_slice_ext_equal_1))))
  (=> (fuel_bool fuel%vstd!slice.axiom_slice_ext_equal.) a!1)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (slice! Poly) (i! Poly))
             (! (let ((a!1 (has_resolved T&.
                                         T&
                                         (vstd!seq.Seq.index.?
                                           T&.
                                           T&
                                           (vstd!view.View.view.?
                                             $slice
                                             (SLICE T&. T&)
                                             slice!)
                                           i!))))
                (let ((a!2 (=> (and (<= 0 (%I i!))
                                    (< (%I i!)
                                       (vstd!slice.spec_slice_len.?
                                         T&.
                                         T&
                                         slice!)))
                               (=> (has_resolved $slice (SLICE T&. T&) slice!)
                                   a!1))))
                  (=> (and (has_type slice! (SLICE T&. T&)) (has_type i! INT))
                      (=> (sized T&.) a!2))))
                :pattern ((has_resolved $slice (SLICE T&. T&) slice!)
                          (vstd!seq.Seq.index.?
                            T&.
                            T&
                            (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
                            i!))
                :skolemid skolem_user_vstd__slice__axiom_slice_has_resolved_0
                :qid user_vstd__slice__axiom_slice_has_resolved_0))))
  (=> (fuel_bool fuel%vstd!slice.axiom_slice_has_resolved.) a!1)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (s! Poly))
             (! (let ((a!1 (height_lt (height (vstd!view.View.view.?
                                                $slice
                                                (SLICE T&. T&)
                                                s!))
                                      (height s!))))
                  (=> (has_type s! (SLICE T&. T&)) (=> (sized T&.) a!1)))
                :pattern ((height (vstd!view.View.view.?
                                    $slice
                                    (SLICE T&. T&)
                                    s!)))
                :skolemid skolem_user_vstd__slice__axiom_slice_decreases_to_seq_0
                :qid user_vstd__slice__axiom_slice_decreases_to_seq_0))))
  (=> (fuel_bool fuel%vstd!slice.axiom_slice_decreases_to_seq.) a!1)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (s! Poly) (i! Poly))
             (! (let ((a!1 (< (%I i!)
                              (vstd!seq.Seq.len.?
                                T&.
                                T&
                                (vstd!view.View.view.? $slice (SLICE T&. T&) s!))))
                      (a!2 (height (vstd!seq.Seq.index.?
                                     T&.
                                     T&
                                     (vstd!view.View.view.?
                                       $slice
                                       (SLICE T&. T&)
                                       s!)
                                     i!))))
                (let ((a!3 (=> (and (sized T&.) (<= 0 (%I i!)) a!1)
                               (height_lt a!2 (height s!)))))
                  (=> (and (has_type s! (SLICE T&. T&)) (has_type i! INT)) a!3)))
                :pattern ((height (vstd!seq.Seq.index.?
                                    T&.
                                    T&
                                    (vstd!view.View.view.?
                                      $slice
                                      (SLICE T&. T&)
                                      s!)
                                    i!)))
                :skolemid skolem_user_vstd__slice__lemma_slice_index_decreases_0
                :qid user_vstd__slice__lemma_slice_index_decreases_0))))
  (=> (fuel_bool fuel%vstd!slice.lemma_slice_index_decreases.) a!1)))
(assert (forall ((T&. Dcr) (T& Type) (data! Poly))
  (! (=> (has_type data! (TYPE%vstd!raw_ptr.PtrData. T&. T&))
         (has_type (vstd!raw_ptr.view_reverse_for_eq.? T&. T& data!)
                   (PTR T&. T&)))
     :pattern ((vstd!raw_ptr.view_reverse_for_eq.? T&. T& data!))
     :skolemid skolem_internal_vstd!raw_ptr.view_reverse_for_eq.?_pre_post_definition
     :qid internal_vstd!raw_ptr.view_reverse_for_eq.?_pre_post_definition)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (tr_bound%vstd!view.View. $ (PTR T&. T&))
     :pattern ((tr_bound%vstd!view.View. $ (PTR T&. T&)))
     :skolemid skolem_internal_vstd__raw_ptr__impl&__2_trait_impl_definition
     :qid internal_vstd__raw_ptr__impl&__2_trait_impl_definition)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (a! Poly))
             (! (let ((a!1 (= (vstd!raw_ptr.view_reverse_for_eq.?
                                T&.
                                T&
                                (vstd!view.View.view.? $ (PTR T&. T&) a!))
                              a!)))
                  (=> (has_type a! (PTR T&. T&)) a!1))
                :pattern ((vstd!view.View.view.? $ (PTR T&. T&) a!))
                :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_0
                :qid user_vstd__raw_ptr__ptrs_mut_eq_0))))
  (=> (fuel_bool fuel%vstd!raw_ptr.ptrs_mut_eq.) a!1)))
(assert (forall ((T&. Dcr) (T& Type) (addr! Poly) (provenance! Poly))
  (! (=> (and (has_type addr! USIZE)
              (has_type provenance! TYPE%vstd!raw_ptr.Provenance.))
         (has_type (vstd!raw_ptr.view_reverse_for_eq_sized.?
                     T&.
                     T&
                     addr!
                     provenance!)
                   (PTR T&. T&)))
     :pattern ((vstd!raw_ptr.view_reverse_for_eq_sized.?
                 T&.
                 T&
                 addr!
                 provenance!))
     :skolemid skolem_internal_vstd!raw_ptr.view_reverse_for_eq_sized.?_pre_post_definition
     :qid internal_vstd!raw_ptr.view_reverse_for_eq_sized.?_pre_post_definition)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (a! Poly))
             (! (let ((a!1 (vstd!raw_ptr.PtrData./PtrData/addr
                             (%Poly%vstd!raw_ptr.PtrData.
                               (vstd!view.View.view.? $ (PTR T&. T&) a!))))
                      (a!2 (vstd!raw_ptr.PtrData./PtrData/provenance
                             (%Poly%vstd!raw_ptr.PtrData.
                               (vstd!view.View.view.? $ (PTR T&. T&) a!)))))
                (let ((a!3 (=> (sized T&.)
                               (= (vstd!raw_ptr.view_reverse_for_eq_sized.?
                                    T&.
                                    T&
                                    (I a!1)
                                    (Poly%vstd!raw_ptr.Provenance. a!2))
                                  a!))))
                  (=> (has_type a! (PTR T&. T&)) a!3)))
                :pattern ((vstd!view.View.view.? $ (PTR T&. T&) a!))
                :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_sized_0
                :qid user_vstd__raw_ptr__ptrs_mut_eq_sized_0))))
  (=> (fuel_bool fuel%vstd!raw_ptr.ptrs_mut_eq_sized.) a!1)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (v! Poly))
  (! (=> (has_type v! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
         (uInv SZ (vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!)))
     :pattern ((vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!))
     :skolemid skolem_internal_vstd!std_specs.vec.spec_vec_len.?_pre_post_definition
     :qid internal_vstd!std_specs.vec.spec_vec_len.?_pre_post_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized T&.) (sized A&.) (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%vstd!view.View. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
     :pattern ((tr_bound%vstd!view.View. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
     :skolemid skolem_internal_vstd__view__impl&__8_trait_impl_definition
     :qid internal_vstd__view__impl&__8_trait_impl_definition)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (v! Poly))
             (! (let ((a!1 (= (vstd!std_specs.vec.spec_vec_len.?
                                T&.
                                T&
                                A&.
                                A&
                                v!)
                              (vstd!seq.Seq.len.?
                                T&.
                                T&
                                (vstd!view.View.view.?
                                  $
                                  (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                                  v!)))))
                  (=> (has_type v! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
                      (=> (and (sized T&.)
                               (sized A&.)
                               (tr_bound%core!alloc.Allocator. A&. A&))
                          a!1)))
                :pattern ((vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!))
                :skolemid skolem_user_vstd__std_specs__vec__axiom_spec_len_0
                :qid user_vstd__std_specs__vec__axiom_spec_len_0))))
  (=> (fuel_bool fuel%vstd!std_specs.vec.axiom_spec_len.) a!1)))
(assert (tr_bound%core!alloc.Allocator. $ TYPE%alloc!alloc.Global.))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (vec! Poly) (i! Poly))
             (! (let ((a!1 (has_resolved T&.
                                         T&
                                         (vstd!seq.Seq.index.?
                                           T&.
                                           T&
                                           (vstd!view.View.view.?
                                             $
                                             (TYPE%alloc!vec.Vec.
                                               T&.
                                               T&
                                               $
                                               TYPE%alloc!alloc.Global.)
                                             vec!)
                                           i!))))
                (let ((a!2 (=> (and (<= 0 (%I i!))
                                    (< (%I i!)
                                       (vstd!std_specs.vec.spec_vec_len.?
                                         T&.
                                         T&
                                         $
                                         TYPE%alloc!alloc.Global.
                                         vec!)))
                               (=> (has_resolved $
                                                 (TYPE%alloc!vec.Vec.
                                                   T&.
                                                   T&
                                                   $
                                                   TYPE%alloc!alloc.Global.)
                                                 vec!)
                                   a!1))))
                  (=> (and (has_type vec!
                                     (TYPE%alloc!vec.Vec.
                                       T&.
                                       T&
                                       $
                                       TYPE%alloc!alloc.Global.))
                           (has_type i! INT))
                      (=> (sized T&.) a!2))))
                :pattern ((has_resolved $
                                        (TYPE%alloc!vec.Vec.
                                          T&.
                                          T&
                                          $
                                          TYPE%alloc!alloc.Global.)
                                        vec!)
                          (vstd!seq.Seq.index.?
                            T&.
                            T&
                            (vstd!view.View.view.?
                              $
                              (TYPE%alloc!vec.Vec.
                                T&.
                                T&
                                $
                                TYPE%alloc!alloc.Global.)
                              vec!)
                            i!))
                :skolemid skolem_user_vstd__std_specs__vec__axiom_vec_has_resolved_0
                :qid user_vstd__std_specs__vec__axiom_vec_has_resolved_0))))
  (=> (fuel_bool fuel%vstd!std_specs.vec.axiom_vec_has_resolved.) a!1)))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (v! Poly))
             (! (let ((a!1 (height_lt (height (vstd!view.View.view.?
                                                $
                                                (TYPE%alloc!vec.Vec.
                                                  T&.
                                                  T&
                                                  $
                                                  TYPE%alloc!alloc.Global.)
                                                v!))
                                      (height v!))))
                  (=> (has_type v!
                                (TYPE%alloc!vec.Vec.
                                  T&.
                                  T&
                                  $
                                  TYPE%alloc!alloc.Global.))
                      (=> (sized T&.) a!1)))
                :pattern ((height (vstd!view.View.view.?
                                    $
                                    (TYPE%alloc!vec.Vec.
                                      T&.
                                      T&
                                      $
                                      TYPE%alloc!alloc.Global.)
                                    v!)))
                :skolemid skolem_user_vstd__std_specs__vec__axiom_vec_decreases_to_view_0
                :qid user_vstd__std_specs__vec__axiom_vec_decreases_to_view_0))))
  (=> (fuel_bool fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view.) a!1)))
(assert (tr_bound%core!marker.Tuple. $ TYPE%tuple%0.))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (vec! Poly) (result! Poly))
  (! (= (ens%alloc!vec.impl&%29.as_ref. T&. T& A&. A& vec! result!)
        (and (has_type result! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
             (= result! vec!)))
     :pattern ((ens%alloc!vec.impl&%29.as_ref. T&. T& A&. A& vec! result!))
     :skolemid skolem_internal_ens__alloc!vec.impl&__29.as_ref._definition
     :qid internal_ens__alloc!vec.impl&__29.as_ref._definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (vec! Poly) (result! Poly))
  (! (let ((a!1 (and (has_type result! (SLICE T&. T&))
                     (= (vstd!view.View.view.? $slice (SLICE T&. T&) result!)
                        (vstd!view.View.view.?
                          $
                          (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                          vec!)))))
       (= (ens%alloc!vec.impl&%31.as_ref. T&. T& A&. A& vec! result!) a!1))
     :pattern ((ens%alloc!vec.impl&%31.as_ref. T&. T& A&. A& vec! result!))
     :skolemid skolem_internal_ens__alloc!vec.impl&__31.as_ref._definition
     :qid internal_ens__alloc!vec.impl&__31.as_ref._definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (vec! Poly) (result! Poly))
  (! (let ((a!1 (and (has_type result!
                               (MUTREF $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
                     (= (mut_ref_current% result!) (mut_ref_current% vec!))
                     (= (mut_ref_future% result!) (mut_ref_future% vec!)))))
       (= (ens%alloc!vec.impl&%30.as_mut. T&. T& A&. A& vec! result!) a!1))
     :pattern ((ens%alloc!vec.impl&%30.as_mut. T&. T& A&. A& vec! result!))
     :skolemid skolem_internal_ens__alloc!vec.impl&__30.as_mut._definition
     :qid internal_ens__alloc!vec.impl&__30.as_mut._definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (vec! Poly) (result! Poly))
  (! (let ((a!1 (and (has_type result! (MUTREF $slice (SLICE T&. T&)))
                     (= (vstd!view.View.view.?
                          $slice
                          (SLICE T&. T&)
                          (mut_ref_current% result!))
                        (vstd!view.View.view.?
                          $
                          (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                          (mut_ref_current% vec!)))
                     (= (vstd!view.View.view.?
                          $slice
                          (SLICE T&. T&)
                          (mut_ref_future% result!))
                        (vstd!view.View.view.?
                          $
                          (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                          (mut_ref_future% vec!))))))
       (= (ens%alloc!vec.impl&%32.as_mut. T&. T& A&. A& vec! result!) a!1))
     :pattern ((ens%alloc!vec.impl&%32.as_mut. T&. T& A&. A& vec! result!))
     :skolemid skolem_internal_ens__alloc!vec.impl&__32.as_mut._definition
     :qid internal_ens__alloc!vec.impl&__32.as_mut._definition)))
(assert (fuel_bool_default fuel%vstd!raw_ptr.impl&%3.view.))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (self! Poly))
             (! (= (vstd!view.View.view.? (CONST_PTR $) (PTR T&. T&) self!)
                   (vstd!view.View.view.? $ (PTR T&. T&) self!))
                :pattern ((vstd!view.View.view.?
                            (CONST_PTR $)
                            (PTR T&. T&)
                            self!))
                :skolemid skolem_internal_vstd!raw_ptr.impl&__3.view.?_definition
                :qid internal_vstd!raw_ptr.impl&__3.view.?_definition))))
  (=> (fuel_bool fuel%vstd!raw_ptr.impl&%3.view.) a!1)))
(assert (fuel_bool_default fuel%vstd!view.impl&%0.view.))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (self! Poly))
             (! (=> (tr_bound%vstd!view.View. A&. A&)
                    (= (vstd!view.View.view.? (REF A&.) A& self!)
                       (vstd!view.View.view.? A&. A& self!)))
                :pattern ((vstd!view.View.view.? (REF A&.) A& self!))
                :skolemid skolem_internal_vstd!view.impl&__0.view.?_definition
                :qid internal_vstd!view.impl&__0.view.?_definition))))
  (=> (fuel_bool fuel%vstd!view.impl&%0.view.) a!1)))
(assert (fuel_bool_default fuel%vstd!view.impl&%2.view.))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (self! Poly))
             (! (=> (tr_bound%vstd!view.View. A&. A&)
                    (= (vstd!view.View.view.?
                         (BOX $ TYPE%alloc!alloc.Global. A&.)
                         A&
                         self!)
                       (vstd!view.View.view.? A&. A& self!)))
                :pattern ((vstd!view.View.view.?
                            (BOX $ TYPE%alloc!alloc.Global. A&.)
                            A&
                            self!))
                :skolemid skolem_internal_vstd!view.impl&__2.view.?_definition
                :qid internal_vstd!view.impl&__2.view.?_definition))))
  (=> (fuel_bool fuel%vstd!view.impl&%2.view.) a!1)))
(assert (fuel_bool_default fuel%vstd!view.impl&%4.view.))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (self! Poly))
             (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
                    (= (vstd!view.View.view.?
                         (RC $ TYPE%alloc!alloc.Global. A&.)
                         A&
                         self!)
                       (vstd!view.View.view.? A&. A& self!)))
                :pattern ((vstd!view.View.view.?
                            (RC $ TYPE%alloc!alloc.Global. A&.)
                            A&
                            self!))
                :skolemid skolem_internal_vstd!view.impl&__4.view.?_definition
                :qid internal_vstd!view.impl&__4.view.?_definition))))
  (=> (fuel_bool fuel%vstd!view.impl&%4.view.) a!1)))
(assert (fuel_bool_default fuel%vstd!view.impl&%6.view.))
(assert (let ((a!1 (forall ((A&. Dcr) (A& Type) (self! Poly))
             (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
                    (= (vstd!view.View.view.?
                         (ARC $ TYPE%alloc!alloc.Global. A&.)
                         A&
                         self!)
                       (vstd!view.View.view.? A&. A& self!)))
                :pattern ((vstd!view.View.view.?
                            (ARC $ TYPE%alloc!alloc.Global. A&.)
                            A&
                            self!))
                :skolemid skolem_internal_vstd!view.impl&__6.view.?_definition
                :qid internal_vstd!view.impl&__6.view.?_definition))))
  (=> (fuel_bool fuel%vstd!view.impl&%6.view.) a!1)))
(assert (fuel_bool_default fuel%vstd!view.impl&%16.view.))
(assert (=> (fuel_bool fuel%vstd!view.impl&%16.view.)
    (forall ((self! Poly))
      (! (= (vstd!view.View.view.? $ TYPE%tuple%0. self!) self!)
         :pattern ((vstd!view.View.view.? $ TYPE%tuple%0. self!))
         :skolemid skolem_internal_vstd!view.impl&__16.view.?_definition
         :qid internal_vstd!view.impl&__16.view.?_definition))))
(assert (fuel_bool_default fuel%vstd!view.impl&%18.view.))
(assert (=> (fuel_bool fuel%vstd!view.impl&%18.view.)
    (forall ((self! Poly))
      (! (= (vstd!view.View.view.? $ BOOL self!) self!)
         :pattern ((vstd!view.View.view.? $ BOOL self!))
         :skolemid skolem_internal_vstd!view.impl&__18.view.?_definition
         :qid internal_vstd!view.impl&__18.view.?_definition))))
(assert (fuel_bool_default fuel%vstd!view.impl&%30.view.))
(assert (=> (fuel_bool fuel%vstd!view.impl&%30.view.)
    (forall ((self! Poly))
      (! (= (vstd!view.View.view.? $ USIZE self!) self!)
         :pattern ((vstd!view.View.view.? $ USIZE self!))
         :skolemid skolem_internal_vstd!view.impl&__30.view.?_definition
         :qid internal_vstd!view.impl&__30.view.?_definition))))
(assert (fuel_bool_default
  fuel%lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.))
(assert (let ((a!1 (forall ((T&. Dcr) (T& Type) (r1! Poly) (r2! Poly))
             (! (= (lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
                     T&.
                     T&
                     r1!
                     r2!)
                   (ext_eq false (SLICE T&. T&) r1! r2!))
                :pattern ((lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
                            T&.
                            T&
                            r1!
                            r2!))
                :skolemid skolem_internal_lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?_definition
                :qid internal_lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?_definition))))
  (=> (fuel_bool fuel%lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.)
      a!1)))
(assert (forall ((T&. Dcr) (T& Type))
  (! (tr_bound%vstd!view.View. (CONST_PTR $) (PTR T&. T&))
     :pattern ((tr_bound%vstd!view.View. (CONST_PTR $) (PTR T&. T&)))
     :skolemid skolem_internal_vstd__raw_ptr__impl&__3_trait_impl_definition
     :qid internal_vstd__raw_ptr__impl&__3_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (tr_bound%vstd!view.View. (REF A&.) A&))
     :pattern ((tr_bound%vstd!view.View. (REF A&.) A&))
     :skolemid skolem_internal_vstd__view__impl&__0_trait_impl_definition
     :qid internal_vstd__view__impl&__0_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%vstd!view.View. A&. A&)
         (tr_bound%vstd!view.View. (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
     :pattern ((tr_bound%vstd!view.View.
                 (BOX $ TYPE%alloc!alloc.Global. A&.)
                 A&))
     :skolemid skolem_internal_vstd__view__impl&__2_trait_impl_definition
     :qid internal_vstd__view__impl&__2_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (tr_bound%vstd!view.View. (RC $ TYPE%alloc!alloc.Global. A&.) A&))
     :pattern ((tr_bound%vstd!view.View. (RC $ TYPE%alloc!alloc.Global. A&.) A&))
     :skolemid skolem_internal_vstd__view__impl&__4_trait_impl_definition
     :qid internal_vstd__view__impl&__4_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (and (sized A&.) (tr_bound%vstd!view.View. A&. A&))
         (tr_bound%vstd!view.View. (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
     :pattern ((tr_bound%vstd!view.View.
                 (ARC $ TYPE%alloc!alloc.Global. A&.)
                 A&))
     :skolemid skolem_internal_vstd__view__impl&__6_trait_impl_definition
     :qid internal_vstd__view__impl&__6_trait_impl_definition)))
(assert (tr_bound%vstd!view.View. $ TYPE%tuple%0.))
(assert (tr_bound%vstd!view.View. $ BOOL))
(assert (tr_bound%vstd!view.View. $ USIZE))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.Fn. F&. F& A&. A&))
         (tr_bound%core!ops.function.FnOnce. (REF F&.) F& A&. A&))
     :pattern ((tr_bound%core!ops.function.FnOnce. (REF F&.) F& A&. A&))
     :skolemid skolem_internal_core__ops__function__impls__impl&__2_trait_impl_definition
     :qid internal_core__ops__function__impls__impl&__2_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.Fn. F&. F& A&. A&))
         (tr_bound%core!ops.function.FnMut. (REF F&.) F& A&. A&))
     :pattern ((tr_bound%core!ops.function.FnMut. (REF F&.) F& A&. A&))
     :skolemid skolem_internal_core__ops__function__impls__impl&__1_trait_impl_definition
     :qid internal_core__ops__function__impls__impl&__1_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.Fn. F&. F& A&. A&))
         (tr_bound%core!ops.function.Fn. (REF F&.) F& A&. A&))
     :pattern ((tr_bound%core!ops.function.Fn. (REF F&.) F& A&. A&))
     :skolemid skolem_internal_core__ops__function__impls__impl&__0_trait_impl_definition
     :qid internal_core__ops__function__impls__impl&__0_trait_impl_definition)))
(assert (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized Args&.)
              (sized A&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!ops.function.FnOnce. (BOX A&. A& F&.) F& Args&. Args&))
     :pattern ((tr_bound%core!ops.function.FnOnce.
                 (BOX A&. A& F&.)
                 F&
                 Args&.
                 Args&))
     :skolemid skolem_internal_alloc__boxed__impl&__31_trait_impl_definition
     :qid internal_alloc__boxed__impl&__31_trait_impl_definition)))
(assert (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized Args&.)
              (sized A&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (tr_bound%core!ops.function.FnMut. F&. F& Args&. Args&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!ops.function.FnMut. (BOX A&. A& F&.) F& Args&. Args&))
     :pattern ((tr_bound%core!ops.function.FnMut.
                 (BOX A&. A& F&.)
                 F&
                 Args&.
                 Args&))
     :skolemid skolem_internal_alloc__boxed__impl&__32_trait_impl_definition
     :qid internal_alloc__boxed__impl&__32_trait_impl_definition)))
(assert (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized Args&.)
              (sized A&.)
              (tr_bound%core!marker.Tuple. Args&. Args&)
              (tr_bound%core!ops.function.Fn. F&. F& Args&. Args&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!ops.function.Fn. (BOX A&. A& F&.) F& Args&. Args&))
     :pattern ((tr_bound%core!ops.function.Fn. (BOX A&. A& F&.) F& Args&. Args&))
     :skolemid skolem_internal_alloc__boxed__impl&__33_trait_impl_definition
     :qid internal_alloc__boxed__impl&__33_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!marker.Tuple. A&. A&)
              (tr_bound%core!ops.function.FnMut. F&. F& A&. A&))
         (tr_bound%core!ops.function.FnMut. $ (MUTREF F&. F&) A&. A&))
     :pattern ((tr_bound%core!ops.function.FnMut. $ (MUTREF F&. F&) A&. A&))
     :skolemid skolem_internal_core__ops__function__impls__impl&__3_trait_impl_definition
     :qid internal_core__ops__function__impls__impl&__3_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%core!alloc.Allocator. A&. A&)
         (tr_bound%core!alloc.Allocator. (REF A&.) A&))
     :pattern ((tr_bound%core!alloc.Allocator. (REF A&.) A&))
     :skolemid skolem_internal_core__alloc__impl&__2_trait_impl_definition
     :qid internal_core__alloc__impl&__2_trait_impl_definition)))
(assert (forall ((A&. Dcr) (A& Type))
  (! (=> (tr_bound%core!alloc.Allocator. A&. A&)
         (tr_bound%core!alloc.Allocator. $ (MUTREF A&. A&)))
     :pattern ((tr_bound%core!alloc.Allocator. $ (MUTREF A&. A&)))
     :skolemid skolem_internal_core__alloc__impl&__3_trait_impl_definition
     :qid internal_core__alloc__impl&__3_trait_impl_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!alloc.Allocator. T&. T&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!alloc.Allocator. (BOX A&. A& T&.) T&))
     :pattern ((tr_bound%core!alloc.Allocator. (BOX A&. A& T&.) T&))
     :skolemid skolem_internal_alloc__boxed__impl&__49_trait_impl_definition
     :qid internal_alloc__boxed__impl&__49_trait_impl_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!alloc.Allocator. T&. T&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!alloc.Allocator. (RC A&. A& T&.) T&))
     :pattern ((tr_bound%core!alloc.Allocator. (RC A&. A& T&.) T&))
     :skolemid skolem_internal_alloc__rc__impl&__116_trait_impl_definition
     :qid internal_alloc__rc__impl&__116_trait_impl_definition)))
(assert (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type))
  (! (=> (and (sized A&.)
              (tr_bound%core!alloc.Allocator. T&. T&)
              (tr_bound%core!alloc.Allocator. A&. A&))
         (tr_bound%core!alloc.Allocator. (ARC A&. A& T&.) T&))
     :pattern ((tr_bound%core!alloc.Allocator. (ARC A&. A& T&.) T&))
     :skolemid skolem_internal_alloc__sync__impl&__118_trait_impl_definition
     :qid internal_alloc__sync__impl&__118_trait_impl_definition)))
(assert (forall ((T&. Dcr)
         (T& Type)
         (A&. Dcr)
         (A& Type)
         (g_vec_leneq! Bool)
         (k_vec_leneq! Int)
         (g_vec_lenrng! Bool)
         (k_vec_lenrng_lo! Int)
         (k_vec_lenrng_hi! Int)
         (g_r1_leneq! Bool)
         (k_r1_leneq! Int)
         (g_r1_lenrng! Bool)
         (k_r1_lenrng_lo! Int)
         (k_r1_lenrng_hi! Int)
         (g_r2_leneq! Bool)
         (k_r2_leneq! Int)
         (g_r2_lenrng! Bool)
         (k_r2_lenrng_lo! Int)
         (k_r2_lenrng_hi! Int)
         (g_neq_tuple! Bool)
         (vec! Poly)
         (r1! Poly)
         (r2! Poly))
  (! (let ((a!1 (and (= (vstd!view.View.view.? $slice (SLICE T&. T&) r1!)
                        (vstd!view.View.view.?
                          $
                          (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                          vec!))
                     (= (vstd!view.View.view.? $slice (SLICE T&. T&) r2!)
                        (vstd!view.View.view.?
                          $
                          (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                          vec!)))))
       (= (ens%lib!vec.borrowed.__specdet_6576671712930c59306307a6.
            T&.
            T&
            A&.
            A&
            g_vec_leneq!
            k_vec_leneq!
            g_vec_lenrng!
            k_vec_lenrng_lo!
            k_vec_lenrng_hi!
            g_r1_leneq!
            k_r1_leneq!
            g_r1_lenrng!
            k_r1_lenrng_lo!
            k_r1_lenrng_hi!
            g_r2_leneq!
            k_r2_leneq!
            g_r2_lenrng!
            k_r2_lenrng_lo!
            k_r2_lenrng_hi!
            g_neq_tuple!
            vec!
            r1!
            r2!)
          (=> a!1
              (lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
                T&.
                T&
                r1!
                r2!))))
     :pattern ((ens%lib!vec.borrowed.__specdet_6576671712930c59306307a6.
                 T&.
                 T&
                 A&.
                 A&
                 g_vec_leneq!
                 k_vec_leneq!
                 g_vec_lenrng!
                 k_vec_lenrng_lo!
                 k_vec_lenrng_hi!
                 g_r1_leneq!
                 k_r1_leneq!
                 g_r1_lenrng!
                 k_r1_lenrng_lo!
                 k_r1_lenrng_hi!
                 g_r2_leneq!
                 k_r2_leneq!
                 g_r2_lenrng!
                 k_r2_lenrng_lo!
                 k_r2_lenrng_hi!
                 g_neq_tuple!
                 vec!
                 r1!
                 r2!))
     :skolemid skolem_internal_ens__lib!vec.borrowed.__specdet_6576671712930c59306307a6._definition
     :qid internal_ens__lib!vec.borrowed.__specdet_6576671712930c59306307a6._definition)))
(assert fuel_defaults)
(assert (sized T&.))
(assert (sized A&.))
(assert (tr_bound%core!alloc.Allocator. A&. A&))
(assert (<= 0 k_vec_leneq!))
(assert (<= 0 k_vec_lenrng_lo!))
(assert (<= 0 k_vec_lenrng_hi!))
(assert (<= 0 k_r1_leneq!))
(assert (<= 0 k_r1_lenrng_lo!))
(assert (<= 0 k_r1_lenrng_hi!))
(assert (<= 0 k_r2_leneq!))
(assert (<= 0 k_r2_lenrng_lo!))
(assert (<= 0 k_r2_lenrng_hi!))
(assert (has_type vec! (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
(assert (has_type r1! (SLICE T&. T&)))
(assert (has_type r2! (SLICE T&. T&)))
(assert (let ((a!1 (vstd!seq.Seq.len.?
             T&.
             T&
             (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) vec!)))
      (a!4 (=> g_r1_leneq!
               (=> (= (vstd!slice.len%returns_clause_autospec.? T&. T& r1!)
                      k_r1_leneq!)
                   %%switch_label%%4)))
      (a!5 (=> (and (>= (vstd!slice.len%returns_clause_autospec.? T&. T& r1!)
                        k_r1_lenrng_lo!)
                    (<= (vstd!slice.len%returns_clause_autospec.? T&. T& r1!)
                        k_r1_lenrng_hi!))
               %%switch_label%%3))
      (a!6 (=> g_r2_leneq!
               (=> (= (vstd!slice.len%returns_clause_autospec.? T&. T& r2!)
                      k_r2_leneq!)
                   %%switch_label%%2)))
      (a!7 (=> (and (>= (vstd!slice.len%returns_clause_autospec.? T&. T& r2!)
                        k_r2_lenrng_lo!)
                    (<= (vstd!slice.len%returns_clause_autospec.? T&. T& r2!)
                        k_r2_lenrng_hi!))
               %%switch_label%%1))
      (a!8 (=> g_neq_tuple!
               (=> (not (lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
                          T&.
                          T&
                          r1!
                          r2!))
                   %%switch_label%%0)))
      (a!9 (and (= (vstd!view.View.view.? $slice (SLICE T&. T&) r1!)
                   (vstd!view.View.view.?
                     $
                     (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                     vec!))
                (= (vstd!view.View.view.? $slice (SLICE T&. T&) r2!)
                   (vstd!view.View.view.?
                     $
                     (TYPE%alloc!vec.Vec. T&. T& A&. A&)
                     vec!)))))
(let ((a!2 (and (=> g_vec_leneq! (=> (= a!1 k_vec_leneq!) %%switch_label%%6))
                (=> (not g_vec_leneq!) %%switch_label%%6)))
      (a!3 (=> g_vec_lenrng!
               (=> (and (>= a!1 k_vec_lenrng_lo!) (<= a!1 k_vec_lenrng_hi!))
                   %%switch_label%%5)))
      (a!10 (and (not %%switch_label%%0)
                 (=> %%location_label%%0
                     (=> a!9
                         (lib!vec.borrowed.__specdet_6576671712930c59306307a6_equal.?
                           T&.
                           T&
                           r1!
                           r2!))))))
(let ((a!11 (or (and a!8 (=> (not g_neq_tuple!) %%switch_label%%0)) a!10)))
(let ((a!12 (or (and (=> g_r2_lenrng! a!7)
                     (=> (not g_r2_lenrng!) %%switch_label%%1))
                (and (not %%switch_label%%1) a!11))))
(let ((a!13 (or (and a!6 (=> (not g_r2_leneq!) %%switch_label%%2))
                (and (not %%switch_label%%2) a!12))))
(let ((a!14 (or (and (=> g_r1_lenrng! a!5)
                     (=> (not g_r1_lenrng!) %%switch_label%%3))
                (and (not %%switch_label%%3) a!13))))
(let ((a!15 (or (and a!4 (=> (not g_r1_leneq!) %%switch_label%%4))
                (and (not %%switch_label%%4) a!14))))
(let ((a!16 (or (and a!3 (=> (not g_vec_lenrng!) %%switch_label%%5))
                (and (not %%switch_label%%5) a!15))))
  (not (or a!2 (and (not %%switch_label%%6) a!16))))))))))))

(check-sat-assuming ((not g_vec_leneq!) (not g_vec_lenrng!) (not g_r1_leneq!) (not g_r1_lenrng!) (not g_r2_leneq!) (not g_r2_lenrng!) (not g_neq_tuple!)))
