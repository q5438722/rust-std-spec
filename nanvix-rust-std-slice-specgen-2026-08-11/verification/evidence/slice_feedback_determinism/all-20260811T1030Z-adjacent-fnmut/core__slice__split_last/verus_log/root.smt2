(set-option :auto_config false)
(set-option :smt.mbqi false)
(set-option :smt.case_split 3)
(set-option :smt.qi.eager_threshold 100.0)
(set-option :smt.delay_units true)
(set-option :smt.arith.solver 2)
(set-option :smt.arith.nl false)
(set-option :pi.enabled false)
(set-option :rewriter.sort_disjunctions false)

;; Prelude

;; AIR prelude
(declare-sort %%Function%% 0)

(declare-sort FuelId 0)
(declare-sort Fuel 0)
(declare-const zero Fuel)
(declare-fun succ (Fuel) Fuel)
(declare-fun fuel_bool (FuelId) Bool)
(declare-fun fuel_bool_default (FuelId) Bool)
(declare-const fuel_defaults Bool)
(assert
 (=>
  fuel_defaults
  (forall ((id FuelId)) (!
    (= (fuel_bool id) (fuel_bool_default id))
    :pattern ((fuel_bool id))
    :qid prelude_fuel_defaults
    :skolemid skolem_prelude_fuel_defaults
))))
(declare-datatypes ((fndef 0)) (((fndef_singleton))))
(declare-sort Poly 0)
(declare-sort Height 0)
(declare-fun I (Int) Poly)
(declare-fun B (Bool) Poly)
(declare-fun R (Real) Poly)
(declare-fun F (fndef) Poly)
(declare-fun %I (Poly) Int)
(declare-fun %B (Poly) Bool)
(declare-fun %R (Poly) Real)
(declare-fun %F (Poly) fndef)
(declare-sort Type 0)
(declare-const BOOL Type)
(declare-const INT Type)
(declare-const NAT Type)
(declare-const REAL Type)
(declare-const CHAR Type)
(declare-const USIZE Type)
(declare-const ISIZE Type)
(declare-const TYPE%tuple%0. Type)
(declare-fun UINT (Int) Type)
(declare-fun SINT (Int) Type)
(declare-fun FLOAT (Int) Type)
(declare-fun CONST_INT (Int) Type)
(declare-fun CONST_BOOL (Bool) Type)
(declare-sort Dcr 0)
(declare-const $ Dcr)
(declare-const $slice Dcr)
(declare-const $dyn Dcr)
(declare-fun DST (Dcr) Dcr)
(declare-fun REF (Dcr) Dcr)
(declare-fun BOX (Dcr Type Dcr) Dcr)
(declare-fun RC (Dcr Type Dcr) Dcr)
(declare-fun ARC (Dcr Type Dcr) Dcr)
(declare-fun GHOST (Dcr) Dcr)
(declare-fun TRACKED (Dcr) Dcr)
(declare-fun NEVER (Dcr) Dcr)
(declare-fun CONST_PTR (Dcr) Dcr)
(declare-fun ARRAY (Dcr Type Dcr Type) Type)
(declare-fun MUTREF (Dcr Type) Type)
(declare-fun SLICE (Dcr Type) Type)
(declare-const STRSLICE Type)
(declare-const ALLOCATOR_GLOBAL Type)
(declare-fun PTR (Dcr Type) Type)
(declare-fun has_type (Poly Type) Bool)
(declare-fun sized (Dcr) Bool)
(declare-fun as_type (Poly Type) Poly)
(declare-fun mk_fun (%%Function%%) %%Function%%)
(declare-fun const_int (Type) Int)
(declare-fun const_bool (Type) Bool)
(declare-fun mut_ref_current% (Poly) Poly)
(declare-fun mut_ref_future% (Poly) Poly)
(declare-fun mut_ref_update_current% (Poly Poly) Poly)
(assert
 (forall ((m Poly) (arg Poly)) (!
   (= (mut_ref_current% (mut_ref_update_current% m arg)) arg)
   :pattern ((mut_ref_update_current% m arg))
   :qid prelude_mut_ref_update_current_current
   :skolemid skolem_prelude_mut_ref_update_current_current
)))
(assert
 (forall ((m Poly) (arg Poly)) (!
   (= (mut_ref_future% (mut_ref_update_current% m arg)) (mut_ref_future% m))
   :pattern ((mut_ref_update_current% m arg))
   :qid prelude_mut_ref_update_current_future
   :skolemid skolem_prelude_mut_ref_update_current_future
)))
(assert
 (forall ((m Poly) (d Dcr) (t Type)) (!
   (=>
    (has_type m (MUTREF d t))
    (has_type (mut_ref_current% m) t)
   )
   :pattern ((has_type m (MUTREF d t)) (mut_ref_current% m))
   :qid prelude_mut_ref_current_has_type
   :skolemid skolem_prelude_mut_ref_current_has_type
)))
(assert
 (forall ((m Poly) (d Dcr) (t Type)) (!
   (=>
    (has_type m (MUTREF d t))
    (has_type (mut_ref_future% m) t)
   )
   :pattern ((has_type m (MUTREF d t)) (mut_ref_future% m))
   :qid prelude_mut_ref_current_has_type
   :skolemid skolem_prelude_mut_ref_current_has_type
)))
(assert
 (forall ((m Poly) (d Dcr) (t Type) (arg Poly)) (!
   (=>
    (and
     (has_type m (MUTREF d t))
     (has_type arg t)
    )
    (has_type (mut_ref_update_current% m arg) (MUTREF d t))
   )
   :pattern ((has_type m (MUTREF d t)) (mut_ref_update_current% m arg))
   :qid prelude_mut_ref_update_has_type
   :skolemid skolem_prelude_mut_ref_update_has_type
)))
(assert
 (forall ((d Dcr)) (!
   (=>
    (sized d)
    (sized (DST d))
   )
   :pattern ((sized (DST d)))
   :qid prelude_sized_decorate_struct_inherit
   :skolemid skolem_prelude_sized_decorate_struct_inherit
)))
(assert
 (forall ((d Dcr)) (!
   (sized (REF d))
   :pattern ((sized (REF d)))
   :qid prelude_sized_decorate_ref
   :skolemid skolem_prelude_sized_decorate_ref
)))
(assert
 (forall ((d Dcr) (t Type) (d2 Dcr)) (!
   (sized (BOX d t d2))
   :pattern ((sized (BOX d t d2)))
   :qid prelude_sized_decorate_box
   :skolemid skolem_prelude_sized_decorate_box
)))
(assert
 (forall ((d Dcr) (t Type) (d2 Dcr)) (!
   (sized (RC d t d2))
   :pattern ((sized (RC d t d2)))
   :qid prelude_sized_decorate_rc
   :skolemid skolem_prelude_sized_decorate_rc
)))
(assert
 (forall ((d Dcr) (t Type) (d2 Dcr)) (!
   (sized (ARC d t d2))
   :pattern ((sized (ARC d t d2)))
   :qid prelude_sized_decorate_arc
   :skolemid skolem_prelude_sized_decorate_arc
)))
(assert
 (forall ((d Dcr)) (!
   (sized (GHOST d))
   :pattern ((sized (GHOST d)))
   :qid prelude_sized_decorate_ghost
   :skolemid skolem_prelude_sized_decorate_ghost
)))
(assert
 (forall ((d Dcr)) (!
   (sized (TRACKED d))
   :pattern ((sized (TRACKED d)))
   :qid prelude_sized_decorate_tracked
   :skolemid skolem_prelude_sized_decorate_tracked
)))
(assert
 (forall ((d Dcr)) (!
   (sized (NEVER d))
   :pattern ((sized (NEVER d)))
   :qid prelude_sized_decorate_never
   :skolemid skolem_prelude_sized_decorate_never
)))
(assert
 (forall ((d Dcr)) (!
   (sized (CONST_PTR d))
   :pattern ((sized (CONST_PTR d)))
   :qid prelude_sized_decorate_const_ptr
   :skolemid skolem_prelude_sized_decorate_const_ptr
)))
(assert
 (sized $)
)
(assert
 (forall ((i Int)) (!
   (= i (const_int (CONST_INT i)))
   :pattern ((CONST_INT i))
   :qid prelude_type_id_const_int
   :skolemid skolem_prelude_type_id_const_int
)))
(assert
 (forall ((b Bool)) (!
   (= b (const_bool (CONST_BOOL b)))
   :pattern ((CONST_BOOL b))
   :qid prelude_type_id_const_bool
   :skolemid skolem_prelude_type_id_const_bool
)))
(assert
 (forall ((b Bool)) (!
   (has_type (B b) BOOL)
   :pattern ((has_type (B b) BOOL))
   :qid prelude_has_type_bool
   :skolemid skolem_prelude_has_type_bool
)))
(assert
 (forall ((r Real)) (!
   (has_type (R r) REAL)
   :pattern ((has_type (R r) REAL))
   :qid prelude_has_type_real
   :skolemid skolem_prelude_has_type_real
)))
(assert
 (forall ((x Poly) (t Type)) (!
   (and
    (has_type (as_type x t) t)
    (=>
     (has_type x t)
     (= x (as_type x t))
   ))
   :pattern ((as_type x t))
   :qid prelude_as_type
   :skolemid skolem_prelude_as_type
)))
(assert
 (forall ((x %%Function%%)) (!
   (= (mk_fun x) x)
   :pattern ((mk_fun x))
   :qid prelude_mk_fun
   :skolemid skolem_prelude_mk_fun
)))
(assert
 (forall ((x Bool)) (!
   (= x (%B (B x)))
   :pattern ((B x))
   :qid prelude_unbox_box_bool
   :skolemid skolem_prelude_unbox_box_bool
)))
(assert
 (forall ((x Int)) (!
   (= x (%I (I x)))
   :pattern ((I x))
   :qid prelude_unbox_box_int
   :skolemid skolem_prelude_unbox_box_int
)))
(assert
 (forall ((x Real)) (!
   (= x (%R (R x)))
   :pattern ((R x))
   :qid prelude_unbox_box_real
   :skolemid skolem_prelude_unbox_box_real
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x BOOL)
    (= x (B (%B x)))
   )
   :pattern ((has_type x BOOL))
   :qid prelude_box_unbox_bool
   :skolemid skolem_prelude_box_unbox_bool
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x INT)
    (= x (I (%I x)))
   )
   :pattern ((has_type x INT))
   :qid prelude_box_unbox_int
   :skolemid skolem_prelude_box_unbox_int
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x NAT)
    (= x (I (%I x)))
   )
   :pattern ((has_type x NAT))
   :qid prelude_box_unbox_nat
   :skolemid skolem_prelude_box_unbox_nat
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x USIZE)
    (= x (I (%I x)))
   )
   :pattern ((has_type x USIZE))
   :qid prelude_box_unbox_usize
   :skolemid skolem_prelude_box_unbox_usize
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x ISIZE)
    (= x (I (%I x)))
   )
   :pattern ((has_type x ISIZE))
   :qid prelude_box_unbox_isize
   :skolemid skolem_prelude_box_unbox_isize
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (UINT bits))
    (= x (I (%I x)))
   )
   :pattern ((has_type x (UINT bits)))
   :qid prelude_box_unbox_uint
   :skolemid skolem_prelude_box_unbox_uint
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (SINT bits))
    (= x (I (%I x)))
   )
   :pattern ((has_type x (SINT bits)))
   :qid prelude_box_unbox_sint
   :skolemid skolem_prelude_box_unbox_sint
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (FLOAT bits))
    (= x (I (%I x)))
   )
   :pattern ((has_type x (FLOAT bits)))
   :qid prelude_box_unbox_sint
   :skolemid skolem_prelude_box_unbox_sint
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x CHAR)
    (= x (I (%I x)))
   )
   :pattern ((has_type x CHAR))
   :qid prelude_box_unbox_char
   :skolemid skolem_prelude_box_unbox_char
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x REAL)
    (= x (R (%R x)))
   )
   :pattern ((has_type x REAL))
   :qid prelude_box_unbox_real
   :skolemid skolem_prelude_box_unbox_real
)))
(declare-fun ext_eq (Bool Type Poly Poly) Bool)
(assert
 (forall ((deep Bool) (t Type) (x Poly) (y Poly)) (!
   (= (= x y) (ext_eq deep t x y))
   :pattern ((ext_eq deep t x y))
   :qid prelude_ext_eq
   :skolemid skolem_prelude_ext_eq
)))
(declare-const SZ Int)
(assert
 (or
  (= SZ 32)
  (= SZ 64)
))
(declare-fun uHi (Int) Int)
(declare-fun iLo (Int) Int)
(declare-fun iHi (Int) Int)
(assert
 (= (uHi 8) 256)
)
(assert
 (= (uHi 16) 65536)
)
(assert
 (= (uHi 32) 4294967296)
)
(assert
 (= (uHi 64) 18446744073709551616)
)
(assert
 (= (uHi 128) (+ 1 340282366920938463463374607431768211455))
)
(assert
 (= (iLo 8) (- 128))
)
(assert
 (= (iLo 16) (- 32768))
)
(assert
 (= (iLo 32) (- 2147483648))
)
(assert
 (= (iLo 64) (- 9223372036854775808))
)
(assert
 (= (iLo 128) (- 170141183460469231731687303715884105728))
)
(assert
 (= (iHi 8) 128)
)
(assert
 (= (iHi 16) 32768)
)
(assert
 (= (iHi 32) 2147483648)
)
(assert
 (= (iHi 64) 9223372036854775808)
)
(assert
 (= (iHi 128) 170141183460469231731687303715884105728)
)
(declare-fun nClip (Int) Int)
(declare-fun uClip (Int Int) Int)
(declare-fun iClip (Int Int) Int)
(declare-fun charClip (Int) Int)
(assert
 (forall ((i Int)) (!
   (and
    (<= 0 (nClip i))
    (=>
     (<= 0 i)
     (= i (nClip i))
   ))
   :pattern ((nClip i))
   :qid prelude_nat_clip
   :skolemid skolem_prelude_nat_clip
)))
(assert
 (forall ((bits Int) (i Int)) (!
   (and
    (<= 0 (uClip bits i))
    (< (uClip bits i) (uHi bits))
    (=>
     (and
      (<= 0 i)
      (< i (uHi bits))
     )
     (= i (uClip bits i))
   ))
   :pattern ((uClip bits i))
   :qid prelude_u_clip
   :skolemid skolem_prelude_u_clip
)))
(assert
 (forall ((bits Int) (i Int)) (!
   (and
    (<= (iLo bits) (iClip bits i))
    (< (iClip bits i) (iHi bits))
    (=>
     (and
      (<= (iLo bits) i)
      (< i (iHi bits))
     )
     (= i (iClip bits i))
   ))
   :pattern ((iClip bits i))
   :qid prelude_i_clip
   :skolemid skolem_prelude_i_clip
)))
(assert
 (forall ((i Int)) (!
   (and
    (or
     (and
      (<= 0 (charClip i))
      (<= (charClip i) 55295)
     )
     (and
      (<= 57344 (charClip i))
      (<= (charClip i) 1114111)
    ))
    (=>
     (or
      (and
       (<= 0 i)
       (<= i 55295)
      )
      (and
       (<= 57344 i)
       (<= i 1114111)
     ))
     (= i (charClip i))
   ))
   :pattern ((charClip i))
   :qid prelude_char_clip
   :skolemid skolem_prelude_char_clip
)))
(declare-fun uInv (Int Int) Bool)
(declare-fun iInv (Int Int) Bool)
(declare-fun charInv (Int) Bool)
(assert
 (forall ((bits Int) (i Int)) (!
   (= (uInv bits i) (and
     (<= 0 i)
     (< i (uHi bits))
   ))
   :pattern ((uInv bits i))
   :qid prelude_u_inv
   :skolemid skolem_prelude_u_inv
)))
(assert
 (forall ((bits Int) (i Int)) (!
   (= (iInv bits i) (and
     (<= (iLo bits) i)
     (< i (iHi bits))
   ))
   :pattern ((iInv bits i))
   :qid prelude_i_inv
   :skolemid skolem_prelude_i_inv
)))
(assert
 (forall ((i Int)) (!
   (= (charInv i) (or
     (and
      (<= 0 i)
      (<= i 55295)
     )
     (and
      (<= 57344 i)
      (<= i 1114111)
   )))
   :pattern ((charInv i))
   :qid prelude_char_inv
   :skolemid skolem_prelude_char_inv
)))
(assert
 (forall ((x Int)) (!
   (has_type (I x) INT)
   :pattern ((has_type (I x) INT))
   :qid prelude_has_type_int
   :skolemid skolem_prelude_has_type_int
)))
(assert
 (forall ((x Int)) (!
   (=>
    (<= 0 x)
    (has_type (I x) NAT)
   )
   :pattern ((has_type (I x) NAT))
   :qid prelude_has_type_nat
   :skolemid skolem_prelude_has_type_nat
)))
(assert
 (forall ((x Int)) (!
   (=>
    (uInv SZ x)
    (has_type (I x) USIZE)
   )
   :pattern ((has_type (I x) USIZE))
   :qid prelude_has_type_usize
   :skolemid skolem_prelude_has_type_usize
)))
(assert
 (forall ((x Int)) (!
   (=>
    (iInv SZ x)
    (has_type (I x) ISIZE)
   )
   :pattern ((has_type (I x) ISIZE))
   :qid prelude_has_type_isize
   :skolemid skolem_prelude_has_type_isize
)))
(assert
 (forall ((bits Int) (x Int)) (!
   (=>
    (uInv bits x)
    (has_type (I x) (UINT bits))
   )
   :pattern ((has_type (I x) (UINT bits)))
   :qid prelude_has_type_uint
   :skolemid skolem_prelude_has_type_uint
)))
(assert
 (forall ((bits Int) (x Int)) (!
   (=>
    (iInv bits x)
    (has_type (I x) (SINT bits))
   )
   :pattern ((has_type (I x) (SINT bits)))
   :qid prelude_has_type_sint
   :skolemid skolem_prelude_has_type_sint
)))
(assert
 (forall ((bits Int) (x Int)) (!
   (=>
    (uInv bits x)
    (has_type (I x) (FLOAT bits))
   )
   :pattern ((has_type (I x) (FLOAT bits)))
   :qid prelude_has_type_sint
   :skolemid skolem_prelude_has_type_sint
)))
(assert
 (forall ((x Int)) (!
   (=>
    (charInv x)
    (has_type (I x) CHAR)
   )
   :pattern ((has_type (I x) CHAR))
   :qid prelude_has_type_char
   :skolemid skolem_prelude_has_type_char
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x NAT)
    (<= 0 (%I x))
   )
   :pattern ((has_type x NAT))
   :qid prelude_unbox_int
   :skolemid skolem_prelude_unbox_int
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x USIZE)
    (uInv SZ (%I x))
   )
   :pattern ((has_type x USIZE))
   :qid prelude_unbox_usize
   :skolemid skolem_prelude_unbox_usize
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x ISIZE)
    (iInv SZ (%I x))
   )
   :pattern ((has_type x ISIZE))
   :qid prelude_unbox_isize
   :skolemid skolem_prelude_unbox_isize
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (UINT bits))
    (uInv bits (%I x))
   )
   :pattern ((has_type x (UINT bits)))
   :qid prelude_unbox_uint
   :skolemid skolem_prelude_unbox_uint
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (SINT bits))
    (iInv bits (%I x))
   )
   :pattern ((has_type x (SINT bits)))
   :qid prelude_unbox_sint
   :skolemid skolem_prelude_unbox_sint
)))
(assert
 (forall ((bits Int) (x Poly)) (!
   (=>
    (has_type x (FLOAT bits))
    (uInv bits (%I x))
   )
   :pattern ((has_type x (FLOAT bits)))
   :qid prelude_unbox_sint
   :skolemid skolem_prelude_unbox_sint
)))
(declare-fun Add (Int Int) Int)
(declare-fun Sub (Int Int) Int)
(declare-fun Mul (Int Int) Int)
(declare-fun EucDiv (Int Int) Int)
(declare-fun EucMod (Int Int) Int)
(declare-fun RAdd (Real Real) Real)
(declare-fun RSub (Real Real) Real)
(declare-fun RMul (Real Real) Real)
(declare-fun RDiv (Real Real) Real)
(assert
 (forall ((x Int) (y Int)) (!
   (= (Add x y) (+ x y))
   :pattern ((Add x y))
   :qid prelude_add
   :skolemid skolem_prelude_add
)))
(assert
 (forall ((x Int) (y Int)) (!
   (= (Sub x y) (- x y))
   :pattern ((Sub x y))
   :qid prelude_sub
   :skolemid skolem_prelude_sub
)))
(assert
 (forall ((x Int) (y Int)) (!
   (= (Mul x y) (* x y))
   :pattern ((Mul x y))
   :qid prelude_mul
   :skolemid skolem_prelude_mul
)))
(assert
 (forall ((x Int) (y Int)) (!
   (= (EucDiv x y) (div x y))
   :pattern ((EucDiv x y))
   :qid prelude_eucdiv
   :skolemid skolem_prelude_eucdiv
)))
(assert
 (forall ((x Int) (y Int)) (!
   (= (EucMod x y) (mod x y))
   :pattern ((EucMod x y))
   :qid prelude_eucmod
   :skolemid skolem_prelude_eucmod
)))
(assert
 (forall ((x Real) (y Real)) (!
   (= (RAdd x y) (+ x y))
   :pattern ((RAdd x y))
   :qid prelude_radd
   :skolemid skolem_prelude_radd
)))
(assert
 (forall ((x Real) (y Real)) (!
   (= (RSub x y) (- x y))
   :pattern ((RSub x y))
   :qid prelude_rsub
   :skolemid skolem_prelude_rsub
)))
(assert
 (forall ((x Real) (y Real)) (!
   (= (RMul x y) (* x y))
   :pattern ((RMul x y))
   :qid prelude_rmul
   :skolemid skolem_prelude_rmul
)))
(assert
 (forall ((x Real) (y Real)) (!
   (= (RDiv x y) (/ x y))
   :pattern ((RDiv x y))
   :qid prelude_rdiv
   :skolemid skolem_prelude_rdiv
)))
(assert
 (forall ((x Int) (y Int)) (!
   (=>
    (and
     (<= 0 x)
     (<= 0 y)
    )
    (<= 0 (Mul x y))
   )
   :pattern ((Mul x y))
   :qid prelude_mul_nats
   :skolemid skolem_prelude_mul_nats
)))
(assert
 (forall ((x Int) (y Int)) (!
   (=>
    (and
     (<= 0 x)
     (< 0 y)
    )
    (and
     (<= 0 (EucDiv x y))
     (<= (EucDiv x y) x)
   ))
   :pattern ((EucDiv x y))
   :qid prelude_div_unsigned_in_bounds
   :skolemid skolem_prelude_div_unsigned_in_bounds
)))
(assert
 (forall ((x Int) (y Int)) (!
   (=>
    (and
     (<= 0 x)
     (< 0 y)
    )
    (and
     (<= 0 (EucMod x y))
     (< (EucMod x y) y)
   ))
   :pattern ((EucMod x y))
   :qid prelude_mod_unsigned_in_bounds
   :skolemid skolem_prelude_mod_unsigned_in_bounds
)))
(declare-fun bitxor (Poly Poly) Int)
(declare-fun bitand (Poly Poly) Int)
(declare-fun bitor (Poly Poly) Int)
(declare-fun bitshr (Poly Poly) Int)
(declare-fun bitshl (Poly Poly) Int)
(declare-fun bitnot (Poly) Int)
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (uInv bits (%I x))
     (uInv bits (%I y))
    )
    (uInv bits (bitxor x y))
   )
   :pattern ((uClip bits (bitxor x y)))
   :qid prelude_bit_xor_u_inv
   :skolemid skolem_prelude_bit_xor_u_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (iInv bits (%I x))
     (iInv bits (%I y))
    )
    (iInv bits (bitxor x y))
   )
   :pattern ((iClip bits (bitxor x y)))
   :qid prelude_bit_xor_i_inv
   :skolemid skolem_prelude_bit_xor_i_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (uInv bits (%I x))
     (uInv bits (%I y))
    )
    (uInv bits (bitor x y))
   )
   :pattern ((uClip bits (bitor x y)))
   :qid prelude_bit_or_u_inv
   :skolemid skolem_prelude_bit_or_u_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (iInv bits (%I x))
     (iInv bits (%I y))
    )
    (iInv bits (bitor x y))
   )
   :pattern ((iClip bits (bitor x y)))
   :qid prelude_bit_or_i_inv
   :skolemid skolem_prelude_bit_or_i_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (uInv bits (%I x))
     (uInv bits (%I y))
    )
    (uInv bits (bitand x y))
   )
   :pattern ((uClip bits (bitand x y)))
   :qid prelude_bit_and_u_inv
   :skolemid skolem_prelude_bit_and_u_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (iInv bits (%I x))
     (iInv bits (%I y))
    )
    (iInv bits (bitand x y))
   )
   :pattern ((iClip bits (bitand x y)))
   :qid prelude_bit_and_i_inv
   :skolemid skolem_prelude_bit_and_i_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (uInv bits (%I x))
     (<= 0 (%I y))
    )
    (uInv bits (bitshr x y))
   )
   :pattern ((uClip bits (bitshr x y)))
   :qid prelude_bit_shr_u_inv
   :skolemid skolem_prelude_bit_shr_u_inv
)))
(assert
 (forall ((x Poly) (y Poly) (bits Int)) (!
   (=>
    (and
     (iInv bits (%I x))
     (<= 0 (%I y))
    )
    (iInv bits (bitshr x y))
   )
   :pattern ((iClip bits (bitshr x y)))
   :qid prelude_bit_shr_i_inv
   :skolemid skolem_prelude_bit_shr_i_inv
)))
(declare-fun singular_mod (Int Int) Int)
(assert
 (forall ((x Int) (y Int)) (!
   (=>
    (not (= y 0))
    (= (EucMod x y) (singular_mod x y))
   )
   :pattern ((singular_mod x y))
   :qid prelude_singularmod
   :skolemid skolem_prelude_singularmod
)))
(declare-fun has_resolved (Dcr Type Poly) Bool)
(declare-fun closure_req (Type Dcr Type Poly Poly) Bool)
(declare-fun closure_ens (Type Dcr Type Poly Poly Poly) Bool)
(declare-fun default_ens (Type Dcr Type Poly Poly Poly) Bool)
(declare-fun height (Poly) Height)
(declare-fun height_lt (Height Height) Bool)
(declare-fun fun_from_recursive_field (Poly) Poly)
(declare-fun check_decrease_height (Poly Poly Bool) Bool)
(assert
 (forall ((cur Poly) (prev Poly) (otherwise Bool)) (!
   (= (check_decrease_height cur prev otherwise) (or
     (height_lt (height cur) (height prev))
     (and
      (= (height cur) (height prev))
      otherwise
   )))
   :pattern ((check_decrease_height cur prev otherwise))
   :qid prelude_check_decrease_height
   :skolemid skolem_prelude_check_decrease_height
)))
(assert
 (forall ((cur Int) (prev Int)) (!
   (= (height_lt (height (I cur)) (height (I prev))) (and
     (<= 0 cur)
     (< cur prev)
   ))
   :pattern ((height_lt (height (I cur)) (height (I prev))))
   :qid prelude_check_decrease_int_height
   :skolemid skolem_prelude_check_decrease_int_height
)))
(assert
 (forall ((x Height) (y Height)) (!
   (= (height_lt x y) (and
     ((_ partial-order 0) x y)
     (not (= x y))
   ))
   :pattern ((height_lt x y))
   :qid prelude_height_lt
   :skolemid skolem_prelude_height_lt
)))

;; MODULE 'root module'

;; Fuel
(declare-const fuel%vstd!std_specs.option.impl&%0.arrow_Some_0. FuelId)
(declare-const fuel%vstd!std_specs.option.impl&%0.arrow_0. FuelId)
(declare-const fuel%vstd!std_specs.option.is_some. FuelId)
(declare-const fuel%vstd!std_specs.option.is_none. FuelId)
(declare-const fuel%vstd!std_specs.option.spec_unwrap. FuelId)
(declare-const fuel%vstd!array.array_view. FuelId)
(declare-const fuel%vstd!array.impl&%0.view. FuelId)
(declare-const fuel%vstd!array.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!array.lemma_array_index. FuelId)
(declare-const fuel%vstd!array.array_len_matches_n. FuelId)
(declare-const fuel%vstd!array.axiom_array_ext_equal. FuelId)
(declare-const fuel%vstd!array.axiom_array_has_resolved. FuelId)
(declare-const fuel%vstd!function.axiom_fn_mut_call_requires. FuelId)
(declare-const fuel%vstd!function.axiom_fn_mut_call_ensures. FuelId)
(declare-const fuel%vstd!multiset.axiom_multiset_ext_equal. FuelId)
(declare-const fuel%vstd!multiset.axiom_multiset_ext_equal_deep. FuelId)
(declare-const fuel%vstd!pervasive.strictly_cloned. FuelId)
(declare-const fuel%vstd!pervasive.cloned. FuelId)
(declare-const fuel%vstd!raw_ptr.impl&%3.view. FuelId)
(declare-const fuel%vstd!raw_ptr.ptrs_mut_eq. FuelId)
(declare-const fuel%vstd!raw_ptr.ptrs_mut_eq_sized. FuelId)
(declare-const fuel%vstd!seq.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!seq.impl&%2.spec_add. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_index_decreases. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_subrange_decreases. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_empty. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_new_len. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_new_index. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_update_len. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_update_same. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_update_different. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_ext_equal. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_ext_equal_deep. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_subrange_len. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_subrange_index. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_two_subranges_index. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_add_len. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_add_index1. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_add_index2. FuelId)
(declare-const fuel%vstd!seq_lib.impl&%0.add_empty_left. FuelId)
(declare-const fuel%vstd!seq_lib.impl&%0.add_empty_right. FuelId)
(declare-const fuel%vstd!slice.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!slice.axiom_spec_len. FuelId)
(declare-const fuel%vstd!slice.len%returns_clause_autospec. FuelId)
(declare-const fuel%vstd!slice.axiom_slice_ext_equal. FuelId)
(declare-const fuel%vstd!slice.axiom_slice_has_resolved. FuelId)
(declare-const fuel%vstd!string.axiom_str_literal_len. FuelId)
(declare-const fuel%vstd!string.axiom_str_literal_get_char. FuelId)
(declare-const fuel%vstd!view.impl&%0.view. FuelId)
(declare-const fuel%vstd!view.impl&%2.view. FuelId)
(declare-const fuel%vstd!view.impl&%4.view. FuelId)
(declare-const fuel%vstd!view.impl&%6.view. FuelId)
(declare-const fuel%vstd!view.impl&%14.view. FuelId)
(declare-const fuel%vstd!view.impl&%16.view. FuelId)
(declare-const fuel%vstd!view.impl&%18.view. FuelId)
(declare-const fuel%vstd!view.impl&%20.view. FuelId)
(declare-const fuel%vstd!view.impl&%30.view. FuelId)
(declare-const fuel%vstd!view.impl&%44.view. FuelId)
(declare-const fuel%vstd!view.impl&%46.view. FuelId)
(declare-const fuel%vstd!view.impl&%48.view. FuelId)
(declare-const fuel%det_harness!slice_seq. FuelId)
(declare-const fuel%det_harness!slice_len. FuelId)
(declare-const fuel%det_harness!slice_subrange. FuelId)
(declare-const fuel%det_harness!seq_subrange. FuelId)
(declare-const fuel%det_harness!seq_update. FuelId)
(declare-const fuel%det_harness!axiom_partial_eq_observed_symmetric. FuelId)
(declare-const fuel%det_harness!axiom_partial_eq_observed_transitive. FuelId)
(declare-const fuel%det_harness!slice_contains_value. FuelId)
(declare-const fuel%det_harness!slice_is_prefix. FuelId)
(declare-const fuel%det_harness!slice_is_suffix. FuelId)
(declare-const fuel%det_harness!slice_strip_prefix_result. FuelId)
(declare-const fuel%det_harness!slice_strip_suffix_result. FuelId)
(declare-const fuel%det_harness!slice_strip_circumfix_result. FuelId)
(declare-const fuel%det_harness!slice_filled. FuelId)
(declare-const fuel%det_harness!slice_cloned_from. FuelId)
(declare-const fuel%det_harness!slice_filled_with_clone. FuelId)
(declare-const fuel%det_harness!slice_reversed. FuelId)
(declare-const fuel%det_harness!slice_rotated_left. FuelId)
(declare-const fuel%det_harness!slice_rotated_right. FuelId)
(declare-const fuel%det_harness!slice_swapped. FuelId)
(declare-const fuel%det_harness!axiom_zero_arg_fnmut_outputs_len. FuelId)
(declare-const fuel%det_harness!slice_multiplicity. FuelId)
(declare-const fuel%det_harness!slice_permutation. FuelId)
(declare-const fuel%det_harness!axiom_ord_cmp_observed_reflexive. FuelId)
(declare-const fuel%det_harness!axiom_ord_cmp_observed_dual. FuelId)
(declare-const fuel%det_harness!axiom_ord_cmp_observed_matches_partial_eq. FuelId)
(declare-const fuel%det_harness!ordering_rank. FuelId)
(declare-const fuel%det_harness!ord_leq_observed. FuelId)
(declare-const fuel%det_harness!axiom_ord_leq_observed_total. FuelId)
(declare-const fuel%det_harness!axiom_ord_leq_observed_transitive. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_ord. FuelId)
(declare-const fuel%det_harness!axiom_partial_ord_leq_observed_matches_partial_eq.
 FuelId
)
(declare-const fuel%det_harness!axiom_partial_ord_leq_observed_antisymmetric. FuelId)
(declare-const fuel%det_harness!axiom_partial_ord_leq_observed_transitive. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_partial_ord. FuelId)
(declare-const fuel%det_harness!slice_adjacent_pair_count. FuelId)
(declare-const fuel%det_harness!fnmut_adjacent_bool_trace_valid. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_bool_compare. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_bool_compare_result. FuelId)
(declare-const fuel%det_harness!fnmut_adjacent_key_trace_valid. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_partial_key. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_partial_key_result. FuelId)
(declare-const fuel%det_harness!slice_ord_equal_at. FuelId)
(declare-const fuel%det_harness!slice_ord_insertion_point. FuelId)
(declare-const fuel%det_harness!slice_binary_search_result. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_ordered. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_equal_at. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_insertion_point. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_result. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_key_ordered. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_key_equal_at. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_key_insertion_point. FuelId)
(declare-const fuel%det_harness!slice_binary_search_by_key_result. FuelId)
(declare-const fuel%det_harness!slice_partitioned_by_predicate. FuelId)
(declare-const fuel%det_harness!slice_partition_point_result. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_cmp. FuelId)
(declare-const fuel%det_harness!axiom_comparator_observation_domain. FuelId)
(declare-const fuel%det_harness!axiom_comparator_leq_observed_reflexive. FuelId)
(declare-const fuel%det_harness!axiom_comparator_leq_observed_total. FuelId)
(declare-const fuel%det_harness!axiom_comparator_leq_observed_transitive. FuelId)
(declare-const fuel%det_harness!slice_sorted_by_key. FuelId)
(declare-const fuel%det_harness!slice_select_partition_ord. FuelId)
(declare-const fuel%det_harness!slice_select_partition_cmp. FuelId)
(declare-const fuel%det_harness!slice_select_partition_key. FuelId)
(declare-const fuel%det_harness!slice_partitioned_at. FuelId)
(declare-const fuel%det_harness!slice_iterator_well_formed. FuelId)
(declare-const fuel%det_harness!axiom_slice_iterator_view_well_formed. FuelId)
(declare-const fuel%det_harness!slice_chunk_partition. FuelId)
(declare-const fuel%det_harness!slice_predicate_split_view. FuelId)
(declare-const fuel%det_harness!slice_adjacent_chunk_view. FuelId)
(declare-const fuel%det_harness!slice_split_off_partition. FuelId)
(declare-const fuel%det_harness!slice_split_off_first_result. FuelId)
(declare-const fuel%det_harness!slice_split_off_last_result. FuelId)
(declare-const fuel%det_harness!utf8_chunk_partition. FuelId)
(declare-const fuel%det_harness!array_ref_view. FuelId)
(declare-const fuel%det_harness!array_mut_ref_view. FuelId)
(declare-const fuel%det_harness!array_value_view. FuelId)
(declare-const fuel%det_harness!split_point_in_range. FuelId)
(declare-const fuel%det_harness!slice_fixed_prefix. FuelId)
(declare-const fuel%det_harness!slice_fixed_suffix. FuelId)
(declare-const fuel%det_harness!flatten_array_chunks. FuelId)
(declare-const fuel%det_harness!slice_array_chunks_partition. FuelId)
(declare-const fuel%det_harness!slice_array_rchunks_partition. FuelId)
(declare-const fuel%det_harness!slice_raw_domain_valid. FuelId)
(declare-const fuel%det_harness!slice_from_raw_parts_result. FuelId)
(declare-const fuel%det_harness!slice_from_raw_parts_mut_result. FuelId)
(declare-const fuel%det_harness!slice_align_to_result. FuelId)
(declare-const fuel%det_harness!slice_align_to_mut_result. FuelId)
(declare-const fuel%det_harness!maybe_uninit_relation_well_formed. FuelId)
(declare-const fuel%det_harness!maybe_uninit_all_initialized. FuelId)
(declare-const fuel%det_harness!maybe_uninit_written_from. FuelId)
(declare-const fuel%det_harness!maybe_uninit_drop_all. FuelId)
(declare-const fuel%det_harness!ascii_is_uppercase. FuelId)
(declare-const fuel%det_harness!ascii_is_lowercase. FuelId)
(declare-const fuel%det_harness!ascii_lower_byte. FuelId)
(declare-const fuel%det_harness!ascii_upper_byte. FuelId)
(declare-const fuel%det_harness!ascii_is_byte. FuelId)
(declare-const fuel%det_harness!ascii_is_whitespace. FuelId)
(declare-const fuel%det_harness!ascii_all. FuelId)
(declare-const fuel%det_harness!ascii_lower_seq. FuelId)
(declare-const fuel%det_harness!ascii_upper_seq. FuelId)
(declare-const fuel%det_harness!ascii_eq_ignore_case. FuelId)
(declare-const fuel%det_harness!ascii_trim_start_boundary. FuelId)
(declare-const fuel%det_harness!ascii_trim_end_boundary. FuelId)
(declare-const fuel%det_harness!ascii_trim_start_index. FuelId)
(declare-const fuel%det_harness!ascii_trim_end_index. FuelId)
(declare-const fuel%det_harness!ascii_trim_start_result. FuelId)
(declare-const fuel%det_harness!ascii_trim_end_result. FuelId)
(declare-const fuel%det_harness!ascii_trim_result. FuelId)
(declare-const fuel%det_harness!det___rust_std_candidate_equal. FuelId)
(declare-const fuel%vstd!array.group_array_axioms. FuelId)
(declare-const fuel%vstd!function.group_function_axioms. FuelId)
(declare-const fuel%vstd!imap.group_imap_lemmas. FuelId)
(declare-const fuel%vstd!iset.group_iset_lemmas. FuelId)
(declare-const fuel%vstd!laws_cmp.group_laws_cmp. FuelId)
(declare-const fuel%vstd!laws_eq.bool_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.u8_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.i8_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.u16_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.i16_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.u32_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.i32_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.u64_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.i64_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.u128_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.i128_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.usize_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.isize_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_1_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_2_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_3_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_4_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_5_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_6_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_7_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_8_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_9_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_10_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_11_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq. FuelId)
(declare-const fuel%vstd!laws_eq.group_laws_eq. FuelId)
(declare-const fuel%vstd!layout.group_align_properties. FuelId)
(declare-const fuel%vstd!layout.group_layout_axioms. FuelId)
(declare-const fuel%vstd!map.group_map_lemmas. FuelId)
(declare-const fuel%vstd!multiset.group_multiset_axioms. FuelId)
(declare-const fuel%vstd!raw_ptr.group_raw_ptr_axioms. FuelId)
(declare-const fuel%vstd!seq.group_seq_lemmas. FuelId)
(declare-const fuel%vstd!seq_lib.group_filter_ensures. FuelId)
(declare-const fuel%vstd!seq_lib.group_seq_lib_default. FuelId)
(declare-const fuel%vstd!set.group_set_lemmas. FuelId)
(declare-const fuel%vstd!set_lib.group_set_lib_default. FuelId)
(declare-const fuel%vstd!slice.group_slice_axioms. FuelId)
(declare-const fuel%vstd!string.group_string_axioms. FuelId)
(declare-const fuel%vstd!std_specs.bits.group_bits_axioms. FuelId)
(declare-const fuel%vstd!std_specs.iter.group_iter_axioms. FuelId)
(declare-const fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms. FuelId)
(declare-const fuel%vstd!std_specs.btree.group_btree_axioms. FuelId)
(declare-const fuel%vstd!std_specs.hash.group_hash_axioms. FuelId)
(declare-const fuel%vstd!std_specs.range.group_range_axioms. FuelId)
(declare-const fuel%vstd!std_specs.slice.group_slice_axioms. FuelId)
(declare-const fuel%vstd!std_specs.vec.group_vec_axioms. FuelId)
(declare-const fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.group_nonzero_axioms. FuelId)
(declare-const fuel%vstd!group_vstd_default. FuelId)
(assert
 (distinct fuel%vstd!std_specs.option.impl&%0.arrow_Some_0. fuel%vstd!std_specs.option.impl&%0.arrow_0.
  fuel%vstd!std_specs.option.is_some. fuel%vstd!std_specs.option.is_none. fuel%vstd!std_specs.option.spec_unwrap.
  fuel%vstd!array.array_view. fuel%vstd!array.impl&%0.view. fuel%vstd!array.impl&%2.spec_index.
  fuel%vstd!array.lemma_array_index. fuel%vstd!array.array_len_matches_n. fuel%vstd!array.axiom_array_ext_equal.
  fuel%vstd!array.axiom_array_has_resolved. fuel%vstd!function.axiom_fn_mut_call_requires.
  fuel%vstd!function.axiom_fn_mut_call_ensures. fuel%vstd!multiset.axiom_multiset_ext_equal.
  fuel%vstd!multiset.axiom_multiset_ext_equal_deep. fuel%vstd!pervasive.strictly_cloned.
  fuel%vstd!pervasive.cloned. fuel%vstd!raw_ptr.impl&%3.view. fuel%vstd!raw_ptr.ptrs_mut_eq.
  fuel%vstd!raw_ptr.ptrs_mut_eq_sized. fuel%vstd!seq.impl&%2.spec_index. fuel%vstd!seq.impl&%2.spec_add.
  fuel%vstd!seq.lemma_seq_index_decreases. fuel%vstd!seq.lemma_seq_subrange_decreases.
  fuel%vstd!seq.lemma_seq_empty. fuel%vstd!seq.lemma_seq_new_len. fuel%vstd!seq.lemma_seq_new_index.
  fuel%vstd!seq.lemma_seq_update_len. fuel%vstd!seq.lemma_seq_update_same. fuel%vstd!seq.lemma_seq_update_different.
  fuel%vstd!seq.lemma_seq_ext_equal. fuel%vstd!seq.lemma_seq_ext_equal_deep. fuel%vstd!seq.lemma_seq_subrange_len.
  fuel%vstd!seq.lemma_seq_subrange_index. fuel%vstd!seq.lemma_seq_two_subranges_index.
  fuel%vstd!seq.lemma_seq_add_len. fuel%vstd!seq.lemma_seq_add_index1. fuel%vstd!seq.lemma_seq_add_index2.
  fuel%vstd!seq_lib.impl&%0.add_empty_left. fuel%vstd!seq_lib.impl&%0.add_empty_right.
  fuel%vstd!slice.impl&%2.spec_index. fuel%vstd!slice.axiom_spec_len. fuel%vstd!slice.len%returns_clause_autospec.
  fuel%vstd!slice.axiom_slice_ext_equal. fuel%vstd!slice.axiom_slice_has_resolved.
  fuel%vstd!string.axiom_str_literal_len. fuel%vstd!string.axiom_str_literal_get_char.
  fuel%vstd!view.impl&%0.view. fuel%vstd!view.impl&%2.view. fuel%vstd!view.impl&%4.view.
  fuel%vstd!view.impl&%6.view. fuel%vstd!view.impl&%14.view. fuel%vstd!view.impl&%16.view.
  fuel%vstd!view.impl&%18.view. fuel%vstd!view.impl&%20.view. fuel%vstd!view.impl&%30.view.
  fuel%vstd!view.impl&%44.view. fuel%vstd!view.impl&%46.view. fuel%vstd!view.impl&%48.view.
  fuel%det_harness!slice_seq. fuel%det_harness!slice_len. fuel%det_harness!slice_subrange.
  fuel%det_harness!seq_subrange. fuel%det_harness!seq_update. fuel%det_harness!axiom_partial_eq_observed_symmetric.
  fuel%det_harness!axiom_partial_eq_observed_transitive. fuel%det_harness!slice_contains_value.
  fuel%det_harness!slice_is_prefix. fuel%det_harness!slice_is_suffix. fuel%det_harness!slice_strip_prefix_result.
  fuel%det_harness!slice_strip_suffix_result. fuel%det_harness!slice_strip_circumfix_result.
  fuel%det_harness!slice_filled. fuel%det_harness!slice_cloned_from. fuel%det_harness!slice_filled_with_clone.
  fuel%det_harness!slice_reversed. fuel%det_harness!slice_rotated_left. fuel%det_harness!slice_rotated_right.
  fuel%det_harness!slice_swapped. fuel%det_harness!axiom_zero_arg_fnmut_outputs_len.
  fuel%det_harness!slice_multiplicity. fuel%det_harness!slice_permutation. fuel%det_harness!axiom_ord_cmp_observed_reflexive.
  fuel%det_harness!axiom_ord_cmp_observed_dual. fuel%det_harness!axiom_ord_cmp_observed_matches_partial_eq.
  fuel%det_harness!ordering_rank. fuel%det_harness!ord_leq_observed. fuel%det_harness!axiom_ord_leq_observed_total.
  fuel%det_harness!axiom_ord_leq_observed_transitive. fuel%det_harness!slice_sorted_by_ord.
  fuel%det_harness!axiom_partial_ord_leq_observed_matches_partial_eq. fuel%det_harness!axiom_partial_ord_leq_observed_antisymmetric.
  fuel%det_harness!axiom_partial_ord_leq_observed_transitive. fuel%det_harness!slice_sorted_by_partial_ord.
  fuel%det_harness!slice_adjacent_pair_count. fuel%det_harness!fnmut_adjacent_bool_trace_valid.
  fuel%det_harness!slice_sorted_by_bool_compare. fuel%det_harness!slice_sorted_by_bool_compare_result.
  fuel%det_harness!fnmut_adjacent_key_trace_valid. fuel%det_harness!slice_sorted_by_partial_key.
  fuel%det_harness!slice_sorted_by_partial_key_result. fuel%det_harness!slice_ord_equal_at.
  fuel%det_harness!slice_ord_insertion_point. fuel%det_harness!slice_binary_search_result.
  fuel%det_harness!slice_binary_search_by_ordered. fuel%det_harness!slice_binary_search_by_equal_at.
  fuel%det_harness!slice_binary_search_by_insertion_point. fuel%det_harness!slice_binary_search_by_result.
  fuel%det_harness!slice_binary_search_by_key_ordered. fuel%det_harness!slice_binary_search_by_key_equal_at.
  fuel%det_harness!slice_binary_search_by_key_insertion_point. fuel%det_harness!slice_binary_search_by_key_result.
  fuel%det_harness!slice_partitioned_by_predicate. fuel%det_harness!slice_partition_point_result.
  fuel%det_harness!slice_sorted_by_cmp. fuel%det_harness!axiom_comparator_observation_domain.
  fuel%det_harness!axiom_comparator_leq_observed_reflexive. fuel%det_harness!axiom_comparator_leq_observed_total.
  fuel%det_harness!axiom_comparator_leq_observed_transitive. fuel%det_harness!slice_sorted_by_key.
  fuel%det_harness!slice_select_partition_ord. fuel%det_harness!slice_select_partition_cmp.
  fuel%det_harness!slice_select_partition_key. fuel%det_harness!slice_partitioned_at.
  fuel%det_harness!slice_iterator_well_formed. fuel%det_harness!axiom_slice_iterator_view_well_formed.
  fuel%det_harness!slice_chunk_partition. fuel%det_harness!slice_predicate_split_view.
  fuel%det_harness!slice_adjacent_chunk_view. fuel%det_harness!slice_split_off_partition.
  fuel%det_harness!slice_split_off_first_result. fuel%det_harness!slice_split_off_last_result.
  fuel%det_harness!utf8_chunk_partition. fuel%det_harness!array_ref_view. fuel%det_harness!array_mut_ref_view.
  fuel%det_harness!array_value_view. fuel%det_harness!split_point_in_range. fuel%det_harness!slice_fixed_prefix.
  fuel%det_harness!slice_fixed_suffix. fuel%det_harness!flatten_array_chunks. fuel%det_harness!slice_array_chunks_partition.
  fuel%det_harness!slice_array_rchunks_partition. fuel%det_harness!slice_raw_domain_valid.
  fuel%det_harness!slice_from_raw_parts_result. fuel%det_harness!slice_from_raw_parts_mut_result.
  fuel%det_harness!slice_align_to_result. fuel%det_harness!slice_align_to_mut_result.
  fuel%det_harness!maybe_uninit_relation_well_formed. fuel%det_harness!maybe_uninit_all_initialized.
  fuel%det_harness!maybe_uninit_written_from. fuel%det_harness!maybe_uninit_drop_all.
  fuel%det_harness!ascii_is_uppercase. fuel%det_harness!ascii_is_lowercase. fuel%det_harness!ascii_lower_byte.
  fuel%det_harness!ascii_upper_byte. fuel%det_harness!ascii_is_byte. fuel%det_harness!ascii_is_whitespace.
  fuel%det_harness!ascii_all. fuel%det_harness!ascii_lower_seq. fuel%det_harness!ascii_upper_seq.
  fuel%det_harness!ascii_eq_ignore_case. fuel%det_harness!ascii_trim_start_boundary.
  fuel%det_harness!ascii_trim_end_boundary. fuel%det_harness!ascii_trim_start_index.
  fuel%det_harness!ascii_trim_end_index. fuel%det_harness!ascii_trim_start_result.
  fuel%det_harness!ascii_trim_end_result. fuel%det_harness!ascii_trim_result. fuel%det_harness!det___rust_std_candidate_equal.
  fuel%vstd!array.group_array_axioms. fuel%vstd!function.group_function_axioms. fuel%vstd!imap.group_imap_lemmas.
  fuel%vstd!iset.group_iset_lemmas. fuel%vstd!laws_cmp.group_laws_cmp. fuel%vstd!laws_eq.bool_laws.group_laws_eq.
  fuel%vstd!laws_eq.u8_laws.group_laws_eq. fuel%vstd!laws_eq.i8_laws.group_laws_eq.
  fuel%vstd!laws_eq.u16_laws.group_laws_eq. fuel%vstd!laws_eq.i16_laws.group_laws_eq.
  fuel%vstd!laws_eq.u32_laws.group_laws_eq. fuel%vstd!laws_eq.i32_laws.group_laws_eq.
  fuel%vstd!laws_eq.u64_laws.group_laws_eq. fuel%vstd!laws_eq.i64_laws.group_laws_eq.
  fuel%vstd!laws_eq.u128_laws.group_laws_eq. fuel%vstd!laws_eq.i128_laws.group_laws_eq.
  fuel%vstd!laws_eq.usize_laws.group_laws_eq. fuel%vstd!laws_eq.isize_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_1_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_2_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_3_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_4_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_5_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_6_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_7_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_8_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_9_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_10_laws.group_laws_eq.
  fuel%vstd!laws_eq.tuple_11_laws.group_laws_eq. fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq.
  fuel%vstd!laws_eq.group_laws_eq. fuel%vstd!layout.group_align_properties. fuel%vstd!layout.group_layout_axioms.
  fuel%vstd!map.group_map_lemmas. fuel%vstd!multiset.group_multiset_axioms. fuel%vstd!raw_ptr.group_raw_ptr_axioms.
  fuel%vstd!seq.group_seq_lemmas. fuel%vstd!seq_lib.group_filter_ensures. fuel%vstd!seq_lib.group_seq_lib_default.
  fuel%vstd!set.group_set_lemmas. fuel%vstd!set_lib.group_set_lib_default. fuel%vstd!slice.group_slice_axioms.
  fuel%vstd!string.group_string_axioms. fuel%vstd!std_specs.bits.group_bits_axioms.
  fuel%vstd!std_specs.iter.group_iter_axioms. fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.
  fuel%vstd!std_specs.btree.group_btree_axioms. fuel%vstd!std_specs.hash.group_hash_axioms.
  fuel%vstd!std_specs.range.group_range_axioms. fuel%vstd!std_specs.slice.group_slice_axioms.
  fuel%vstd!std_specs.vec.group_vec_axioms. fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms.
  fuel%vstd!std_specs.nonzero.group_nonzero_axioms. fuel%vstd!group_vstd_default.
))
(assert
 (=>
  (fuel_bool_default fuel%vstd!array.group_array_axioms.)
  (and
   (fuel_bool_default fuel%vstd!array.array_len_matches_n.)
   (fuel_bool_default fuel%vstd!array.lemma_array_index.)
   (fuel_bool_default fuel%vstd!array.axiom_array_ext_equal.)
   (fuel_bool_default fuel%vstd!array.axiom_array_has_resolved.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!function.group_function_axioms.)
  (and
   (fuel_bool_default fuel%vstd!function.axiom_fn_mut_call_requires.)
   (fuel_bool_default fuel%vstd!function.axiom_fn_mut_call_ensures.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!laws_eq.group_laws_eq.)
  (and
   (fuel_bool_default fuel%vstd!laws_eq.bool_laws.group_laws_eq.)
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
   (fuel_bool_default fuel%vstd!laws_eq.tuple_12_laws.group_laws_eq.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!layout.group_layout_axioms.)
  (fuel_bool_default fuel%vstd!layout.group_align_properties.)
))
(assert
 (=>
  (fuel_bool_default fuel%vstd!multiset.group_multiset_axioms.)
  (and
   (fuel_bool_default fuel%vstd!multiset.axiom_multiset_ext_equal.)
   (fuel_bool_default fuel%vstd!multiset.axiom_multiset_ext_equal_deep.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!raw_ptr.group_raw_ptr_axioms.)
  (and
   (fuel_bool_default fuel%vstd!raw_ptr.ptrs_mut_eq.)
   (fuel_bool_default fuel%vstd!raw_ptr.ptrs_mut_eq_sized.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!seq.group_seq_lemmas.)
  (and
   (fuel_bool_default fuel%vstd!seq.lemma_seq_index_decreases.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_subrange_decreases.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_empty.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_new_len.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_new_index.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_update_len.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_update_same.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_update_different.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal_deep.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_subrange_len.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_subrange_index.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_two_subranges_index.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_add_len.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_add_index1.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_add_index2.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!seq_lib.group_seq_lib_default.)
  (and
   (fuel_bool_default fuel%vstd!seq_lib.group_filter_ensures.)
   (fuel_bool_default fuel%vstd!seq_lib.impl&%0.add_empty_left.)
   (fuel_bool_default fuel%vstd!seq_lib.impl&%0.add_empty_right.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!slice.group_slice_axioms.)
  (and
   (fuel_bool_default fuel%vstd!slice.axiom_spec_len.)
   (fuel_bool_default fuel%vstd!slice.axiom_slice_ext_equal.)
   (fuel_bool_default fuel%vstd!slice.axiom_slice_has_resolved.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!string.group_string_axioms.)
  (and
   (fuel_bool_default fuel%vstd!string.axiom_str_literal_len.)
   (fuel_bool_default fuel%vstd!string.axiom_str_literal_get_char.)
)))
(assert
 (fuel_bool_default fuel%vstd!group_vstd_default.)
)
(assert
 (=>
  (fuel_bool_default fuel%vstd!group_vstd_default.)
  (and
   (fuel_bool_default fuel%vstd!seq.group_seq_lemmas.)
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
   (fuel_bool_default fuel%vstd!std_specs.range.group_range_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.bits.group_bits_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.slice.group_slice_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.iter.group_iter_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.vec.group_vec_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.hash.group_hash_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.btree.group_btree_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.nonzero.group_nonzero_axioms.)
)))

;; Trait-Decls
(declare-fun tr_bound%vstd!array.ArrayAdditionalSpecFns. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%vstd!slice.SliceAdditionalSpecFns. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!slice.index.SliceIndex. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%vstd!view.View. (Dcr Type) Bool)
(declare-fun tr_bound%core!clone.Clone. (Dcr Type) Bool)
(declare-fun tr_bound%core!marker.Copy. (Dcr Type) Bool)
(declare-fun tr_bound%core!cmp.PartialEq. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!cmp.Eq. (Dcr Type) Bool)
(declare-fun tr_bound%core!cmp.PartialOrd. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!cmp.Ord. (Dcr Type) Bool)
(declare-fun tr_bound%core!marker.Tuple. (Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.FnOnce. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.FnMut. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.Fn. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!alloc.Allocator. (Dcr Type) Bool)
(declare-fun tr_bound%vstd!std_specs.option.OptionAdditionalFns. (Dcr Type Dcr Type)
 Bool
)

;; Associated-Type-Decls
(declare-fun proj%%core!slice.index.SliceIndex./Output (Dcr Type Dcr Type) Dcr)
(declare-fun proj%core!slice.index.SliceIndex./Output (Dcr Type Dcr Type) Type)
(declare-fun proj%%vstd!view.View./V (Dcr Type) Dcr)
(declare-fun proj%vstd!view.View./V (Dcr Type) Type)
(declare-fun proj%%core!ops.function.FnOnce./Output (Dcr Type Dcr Type) Dcr)
(declare-fun proj%core!ops.function.FnOnce./Output (Dcr Type Dcr Type) Type)

;; Datatypes
(declare-fun pointee_metadata% (Dcr) Type)
(declare-fun pointee_metadata%% (Dcr) Dcr)
(assert
 (forall ((d Dcr)) (!
   (=>
    (sized d)
    (= (pointee_metadata% d) TYPE%tuple%0.)
   )
   :pattern ((pointee_metadata% d))
   :qid prelude_project_pointee_metadata_sized
   :skolemid skolem_prelude_project_pointee_metadata_sized
)))
(assert
 (forall ((d Dcr)) (!
   (=>
    (sized d)
    (= (pointee_metadata%% d) $)
   )
   :pattern ((pointee_metadata%% d))
   :qid prelude_project_pointee_metadata_decoration_sized
   :skolemid skolem_prelude_project_pointee_metadata_decoration_sized
)))
(assert
 (= (pointee_metadata% $slice) USIZE)
)
(assert
 (= (pointee_metadata%% $slice) $)
)
(assert
 (forall ((d Dcr)) (!
   (= (pointee_metadata% (DST d)) (pointee_metadata% d))
   :pattern ((pointee_metadata% (DST d)))
   :qid prelude_project_pointee_metadata_decorate_struct_inherit
   :skolemid skolem_prelude_project_pointee_metadata_decorate_struct_inherit
)))
(assert
 (forall ((d Dcr)) (!
   (= (pointee_metadata%% (DST d)) (pointee_metadata%% d))
   :pattern ((pointee_metadata%% (DST d)))
   :qid prelude_project_pointee_metadata_decoration_decorate_struct_inherit
   :skolemid skolem_prelude_project_pointee_metadata_decoration_decorate_struct_inherit
)))
(declare-sort core!range.Range<usize.>. 0)
(declare-sort core!slice.GetDisjointMutError. 0)
(declare-sort core!slice.ascii.EscapeAscii. 0)
(declare-sort core!str.lossy.Utf8Chunks. 0)
(declare-sort alloc!alloc.Global. 0)
(declare-sort vstd!raw_ptr.Provenance. 0)
(declare-sort vstd!seq.Seq<bool.>. 0)
(declare-sort vstd!seq.Seq<u8.>. 0)
(declare-sort vstd!seq.Seq<char.>. 0)
(declare-sort slice%<u8.>. 0)
(declare-sort strslice%. 0)
(declare-datatypes ((core!cmp.Ordering. 0) (core!option.Option. 0) (core!result.Result.
   0
  ) (core!ops.range.Range. 0) (core!ops.range.Bound. 0) (vstd!raw_ptr.PtrData. 0) (
   det_harness!ComparatorObservation. 0
  ) (det_harness!SliceIteratorView. 0) (det_harness!SliceRawMutability. 0) (det_harness!SliceRawDomain.
   0
  ) (det_harness!MaybeUninitSliceRelation. 0) (tuple%0. 0) (tuple%1. 0) (tuple%2. 0)
 ) (((core!cmp.Ordering./Less) (core!cmp.Ordering./Equal) (core!cmp.Ordering./Greater))
  ((core!option.Option./None) (core!option.Option./Some (core!option.Option./Some/?0 Poly)))
  ((core!result.Result./Ok (core!result.Result./Ok/?0 Poly)) (core!result.Result./Err
    (core!result.Result./Err/?0 Poly)
   )
  ) ((core!ops.range.Range./Range (core!ops.range.Range./Range/?start Poly) (core!ops.range.Range./Range/?end
     Poly
   ))
  ) ((core!ops.range.Bound./Included (core!ops.range.Bound./Included/?0 Poly)) (core!ops.range.Bound./Excluded
    (core!ops.range.Bound./Excluded/?0 Poly)
   ) (core!ops.range.Bound./Unbounded)
  ) ((vstd!raw_ptr.PtrData./PtrData (vstd!raw_ptr.PtrData./PtrData/?addr Int) (vstd!raw_ptr.PtrData./PtrData/?provenance
     vstd!raw_ptr.Provenance.
    ) (vstd!raw_ptr.PtrData./PtrData/?metadata Poly)
   )
  ) ((det_harness!ComparatorObservation./ComparatorObservation (det_harness!ComparatorObservation./ComparatorObservation/?domain
     Poly
    ) (det_harness!ComparatorObservation./ComparatorObservation/?trace_id Int)
   )
  ) ((det_harness!SliceIteratorView./SliceIteratorView (det_harness!SliceIteratorView./SliceIteratorView/?source
     Poly
    ) (det_harness!SliceIteratorView./SliceIteratorView/?remaining Poly) (det_harness!SliceIteratorView./SliceIteratorView/?yielded_prefix
     Poly
    ) (det_harness!SliceIteratorView./SliceIteratorView/?remainder Poly) (det_harness!SliceIteratorView./SliceIteratorView/?chunk_size
     Int
    ) (det_harness!SliceIteratorView./SliceIteratorView/?reverse Bool)
   )
  ) ((det_harness!SliceRawMutability./Immutable) (det_harness!SliceRawMutability./Mutable))
  ((det_harness!SliceRawDomain./SliceRawDomain (det_harness!SliceRawDomain./SliceRawDomain/?len
     Int
    ) (det_harness!SliceRawDomain./SliceRawDomain/?non_null Bool) (det_harness!SliceRawDomain./SliceRawDomain/?aligned
     Bool
    ) (det_harness!SliceRawDomain./SliceRawDomain/?one_allocation Bool) (det_harness!SliceRawDomain./SliceRawDomain/?initialized
     Bool
    ) (det_harness!SliceRawDomain./SliceRawDomain/?aliasing_ok Bool) (det_harness!SliceRawDomain./SliceRawDomain/?within_isize
     Bool
    ) (det_harness!SliceRawDomain./SliceRawDomain/?mutability det_harness!SliceRawMutability.)
   )
  ) ((det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/?initialized
     vstd!seq.Seq<bool.>.
    ) (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/?values Poly)
   )
  ) ((tuple%0./tuple%0)) ((tuple%1./tuple%1 (tuple%1./tuple%1/?0 Poly))) ((tuple%2./tuple%2
    (tuple%2./tuple%2/?0 Poly) (tuple%2./tuple%2/?1 Poly)
))))
(declare-fun core!option.Option./Some/0 (Dcr Type core!option.Option.) Poly)
(declare-fun core!result.Result./Ok/0 (Dcr Type Dcr Type core!result.Result.) Poly)
(declare-fun core!result.Result./Err/0 (Dcr Type Dcr Type core!result.Result.) Poly)
(declare-fun core!ops.range.Range./Range/start (core!ops.range.Range.) Poly)
(declare-fun core!ops.range.Range./Range/end (core!ops.range.Range.) Poly)
(declare-fun core!ops.range.Bound./Included/0 (Dcr Type core!ops.range.Bound.) Poly)
(declare-fun core!ops.range.Bound./Excluded/0 (Dcr Type core!ops.range.Bound.) Poly)
(declare-fun vstd!raw_ptr.PtrData./PtrData/addr (vstd!raw_ptr.PtrData.) Int)
(declare-fun vstd!raw_ptr.PtrData./PtrData/provenance (vstd!raw_ptr.PtrData.) vstd!raw_ptr.Provenance.)
(declare-fun vstd!raw_ptr.PtrData./PtrData/metadata (vstd!raw_ptr.PtrData.) Poly)
(declare-fun det_harness!ComparatorObservation./ComparatorObservation/domain (det_harness!ComparatorObservation.)
 Poly
)
(declare-fun det_harness!ComparatorObservation./ComparatorObservation/trace_id (det_harness!ComparatorObservation.)
 Int
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/source (det_harness!SliceIteratorView.)
 Poly
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/remaining (det_harness!SliceIteratorView.)
 Poly
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix (det_harness!SliceIteratorView.)
 Poly
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/remainder (det_harness!SliceIteratorView.)
 Poly
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/chunk_size (det_harness!SliceIteratorView.)
 Int
)
(declare-fun det_harness!SliceIteratorView./SliceIteratorView/reverse (det_harness!SliceIteratorView.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/len (det_harness!SliceRawDomain.)
 Int
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/non_null (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/aligned (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/one_allocation (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/initialized (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/within_isize (det_harness!SliceRawDomain.)
 Bool
)
(declare-fun det_harness!SliceRawDomain./SliceRawDomain/mutability (det_harness!SliceRawDomain.)
 det_harness!SliceRawMutability.
)
(declare-fun det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
 (det_harness!MaybeUninitSliceRelation.) vstd!seq.Seq<bool.>.
)
(declare-fun det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
 (det_harness!MaybeUninitSliceRelation.) Poly
)
(declare-fun tuple%1./tuple%1/0 (tuple%1.) Poly)
(declare-fun tuple%2./tuple%2/0 (tuple%2.) Poly)
(declare-fun tuple%2./tuple%2/1 (tuple%2.) Poly)
(declare-fun TYPE%fun%1. (Dcr Type Dcr Type) Type)
(declare-const TYPE%alloc!alloc.Global. Type)
(declare-const TYPE%core!cmp.Ordering. Type)
(declare-fun TYPE%core!option.Option. (Dcr Type) Type)
(declare-fun TYPE%core!result.Result. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!mem.maybe_uninit.MaybeUninit. (Dcr Type) Type)
(declare-fun TYPE%core!ops.range.Range. (Dcr Type) Type)
(declare-fun TYPE%core!ops.range.Bound. (Dcr Type) Type)
(declare-fun TYPE%vstd!multiset.Multiset. (Dcr Type) Type)
(declare-const TYPE%vstd!raw_ptr.Provenance. Type)
(declare-fun TYPE%vstd!raw_ptr.PtrData. (Dcr Type) Type)
(declare-fun TYPE%vstd!seq.Seq. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.IterMut. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.Chunks. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ChunksExact. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ChunksMut. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ChunksExactMut. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RChunks. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RChunksExact. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RChunksMut. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RChunksExactMut. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.Windows. (Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ArrayWindows. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.Split. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.SplitMut. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.SplitInclusive. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.SplitInclusiveMut. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.SplitN. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.SplitNMut. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RSplit. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RSplitMut. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RSplitN. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.RSplitNMut. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ChunkBy. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!slice.iter.ChunkByMut. (Dcr Type Dcr Type) Type)
(declare-const TYPE%core!str.lossy.Utf8Chunks. Type)
(declare-const TYPE%core!slice.ascii.EscapeAscii. Type)
(declare-const TYPE%core!slice.GetDisjointMutError. Type)
(declare-fun TYPE%core!range.Range. (Dcr Type) Type)
(declare-fun TYPE%det_harness!ComparatorObservation. (Dcr Type) Type)
(declare-fun TYPE%det_harness!SliceIteratorView. (Dcr Type) Type)
(declare-const TYPE%det_harness!SliceRawMutability. Type)
(declare-const TYPE%det_harness!SliceRawDomain. Type)
(declare-fun TYPE%det_harness!MaybeUninitSliceRelation. (Dcr Type) Type)
(declare-fun TYPE%tuple%1. (Dcr Type) Type)
(declare-fun TYPE%tuple%2. (Dcr Type Dcr Type) Type)
(declare-fun FNDEF%core!clone.Clone.clone. (Dcr Type) Type)
(declare-fun Poly%fun%1. (%%Function%%) Poly)
(declare-fun %Poly%fun%1. (Poly) %%Function%%)
(declare-fun Poly%array%. (%%Function%%) Poly)
(declare-fun %Poly%array%. (Poly) %%Function%%)
(declare-fun Poly%core!range.Range<usize.>. (core!range.Range<usize.>.) Poly)
(declare-fun %Poly%core!range.Range<usize.>. (Poly) core!range.Range<usize.>.)
(declare-fun Poly%core!slice.GetDisjointMutError. (core!slice.GetDisjointMutError.)
 Poly
)
(declare-fun %Poly%core!slice.GetDisjointMutError. (Poly) core!slice.GetDisjointMutError.)
(declare-fun Poly%core!slice.ascii.EscapeAscii. (core!slice.ascii.EscapeAscii.) Poly)
(declare-fun %Poly%core!slice.ascii.EscapeAscii. (Poly) core!slice.ascii.EscapeAscii.)
(declare-fun Poly%core!str.lossy.Utf8Chunks. (core!str.lossy.Utf8Chunks.) Poly)
(declare-fun %Poly%core!str.lossy.Utf8Chunks. (Poly) core!str.lossy.Utf8Chunks.)
(declare-fun Poly%alloc!alloc.Global. (alloc!alloc.Global.) Poly)
(declare-fun %Poly%alloc!alloc.Global. (Poly) alloc!alloc.Global.)
(declare-fun Poly%vstd!raw_ptr.Provenance. (vstd!raw_ptr.Provenance.) Poly)
(declare-fun %Poly%vstd!raw_ptr.Provenance. (Poly) vstd!raw_ptr.Provenance.)
(declare-fun Poly%vstd!seq.Seq<bool.>. (vstd!seq.Seq<bool.>.) Poly)
(declare-fun %Poly%vstd!seq.Seq<bool.>. (Poly) vstd!seq.Seq<bool.>.)
(declare-fun Poly%vstd!seq.Seq<u8.>. (vstd!seq.Seq<u8.>.) Poly)
(declare-fun %Poly%vstd!seq.Seq<u8.>. (Poly) vstd!seq.Seq<u8.>.)
(declare-fun Poly%vstd!seq.Seq<char.>. (vstd!seq.Seq<char.>.) Poly)
(declare-fun %Poly%vstd!seq.Seq<char.>. (Poly) vstd!seq.Seq<char.>.)
(declare-fun Poly%slice%<u8.>. (slice%<u8.>.) Poly)
(declare-fun %Poly%slice%<u8.>. (Poly) slice%<u8.>.)
(declare-fun Poly%strslice%. (strslice%.) Poly)
(declare-fun %Poly%strslice%. (Poly) strslice%.)
(declare-fun Poly%core!cmp.Ordering. (core!cmp.Ordering.) Poly)
(declare-fun %Poly%core!cmp.Ordering. (Poly) core!cmp.Ordering.)
(declare-fun Poly%core!option.Option. (core!option.Option.) Poly)
(declare-fun %Poly%core!option.Option. (Poly) core!option.Option.)
(declare-fun Poly%core!result.Result. (core!result.Result.) Poly)
(declare-fun %Poly%core!result.Result. (Poly) core!result.Result.)
(declare-fun Poly%core!ops.range.Range. (core!ops.range.Range.) Poly)
(declare-fun %Poly%core!ops.range.Range. (Poly) core!ops.range.Range.)
(declare-fun Poly%core!ops.range.Bound. (core!ops.range.Bound.) Poly)
(declare-fun %Poly%core!ops.range.Bound. (Poly) core!ops.range.Bound.)
(declare-fun Poly%vstd!raw_ptr.PtrData. (vstd!raw_ptr.PtrData.) Poly)
(declare-fun %Poly%vstd!raw_ptr.PtrData. (Poly) vstd!raw_ptr.PtrData.)
(declare-fun Poly%det_harness!ComparatorObservation. (det_harness!ComparatorObservation.)
 Poly
)
(declare-fun %Poly%det_harness!ComparatorObservation. (Poly) det_harness!ComparatorObservation.)
(declare-fun Poly%det_harness!SliceIteratorView. (det_harness!SliceIteratorView.)
 Poly
)
(declare-fun %Poly%det_harness!SliceIteratorView. (Poly) det_harness!SliceIteratorView.)
(declare-fun Poly%det_harness!SliceRawMutability. (det_harness!SliceRawMutability.)
 Poly
)
(declare-fun %Poly%det_harness!SliceRawMutability. (Poly) det_harness!SliceRawMutability.)
(declare-fun Poly%det_harness!SliceRawDomain. (det_harness!SliceRawDomain.) Poly)
(declare-fun %Poly%det_harness!SliceRawDomain. (Poly) det_harness!SliceRawDomain.)
(declare-fun Poly%det_harness!MaybeUninitSliceRelation. (det_harness!MaybeUninitSliceRelation.)
 Poly
)
(declare-fun %Poly%det_harness!MaybeUninitSliceRelation. (Poly) det_harness!MaybeUninitSliceRelation.)
(declare-fun Poly%tuple%0. (tuple%0.) Poly)
(declare-fun %Poly%tuple%0. (Poly) tuple%0.)
(declare-fun Poly%tuple%1. (tuple%1.) Poly)
(declare-fun %Poly%tuple%1. (Poly) tuple%1.)
(declare-fun Poly%tuple%2. (tuple%2.) Poly)
(declare-fun %Poly%tuple%2. (Poly) tuple%2.)
(assert
 (forall ((x %%Function%%)) (!
   (= x (%Poly%fun%1. (Poly%fun%1. x)))
   :pattern ((Poly%fun%1. x))
   :qid internal_crate__fun__1_box_axiom_definition
   :skolemid skolem_internal_crate__fun__1_box_axiom_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
    (= x (Poly%fun%1. (%Poly%fun%1. x)))
   )
   :pattern ((has_type x (TYPE%fun%1. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__fun__1_unbox_axiom_definition
   :skolemid skolem_internal_crate__fun__1_unbox_axiom_definition
)))
(declare-fun %%apply%%0 (%%Function%% Poly) Poly)
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (x %%Function%%)) (!
   (=>
    (forall ((T%0 Poly)) (!
      (=>
       (has_type T%0 T%0&)
       (has_type (%%apply%%0 x T%0) T%1&)
      )
      :pattern ((has_type (%%apply%%0 x T%0) T%1&))
      :qid internal_crate__fun__1_constructor_inner_definition
      :skolemid skolem_internal_crate__fun__1_constructor_inner_definition
    ))
    (has_type (Poly%fun%1. (mk_fun x)) (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
   )
   :pattern ((has_type (Poly%fun%1. (mk_fun x)) (TYPE%fun%1. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__fun__1_constructor_definition
   :skolemid skolem_internal_crate__fun__1_constructor_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (T%0 Poly) (x %%Function%%))
  (!
   (=>
    (and
     (has_type (Poly%fun%1. x) (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
     (has_type T%0 T%0&)
    )
    (has_type (%%apply%%0 x T%0) T%1&)
   )
   :pattern ((%%apply%%0 x T%0) (has_type (Poly%fun%1. x) (TYPE%fun%1. T%0&. T%0& T%1&.
      T%1&
   )))
   :qid internal_crate__fun__1_apply_definition
   :skolemid skolem_internal_crate__fun__1_apply_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (T%0 Poly) (x %%Function%%))
  (!
   (=>
    (and
     (has_type (Poly%fun%1. x) (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
     (has_type T%0 T%0&)
    )
    (height_lt (height (%%apply%%0 x T%0)) (height (fun_from_recursive_field (Poly%fun%1.
        (mk_fun x)
   )))))
   :pattern ((height (%%apply%%0 x T%0)) (has_type (Poly%fun%1. x) (TYPE%fun%1. T%0&. T%0&
      T%1&. T%1&
   )))
   :qid internal_crate__fun__1_height_apply_definition
   :skolemid skolem_internal_crate__fun__1_height_apply_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (deep Bool) (x Poly) (y Poly))
  (!
   (=>
    (and
     (has_type x (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
     (has_type y (TYPE%fun%1. T%0&. T%0& T%1&. T%1&))
     (forall ((T%0 Poly)) (!
       (=>
        (has_type T%0 T%0&)
        (ext_eq deep T%1& (%%apply%%0 (%Poly%fun%1. x) T%0) (%%apply%%0 (%Poly%fun%1. y) T%0))
       )
       :pattern ((ext_eq deep T%1& (%%apply%%0 (%Poly%fun%1. x) T%0) (%%apply%%0 (%Poly%fun%1.
           y
          ) T%0
       )))
       :qid internal_crate__fun__1_inner_ext_equal_definition
       :skolemid skolem_internal_crate__fun__1_inner_ext_equal_definition
    )))
    (ext_eq deep (TYPE%fun%1. T%0&. T%0& T%1&. T%1&) x y)
   )
   :pattern ((ext_eq deep (TYPE%fun%1. T%0&. T%0& T%1&. T%1&) x y))
   :qid internal_crate__fun__1_ext_equal_definition
   :skolemid skolem_internal_crate__fun__1_ext_equal_definition
)))
(assert
 (forall ((x %%Function%%)) (!
   (= x (%Poly%array%. (Poly%array%. x)))
   :pattern ((Poly%array%. x))
   :qid internal_crate__array___box_axiom_definition
   :skolemid skolem_internal_crate__array___box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (x Poly)) (!
   (=>
    (has_type x (ARRAY T&. T& N&. N&))
    (= x (Poly%array%. (%Poly%array%. x)))
   )
   :pattern ((has_type x (ARRAY T&. T& N&. N&)))
   :qid internal_crate__array___unbox_axiom_definition
   :skolemid skolem_internal_crate__array___unbox_axiom_definition
)))
(assert
 (forall ((x core!range.Range<usize.>.)) (!
   (= x (%Poly%core!range.Range<usize.>. (Poly%core!range.Range<usize.>. x)))
   :pattern ((Poly%core!range.Range<usize.>. x))
   :qid internal_core__range__Range<usize.>_box_axiom_definition
   :skolemid skolem_internal_core__range__Range<usize.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!range.Range. $ USIZE))
    (= x (Poly%core!range.Range<usize.>. (%Poly%core!range.Range<usize.>. x)))
   )
   :pattern ((has_type x (TYPE%core!range.Range. $ USIZE)))
   :qid internal_core__range__Range<usize.>_unbox_axiom_definition
   :skolemid skolem_internal_core__range__Range<usize.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!range.Range<usize.>.)) (!
   (has_type (Poly%core!range.Range<usize.>. x) (TYPE%core!range.Range. $ USIZE))
   :pattern ((has_type (Poly%core!range.Range<usize.>. x) (TYPE%core!range.Range. $ USIZE)))
   :qid internal_core__range__Range<usize.>_has_type_always_definition
   :skolemid skolem_internal_core__range__Range<usize.>_has_type_always_definition
)))
(assert
 (forall ((x core!slice.GetDisjointMutError.)) (!
   (= x (%Poly%core!slice.GetDisjointMutError. (Poly%core!slice.GetDisjointMutError. x)))
   :pattern ((Poly%core!slice.GetDisjointMutError. x))
   :qid internal_core__slice__GetDisjointMutError_box_axiom_definition
   :skolemid skolem_internal_core__slice__GetDisjointMutError_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%core!slice.GetDisjointMutError.)
    (= x (Poly%core!slice.GetDisjointMutError. (%Poly%core!slice.GetDisjointMutError. x)))
   )
   :pattern ((has_type x TYPE%core!slice.GetDisjointMutError.))
   :qid internal_core__slice__GetDisjointMutError_unbox_axiom_definition
   :skolemid skolem_internal_core__slice__GetDisjointMutError_unbox_axiom_definition
)))
(assert
 (forall ((x core!slice.GetDisjointMutError.)) (!
   (has_type (Poly%core!slice.GetDisjointMutError. x) TYPE%core!slice.GetDisjointMutError.)
   :pattern ((has_type (Poly%core!slice.GetDisjointMutError. x) TYPE%core!slice.GetDisjointMutError.))
   :qid internal_core__slice__GetDisjointMutError_has_type_always_definition
   :skolemid skolem_internal_core__slice__GetDisjointMutError_has_type_always_definition
)))
(assert
 (forall ((x core!slice.ascii.EscapeAscii.)) (!
   (= x (%Poly%core!slice.ascii.EscapeAscii. (Poly%core!slice.ascii.EscapeAscii. x)))
   :pattern ((Poly%core!slice.ascii.EscapeAscii. x))
   :qid internal_core__slice__ascii__EscapeAscii_box_axiom_definition
   :skolemid skolem_internal_core__slice__ascii__EscapeAscii_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%core!slice.ascii.EscapeAscii.)
    (= x (Poly%core!slice.ascii.EscapeAscii. (%Poly%core!slice.ascii.EscapeAscii. x)))
   )
   :pattern ((has_type x TYPE%core!slice.ascii.EscapeAscii.))
   :qid internal_core__slice__ascii__EscapeAscii_unbox_axiom_definition
   :skolemid skolem_internal_core__slice__ascii__EscapeAscii_unbox_axiom_definition
)))
(assert
 (forall ((x core!slice.ascii.EscapeAscii.)) (!
   (has_type (Poly%core!slice.ascii.EscapeAscii. x) TYPE%core!slice.ascii.EscapeAscii.)
   :pattern ((has_type (Poly%core!slice.ascii.EscapeAscii. x) TYPE%core!slice.ascii.EscapeAscii.))
   :qid internal_core__slice__ascii__EscapeAscii_has_type_always_definition
   :skolemid skolem_internal_core__slice__ascii__EscapeAscii_has_type_always_definition
)))
(assert
 (forall ((x core!str.lossy.Utf8Chunks.)) (!
   (= x (%Poly%core!str.lossy.Utf8Chunks. (Poly%core!str.lossy.Utf8Chunks. x)))
   :pattern ((Poly%core!str.lossy.Utf8Chunks. x))
   :qid internal_core__str__lossy__Utf8Chunks_box_axiom_definition
   :skolemid skolem_internal_core__str__lossy__Utf8Chunks_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%core!str.lossy.Utf8Chunks.)
    (= x (Poly%core!str.lossy.Utf8Chunks. (%Poly%core!str.lossy.Utf8Chunks. x)))
   )
   :pattern ((has_type x TYPE%core!str.lossy.Utf8Chunks.))
   :qid internal_core__str__lossy__Utf8Chunks_unbox_axiom_definition
   :skolemid skolem_internal_core__str__lossy__Utf8Chunks_unbox_axiom_definition
)))
(assert
 (forall ((x core!str.lossy.Utf8Chunks.)) (!
   (has_type (Poly%core!str.lossy.Utf8Chunks. x) TYPE%core!str.lossy.Utf8Chunks.)
   :pattern ((has_type (Poly%core!str.lossy.Utf8Chunks. x) TYPE%core!str.lossy.Utf8Chunks.))
   :qid internal_core__str__lossy__Utf8Chunks_has_type_always_definition
   :skolemid skolem_internal_core__str__lossy__Utf8Chunks_has_type_always_definition
)))
(assert
 (forall ((x alloc!alloc.Global.)) (!
   (= x (%Poly%alloc!alloc.Global. (Poly%alloc!alloc.Global. x)))
   :pattern ((Poly%alloc!alloc.Global. x))
   :qid internal_alloc__alloc__Global_box_axiom_definition
   :skolemid skolem_internal_alloc__alloc__Global_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%alloc!alloc.Global.)
    (= x (Poly%alloc!alloc.Global. (%Poly%alloc!alloc.Global. x)))
   )
   :pattern ((has_type x TYPE%alloc!alloc.Global.))
   :qid internal_alloc__alloc__Global_unbox_axiom_definition
   :skolemid skolem_internal_alloc__alloc__Global_unbox_axiom_definition
)))
(assert
 (forall ((x alloc!alloc.Global.)) (!
   (has_type (Poly%alloc!alloc.Global. x) TYPE%alloc!alloc.Global.)
   :pattern ((has_type (Poly%alloc!alloc.Global. x) TYPE%alloc!alloc.Global.))
   :qid internal_alloc__alloc__Global_has_type_always_definition
   :skolemid skolem_internal_alloc__alloc__Global_has_type_always_definition
)))
(assert
 (forall ((x vstd!raw_ptr.Provenance.)) (!
   (= x (%Poly%vstd!raw_ptr.Provenance. (Poly%vstd!raw_ptr.Provenance. x)))
   :pattern ((Poly%vstd!raw_ptr.Provenance. x))
   :qid internal_vstd__raw_ptr__Provenance_box_axiom_definition
   :skolemid skolem_internal_vstd__raw_ptr__Provenance_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%vstd!raw_ptr.Provenance.)
    (= x (Poly%vstd!raw_ptr.Provenance. (%Poly%vstd!raw_ptr.Provenance. x)))
   )
   :pattern ((has_type x TYPE%vstd!raw_ptr.Provenance.))
   :qid internal_vstd__raw_ptr__Provenance_unbox_axiom_definition
   :skolemid skolem_internal_vstd__raw_ptr__Provenance_unbox_axiom_definition
)))
(assert
 (forall ((x vstd!raw_ptr.Provenance.)) (!
   (has_type (Poly%vstd!raw_ptr.Provenance. x) TYPE%vstd!raw_ptr.Provenance.)
   :pattern ((has_type (Poly%vstd!raw_ptr.Provenance. x) TYPE%vstd!raw_ptr.Provenance.))
   :qid internal_vstd__raw_ptr__Provenance_has_type_always_definition
   :skolemid skolem_internal_vstd__raw_ptr__Provenance_has_type_always_definition
)))
(assert
 (forall ((x vstd!seq.Seq<bool.>.)) (!
   (= x (%Poly%vstd!seq.Seq<bool.>. (Poly%vstd!seq.Seq<bool.>. x)))
   :pattern ((Poly%vstd!seq.Seq<bool.>. x))
   :qid internal_vstd__seq__Seq<bool.>_box_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<bool.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!seq.Seq. $ BOOL))
    (= x (Poly%vstd!seq.Seq<bool.>. (%Poly%vstd!seq.Seq<bool.>. x)))
   )
   :pattern ((has_type x (TYPE%vstd!seq.Seq. $ BOOL)))
   :qid internal_vstd__seq__Seq<bool.>_unbox_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<bool.>_unbox_axiom_definition
)))
(assert
 (forall ((x vstd!seq.Seq<bool.>.)) (!
   (has_type (Poly%vstd!seq.Seq<bool.>. x) (TYPE%vstd!seq.Seq. $ BOOL))
   :pattern ((has_type (Poly%vstd!seq.Seq<bool.>. x) (TYPE%vstd!seq.Seq. $ BOOL)))
   :qid internal_vstd__seq__Seq<bool.>_has_type_always_definition
   :skolemid skolem_internal_vstd__seq__Seq<bool.>_has_type_always_definition
)))
(assert
 (forall ((x vstd!seq.Seq<u8.>.)) (!
   (= x (%Poly%vstd!seq.Seq<u8.>. (Poly%vstd!seq.Seq<u8.>. x)))
   :pattern ((Poly%vstd!seq.Seq<u8.>. x))
   :qid internal_vstd__seq__Seq<u8.>_box_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<u8.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!seq.Seq. $ (UINT 8)))
    (= x (Poly%vstd!seq.Seq<u8.>. (%Poly%vstd!seq.Seq<u8.>. x)))
   )
   :pattern ((has_type x (TYPE%vstd!seq.Seq. $ (UINT 8))))
   :qid internal_vstd__seq__Seq<u8.>_unbox_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<u8.>_unbox_axiom_definition
)))
(assert
 (forall ((x vstd!seq.Seq<u8.>.)) (!
   (has_type (Poly%vstd!seq.Seq<u8.>. x) (TYPE%vstd!seq.Seq. $ (UINT 8)))
   :pattern ((has_type (Poly%vstd!seq.Seq<u8.>. x) (TYPE%vstd!seq.Seq. $ (UINT 8))))
   :qid internal_vstd__seq__Seq<u8.>_has_type_always_definition
   :skolemid skolem_internal_vstd__seq__Seq<u8.>_has_type_always_definition
)))
(assert
 (forall ((x vstd!seq.Seq<char.>.)) (!
   (= x (%Poly%vstd!seq.Seq<char.>. (Poly%vstd!seq.Seq<char.>. x)))
   :pattern ((Poly%vstd!seq.Seq<char.>. x))
   :qid internal_vstd__seq__Seq<char.>_box_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<char.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!seq.Seq. $ CHAR))
    (= x (Poly%vstd!seq.Seq<char.>. (%Poly%vstd!seq.Seq<char.>. x)))
   )
   :pattern ((has_type x (TYPE%vstd!seq.Seq. $ CHAR)))
   :qid internal_vstd__seq__Seq<char.>_unbox_axiom_definition
   :skolemid skolem_internal_vstd__seq__Seq<char.>_unbox_axiom_definition
)))
(assert
 (forall ((x vstd!seq.Seq<char.>.)) (!
   (has_type (Poly%vstd!seq.Seq<char.>. x) (TYPE%vstd!seq.Seq. $ CHAR))
   :pattern ((has_type (Poly%vstd!seq.Seq<char.>. x) (TYPE%vstd!seq.Seq. $ CHAR)))
   :qid internal_vstd__seq__Seq<char.>_has_type_always_definition
   :skolemid skolem_internal_vstd__seq__Seq<char.>_has_type_always_definition
)))
(assert
 (forall ((x slice%<u8.>.)) (!
   (= x (%Poly%slice%<u8.>. (Poly%slice%<u8.>. x)))
   :pattern ((Poly%slice%<u8.>. x))
   :qid internal_crate__slice__<u8.>_box_axiom_definition
   :skolemid skolem_internal_crate__slice__<u8.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (SLICE $ (UINT 8)))
    (= x (Poly%slice%<u8.>. (%Poly%slice%<u8.>. x)))
   )
   :pattern ((has_type x (SLICE $ (UINT 8))))
   :qid internal_crate__slice__<u8.>_unbox_axiom_definition
   :skolemid skolem_internal_crate__slice__<u8.>_unbox_axiom_definition
)))
(assert
 (forall ((x slice%<u8.>.)) (!
   (has_type (Poly%slice%<u8.>. x) (SLICE $ (UINT 8)))
   :pattern ((has_type (Poly%slice%<u8.>. x) (SLICE $ (UINT 8))))
   :qid internal_crate__slice__<u8.>_has_type_always_definition
   :skolemid skolem_internal_crate__slice__<u8.>_has_type_always_definition
)))
(assert
 (forall ((x strslice%.)) (!
   (= x (%Poly%strslice%. (Poly%strslice%. x)))
   :pattern ((Poly%strslice%. x))
   :qid internal_crate__strslice___box_axiom_definition
   :skolemid skolem_internal_crate__strslice___box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x STRSLICE)
    (= x (Poly%strslice%. (%Poly%strslice%. x)))
   )
   :pattern ((has_type x STRSLICE))
   :qid internal_crate__strslice___unbox_axiom_definition
   :skolemid skolem_internal_crate__strslice___unbox_axiom_definition
)))
(assert
 (forall ((x strslice%.)) (!
   (has_type (Poly%strslice%. x) STRSLICE)
   :pattern ((has_type (Poly%strslice%. x) STRSLICE))
   :qid internal_crate__strslice___has_type_always_definition
   :skolemid skolem_internal_crate__strslice___has_type_always_definition
)))
(assert
 (forall ((x core!cmp.Ordering.)) (!
   (= x (%Poly%core!cmp.Ordering. (Poly%core!cmp.Ordering. x)))
   :pattern ((Poly%core!cmp.Ordering. x))
   :qid internal_core__cmp__Ordering_box_axiom_definition
   :skolemid skolem_internal_core__cmp__Ordering_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%core!cmp.Ordering.)
    (= x (Poly%core!cmp.Ordering. (%Poly%core!cmp.Ordering. x)))
   )
   :pattern ((has_type x TYPE%core!cmp.Ordering.))
   :qid internal_core__cmp__Ordering_unbox_axiom_definition
   :skolemid skolem_internal_core__cmp__Ordering_unbox_axiom_definition
)))
(assert
 (forall ((x core!cmp.Ordering.)) (!
   (has_type (Poly%core!cmp.Ordering. x) TYPE%core!cmp.Ordering.)
   :pattern ((has_type (Poly%core!cmp.Ordering. x) TYPE%core!cmp.Ordering.))
   :qid internal_core__cmp__Ordering_has_type_always_definition
   :skolemid skolem_internal_core__cmp__Ordering_has_type_always_definition
)))
(assert
 (forall ((x core!option.Option.)) (!
   (= x (%Poly%core!option.Option. (Poly%core!option.Option. x)))
   :pattern ((Poly%core!option.Option. x))
   :qid internal_core__option__Option_box_axiom_definition
   :skolemid skolem_internal_core__option__Option_box_axiom_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!option.Option. V&. V&))
    (= x (Poly%core!option.Option. (%Poly%core!option.Option. x)))
   )
   :pattern ((has_type x (TYPE%core!option.Option. V&. V&)))
   :qid internal_core__option__Option_unbox_axiom_definition
   :skolemid skolem_internal_core__option__Option_unbox_axiom_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type)) (!
   (has_type (Poly%core!option.Option. core!option.Option./None) (TYPE%core!option.Option.
     V&. V&
   ))
   :pattern ((has_type (Poly%core!option.Option. core!option.Option./None) (TYPE%core!option.Option.
      V&. V&
   )))
   :qid internal_core!option.Option./None_constructor_definition
   :skolemid skolem_internal_core!option.Option./None_constructor_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (_0! Poly)) (!
   (=>
    (has_type _0! V&)
    (has_type (Poly%core!option.Option. (core!option.Option./Some _0!)) (TYPE%core!option.Option.
      V&. V&
   )))
   :pattern ((has_type (Poly%core!option.Option. (core!option.Option./Some _0!)) (TYPE%core!option.Option.
      V&. V&
   )))
   :qid internal_core!option.Option./Some_constructor_definition
   :skolemid skolem_internal_core!option.Option./Some_constructor_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (x core!option.Option.)) (!
   (=>
    (is-core!option.Option./Some x)
    (= (core!option.Option./Some/0 V&. V& x) (core!option.Option./Some/?0 x))
   )
   :pattern ((core!option.Option./Some/0 V&. V& x))
   :qid internal_core!option.Option./Some/0_accessor_definition
   :skolemid skolem_internal_core!option.Option./Some/0_accessor_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!option.Option. V&. V&))
    (has_type (core!option.Option./Some/0 V&. V& (%Poly%core!option.Option. x)) V&)
   )
   :pattern ((core!option.Option./Some/0 V&. V& (%Poly%core!option.Option. x)) (has_type
     x (TYPE%core!option.Option. V&. V&)
   ))
   :qid internal_core!option.Option./Some/0_invariant_definition
   :skolemid skolem_internal_core!option.Option./Some/0_invariant_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (x core!option.Option.)) (!
   (=>
    (is-core!option.Option./Some x)
    (height_lt (height (core!option.Option./Some/0 V&. V& x)) (height (Poly%core!option.Option.
       x
   ))))
   :pattern ((height (core!option.Option./Some/0 V&. V& x)))
   :qid prelude_datatype_height_core!option.Option./Some/0
   :skolemid skolem_prelude_datatype_height_core!option.Option./Some/0
)))
(assert
 (forall ((V&. Dcr) (V& Type) (deep Bool) (x Poly) (y Poly)) (!
   (=>
    (and
     (has_type x (TYPE%core!option.Option. V&. V&))
     (has_type y (TYPE%core!option.Option. V&. V&))
     (is-core!option.Option./None (%Poly%core!option.Option. x))
     (is-core!option.Option./None (%Poly%core!option.Option. y))
    )
    (ext_eq deep (TYPE%core!option.Option. V&. V&) x y)
   )
   :pattern ((ext_eq deep (TYPE%core!option.Option. V&. V&) x y))
   :qid internal_core!option.Option./None_ext_equal_definition
   :skolemid skolem_internal_core!option.Option./None_ext_equal_definition
)))
(assert
 (forall ((V&. Dcr) (V& Type) (deep Bool) (x Poly) (y Poly)) (!
   (=>
    (and
     (has_type x (TYPE%core!option.Option. V&. V&))
     (has_type y (TYPE%core!option.Option. V&. V&))
     (is-core!option.Option./Some (%Poly%core!option.Option. x))
     (is-core!option.Option./Some (%Poly%core!option.Option. y))
     (ext_eq deep V& (core!option.Option./Some/0 V&. V& (%Poly%core!option.Option. x))
      (core!option.Option./Some/0 V&. V& (%Poly%core!option.Option. y))
    ))
    (ext_eq deep (TYPE%core!option.Option. V&. V&) x y)
   )
   :pattern ((ext_eq deep (TYPE%core!option.Option. V&. V&) x y))
   :qid internal_core!option.Option./Some_ext_equal_definition
   :skolemid skolem_internal_core!option.Option./Some_ext_equal_definition
)))
(assert
 (forall ((x core!result.Result.)) (!
   (= x (%Poly%core!result.Result. (Poly%core!result.Result. x)))
   :pattern ((Poly%core!result.Result. x))
   :qid internal_core__result__Result_box_axiom_definition
   :skolemid skolem_internal_core__result__Result_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!result.Result. T&. T& E&. E&))
    (= x (Poly%core!result.Result. (%Poly%core!result.Result. x)))
   )
   :pattern ((has_type x (TYPE%core!result.Result. T&. T& E&. E&)))
   :qid internal_core__result__Result_unbox_axiom_definition
   :skolemid skolem_internal_core__result__Result_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (_0! Poly)) (!
   (=>
    (has_type _0! T&)
    (has_type (Poly%core!result.Result. (core!result.Result./Ok _0!)) (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :pattern ((has_type (Poly%core!result.Result. (core!result.Result./Ok _0!)) (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :qid internal_core!result.Result./Ok_constructor_definition
   :skolemid skolem_internal_core!result.Result./Ok_constructor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x core!result.Result.)) (!
   (=>
    (is-core!result.Result./Ok x)
    (= (core!result.Result./Ok/0 T&. T& E&. E& x) (core!result.Result./Ok/?0 x))
   )
   :pattern ((core!result.Result./Ok/0 T&. T& E&. E& x))
   :qid internal_core!result.Result./Ok/0_accessor_definition
   :skolemid skolem_internal_core!result.Result./Ok/0_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!result.Result. T&. T& E&. E&))
    (has_type (core!result.Result./Ok/0 T&. T& E&. E& (%Poly%core!result.Result. x)) T&)
   )
   :pattern ((core!result.Result./Ok/0 T&. T& E&. E& (%Poly%core!result.Result. x)) (
     has_type x (TYPE%core!result.Result. T&. T& E&. E&)
   ))
   :qid internal_core!result.Result./Ok/0_invariant_definition
   :skolemid skolem_internal_core!result.Result./Ok/0_invariant_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (_0! Poly)) (!
   (=>
    (has_type _0! E&)
    (has_type (Poly%core!result.Result. (core!result.Result./Err _0!)) (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :pattern ((has_type (Poly%core!result.Result. (core!result.Result./Err _0!)) (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :qid internal_core!result.Result./Err_constructor_definition
   :skolemid skolem_internal_core!result.Result./Err_constructor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x core!result.Result.)) (!
   (=>
    (is-core!result.Result./Err x)
    (= (core!result.Result./Err/0 T&. T& E&. E& x) (core!result.Result./Err/?0 x))
   )
   :pattern ((core!result.Result./Err/0 T&. T& E&. E& x))
   :qid internal_core!result.Result./Err/0_accessor_definition
   :skolemid skolem_internal_core!result.Result./Err/0_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!result.Result. T&. T& E&. E&))
    (has_type (core!result.Result./Err/0 T&. T& E&. E& (%Poly%core!result.Result. x))
     E&
   ))
   :pattern ((core!result.Result./Err/0 T&. T& E&. E& (%Poly%core!result.Result. x))
    (has_type x (TYPE%core!result.Result. T&. T& E&. E&))
   )
   :qid internal_core!result.Result./Err/0_invariant_definition
   :skolemid skolem_internal_core!result.Result./Err/0_invariant_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x core!result.Result.)) (!
   (=>
    (is-core!result.Result./Ok x)
    (height_lt (height (core!result.Result./Ok/0 T&. T& E&. E& x)) (height (Poly%core!result.Result.
       x
   ))))
   :pattern ((height (core!result.Result./Ok/0 T&. T& E&. E& x)))
   :qid prelude_datatype_height_core!result.Result./Ok/0
   :skolemid skolem_prelude_datatype_height_core!result.Result./Ok/0
)))
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type) (x core!result.Result.)) (!
   (=>
    (is-core!result.Result./Err x)
    (height_lt (height (core!result.Result./Err/0 T&. T& E&. E& x)) (height (Poly%core!result.Result.
       x
   ))))
   :pattern ((height (core!result.Result./Err/0 T&. T& E&. E& x)))
   :qid prelude_datatype_height_core!result.Result./Err/0
   :skolemid skolem_prelude_datatype_height_core!result.Result./Err/0
)))
(assert
 (forall ((x core!ops.range.Range.)) (!
   (= x (%Poly%core!ops.range.Range. (Poly%core!ops.range.Range. x)))
   :pattern ((Poly%core!ops.range.Range. x))
   :qid internal_core__ops__range__Range_box_axiom_definition
   :skolemid skolem_internal_core__ops__range__Range_box_axiom_definition
)))
(assert
 (forall ((Idx&. Dcr) (Idx& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Range. Idx&. Idx&))
    (= x (Poly%core!ops.range.Range. (%Poly%core!ops.range.Range. x)))
   )
   :pattern ((has_type x (TYPE%core!ops.range.Range. Idx&. Idx&)))
   :qid internal_core__ops__range__Range_unbox_axiom_definition
   :skolemid skolem_internal_core__ops__range__Range_unbox_axiom_definition
)))
(assert
 (forall ((Idx&. Dcr) (Idx& Type) (_start! Poly) (_end! Poly)) (!
   (=>
    (and
     (has_type _start! Idx&)
     (has_type _end! Idx&)
    )
    (has_type (Poly%core!ops.range.Range. (core!ops.range.Range./Range _start! _end!))
     (TYPE%core!ops.range.Range. Idx&. Idx&)
   ))
   :pattern ((has_type (Poly%core!ops.range.Range. (core!ops.range.Range./Range _start!
       _end!
      )
     ) (TYPE%core!ops.range.Range. Idx&. Idx&)
   ))
   :qid internal_core!ops.range.Range./Range_constructor_definition
   :skolemid skolem_internal_core!ops.range.Range./Range_constructor_definition
)))
(assert
 (forall ((x core!ops.range.Range.)) (!
   (= (core!ops.range.Range./Range/start x) (core!ops.range.Range./Range/?start x))
   :pattern ((core!ops.range.Range./Range/start x))
   :qid internal_core!ops.range.Range./Range/start_accessor_definition
   :skolemid skolem_internal_core!ops.range.Range./Range/start_accessor_definition
)))
(assert
 (forall ((Idx&. Dcr) (Idx& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Range. Idx&. Idx&))
    (has_type (core!ops.range.Range./Range/start (%Poly%core!ops.range.Range. x)) Idx&)
   )
   :pattern ((core!ops.range.Range./Range/start (%Poly%core!ops.range.Range. x)) (has_type
     x (TYPE%core!ops.range.Range. Idx&. Idx&)
   ))
   :qid internal_core!ops.range.Range./Range/start_invariant_definition
   :skolemid skolem_internal_core!ops.range.Range./Range/start_invariant_definition
)))
(assert
 (forall ((x core!ops.range.Range.)) (!
   (= (core!ops.range.Range./Range/end x) (core!ops.range.Range./Range/?end x))
   :pattern ((core!ops.range.Range./Range/end x))
   :qid internal_core!ops.range.Range./Range/end_accessor_definition
   :skolemid skolem_internal_core!ops.range.Range./Range/end_accessor_definition
)))
(assert
 (forall ((Idx&. Dcr) (Idx& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Range. Idx&. Idx&))
    (has_type (core!ops.range.Range./Range/end (%Poly%core!ops.range.Range. x)) Idx&)
   )
   :pattern ((core!ops.range.Range./Range/end (%Poly%core!ops.range.Range. x)) (has_type
     x (TYPE%core!ops.range.Range. Idx&. Idx&)
   ))
   :qid internal_core!ops.range.Range./Range/end_invariant_definition
   :skolemid skolem_internal_core!ops.range.Range./Range/end_invariant_definition
)))
(assert
 (forall ((x core!ops.range.Range.)) (!
   (=>
    (is-core!ops.range.Range./Range x)
    (height_lt (height (core!ops.range.Range./Range/start x)) (height (Poly%core!ops.range.Range.
       x
   ))))
   :pattern ((height (core!ops.range.Range./Range/start x)))
   :qid prelude_datatype_height_core!ops.range.Range./Range/start
   :skolemid skolem_prelude_datatype_height_core!ops.range.Range./Range/start
)))
(assert
 (forall ((x core!ops.range.Range.)) (!
   (=>
    (is-core!ops.range.Range./Range x)
    (height_lt (height (core!ops.range.Range./Range/end x)) (height (Poly%core!ops.range.Range.
       x
   ))))
   :pattern ((height (core!ops.range.Range./Range/end x)))
   :qid prelude_datatype_height_core!ops.range.Range./Range/end
   :skolemid skolem_prelude_datatype_height_core!ops.range.Range./Range/end
)))
(assert
 (forall ((x core!ops.range.Bound.)) (!
   (= x (%Poly%core!ops.range.Bound. (Poly%core!ops.range.Bound. x)))
   :pattern ((Poly%core!ops.range.Bound. x))
   :qid internal_core__ops__range__Bound_box_axiom_definition
   :skolemid skolem_internal_core__ops__range__Bound_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Bound. T&. T&))
    (= x (Poly%core!ops.range.Bound. (%Poly%core!ops.range.Bound. x)))
   )
   :pattern ((has_type x (TYPE%core!ops.range.Bound. T&. T&)))
   :qid internal_core__ops__range__Bound_unbox_axiom_definition
   :skolemid skolem_internal_core__ops__range__Bound_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_0! Poly)) (!
   (=>
    (has_type _0! T&)
    (has_type (Poly%core!ops.range.Bound. (core!ops.range.Bound./Included _0!)) (TYPE%core!ops.range.Bound.
      T&. T&
   )))
   :pattern ((has_type (Poly%core!ops.range.Bound. (core!ops.range.Bound./Included _0!))
     (TYPE%core!ops.range.Bound. T&. T&)
   ))
   :qid internal_core!ops.range.Bound./Included_constructor_definition
   :skolemid skolem_internal_core!ops.range.Bound./Included_constructor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x core!ops.range.Bound.)) (!
   (=>
    (is-core!ops.range.Bound./Included x)
    (= (core!ops.range.Bound./Included/0 T&. T& x) (core!ops.range.Bound./Included/?0 x))
   )
   :pattern ((core!ops.range.Bound./Included/0 T&. T& x))
   :qid internal_core!ops.range.Bound./Included/0_accessor_definition
   :skolemid skolem_internal_core!ops.range.Bound./Included/0_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Bound. T&. T&))
    (has_type (core!ops.range.Bound./Included/0 T&. T& (%Poly%core!ops.range.Bound. x))
     T&
   ))
   :pattern ((core!ops.range.Bound./Included/0 T&. T& (%Poly%core!ops.range.Bound. x))
    (has_type x (TYPE%core!ops.range.Bound. T&. T&))
   )
   :qid internal_core!ops.range.Bound./Included/0_invariant_definition
   :skolemid skolem_internal_core!ops.range.Bound./Included/0_invariant_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_0! Poly)) (!
   (=>
    (has_type _0! T&)
    (has_type (Poly%core!ops.range.Bound. (core!ops.range.Bound./Excluded _0!)) (TYPE%core!ops.range.Bound.
      T&. T&
   )))
   :pattern ((has_type (Poly%core!ops.range.Bound. (core!ops.range.Bound./Excluded _0!))
     (TYPE%core!ops.range.Bound. T&. T&)
   ))
   :qid internal_core!ops.range.Bound./Excluded_constructor_definition
   :skolemid skolem_internal_core!ops.range.Bound./Excluded_constructor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x core!ops.range.Bound.)) (!
   (=>
    (is-core!ops.range.Bound./Excluded x)
    (= (core!ops.range.Bound./Excluded/0 T&. T& x) (core!ops.range.Bound./Excluded/?0 x))
   )
   :pattern ((core!ops.range.Bound./Excluded/0 T&. T& x))
   :qid internal_core!ops.range.Bound./Excluded/0_accessor_definition
   :skolemid skolem_internal_core!ops.range.Bound./Excluded/0_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%core!ops.range.Bound. T&. T&))
    (has_type (core!ops.range.Bound./Excluded/0 T&. T& (%Poly%core!ops.range.Bound. x))
     T&
   ))
   :pattern ((core!ops.range.Bound./Excluded/0 T&. T& (%Poly%core!ops.range.Bound. x))
    (has_type x (TYPE%core!ops.range.Bound. T&. T&))
   )
   :qid internal_core!ops.range.Bound./Excluded/0_invariant_definition
   :skolemid skolem_internal_core!ops.range.Bound./Excluded/0_invariant_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (has_type (Poly%core!ops.range.Bound. core!ops.range.Bound./Unbounded) (TYPE%core!ops.range.Bound.
     T&. T&
   ))
   :pattern ((has_type (Poly%core!ops.range.Bound. core!ops.range.Bound./Unbounded) (TYPE%core!ops.range.Bound.
      T&. T&
   )))
   :qid internal_core!ops.range.Bound./Unbounded_constructor_definition
   :skolemid skolem_internal_core!ops.range.Bound./Unbounded_constructor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x core!ops.range.Bound.)) (!
   (=>
    (is-core!ops.range.Bound./Included x)
    (height_lt (height (core!ops.range.Bound./Included/0 T&. T& x)) (height (Poly%core!ops.range.Bound.
       x
   ))))
   :pattern ((height (core!ops.range.Bound./Included/0 T&. T& x)))
   :qid prelude_datatype_height_core!ops.range.Bound./Included/0
   :skolemid skolem_prelude_datatype_height_core!ops.range.Bound./Included/0
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x core!ops.range.Bound.)) (!
   (=>
    (is-core!ops.range.Bound./Excluded x)
    (height_lt (height (core!ops.range.Bound./Excluded/0 T&. T& x)) (height (Poly%core!ops.range.Bound.
       x
   ))))
   :pattern ((height (core!ops.range.Bound./Excluded/0 T&. T& x)))
   :qid prelude_datatype_height_core!ops.range.Bound./Excluded/0
   :skolemid skolem_prelude_datatype_height_core!ops.range.Bound./Excluded/0
)))
(assert
 (forall ((x vstd!raw_ptr.PtrData.)) (!
   (= x (%Poly%vstd!raw_ptr.PtrData. (Poly%vstd!raw_ptr.PtrData. x)))
   :pattern ((Poly%vstd!raw_ptr.PtrData. x))
   :qid internal_vstd__raw_ptr__PtrData_box_axiom_definition
   :skolemid skolem_internal_vstd__raw_ptr__PtrData_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
    (= x (Poly%vstd!raw_ptr.PtrData. (%Poly%vstd!raw_ptr.PtrData. x)))
   )
   :pattern ((has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&)))
   :qid internal_vstd__raw_ptr__PtrData_unbox_axiom_definition
   :skolemid skolem_internal_vstd__raw_ptr__PtrData_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_addr! Int) (_provenance! vstd!raw_ptr.Provenance.) (
    _metadata! Poly
   )
  ) (!
   (=>
    (and
     (uInv SZ _addr!)
     (has_type _metadata! (pointee_metadata% T&.))
    )
    (has_type (Poly%vstd!raw_ptr.PtrData. (vstd!raw_ptr.PtrData./PtrData _addr! _provenance!
       _metadata!
      )
     ) (TYPE%vstd!raw_ptr.PtrData. T&. T&)
   ))
   :pattern ((has_type (Poly%vstd!raw_ptr.PtrData. (vstd!raw_ptr.PtrData./PtrData _addr!
       _provenance! _metadata!
      )
     ) (TYPE%vstd!raw_ptr.PtrData. T&. T&)
   ))
   :qid internal_vstd!raw_ptr.PtrData./PtrData_constructor_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData_constructor_definition
)))
(assert
 (forall ((x vstd!raw_ptr.PtrData.)) (!
   (= (vstd!raw_ptr.PtrData./PtrData/addr x) (vstd!raw_ptr.PtrData./PtrData/?addr x))
   :pattern ((vstd!raw_ptr.PtrData./PtrData/addr x))
   :qid internal_vstd!raw_ptr.PtrData./PtrData/addr_accessor_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/addr_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
    (uInv SZ (vstd!raw_ptr.PtrData./PtrData/addr (%Poly%vstd!raw_ptr.PtrData. x)))
   )
   :pattern ((vstd!raw_ptr.PtrData./PtrData/addr (%Poly%vstd!raw_ptr.PtrData. x)) (has_type
     x (TYPE%vstd!raw_ptr.PtrData. T&. T&)
   ))
   :qid internal_vstd!raw_ptr.PtrData./PtrData/addr_invariant_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/addr_invariant_definition
)))
(assert
 (forall ((x vstd!raw_ptr.PtrData.)) (!
   (= (vstd!raw_ptr.PtrData./PtrData/provenance x) (vstd!raw_ptr.PtrData./PtrData/?provenance
     x
   ))
   :pattern ((vstd!raw_ptr.PtrData./PtrData/provenance x))
   :qid internal_vstd!raw_ptr.PtrData./PtrData/provenance_accessor_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/provenance_accessor_definition
)))
(assert
 (forall ((x vstd!raw_ptr.PtrData.)) (!
   (= (vstd!raw_ptr.PtrData./PtrData/metadata x) (vstd!raw_ptr.PtrData./PtrData/?metadata
     x
   ))
   :pattern ((vstd!raw_ptr.PtrData./PtrData/metadata x))
   :qid internal_vstd!raw_ptr.PtrData./PtrData/metadata_accessor_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/metadata_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
    (has_type (vstd!raw_ptr.PtrData./PtrData/metadata (%Poly%vstd!raw_ptr.PtrData. x))
     (pointee_metadata% T&.)
   ))
   :pattern ((vstd!raw_ptr.PtrData./PtrData/metadata (%Poly%vstd!raw_ptr.PtrData. x))
    (has_type x (TYPE%vstd!raw_ptr.PtrData. T&. T&))
   )
   :qid internal_vstd!raw_ptr.PtrData./PtrData/metadata_invariant_definition
   :skolemid skolem_internal_vstd!raw_ptr.PtrData./PtrData/metadata_invariant_definition
)))
(assert
 (forall ((x det_harness!ComparatorObservation.)) (!
   (= x (%Poly%det_harness!ComparatorObservation. (Poly%det_harness!ComparatorObservation.
      x
   )))
   :pattern ((Poly%det_harness!ComparatorObservation. x))
   :qid internal_det_harness__ComparatorObservation_box_axiom_definition
   :skolemid skolem_internal_det_harness__ComparatorObservation_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!ComparatorObservation. T&. T&))
    (= x (Poly%det_harness!ComparatorObservation. (%Poly%det_harness!ComparatorObservation.
       x
   ))))
   :pattern ((has_type x (TYPE%det_harness!ComparatorObservation. T&. T&)))
   :qid internal_det_harness__ComparatorObservation_unbox_axiom_definition
   :skolemid skolem_internal_det_harness__ComparatorObservation_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_domain! Poly) (_trace_id! Int)) (!
   (=>
    (has_type _domain! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (Poly%det_harness!ComparatorObservation. (det_harness!ComparatorObservation./ComparatorObservation
       _domain! _trace_id!
      )
     ) (TYPE%det_harness!ComparatorObservation. T&. T&)
   ))
   :pattern ((has_type (Poly%det_harness!ComparatorObservation. (det_harness!ComparatorObservation./ComparatorObservation
       _domain! _trace_id!
      )
     ) (TYPE%det_harness!ComparatorObservation. T&. T&)
   ))
   :qid internal_det_harness!ComparatorObservation./ComparatorObservation_constructor_definition
   :skolemid skolem_internal_det_harness!ComparatorObservation./ComparatorObservation_constructor_definition
)))
(assert
 (forall ((x det_harness!ComparatorObservation.)) (!
   (= (det_harness!ComparatorObservation./ComparatorObservation/domain x) (det_harness!ComparatorObservation./ComparatorObservation/?domain
     x
   ))
   :pattern ((det_harness!ComparatorObservation./ComparatorObservation/domain x))
   :qid internal_det_harness!ComparatorObservation./ComparatorObservation/domain_accessor_definition
   :skolemid skolem_internal_det_harness!ComparatorObservation./ComparatorObservation/domain_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!ComparatorObservation. T&. T&))
    (has_type (det_harness!ComparatorObservation./ComparatorObservation/domain (%Poly%det_harness!ComparatorObservation.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!ComparatorObservation./ComparatorObservation/domain (%Poly%det_harness!ComparatorObservation.
      x
     )
    ) (has_type x (TYPE%det_harness!ComparatorObservation. T&. T&))
   )
   :qid internal_det_harness!ComparatorObservation./ComparatorObservation/domain_invariant_definition
   :skolemid skolem_internal_det_harness!ComparatorObservation./ComparatorObservation/domain_invariant_definition
)))
(assert
 (forall ((x det_harness!ComparatorObservation.)) (!
   (= (det_harness!ComparatorObservation./ComparatorObservation/trace_id x) (det_harness!ComparatorObservation./ComparatorObservation/?trace_id
     x
   ))
   :pattern ((det_harness!ComparatorObservation./ComparatorObservation/trace_id x))
   :qid internal_det_harness!ComparatorObservation./ComparatorObservation/trace_id_accessor_definition
   :skolemid skolem_internal_det_harness!ComparatorObservation./ComparatorObservation/trace_id_accessor_definition
)))
(assert
 (forall ((x det_harness!ComparatorObservation.)) (!
   (=>
    (is-det_harness!ComparatorObservation./ComparatorObservation x)
    (height_lt (height (det_harness!ComparatorObservation./ComparatorObservation/domain
       x
      )
     ) (height (Poly%det_harness!ComparatorObservation. x))
   ))
   :pattern ((height (det_harness!ComparatorObservation./ComparatorObservation/domain x)))
   :qid prelude_datatype_height_det_harness!ComparatorObservation./ComparatorObservation/domain
   :skolemid skolem_prelude_datatype_height_det_harness!ComparatorObservation./ComparatorObservation/domain
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= x (%Poly%det_harness!SliceIteratorView. (Poly%det_harness!SliceIteratorView. x)))
   :pattern ((Poly%det_harness!SliceIteratorView. x))
   :qid internal_det_harness__SliceIteratorView_box_axiom_definition
   :skolemid skolem_internal_det_harness__SliceIteratorView_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
    (= x (Poly%det_harness!SliceIteratorView. (%Poly%det_harness!SliceIteratorView. x)))
   )
   :pattern ((has_type x (TYPE%det_harness!SliceIteratorView. T&. T&)))
   :qid internal_det_harness__SliceIteratorView_unbox_axiom_definition
   :skolemid skolem_internal_det_harness__SliceIteratorView_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_source! Poly) (_remaining! Poly) (_yielded_prefix! Poly)
   (_remainder! Poly) (_chunk_size! Int) (_reverse! Bool)
  ) (!
   (=>
    (and
     (has_type _source! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type _remaining! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type _yielded_prefix! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type _remainder! (TYPE%vstd!seq.Seq. T&. T&))
    )
    (has_type (Poly%det_harness!SliceIteratorView. (det_harness!SliceIteratorView./SliceIteratorView
       _source! _remaining! _yielded_prefix! _remainder! _chunk_size! _reverse!
      )
     ) (TYPE%det_harness!SliceIteratorView. T&. T&)
   ))
   :pattern ((has_type (Poly%det_harness!SliceIteratorView. (det_harness!SliceIteratorView./SliceIteratorView
       _source! _remaining! _yielded_prefix! _remainder! _chunk_size! _reverse!
      )
     ) (TYPE%det_harness!SliceIteratorView. T&. T&)
   ))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView_constructor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView_constructor_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/source x) (det_harness!SliceIteratorView./SliceIteratorView/?source
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/source x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/source_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/source_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
    (has_type (det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
      x
     )
    ) (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
   )
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/source_invariant_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/source_invariant_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/remaining x) (det_harness!SliceIteratorView./SliceIteratorView/?remaining
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/remaining x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/remaining_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/remaining_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
    (has_type (det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
      x
     )
    ) (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
   )
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/remaining_invariant_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/remaining_invariant_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix x) (det_harness!SliceIteratorView./SliceIteratorView/?yielded_prefix
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
    (has_type (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix (%Poly%det_harness!SliceIteratorView.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix (%Poly%det_harness!SliceIteratorView.
      x
     )
    ) (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
   )
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix_invariant_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix_invariant_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/remainder x) (det_harness!SliceIteratorView./SliceIteratorView/?remainder
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/remainder x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/remainder_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/remainder_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
    (has_type (det_harness!SliceIteratorView./SliceIteratorView/remainder (%Poly%det_harness!SliceIteratorView.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/remainder (%Poly%det_harness!SliceIteratorView.
      x
     )
    ) (has_type x (TYPE%det_harness!SliceIteratorView. T&. T&))
   )
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/remainder_invariant_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/remainder_invariant_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/chunk_size x) (det_harness!SliceIteratorView./SliceIteratorView/?chunk_size
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/chunk_size x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/chunk_size_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/chunk_size_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (= (det_harness!SliceIteratorView./SliceIteratorView/reverse x) (det_harness!SliceIteratorView./SliceIteratorView/?reverse
     x
   ))
   :pattern ((det_harness!SliceIteratorView./SliceIteratorView/reverse x))
   :qid internal_det_harness!SliceIteratorView./SliceIteratorView/reverse_accessor_definition
   :skolemid skolem_internal_det_harness!SliceIteratorView./SliceIteratorView/reverse_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (=>
    (is-det_harness!SliceIteratorView./SliceIteratorView x)
    (height_lt (height (det_harness!SliceIteratorView./SliceIteratorView/source x)) (height
      (Poly%det_harness!SliceIteratorView. x)
   )))
   :pattern ((height (det_harness!SliceIteratorView./SliceIteratorView/source x)))
   :qid prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/source
   :skolemid skolem_prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/source
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (=>
    (is-det_harness!SliceIteratorView./SliceIteratorView x)
    (height_lt (height (det_harness!SliceIteratorView./SliceIteratorView/remaining x))
     (height (Poly%det_harness!SliceIteratorView. x))
   ))
   :pattern ((height (det_harness!SliceIteratorView./SliceIteratorView/remaining x)))
   :qid prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/remaining
   :skolemid skolem_prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/remaining
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (=>
    (is-det_harness!SliceIteratorView./SliceIteratorView x)
    (height_lt (height (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
       x
      )
     ) (height (Poly%det_harness!SliceIteratorView. x))
   ))
   :pattern ((height (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix x)))
   :qid prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
   :skolemid skolem_prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
)))
(assert
 (forall ((x det_harness!SliceIteratorView.)) (!
   (=>
    (is-det_harness!SliceIteratorView./SliceIteratorView x)
    (height_lt (height (det_harness!SliceIteratorView./SliceIteratorView/remainder x))
     (height (Poly%det_harness!SliceIteratorView. x))
   ))
   :pattern ((height (det_harness!SliceIteratorView./SliceIteratorView/remainder x)))
   :qid prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/remainder
   :skolemid skolem_prelude_datatype_height_det_harness!SliceIteratorView./SliceIteratorView/remainder
)))
(assert
 (forall ((x det_harness!SliceRawMutability.)) (!
   (= x (%Poly%det_harness!SliceRawMutability. (Poly%det_harness!SliceRawMutability. x)))
   :pattern ((Poly%det_harness!SliceRawMutability. x))
   :qid internal_det_harness__SliceRawMutability_box_axiom_definition
   :skolemid skolem_internal_det_harness__SliceRawMutability_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%det_harness!SliceRawMutability.)
    (= x (Poly%det_harness!SliceRawMutability. (%Poly%det_harness!SliceRawMutability. x)))
   )
   :pattern ((has_type x TYPE%det_harness!SliceRawMutability.))
   :qid internal_det_harness__SliceRawMutability_unbox_axiom_definition
   :skolemid skolem_internal_det_harness__SliceRawMutability_unbox_axiom_definition
)))
(assert
 (forall ((x det_harness!SliceRawMutability.)) (!
   (has_type (Poly%det_harness!SliceRawMutability. x) TYPE%det_harness!SliceRawMutability.)
   :pattern ((has_type (Poly%det_harness!SliceRawMutability. x) TYPE%det_harness!SliceRawMutability.))
   :qid internal_det_harness__SliceRawMutability_has_type_always_definition
   :skolemid skolem_internal_det_harness__SliceRawMutability_has_type_always_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= x (%Poly%det_harness!SliceRawDomain. (Poly%det_harness!SliceRawDomain. x)))
   :pattern ((Poly%det_harness!SliceRawDomain. x))
   :qid internal_det_harness__SliceRawDomain_box_axiom_definition
   :skolemid skolem_internal_det_harness__SliceRawDomain_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%det_harness!SliceRawDomain.)
    (= x (Poly%det_harness!SliceRawDomain. (%Poly%det_harness!SliceRawDomain. x)))
   )
   :pattern ((has_type x TYPE%det_harness!SliceRawDomain.))
   :qid internal_det_harness__SliceRawDomain_unbox_axiom_definition
   :skolemid skolem_internal_det_harness__SliceRawDomain_unbox_axiom_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/len x) (det_harness!SliceRawDomain./SliceRawDomain/?len
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/len x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/len_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/len_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/non_null x) (det_harness!SliceRawDomain./SliceRawDomain/?non_null
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/non_null x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/non_null_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/non_null_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/aligned x) (det_harness!SliceRawDomain./SliceRawDomain/?aligned
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/aligned x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/aligned_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/aligned_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/one_allocation x) (det_harness!SliceRawDomain./SliceRawDomain/?one_allocation
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/one_allocation x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/one_allocation_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/one_allocation_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/initialized x) (det_harness!SliceRawDomain./SliceRawDomain/?initialized
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/initialized x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/initialized_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/initialized_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok x) (det_harness!SliceRawDomain./SliceRawDomain/?aliasing_ok
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/within_isize x) (det_harness!SliceRawDomain./SliceRawDomain/?within_isize
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/within_isize x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/within_isize_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/within_isize_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (= (det_harness!SliceRawDomain./SliceRawDomain/mutability x) (det_harness!SliceRawDomain./SliceRawDomain/?mutability
     x
   ))
   :pattern ((det_harness!SliceRawDomain./SliceRawDomain/mutability x))
   :qid internal_det_harness!SliceRawDomain./SliceRawDomain/mutability_accessor_definition
   :skolemid skolem_internal_det_harness!SliceRawDomain./SliceRawDomain/mutability_accessor_definition
)))
(assert
 (forall ((x det_harness!SliceRawDomain.)) (!
   (has_type (Poly%det_harness!SliceRawDomain. x) TYPE%det_harness!SliceRawDomain.)
   :pattern ((has_type (Poly%det_harness!SliceRawDomain. x) TYPE%det_harness!SliceRawDomain.))
   :qid internal_det_harness__SliceRawDomain_has_type_always_definition
   :skolemid skolem_internal_det_harness__SliceRawDomain_has_type_always_definition
)))
(assert
 (forall ((x det_harness!MaybeUninitSliceRelation.)) (!
   (= x (%Poly%det_harness!MaybeUninitSliceRelation. (Poly%det_harness!MaybeUninitSliceRelation.
      x
   )))
   :pattern ((Poly%det_harness!MaybeUninitSliceRelation. x))
   :qid internal_det_harness__MaybeUninitSliceRelation_box_axiom_definition
   :skolemid skolem_internal_det_harness__MaybeUninitSliceRelation_box_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&))
    (= x (Poly%det_harness!MaybeUninitSliceRelation. (%Poly%det_harness!MaybeUninitSliceRelation.
       x
   ))))
   :pattern ((has_type x (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&)))
   :qid internal_det_harness__MaybeUninitSliceRelation_unbox_axiom_definition
   :skolemid skolem_internal_det_harness__MaybeUninitSliceRelation_unbox_axiom_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (_initialized! vstd!seq.Seq<bool.>.) (_values! Poly))
  (!
   (=>
    (has_type _values! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (Poly%det_harness!MaybeUninitSliceRelation. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation
       _initialized! _values!
      )
     ) (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&)
   ))
   :pattern ((has_type (Poly%det_harness!MaybeUninitSliceRelation. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation
       _initialized! _values!
      )
     ) (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&)
   ))
   :qid internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation_constructor_definition
   :skolemid skolem_internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation_constructor_definition
)))
(assert
 (forall ((x det_harness!MaybeUninitSliceRelation.)) (!
   (= (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized x)
    (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/?initialized x)
   )
   :pattern ((det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
     x
   ))
   :qid internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized_accessor_definition
   :skolemid skolem_internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized_accessor_definition
)))
(assert
 (forall ((x det_harness!MaybeUninitSliceRelation.)) (!
   (= (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values x) (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/?values
     x
   ))
   :pattern ((det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values x))
   :qid internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values_accessor_definition
   :skolemid skolem_internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values_accessor_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&))
    (has_type (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values (%Poly%det_harness!MaybeUninitSliceRelation.
       x
      )
     ) (TYPE%vstd!seq.Seq. T&. T&)
   ))
   :pattern ((det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values (%Poly%det_harness!MaybeUninitSliceRelation.
      x
     )
    ) (has_type x (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&))
   )
   :qid internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values_invariant_definition
   :skolemid skolem_internal_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values_invariant_definition
)))
(assert
 (forall ((x det_harness!MaybeUninitSliceRelation.)) (!
   (=>
    (is-det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation x)
    (height_lt (height (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
       x
      )
     ) (height (Poly%det_harness!MaybeUninitSliceRelation. x))
   ))
   :pattern ((height (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
      x
   )))
   :qid prelude_datatype_height_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
   :skolemid skolem_prelude_datatype_height_det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
)))
(assert
 (forall ((x tuple%0.)) (!
   (= x (%Poly%tuple%0. (Poly%tuple%0. x)))
   :pattern ((Poly%tuple%0. x))
   :qid internal_crate__tuple__0_box_axiom_definition
   :skolemid skolem_internal_crate__tuple__0_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x TYPE%tuple%0.)
    (= x (Poly%tuple%0. (%Poly%tuple%0. x)))
   )
   :pattern ((has_type x TYPE%tuple%0.))
   :qid internal_crate__tuple__0_unbox_axiom_definition
   :skolemid skolem_internal_crate__tuple__0_unbox_axiom_definition
)))
(assert
 (forall ((x tuple%0.)) (!
   (has_type (Poly%tuple%0. x) TYPE%tuple%0.)
   :pattern ((has_type (Poly%tuple%0. x) TYPE%tuple%0.))
   :qid internal_crate__tuple__0_has_type_always_definition
   :skolemid skolem_internal_crate__tuple__0_has_type_always_definition
)))
(assert
 (forall ((x tuple%1.)) (!
   (= x (%Poly%tuple%1. (Poly%tuple%1. x)))
   :pattern ((Poly%tuple%1. x))
   :qid internal_crate__tuple__1_box_axiom_definition
   :skolemid skolem_internal_crate__tuple__1_box_axiom_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%tuple%1. T%0&. T%0&))
    (= x (Poly%tuple%1. (%Poly%tuple%1. x)))
   )
   :pattern ((has_type x (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_crate__tuple__1_unbox_axiom_definition
   :skolemid skolem_internal_crate__tuple__1_unbox_axiom_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (_0! Poly)) (!
   (=>
    (has_type _0! T%0&)
    (has_type (Poly%tuple%1. (tuple%1./tuple%1 _0!)) (TYPE%tuple%1. T%0&. T%0&))
   )
   :pattern ((has_type (Poly%tuple%1. (tuple%1./tuple%1 _0!)) (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_tuple__1./tuple__1_constructor_definition
   :skolemid skolem_internal_tuple__1./tuple__1_constructor_definition
)))
(assert
 (forall ((x tuple%1.)) (!
   (= (tuple%1./tuple%1/0 x) (tuple%1./tuple%1/?0 x))
   :pattern ((tuple%1./tuple%1/0 x))
   :qid internal_tuple__1./tuple__1/0_accessor_definition
   :skolemid skolem_internal_tuple__1./tuple__1/0_accessor_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%tuple%1. T%0&. T%0&))
    (has_type (tuple%1./tuple%1/0 (%Poly%tuple%1. x)) T%0&)
   )
   :pattern ((tuple%1./tuple%1/0 (%Poly%tuple%1. x)) (has_type x (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_tuple__1./tuple__1/0_invariant_definition
   :skolemid skolem_internal_tuple__1./tuple__1/0_invariant_definition
)))
(assert
 (forall ((x tuple%1.)) (!
   (=>
    (is-tuple%1./tuple%1 x)
    (height_lt (height (tuple%1./tuple%1/0 x)) (height (Poly%tuple%1. x)))
   )
   :pattern ((height (tuple%1./tuple%1/0 x)))
   :qid prelude_datatype_height_tuple%1./tuple%1/0
   :skolemid skolem_prelude_datatype_height_tuple%1./tuple%1/0
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (deep Bool) (x Poly) (y Poly)) (!
   (=>
    (and
     (has_type x (TYPE%tuple%1. T%0&. T%0&))
     (has_type y (TYPE%tuple%1. T%0&. T%0&))
     (ext_eq deep T%0& (tuple%1./tuple%1/0 (%Poly%tuple%1. x)) (tuple%1./tuple%1/0 (%Poly%tuple%1.
        y
    ))))
    (ext_eq deep (TYPE%tuple%1. T%0&. T%0&) x y)
   )
   :pattern ((ext_eq deep (TYPE%tuple%1. T%0&. T%0&) x y))
   :qid internal_tuple__1./tuple__1_ext_equal_definition
   :skolemid skolem_internal_tuple__1./tuple__1_ext_equal_definition
)))
(assert
 (forall ((x tuple%2.)) (!
   (= x (%Poly%tuple%2. (Poly%tuple%2. x)))
   :pattern ((Poly%tuple%2. x))
   :qid internal_crate__tuple__2_box_axiom_definition
   :skolemid skolem_internal_crate__tuple__2_box_axiom_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
    (= x (Poly%tuple%2. (%Poly%tuple%2. x)))
   )
   :pattern ((has_type x (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__tuple__2_unbox_axiom_definition
   :skolemid skolem_internal_crate__tuple__2_unbox_axiom_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (_0! Poly) (_1! Poly)) (!
   (=>
    (and
     (has_type _0! T%0&)
     (has_type _1! T%1&)
    )
    (has_type (Poly%tuple%2. (tuple%2./tuple%2 _0! _1!)) (TYPE%tuple%2. T%0&. T%0& T%1&.
      T%1&
   )))
   :pattern ((has_type (Poly%tuple%2. (tuple%2./tuple%2 _0! _1!)) (TYPE%tuple%2. T%0&.
      T%0& T%1&. T%1&
   )))
   :qid internal_tuple__2./tuple__2_constructor_definition
   :skolemid skolem_internal_tuple__2./tuple__2_constructor_definition
)))
(assert
 (forall ((x tuple%2.)) (!
   (= (tuple%2./tuple%2/0 x) (tuple%2./tuple%2/?0 x))
   :pattern ((tuple%2./tuple%2/0 x))
   :qid internal_tuple__2./tuple__2/0_accessor_definition
   :skolemid skolem_internal_tuple__2./tuple__2/0_accessor_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
    (has_type (tuple%2./tuple%2/0 (%Poly%tuple%2. x)) T%0&)
   )
   :pattern ((tuple%2./tuple%2/0 (%Poly%tuple%2. x)) (has_type x (TYPE%tuple%2. T%0&. T%0&
      T%1&. T%1&
   )))
   :qid internal_tuple__2./tuple__2/0_invariant_definition
   :skolemid skolem_internal_tuple__2./tuple__2/0_invariant_definition
)))
(assert
 (forall ((x tuple%2.)) (!
   (= (tuple%2./tuple%2/1 x) (tuple%2./tuple%2/?1 x))
   :pattern ((tuple%2./tuple%2/1 x))
   :qid internal_tuple__2./tuple__2/1_accessor_definition
   :skolemid skolem_internal_tuple__2./tuple__2/1_accessor_definition
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (x Poly)) (!
   (=>
    (has_type x (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
    (has_type (tuple%2./tuple%2/1 (%Poly%tuple%2. x)) T%1&)
   )
   :pattern ((tuple%2./tuple%2/1 (%Poly%tuple%2. x)) (has_type x (TYPE%tuple%2. T%0&. T%0&
      T%1&. T%1&
   )))
   :qid internal_tuple__2./tuple__2/1_invariant_definition
   :skolemid skolem_internal_tuple__2./tuple__2/1_invariant_definition
)))
(assert
 (forall ((x tuple%2.)) (!
   (=>
    (is-tuple%2./tuple%2 x)
    (height_lt (height (tuple%2./tuple%2/0 x)) (height (Poly%tuple%2. x)))
   )
   :pattern ((height (tuple%2./tuple%2/0 x)))
   :qid prelude_datatype_height_tuple%2./tuple%2/0
   :skolemid skolem_prelude_datatype_height_tuple%2./tuple%2/0
)))
(assert
 (forall ((x tuple%2.)) (!
   (=>
    (is-tuple%2./tuple%2 x)
    (height_lt (height (tuple%2./tuple%2/1 x)) (height (Poly%tuple%2. x)))
   )
   :pattern ((height (tuple%2./tuple%2/1 x)))
   :qid prelude_datatype_height_tuple%2./tuple%2/1
   :skolemid skolem_prelude_datatype_height_tuple%2./tuple%2/1
)))
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type) (deep Bool) (x Poly) (y Poly))
  (!
   (=>
    (and
     (has_type x (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
     (has_type y (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
     (ext_eq deep T%0& (tuple%2./tuple%2/0 (%Poly%tuple%2. x)) (tuple%2./tuple%2/0 (%Poly%tuple%2.
        y
     )))
     (ext_eq deep T%1& (tuple%2./tuple%2/1 (%Poly%tuple%2. x)) (tuple%2./tuple%2/1 (%Poly%tuple%2.
        y
    ))))
    (ext_eq deep (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&) x y)
   )
   :pattern ((ext_eq deep (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&) x y))
   :qid internal_tuple__2./tuple__2_ext_equal_definition
   :skolemid skolem_internal_tuple__2./tuple__2_ext_equal_definition
)))
(declare-fun array_new (Dcr Type Int %%Function%%) Poly)
(declare-fun array_index (Dcr Type Dcr Type %%Function%% Poly) Poly)
(assert
 (forall ((Tdcr Dcr) (T Type) (N Int) (Fn %%Function%%)) (!
   (= (array_new Tdcr T N Fn) (Poly%array%. Fn))
   :pattern ((array_new Tdcr T N Fn))
   :qid prelude_array_new
   :skolemid skolem_prelude_array_new
)))
(declare-fun %%apply%%1 (%%Function%% Int) Poly)
(assert
 (forall ((Tdcr Dcr) (T Type) (N Int) (Fn %%Function%%)) (!
   (=>
    (forall ((i Int)) (!
      (=>
       (and
        (<= 0 i)
        (< i N)
       )
       (has_type (%%apply%%1 Fn i) T)
      )
      :pattern ((has_type (%%apply%%1 Fn i) T))
      :qid prelude_has_type_array_elts
      :skolemid skolem_prelude_has_type_array_elts
    ))
    (has_type (array_new Tdcr T N Fn) (ARRAY Tdcr T $ (CONST_INT N)))
   )
   :pattern ((array_new Tdcr T N Fn))
   :qid prelude_has_type_array_new
   :skolemid skolem_prelude_has_type_array_new
)))
(assert
 (forall ((Tdcr Dcr) (T Type) (Nd Dcr) (Ndcr Dcr) (N Type) (Fn %%Function%%) (i Poly))
  (!
   (=>
    (and
     (has_type (Poly%array%. Fn) (ARRAY Tdcr T Ndcr N))
     (has_type i INT)
    )
    (has_type (array_index Tdcr T Nd N Fn i) T)
   )
   :pattern ((array_index Tdcr T Nd N Fn i) (has_type (Poly%array%. Fn) (ARRAY Tdcr T Ndcr
      N
   )))
   :qid prelude_has_type_array_index
   :skolemid skolem_prelude_has_type_array_index
)))
(assert
 (!
  (forall ((Tdcr Dcr) (T Type) (N Int) (Fn %%Function%%) (i Int)) (!
    (= (array_index Tdcr T $ (CONST_INT N) Fn (I i)) (%%apply%%1 Fn i))
    :pattern ((array_new Tdcr T N Fn) (%%apply%%1 Fn i))
    :qid prelude_array_index_trigger
    :skolemid skolem_prelude_array_index_trigger
  ))
  :named
  prelude_axiom_array_index
))
(declare-fun str%strslice_len (strslice%.) Int)
(declare-fun str%strslice_get_char (strslice%. Int) Int)
(declare-fun str%new_strlit (Int) strslice%.)
(declare-fun str%from_strlit (strslice%.) Int)
(assert
 (forall ((x Int)) (!
   (= (str%from_strlit (str%new_strlit x)) x)
   :pattern ((str%new_strlit x))
   :qid prelude_strlit_injective
   :skolemid skolem_prelude_strlit_injective
)))

;; Trait-Bounds
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (tr_bound%vstd!array.ArrayAdditionalSpecFns. Self%&. Self%& T&. T&)
    (and
     (tr_bound%vstd!view.View. Self%&. Self%&)
     (and
      (= $ (proj%%vstd!view.View./V Self%&. Self%&))
      (= (TYPE%vstd!seq.Seq. T&. T&) (proj%vstd!view.View./V Self%&. Self%&))
     )
     (sized T&.)
   ))
   :pattern ((tr_bound%vstd!array.ArrayAdditionalSpecFns. Self%&. Self%& T&. T&))
   :qid internal_vstd__array__ArrayAdditionalSpecFns_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__array__ArrayAdditionalSpecFns_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (tr_bound%vstd!slice.SliceAdditionalSpecFns. Self%&. Self%& T&. T&)
    (and
     (tr_bound%vstd!view.View. Self%&. Self%&)
     (and
      (= $ (proj%%vstd!view.View./V Self%&. Self%&))
      (= (TYPE%vstd!seq.Seq. T&. T&) (proj%vstd!view.View./V Self%&. Self%&))
     )
     (sized T&.)
   ))
   :pattern ((tr_bound%vstd!slice.SliceAdditionalSpecFns. Self%&. Self%& T&. T&))
   :qid internal_vstd__slice__SliceAdditionalSpecFns_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__slice__SliceAdditionalSpecFns_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   true
   :pattern ((tr_bound%core!slice.index.SliceIndex. Self%&. Self%& T&. T&))
   :qid internal_core__slice__index__SliceIndex_trait_type_bounds_definition
   :skolemid skolem_internal_core__slice__index__SliceIndex_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%vstd!view.View. Self%&. Self%&)
    (sized (proj%%vstd!view.View./V Self%&. Self%&))
   )
   :pattern ((tr_bound%vstd!view.View. Self%&. Self%&))
   :qid internal_vstd__view__View_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__view__View_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%core!clone.Clone. Self%&. Self%&)
    (sized Self%&.)
   )
   :pattern ((tr_bound%core!clone.Clone. Self%&. Self%&))
   :qid internal_core__clone__Clone_trait_type_bounds_definition
   :skolemid skolem_internal_core__clone__Clone_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%core!marker.Copy. Self%&. Self%&)
    (tr_bound%core!clone.Clone. Self%&. Self%&)
   )
   :pattern ((tr_bound%core!marker.Copy. Self%&. Self%&))
   :qid internal_core__marker__Copy_trait_type_bounds_definition
   :skolemid skolem_internal_core__marker__Copy_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (Rhs&. Dcr) (Rhs& Type)) (!
   true
   :pattern ((tr_bound%core!cmp.PartialEq. Self%&. Self%& Rhs&. Rhs&))
   :qid internal_core__cmp__PartialEq_trait_type_bounds_definition
   :skolemid skolem_internal_core__cmp__PartialEq_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%core!cmp.Eq. Self%&. Self%&)
    (tr_bound%core!cmp.PartialEq. Self%&. Self%& Self%&. Self%&)
   )
   :pattern ((tr_bound%core!cmp.Eq. Self%&. Self%&))
   :qid internal_core__cmp__Eq_trait_type_bounds_definition
   :skolemid skolem_internal_core__cmp__Eq_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (Rhs&. Dcr) (Rhs& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialOrd. Self%&. Self%& Rhs&. Rhs&)
    (tr_bound%core!cmp.PartialEq. Self%&. Self%& Rhs&. Rhs&)
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. Self%&. Self%& Rhs&. Rhs&))
   :qid internal_core__cmp__PartialOrd_trait_type_bounds_definition
   :skolemid skolem_internal_core__cmp__PartialOrd_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%core!cmp.Ord. Self%&. Self%&)
    (and
     (tr_bound%core!cmp.Eq. Self%&. Self%&)
     (tr_bound%core!cmp.PartialOrd. Self%&. Self%& Self%&. Self%&)
   ))
   :pattern ((tr_bound%core!cmp.Ord. Self%&. Self%&))
   :qid internal_core__cmp__Ord_trait_type_bounds_definition
   :skolemid skolem_internal_core__cmp__Ord_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   true
   :pattern ((tr_bound%core!marker.Tuple. Self%&. Self%&))
   :qid internal_core__marker__Tuple_trait_type_bounds_definition
   :skolemid skolem_internal_core__marker__Tuple_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type)) (!
   (=>
    (tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&)
    (and
     (sized Args&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (sized (proj%%core!ops.function.FnOnce./Output Self%&. Self%& Args&. Args&))
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&))
   :qid internal_core__ops__function__FnOnce_trait_type_bounds_definition
   :skolemid skolem_internal_core__ops__function__FnOnce_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type)) (!
   (=>
    (tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&)
    (and
     (tr_bound%core!ops.function.FnOnce. Self%&. Self%& Args&. Args&)
     (sized Args&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&))
   :qid internal_core__ops__function__FnMut_trait_type_bounds_definition
   :skolemid skolem_internal_core__ops__function__FnMut_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (Args&. Dcr) (Args& Type)) (!
   (=>
    (tr_bound%core!ops.function.Fn. Self%&. Self%& Args&. Args&)
    (and
     (tr_bound%core!ops.function.FnMut. Self%&. Self%& Args&. Args&)
     (sized Args&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
   ))
   :pattern ((tr_bound%core!ops.function.Fn. Self%&. Self%& Args&. Args&))
   :qid internal_core__ops__function__Fn_trait_type_bounds_definition
   :skolemid skolem_internal_core__ops__function__Fn_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   true
   :pattern ((tr_bound%core!alloc.Allocator. Self%&. Self%&))
   :qid internal_core__alloc__Allocator_trait_type_bounds_definition
   :skolemid skolem_internal_core__alloc__Allocator_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (tr_bound%vstd!std_specs.option.OptionAdditionalFns. Self%&. Self%& T&. T&)
    (and
     (sized Self%&.)
     (sized T&.)
   ))
   :pattern ((tr_bound%vstd!std_specs.option.OptionAdditionalFns. Self%&. Self%& T&. T&))
   :qid internal_vstd__std_specs__option__OptionAdditionalFns_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__std_specs__option__OptionAdditionalFns_trait_type_bounds_definition
)))

;; Associated-Type-Impls
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (= (proj%%vstd!view.View./V $ (ARRAY T&. T& N&. N&)) $)
   )
   :pattern ((proj%%vstd!view.View./V $ (ARRAY T&. T& N&. N&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (= (proj%vstd!view.View./V $ (ARRAY T&. T& N&. N&)) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((proj%vstd!view.View./V $ (ARRAY T&. T& N&. N&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%%vstd!view.View./V $ (PTR T&. T&)) $)
   :pattern ((proj%%vstd!view.View./V $ (PTR T&. T&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%vstd!view.View./V $ (PTR T&. T&)) (TYPE%vstd!raw_ptr.PtrData. T&. T&))
   :pattern ((proj%vstd!view.View./V $ (PTR T&. T&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)) $)
   :pattern ((proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)) (TYPE%vstd!raw_ptr.PtrData.
     T&. T&
   ))
   :pattern ((proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%vstd!view.View./V $slice (SLICE T&. T&)) $)
   )
   :pattern ((proj%%vstd!view.View./V $slice (SLICE T&. T&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%vstd!view.View./V $slice (SLICE T&. T&)) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((proj%vstd!view.View./V $slice (SLICE T&. T&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%vstd!view.View./V $slice STRSLICE) $)
)
(assert
 (= (proj%vstd!view.View./V $slice STRSLICE) (TYPE%vstd!seq.Seq. $ CHAR))
)
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%%vstd!view.View./V (REF A&.) A&) (proj%%vstd!view.View./V A&. A&))
   )
   :pattern ((proj%%vstd!view.View./V (REF A&.) A&))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%vstd!view.View./V (REF A&.) A&) (proj%vstd!view.View./V A&. A&))
   )
   :pattern ((proj%vstd!view.View./V (REF A&.) A&))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&) (proj%%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&) (proj%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (= (proj%%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&) (proj%%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (= (proj%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&) (proj%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%vstd!view.View./V (RC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (= (proj%%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&) (proj%%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (= (proj%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&) (proj%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%vstd!view.View./V (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%vstd!view.View./V $ (TYPE%core!option.Option. T&. T&)) $)
   )
   :pattern ((proj%%vstd!view.View./V $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%vstd!view.View./V $ (TYPE%core!option.Option. T&. T&)) (TYPE%core!option.Option.
      T&. T&
   )))
   :pattern ((proj%vstd!view.View./V $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%vstd!view.View./V $ TYPE%tuple%0.) $)
)
(assert
 (= (proj%vstd!view.View./V $ TYPE%tuple%0.) TYPE%tuple%0.)
)
(assert
 (= (proj%%vstd!view.View./V $ BOOL) $)
)
(assert
 (= (proj%vstd!view.View./V $ BOOL) BOOL)
)
(assert
 (= (proj%%vstd!view.View./V $ (UINT 8)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (UINT 8)) (UINT 8))
)
(assert
 (= (proj%%vstd!view.View./V $ USIZE) $)
)
(assert
 (= (proj%vstd!view.View./V $ USIZE) USIZE)
)
(assert
 (= (proj%%vstd!view.View./V $ CHAR) $)
)
(assert
 (= (proj%vstd!view.View./V $ CHAR) CHAR)
)
(assert
 (forall ((A0&. Dcr) (A0& Type)) (!
   (=>
    (and
     (sized A0&.)
     (tr_bound%vstd!view.View. A0&. A0&)
    )
    (= (proj%%vstd!view.View./V (DST A0&.) (TYPE%tuple%1. A0&. A0&)) (DST (proj%%vstd!view.View./V
       A0&. A0&
   ))))
   :pattern ((proj%%vstd!view.View./V (DST A0&.) (TYPE%tuple%1. A0&. A0&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A0&. Dcr) (A0& Type)) (!
   (=>
    (and
     (sized A0&.)
     (tr_bound%vstd!view.View. A0&. A0&)
    )
    (= (proj%vstd!view.View./V (DST A0&.) (TYPE%tuple%1. A0&. A0&)) (TYPE%tuple%1. (proj%%vstd!view.View./V
       A0&. A0&
      ) (proj%vstd!view.View./V A0&. A0&)
   )))
   :pattern ((proj%vstd!view.View./V (DST A0&.) (TYPE%tuple%1. A0&. A0&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((A0&. Dcr) (A0& Type) (A1&. Dcr) (A1& Type)) (!
   (=>
    (and
     (sized A0&.)
     (sized A1&.)
     (tr_bound%vstd!view.View. A0&. A0&)
     (tr_bound%vstd!view.View. A1&. A1&)
    )
    (= (proj%%vstd!view.View./V (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&)) (DST (proj%%vstd!view.View./V
       A1&. A1&
   ))))
   :pattern ((proj%%vstd!view.View./V (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&)))
   :qid internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_assoc_type_impl_true_definition
)))
(assert
 (forall ((A0&. Dcr) (A0& Type) (A1&. Dcr) (A1& Type)) (!
   (=>
    (and
     (sized A0&.)
     (sized A1&.)
     (tr_bound%vstd!view.View. A0&. A0&)
     (tr_bound%vstd!view.View. A1&. A1&)
    )
    (= (proj%vstd!view.View./V (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&)) (TYPE%tuple%2.
      (proj%%vstd!view.View./V A0&. A0&) (proj%vstd!view.View./V A0&. A0&) (proj%%vstd!view.View./V
       A1&. A1&
      ) (proj%vstd!view.View./V A1&. A1&)
   )))
   :pattern ((proj%vstd!view.View./V (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&)))
   :qid internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.Fn. F&. F& A&. A&)
    )
    (= (proj%%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&) (proj%%core!ops.function.FnOnce./Output
      F&. F& A&. A&
   )))
   :pattern ((proj%%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.Fn. F&. F& A&. A&)
    )
    (= (proj%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&) (proj%core!ops.function.FnOnce./Output
      F&. F& A&. A&
   )))
   :pattern ((proj%core!ops.function.FnOnce./Output (REF F&.) F& A&. A&))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.FnMut. F&. F& A&. A&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&) (proj%%core!ops.function.FnOnce./Output
      F&. F& A&. A&
   )))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.FnMut. F&. F& A&. A&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&) (proj%core!ops.function.FnOnce./Output
      F&. F& A&. A&
   )))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (MUTREF F&. F&) A&. A&))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized Args&.)
     (sized A&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (= (proj%%core!ops.function.FnOnce./Output (BOX A&. A& F&.) F& Args&. Args&) (proj%%core!ops.function.FnOnce./Output
      F&. F& Args&. Args&
   )))
   :pattern ((proj%%core!ops.function.FnOnce./Output (BOX A&. A& F&.) F& Args&. Args&))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized Args&.)
     (sized A&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (= (proj%core!ops.function.FnOnce./Output (BOX A&. A& F&.) F& Args&. Args&) (proj%core!ops.function.FnOnce./Output
      F&. F& Args&. Args&
   )))
   :pattern ((proj%core!ops.function.FnOnce./Output (BOX A&. A& F&.) F& Args&. Args&))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%core!slice.index.SliceIndex./Output $ USIZE $slice (SLICE T&. T&)) T&.)
   )
   :pattern ((proj%%core!slice.index.SliceIndex./Output $ USIZE $slice (SLICE T&. T&)))
   :qid internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%core!slice.index.SliceIndex./Output $ USIZE $slice (SLICE T&. T&)) T&)
   )
   :pattern ((proj%core!slice.index.SliceIndex./Output $ USIZE $slice (SLICE T&. T&)))
   :qid internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $ USIZE)
      $slice (SLICE T&. T&)
     ) $slice
   ))
   :pattern ((proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $
      USIZE
     ) $slice (SLICE T&. T&)
   ))
   :qid internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $ USIZE)
      $slice (SLICE T&. T&)
     ) (SLICE T&. T&)
   ))
   :pattern ((proj%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $
      USIZE
     ) $slice (SLICE T&. T&)
   ))
   :qid internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $ USIZE)
   $slice STRSLICE
  ) $slice
))
(assert
 (= (proj%core!slice.index.SliceIndex./Output $ (TYPE%core!ops.range.Range. $ USIZE)
   $slice STRSLICE
  ) STRSLICE
))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
        $ USIZE
       ) $ (TYPE%core!ops.range.Bound. $ USIZE)
      ) $slice (SLICE T&. T&)
     ) $slice
   ))
   :pattern ((proj%%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
       $ USIZE
      ) $ (TYPE%core!ops.range.Bound. $ USIZE)
     ) $slice (SLICE T&. T&)
   ))
   :qid internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
        $ USIZE
       ) $ (TYPE%core!ops.range.Bound. $ USIZE)
      ) $slice (SLICE T&. T&)
     ) (SLICE T&. T&)
   ))
   :pattern ((proj%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
       $ USIZE
      ) $ (TYPE%core!ops.range.Bound. $ USIZE)
     ) $slice (SLICE T&. T&)
   ))
   :qid internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
     $ USIZE
    ) $ (TYPE%core!ops.range.Bound. $ USIZE)
   ) $slice STRSLICE
  ) $slice
))
(assert
 (= (proj%core!slice.index.SliceIndex./Output (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
     $ USIZE
    ) $ (TYPE%core!ops.range.Bound. $ USIZE)
   ) $slice STRSLICE
  ) STRSLICE
))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE) $slice
      (SLICE T&. T&)
     ) $slice
   ))
   :pattern ((proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE)
     $slice (SLICE T&. T&)
   ))
   :qid internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!slice.index.SliceIndex./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE) $slice
      (SLICE T&. T&)
     ) (SLICE T&. T&)
   ))
   :pattern ((proj%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE)
     $slice (SLICE T&. T&)
   ))
   :qid internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!slice.index.SliceIndex./Output_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE) $slice
   STRSLICE
  ) $slice
))
(assert
 (= (proj%core!slice.index.SliceIndex./Output $ (TYPE%core!range.Range. $ USIZE) $slice
   STRSLICE
  ) STRSLICE
))
(assert
 (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (UINT 8))
   (DST (REF $)) (TYPE%tuple%1. (REF $) (UINT 8))
  ) $
))
(assert
 (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (UINT 8))
   (DST (REF $)) (TYPE%tuple%1. (REF $) (UINT 8))
  ) (UINT 8)
))
(assert
 (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ USIZE)
   (DST (REF $)) (TYPE%tuple%1. (REF $) USIZE)
  ) $
))
(assert
 (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ USIZE)
   (DST (REF $)) (TYPE%tuple%1. (REF $) USIZE)
  ) USIZE
))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (and
     (sized Self%&.)
     (tr_bound%core!clone.Clone. Self%&. Self%&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. Self%&.
       Self%&
      ) (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
     ) Self%&.
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. Self%&.
      Self%&
     ) (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (and
     (sized Self%&.)
     (tr_bound%core!clone.Clone. Self%&. Self%&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. Self%&. Self%&)
      (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
     ) Self%&
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. Self%&.
      Self%&
     ) (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ BOOL)
   (DST (REF $)) (TYPE%tuple%1. (REF $) BOOL)
  ) $
))
(assert
 (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ BOOL)
   (DST (REF $)) (TYPE%tuple%1. (REF $) BOOL)
  ) BOOL
))
(assert
 (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ CHAR)
   (DST (REF $)) (TYPE%tuple%1. (REF $) CHAR)
  ) $
))
(assert
 (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ CHAR)
   (DST (REF $)) (TYPE%tuple%1. (REF $) CHAR)
  ) CHAR
))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (REF T&.)
      T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
    ) (REF T&.)
   )
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (
       REF T&.
      ) T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (REF T&.)
      T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
    ) T&
   )
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (REF
       T&.
      ) T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (ARRAY
        T&. T& N&. N&
       )
      ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
     ) $
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $
      (ARRAY T&. T& N&. N&)
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (ARRAY T&.
        T& N&. N&
       )
      ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
     ) (ARRAY T&. T& N&. N&)
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $
      (ARRAY T&. T& N&. N&)
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (TRACKED
        T&.
       ) T&
      ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
     ) (TRACKED T&.)
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (
       TRACKED T&.
      ) T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (TRACKED T&.)
       T&
      ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
     ) T&
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (TRACKED
       T&.
      ) T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (GHOST T&.)
       T&
      ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
     ) (GHOST T&.)
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (
       GHOST T&.
      ) T&
     ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (GHOST T&.)
       T&
      ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
     ) T&
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (GHOST
       T&.
      ) T&
     ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
        T&. T&
       )
      ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
     ) $
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $
      (TYPE%core!option.Option. T&. T&)
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
        T&. T&
       )
      ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
     ) (TYPE%core!option.Option. T&. T&)
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. $
      (TYPE%core!option.Option. T&. T&)
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (= (proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (BOX A&.
        A& T&.
       ) T&
      ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
     ) (BOX A&. A& T&.)
   ))
   :pattern ((proj%%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (
       BOX A&. A& T&.
      ) T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :qid internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (= (proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (BOX A&. A&
        T&.
       ) T&
      ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
     ) T&
   ))
   :pattern ((proj%core!ops.function.FnOnce./Output $ (FNDEF%core!clone.Clone.clone. (BOX
       A&. A& T&.
      ) T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :qid internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_assoc_type_impl_false_definition
)))

;; Function-Decl vstd::seq::Seq::len
(declare-fun vstd!seq.Seq.len.? (Dcr Type Poly) Int)

;; Function-Decl vstd::seq::Seq::index
(declare-fun vstd!seq.Seq.index.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::impl&%2::spec_index
(declare-fun vstd!seq.impl&%2.spec_index.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::Seq::subrange
(declare-fun vstd!seq.Seq.subrange.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl vstd::seq::Seq::empty
(declare-fun vstd!seq.Seq.empty.? (Dcr Type) Poly)

;; Function-Decl vstd::seq::Seq::new
(declare-fun vstd!seq.Seq.new.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::Seq::update
(declare-fun vstd!seq.Seq.update.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl vstd::seq::Seq::add
(declare-fun vstd!seq.Seq.add.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::impl&%2::spec_add
(declare-fun vstd!seq.impl&%2.spec_add.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::multiset::impl&%0::count
(declare-fun vstd!multiset.impl&%0.count.? (Dcr Type Poly Poly) Int)

;; Function-Decl vstd::slice::spec_slice_len
(declare-fun vstd!slice.spec_slice_len.? (Dcr Type Poly) Int)

;; Function-Decl vstd::view::View::view
(declare-fun vstd!view.View.view.? (Dcr Type Poly) Poly)
(declare-fun vstd!view.View.view%default%.? (Dcr Type Poly) Poly)

;; Function-Decl vstd::slice::len%returns_clause_autospec
(declare-fun vstd!slice.len%returns_clause_autospec.? (Dcr Type Poly) Int)

;; Function-Decl vstd::slice::SliceAdditionalSpecFns::spec_index
(declare-fun vstd!slice.SliceAdditionalSpecFns.spec_index.? (Dcr Type Dcr Type Poly
  Poly
 ) Poly
)
(declare-fun vstd!slice.SliceAdditionalSpecFns.spec_index%default%.? (Dcr Type Dcr
  Type Poly Poly
 ) Poly
)

;; Function-Decl vstd::array::array_view
(declare-fun vstd!array.array_view.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl vstd::array::ArrayAdditionalSpecFns::spec_index
(declare-fun vstd!array.ArrayAdditionalSpecFns.spec_index.? (Dcr Type Dcr Type Poly
  Poly
 ) Poly
)
(declare-fun vstd!array.ArrayAdditionalSpecFns.spec_index%default%.? (Dcr Type Dcr
  Type Poly Poly
 ) Poly
)

;; Function-Decl vstd::raw_ptr::view_reverse_for_eq
(declare-fun vstd!raw_ptr.view_reverse_for_eq.? (Dcr Type Poly) Poly)

;; Function-Decl vstd::raw_ptr::view_reverse_for_eq_sized
(declare-fun vstd!raw_ptr.view_reverse_for_eq_sized.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::pervasive::strictly_cloned
(declare-fun vstd!pervasive.strictly_cloned.? (Dcr Type Poly Poly) Bool)

;; Function-Decl vstd::pervasive::cloned
(declare-fun vstd!pervasive.cloned.? (Dcr Type Poly Poly) Bool)

;; Function-Decl vstd::std_specs::option::OptionAdditionalFns::arrow_Some_0
(declare-fun vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.? (Dcr Type Dcr
  Type Poly
 ) Poly
)
(declare-fun vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0%default%.? (Dcr
  Type Dcr Type Poly
 ) Poly
)

;; Function-Decl vstd::std_specs::option::OptionAdditionalFns::arrow_0
(declare-fun vstd!std_specs.option.OptionAdditionalFns.arrow_0.? (Dcr Type Dcr Type
  Poly
 ) Poly
)
(declare-fun vstd!std_specs.option.OptionAdditionalFns.arrow_0%default%.? (Dcr Type
  Dcr Type Poly
 ) Poly
)

;; Function-Decl vstd::std_specs::option::is_some
(declare-fun vstd!std_specs.option.is_some.? (Dcr Type Poly) Bool)

;; Function-Decl vstd::std_specs::option::is_none
(declare-fun vstd!std_specs.option.is_none.? (Dcr Type Poly) Bool)

;; Function-Decl vstd::std_specs::option::spec_unwrap
(declare-fun vstd!std_specs.option.spec_unwrap.? (Dcr Type Poly) Poly)

;; Function-Decl vstd::seq_lib::impl&%0::to_multiset
(declare-fun vstd!seq_lib.impl&%0.to_multiset.? (Dcr Type Poly) Poly)

;; Function-Decl det_harness::partial_eq_observed
(declare-fun det_harness!partial_eq_observed.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_pattern_view
(declare-fun det_harness!slice_pattern_view.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::zero_arg_fnmut_outputs
(declare-fun det_harness!zero_arg_fnmut_outputs.? (Dcr Type Dcr Type Poly Poly) Poly)

;; Function-Decl det_harness::ord_cmp_observed
(declare-fun det_harness!ord_cmp_observed.? (Dcr Type Poly Poly) core!cmp.Ordering.)

;; Function-Decl det_harness::ordering_rank
(declare-fun det_harness!ordering_rank.? (Poly) Int)

;; Function-Decl det_harness::ord_leq_observed
(declare-fun det_harness!ord_leq_observed.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::partial_ord_leq_observed
(declare-fun det_harness!partial_ord_leq_observed.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::fnmut_adjacent_bool_outputs
(declare-fun det_harness!fnmut_adjacent_bool_outputs.? (Dcr Type Dcr Type Poly Poly)
 vstd!seq.Seq<bool.>.
)

;; Function-Decl det_harness::fnmut_adjacent_key_outputs
(declare-fun det_harness!fnmut_adjacent_key_outputs.? (Dcr Type Dcr Type Dcr Type Poly
  Poly
 ) Poly
)

;; Function-Decl det_harness::fnmut_ordering_observed
(declare-fun det_harness!fnmut_ordering_observed.? (Dcr Type Dcr Type Poly Poly) core!cmp.Ordering.)

;; Function-Decl det_harness::fnmut_key_observed
(declare-fun det_harness!fnmut_key_observed.? (Dcr Type Dcr Type Dcr Type Poly Poly)
 Poly
)

;; Function-Decl det_harness::fnmut_predicate_observed
(declare-fun det_harness!fnmut_predicate_observed.? (Dcr Type Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::comparator_leq_observed
(declare-fun det_harness!comparator_leq_observed.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::comparator_observation
(declare-fun det_harness!comparator_observation.? (Dcr Type Dcr Type Poly Poly) det_harness!ComparatorObservation.)

;; Function-Decl det_harness::slice_iterator_view
(declare-fun det_harness!slice_iterator_view.? (Dcr Type Dcr Type Poly) det_harness!SliceIteratorView.)

;; Function-Decl det_harness::slice_iterator_well_formed
(declare-fun det_harness!slice_iterator_well_formed.? (Dcr Type Poly) Bool)

;; Function-Decl det_harness::fnmut_adjacent_predicate_observed
(declare-fun det_harness!fnmut_adjacent_predicate_observed.? (Dcr Type Dcr Type Poly
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_raw_domain
(declare-fun det_harness!slice_raw_domain.? (Dcr Type Poly Poly Poly) det_harness!SliceRawDomain.)

;; Function-Decl det_harness::slice_raw_mut_domain
(declare-fun det_harness!slice_raw_mut_domain.? (Dcr Type Poly Poly Poly) det_harness!SliceRawDomain.)

;; Function-Decl det_harness::slice_start_ptr
(declare-fun det_harness!slice_start_ptr.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_start_mut_ptr
(declare-fun det_harness!slice_start_mut_ptr.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_ptr_range_result
(declare-fun det_harness!slice_ptr_range_result.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_mut_ptr_range_result
(declare-fun det_harness!slice_mut_ptr_range_result.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_align_to_domain
(declare-fun det_harness!slice_align_to_domain.? (Dcr Type Dcr Type Poly) Bool)

;; Function-Decl det_harness::slice_aligned_middle
(declare-fun det_harness!slice_aligned_middle.? (Dcr Type Dcr Type Poly Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_element_offset_result
(declare-fun det_harness!slice_element_offset_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_element_in_domain
(declare-fun det_harness!slice_element_in_domain.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_subslice_range_result
(declare-fun det_harness!slice_subslice_range_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_subslice_in_domain
(declare-fun det_harness!slice_subslice_in_domain.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_index_in_range
(declare-fun det_harness!slice_index_in_range.? (Dcr Type Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_index_result
(declare-fun det_harness!slice_index_result.? (Dcr Type Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_index_mut_frame
(declare-fun det_harness!slice_index_mut_frame.? (Dcr Type Dcr Type Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_disjoint_indices_valid
(declare-fun det_harness!slice_disjoint_indices_valid.? (Dcr Type Dcr Type Dcr Type
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::maybe_uninit_storage_relation
(declare-fun det_harness!maybe_uninit_storage_relation.? (Dcr Type Poly) det_harness!MaybeUninitSliceRelation.)

;; Function-Decl det_harness::maybe_uninit_seq_relation
(declare-fun det_harness!maybe_uninit_seq_relation.? (Dcr Type Poly) det_harness!MaybeUninitSliceRelation.)

;; Function-Decl det_harness::maybe_uninit_from_initialized
(declare-fun det_harness!maybe_uninit_from_initialized.? (Dcr Type Poly) Poly)

;; Function-Decl det_harness::ascii_escape_seq
(declare-fun det_harness!ascii_escape_seq.? (Poly) vstd!seq.Seq<u8.>.)

;; Function-Decl det_harness::slice_seq
(declare-fun det_harness!slice_seq.? (Dcr Type Poly) Poly)

;; Function-Decl det_harness::slice_len
(declare-fun det_harness!slice_len.? (Dcr Type Poly) Int)

;; Function-Decl det_harness::slice_subrange
(declare-fun det_harness!slice_subrange.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl det_harness::seq_subrange
(declare-fun det_harness!seq_subrange.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl det_harness::seq_update
(declare-fun det_harness!seq_update.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl det_harness::slice_contains_value
(declare-fun det_harness!slice_contains_value.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_is_prefix
(declare-fun det_harness!slice_is_prefix.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_is_suffix
(declare-fun det_harness!slice_is_suffix.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_strip_prefix_result
(declare-fun det_harness!slice_strip_prefix_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_strip_suffix_result
(declare-fun det_harness!slice_strip_suffix_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_strip_circumfix_result
(declare-fun det_harness!slice_strip_circumfix_result.? (Dcr Type Poly Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_filled
(declare-fun det_harness!slice_filled.? (Dcr Type Poly Poly) Poly)

;; Function-Decl det_harness::slice_cloned_from
(declare-fun det_harness!slice_cloned_from.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_filled_with_clone
(declare-fun det_harness!slice_filled_with_clone.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_reversed
(declare-fun det_harness!slice_reversed.? (Dcr Type Poly) Poly)

;; Function-Decl det_harness::slice_rotated_left
(declare-fun det_harness!slice_rotated_left.? (Dcr Type Poly Poly) Poly)

;; Function-Decl det_harness::slice_rotated_right
(declare-fun det_harness!slice_rotated_right.? (Dcr Type Poly Poly) Poly)

;; Function-Decl det_harness::slice_swapped
(declare-fun det_harness!slice_swapped.? (Dcr Type Poly Poly Poly) Poly)

;; Function-Decl det_harness::slice_multiplicity
(declare-fun det_harness!slice_multiplicity.? (Dcr Type Poly Poly) Int)

;; Function-Decl det_harness::slice_permutation
(declare-fun det_harness!slice_permutation.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_sorted_by_ord
(declare-fun det_harness!slice_sorted_by_ord.? (Dcr Type Poly) Bool)

;; Function-Decl det_harness::slice_sorted_by_partial_ord
(declare-fun det_harness!slice_sorted_by_partial_ord.? (Dcr Type Poly) Bool)

;; Function-Decl det_harness::slice_adjacent_pair_count
(declare-fun det_harness!slice_adjacent_pair_count.? (Dcr Type Poly) Int)

;; Function-Decl det_harness::fnmut_adjacent_bool_trace_valid
(declare-fun det_harness!fnmut_adjacent_bool_trace_valid.? (Dcr Type Dcr Type Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_sorted_by_bool_compare
(declare-fun det_harness!slice_sorted_by_bool_compare.? (Dcr Type Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_sorted_by_bool_compare_result
(declare-fun det_harness!slice_sorted_by_bool_compare_result.? (Dcr Type Dcr Type Poly
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::fnmut_adjacent_key_trace_valid
(declare-fun det_harness!fnmut_adjacent_key_trace_valid.? (Dcr Type Dcr Type Dcr Type
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_sorted_by_partial_key
(declare-fun det_harness!slice_sorted_by_partial_key.? (Dcr Type Dcr Type Dcr Type
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_sorted_by_partial_key_result
(declare-fun det_harness!slice_sorted_by_partial_key_result.? (Dcr Type Dcr Type Dcr
  Type Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_ord_equal_at
(declare-fun det_harness!slice_ord_equal_at.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_ord_insertion_point
(declare-fun det_harness!slice_ord_insertion_point.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_binary_search_result
(declare-fun det_harness!slice_binary_search_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_binary_search_by_ordered
(declare-fun det_harness!slice_binary_search_by_ordered.? (Dcr Type Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_binary_search_by_equal_at
(declare-fun det_harness!slice_binary_search_by_equal_at.? (Dcr Type Dcr Type Poly
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_insertion_point
(declare-fun det_harness!slice_binary_search_by_insertion_point.? (Dcr Type Dcr Type
  Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_result
(declare-fun det_harness!slice_binary_search_by_result.? (Dcr Type Dcr Type Poly Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_key_ordered
(declare-fun det_harness!slice_binary_search_by_key_ordered.? (Dcr Type Dcr Type Dcr
  Type Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_key_equal_at
(declare-fun det_harness!slice_binary_search_by_key_equal_at.? (Dcr Type Dcr Type Dcr
  Type Poly Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_key_insertion_point
(declare-fun det_harness!slice_binary_search_by_key_insertion_point.? (Dcr Type Dcr
  Type Dcr Type Poly Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_binary_search_by_key_result
(declare-fun det_harness!slice_binary_search_by_key_result.? (Dcr Type Dcr Type Dcr
  Type Poly Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_partitioned_by_predicate
(declare-fun det_harness!slice_partitioned_by_predicate.? (Dcr Type Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_partition_point_result
(declare-fun det_harness!slice_partition_point_result.? (Dcr Type Dcr Type Poly Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_sorted_by_cmp
(declare-fun det_harness!slice_sorted_by_cmp.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_sorted_by_key
(declare-fun det_harness!slice_sorted_by_key.? (Dcr Type Dcr Type Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_select_partition_ord
(declare-fun det_harness!slice_select_partition_ord.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_select_partition_cmp
(declare-fun det_harness!slice_select_partition_cmp.? (Dcr Type Poly Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_select_partition_key
(declare-fun det_harness!slice_select_partition_key.? (Dcr Type Dcr Type Dcr Type Poly
  Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_partitioned_at
(declare-fun det_harness!slice_partitioned_at.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_chunk_partition
(declare-fun det_harness!slice_chunk_partition.? (Dcr Type Poly) Bool)

;; Function-Decl det_harness::slice_predicate_split_view
(declare-fun det_harness!slice_predicate_split_view.? (Dcr Type Dcr Type Dcr Type Poly
  Poly Poly Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_adjacent_chunk_view
(declare-fun det_harness!slice_adjacent_chunk_view.? (Dcr Type Dcr Type Dcr Type Poly
  Poly Poly
 ) Bool
)

;; Function-Decl det_harness::slice_split_off_partition
(declare-fun det_harness!slice_split_off_partition.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_split_off_first_result
(declare-fun det_harness!slice_split_off_first_result.? (Dcr Type Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_split_off_last_result
(declare-fun det_harness!slice_split_off_last_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::utf8_chunk_partition
(declare-fun det_harness!utf8_chunk_partition.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::array_ref_view
(declare-fun det_harness!array_ref_view.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::array_mut_ref_view
(declare-fun det_harness!array_mut_ref_view.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::array_value_view
(declare-fun det_harness!array_value_view.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::split_point_in_range
(declare-fun det_harness!split_point_in_range.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::slice_fixed_prefix
(declare-fun det_harness!slice_fixed_prefix.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::slice_fixed_suffix
(declare-fun det_harness!slice_fixed_suffix.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::flatten_array_chunks
(declare-fun det_harness!flatten_array_chunks.? (Dcr Type Dcr Type Poly) Poly)

;; Function-Decl det_harness::slice_array_chunks_partition
(declare-fun det_harness!slice_array_chunks_partition.? (Dcr Type Dcr Type Poly Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_array_rchunks_partition
(declare-fun det_harness!slice_array_rchunks_partition.? (Dcr Type Dcr Type Poly Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_raw_domain_valid
(declare-fun det_harness!slice_raw_domain_valid.? (Poly) Bool)

;; Function-Decl det_harness::slice_from_raw_parts_result
(declare-fun det_harness!slice_from_raw_parts_result.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::slice_from_raw_parts_mut_result
(declare-fun det_harness!slice_from_raw_parts_mut_result.? (Dcr Type Poly Poly Poly)
 Bool
)

;; Function-Decl det_harness::slice_align_to_result
(declare-fun det_harness!slice_align_to_result.? (Dcr Type Dcr Type Poly Poly Poly
  Poly
 ) Bool
)

;; Function-Decl det_harness::slice_align_to_mut_result
(declare-fun det_harness!slice_align_to_mut_result.? (Dcr Type Dcr Type Poly Poly Poly
  Poly Poly Poly Poly Poly
 ) Bool
)

;; Function-Decl det_harness::maybe_uninit_relation_well_formed
(declare-fun det_harness!maybe_uninit_relation_well_formed.? (Dcr Type Poly Poly)
 Bool
)

;; Function-Decl det_harness::maybe_uninit_all_initialized
(declare-fun det_harness!maybe_uninit_all_initialized.? (Dcr Type Poly) Bool)

;; Function-Decl det_harness::maybe_uninit_written_from
(declare-fun det_harness!maybe_uninit_written_from.? (Dcr Type Poly Poly Poly) Bool)

;; Function-Decl det_harness::maybe_uninit_drop_all
(declare-fun det_harness!maybe_uninit_drop_all.? (Dcr Type Poly Poly) Bool)

;; Function-Decl det_harness::ascii_is_uppercase
(declare-fun det_harness!ascii_is_uppercase.? (Poly) Bool)

;; Function-Decl det_harness::ascii_is_lowercase
(declare-fun det_harness!ascii_is_lowercase.? (Poly) Bool)

;; Function-Decl det_harness::ascii_lower_byte
(declare-fun det_harness!ascii_lower_byte.? (Poly) Int)

;; Function-Decl det_harness::ascii_upper_byte
(declare-fun det_harness!ascii_upper_byte.? (Poly) Int)

;; Function-Decl det_harness::ascii_is_byte
(declare-fun det_harness!ascii_is_byte.? (Poly) Bool)

;; Function-Decl det_harness::ascii_is_whitespace
(declare-fun det_harness!ascii_is_whitespace.? (Poly) Bool)

;; Function-Decl det_harness::ascii_all
(declare-fun det_harness!ascii_all.? (Poly) Bool)

;; Function-Decl det_harness::ascii_lower_seq
(declare-fun det_harness!ascii_lower_seq.? (Poly) vstd!seq.Seq<u8.>.)

;; Function-Decl det_harness::ascii_upper_seq
(declare-fun det_harness!ascii_upper_seq.? (Poly) vstd!seq.Seq<u8.>.)

;; Function-Decl det_harness::ascii_eq_ignore_case
(declare-fun det_harness!ascii_eq_ignore_case.? (Poly Poly) Bool)

;; Function-Decl det_harness::ascii_trim_start_boundary
(declare-fun det_harness!ascii_trim_start_boundary.? (Poly Poly) Bool)

;; Function-Decl det_harness::ascii_trim_end_boundary
(declare-fun det_harness!ascii_trim_end_boundary.? (Poly Poly) Bool)

;; Function-Decl det_harness::ascii_trim_start_index
(declare-fun det_harness!ascii_trim_start_index.? (Poly) Int)

;; Function-Decl det_harness::ascii_trim_end_index
(declare-fun det_harness!ascii_trim_end_index.? (Poly) Int)

;; Function-Decl det_harness::ascii_trim_start_result
(declare-fun det_harness!ascii_trim_start_result.? (Poly Poly) Bool)

;; Function-Decl det_harness::ascii_trim_end_result
(declare-fun det_harness!ascii_trim_end_result.? (Poly Poly) Bool)

;; Function-Decl det_harness::ascii_trim_result
(declare-fun det_harness!ascii_trim_result.? (Poly Poly) Bool)

;; Function-Decl det_harness::det___rust_std_candidate_equal
(declare-fun det_harness!det___rust_std_candidate_equal.? (Dcr Type Poly Poly) Bool)

;; Function-Axioms vstd::seq::Seq::len
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
   (=>
    (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
    (<= 0 (vstd!seq.Seq.len.? A&. A& self!))
   )
   :pattern ((vstd!seq.Seq.len.? A&. A& self!))
   :qid internal_vstd!seq.Seq.len.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.len.?_pre_post_definition
)))

;; Function-Specs vstd::seq::Seq::index
(declare-fun req%vstd!seq.Seq.index. (Dcr Type Poly Poly) Bool)
(declare-const %%global_location_label%%0 Bool)
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly)) (!
   (= (req%vstd!seq.Seq.index. A&. A& self! i!) (=>
     %%global_location_label%%0
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I i!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& self!)))
        (and
         (<= tmp%%$ tmp%%$1)
         (< tmp%%$1 tmp%%$2)
   ))))))
   :pattern ((req%vstd!seq.Seq.index. A&. A& self! i!))
   :qid internal_req__vstd!seq.Seq.index._definition
   :skolemid skolem_internal_req__vstd!seq.Seq.index._definition
)))

;; Function-Axioms vstd::seq::Seq::index
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type i! INT)
    )
    (has_type (vstd!seq.Seq.index.? A&. A& self! i!) A&)
   )
   :pattern ((vstd!seq.Seq.index.? A&. A& self! i!))
   :qid internal_vstd!seq.Seq.index.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.index.?_pre_post_definition
)))

;; Function-Specs vstd::seq::impl&%2::spec_index
(declare-fun req%vstd!seq.impl&%2.spec_index. (Dcr Type Poly Poly) Bool)
(declare-const %%global_location_label%%1 Bool)
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly)) (!
   (= (req%vstd!seq.impl&%2.spec_index. A&. A& self! i!) (=>
     %%global_location_label%%1
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I i!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& self!)))
        (and
         (<= tmp%%$ tmp%%$1)
         (< tmp%%$1 tmp%%$2)
   ))))))
   :pattern ((req%vstd!seq.impl&%2.spec_index. A&. A& self! i!))
   :qid internal_req__vstd!seq.impl&__2.spec_index._definition
   :skolemid skolem_internal_req__vstd!seq.impl&__2.spec_index._definition
)))

;; Function-Axioms vstd::seq::impl&%2::spec_index
(assert
 (fuel_bool_default fuel%vstd!seq.impl&%2.spec_index.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!seq.impl&%2.spec_index.)
  (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly)) (!
    (= (vstd!seq.impl&%2.spec_index.? A&. A& self! i!) (vstd!seq.Seq.index.? A&. A& self!
      i!
    ))
    :pattern ((vstd!seq.impl&%2.spec_index.? A&. A& self! i!))
    :qid internal_vstd!seq.impl&__2.spec_index.?_definition
    :skolemid skolem_internal_vstd!seq.impl&__2.spec_index.?_definition
))))
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type i! INT)
    )
    (has_type (vstd!seq.impl&%2.spec_index.? A&. A& self! i!) A&)
   )
   :pattern ((vstd!seq.impl&%2.spec_index.? A&. A& self! i!))
   :qid internal_vstd!seq.impl&__2.spec_index.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.impl&__2.spec_index.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_index_decreases
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_index_decreases.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized A&.)
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& s!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (height_lt (height (vstd!seq.Seq.index.? A&. A& s! i!)) (height s!))
    ))
    :pattern ((height (vstd!seq.Seq.index.? A&. A& s! i!)))
    :qid user_vstd__seq__lemma_seq_index_decreases_0
    :skolemid skolem_user_vstd__seq__lemma_seq_index_decreases_0
))))

;; Function-Specs vstd::seq::Seq::subrange
(declare-fun req%vstd!seq.Seq.subrange. (Dcr Type Poly Poly Poly) Bool)
(declare-const %%global_location_label%%2 Bool)
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (start_inclusive! Poly) (end_exclusive! Poly))
  (!
   (= (req%vstd!seq.Seq.subrange. A&. A& self! start_inclusive! end_exclusive!) (=>
     %%global_location_label%%2
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I start_inclusive!)))
       (let
        ((tmp%%$2 (%I end_exclusive!)))
        (let
         ((tmp%%$3 (vstd!seq.Seq.len.? A&. A& self!)))
         (and
          (and
           (<= tmp%%$ tmp%%$1)
           (<= tmp%%$1 tmp%%$2)
          )
          (<= tmp%%$2 tmp%%$3)
   )))))))
   :pattern ((req%vstd!seq.Seq.subrange. A&. A& self! start_inclusive! end_exclusive!))
   :qid internal_req__vstd!seq.Seq.subrange._definition
   :skolemid skolem_internal_req__vstd!seq.Seq.subrange._definition
)))

;; Function-Axioms vstd::seq::Seq::subrange
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (start_inclusive! Poly) (end_exclusive! Poly))
  (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type start_inclusive! INT)
     (has_type end_exclusive! INT)
    )
    (has_type (vstd!seq.Seq.subrange.? A&. A& self! start_inclusive! end_exclusive!) (
      TYPE%vstd!seq.Seq. A&. A&
   )))
   :pattern ((vstd!seq.Seq.subrange.? A&. A& self! start_inclusive! end_exclusive!))
   :qid internal_vstd!seq.Seq.subrange.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.subrange.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_subrange_decreases
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_subrange_decreases.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (i! Poly) (j! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
      (has_type j! INT)
     )
     (=>
      (and
       (and
        (sized A&.)
        (let
         ((tmp%%$ 0))
         (let
          ((tmp%%$1 (%I i!)))
          (let
           ((tmp%%$2 (%I j!)))
           (let
            ((tmp%%$3 (vstd!seq.Seq.len.? A&. A& s!)))
            (and
             (and
              (<= tmp%%$ tmp%%$1)
              (<= tmp%%$1 tmp%%$2)
             )
             (<= tmp%%$2 tmp%%$3)
       ))))))
       (< (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! i! j!)) (vstd!seq.Seq.len.?
         A&. A& s!
      )))
      (height_lt (height (vstd!seq.Seq.subrange.? A&. A& s! i! j!)) (height s!))
    ))
    :pattern ((height (vstd!seq.Seq.subrange.? A&. A& s! i! j!)))
    :qid user_vstd__seq__lemma_seq_subrange_decreases_1
    :skolemid skolem_user_vstd__seq__lemma_seq_subrange_decreases_1
))))

;; Function-Axioms vstd::seq::Seq::empty
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (has_type (vstd!seq.Seq.empty.? A&. A&) (TYPE%vstd!seq.Seq. A&. A&))
   :pattern ((vstd!seq.Seq.empty.? A&. A&))
   :qid internal_vstd!seq.Seq.empty.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.empty.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_empty
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_empty.)
  (forall ((A&. Dcr) (A& Type)) (!
    (=>
     (sized A&.)
     (= (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.empty.? A&. A&)) 0)
    )
    :pattern ((vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.empty.? A&. A&)))
    :qid user_vstd__seq__lemma_seq_empty_2
    :skolemid skolem_user_vstd__seq__lemma_seq_empty_2
))))

;; Function-Axioms vstd::seq::Seq::new
(assert
 (forall ((A&. Dcr) (A& Type) (len! Poly) (f! Poly)) (!
   (=>
    (and
     (has_type len! NAT)
     (has_type f! (TYPE%fun%1. $ INT A&. A&))
    )
    (has_type (vstd!seq.Seq.new.? A&. A& len! f!) (TYPE%vstd!seq.Seq. A&. A&))
   )
   :pattern ((vstd!seq.Seq.new.? A&. A& len! f!))
   :qid internal_vstd!seq.Seq.new.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.new.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_new_len
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_new_len.)
  (forall ((A&. Dcr) (A& Type) (len! Poly) (f! Poly)) (!
    (=>
     (and
      (has_type len! NAT)
      (has_type f! (TYPE%fun%1. $ INT A&. A&))
     )
     (=>
      (sized A&.)
      (= (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.new.? A&. A& len! f!)) (%I len!))
    ))
    :pattern ((vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.new.? A&. A& len! f!)))
    :qid user_vstd__seq__lemma_seq_new_len_3
    :skolemid skolem_user_vstd__seq__lemma_seq_new_len_3
))))

;; Broadcast vstd::seq::lemma_seq_new_index
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_new_index.)
  (forall ((A&. Dcr) (A& Type) (len! Poly) (f! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type len! NAT)
      (has_type f! (TYPE%fun%1. $ INT A&. A&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized A&.)
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (%I len!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.new.? A&. A& len! f!) i!) (%%apply%%0
        (%Poly%fun%1. f!) i!
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.new.? A&. A& len! f!) i!))
    :qid user_vstd__seq__lemma_seq_new_index_4
    :skolemid skolem_user_vstd__seq__lemma_seq_new_index_4
))))

;; Function-Specs vstd::seq::Seq::update
(declare-fun req%vstd!seq.Seq.update. (Dcr Type Poly Poly Poly) Bool)
(declare-const %%global_location_label%%3 Bool)
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly) (a! Poly)) (!
   (= (req%vstd!seq.Seq.update. A&. A& self! i! a!) (=>
     %%global_location_label%%3
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I i!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& self!)))
        (and
         (<= tmp%%$ tmp%%$1)
         (< tmp%%$1 tmp%%$2)
   ))))))
   :pattern ((req%vstd!seq.Seq.update. A&. A& self! i! a!))
   :qid internal_req__vstd!seq.Seq.update._definition
   :skolemid skolem_internal_req__vstd!seq.Seq.update._definition
)))

;; Function-Axioms vstd::seq::Seq::update
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (i! Poly) (a! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type i! INT)
     (has_type a! A&)
    )
    (has_type (vstd!seq.Seq.update.? A&. A& self! i! a!) (TYPE%vstd!seq.Seq. A&. A&))
   )
   :pattern ((vstd!seq.Seq.update.? A&. A& self! i! a!))
   :qid internal_vstd!seq.Seq.update.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.update.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_update_len
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_update_len.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (i! Poly) (a! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
      (has_type a! A&)
     )
     (=>
      (sized A&.)
      (= (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i! a!)) (vstd!seq.Seq.len.?
        A&. A& s!
    ))))
    :pattern ((vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i! a!)))
    :qid user_vstd__seq__lemma_seq_update_len_5
    :skolemid skolem_user_vstd__seq__lemma_seq_update_len_5
))))

;; Broadcast vstd::seq::lemma_seq_update_same
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_update_same.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (i! Poly) (a! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
      (has_type a! A&)
     )
     (=>
      (and
       (sized A&.)
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& s!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i! a!) i!) a!)
    ))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i! a!) i!))
    :qid user_vstd__seq__lemma_seq_update_same_6
    :skolemid skolem_user_vstd__seq__lemma_seq_update_same_6
))))

;; Broadcast vstd::seq::lemma_seq_update_different
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_update_different.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (i1! Poly) (i2! Poly) (a! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i1! INT)
      (has_type i2! INT)
      (has_type a! A&)
     )
     (=>
      (and
       (sized A&.)
       (not (= i1! i2!))
      )
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i2! a!) i1!) (vstd!seq.Seq.index.?
        A&. A& s! i1!
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.update.? A&. A& s! i2! a!) i1!))
    :qid user_vstd__seq__lemma_seq_update_different_7
    :skolemid skolem_user_vstd__seq__lemma_seq_update_different_7
))))

;; Broadcast vstd::seq::lemma_seq_ext_equal
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_ext_equal.)
  (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly)) (!
    (=>
     (and
      (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type s2! (TYPE%vstd!seq.Seq. A&. A&))
     )
     (=>
      (sized A&.)
      (= (ext_eq false (TYPE%vstd!seq.Seq. A&. A&) s1! s2!) (and
        (= (vstd!seq.Seq.len.? A&. A& s1!) (vstd!seq.Seq.len.? A&. A& s2!))
        (forall ((i$ Poly)) (!
          (=>
           (has_type i$ INT)
           (=>
            (let
             ((tmp%%$ 0))
             (let
              ((tmp%%$1 (%I i$)))
              (let
               ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& s1!)))
               (and
                (<= tmp%%$ tmp%%$1)
                (< tmp%%$1 tmp%%$2)
            ))))
            (= (vstd!seq.Seq.index.? A&. A& s1! i$) (vstd!seq.Seq.index.? A&. A& s2! i$))
          ))
          :pattern ((vstd!seq.Seq.index.? A&. A& s1! i$))
          :pattern ((vstd!seq.Seq.index.? A&. A& s2! i$))
          :qid user_vstd__seq__lemma_seq_ext_equal_8
          :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_8
    ))))))
    :pattern ((ext_eq false (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
    :qid user_vstd__seq__lemma_seq_ext_equal_9
    :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_9
))))

;; Broadcast vstd::seq::lemma_seq_ext_equal_deep
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_ext_equal_deep.)
  (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly)) (!
    (=>
     (and
      (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type s2! (TYPE%vstd!seq.Seq. A&. A&))
     )
     (=>
      (sized A&.)
      (= (ext_eq true (TYPE%vstd!seq.Seq. A&. A&) s1! s2!) (and
        (= (vstd!seq.Seq.len.? A&. A& s1!) (vstd!seq.Seq.len.? A&. A& s2!))
        (forall ((i$ Poly)) (!
          (=>
           (has_type i$ INT)
           (=>
            (let
             ((tmp%%$ 0))
             (let
              ((tmp%%$1 (%I i$)))
              (let
               ((tmp%%$2 (vstd!seq.Seq.len.? A&. A& s1!)))
               (and
                (<= tmp%%$ tmp%%$1)
                (< tmp%%$1 tmp%%$2)
            ))))
            (ext_eq true A& (vstd!seq.Seq.index.? A&. A& s1! i$) (vstd!seq.Seq.index.? A&. A& s2!
              i$
          ))))
          :pattern ((vstd!seq.Seq.index.? A&. A& s1! i$))
          :pattern ((vstd!seq.Seq.index.? A&. A& s2! i$))
          :qid user_vstd__seq__lemma_seq_ext_equal_deep_10
          :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_10
    ))))))
    :pattern ((ext_eq true (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
    :qid user_vstd__seq__lemma_seq_ext_equal_deep_11
    :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_11
))))

;; Broadcast vstd::seq::lemma_seq_subrange_len
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_subrange_len.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (j! Poly) (k! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type j! INT)
      (has_type k! INT)
     )
     (=>
      (and
       (sized A&.)
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I j!)))
         (let
          ((tmp%%$2 (%I k!)))
          (let
           ((tmp%%$3 (vstd!seq.Seq.len.? A&. A& s!)))
           (and
            (and
             (<= tmp%%$ tmp%%$1)
             (<= tmp%%$1 tmp%%$2)
            )
            (<= tmp%%$2 tmp%%$3)
      ))))))
      (= (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k!)) (Sub (%I k!)
        (%I j!)
    ))))
    :pattern ((vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k!)))
    :qid user_vstd__seq__lemma_seq_subrange_len_12
    :skolemid skolem_user_vstd__seq__lemma_seq_subrange_len_12
))))

;; Broadcast vstd::seq::lemma_seq_subrange_index
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_subrange_index.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (j! Poly) (k! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type j! INT)
      (has_type k! INT)
      (has_type i! INT)
     )
     (=>
      (and
       (and
        (sized A&.)
        (let
         ((tmp%%$ 0))
         (let
          ((tmp%%$1 (%I j!)))
          (let
           ((tmp%%$2 (%I k!)))
           (let
            ((tmp%%$3 (vstd!seq.Seq.len.? A&. A& s!)))
            (and
             (and
              (<= tmp%%$ tmp%%$1)
              (<= tmp%%$1 tmp%%$2)
             )
             (<= tmp%%$2 tmp%%$3)
       ))))))
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$5 (%I i!)))
         (let
          ((tmp%%$6 (Sub (%I k!) (%I j!))))
          (and
           (<= tmp%%$ tmp%%$5)
           (< tmp%%$5 tmp%%$6)
      )))))
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k!) i!) (vstd!seq.Seq.index.?
        A&. A& s! (I (Add (%I i!) (%I j!)))
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k!) i!))
    :qid user_vstd__seq__lemma_seq_subrange_index_13
    :skolemid skolem_user_vstd__seq__lemma_seq_subrange_index_13
))))

;; Broadcast vstd::seq::lemma_seq_two_subranges_index
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_two_subranges_index.)
  (forall ((A&. Dcr) (A& Type) (s! Poly) (j! Poly) (k1! Poly) (k2! Poly) (i! Poly))
   (!
    (=>
     (and
      (has_type s! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type j! INT)
      (has_type k1! INT)
      (has_type k2! INT)
      (has_type i! INT)
     )
     (=>
      (and
       (and
        (and
         (and
          (sized A&.)
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I j!)))
            (let
             ((tmp%%$2 (%I k1!)))
             (let
              ((tmp%%$3 (vstd!seq.Seq.len.? A&. A& s!)))
              (and
               (and
                (<= tmp%%$ tmp%%$1)
                (<= tmp%%$1 tmp%%$2)
               )
               (<= tmp%%$2 tmp%%$3)
         ))))))
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$5 (%I j!)))
           (let
            ((tmp%%$6 (%I k2!)))
            (let
             ((tmp%%$7 (vstd!seq.Seq.len.? A&. A& s!)))
             (and
              (and
               (<= tmp%%$ tmp%%$5)
               (<= tmp%%$5 tmp%%$6)
              )
              (<= tmp%%$6 tmp%%$7)
        ))))))
        (let
         ((tmp%%$ 0))
         (let
          ((tmp%%$9 (%I i!)))
          (let
           ((tmp%%$10 (Sub (%I k1!) (%I j!))))
           (and
            (<= tmp%%$ tmp%%$9)
            (< tmp%%$9 tmp%%$10)
       )))))
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$12 (%I i!)))
         (let
          ((tmp%%$13 (Sub (%I k2!) (%I j!))))
          (and
           (<= tmp%%$ tmp%%$12)
           (< tmp%%$12 tmp%%$13)
      )))))
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k1!) i!) (vstd!seq.Seq.index.?
        A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k2!) i!
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.subrange.? A&. A& s! j! k1!) i!)
     (vstd!seq.Seq.subrange.? A&. A& s! j! k2!)
    )
    :qid user_vstd__seq__lemma_seq_two_subranges_index_14
    :skolemid skolem_user_vstd__seq__lemma_seq_two_subranges_index_14
))))

;; Function-Axioms vstd::seq::Seq::add
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (rhs! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type rhs! (TYPE%vstd!seq.Seq. A&. A&))
    )
    (has_type (vstd!seq.Seq.add.? A&. A& self! rhs!) (TYPE%vstd!seq.Seq. A&. A&))
   )
   :pattern ((vstd!seq.Seq.add.? A&. A& self! rhs!))
   :qid internal_vstd!seq.Seq.add.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.Seq.add.?_pre_post_definition
)))

;; Broadcast vstd::seq::lemma_seq_add_len
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_add_len.)
  (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly)) (!
    (=>
     (and
      (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type s2! (TYPE%vstd!seq.Seq. A&. A&))
     )
     (=>
      (sized A&.)
      (= (vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!)) (nClip (Add (vstd!seq.Seq.len.?
          A&. A& s1!
         ) (vstd!seq.Seq.len.? A&. A& s2!)
    )))))
    :pattern ((vstd!seq.Seq.len.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!)))
    :qid user_vstd__seq__lemma_seq_add_len_15
    :skolemid skolem_user_vstd__seq__lemma_seq_add_len_15
))))

;; Broadcast vstd::seq::lemma_seq_add_index1
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_add_index1.)
  (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type s2! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized A&.)
       (< (%I i!) (vstd!seq.Seq.len.? A&. A& s1!))
      )
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!) i!) (vstd!seq.Seq.index.?
        A&. A& s1! i!
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!) i!))
    :qid user_vstd__seq__lemma_seq_add_index1_16
    :skolemid skolem_user_vstd__seq__lemma_seq_add_index1_16
))))

;; Broadcast vstd::seq::lemma_seq_add_index2
(assert
 (=>
  (fuel_bool fuel%vstd!seq.lemma_seq_add_index2.)
  (forall ((A&. Dcr) (A& Type) (s1! Poly) (s2! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s1! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type s2! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized A&.)
       (let
        ((tmp%%$ (vstd!seq.Seq.len.? A&. A& s1!)))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (nClip (Add (vstd!seq.Seq.len.? A&. A& s1!) (vstd!seq.Seq.len.? A&. A& s2!)))))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (= (vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!) i!) (vstd!seq.Seq.index.?
        A&. A& s2! (I (Sub (%I i!) (vstd!seq.Seq.len.? A&. A& s1!)))
    ))))
    :pattern ((vstd!seq.Seq.index.? A&. A& (vstd!seq.Seq.add.? A&. A& s1! s2!) i!))
    :qid user_vstd__seq__lemma_seq_add_index2_17
    :skolemid skolem_user_vstd__seq__lemma_seq_add_index2_17
))))

;; Function-Axioms vstd::seq::impl&%2::spec_add
(assert
 (fuel_bool_default fuel%vstd!seq.impl&%2.spec_add.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!seq.impl&%2.spec_add.)
  (forall ((A&. Dcr) (A& Type) (self! Poly) (rhs! Poly)) (!
    (= (vstd!seq.impl&%2.spec_add.? A&. A& self! rhs!) (vstd!seq.Seq.add.? A&. A& self!
      rhs!
    ))
    :pattern ((vstd!seq.impl&%2.spec_add.? A&. A& self! rhs!))
    :qid internal_vstd!seq.impl&__2.spec_add.?_definition
    :skolemid skolem_internal_vstd!seq.impl&__2.spec_add.?_definition
))))
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly) (rhs! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
     (has_type rhs! (TYPE%vstd!seq.Seq. A&. A&))
    )
    (has_type (vstd!seq.impl&%2.spec_add.? A&. A& self! rhs!) (TYPE%vstd!seq.Seq. A&. A&))
   )
   :pattern ((vstd!seq.impl&%2.spec_add.? A&. A& self! rhs!))
   :qid internal_vstd!seq.impl&__2.spec_add.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq.impl&__2.spec_add.?_pre_post_definition
)))

;; Broadcast vstd::seq_lib::impl&%0::add_empty_left
(assert
 (=>
  (fuel_bool fuel%vstd!seq_lib.impl&%0.add_empty_left.)
  (forall ((A&. Dcr) (A& Type) (a! Poly) (b! Poly)) (!
    (=>
     (and
      (has_type a! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type b! (TYPE%vstd!seq.Seq. A&. A&))
     )
     (=>
      (and
       (sized A&.)
       (= (vstd!seq.Seq.len.? A&. A& a!) 0)
      )
      (= (vstd!seq.Seq.add.? A&. A& a! b!) b!)
    ))
    :pattern ((vstd!seq.Seq.add.? A&. A& a! b!))
    :qid user_vstd__seq_lib__impl&%0__add_empty_left_18
    :skolemid skolem_user_vstd__seq_lib__impl&%0__add_empty_left_18
))))

;; Broadcast vstd::seq_lib::impl&%0::add_empty_right
(assert
 (=>
  (fuel_bool fuel%vstd!seq_lib.impl&%0.add_empty_right.)
  (forall ((A&. Dcr) (A& Type) (a! Poly) (b! Poly)) (!
    (=>
     (and
      (has_type a! (TYPE%vstd!seq.Seq. A&. A&))
      (has_type b! (TYPE%vstd!seq.Seq. A&. A&))
     )
     (=>
      (and
       (sized A&.)
       (= (vstd!seq.Seq.len.? A&. A& b!) 0)
      )
      (= (vstd!seq.Seq.add.? A&. A& a! b!) a!)
    ))
    :pattern ((vstd!seq.Seq.add.? A&. A& a! b!))
    :qid user_vstd__seq_lib__impl&%0__add_empty_right_19
    :skolemid skolem_user_vstd__seq_lib__impl&%0__add_empty_right_19
))))

;; Function-Axioms vstd::multiset::impl&%0::count
(assert
 (forall ((V&. Dcr) (V& Type) (self! Poly) (value! Poly)) (!
   (=>
    (and
     (has_type self! (TYPE%vstd!multiset.Multiset. V&. V&))
     (has_type value! V&)
    )
    (<= 0 (vstd!multiset.impl&%0.count.? V&. V& self! value!))
   )
   :pattern ((vstd!multiset.impl&%0.count.? V&. V& self! value!))
   :qid internal_vstd!multiset.impl&__0.count.?_pre_post_definition
   :skolemid skolem_internal_vstd!multiset.impl&__0.count.?_pre_post_definition
)))

;; Broadcast vstd::multiset::axiom_multiset_ext_equal
(assert
 (=>
  (fuel_bool fuel%vstd!multiset.axiom_multiset_ext_equal.)
  (forall ((V&. Dcr) (V& Type) (m1! Poly) (m2! Poly)) (!
    (=>
     (and
      (has_type m1! (TYPE%vstd!multiset.Multiset. V&. V&))
      (has_type m2! (TYPE%vstd!multiset.Multiset. V&. V&))
     )
     (=>
      (sized V&.)
      (= (ext_eq false (TYPE%vstd!multiset.Multiset. V&. V&) m1! m2!) (forall ((v$ Poly))
        (!
         (=>
          (has_type v$ V&)
          (= (vstd!multiset.impl&%0.count.? V&. V& m1! v$) (vstd!multiset.impl&%0.count.? V&.
            V& m2! v$
         )))
         :pattern ((vstd!multiset.impl&%0.count.? V&. V& m1! v$))
         :pattern ((vstd!multiset.impl&%0.count.? V&. V& m2! v$))
         :qid user_vstd__multiset__axiom_multiset_ext_equal_20
         :skolemid skolem_user_vstd__multiset__axiom_multiset_ext_equal_20
    )))))
    :pattern ((ext_eq false (TYPE%vstd!multiset.Multiset. V&. V&) m1! m2!))
    :qid user_vstd__multiset__axiom_multiset_ext_equal_21
    :skolemid skolem_user_vstd__multiset__axiom_multiset_ext_equal_21
))))

;; Broadcast vstd::multiset::axiom_multiset_ext_equal_deep
(assert
 (=>
  (fuel_bool fuel%vstd!multiset.axiom_multiset_ext_equal_deep.)
  (forall ((V&. Dcr) (V& Type) (m1! Poly) (m2! Poly)) (!
    (=>
     (and
      (has_type m1! (TYPE%vstd!multiset.Multiset. V&. V&))
      (has_type m2! (TYPE%vstd!multiset.Multiset. V&. V&))
     )
     (=>
      (sized V&.)
      (= (ext_eq true (TYPE%vstd!multiset.Multiset. V&. V&) m1! m2!) (ext_eq false (TYPE%vstd!multiset.Multiset.
         V&. V&
        ) m1! m2!
    ))))
    :pattern ((ext_eq true (TYPE%vstd!multiset.Multiset. V&. V&) m1! m2!))
    :qid user_vstd__multiset__axiom_multiset_ext_equal_deep_22
    :skolemid skolem_user_vstd__multiset__axiom_multiset_ext_equal_deep_22
))))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.FnMut. F&. F& A&. A&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (MUTREF F&. F&) A&. A&)
   )
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (MUTREF F&. F&) A&. A&))
   :qid internal_core__ops__function__impls__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__ops__function__impls__impl&__4_trait_impl_definition
)))

;; Broadcast vstd::function::axiom_fn_mut_call_requires
(assert
 (=>
  (fuel_bool fuel%vstd!function.axiom_fn_mut_call_requires.)
  (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (f! Poly) (args! Poly)) (!
    (=>
     (and
      (has_type f! (MUTREF F&. F&))
      (has_type args! Args&)
     )
     (=>
      (and
       (and
        (and
         (and
          (sized Args&.)
          (sized F&.)
         )
         (tr_bound%core!marker.Tuple. Args&. Args&)
        )
        (tr_bound%core!ops.function.FnMut. F&. F& Args&. Args&)
       )
       (closure_req F& Args&. Args& (mut_ref_current% f!) args!)
      )
      (closure_req (MUTREF F&. F&) Args&. Args& f! args!)
    ))
    :pattern ((closure_req (MUTREF F&. F&) Args&. Args& f! args!))
    :qid user_vstd__function__axiom_fn_mut_call_requires_23
    :skolemid skolem_user_vstd__function__axiom_fn_mut_call_requires_23
))))

;; Broadcast vstd::function::axiom_fn_mut_call_ensures
(assert
 (=>
  (fuel_bool fuel%vstd!function.axiom_fn_mut_call_ensures.)
  (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (f! Poly) (args! Poly) (output!
     Poly
    )
   ) (!
    (=>
     (and
      (has_type f! (MUTREF F&. F&))
      (has_type args! Args&)
      (has_type output! (proj%core!ops.function.FnOnce./Output F&. F& Args&. Args&))
     )
     (=>
      (and
       (and
        (and
         (and
          (sized Args&.)
          (sized F&.)
         )
         (tr_bound%core!marker.Tuple. Args&. Args&)
        )
        (tr_bound%core!ops.function.FnMut. F&. F& Args&. Args&)
       )
       (closure_ens (MUTREF F&. F&) Args&. Args& f! args! output!)
      )
      (and
       (closure_ens F& Args&. Args& (mut_ref_current% f!) args! output!)
       (= (mut_ref_current% f!) (mut_ref_future% f!))
    )))
    :pattern ((closure_ens (MUTREF F&. F&) Args&. Args& f! args! output!))
    :qid user_vstd__function__axiom_fn_mut_call_ensures_24
    :skolemid skolem_user_vstd__function__axiom_fn_mut_call_ensures_24
))))

;; Function-Axioms vstd::slice::spec_slice_len
(assert
 (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
   (=>
    (has_type slice! (SLICE T&. T&))
    (uInv SZ (vstd!slice.spec_slice_len.? T&. T& slice!))
   )
   :pattern ((vstd!slice.spec_slice_len.? T&. T& slice!))
   :qid internal_vstd!slice.spec_slice_len.?_pre_post_definition
   :skolemid skolem_internal_vstd!slice.spec_slice_len.?_pre_post_definition
)))

;; Function-Axioms vstd::view::View::view
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (self! Poly)) (!
   (=>
    (has_type self! Self%&)
    (has_type (vstd!view.View.view.? Self%&. Self%& self!) (proj%vstd!view.View./V Self%&.
      Self%&
   )))
   :pattern ((vstd!view.View.view.? Self%&. Self%& self!))
   :qid internal_vstd!view.View.view.?_pre_post_definition
   :skolemid skolem_internal_vstd!view.View.view.?_pre_post_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%vstd!view.View. $slice (SLICE T&. T&))
   )
   :pattern ((tr_bound%vstd!view.View. $slice (SLICE T&. T&)))
   :qid internal_vstd__slice__impl&__0_trait_impl_definition
   :skolemid skolem_internal_vstd__slice__impl&__0_trait_impl_definition
)))

;; Broadcast vstd::slice::axiom_spec_len
(assert
 (=>
  (fuel_bool fuel%vstd!slice.axiom_spec_len.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
    (=>
     (has_type slice! (SLICE T&. T&))
     (=>
      (sized T&.)
      (= (vstd!slice.spec_slice_len.? T&. T& slice!) (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.?
         $slice (SLICE T&. T&) slice!
    )))))
    :pattern ((vstd!slice.spec_slice_len.? T&. T& slice!))
    :qid user_vstd__slice__axiom_spec_len_25
    :skolemid skolem_user_vstd__slice__axiom_spec_len_25
))))

;; Function-Axioms vstd::slice::len%returns_clause_autospec
(assert
 (fuel_bool_default fuel%vstd!slice.len%returns_clause_autospec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!slice.len%returns_clause_autospec.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
    (= (vstd!slice.len%returns_clause_autospec.? T&. T& slice!) (vstd!slice.spec_slice_len.?
      T&. T& slice!
    ))
    :pattern ((vstd!slice.len%returns_clause_autospec.? T&. T& slice!))
    :qid internal_vstd!slice.len__returns_clause_autospec.?_definition
    :skolemid skolem_internal_vstd!slice.len__returns_clause_autospec.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
   (=>
    (has_type slice! (SLICE T&. T&))
    (uInv SZ (vstd!slice.len%returns_clause_autospec.? T&. T& slice!))
   )
   :pattern ((vstd!slice.len%returns_clause_autospec.? T&. T& slice!))
   :qid internal_vstd!slice.len__returns_clause_autospec.?_pre_post_definition
   :skolemid skolem_internal_vstd!slice.len__returns_clause_autospec.?_pre_post_definition
)))

;; Function-Specs vstd::slice::SliceAdditionalSpecFns::spec_index
(declare-fun req%vstd!slice.SliceAdditionalSpecFns.spec_index. (Dcr Type Dcr Type Poly
  Poly
 ) Bool
)
(declare-const %%global_location_label%%4 Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (= (req%vstd!slice.SliceAdditionalSpecFns.spec_index. Self%&. Self%& T&. T& self! i!)
    (=>
     %%global_location_label%%4
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I i!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? Self%&. Self%& self!))))
        (and
         (<= tmp%%$ tmp%%$1)
         (< tmp%%$1 tmp%%$2)
   ))))))
   :pattern ((req%vstd!slice.SliceAdditionalSpecFns.spec_index. Self%&. Self%& T&. T&
     self! i!
   ))
   :qid internal_req__vstd!slice.SliceAdditionalSpecFns.spec_index._definition
   :skolemid skolem_internal_req__vstd!slice.SliceAdditionalSpecFns.spec_index._definition
)))

;; Function-Axioms vstd::slice::SliceAdditionalSpecFns::spec_index
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (=>
    (and
     (has_type self! Self%&)
     (has_type i! INT)
    )
    (has_type (vstd!slice.SliceAdditionalSpecFns.spec_index.? Self%&. Self%& T&. T& self!
      i!
     ) T&
   ))
   :pattern ((vstd!slice.SliceAdditionalSpecFns.spec_index.? Self%&. Self%& T&. T& self!
     i!
   ))
   :qid internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_pre_post_definition
   :skolemid skolem_internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_pre_post_definition
)))

;; Function-Axioms vstd::slice::impl&%2::spec_index
(assert
 (fuel_bool_default fuel%vstd!slice.impl&%2.spec_index.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!slice.impl&%2.spec_index.)
  (forall ((T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (!
    (=>
     (sized T&.)
     (= (vstd!slice.SliceAdditionalSpecFns.spec_index.? $slice (SLICE T&. T&) T&. T& self!
       i!
      ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) self!)
       i!
    )))
    :pattern ((vstd!slice.SliceAdditionalSpecFns.spec_index.? $slice (SLICE T&. T&) T&.
      T& self! i!
    ))
    :qid internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_definition
    :skolemid skolem_internal_vstd!slice.SliceAdditionalSpecFns.spec_index.?_definition
))))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%vstd!slice.SliceAdditionalSpecFns. $slice (SLICE T&. T&) T&. T&)
   )
   :pattern ((tr_bound%vstd!slice.SliceAdditionalSpecFns. $slice (SLICE T&. T&) T&. T&))
   :qid internal_vstd__slice__impl&__2_trait_impl_definition
   :skolemid skolem_internal_vstd__slice__impl&__2_trait_impl_definition
)))

;; Broadcast vstd::slice::axiom_slice_ext_equal
(assert
 (=>
  (fuel_bool fuel%vstd!slice.axiom_slice_ext_equal.)
  (forall ((T&. Dcr) (T& Type) (a1! Poly) (a2! Poly)) (!
    (=>
     (and
      (has_type a1! (SLICE T&. T&))
      (has_type a2! (SLICE T&. T&))
     )
     (=>
      (sized T&.)
      (= (ext_eq false (SLICE T&. T&) a1! a2!) (and
        (= (vstd!slice.len%returns_clause_autospec.? T&. T& a1!) (vstd!slice.len%returns_clause_autospec.?
          T&. T& a2!
        ))
        (forall ((i$ Poly)) (!
          (=>
           (has_type i$ INT)
           (=>
            (let
             ((tmp%%$ 0))
             (let
              ((tmp%%$1 (%I i$)))
              (let
               ((tmp%%$2 (vstd!slice.len%returns_clause_autospec.? T&. T& a1!)))
               (and
                (<= tmp%%$ tmp%%$1)
                (< tmp%%$1 tmp%%$2)
            ))))
            (= (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) a1!) i$)
             (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) a2!) i$)
          )))
          :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
             a1!
            ) i$
          ))
          :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
             a2!
            ) i$
          ))
          :qid user_vstd__slice__axiom_slice_ext_equal_26
          :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_26
    ))))))
    :pattern ((ext_eq false (SLICE T&. T&) a1! a2!))
    :qid user_vstd__slice__axiom_slice_ext_equal_27
    :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_27
))))

;; Broadcast vstd::slice::axiom_slice_has_resolved
(assert
 (=>
  (fuel_bool fuel%vstd!slice.axiom_slice_has_resolved.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type slice! (SLICE T&. T&))
      (has_type i! INT)
     )
     (=>
      (sized T&.)
      (=>
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!slice.spec_slice_len.? T&. T& slice!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
       ))))
       (=>
        (has_resolved $slice (SLICE T&. T&) slice!)
        (has_resolved T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE
            T&. T&
           ) slice!
          ) i!
    ))))))
    :pattern ((has_resolved $slice (SLICE T&. T&) slice!) (vstd!seq.Seq.index.? T&. T&
      (vstd!view.View.view.? $slice (SLICE T&. T&) slice!) i!
    ))
    :qid user_vstd__slice__axiom_slice_has_resolved_28
    :skolemid skolem_user_vstd__slice__axiom_slice_has_resolved_28
))))

;; Function-Axioms vstd::array::array_view
(assert
 (fuel_bool_default fuel%vstd!array.array_view.)
)
(declare-fun %%lambda%%0 (Dcr Type Dcr Type %%Function%%) %%Function%%)
(assert
 (forall ((%%hole%%0 Dcr) (%%hole%%1 Type) (%%hole%%2 Dcr) (%%hole%%3 Type) (%%hole%%4
    %%Function%%
   ) (i$ Poly)
  ) (!
   (= (%%apply%%0 (%%lambda%%0 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3 %%hole%%4) i$)
    (array_index %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3 %%hole%%4 i$)
   )
   :pattern ((%%apply%%0 (%%lambda%%0 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3 %%hole%%4)
     i$
)))))
(assert
 (=>
  (fuel_bool fuel%vstd!array.array_view.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a! Poly)) (!
    (= (vstd!array.array_view.? T&. T& N&. N& a!) (vstd!seq.Seq.new.? T&. T& (I (const_int
        N&
       )
      ) (Poly%fun%1. (mk_fun (%%lambda%%0 T&. T& N&. N& (%Poly%array%. a!))))
    ))
    :pattern ((vstd!array.array_view.? T&. T& N&. N& a!))
    :qid internal_vstd!array.array_view.?_definition
    :skolemid skolem_internal_vstd!array.array_view.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a! Poly)) (!
   (=>
    (has_type a! (ARRAY T&. T& N&. N&))
    (has_type (vstd!array.array_view.? T&. T& N&. N& a!) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((vstd!array.array_view.? T&. T& N&. N& a!))
   :qid internal_vstd!array.array_view.?_pre_post_definition
   :skolemid skolem_internal_vstd!array.array_view.?_pre_post_definition
)))

;; Function-Axioms vstd::array::impl&%0::view
(assert
 (fuel_bool_default fuel%vstd!array.impl&%0.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!array.impl&%0.view.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (self! Poly)) (!
    (=>
     (and
      (sized T&.)
      (uInv SZ (const_int N&))
     )
     (= (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) self!) (vstd!array.array_view.? T&.
       T& N&. N& self!
    )))
    :pattern ((vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%vstd!view.View. $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%vstd!view.View. $ (ARRAY T&. T& N&. N&)))
   :qid internal_vstd__array__impl&__0_trait_impl_definition
   :skolemid skolem_internal_vstd__array__impl&__0_trait_impl_definition
)))

;; Broadcast vstd::array::array_len_matches_n
(assert
 (=>
  (fuel_bool fuel%vstd!array.array_len_matches_n.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (ar! Poly)) (!
    (=>
     (has_type ar! (ARRAY T&. T& N&. N&))
     (=>
      (and
       (sized T&.)
       (uInv SZ (const_int N&))
      )
      (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) ar!))
       (const_int N&)
    )))
    :pattern ((vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
       ar!
    )))
    :qid user_vstd__array__array_len_matches_n_29
    :skolemid skolem_user_vstd__array__array_len_matches_n_29
))))

;; Function-Specs vstd::array::ArrayAdditionalSpecFns::spec_index
(declare-fun req%vstd!array.ArrayAdditionalSpecFns.spec_index. (Dcr Type Dcr Type Poly
  Poly
 ) Bool
)
(declare-const %%global_location_label%%5 Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (= (req%vstd!array.ArrayAdditionalSpecFns.spec_index. Self%&. Self%& T&. T& self! i!)
    (=>
     %%global_location_label%%5
     (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I i!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? Self%&. Self%& self!))))
        (and
         (<= tmp%%$ tmp%%$1)
         (< tmp%%$1 tmp%%$2)
   ))))))
   :pattern ((req%vstd!array.ArrayAdditionalSpecFns.spec_index. Self%&. Self%& T&. T&
     self! i!
   ))
   :qid internal_req__vstd!array.ArrayAdditionalSpecFns.spec_index._definition
   :skolemid skolem_internal_req__vstd!array.ArrayAdditionalSpecFns.spec_index._definition
)))

;; Function-Axioms vstd::array::ArrayAdditionalSpecFns::spec_index
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (=>
    (and
     (has_type self! Self%&)
     (has_type i! INT)
    )
    (has_type (vstd!array.ArrayAdditionalSpecFns.spec_index.? Self%&. Self%& T&. T& self!
      i!
     ) T&
   ))
   :pattern ((vstd!array.ArrayAdditionalSpecFns.spec_index.? Self%&. Self%& T&. T& self!
     i!
   ))
   :qid internal_vstd!array.ArrayAdditionalSpecFns.spec_index.?_pre_post_definition
   :skolemid skolem_internal_vstd!array.ArrayAdditionalSpecFns.spec_index.?_pre_post_definition
)))

;; Function-Axioms vstd::array::impl&%2::spec_index
(assert
 (fuel_bool_default fuel%vstd!array.impl&%2.spec_index.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!array.impl&%2.spec_index.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (self! Poly) (i! Poly)) (!
    (=>
     (and
      (sized T&.)
      (uInv SZ (const_int N&))
     )
     (= (vstd!array.ArrayAdditionalSpecFns.spec_index.? $ (ARRAY T&. T& N&. N&) T&. T& self!
       i!
      ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) self!)
       i!
    )))
    :pattern ((vstd!array.ArrayAdditionalSpecFns.spec_index.? $ (ARRAY T&. T& N&. N&) T&.
      T& self! i!
    ))
    :qid internal_vstd!array.ArrayAdditionalSpecFns.spec_index.?_definition
    :skolemid skolem_internal_vstd!array.ArrayAdditionalSpecFns.spec_index.?_definition
))))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%vstd!array.ArrayAdditionalSpecFns. $ (ARRAY T&. T& N&. N&) T&. T&)
   )
   :pattern ((tr_bound%vstd!array.ArrayAdditionalSpecFns. $ (ARRAY T&. T& N&. N&) T&.
     T&
   ))
   :qid internal_vstd__array__impl&__2_trait_impl_definition
   :skolemid skolem_internal_vstd__array__impl&__2_trait_impl_definition
)))

;; Broadcast vstd::array::lemma_array_index
(assert
 (=>
  (fuel_bool fuel%vstd!array.lemma_array_index.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type a! (ARRAY T&. T& N&. N&))
      (has_type i! INT)
     )
     (=>
      (and
       (and
        (sized T&.)
        (uInv SZ (const_int N&))
       )
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (const_int N&)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (= (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a!)
        i!
       ) (vstd!seq.Seq.index.? T&. T& (vstd!array.array_view.? T&. T& N&. N& a!) i!)
    )))
    :pattern ((array_index T&. T& N&. N& (%Poly%array%. a!) i!))
    :qid user_vstd__array__lemma_array_index_30
    :skolemid skolem_user_vstd__array__lemma_array_index_30
))))

;; Broadcast vstd::array::axiom_array_ext_equal
(assert
 (=>
  (fuel_bool fuel%vstd!array.axiom_array_ext_equal.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a1! Poly) (a2! Poly)) (!
    (=>
     (and
      (has_type a1! (ARRAY T&. T& N&. N&))
      (has_type a2! (ARRAY T&. T& N&. N&))
     )
     (=>
      (and
       (sized T&.)
       (uInv SZ (const_int N&))
      )
      (= (ext_eq false (ARRAY T&. T& N&. N&) a1! a2!) (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$1 (%I i$)))
             (let
              ((tmp%%$2 (const_int N&)))
              (and
               (<= tmp%%$ tmp%%$1)
               (< tmp%%$1 tmp%%$2)
           ))))
           (= (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a1!)
             i$
            ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a2!)
             i$
         ))))
         :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
            a1!
           ) i$
         ))
         :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
            a2!
           ) i$
         ))
         :qid user_vstd__array__axiom_array_ext_equal_31
         :skolemid skolem_user_vstd__array__axiom_array_ext_equal_31
    )))))
    :pattern ((ext_eq false (ARRAY T&. T& N&. N&) a1! a2!))
    :qid user_vstd__array__axiom_array_ext_equal_32
    :skolemid skolem_user_vstd__array__axiom_array_ext_equal_32
))))

;; Broadcast vstd::array::axiom_array_has_resolved
(assert
 (=>
  (fuel_bool fuel%vstd!array.axiom_array_has_resolved.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type array! (ARRAY T&. T& N&. N&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized T&.)
       (uInv SZ (const_int N&))
      )
      (=>
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (const_int N&)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
       ))))
       (=>
        (has_resolved $ (ARRAY T&. T& N&. N&) array!)
        (has_resolved T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&.
            T& N&. N&
           ) array!
          ) i!
    ))))))
    :pattern ((has_resolved $ (ARRAY T&. T& N&. N&) array!) (vstd!seq.Seq.index.? T&. T&
      (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) array!) i!
    ))
    :qid user_vstd__array__axiom_array_has_resolved_33
    :skolemid skolem_user_vstd__array__axiom_array_has_resolved_33
))))

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $slice STRSLICE)
)

;; Broadcast vstd::string::axiom_str_literal_len
(assert
 (=>
  (fuel_bool fuel%vstd!string.axiom_str_literal_len.)
  (forall ((s! Poly)) (!
    (=>
     (has_type s! STRSLICE)
     (= (vstd!seq.Seq.len.? $ CHAR (vstd!view.View.view.? $slice STRSLICE s!)) (str%strslice_len
       (%Poly%strslice%. s!)
    )))
    :pattern ((vstd!seq.Seq.len.? $ CHAR (vstd!view.View.view.? $slice STRSLICE s!)))
    :qid user_vstd__string__axiom_str_literal_len_34
    :skolemid skolem_user_vstd__string__axiom_str_literal_len_34
))))

;; Broadcast vstd::string::axiom_str_literal_get_char
(assert
 (=>
  (fuel_bool fuel%vstd!string.axiom_str_literal_get_char.)
  (forall ((s! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s! STRSLICE)
      (has_type i! INT)
     )
     (= (%I (vstd!seq.Seq.index.? $ CHAR (vstd!view.View.view.? $slice STRSLICE s!) i!))
      (str%strslice_get_char (%Poly%strslice%. s!) (%I i!))
    ))
    :pattern ((vstd!seq.Seq.index.? $ CHAR (vstd!view.View.view.? $slice STRSLICE s!) i!))
    :qid user_vstd__string__axiom_str_literal_get_char_35
    :skolemid skolem_user_vstd__string__axiom_str_literal_get_char_35
))))

;; Function-Axioms vstd::raw_ptr::view_reverse_for_eq
(assert
 (forall ((T&. Dcr) (T& Type) (data! Poly)) (!
   (=>
    (has_type data! (TYPE%vstd!raw_ptr.PtrData. T&. T&))
    (has_type (vstd!raw_ptr.view_reverse_for_eq.? T&. T& data!) (PTR T&. T&))
   )
   :pattern ((vstd!raw_ptr.view_reverse_for_eq.? T&. T& data!))
   :qid internal_vstd!raw_ptr.view_reverse_for_eq.?_pre_post_definition
   :skolemid skolem_internal_vstd!raw_ptr.view_reverse_for_eq.?_pre_post_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%vstd!view.View. $ (PTR T&. T&))
   :pattern ((tr_bound%vstd!view.View. $ (PTR T&. T&)))
   :qid internal_vstd__raw_ptr__impl&__2_trait_impl_definition
   :skolemid skolem_internal_vstd__raw_ptr__impl&__2_trait_impl_definition
)))

;; Broadcast vstd::raw_ptr::ptrs_mut_eq
(assert
 (=>
  (fuel_bool fuel%vstd!raw_ptr.ptrs_mut_eq.)
  (forall ((T&. Dcr) (T& Type) (a! Poly)) (!
    (=>
     (has_type a! (PTR T&. T&))
     (= (vstd!raw_ptr.view_reverse_for_eq.? T&. T& (vstd!view.View.view.? $ (PTR T&. T&)
        a!
       )
      ) a!
    ))
    :pattern ((vstd!view.View.view.? $ (PTR T&. T&) a!))
    :qid user_vstd__raw_ptr__ptrs_mut_eq_36
    :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_36
))))

;; Function-Axioms vstd::raw_ptr::view_reverse_for_eq_sized
(assert
 (forall ((T&. Dcr) (T& Type) (addr! Poly) (provenance! Poly)) (!
   (=>
    (and
     (has_type addr! USIZE)
     (has_type provenance! TYPE%vstd!raw_ptr.Provenance.)
    )
    (has_type (vstd!raw_ptr.view_reverse_for_eq_sized.? T&. T& addr! provenance!) (PTR
      T&. T&
   )))
   :pattern ((vstd!raw_ptr.view_reverse_for_eq_sized.? T&. T& addr! provenance!))
   :qid internal_vstd!raw_ptr.view_reverse_for_eq_sized.?_pre_post_definition
   :skolemid skolem_internal_vstd!raw_ptr.view_reverse_for_eq_sized.?_pre_post_definition
)))

;; Broadcast vstd::raw_ptr::ptrs_mut_eq_sized
(assert
 (=>
  (fuel_bool fuel%vstd!raw_ptr.ptrs_mut_eq_sized.)
  (forall ((T&. Dcr) (T& Type) (a! Poly)) (!
    (=>
     (has_type a! (PTR T&. T&))
     (=>
      (sized T&.)
      (= (vstd!raw_ptr.view_reverse_for_eq_sized.? T&. T& (I (vstd!raw_ptr.PtrData./PtrData/addr
          (%Poly%vstd!raw_ptr.PtrData. (vstd!view.View.view.? $ (PTR T&. T&) a!))
         )
        ) (Poly%vstd!raw_ptr.Provenance. (vstd!raw_ptr.PtrData./PtrData/provenance (%Poly%vstd!raw_ptr.PtrData.
           (vstd!view.View.view.? $ (PTR T&. T&) a!)
        )))
       ) a!
    )))
    :pattern ((vstd!view.View.view.? $ (PTR T&. T&) a!))
    :qid user_vstd__raw_ptr__ptrs_mut_eq_sized_37
    :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_sized_37
))))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Tuple. $ TYPE%tuple%0.)
)

;; Function-Specs core::clone::Clone::clone
(declare-fun ens%core!clone.Clone.clone. (Dcr Type Poly Poly) Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (self! Poly) (%return! Poly)) (!
   (= (ens%core!clone.Clone.clone. Self%&. Self%& self! %return!) (has_type %return! Self%&))
   :pattern ((ens%core!clone.Clone.clone. Self%&. Self%& self! %return!))
   :qid internal_ens__core!clone.Clone.clone._definition
   :skolemid skolem_internal_ens__core!clone.Clone.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (Self%&. Dcr) (Self%& Type)) (!
   (=>
    (has_type closure%$ (TYPE%tuple%1. (REF Self%&.) Self%&))
    (=>
     (let
      ((self$ (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$))))
      true
     )
     (closure_req (FNDEF%core!clone.Clone.clone. Self%&. Self%&) (DST (REF Self%&.)) (TYPE%tuple%1.
       (REF Self%&.) Self%&
      ) (F fndef_singleton) closure%$
   )))
   :pattern ((closure_req (FNDEF%core!clone.Clone.clone. Self%&. Self%&) (DST (REF Self%&.))
     (TYPE%tuple%1. (REF Self%&.) Self%&) (F fndef_singleton) closure%$
   ))
   :qid user_core__clone__Clone__clone_38
   :skolemid skolem_user_core__clone__Clone__clone_38
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type)) (!
   (tr_bound%core!marker.Tuple. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&))
   :pattern ((tr_bound%core!marker.Tuple. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_crate__impl_tuple&__Tuple1_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Tuple1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type)) (!
   (=>
    (tr_bound%core!clone.Clone. T%0&. T%0&)
    (tr_bound%core!clone.Clone. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&))
   )
   :pattern ((tr_bound%core!clone.Clone. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_crate__impl_tuple&__Clone1_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Clone1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type)) (!
   (=>
    (tr_bound%core!marker.Copy. T%0&. T%0&)
    (tr_bound%core!marker.Copy. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&))
   )
   :pattern ((tr_bound%core!marker.Copy. (DST T%0&.) (TYPE%tuple%1. T%0&. T%0&)))
   :qid internal_crate__impl_tuple&__Copy1_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Copy1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type)) (!
   (tr_bound%core!marker.Tuple. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
   :pattern ((tr_bound%core!marker.Tuple. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__impl_tuple&__Tuple2_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Tuple2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type)) (!
   (=>
    (and
     (tr_bound%core!clone.Clone. T%0&. T%0&)
     (tr_bound%core!clone.Clone. T%1&. T%1&)
    )
    (tr_bound%core!clone.Clone. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
   )
   :pattern ((tr_bound%core!clone.Clone. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__impl_tuple&__Clone2_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Clone2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T%0&. Dcr) (T%0& Type) (T%1&. Dcr) (T%1& Type)) (!
   (=>
    (and
     (tr_bound%core!marker.Copy. T%0&. T%0&)
     (tr_bound%core!marker.Copy. T%1&. T%1&)
    )
    (tr_bound%core!marker.Copy. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&))
   )
   :pattern ((tr_bound%core!marker.Copy. (DST T%1&.) (TYPE%tuple%2. T%0&. T%0& T%1&. T%1&)))
   :qid internal_crate__impl_tuple&__Copy2_trait_impl_definition
   :skolemid skolem_internal_crate__impl_tuple&__Copy2_trait_impl_definition
)))

;; Function-Specs core::clone::impls::impl&%11::clone
(declare-fun ens%core!clone.impls.impl&%11.clone. (Poly Poly) Bool)
(assert
 (forall ((x! Poly) (res! Poly)) (!
   (= (ens%core!clone.impls.impl&%11.clone. x! res!) (and
     (ens%core!clone.Clone.clone. $ (UINT 8) x! res!)
     (= res! x!)
   ))
   :pattern ((ens%core!clone.impls.impl&%11.clone. x! res!))
   :qid internal_ens__core!clone.impls.impl&__11.clone._definition
   :skolemid skolem_internal_ens__core!clone.impls.impl&__11.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) (UINT 8)))
     (has_type res$ (UINT 8))
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ (UINT 8)) (DST (REF $)) (TYPE%tuple%1.
       (REF $) (UINT 8)
      ) (F fndef_singleton) closure%$ res$
     )
     (let
      ((x$ (%I (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (= (%I res$) x$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ (UINT 8)) (DST (REF $)) (TYPE%tuple%1.
      (REF $) (UINT 8)
     ) (F fndef_singleton) closure%$ res$
   ))
   :qid user_core__clone__impls__impl&%11__clone_39
   :skolemid skolem_user_core__clone__impls__impl&%11__clone_39
)))

;; Function-Specs core::clone::impls::impl&%9::clone
(declare-fun ens%core!clone.impls.impl&%9.clone. (Poly Poly) Bool)
(assert
 (forall ((x! Poly) (res! Poly)) (!
   (= (ens%core!clone.impls.impl&%9.clone. x! res!) (and
     (ens%core!clone.Clone.clone. $ USIZE x! res!)
     (= res! x!)
   ))
   :pattern ((ens%core!clone.impls.impl&%9.clone. x! res!))
   :qid internal_ens__core!clone.impls.impl&__9.clone._definition
   :skolemid skolem_internal_ens__core!clone.impls.impl&__9.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) USIZE))
     (has_type res$ USIZE)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ USIZE) (DST (REF $)) (TYPE%tuple%1. (
        REF $
       ) USIZE
      ) (F fndef_singleton) closure%$ res$
     )
     (let
      ((x$ (%I (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (= (%I res$) x$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ USIZE) (DST (REF $)) (TYPE%tuple%1.
      (REF $) USIZE
     ) (F fndef_singleton) closure%$ res$
   ))
   :qid user_core__clone__impls__impl&%9__clone_40
   :skolemid skolem_user_core__clone__impls__impl&%9__clone_40
)))

;; Function-Specs core::clone::impls::impl&%41::clone
(declare-fun ens%core!clone.impls.impl&%41.clone. (Poly Poly) Bool)
(assert
 (forall ((b! Poly) (%return! Poly)) (!
   (= (ens%core!clone.impls.impl&%41.clone. b! %return!) (and
     (ens%core!clone.Clone.clone. $ BOOL b! %return!)
     (= %return! b!)
   ))
   :pattern ((ens%core!clone.impls.impl&%41.clone. b! %return!))
   :qid internal_ens__core!clone.impls.impl&__41.clone._definition
   :skolemid skolem_internal_ens__core!clone.impls.impl&__41.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (%return$ Poly)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) BOOL))
     (has_type %return$ BOOL)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ BOOL) (DST (REF $)) (TYPE%tuple%1. (REF
        $
       ) BOOL
      ) (F fndef_singleton) closure%$ %return$
     )
     (let
      ((b$ (%B (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (= (%B %return$) b$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ BOOL) (DST (REF $)) (TYPE%tuple%1.
      (REF $) BOOL
     ) (F fndef_singleton) closure%$ %return$
   ))
   :qid user_core__clone__impls__impl&%41__clone_41
   :skolemid skolem_user_core__clone__impls__impl&%41__clone_41
)))

;; Function-Specs core::clone::impls::impl&%43::clone
(declare-fun ens%core!clone.impls.impl&%43.clone. (Poly Poly) Bool)
(assert
 (forall ((c! Poly) (%return! Poly)) (!
   (= (ens%core!clone.impls.impl&%43.clone. c! %return!) (and
     (ens%core!clone.Clone.clone. $ CHAR c! %return!)
     (= %return! c!)
   ))
   :pattern ((ens%core!clone.impls.impl&%43.clone. c! %return!))
   :qid internal_ens__core!clone.impls.impl&__43.clone._definition
   :skolemid skolem_internal_ens__core!clone.impls.impl&__43.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (%return$ Poly)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) CHAR))
     (has_type %return$ CHAR)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ CHAR) (DST (REF $)) (TYPE%tuple%1. (REF
        $
       ) CHAR
      ) (F fndef_singleton) closure%$ %return$
     )
     (let
      ((c$ (%I (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (= (%I %return$) c$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ CHAR) (DST (REF $)) (TYPE%tuple%1.
      (REF $) CHAR
     ) (F fndef_singleton) closure%$ %return$
   ))
   :qid user_core__clone__impls__impl&%43__clone_42
   :skolemid skolem_user_core__clone__impls__impl&%43__clone_42
)))

;; Function-Specs core::clone::impls::impl&%6::clone
(declare-fun ens%core!clone.impls.impl&%6.clone. (Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (b! Poly) (res! Poly)) (!
   (= (ens%core!clone.impls.impl&%6.clone. T&. T& b! res!) (and
     (ens%core!clone.Clone.clone. (REF T&.) T& b! res!)
     (= res! b!)
   ))
   :pattern ((ens%core!clone.impls.impl&%6.clone. T&. T& b! res!))
   :qid internal_ens__core!clone.impls.impl&__6.clone._definition
   :skolemid skolem_internal_ens__core!clone.impls.impl&__6.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF (REF T&.)) T&))
     (has_type res$ T&)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. (REF T&.) T&) (DST (REF (REF T&.))) (TYPE%tuple%1.
       (REF (REF T&.)) T&
      ) (F fndef_singleton) closure%$ res$
     )
     (let
      ((b$ (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$))))
      (= res$ b$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. (REF T&.) T&) (DST (REF (REF T&.)))
     (TYPE%tuple%1. (REF (REF T&.)) T&) (F fndef_singleton) closure%$ res$
   ))
   :qid user_core__clone__impls__impl&%6__clone_43
   :skolemid skolem_user_core__clone__impls__impl&%6__clone_43
)))

;; Function-Axioms vstd::pervasive::strictly_cloned
(assert
 (fuel_bool_default fuel%vstd!pervasive.strictly_cloned.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!pervasive.strictly_cloned.)
  (forall ((T&. Dcr) (T& Type) (a! Poly) (b! Poly)) (!
    (= (vstd!pervasive.strictly_cloned.? T&. T& a! b!) (closure_ens (FNDEF%core!clone.Clone.clone.
       T&. T&
      ) (DST (REF T&.)) (TYPE%tuple%1. (REF T&.) T&) (F fndef_singleton) (Poly%tuple%1.
       (tuple%1./tuple%1 a!)
      ) b!
    ))
    :pattern ((vstd!pervasive.strictly_cloned.? T&. T& a! b!))
    :qid internal_vstd!pervasive.strictly_cloned.?_definition
    :skolemid skolem_internal_vstd!pervasive.strictly_cloned.?_definition
))))

;; Function-Axioms vstd::pervasive::cloned
(assert
 (fuel_bool_default fuel%vstd!pervasive.cloned.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!pervasive.cloned.)
  (forall ((T&. Dcr) (T& Type) (a! Poly) (b! Poly)) (!
    (= (vstd!pervasive.cloned.? T&. T& a! b!) (or
      (vstd!pervasive.strictly_cloned.? T&. T& a! b!)
      (= a! b!)
    ))
    :pattern ((vstd!pervasive.cloned.? T&. T& a! b!))
    :qid internal_vstd!pervasive.cloned.?_definition
    :skolemid skolem_internal_vstd!pervasive.cloned.?_definition
))))

;; Function-Specs core::array::impl&%20::clone
(declare-fun ens%core!array.impl&%20.clone. (Dcr Type Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a! Poly) (res! Poly)) (!
   (= (ens%core!array.impl&%20.clone. T&. T& N&. N& a! res!) (and
     (ens%core!clone.Clone.clone. $ (ARRAY T&. T& N&. N&) a! res!)
     (forall ((i$ Poly)) (!
       (=>
        (has_type i$ INT)
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (const_int N&)))
            (and
             (<= tmp%%$ tmp%%$1)
             (< tmp%%$1 tmp%%$2)
         ))))
         (vstd!pervasive.cloned.? T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.?
            $ (ARRAY T&. T& N&. N&) a!
           ) i$
          ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res!)
           i$
       ))))
       :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
          a!
         ) i$
       ))
       :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
          res!
         ) i$
       ))
       :pattern ((vstd!pervasive.cloned.? T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.?
           $ (ARRAY T&. T& N&. N&) a!
          ) i$
         ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res!)
          i$
       )))
       :qid user_core__array__impl&%20__clone_44
       :skolemid skolem_user_core__array__impl&%20__clone_44
     ))
     (=>
      (ext_eq false (TYPE%vstd!seq.Seq. T&. T&) (vstd!view.View.view.? $ (ARRAY T&. T& N&.
         N&
        ) a!
       ) (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res!)
      )
      (= (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a!) (vstd!view.View.view.? $ (ARRAY
         T&. T& N&. N&
        ) res!
   )))))
   :pattern ((ens%core!array.impl&%20.clone. T&. T& N&. N& a! res!))
   :qid internal_ens__core!array.impl&__20.clone._definition
   :skolemid skolem_internal_ens__core!array.impl&__20.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&)))
     (has_type res$ (ARRAY T&. T& N&. N&))
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ (ARRAY T&. T& N&. N&)) (DST (REF $))
      (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&)) (F fndef_singleton) closure%$ res$
     )
     (let
      ((a$ (%Poly%array%. (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (and
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$1 (%I i$)))
             (let
              ((tmp%%$2 (const_int N&)))
              (and
               (<= tmp%%$ tmp%%$1)
               (< tmp%%$1 tmp%%$2)
           ))))
           (vstd!pervasive.cloned.? T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.?
              $ (ARRAY T&. T& N&. N&) (Poly%array%. a$)
             ) i$
            ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res$)
             i$
         ))))
         :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
            (Poly%array%. a$)
           ) i$
         ))
         :pattern ((vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&)
            res$
           ) i$
         ))
         :pattern ((vstd!pervasive.cloned.? T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.?
             $ (ARRAY T&. T& N&. N&) (Poly%array%. a$)
            ) i$
           ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res$)
            i$
         )))
         :qid user_core__array__impl&%20__clone_45
         :skolemid skolem_user_core__array__impl&%20__clone_45
       ))
       (=>
        (ext_eq false (TYPE%vstd!seq.Seq. T&. T&) (vstd!view.View.view.? $ (ARRAY T&. T& N&.
           N&
          ) (Poly%array%. a$)
         ) (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) res$)
        )
        (= (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) (Poly%array%. a$)) (vstd!view.View.view.?
          $ (ARRAY T&. T& N&. N&) res$
   )))))))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ (ARRAY T&. T& N&. N&)) (DST
      (REF $)
     ) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&)) (F fndef_singleton) closure%$ res$
   ))
   :qid user_core__array__impl&%20__clone_46
   :skolemid skolem_user_core__array__impl&%20__clone_46
)))

;; Function-Specs verus_builtin::impl&%9::clone
(declare-fun ens%verus_builtin!impl&%9.clone. (Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (b! Poly) (res! Poly)) (!
   (= (ens%verus_builtin!impl&%9.clone. T&. T& b! res!) (and
     (ens%core!clone.Clone.clone. (TRACKED T&.) T& b! res!)
     (= res! b!)
   ))
   :pattern ((ens%verus_builtin!impl&%9.clone. T&. T& b! res!))
   :qid internal_ens__verus_builtin!impl&__9.clone._definition
   :skolemid skolem_internal_ens__verus_builtin!impl&__9.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF (TRACKED T&.)) T&))
     (has_type res$ T&)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. (TRACKED T&.) T&) (DST (REF (TRACKED T&.)))
      (TYPE%tuple%1. (REF (TRACKED T&.)) T&) (F fndef_singleton) closure%$ res$
     )
     (let
      ((b$ (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$))))
      (= res$ b$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. (TRACKED T&.) T&) (DST (REF (TRACKED
        T&.
      ))
     ) (TYPE%tuple%1. (REF (TRACKED T&.)) T&) (F fndef_singleton) closure%$ res$
   ))
   :qid user_verus_builtin__impl&%9__clone_47
   :skolemid skolem_user_verus_builtin__impl&%9__clone_47
)))

;; Function-Specs verus_builtin::impl&%7::clone
(declare-fun ens%verus_builtin!impl&%7.clone. (Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (b! Poly) (res! Poly)) (!
   (= (ens%verus_builtin!impl&%7.clone. T&. T& b! res!) (and
     (ens%core!clone.Clone.clone. (GHOST T&.) T& b! res!)
     (= res! b!)
   ))
   :pattern ((ens%verus_builtin!impl&%7.clone. T&. T& b! res!))
   :qid internal_ens__verus_builtin!impl&__7.clone._definition
   :skolemid skolem_internal_ens__verus_builtin!impl&__7.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF (GHOST T&.)) T&))
     (has_type res$ T&)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. (GHOST T&.) T&) (DST (REF (GHOST T&.)))
      (TYPE%tuple%1. (REF (GHOST T&.)) T&) (F fndef_singleton) closure%$ res$
     )
     (let
      ((b$ (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$))))
      (= res$ b$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. (GHOST T&.) T&) (DST (REF (GHOST
        T&.
      ))
     ) (TYPE%tuple%1. (REF (GHOST T&.)) T&) (F fndef_singleton) closure%$ res$
   ))
   :qid user_verus_builtin__impl&%7__clone_48
   :skolemid skolem_user_verus_builtin__impl&%7__clone_48
)))

;; Function-Axioms vstd::std_specs::option::OptionAdditionalFns::arrow_Some_0
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly)) (!
   (=>
    (has_type self! Self%&)
    (has_type (vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.? Self%&. Self%&
      T&. T& self!
     ) T&
   ))
   :pattern ((vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.? Self%&. Self%&
     T&. T& self!
   ))
   :qid internal_vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.?_pre_post_definition
)))

;; Function-Axioms vstd::std_specs::option::OptionAdditionalFns::arrow_0
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly)) (!
   (=>
    (has_type self! Self%&)
    (has_type (vstd!std_specs.option.OptionAdditionalFns.arrow_0.? Self%&. Self%& T&. T&
      self!
     ) T&
   ))
   :pattern ((vstd!std_specs.option.OptionAdditionalFns.arrow_0.? Self%&. Self%& T&. T&
     self!
   ))
   :qid internal_vstd!std_specs.option.OptionAdditionalFns.arrow_0.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.option.OptionAdditionalFns.arrow_0.?_pre_post_definition
)))

;; Function-Axioms vstd::std_specs::option::is_some
(assert
 (fuel_bool_default fuel%vstd!std_specs.option.is_some.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.option.is_some.)
  (forall ((T&. Dcr) (T& Type) (option! Poly)) (!
    (= (vstd!std_specs.option.is_some.? T&. T& option!) (is-core!option.Option./Some (%Poly%core!option.Option.
       option!
    )))
    :pattern ((vstd!std_specs.option.is_some.? T&. T& option!))
    :qid internal_vstd!std_specs.option.is_some.?_definition
    :skolemid skolem_internal_vstd!std_specs.option.is_some.?_definition
))))

;; Function-Axioms vstd::std_specs::option::is_none
(assert
 (fuel_bool_default fuel%vstd!std_specs.option.is_none.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.option.is_none.)
  (forall ((T&. Dcr) (T& Type) (option! Poly)) (!
    (= (vstd!std_specs.option.is_none.? T&. T& option!) (is-core!option.Option./None (%Poly%core!option.Option.
       option!
    )))
    :pattern ((vstd!std_specs.option.is_none.? T&. T& option!))
    :qid internal_vstd!std_specs.option.is_none.?_definition
    :skolemid skolem_internal_vstd!std_specs.option.is_none.?_definition
))))

;; Function-Axioms vstd::std_specs::option::impl&%0::arrow_0
(assert
 (fuel_bool_default fuel%vstd!std_specs.option.impl&%0.arrow_0.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.option.impl&%0.arrow_0.)
  (forall ((T&. Dcr) (T& Type) (self! Poly)) (!
    (=>
     (sized T&.)
     (= (vstd!std_specs.option.OptionAdditionalFns.arrow_0.? $ (TYPE%core!option.Option.
        T&. T&
       ) T&. T& self!
      ) (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option. self!))
    ))
    :pattern ((vstd!std_specs.option.OptionAdditionalFns.arrow_0.? $ (TYPE%core!option.Option.
       T&. T&
      ) T&. T& self!
    ))
    :qid internal_vstd!std_specs.option.OptionAdditionalFns.arrow_0.?_definition
    :skolemid skolem_internal_vstd!std_specs.option.OptionAdditionalFns.arrow_0.?_definition
))))

;; Function-Axioms vstd::std_specs::option::impl&%0::arrow_Some_0
(assert
 (fuel_bool_default fuel%vstd!std_specs.option.impl&%0.arrow_Some_0.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.option.impl&%0.arrow_Some_0.)
  (forall ((T&. Dcr) (T& Type) (self! Poly)) (!
    (=>
     (sized T&.)
     (= (vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.? $ (TYPE%core!option.Option.
        T&. T&
       ) T&. T& self!
      ) (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option. self!))
    ))
    :pattern ((vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.? $ (TYPE%core!option.Option.
       T&. T&
      ) T&. T& self!
    ))
    :qid internal_vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.?_definition
    :skolemid skolem_internal_vstd!std_specs.option.OptionAdditionalFns.arrow_Some_0.?_definition
))))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%vstd!std_specs.option.OptionAdditionalFns. $ (TYPE%core!option.Option. T&.
      T&
     ) T&. T&
   ))
   :pattern ((tr_bound%vstd!std_specs.option.OptionAdditionalFns. $ (TYPE%core!option.Option.
      T&. T&
     ) T&. T&
   ))
   :qid internal_vstd__std_specs__option__impl&__0_trait_impl_definition
   :skolemid skolem_internal_vstd__std_specs__option__impl&__0_trait_impl_definition
)))

;; Function-Specs vstd::std_specs::option::spec_unwrap
(declare-fun req%vstd!std_specs.option.spec_unwrap. (Dcr Type Poly) Bool)
(declare-const %%global_location_label%%6 Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (option! Poly)) (!
   (= (req%vstd!std_specs.option.spec_unwrap. T&. T& option!) (=>
     %%global_location_label%%6
     (is-core!option.Option./Some (%Poly%core!option.Option. option!))
   ))
   :pattern ((req%vstd!std_specs.option.spec_unwrap. T&. T& option!))
   :qid internal_req__vstd!std_specs.option.spec_unwrap._definition
   :skolemid skolem_internal_req__vstd!std_specs.option.spec_unwrap._definition
)))

;; Function-Axioms vstd::std_specs::option::spec_unwrap
(assert
 (fuel_bool_default fuel%vstd!std_specs.option.spec_unwrap.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.option.spec_unwrap.)
  (forall ((T&. Dcr) (T& Type) (option! Poly)) (!
    (= (vstd!std_specs.option.spec_unwrap.? T&. T& option!) (core!option.Option./Some/0
      T&. T& (%Poly%core!option.Option. option!)
    ))
    :pattern ((vstd!std_specs.option.spec_unwrap.? T&. T& option!))
    :qid internal_vstd!std_specs.option.spec_unwrap.?_definition
    :skolemid skolem_internal_vstd!std_specs.option.spec_unwrap.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (option! Poly)) (!
   (=>
    (has_type option! (TYPE%core!option.Option. T&. T&))
    (has_type (vstd!std_specs.option.spec_unwrap.? T&. T& option!) T&)
   )
   :pattern ((vstd!std_specs.option.spec_unwrap.? T&. T& option!))
   :qid internal_vstd!std_specs.option.spec_unwrap.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.option.spec_unwrap.?_pre_post_definition
)))

;; Function-Specs core::option::impl&%6::clone
(declare-fun ens%core!option.impl&%6.clone. (Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (opt! Poly) (res! Poly)) (!
   (= (ens%core!option.impl&%6.clone. T&. T& opt! res!) (and
     (ens%core!clone.Clone.clone. $ (TYPE%core!option.Option. T&. T&) opt! res!)
     (=>
      (is-core!option.Option./None (%Poly%core!option.Option. opt!))
      (is-core!option.Option./None (%Poly%core!option.Option. res!))
     )
     (=>
      (is-core!option.Option./Some (%Poly%core!option.Option. opt!))
      (and
       (is-core!option.Option./Some (%Poly%core!option.Option. res!))
       (vstd!pervasive.cloned.? T&. T& (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option.
          opt!
         )
        ) (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option. res!))
   )))))
   :pattern ((ens%core!option.impl&%6.clone. T&. T& opt! res!))
   :qid internal_ens__core!option.impl&__6.clone._definition
   :skolemid skolem_internal_ens__core!option.impl&__6.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&)))
     (has_type res$ (TYPE%core!option.Option. T&. T&))
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option. T&. T&)) (
       DST (REF $)
      ) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&)) (F fndef_singleton) closure%$
      res$
     )
     (let
      ((opt$ (%Poly%core!option.Option. (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$)))))
      (and
       (=>
        (is-core!option.Option./None opt$)
        (is-core!option.Option./None (%Poly%core!option.Option. res$))
       )
       (=>
        (is-core!option.Option./Some opt$)
        (and
         (is-core!option.Option./Some (%Poly%core!option.Option. res$))
         (vstd!pervasive.cloned.? T&. T& (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option.
            (Poly%core!option.Option. opt$)
           )
          ) (core!option.Option./Some/0 T&. T& (%Poly%core!option.Option. res$))
   )))))))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option. T&.
       T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&)) (F fndef_singleton)
     closure%$ res$
   ))
   :qid user_core__option__impl&%6__clone_49
   :skolemid skolem_user_core__option__impl&%6__clone_49
)))

;; Function-Specs alloc::boxed::impl&%15::clone
(declare-fun ens%alloc!boxed.impl&%15.clone. (Dcr Type Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (b! Poly) (res! Poly)) (!
   (= (ens%alloc!boxed.impl&%15.clone. T&. T& A&. A& b! res!) (and
     (ens%core!clone.Clone.clone. (BOX A&. A& T&.) T& b! res!)
     (vstd!pervasive.cloned.? T&. T& b! res!)
   ))
   :pattern ((ens%alloc!boxed.impl&%15.clone. T&. T& A&. A& b! res!))
   :qid internal_ens__alloc!boxed.impl&__15.clone._definition
   :skolemid skolem_internal_ens__alloc!boxed.impl&__15.clone._definition
)))
(assert
 (forall ((closure%$ Poly) (res$ Poly) (T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (has_type closure%$ (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&))
     (has_type res$ T&)
    )
    (=>
     (closure_ens (FNDEF%core!clone.Clone.clone. (BOX A&. A& T&.) T&) (DST (REF (BOX A&. A&
         T&.
       ))
      ) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&) (F fndef_singleton) closure%$ res$
     )
     (let
      ((b$ (tuple%1./tuple%1/0 (%Poly%tuple%1. closure%$))))
      (vstd!pervasive.cloned.? T&. T& b$ res$)
   )))
   :pattern ((closure_ens (FNDEF%core!clone.Clone.clone. (BOX A&. A& T&.) T&) (DST (REF
       (BOX A&. A& T&.)
      )
     ) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&) (F fndef_singleton) closure%$ res$
   ))
   :qid user_alloc__boxed__impl&%15__clone_50
   :skolemid skolem_user_alloc__boxed__impl&%15__clone_50
)))

;; Function-Axioms vstd::seq_lib::impl&%0::to_multiset
(assert
 (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
   (=>
    (has_type self! (TYPE%vstd!seq.Seq. A&. A&))
    (has_type (vstd!seq_lib.impl&%0.to_multiset.? A&. A& self!) (TYPE%vstd!multiset.Multiset.
      A&. A&
   )))
   :pattern ((vstd!seq_lib.impl&%0.to_multiset.? A&. A& self!))
   :qid internal_vstd!seq_lib.impl&__0.to_multiset.?_pre_post_definition
   :skolemid skolem_internal_vstd!seq_lib.impl&__0.to_multiset.?_pre_post_definition
)))

;; Broadcast det_harness::axiom_partial_eq_observed_symmetric
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_partial_eq_observed_symmetric.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
      )
      (= (det_harness!partial_eq_observed.? T&. T& left! right!) (det_harness!partial_eq_observed.?
        T&. T& right! left!
    ))))
    :pattern ((det_harness!partial_eq_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_partial_eq_observed_symmetric_51
    :skolemid skolem_user_det_harness__axiom_partial_eq_observed_symmetric_51
))))

;; Broadcast det_harness::axiom_partial_eq_observed_transitive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_partial_eq_observed_transitive.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (middle! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type middle! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
      )
      (=>
       (and
        (det_harness!partial_eq_observed.? T&. T& left! middle!)
        (det_harness!partial_eq_observed.? T&. T& middle! right!)
       )
       (det_harness!partial_eq_observed.? T&. T& left! right!)
    )))
    :pattern ((det_harness!partial_eq_observed.? T&. T& left! middle!) (det_harness!partial_eq_observed.?
      T&. T& middle! right!
    ))
    :qid user_det_harness__axiom_partial_eq_observed_transitive_52
    :skolemid skolem_user_det_harness__axiom_partial_eq_observed_transitive_52
))))

;; Function-Axioms det_harness::slice_pattern_view
(assert
 (forall ((P&. Dcr) (P& Type) (T&. Dcr) (T& Type) (pattern! Poly)) (!
   (=>
    (has_type pattern! P&)
    (has_type (det_harness!slice_pattern_view.? P&. P& T&. T& pattern!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!slice_pattern_view.? P&. P& T&. T& pattern!))
   :qid internal_det_harness!slice_pattern_view.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_pattern_view.?_pre_post_definition
)))

;; Function-Axioms det_harness::zero_arg_fnmut_outputs
(assert
 (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (f! Poly) (len! Poly)) (!
   (=>
    (and
     (has_type f! F&)
     (has_type len! NAT)
    )
    (has_type (det_harness!zero_arg_fnmut_outputs.? F&. F& T&. T& f! len!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!zero_arg_fnmut_outputs.? F&. F& T&. T& f! len!))
   :qid internal_det_harness!zero_arg_fnmut_outputs.?_pre_post_definition
   :skolemid skolem_internal_det_harness!zero_arg_fnmut_outputs.?_pre_post_definition
)))

;; Broadcast det_harness::axiom_zero_arg_fnmut_outputs_len
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_zero_arg_fnmut_outputs_len.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (f! Poly) (len! Poly)) (!
    (=>
     (and
      (has_type f! F&)
      (has_type len! NAT)
     )
     (=>
      (and
       (sized F&.)
       (sized T&.)
      )
      (= (vstd!seq.Seq.len.? T&. T& (det_harness!zero_arg_fnmut_outputs.? F&. F& T&. T& f!
         len!
        )
       ) (%I len!)
    )))
    :pattern ((vstd!seq.Seq.len.? T&. T& (det_harness!zero_arg_fnmut_outputs.? F&. F& T&.
       T& f! len!
    )))
    :qid user_det_harness__axiom_zero_arg_fnmut_outputs_len_53
    :skolemid skolem_user_det_harness__axiom_zero_arg_fnmut_outputs_len_53
))))

;; Broadcast det_harness::axiom_ord_cmp_observed_reflexive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_ord_cmp_observed_reflexive.)
  (forall ((T&. Dcr) (T& Type) (value! Poly)) (!
    (=>
     (has_type value! T&)
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.Ord. T&. T&)
      )
      (= (det_harness!ord_cmp_observed.? T&. T& value! value!) core!cmp.Ordering./Equal)
    ))
    :pattern ((det_harness!ord_cmp_observed.? T&. T& value! value!))
    :qid user_det_harness__axiom_ord_cmp_observed_reflexive_54
    :skolemid skolem_user_det_harness__axiom_ord_cmp_observed_reflexive_54
))))

;; Broadcast det_harness::axiom_ord_cmp_observed_dual
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_ord_cmp_observed_dual.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.Ord. T&. T&)
      )
      (and
       (and
        (= (= (det_harness!ord_cmp_observed.? T&. T& left! right!) core!cmp.Ordering./Less)
         (= (det_harness!ord_cmp_observed.? T&. T& right! left!) core!cmp.Ordering./Greater)
        )
        (= (= (det_harness!ord_cmp_observed.? T&. T& left! right!) core!cmp.Ordering./Equal)
         (= (det_harness!ord_cmp_observed.? T&. T& right! left!) core!cmp.Ordering./Equal)
       ))
       (= (= (det_harness!ord_cmp_observed.? T&. T& left! right!) core!cmp.Ordering./Greater)
        (= (det_harness!ord_cmp_observed.? T&. T& right! left!) core!cmp.Ordering./Less)
    ))))
    :pattern ((det_harness!ord_cmp_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_ord_cmp_observed_dual_55
    :skolemid skolem_user_det_harness__axiom_ord_cmp_observed_dual_55
))))

;; Broadcast det_harness::axiom_ord_cmp_observed_matches_partial_eq
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_ord_cmp_observed_matches_partial_eq.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.Ord. T&. T&)
      )
      (= (= (det_harness!ord_cmp_observed.? T&. T& left! right!) core!cmp.Ordering./Equal)
       (det_harness!partial_eq_observed.? T&. T& left! right!)
    )))
    :pattern ((det_harness!ord_cmp_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_ord_cmp_observed_matches_partial_eq_56
    :skolemid skolem_user_det_harness__axiom_ord_cmp_observed_matches_partial_eq_56
))))

;; Function-Axioms det_harness::ordering_rank
(assert
 (fuel_bool_default fuel%det_harness!ordering_rank.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ordering_rank.)
  (forall ((ordering! Poly)) (!
    (= (det_harness!ordering_rank.? ordering!) (ite
      (is-core!cmp.Ordering./Less (%Poly%core!cmp.Ordering. ordering!))
      (Sub 0 1)
      (ite
       (is-core!cmp.Ordering./Equal (%Poly%core!cmp.Ordering. ordering!))
       0
       1
    )))
    :pattern ((det_harness!ordering_rank.? ordering!))
    :qid internal_det_harness!ordering_rank.?_definition
    :skolemid skolem_internal_det_harness!ordering_rank.?_definition
))))

;; Function-Axioms det_harness::ord_leq_observed
(assert
 (fuel_bool_default fuel%det_harness!ord_leq_observed.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ord_leq_observed.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (= (det_harness!ord_leq_observed.? T&. T& left! right!) (<= (det_harness!ordering_rank.?
       (Poly%core!cmp.Ordering. (det_harness!ord_cmp_observed.? T&. T& left! right!))
      ) 0
    ))
    :pattern ((det_harness!ord_leq_observed.? T&. T& left! right!))
    :qid internal_det_harness!ord_leq_observed.?_definition
    :skolemid skolem_internal_det_harness!ord_leq_observed.?_definition
))))

;; Broadcast det_harness::axiom_ord_leq_observed_total
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_ord_leq_observed_total.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.Ord. T&. T&)
      )
      (or
       (det_harness!ord_leq_observed.? T&. T& left! right!)
       (det_harness!ord_leq_observed.? T&. T& right! left!)
    )))
    :pattern ((det_harness!ord_leq_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_ord_leq_observed_total_57
    :skolemid skolem_user_det_harness__axiom_ord_leq_observed_total_57
))))

;; Broadcast det_harness::axiom_ord_leq_observed_transitive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_ord_leq_observed_transitive.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (middle! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type middle! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.Ord. T&. T&)
      )
      (=>
       (and
        (det_harness!ord_leq_observed.? T&. T& left! middle!)
        (det_harness!ord_leq_observed.? T&. T& middle! right!)
       )
       (det_harness!ord_leq_observed.? T&. T& left! right!)
    )))
    :pattern ((det_harness!ord_leq_observed.? T&. T& left! middle!) (det_harness!ord_leq_observed.?
      T&. T& middle! right!
    ))
    :qid user_det_harness__axiom_ord_leq_observed_transitive_58
    :skolemid skolem_user_det_harness__axiom_ord_leq_observed_transitive_58
))))

;; Broadcast det_harness::axiom_partial_ord_leq_observed_matches_partial_eq
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_partial_ord_leq_observed_matches_partial_eq.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
      )
      (=>
       (det_harness!partial_eq_observed.? T&. T& left! right!)
       (and
        (det_harness!partial_ord_leq_observed.? T&. T& left! right!)
        (det_harness!partial_ord_leq_observed.? T&. T& right! left!)
    ))))
    :pattern ((det_harness!partial_ord_leq_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_partial_ord_leq_observed_matches_partial_eq_59
    :skolemid skolem_user_det_harness__axiom_partial_ord_leq_observed_matches_partial_eq_59
))))

;; Broadcast det_harness::axiom_partial_ord_leq_observed_antisymmetric
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_partial_ord_leq_observed_antisymmetric.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
      )
      (=>
       (and
        (det_harness!partial_ord_leq_observed.? T&. T& left! right!)
        (det_harness!partial_ord_leq_observed.? T&. T& right! left!)
       )
       (det_harness!partial_eq_observed.? T&. T& left! right!)
    )))
    :pattern ((det_harness!partial_ord_leq_observed.? T&. T& left! right!))
    :qid user_det_harness__axiom_partial_ord_leq_observed_antisymmetric_60
    :skolemid skolem_user_det_harness__axiom_partial_ord_leq_observed_antisymmetric_60
))))

;; Broadcast det_harness::axiom_partial_ord_leq_observed_transitive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_partial_ord_leq_observed_transitive.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (middle! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type left! T&)
      (has_type middle! T&)
      (has_type right! T&)
     )
     (=>
      (and
       (sized T&.)
       (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
      )
      (=>
       (and
        (det_harness!partial_ord_leq_observed.? T&. T& left! middle!)
        (det_harness!partial_ord_leq_observed.? T&. T& middle! right!)
       )
       (det_harness!partial_ord_leq_observed.? T&. T& left! right!)
    )))
    :pattern ((det_harness!partial_ord_leq_observed.? T&. T& left! middle!) (det_harness!partial_ord_leq_observed.?
      T&. T& middle! right!
    ))
    :qid user_det_harness__axiom_partial_ord_leq_observed_transitive_61
    :skolemid skolem_user_det_harness__axiom_partial_ord_leq_observed_transitive_61
))))

;; Function-Axioms det_harness::fnmut_adjacent_key_outputs
(assert
 (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (f! Poly) (source!
    Poly
   )
  ) (!
   (=>
    (and
     (has_type f! F&)
     (has_type source! (TYPE%vstd!seq.Seq. T&. T&))
    )
    (has_type (det_harness!fnmut_adjacent_key_outputs.? F&. F& T&. T& K&. K& f! source!)
     (TYPE%vstd!seq.Seq. K&. K&)
   ))
   :pattern ((det_harness!fnmut_adjacent_key_outputs.? F&. F& T&. T& K&. K& f! source!))
   :qid internal_det_harness!fnmut_adjacent_key_outputs.?_pre_post_definition
   :skolemid skolem_internal_det_harness!fnmut_adjacent_key_outputs.?_pre_post_definition
)))

;; Function-Axioms det_harness::fnmut_key_observed
(assert
 (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (B&. Dcr) (B& Type) (f! Poly) (value!
    Poly
   )
  ) (!
   (=>
    (and
     (has_type f! F&)
     (has_type value! T&)
    )
    (has_type (det_harness!fnmut_key_observed.? F&. F& T&. T& B&. B& f! value!) B&)
   )
   :pattern ((det_harness!fnmut_key_observed.? F&. F& T&. T& B&. B& f! value!))
   :qid internal_det_harness!fnmut_key_observed.?_pre_post_definition
   :skolemid skolem_internal_det_harness!fnmut_key_observed.?_pre_post_definition
)))

;; Function-Axioms det_harness::comparator_observation
(assert
 (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (compare! Poly) (domain! Poly)) (
   !
   (=>
    (and
     (has_type compare! F&)
     (has_type domain! (TYPE%vstd!seq.Seq. T&. T&))
    )
    (has_type (Poly%det_harness!ComparatorObservation. (det_harness!comparator_observation.?
       F&. F& T&. T& compare! domain!
      )
     ) (TYPE%det_harness!ComparatorObservation. T&. T&)
   ))
   :pattern ((det_harness!comparator_observation.? F&. F& T&. T& compare! domain!))
   :qid internal_det_harness!comparator_observation.?_pre_post_definition
   :skolemid skolem_internal_det_harness!comparator_observation.?_pre_post_definition
)))

;; Broadcast det_harness::axiom_comparator_observation_domain
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_comparator_observation_domain.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (compare! Poly) (domain! Poly)) (
    !
    (=>
     (and
      (has_type compare! F&)
      (has_type domain! (TYPE%vstd!seq.Seq. T&. T&))
     )
     (=>
      (and
       (sized F&.)
       (sized T&.)
      )
      (= (det_harness!ComparatorObservation./ComparatorObservation/domain (%Poly%det_harness!ComparatorObservation.
         (Poly%det_harness!ComparatorObservation. (det_harness!comparator_observation.? F&.
           F& T&. T& compare! domain!
        )))
       ) domain!
    )))
    :pattern ((det_harness!ComparatorObservation./ComparatorObservation/domain (%Poly%det_harness!ComparatorObservation.
       (Poly%det_harness!ComparatorObservation. (det_harness!comparator_observation.? F&.
         F& T&. T& compare! domain!
    )))))
    :qid user_det_harness__axiom_comparator_observation_domain_62
    :skolemid skolem_user_det_harness__axiom_comparator_observation_domain_62
))))

;; Broadcast det_harness::axiom_comparator_leq_observed_reflexive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_comparator_leq_observed_reflexive.)
  (forall ((T&. Dcr) (T& Type) (observation! Poly) (value! Poly)) (!
    (=>
     (and
      (has_type observation! (TYPE%det_harness!ComparatorObservation. T&. T&))
      (has_type value! T&)
     )
     (=>
      (sized T&.)
      (det_harness!comparator_leq_observed.? T&. T& observation! value! value!)
    ))
    :pattern ((det_harness!comparator_leq_observed.? T&. T& observation! value! value!))
    :qid user_det_harness__axiom_comparator_leq_observed_reflexive_63
    :skolemid skolem_user_det_harness__axiom_comparator_leq_observed_reflexive_63
))))

;; Broadcast det_harness::axiom_comparator_leq_observed_total
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_comparator_leq_observed_total.)
  (forall ((T&. Dcr) (T& Type) (observation! Poly) (left! Poly) (right! Poly)) (!
    (=>
     (and
      (has_type observation! (TYPE%det_harness!ComparatorObservation. T&. T&))
      (has_type left! T&)
      (has_type right! T&)
     )
     (=>
      (sized T&.)
      (or
       (det_harness!comparator_leq_observed.? T&. T& observation! left! right!)
       (det_harness!comparator_leq_observed.? T&. T& observation! right! left!)
    )))
    :pattern ((det_harness!comparator_leq_observed.? T&. T& observation! left! right!))
    :qid user_det_harness__axiom_comparator_leq_observed_total_64
    :skolemid skolem_user_det_harness__axiom_comparator_leq_observed_total_64
))))

;; Broadcast det_harness::axiom_comparator_leq_observed_transitive
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_comparator_leq_observed_transitive.)
  (forall ((T&. Dcr) (T& Type) (observation! Poly) (left! Poly) (middle! Poly) (right!
     Poly
    )
   ) (!
    (=>
     (and
      (has_type observation! (TYPE%det_harness!ComparatorObservation. T&. T&))
      (has_type left! T&)
      (has_type middle! T&)
      (has_type right! T&)
     )
     (=>
      (sized T&.)
      (=>
       (and
        (det_harness!comparator_leq_observed.? T&. T& observation! left! middle!)
        (det_harness!comparator_leq_observed.? T&. T& observation! middle! right!)
       )
       (det_harness!comparator_leq_observed.? T&. T& observation! left! right!)
    )))
    :pattern ((det_harness!comparator_leq_observed.? T&. T& observation! left! middle!)
     (det_harness!comparator_leq_observed.? T&. T& observation! middle! right!)
    )
    :qid user_det_harness__axiom_comparator_leq_observed_transitive_65
    :skolemid skolem_user_det_harness__axiom_comparator_leq_observed_transitive_65
))))

;; Function-Axioms det_harness::slice_iterator_view
(assert
 (forall ((I&. Dcr) (I& Type) (T&. Dcr) (T& Type) (iter! Poly)) (!
   (=>
    (has_type iter! I&)
    (has_type (Poly%det_harness!SliceIteratorView. (det_harness!slice_iterator_view.? I&.
       I& T&. T& iter!
      )
     ) (TYPE%det_harness!SliceIteratorView. T&. T&)
   ))
   :pattern ((det_harness!slice_iterator_view.? I&. I& T&. T& iter!))
   :qid internal_det_harness!slice_iterator_view.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_iterator_view.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_iterator_well_formed
(assert
 (fuel_bool_default fuel%det_harness!slice_iterator_well_formed.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_iterator_well_formed.)
  (forall ((T&. Dcr) (T& Type) (view! Poly)) (!
    (= (det_harness!slice_iterator_well_formed.? T&. T& view!) (and
      (<= 0 (det_harness!SliceIteratorView./SliceIteratorView/chunk_size (%Poly%det_harness!SliceIteratorView.
         view!
      )))
      (<= (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/remainder
         (%Poly%det_harness!SliceIteratorView. view!)
        )
       ) (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/source
         (%Poly%det_harness!SliceIteratorView. view!)
    )))))
    :pattern ((det_harness!slice_iterator_well_formed.? T&. T& view!))
    :qid internal_det_harness!slice_iterator_well_formed.?_definition
    :skolemid skolem_internal_det_harness!slice_iterator_well_formed.?_definition
))))

;; Broadcast det_harness::axiom_slice_iterator_view_well_formed
(assert
 (=>
  (fuel_bool fuel%det_harness!axiom_slice_iterator_view_well_formed.)
  (forall ((I&. Dcr) (I& Type) (T&. Dcr) (T& Type) (iter! Poly)) (!
    (=>
     (has_type iter! I&)
     (=>
      (and
       (sized I&.)
       (sized T&.)
      )
      (det_harness!slice_iterator_well_formed.? T&. T& (Poly%det_harness!SliceIteratorView.
        (det_harness!slice_iterator_view.? I&. I& T&. T& iter!)
    ))))
    :pattern ((det_harness!slice_iterator_view.? I&. I& T&. T& iter!))
    :qid user_det_harness__axiom_slice_iterator_view_well_formed_66
    :skolemid skolem_user_det_harness__axiom_slice_iterator_view_well_formed_66
))))

;; Function-Axioms det_harness::maybe_uninit_storage_relation
(assert
 (forall ((T&. Dcr) (T& Type) (storage! Poly)) (!
   (=>
    (has_type storage! (SLICE $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&. T&)))
    (has_type (Poly%det_harness!MaybeUninitSliceRelation. (det_harness!maybe_uninit_storage_relation.?
       T&. T& storage!
      )
     ) (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&)
   ))
   :pattern ((det_harness!maybe_uninit_storage_relation.? T&. T& storage!))
   :qid internal_det_harness!maybe_uninit_storage_relation.?_pre_post_definition
   :skolemid skolem_internal_det_harness!maybe_uninit_storage_relation.?_pre_post_definition
)))

;; Function-Axioms det_harness::maybe_uninit_seq_relation
(assert
 (forall ((T&. Dcr) (T& Type) (storage! Poly)) (!
   (=>
    (has_type storage! (TYPE%vstd!seq.Seq. $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&.
       T&
    )))
    (has_type (Poly%det_harness!MaybeUninitSliceRelation. (det_harness!maybe_uninit_seq_relation.?
       T&. T& storage!
      )
     ) (TYPE%det_harness!MaybeUninitSliceRelation. T&. T&)
   ))
   :pattern ((det_harness!maybe_uninit_seq_relation.? T&. T& storage!))
   :qid internal_det_harness!maybe_uninit_seq_relation.?_pre_post_definition
   :skolemid skolem_internal_det_harness!maybe_uninit_seq_relation.?_pre_post_definition
)))

;; Function-Axioms det_harness::maybe_uninit_from_initialized
(assert
 (forall ((T&. Dcr) (T& Type) (values! Poly)) (!
   (=>
    (has_type values! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (det_harness!maybe_uninit_from_initialized.? T&. T& values!) (TYPE%vstd!seq.Seq.
      $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&. T&)
   )))
   :pattern ((det_harness!maybe_uninit_from_initialized.? T&. T& values!))
   :qid internal_det_harness!maybe_uninit_from_initialized.?_pre_post_definition
   :skolemid skolem_internal_det_harness!maybe_uninit_from_initialized.?_pre_post_definition
)))

;; Function-Axioms vstd::raw_ptr::impl&%3::view
(assert
 (fuel_bool_default fuel%vstd!raw_ptr.impl&%3.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!raw_ptr.impl&%3.view.)
  (forall ((T&. Dcr) (T& Type) (self! Poly)) (!
    (= (vstd!view.View.view.? (CONST_PTR $) (PTR T&. T&) self!) (vstd!view.View.view.?
      $ (PTR T&. T&) self!
    ))
    :pattern ((vstd!view.View.view.? (CONST_PTR $) (PTR T&. T&) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%0::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%0.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%0.view.)
  (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
    (=>
     (tr_bound%vstd!view.View. A&. A&)
     (= (vstd!view.View.view.? (REF A&.) A& self!) (vstd!view.View.view.? A&. A& self!))
    )
    :pattern ((vstd!view.View.view.? (REF A&.) A& self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%2::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%2.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%2.view.)
  (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
    (=>
     (tr_bound%vstd!view.View. A&. A&)
     (= (vstd!view.View.view.? (BOX $ TYPE%alloc!alloc.Global. A&.) A& self!) (vstd!view.View.view.?
       A&. A& self!
    )))
    :pattern ((vstd!view.View.view.? (BOX $ TYPE%alloc!alloc.Global. A&.) A& self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%4::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%4.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%4.view.)
  (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
    (=>
     (and
      (sized A&.)
      (tr_bound%vstd!view.View. A&. A&)
     )
     (= (vstd!view.View.view.? (RC $ TYPE%alloc!alloc.Global. A&.) A& self!) (vstd!view.View.view.?
       A&. A& self!
    )))
    :pattern ((vstd!view.View.view.? (RC $ TYPE%alloc!alloc.Global. A&.) A& self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%6::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%6.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%6.view.)
  (forall ((A&. Dcr) (A& Type) (self! Poly)) (!
    (=>
     (and
      (sized A&.)
      (tr_bound%vstd!view.View. A&. A&)
     )
     (= (vstd!view.View.view.? (ARC $ TYPE%alloc!alloc.Global. A&.) A& self!) (vstd!view.View.view.?
       A&. A& self!
    )))
    :pattern ((vstd!view.View.view.? (ARC $ TYPE%alloc!alloc.Global. A&.) A& self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%14::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%14.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%14.view.)
  (forall ((T&. Dcr) (T& Type) (self! Poly)) (!
    (=>
     (sized T&.)
     (= (vstd!view.View.view.? $ (TYPE%core!option.Option. T&. T&) self!) self!)
    )
    :pattern ((vstd!view.View.view.? $ (TYPE%core!option.Option. T&. T&) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%16::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%16.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%16.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ TYPE%tuple%0. self!) self!)
    :pattern ((vstd!view.View.view.? $ TYPE%tuple%0. self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%18::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%18.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%18.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ BOOL self!) self!)
    :pattern ((vstd!view.View.view.? $ BOOL self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%20::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%20.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%20.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (UINT 8) self!) self!)
    :pattern ((vstd!view.View.view.? $ (UINT 8) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%30::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%30.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%30.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ USIZE self!) self!)
    :pattern ((vstd!view.View.view.? $ USIZE self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%44::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%44.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%44.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ CHAR self!) self!)
    :pattern ((vstd!view.View.view.? $ CHAR self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%46::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%46.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%46.view.)
  (forall ((A0&. Dcr) (A0& Type) (self! Poly)) (!
    (=>
     (and
      (sized A0&.)
      (tr_bound%vstd!view.View. A0&. A0&)
     )
     (= (vstd!view.View.view.? (DST A0&.) (TYPE%tuple%1. A0&. A0&) self!) (Poly%tuple%1.
       (tuple%1./tuple%1 (vstd!view.View.view.? A0&. A0& (tuple%1./tuple%1/0 (%Poly%tuple%1.
           self!
    )))))))
    :pattern ((vstd!view.View.view.? (DST A0&.) (TYPE%tuple%1. A0&. A0&) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%48::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%48.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%48.view.)
  (forall ((A0&. Dcr) (A0& Type) (A1&. Dcr) (A1& Type) (self! Poly)) (!
    (=>
     (and
      (sized A0&.)
      (sized A1&.)
      (tr_bound%vstd!view.View. A0&. A0&)
      (tr_bound%vstd!view.View. A1&. A1&)
     )
     (= (vstd!view.View.view.? (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&) self!) (Poly%tuple%2.
       (tuple%2./tuple%2 (vstd!view.View.view.? A0&. A0& (tuple%2./tuple%2/0 (%Poly%tuple%2.
           self!
         ))
        ) (vstd!view.View.view.? A1&. A1& (tuple%2./tuple%2/1 (%Poly%tuple%2. self!)))
    ))))
    :pattern ((vstd!view.View.view.? (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&) self!))
    :qid internal_vstd!view.View.view.?_definition
    :skolemid skolem_internal_vstd!view.View.view.?_definition
))))

;; Function-Axioms det_harness::slice_seq
(assert
 (fuel_bool_default fuel%det_harness!slice_seq.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_seq.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
    (= (det_harness!slice_seq.? T&. T& slice!) (vstd!view.View.view.? $slice (SLICE T&.
       T&
      ) slice!
    ))
    :pattern ((det_harness!slice_seq.? T&. T& slice!))
    :qid internal_det_harness!slice_seq.?_definition
    :skolemid skolem_internal_det_harness!slice_seq.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
   (=>
    (has_type slice! (SLICE T&. T&))
    (has_type (det_harness!slice_seq.? T&. T& slice!) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((det_harness!slice_seq.? T&. T& slice!))
   :qid internal_det_harness!slice_seq.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_seq.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_len
(assert
 (fuel_bool_default fuel%det_harness!slice_len.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_len.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
    (= (det_harness!slice_len.? T&. T& slice!) (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.?
       $slice (SLICE T&. T&) slice!
    )))
    :pattern ((det_harness!slice_len.? T&. T& slice!))
    :qid internal_det_harness!slice_len.?_definition
    :skolemid skolem_internal_det_harness!slice_len.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (slice! Poly)) (!
   (=>
    (has_type slice! (SLICE T&. T&))
    (<= 0 (det_harness!slice_len.? T&. T& slice!))
   )
   :pattern ((det_harness!slice_len.? T&. T& slice!))
   :qid internal_det_harness!slice_len.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_len.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_subrange
(assert
 (fuel_bool_default fuel%det_harness!slice_subrange.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_subrange.)
  (forall ((T&. Dcr) (T& Type) (slice! Poly) (lo! Poly) (hi! Poly)) (!
    (= (det_harness!slice_subrange.? T&. T& slice! lo! hi!) (vstd!seq.Seq.subrange.? T&.
      T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!) lo! hi!
    ))
    :pattern ((det_harness!slice_subrange.? T&. T& slice! lo! hi!))
    :qid internal_det_harness!slice_subrange.?_definition
    :skolemid skolem_internal_det_harness!slice_subrange.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (slice! Poly) (lo! Poly) (hi! Poly)) (!
   (=>
    (and
     (has_type slice! (SLICE T&. T&))
     (has_type lo! INT)
     (has_type hi! INT)
    )
    (has_type (det_harness!slice_subrange.? T&. T& slice! lo! hi!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!slice_subrange.? T&. T& slice! lo! hi!))
   :qid internal_det_harness!slice_subrange.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_subrange.?_pre_post_definition
)))

;; Function-Axioms det_harness::seq_subrange
(assert
 (fuel_bool_default fuel%det_harness!seq_subrange.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!seq_subrange.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (lo! Poly) (hi! Poly)) (!
    (= (det_harness!seq_subrange.? T&. T& seq! lo! hi!) (vstd!seq.Seq.subrange.? T&. T&
      seq! lo! hi!
    ))
    :pattern ((det_harness!seq_subrange.? T&. T& seq! lo! hi!))
    :qid internal_det_harness!seq_subrange.?_definition
    :skolemid skolem_internal_det_harness!seq_subrange.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (lo! Poly) (hi! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type lo! INT)
     (has_type hi! INT)
    )
    (has_type (det_harness!seq_subrange.? T&. T& seq! lo! hi!) (TYPE%vstd!seq.Seq. T&.
      T&
   )))
   :pattern ((det_harness!seq_subrange.? T&. T& seq! lo! hi!))
   :qid internal_det_harness!seq_subrange.?_pre_post_definition
   :skolemid skolem_internal_det_harness!seq_subrange.?_pre_post_definition
)))

;; Function-Axioms det_harness::seq_update
(assert
 (fuel_bool_default fuel%det_harness!seq_update.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!seq_update.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (index! Poly) (value! Poly)) (!
    (= (det_harness!seq_update.? T&. T& seq! index! value!) (vstd!seq.Seq.update.? T&.
      T& seq! index! value!
    ))
    :pattern ((det_harness!seq_update.? T&. T& seq! index! value!))
    :qid internal_det_harness!seq_update.?_definition
    :skolemid skolem_internal_det_harness!seq_update.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (index! Poly) (value! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type index! INT)
     (has_type value! T&)
    )
    (has_type (det_harness!seq_update.? T&. T& seq! index! value!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!seq_update.? T&. T& seq! index! value!))
   :qid internal_det_harness!seq_update.?_pre_post_definition
   :skolemid skolem_internal_det_harness!seq_update.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_contains_value
(assert
 (fuel_bool_default fuel%det_harness!slice_contains_value.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_contains_value.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly)) (!
    (= (det_harness!slice_contains_value.? T&. T& seq! value!) (exists ((i$ Poly)) (!
       (and
        (has_type i$ INT)
        (and
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& seq!)))
            (and
             (<= tmp%%$ tmp%%$1)
             (< tmp%%$1 tmp%%$2)
         ))))
         (det_harness!partial_eq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! i$) value!)
       ))
       :pattern ((vstd!seq.Seq.index.? T&. T& seq! i$))
       :qid user_det_harness__slice_contains_value_67
       :skolemid skolem_user_det_harness__slice_contains_value_67
    )))
    :pattern ((det_harness!slice_contains_value.? T&. T& seq! value!))
    :qid internal_det_harness!slice_contains_value.?_definition
    :skolemid skolem_internal_det_harness!slice_contains_value.?_definition
))))

;; Function-Axioms det_harness::slice_is_prefix
(assert
 (fuel_bool_default fuel%det_harness!slice_is_prefix.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_is_prefix.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (prefix! Poly)) (!
    (= (det_harness!slice_is_prefix.? T&. T& seq! prefix!) (and
      (<= (vstd!seq.Seq.len.? T&. T& prefix!) (vstd!seq.Seq.len.? T&. T& seq!))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& prefix!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (det_harness!partial_eq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! i$) (vstd!seq.Seq.index.?
            T&. T& prefix! i$
        ))))
        :pattern ((vstd!seq.Seq.index.? T&. T& seq! i$))
        :pattern ((vstd!seq.Seq.index.? T&. T& prefix! i$))
        :qid user_det_harness__slice_is_prefix_68
        :skolemid skolem_user_det_harness__slice_is_prefix_68
    ))))
    :pattern ((det_harness!slice_is_prefix.? T&. T& seq! prefix!))
    :qid internal_det_harness!slice_is_prefix.?_definition
    :skolemid skolem_internal_det_harness!slice_is_prefix.?_definition
))))

;; Function-Axioms det_harness::slice_is_suffix
(assert
 (fuel_bool_default fuel%det_harness!slice_is_suffix.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_is_suffix.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (suffix! Poly)) (!
    (= (det_harness!slice_is_suffix.? T&. T& seq! suffix!) (and
      (<= (vstd!seq.Seq.len.? T&. T& suffix!) (vstd!seq.Seq.len.? T&. T& seq!))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& suffix!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (det_harness!partial_eq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! (I (Add (
               Sub (vstd!seq.Seq.len.? T&. T& seq!) (vstd!seq.Seq.len.? T&. T& suffix!)
              ) (%I i$)
            ))
           ) (vstd!seq.Seq.index.? T&. T& suffix! i$)
        )))
        :pattern ((vstd!seq.Seq.index.? T&. T& suffix! i$))
        :qid user_det_harness__slice_is_suffix_69
        :skolemid skolem_user_det_harness__slice_is_suffix_69
    ))))
    :pattern ((det_harness!slice_is_suffix.? T&. T& seq! suffix!))
    :qid internal_det_harness!slice_is_suffix.?_definition
    :skolemid skolem_internal_det_harness!slice_is_suffix.?_definition
))))

;; Function-Axioms det_harness::slice_strip_prefix_result
(assert
 (fuel_bool_default fuel%det_harness!slice_strip_prefix_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_strip_prefix_result.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (prefix! Poly) (ret! Poly)) (!
    (= (det_harness!slice_strip_prefix_result.? T&. T& seq! prefix! ret!) (ite
      (det_harness!slice_is_prefix.? T&. T& seq! prefix!)
      (and
       (is-core!option.Option./Some (%Poly%core!option.Option. ret!))
       (= (vstd!view.View.view.? $slice (SLICE T&. T&) (core!option.Option./Some/0 (REF $slice)
          (SLICE T&. T&) (%Poly%core!option.Option. ret!)
         )
        ) (vstd!seq.Seq.subrange.? T&. T& seq! (I (vstd!seq.Seq.len.? T&. T& prefix!)) (I (
           vstd!seq.Seq.len.? T&. T& seq!
      )))))
      (is-core!option.Option./None (%Poly%core!option.Option. ret!))
    ))
    :pattern ((det_harness!slice_strip_prefix_result.? T&. T& seq! prefix! ret!))
    :qid internal_det_harness!slice_strip_prefix_result.?_definition
    :skolemid skolem_internal_det_harness!slice_strip_prefix_result.?_definition
))))

;; Function-Axioms det_harness::slice_strip_suffix_result
(assert
 (fuel_bool_default fuel%det_harness!slice_strip_suffix_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_strip_suffix_result.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (suffix! Poly) (ret! Poly)) (!
    (= (det_harness!slice_strip_suffix_result.? T&. T& seq! suffix! ret!) (ite
      (det_harness!slice_is_suffix.? T&. T& seq! suffix!)
      (and
       (is-core!option.Option./Some (%Poly%core!option.Option. ret!))
       (= (vstd!view.View.view.? $slice (SLICE T&. T&) (core!option.Option./Some/0 (REF $slice)
          (SLICE T&. T&) (%Poly%core!option.Option. ret!)
         )
        ) (vstd!seq.Seq.subrange.? T&. T& seq! (I 0) (I (Sub (vstd!seq.Seq.len.? T&. T& seq!)
           (vstd!seq.Seq.len.? T&. T& suffix!)
      )))))
      (is-core!option.Option./None (%Poly%core!option.Option. ret!))
    ))
    :pattern ((det_harness!slice_strip_suffix_result.? T&. T& seq! suffix! ret!))
    :qid internal_det_harness!slice_strip_suffix_result.?_definition
    :skolemid skolem_internal_det_harness!slice_strip_suffix_result.?_definition
))))

;; Function-Axioms det_harness::slice_strip_circumfix_result
(assert
 (fuel_bool_default fuel%det_harness!slice_strip_circumfix_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_strip_circumfix_result.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (prefix! Poly) (suffix! Poly) (ret! Poly))
   (!
    (= (det_harness!slice_strip_circumfix_result.? T&. T& seq! prefix! suffix! ret!) (
      ite
      (and
       (det_harness!slice_is_prefix.? T&. T& seq! prefix!)
       (det_harness!slice_is_suffix.? T&. T& (vstd!seq.Seq.subrange.? T&. T& seq! (I (vstd!seq.Seq.len.?
           T&. T& prefix!
          )
         ) (I (vstd!seq.Seq.len.? T&. T& seq!))
        ) suffix!
      ))
      (and
       (is-core!option.Option./Some (%Poly%core!option.Option. ret!))
       (= (vstd!view.View.view.? $slice (SLICE T&. T&) (core!option.Option./Some/0 (REF $slice)
          (SLICE T&. T&) (%Poly%core!option.Option. ret!)
         )
        ) (vstd!seq.Seq.subrange.? T&. T& seq! (I (vstd!seq.Seq.len.? T&. T& prefix!)) (I (
           Sub (vstd!seq.Seq.len.? T&. T& seq!) (vstd!seq.Seq.len.? T&. T& suffix!)
      )))))
      (is-core!option.Option./None (%Poly%core!option.Option. ret!))
    ))
    :pattern ((det_harness!slice_strip_circumfix_result.? T&. T& seq! prefix! suffix! ret!))
    :qid internal_det_harness!slice_strip_circumfix_result.?_definition
    :skolemid skolem_internal_det_harness!slice_strip_circumfix_result.?_definition
))))

;; Function-Axioms det_harness::slice_filled
(assert
 (fuel_bool_default fuel%det_harness!slice_filled.)
)
(declare-fun %%lambda%%1 (Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Poly) (i$ Poly)) (!
   (= (%%apply%%0 (%%lambda%%1 %%hole%%0) i$) %%hole%%0)
   :pattern ((%%apply%%0 (%%lambda%%1 %%hole%%0) i$))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_filled.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly)) (!
    (= (det_harness!slice_filled.? T&. T& seq! value!) (vstd!seq.Seq.new.? T&. T& (I (vstd!seq.Seq.len.?
        T&. T& seq!
       )
      ) (Poly%fun%1. (mk_fun (%%lambda%%1 value!)))
    ))
    :pattern ((det_harness!slice_filled.? T&. T& seq! value!))
    :qid internal_det_harness!slice_filled.?_definition
    :skolemid skolem_internal_det_harness!slice_filled.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type value! T&)
    )
    (has_type (det_harness!slice_filled.? T&. T& seq! value!) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((det_harness!slice_filled.? T&. T& seq! value!))
   :qid internal_det_harness!slice_filled.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_filled.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_cloned_from
(assert
 (fuel_bool_default fuel%det_harness!slice_cloned_from.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_cloned_from.)
  (forall ((T&. Dcr) (T& Type) (source! Poly) (dest! Poly)) (!
    (= (det_harness!slice_cloned_from.? T&. T& source! dest!) (and
      (= (vstd!seq.Seq.len.? T&. T& dest!) (vstd!seq.Seq.len.? T&. T& source!))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& source!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (vstd!pervasive.cloned.? T&. T& (vstd!seq.Seq.index.? T&. T& source! i$) (vstd!seq.Seq.index.?
            T&. T& dest! i$
        ))))
        :pattern ((vstd!seq.Seq.index.? T&. T& source! i$))
        :pattern ((vstd!seq.Seq.index.? T&. T& dest! i$))
        :qid user_det_harness__slice_cloned_from_70
        :skolemid skolem_user_det_harness__slice_cloned_from_70
    ))))
    :pattern ((det_harness!slice_cloned_from.? T&. T& source! dest!))
    :qid internal_det_harness!slice_cloned_from.?_definition
    :skolemid skolem_internal_det_harness!slice_cloned_from.?_definition
))))

;; Function-Axioms det_harness::slice_filled_with_clone
(assert
 (fuel_bool_default fuel%det_harness!slice_filled_with_clone.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_filled_with_clone.)
  (forall ((T&. Dcr) (T& Type) (old_seq! Poly) (value! Poly) (dest! Poly)) (!
    (= (det_harness!slice_filled_with_clone.? T&. T& old_seq! value! dest!) (and
      (= (vstd!seq.Seq.len.? T&. T& dest!) (vstd!seq.Seq.len.? T&. T& old_seq!))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& dest!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (vstd!pervasive.cloned.? T&. T& value! (vstd!seq.Seq.index.? T&. T& dest! i$))
        ))
        :pattern ((vstd!seq.Seq.index.? T&. T& dest! i$))
        :qid user_det_harness__slice_filled_with_clone_71
        :skolemid skolem_user_det_harness__slice_filled_with_clone_71
    ))))
    :pattern ((det_harness!slice_filled_with_clone.? T&. T& old_seq! value! dest!))
    :qid internal_det_harness!slice_filled_with_clone.?_definition
    :skolemid skolem_internal_det_harness!slice_filled_with_clone.?_definition
))))

;; Function-Axioms det_harness::slice_reversed
(assert
 (fuel_bool_default fuel%det_harness!slice_reversed.)
)
(declare-fun %%lambda%%2 (Int Dcr Type Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Int) (%%hole%%1 Dcr) (%%hole%%2 Type) (%%hole%%3 Poly) (i$ Poly))
  (!
   (= (%%apply%%0 (%%lambda%%2 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3) i$) (vstd!seq.Seq.index.?
     %%hole%%1 %%hole%%2 %%hole%%3 (I (Sub %%hole%%0 (%I i$)))
   ))
   :pattern ((%%apply%%0 (%%lambda%%2 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3) i$))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_reversed.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
    (= (det_harness!slice_reversed.? T&. T& seq!) (vstd!seq.Seq.new.? T&. T& (I (vstd!seq.Seq.len.?
        T&. T& seq!
       )
      ) (Poly%fun%1. (mk_fun (%%lambda%%2 (Sub (vstd!seq.Seq.len.? T&. T& seq!) 1) T&. T&
         seq!
    )))))
    :pattern ((det_harness!slice_reversed.? T&. T& seq!))
    :qid internal_det_harness!slice_reversed.?_definition
    :skolemid skolem_internal_det_harness!slice_reversed.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
   (=>
    (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (det_harness!slice_reversed.? T&. T& seq!) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((det_harness!slice_reversed.? T&. T& seq!))
   :qid internal_det_harness!slice_reversed.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_reversed.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_rotated_left
(assert
 (fuel_bool_default fuel%det_harness!slice_rotated_left.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_rotated_left.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (mid! Poly)) (!
    (= (det_harness!slice_rotated_left.? T&. T& seq! mid!) (vstd!seq.Seq.add.? T&. T& (
       vstd!seq.Seq.subrange.? T&. T& seq! mid! (I (vstd!seq.Seq.len.? T&. T& seq!))
      ) (vstd!seq.Seq.subrange.? T&. T& seq! (I 0) mid!)
    ))
    :pattern ((det_harness!slice_rotated_left.? T&. T& seq! mid!))
    :qid internal_det_harness!slice_rotated_left.?_definition
    :skolemid skolem_internal_det_harness!slice_rotated_left.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (mid! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type mid! INT)
    )
    (has_type (det_harness!slice_rotated_left.? T&. T& seq! mid!) (TYPE%vstd!seq.Seq. T&.
      T&
   )))
   :pattern ((det_harness!slice_rotated_left.? T&. T& seq! mid!))
   :qid internal_det_harness!slice_rotated_left.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_rotated_left.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_rotated_right
(assert
 (fuel_bool_default fuel%det_harness!slice_rotated_right.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_rotated_right.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (k! Poly)) (!
    (= (det_harness!slice_rotated_right.? T&. T& seq! k!) (let
      ((split$ (Sub (vstd!seq.Seq.len.? T&. T& seq!) (%I k!))))
      (vstd!seq.Seq.add.? T&. T& (vstd!seq.Seq.subrange.? T&. T& seq! (I split$) (I (vstd!seq.Seq.len.?
          T&. T& seq!
        ))
       ) (vstd!seq.Seq.subrange.? T&. T& seq! (I 0) (I split$))
    )))
    :pattern ((det_harness!slice_rotated_right.? T&. T& seq! k!))
    :qid internal_det_harness!slice_rotated_right.?_definition
    :skolemid skolem_internal_det_harness!slice_rotated_right.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (k! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type k! INT)
    )
    (has_type (det_harness!slice_rotated_right.? T&. T& seq! k!) (TYPE%vstd!seq.Seq. T&.
      T&
   )))
   :pattern ((det_harness!slice_rotated_right.? T&. T& seq! k!))
   :qid internal_det_harness!slice_rotated_right.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_rotated_right.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_swapped
(assert
 (fuel_bool_default fuel%det_harness!slice_swapped.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_swapped.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (a! Poly) (b! Poly)) (!
    (= (det_harness!slice_swapped.? T&. T& seq! a! b!) (vstd!seq.Seq.update.? T&. T& (vstd!seq.Seq.update.?
       T&. T& seq! a! (vstd!seq.Seq.index.? T&. T& seq! b!)
      ) b! (vstd!seq.Seq.index.? T&. T& seq! a!)
    ))
    :pattern ((det_harness!slice_swapped.? T&. T& seq! a! b!))
    :qid internal_det_harness!slice_swapped.?_definition
    :skolemid skolem_internal_det_harness!slice_swapped.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (a! Poly) (b! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type a! INT)
     (has_type b! INT)
    )
    (has_type (det_harness!slice_swapped.? T&. T& seq! a! b!) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((det_harness!slice_swapped.? T&. T& seq! a! b!))
   :qid internal_det_harness!slice_swapped.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_swapped.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_multiplicity
(assert
 (fuel_bool_default fuel%det_harness!slice_multiplicity.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_multiplicity.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly)) (!
    (= (det_harness!slice_multiplicity.? T&. T& seq! value!) (vstd!multiset.impl&%0.count.?
      T&. T& (vstd!seq_lib.impl&%0.to_multiset.? T&. T& seq!) value!
    ))
    :pattern ((det_harness!slice_multiplicity.? T&. T& seq! value!))
    :qid internal_det_harness!slice_multiplicity.?_definition
    :skolemid skolem_internal_det_harness!slice_multiplicity.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly)) (!
   (=>
    (and
     (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
     (has_type value! T&)
    )
    (<= 0 (det_harness!slice_multiplicity.? T&. T& seq! value!))
   )
   :pattern ((det_harness!slice_multiplicity.? T&. T& seq! value!))
   :qid internal_det_harness!slice_multiplicity.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_multiplicity.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_permutation
(assert
 (fuel_bool_default fuel%det_harness!slice_permutation.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_permutation.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (right! Poly)) (!
    (= (det_harness!slice_permutation.? T&. T& left! right!) (and
      (= (vstd!seq.Seq.len.? T&. T& left!) (vstd!seq.Seq.len.? T&. T& right!))
      (forall ((value$ Poly)) (!
        (=>
         (has_type value$ T&)
         (= (det_harness!slice_multiplicity.? T&. T& left! value$) (det_harness!slice_multiplicity.?
           T&. T& right! value$
        )))
        :pattern ((det_harness!slice_multiplicity.? T&. T& left! value$))
        :pattern ((det_harness!slice_multiplicity.? T&. T& right! value$))
        :qid user_det_harness__slice_permutation_72
        :skolemid skolem_user_det_harness__slice_permutation_72
    ))))
    :pattern ((det_harness!slice_permutation.? T&. T& left! right!))
    :qid internal_det_harness!slice_permutation.?_definition
    :skolemid skolem_internal_det_harness!slice_permutation.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_ord
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_ord.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_ord.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
    (= (det_harness!slice_sorted_by_ord.? T&. T& seq!) (forall ((i$ Poly) (j$ Poly)) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (det_harness!ord_leq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! i$) (vstd!seq.Seq.index.?
           T&. T& seq! j$
       ))))
       :pattern ((det_harness!ord_leq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! i$)
         (vstd!seq.Seq.index.? T&. T& seq! j$)
       ))
       :qid user_det_harness__slice_sorted_by_ord_73
       :skolemid skolem_user_det_harness__slice_sorted_by_ord_73
    )))
    :pattern ((det_harness!slice_sorted_by_ord.? T&. T& seq!))
    :qid internal_det_harness!slice_sorted_by_ord.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_ord.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_partial_ord
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_partial_ord.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_partial_ord.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
    (= (det_harness!slice_sorted_by_partial_ord.? T&. T& seq!) (forall ((i$ Poly) (j$ Poly))
      (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (det_harness!partial_ord_leq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! i$)
          (vstd!seq.Seq.index.? T&. T& seq! j$)
       )))
       :pattern ((det_harness!partial_ord_leq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T&
          seq! i$
         ) (vstd!seq.Seq.index.? T&. T& seq! j$)
       ))
       :qid user_det_harness__slice_sorted_by_partial_ord_74
       :skolemid skolem_user_det_harness__slice_sorted_by_partial_ord_74
    )))
    :pattern ((det_harness!slice_sorted_by_partial_ord.? T&. T& seq!))
    :qid internal_det_harness!slice_sorted_by_partial_ord.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_partial_ord.?_definition
))))

;; Function-Axioms det_harness::slice_adjacent_pair_count
(assert
 (fuel_bool_default fuel%det_harness!slice_adjacent_pair_count.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_adjacent_pair_count.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
    (= (det_harness!slice_adjacent_pair_count.? T&. T& seq!) (ite
      (= (vstd!seq.Seq.len.? T&. T& seq!) 0)
      0
      (nClip (Sub (vstd!seq.Seq.len.? T&. T& seq!) 1))
    ))
    :pattern ((det_harness!slice_adjacent_pair_count.? T&. T& seq!))
    :qid internal_det_harness!slice_adjacent_pair_count.?_definition
    :skolemid skolem_internal_det_harness!slice_adjacent_pair_count.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (seq! Poly)) (!
   (=>
    (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
    (<= 0 (det_harness!slice_adjacent_pair_count.? T&. T& seq!))
   )
   :pattern ((det_harness!slice_adjacent_pair_count.? T&. T& seq!))
   :qid internal_det_harness!slice_adjacent_pair_count.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_adjacent_pair_count.?_pre_post_definition
)))

;; Function-Axioms det_harness::fnmut_adjacent_bool_trace_valid
(assert
 (fuel_bool_default fuel%det_harness!fnmut_adjacent_bool_trace_valid.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!fnmut_adjacent_bool_trace_valid.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (compare! Poly)) (!
    (= (det_harness!fnmut_adjacent_bool_trace_valid.? F&. F& T&. T& seq! compare!) (let
      ((outputs$ (det_harness!fnmut_adjacent_bool_outputs.? F&. F& T&. T& compare! seq!)))
      (let
       ((pair_count$ (det_harness!slice_adjacent_pair_count.? T&. T& seq!)))
       (and
        (and
         (and
          (and
           (<= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) pair_count$)
           (=>
            (= pair_count$ 0)
            (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) 0)
          ))
          (=>
           (< (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) pair_count$)
           (> (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) 0)
         ))
         (=>
          (< (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) pair_count$)
          (not (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$) (I (Sub (vstd!seq.Seq.len.?
                $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)
               ) 1
        )))))))
        (forall ((i$ Poly)) (!
          (=>
           (has_type i$ INT)
           (=>
            (and
             (<= 0 (%I i$))
             (< (Add (%I i$) 2) (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)))
            )
            (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$) i$))
          ))
          :pattern ((vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$) i$))
          :qid user_det_harness__fnmut_adjacent_bool_trace_valid_75
          :skolemid skolem_user_det_harness__fnmut_adjacent_bool_trace_valid_75
    ))))))
    :pattern ((det_harness!fnmut_adjacent_bool_trace_valid.? F&. F& T&. T& seq! compare!))
    :qid internal_det_harness!fnmut_adjacent_bool_trace_valid.?_definition
    :skolemid skolem_internal_det_harness!fnmut_adjacent_bool_trace_valid.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_bool_compare
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_bool_compare.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_bool_compare.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (compare! Poly)) (!
    (= (det_harness!slice_sorted_by_bool_compare.? F&. F& T&. T& seq! compare!) (let
      ((outputs$ (det_harness!fnmut_adjacent_bool_outputs.? F&. F& T&. T& compare! seq!)))
      (and
       (and
        (det_harness!fnmut_adjacent_bool_trace_valid.? F&. F& T&. T& seq! compare!)
        (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$)) (det_harness!slice_adjacent_pair_count.?
          T&. T& seq!
       )))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$1 (%I i$)))
             (let
              ((tmp%%$2 (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$))))
              (and
               (<= tmp%%$ tmp%%$1)
               (< tmp%%$1 tmp%%$2)
           ))))
           (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$) i$))
         ))
         :pattern ((vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. outputs$) i$))
         :qid user_det_harness__slice_sorted_by_bool_compare_76
         :skolemid skolem_user_det_harness__slice_sorted_by_bool_compare_76
    )))))
    :pattern ((det_harness!slice_sorted_by_bool_compare.? F&. F& T&. T& seq! compare!))
    :qid internal_det_harness!slice_sorted_by_bool_compare.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_bool_compare.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_bool_compare_result
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_bool_compare_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_bool_compare_result.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (compare! Poly) (ret! Poly))
   (!
    (= (det_harness!slice_sorted_by_bool_compare_result.? F&. F& T&. T& seq! compare! ret!)
     (and
      (det_harness!fnmut_adjacent_bool_trace_valid.? F&. F& T&. T& seq! compare!)
      (= (%B ret!) (det_harness!slice_sorted_by_bool_compare.? F&. F& T&. T& seq! compare!))
    ))
    :pattern ((det_harness!slice_sorted_by_bool_compare_result.? F&. F& T&. T& seq! compare!
      ret!
    ))
    :qid internal_det_harness!slice_sorted_by_bool_compare_result.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_bool_compare_result.?_definition
))))

;; Function-Axioms det_harness::fnmut_adjacent_key_trace_valid
(assert
 (fuel_bool_default fuel%det_harness!fnmut_adjacent_key_trace_valid.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!fnmut_adjacent_key_trace_valid.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (seq! Poly) (f!
     Poly
    )
   ) (!
    (= (det_harness!fnmut_adjacent_key_trace_valid.? F&. F& T&. T& K&. K& seq! f!) (let
      ((outputs$ (det_harness!fnmut_adjacent_key_outputs.? F&. F& T&. T& K&. K& f! seq!)))
      (and
       (and
        (and
         (and
          (and
           (<= (vstd!seq.Seq.len.? K&. K& outputs$) (vstd!seq.Seq.len.? T&. T& seq!))
           (=>
            (= (vstd!seq.Seq.len.? T&. T& seq!) 0)
            (= (vstd!seq.Seq.len.? K&. K& outputs$) 0)
          ))
          (=>
           (> (vstd!seq.Seq.len.? T&. T& seq!) 0)
           (> (vstd!seq.Seq.len.? K&. K& outputs$) 0)
         ))
         (=>
          (< (vstd!seq.Seq.len.? K&. K& outputs$) (vstd!seq.Seq.len.? T&. T& seq!))
          (>= (vstd!seq.Seq.len.? K&. K& outputs$) 2)
        ))
        (=>
         (< (vstd!seq.Seq.len.? K&. K& outputs$) (vstd!seq.Seq.len.? T&. T& seq!))
         (not (det_harness!partial_ord_leq_observed.? K&. K& (vstd!seq.Seq.index.? K&. K& outputs$
            (I (Sub (vstd!seq.Seq.len.? K&. K& outputs$) 2))
           ) (vstd!seq.Seq.index.? K&. K& outputs$ (I (Sub (vstd!seq.Seq.len.? K&. K& outputs$)
              1
       )))))))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (and
            (<= 0 (%I i$))
            (< (Add (%I i$) 2) (vstd!seq.Seq.len.? K&. K& outputs$))
           )
           (det_harness!partial_ord_leq_observed.? K&. K& (vstd!seq.Seq.index.? K&. K& outputs$
             i$
            ) (vstd!seq.Seq.index.? K&. K& outputs$ (I (Add (%I i$) 1)))
         )))
         :pattern ((det_harness!partial_ord_leq_observed.? K&. K& (vstd!seq.Seq.index.? K&. K&
            outputs$ i$
           ) (vstd!seq.Seq.index.? K&. K& outputs$ (I (Add (%I i$) 1)))
         ))
         :qid user_det_harness__fnmut_adjacent_key_trace_valid_77
         :skolemid skolem_user_det_harness__fnmut_adjacent_key_trace_valid_77
    )))))
    :pattern ((det_harness!fnmut_adjacent_key_trace_valid.? F&. F& T&. T& K&. K& seq! f!))
    :qid internal_det_harness!fnmut_adjacent_key_trace_valid.?_definition
    :skolemid skolem_internal_det_harness!fnmut_adjacent_key_trace_valid.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_partial_key
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_partial_key.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_partial_key.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (seq! Poly) (f!
     Poly
    )
   ) (!
    (= (det_harness!slice_sorted_by_partial_key.? F&. F& T&. T& K&. K& seq! f!) (let
      ((outputs$ (det_harness!fnmut_adjacent_key_outputs.? F&. F& T&. T& K&. K& f! seq!)))
      (and
       (and
        (det_harness!fnmut_adjacent_key_trace_valid.? F&. F& T&. T& K&. K& seq! f!)
        (= (vstd!seq.Seq.len.? K&. K& outputs$) (vstd!seq.Seq.len.? T&. T& seq!))
       )
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (and
            (<= 0 (%I i$))
            (< (Add (%I i$) 1) (vstd!seq.Seq.len.? K&. K& outputs$))
           )
           (det_harness!partial_ord_leq_observed.? K&. K& (vstd!seq.Seq.index.? K&. K& outputs$
             i$
            ) (vstd!seq.Seq.index.? K&. K& outputs$ (I (Add (%I i$) 1)))
         )))
         :pattern ((det_harness!partial_ord_leq_observed.? K&. K& (vstd!seq.Seq.index.? K&. K&
            outputs$ i$
           ) (vstd!seq.Seq.index.? K&. K& outputs$ (I (Add (%I i$) 1)))
         ))
         :qid user_det_harness__slice_sorted_by_partial_key_78
         :skolemid skolem_user_det_harness__slice_sorted_by_partial_key_78
    )))))
    :pattern ((det_harness!slice_sorted_by_partial_key.? F&. F& T&. T& K&. K& seq! f!))
    :qid internal_det_harness!slice_sorted_by_partial_key.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_partial_key.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_partial_key_result
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_partial_key_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_partial_key_result.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (seq! Poly) (f!
     Poly
    ) (ret! Poly)
   ) (!
    (= (det_harness!slice_sorted_by_partial_key_result.? F&. F& T&. T& K&. K& seq! f! ret!)
     (and
      (det_harness!fnmut_adjacent_key_trace_valid.? F&. F& T&. T& K&. K& seq! f!)
      (= (%B ret!) (det_harness!slice_sorted_by_partial_key.? F&. F& T&. T& K&. K& seq! f!))
    ))
    :pattern ((det_harness!slice_sorted_by_partial_key_result.? F&. F& T&. T& K&. K& seq!
      f! ret!
    ))
    :qid internal_det_harness!slice_sorted_by_partial_key_result.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_partial_key_result.?_definition
))))

;; Function-Axioms det_harness::slice_ord_equal_at
(assert
 (fuel_bool_default fuel%det_harness!slice_ord_equal_at.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_ord_equal_at.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly) (index! Poly)) (!
    (= (det_harness!slice_ord_equal_at.? T&. T& seq! value! index!) (and
      (< (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (= (det_harness!ord_cmp_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! index!)
        value!
       ) core!cmp.Ordering./Equal
    )))
    :pattern ((det_harness!slice_ord_equal_at.? T&. T& seq! value! index!))
    :qid internal_det_harness!slice_ord_equal_at.?_definition
    :skolemid skolem_internal_det_harness!slice_ord_equal_at.?_definition
))))

;; Function-Axioms det_harness::slice_ord_insertion_point
(assert
 (fuel_bool_default fuel%det_harness!slice_ord_insertion_point.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_ord_insertion_point.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly) (index! Poly)) (!
    (= (det_harness!slice_ord_insertion_point.? T&. T& seq! value! index!) (and
      (<= (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (forall ((j$ Poly)) (!
        (=>
         (has_type j$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I j$)))
            (let
             ((tmp%%$2 (%I index!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (and
           (= (det_harness!ord_cmp_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! j$) value!)
            core!cmp.Ordering./Less
           )
           (forall ((j$0 Poly)) (!
             (=>
              (has_type j$0 INT)
              (=>
               (let
                ((tmp%%$ (%I index!)))
                (let
                 ((tmp%%$4 (%I j$0)))
                 (let
                  ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& seq!)))
                  (and
                   (<= tmp%%$ tmp%%$4)
                   (< tmp%%$4 tmp%%$5)
               ))))
               (= (det_harness!ord_cmp_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& seq! j$0) value!)
                core!cmp.Ordering./Greater
             )))
             :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$0))
             :qid user_det_harness__slice_ord_insertion_point_79
             :skolemid skolem_user_det_harness__slice_ord_insertion_point_79
        )))))
        :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$))
        :qid user_det_harness__slice_ord_insertion_point_80
        :skolemid skolem_user_det_harness__slice_ord_insertion_point_80
    ))))
    :pattern ((det_harness!slice_ord_insertion_point.? T&. T& seq! value! index!))
    :qid internal_det_harness!slice_ord_insertion_point.?_definition
    :skolemid skolem_internal_det_harness!slice_ord_insertion_point.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_result
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_result.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (value! Poly) (result! Poly)) (!
    (= (det_harness!slice_binary_search_result.? T&. T& seq! value! result!) (and
      (ite
       (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
       (let
        ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (< index$ (vstd!seq.Seq.len.? T&. T& seq!))
       )
       (let
        ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (<= index$ (vstd!seq.Seq.len.? T&. T& seq!))
      ))
      (=>
       (det_harness!slice_sorted_by_ord.? T&. T& seq!)
       (ite
        (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
        (let
         ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_ord_equal_at.? T&. T& seq! value! (I index$))
        )
        (let
         ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_ord_insertion_point.? T&. T& seq! value! (I index$))
    )))))
    :pattern ((det_harness!slice_binary_search_result.? T&. T& seq! value! result!))
    :qid internal_det_harness!slice_binary_search_result.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_result.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_ordered
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_ordered.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_ordered.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (f! Poly)) (!
    (= (det_harness!slice_binary_search_by_ordered.? F&. F& T&. T& seq! f!) (forall ((i$
        Poly
       ) (j$ Poly)
      ) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (<= (det_harness!ordering_rank.? (Poly%core!cmp.Ordering. (det_harness!fnmut_ordering_observed.?
             F&. F& T&. T& f! (vstd!seq.Seq.index.? T&. T& seq! i$)
           ))
          ) (det_harness!ordering_rank.? (Poly%core!cmp.Ordering. (det_harness!fnmut_ordering_observed.?
             F&. F& T&. T& f! (vstd!seq.Seq.index.? T&. T& seq! j$)
       ))))))
       :pattern ((vstd!seq.Seq.index.? T&. T& seq! i$) (vstd!seq.Seq.index.? T&. T& seq! j$))
       :qid user_det_harness__slice_binary_search_by_ordered_81
       :skolemid skolem_user_det_harness__slice_binary_search_by_ordered_81
    )))
    :pattern ((det_harness!slice_binary_search_by_ordered.? F&. F& T&. T& seq! f!))
    :qid internal_det_harness!slice_binary_search_by_ordered.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_ordered.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_equal_at
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_equal_at.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_equal_at.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (f! Poly) (index! Poly))
   (!
    (= (det_harness!slice_binary_search_by_equal_at.? F&. F& T&. T& seq! f! index!) (and
      (< (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (= (det_harness!fnmut_ordering_observed.? F&. F& T&. T& f! (vstd!seq.Seq.index.? T&.
         T& seq! index!
        )
       ) core!cmp.Ordering./Equal
    )))
    :pattern ((det_harness!slice_binary_search_by_equal_at.? F&. F& T&. T& seq! f! index!))
    :qid internal_det_harness!slice_binary_search_by_equal_at.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_equal_at.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_insertion_point
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_insertion_point.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_insertion_point.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (f! Poly) (index! Poly))
   (!
    (= (det_harness!slice_binary_search_by_insertion_point.? F&. F& T&. T& seq! f! index!)
     (and
      (<= (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (forall ((j$ Poly)) (!
        (=>
         (has_type j$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I j$)))
            (let
             ((tmp%%$2 (%I index!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (and
           (= (det_harness!fnmut_ordering_observed.? F&. F& T&. T& f! (vstd!seq.Seq.index.? T&.
              T& seq! j$
             )
            ) core!cmp.Ordering./Less
           )
           (forall ((j$0 Poly)) (!
             (=>
              (has_type j$0 INT)
              (=>
               (let
                ((tmp%%$ (%I index!)))
                (let
                 ((tmp%%$4 (%I j$0)))
                 (let
                  ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& seq!)))
                  (and
                   (<= tmp%%$ tmp%%$4)
                   (< tmp%%$4 tmp%%$5)
               ))))
               (= (det_harness!fnmut_ordering_observed.? F&. F& T&. T& f! (vstd!seq.Seq.index.? T&.
                  T& seq! j$0
                 )
                ) core!cmp.Ordering./Greater
             )))
             :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$0))
             :qid user_det_harness__slice_binary_search_by_insertion_point_82
             :skolemid skolem_user_det_harness__slice_binary_search_by_insertion_point_82
        )))))
        :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$))
        :qid user_det_harness__slice_binary_search_by_insertion_point_83
        :skolemid skolem_user_det_harness__slice_binary_search_by_insertion_point_83
    ))))
    :pattern ((det_harness!slice_binary_search_by_insertion_point.? F&. F& T&. T& seq!
      f! index!
    ))
    :qid internal_det_harness!slice_binary_search_by_insertion_point.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_insertion_point.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_result
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_result.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (f! Poly) (result! Poly))
   (!
    (= (det_harness!slice_binary_search_by_result.? F&. F& T&. T& seq! f! result!) (and
      (ite
       (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
       (let
        ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (< index$ (vstd!seq.Seq.len.? T&. T& seq!))
       )
       (let
        ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (<= index$ (vstd!seq.Seq.len.? T&. T& seq!))
      ))
      (=>
       (det_harness!slice_binary_search_by_ordered.? F&. F& T&. T& seq! f!)
       (ite
        (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
        (let
         ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_binary_search_by_equal_at.? F&. F& T&. T& seq! f! (I index$))
        )
        (let
         ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_binary_search_by_insertion_point.? F&. F& T&. T& seq! f! (I index$))
    )))))
    :pattern ((det_harness!slice_binary_search_by_result.? F&. F& T&. T& seq! f! result!))
    :qid internal_det_harness!slice_binary_search_by_result.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_result.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_key_ordered
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_key_ordered.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_key_ordered.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (B&. Dcr) (B& Type) (seq! Poly) (f!
     Poly
    )
   ) (!
    (= (det_harness!slice_binary_search_by_key_ordered.? F&. F& T&. T& B&. B& seq! f!)
     (forall ((i$ Poly) (j$ Poly)) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (det_harness!ord_leq_observed.? B&. B& (det_harness!fnmut_key_observed.? F&. F& T&.
           T& B&. B& f! (vstd!seq.Seq.index.? T&. T& seq! i$)
          ) (det_harness!fnmut_key_observed.? F&. F& T&. T& B&. B& f! (vstd!seq.Seq.index.? T&.
            T& seq! j$
       )))))
       :pattern ((det_harness!ord_leq_observed.? B&. B& (det_harness!fnmut_key_observed.? F&.
          F& T&. T& B&. B& f! (vstd!seq.Seq.index.? T&. T& seq! i$)
         ) (det_harness!fnmut_key_observed.? F&. F& T&. T& B&. B& f! (vstd!seq.Seq.index.? T&.
           T& seq! j$
       ))))
       :qid user_det_harness__slice_binary_search_by_key_ordered_84
       :skolemid skolem_user_det_harness__slice_binary_search_by_key_ordered_84
    )))
    :pattern ((det_harness!slice_binary_search_by_key_ordered.? F&. F& T&. T& B&. B& seq!
      f!
    ))
    :qid internal_det_harness!slice_binary_search_by_key_ordered.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_key_ordered.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_key_equal_at
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_key_equal_at.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_key_equal_at.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (B&. Dcr) (B& Type) (seq! Poly) (key!
     Poly
    ) (f! Poly) (index! Poly)
   ) (!
    (= (det_harness!slice_binary_search_by_key_equal_at.? F&. F& T&. T& B&. B& seq! key!
      f! index!
     ) (and
      (< (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (= (det_harness!ord_cmp_observed.? B&. B& (det_harness!fnmut_key_observed.? F&. F& T&.
         T& B&. B& f! (vstd!seq.Seq.index.? T&. T& seq! index!)
        ) key!
       ) core!cmp.Ordering./Equal
    )))
    :pattern ((det_harness!slice_binary_search_by_key_equal_at.? F&. F& T&. T& B&. B& seq!
      key! f! index!
    ))
    :qid internal_det_harness!slice_binary_search_by_key_equal_at.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_key_equal_at.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_key_insertion_point
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_key_insertion_point.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_key_insertion_point.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (B&. Dcr) (B& Type) (seq! Poly) (key!
     Poly
    ) (f! Poly) (index! Poly)
   ) (!
    (= (det_harness!slice_binary_search_by_key_insertion_point.? F&. F& T&. T& B&. B& seq!
      key! f! index!
     ) (and
      (<= (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (forall ((j$ Poly)) (!
        (=>
         (has_type j$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I j$)))
            (let
             ((tmp%%$2 (%I index!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (and
           (= (det_harness!ord_cmp_observed.? B&. B& (det_harness!fnmut_key_observed.? F&. F& T&.
              T& B&. B& f! (vstd!seq.Seq.index.? T&. T& seq! j$)
             ) key!
            ) core!cmp.Ordering./Less
           )
           (forall ((j$0 Poly)) (!
             (=>
              (has_type j$0 INT)
              (=>
               (let
                ((tmp%%$ (%I index!)))
                (let
                 ((tmp%%$4 (%I j$0)))
                 (let
                  ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& seq!)))
                  (and
                   (<= tmp%%$ tmp%%$4)
                   (< tmp%%$4 tmp%%$5)
               ))))
               (= (det_harness!ord_cmp_observed.? B&. B& (det_harness!fnmut_key_observed.? F&. F& T&.
                  T& B&. B& f! (vstd!seq.Seq.index.? T&. T& seq! j$0)
                 ) key!
                ) core!cmp.Ordering./Greater
             )))
             :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$0))
             :qid user_det_harness__slice_binary_search_by_key_insertion_point_85
             :skolemid skolem_user_det_harness__slice_binary_search_by_key_insertion_point_85
        )))))
        :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$))
        :qid user_det_harness__slice_binary_search_by_key_insertion_point_86
        :skolemid skolem_user_det_harness__slice_binary_search_by_key_insertion_point_86
    ))))
    :pattern ((det_harness!slice_binary_search_by_key_insertion_point.? F&. F& T&. T& B&.
      B& seq! key! f! index!
    ))
    :qid internal_det_harness!slice_binary_search_by_key_insertion_point.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_key_insertion_point.?_definition
))))

;; Function-Axioms det_harness::slice_binary_search_by_key_result
(assert
 (fuel_bool_default fuel%det_harness!slice_binary_search_by_key_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_binary_search_by_key_result.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (B&. Dcr) (B& Type) (seq! Poly) (key!
     Poly
    ) (f! Poly) (result! Poly)
   ) (!
    (= (det_harness!slice_binary_search_by_key_result.? F&. F& T&. T& B&. B& seq! key!
      f! result!
     ) (and
      (ite
       (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
       (let
        ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (< index$ (vstd!seq.Seq.len.? T&. T& seq!))
       )
       (let
        ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
        (<= index$ (vstd!seq.Seq.len.? T&. T& seq!))
      ))
      (=>
       (det_harness!slice_binary_search_by_key_ordered.? F&. F& T&. T& B&. B& seq! f!)
       (ite
        (is-core!result.Result./Ok (%Poly%core!result.Result. result!))
        (let
         ((index$ (%I (core!result.Result./Ok/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_binary_search_by_key_equal_at.? F&. F& T&. T& B&. B& seq! key!
          f! (I index$)
        ))
        (let
         ((index$ (%I (core!result.Result./Err/0 $ USIZE $ USIZE (%Poly%core!result.Result. result!)))))
         (det_harness!slice_binary_search_by_key_insertion_point.? F&. F& T&. T& B&. B& seq!
          key! f! (I index$)
    ))))))
    :pattern ((det_harness!slice_binary_search_by_key_result.? F&. F& T&. T& B&. B& seq!
      key! f! result!
    ))
    :qid internal_det_harness!slice_binary_search_by_key_result.?_definition
    :skolemid skolem_internal_det_harness!slice_binary_search_by_key_result.?_definition
))))

;; Function-Axioms det_harness::slice_partitioned_by_predicate
(assert
 (fuel_bool_default fuel%det_harness!slice_partitioned_by_predicate.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_partitioned_by_predicate.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (pred! Poly)) (!
    (= (det_harness!slice_partitioned_by_predicate.? F&. F& T&. T& seq! pred!) (forall
      ((i$ Poly) (j$ Poly)) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (=>
          (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.? T&.
            T& seq! j$
          ))
          (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.? T&.
            T& seq! i$
       )))))
       :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$) (vstd!seq.Seq.index.? T&. T& seq! i$))
       :qid user_det_harness__slice_partitioned_by_predicate_87
       :skolemid skolem_user_det_harness__slice_partitioned_by_predicate_87
    )))
    :pattern ((det_harness!slice_partitioned_by_predicate.? F&. F& T&. T& seq! pred!))
    :qid internal_det_harness!slice_partitioned_by_predicate.?_definition
    :skolemid skolem_internal_det_harness!slice_partitioned_by_predicate.?_definition
))))

;; Function-Axioms det_harness::slice_partition_point_result
(assert
 (fuel_bool_default fuel%det_harness!slice_partition_point_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_partition_point_result.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (seq! Poly) (pred! Poly) (index! Poly))
   (!
    (= (det_harness!slice_partition_point_result.? F&. F& T&. T& seq! pred! index!) (and
      (<= (%I index!) (vstd!seq.Seq.len.? T&. T& seq!))
      (=>
       (det_harness!slice_partitioned_by_predicate.? F&. F& T&. T& seq! pred!)
       (and
        (forall ((j$ Poly)) (!
          (=>
           (has_type j$ INT)
           (=>
            (let
             ((tmp%%$ 0))
             (let
              ((tmp%%$1 (%I j$)))
              (let
               ((tmp%%$2 (%I index!)))
               (and
                (<= tmp%%$ tmp%%$1)
                (< tmp%%$1 tmp%%$2)
            ))))
            (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.? T&.
              T& seq! j$
          ))))
          :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$))
          :qid user_det_harness__slice_partition_point_result_88
          :skolemid skolem_user_det_harness__slice_partition_point_result_88
        ))
        (forall ((j$ Poly)) (!
          (=>
           (has_type j$ INT)
           (=>
            (let
             ((tmp%%$ (%I index!)))
             (let
              ((tmp%%$4 (%I j$)))
              (let
               ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& seq!)))
               (and
                (<= tmp%%$ tmp%%$4)
                (< tmp%%$4 tmp%%$5)
            ))))
            (not (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
               T&. T& seq! j$
          )))))
          :pattern ((vstd!seq.Seq.index.? T&. T& seq! j$))
          :qid user_det_harness__slice_partition_point_result_89
          :skolemid skolem_user_det_harness__slice_partition_point_result_89
    ))))))
    :pattern ((det_harness!slice_partition_point_result.? F&. F& T&. T& seq! pred! index!))
    :qid internal_det_harness!slice_partition_point_result.?_definition
    :skolemid skolem_internal_det_harness!slice_partition_point_result.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_cmp
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_cmp.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_cmp.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (observation! Poly)) (!
    (= (det_harness!slice_sorted_by_cmp.? T&. T& seq! observation!) (forall ((i$ Poly) (
        j$ Poly
       )
      ) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (det_harness!comparator_leq_observed.? T&. T& observation! (vstd!seq.Seq.index.? T&.
           T& seq! i$
          ) (vstd!seq.Seq.index.? T&. T& seq! j$)
       )))
       :pattern ((det_harness!comparator_leq_observed.? T&. T& observation! (vstd!seq.Seq.index.?
          T&. T& seq! i$
         ) (vstd!seq.Seq.index.? T&. T& seq! j$)
       ))
       :qid user_det_harness__slice_sorted_by_cmp_90
       :skolemid skolem_user_det_harness__slice_sorted_by_cmp_90
    )))
    :pattern ((det_harness!slice_sorted_by_cmp.? T&. T& seq! observation!))
    :qid internal_det_harness!slice_sorted_by_cmp.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_cmp.?_definition
))))

;; Function-Axioms det_harness::slice_sorted_by_key
(assert
 (fuel_bool_default fuel%det_harness!slice_sorted_by_key.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_sorted_by_key.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (seq! Poly) (f!
     Poly
    )
   ) (!
    (= (det_harness!slice_sorted_by_key.? F&. F& T&. T& K&. K& seq! f!) (forall ((i$ Poly)
       (j$ Poly)
      ) (!
       (=>
        (and
         (has_type i$ INT)
         (has_type j$ INT)
        )
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (%I j$)))
            (let
             ((tmp%%$3 (vstd!seq.Seq.len.? T&. T& seq!)))
             (and
              (and
               (<= tmp%%$ tmp%%$1)
               (<= tmp%%$1 tmp%%$2)
              )
              (< tmp%%$2 tmp%%$3)
         )))))
         (det_harness!ord_leq_observed.? K&. K& (det_harness!fnmut_key_observed.? F&. F& T&.
           T& K&. K& f! (vstd!seq.Seq.index.? T&. T& seq! i$)
          ) (det_harness!fnmut_key_observed.? F&. F& T&. T& K&. K& f! (vstd!seq.Seq.index.? T&.
            T& seq! j$
       )))))
       :pattern ((det_harness!ord_leq_observed.? K&. K& (det_harness!fnmut_key_observed.? F&.
          F& T&. T& K&. K& f! (vstd!seq.Seq.index.? T&. T& seq! i$)
         ) (det_harness!fnmut_key_observed.? F&. F& T&. T& K&. K& f! (vstd!seq.Seq.index.? T&.
           T& seq! j$
       ))))
       :qid user_det_harness__slice_sorted_by_key_91
       :skolemid skolem_user_det_harness__slice_sorted_by_key_91
    )))
    :pattern ((det_harness!slice_sorted_by_key.? F&. F& T&. T& K&. K& seq! f!))
    :qid internal_det_harness!slice_sorted_by_key.?_definition
    :skolemid skolem_internal_det_harness!slice_sorted_by_key.?_definition
))))

;; Function-Axioms det_harness::slice_select_partition_ord
(assert
 (fuel_bool_default fuel%det_harness!slice_select_partition_ord.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_select_partition_ord.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (pivot! Poly) (right! Poly)) (!
    (= (det_harness!slice_select_partition_ord.? T&. T& left! pivot! right!) (and
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& left!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (det_harness!ord_leq_observed.? T&. T& (vstd!seq.Seq.index.? T&. T& left! i$) pivot!)
        ))
        :pattern ((vstd!seq.Seq.index.? T&. T& left! i$))
        :qid user_det_harness__slice_select_partition_ord_92
        :skolemid skolem_user_det_harness__slice_select_partition_ord_92
      ))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$4 (%I i$)))
            (let
             ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& right!)))
             (and
              (<= tmp%%$ tmp%%$4)
              (< tmp%%$4 tmp%%$5)
          ))))
          (det_harness!ord_leq_observed.? T&. T& pivot! (vstd!seq.Seq.index.? T&. T& right! i$))
        ))
        :pattern ((vstd!seq.Seq.index.? T&. T& right! i$))
        :qid user_det_harness__slice_select_partition_ord_93
        :skolemid skolem_user_det_harness__slice_select_partition_ord_93
    ))))
    :pattern ((det_harness!slice_select_partition_ord.? T&. T& left! pivot! right!))
    :qid internal_det_harness!slice_select_partition_ord.?_definition
    :skolemid skolem_internal_det_harness!slice_select_partition_ord.?_definition
))))

;; Function-Axioms det_harness::slice_select_partition_cmp
(assert
 (fuel_bool_default fuel%det_harness!slice_select_partition_cmp.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_select_partition_cmp.)
  (forall ((T&. Dcr) (T& Type) (left! Poly) (pivot! Poly) (right! Poly) (observation!
     Poly
    )
   ) (!
    (= (det_harness!slice_select_partition_cmp.? T&. T& left! pivot! right! observation!)
     (and
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& left!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (det_harness!comparator_leq_observed.? T&. T& observation! (vstd!seq.Seq.index.? T&.
            T& left! i$
           ) pivot!
        )))
        :pattern ((vstd!seq.Seq.index.? T&. T& left! i$))
        :qid user_det_harness__slice_select_partition_cmp_94
        :skolemid skolem_user_det_harness__slice_select_partition_cmp_94
      ))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$4 (%I i$)))
            (let
             ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& right!)))
             (and
              (<= tmp%%$ tmp%%$4)
              (< tmp%%$4 tmp%%$5)
          ))))
          (det_harness!comparator_leq_observed.? T&. T& observation! pivot! (vstd!seq.Seq.index.?
            T&. T& right! i$
        ))))
        :pattern ((vstd!seq.Seq.index.? T&. T& right! i$))
        :qid user_det_harness__slice_select_partition_cmp_95
        :skolemid skolem_user_det_harness__slice_select_partition_cmp_95
    ))))
    :pattern ((det_harness!slice_select_partition_cmp.? T&. T& left! pivot! right! observation!))
    :qid internal_det_harness!slice_select_partition_cmp.?_definition
    :skolemid skolem_internal_det_harness!slice_select_partition_cmp.?_definition
))))

;; Function-Axioms det_harness::slice_select_partition_key
(assert
 (fuel_bool_default fuel%det_harness!slice_select_partition_key.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_select_partition_key.)
  (forall ((F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (K&. Dcr) (K& Type) (left! Poly) (
     pivot! Poly
    ) (right! Poly) (f! Poly)
   ) (!
    (= (det_harness!slice_select_partition_key.? F&. F& T&. T& K&. K& left! pivot! right!
      f!
     ) (and
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& left!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (det_harness!ord_leq_observed.? K&. K& (det_harness!fnmut_key_observed.? F&. F& T&.
            T& K&. K& f! (vstd!seq.Seq.index.? T&. T& left! i$)
           ) (det_harness!fnmut_key_observed.? F&. F& T&. T& K&. K& f! pivot!)
        )))
        :pattern ((vstd!seq.Seq.index.? T&. T& left! i$))
        :qid user_det_harness__slice_select_partition_key_96
        :skolemid skolem_user_det_harness__slice_select_partition_key_96
      ))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$4 (%I i$)))
            (let
             ((tmp%%$5 (vstd!seq.Seq.len.? T&. T& right!)))
             (and
              (<= tmp%%$ tmp%%$4)
              (< tmp%%$4 tmp%%$5)
          ))))
          (det_harness!ord_leq_observed.? K&. K& (det_harness!fnmut_key_observed.? F&. F& T&.
            T& K&. K& f! pivot!
           ) (det_harness!fnmut_key_observed.? F&. F& T&. T& K&. K& f! (vstd!seq.Seq.index.? T&.
             T& right! i$
        )))))
        :pattern ((vstd!seq.Seq.index.? T&. T& right! i$))
        :qid user_det_harness__slice_select_partition_key_97
        :skolemid skolem_user_det_harness__slice_select_partition_key_97
    ))))
    :pattern ((det_harness!slice_select_partition_key.? F&. F& T&. T& K&. K& left! pivot!
      right! f!
    ))
    :qid internal_det_harness!slice_select_partition_key.?_definition
    :skolemid skolem_internal_det_harness!slice_select_partition_key.?_definition
))))

;; Function-Axioms det_harness::slice_partitioned_at
(assert
 (fuel_bool_default fuel%det_harness!slice_partitioned_at.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_partitioned_at.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (index! Poly)) (!
    (= (det_harness!slice_partitioned_at.? T&. T& seq! index!) (let
      ((tmp%%$ 0))
      (let
       ((tmp%%$1 (%I index!)))
       (let
        ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& seq!)))
        (and
         (<= tmp%%$ tmp%%$1)
         (<= tmp%%$1 tmp%%$2)
    )))))
    :pattern ((det_harness!slice_partitioned_at.? T&. T& seq! index!))
    :qid internal_det_harness!slice_partitioned_at.?_definition
    :skolemid skolem_internal_det_harness!slice_partitioned_at.?_definition
))))

;; Function-Axioms det_harness::slice_chunk_partition
(assert
 (fuel_bool_default fuel%det_harness!slice_chunk_partition.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_chunk_partition.)
  (forall ((T&. Dcr) (T& Type) (view! Poly)) (!
    (= (det_harness!slice_chunk_partition.? T&. T& view!) (and
      (and
       (and
        (and
         (det_harness!slice_iterator_well_formed.? T&. T& view!)
         (> (det_harness!SliceIteratorView./SliceIteratorView/chunk_size (%Poly%det_harness!SliceIteratorView.
            view!
           )
          ) 0
        ))
        (< (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/remainder
           (%Poly%det_harness!SliceIteratorView. view!)
          )
         ) (det_harness!SliceIteratorView./SliceIteratorView/chunk_size (%Poly%det_harness!SliceIteratorView.
           view!
       ))))
       (= (EucMod (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/remaining
           (%Poly%det_harness!SliceIteratorView. view!)
          )
         ) (det_harness!SliceIteratorView./SliceIteratorView/chunk_size (%Poly%det_harness!SliceIteratorView.
           view!
         ))
        ) 0
      ))
      (= (vstd!seq.Seq.add.? T&. T& (vstd!seq.Seq.add.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
          (%Poly%det_harness!SliceIteratorView. view!)
         ) (det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
           view!
         ))
        ) (det_harness!SliceIteratorView./SliceIteratorView/remainder (%Poly%det_harness!SliceIteratorView.
          view!
        ))
       ) (det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
         view!
    )))))
    :pattern ((det_harness!slice_chunk_partition.? T&. T& view!))
    :qid internal_det_harness!slice_chunk_partition.?_definition
    :skolemid skolem_internal_det_harness!slice_chunk_partition.?_definition
))))

;; Function-Axioms det_harness::slice_predicate_split_view
(assert
 (fuel_bool_default fuel%det_harness!slice_predicate_split_view.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_predicate_split_view.)
  (forall ((I&. Dcr) (I& Type) (F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (iter! Poly) (
     source! Poly
    ) (pred! Poly) (inclusive! Poly) (reverse! Poly) (limit! Poly)
   ) (!
    (= (det_harness!slice_predicate_split_view.? I&. I& F&. F& T&. T& iter! source! pred!
      inclusive! reverse! limit!
     ) (let
      ((view$ (det_harness!slice_iterator_view.? I&. I& T&. T& iter!)))
      (and
       (and
        (and
         (and
          (and
           (and
            (and
             (and
              (det_harness!slice_iterator_well_formed.? T&. T& (Poly%det_harness!SliceIteratorView.
                view$
              ))
              (= (det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
                 (Poly%det_harness!SliceIteratorView. view$)
                )
               ) source!
             ))
             (= (det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
                (Poly%det_harness!SliceIteratorView. view$)
               )
              ) source!
            ))
            (= (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
               (%Poly%det_harness!SliceIteratorView. (Poly%det_harness!SliceIteratorView. view$))
              )
             ) 0
           ))
           (= (det_harness!SliceIteratorView./SliceIteratorView/reverse (%Poly%det_harness!SliceIteratorView.
              (Poly%det_harness!SliceIteratorView. view$)
             )
            ) (%B reverse!)
          ))
          (= (det_harness!SliceIteratorView./SliceIteratorView/chunk_size (%Poly%det_harness!SliceIteratorView.
             (Poly%det_harness!SliceIteratorView. view$)
            )
           ) (%I limit!)
         ))
         (>= (%I limit!) 0)
        )
        (or
         (%B inclusive!)
         (not (%B inclusive!))
       ))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$1 (%I i$)))
             (let
              ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& source!)))
              (and
               (<= tmp%%$ tmp%%$1)
               (< tmp%%$1 tmp%%$2)
           ))))
           (or
            (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.? T&.
              T& source! i$
            ))
            (not (det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
               T&. T& source! i$
         ))))))
         :pattern ((det_harness!fnmut_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
            T&. T& source! i$
         )))
         :qid user_det_harness__slice_predicate_split_view_98
         :skolemid skolem_user_det_harness__slice_predicate_split_view_98
    )))))
    :pattern ((det_harness!slice_predicate_split_view.? I&. I& F&. F& T&. T& iter! source!
      pred! inclusive! reverse! limit!
    ))
    :qid internal_det_harness!slice_predicate_split_view.?_definition
    :skolemid skolem_internal_det_harness!slice_predicate_split_view.?_definition
))))

;; Function-Axioms det_harness::slice_adjacent_chunk_view
(assert
 (fuel_bool_default fuel%det_harness!slice_adjacent_chunk_view.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_adjacent_chunk_view.)
  (forall ((I&. Dcr) (I& Type) (F&. Dcr) (F& Type) (T&. Dcr) (T& Type) (iter! Poly) (
     source! Poly
    ) (pred! Poly)
   ) (!
    (= (det_harness!slice_adjacent_chunk_view.? I&. I& F&. F& T&. T& iter! source! pred!)
     (let
      ((view$ (det_harness!slice_iterator_view.? I&. I& T&. T& iter!)))
      (and
       (and
        (and
         (and
          (det_harness!slice_iterator_well_formed.? T&. T& (Poly%det_harness!SliceIteratorView.
            view$
          ))
          (= (det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
             (Poly%det_harness!SliceIteratorView. view$)
            )
           ) source!
         ))
         (= (det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
            (Poly%det_harness!SliceIteratorView. view$)
           )
          ) source!
        ))
        (= (vstd!seq.Seq.len.? T&. T& (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
           (%Poly%det_harness!SliceIteratorView. (Poly%det_harness!SliceIteratorView. view$))
          )
         ) 0
       ))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$1 (Add (%I i$) 1)))
             (let
              ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& source!)))
              (and
               (<= tmp%%$ tmp%%$1)
               (< tmp%%$1 tmp%%$2)
           ))))
           (or
            (det_harness!fnmut_adjacent_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
              T&. T& source! i$
             ) (vstd!seq.Seq.index.? T&. T& source! (I (Add (%I i$) 1)))
            )
            (not (det_harness!fnmut_adjacent_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
               T&. T& source! i$
              ) (vstd!seq.Seq.index.? T&. T& source! (I (Add (%I i$) 1)))
         )))))
         :pattern ((det_harness!fnmut_adjacent_predicate_observed.? F&. F& T&. T& pred! (vstd!seq.Seq.index.?
            T&. T& source! i$
           ) (vstd!seq.Seq.index.? T&. T& source! (I (Add (%I i$) 1)))
         ))
         :qid user_det_harness__slice_adjacent_chunk_view_99
         :skolemid skolem_user_det_harness__slice_adjacent_chunk_view_99
    )))))
    :pattern ((det_harness!slice_adjacent_chunk_view.? I&. I& F&. F& T&. T& iter! source!
      pred!
    ))
    :qid internal_det_harness!slice_adjacent_chunk_view.?_definition
    :skolemid skolem_internal_det_harness!slice_adjacent_chunk_view.?_definition
))))

;; Function-Axioms det_harness::slice_split_off_partition
(assert
 (fuel_bool_default fuel%det_harness!slice_split_off_partition.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_split_off_partition.)
  (forall ((T&. Dcr) (T& Type) (source! Poly) (remaining! Poly) (removed! Poly)) (!
    (= (det_harness!slice_split_off_partition.? T&. T& source! remaining! removed!) (or
      (= (vstd!seq.Seq.add.? T&. T& removed! remaining!) source!)
      (= (vstd!seq.Seq.add.? T&. T& remaining! removed!) source!)
    ))
    :pattern ((det_harness!slice_split_off_partition.? T&. T& source! remaining! removed!))
    :qid internal_det_harness!slice_split_off_partition.?_definition
    :skolemid skolem_internal_det_harness!slice_split_off_partition.?_definition
))))

;; Function-Axioms det_harness::slice_split_off_first_result
(assert
 (fuel_bool_default fuel%det_harness!slice_split_off_first_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_split_off_first_result.)
  (forall ((T&. Dcr) (T& Type) (source! Poly) (remaining! Poly) (value! Poly)) (!
    (= (det_harness!slice_split_off_first_result.? T&. T& source! remaining! value!) (
      and
      (and
       (not (= (vstd!seq.Seq.len.? T&. T& source!) 0))
       (= value! (vstd!seq.Seq.index.? T&. T& source! (I 0)))
      )
      (= remaining! (vstd!seq.Seq.subrange.? T&. T& source! (I 1) (I (vstd!seq.Seq.len.? T&.
          T& source!
    ))))))
    :pattern ((det_harness!slice_split_off_first_result.? T&. T& source! remaining! value!))
    :qid internal_det_harness!slice_split_off_first_result.?_definition
    :skolemid skolem_internal_det_harness!slice_split_off_first_result.?_definition
))))

;; Function-Axioms det_harness::slice_split_off_last_result
(assert
 (fuel_bool_default fuel%det_harness!slice_split_off_last_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_split_off_last_result.)
  (forall ((T&. Dcr) (T& Type) (source! Poly) (remaining! Poly) (value! Poly)) (!
    (= (det_harness!slice_split_off_last_result.? T&. T& source! remaining! value!) (and
      (and
       (not (= (vstd!seq.Seq.len.? T&. T& source!) 0))
       (= value! (vstd!seq.Seq.index.? T&. T& source! (I (Sub (vstd!seq.Seq.len.? T&. T& source!)
           1
      )))))
      (= remaining! (vstd!seq.Seq.subrange.? T&. T& source! (I 0) (I (Sub (vstd!seq.Seq.len.?
           T&. T& source!
          ) 1
    ))))))
    :pattern ((det_harness!slice_split_off_last_result.? T&. T& source! remaining! value!))
    :qid internal_det_harness!slice_split_off_last_result.?_definition
    :skolemid skolem_internal_det_harness!slice_split_off_last_result.?_definition
))))

;; Function-Axioms det_harness::utf8_chunk_partition
(assert
 (fuel_bool_default fuel%det_harness!utf8_chunk_partition.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!utf8_chunk_partition.)
  (forall ((I&. Dcr) (I& Type) (iter! Poly) (source! Poly)) (!
    (= (det_harness!utf8_chunk_partition.? I&. I& iter! source!) (let
      ((view$ (det_harness!slice_iterator_view.? I&. I& $ (UINT 8) iter!)))
      (and
       (and
        (and
         (det_harness!slice_iterator_well_formed.? $ (UINT 8) (Poly%det_harness!SliceIteratorView.
           view$
         ))
         (= (det_harness!SliceIteratorView./SliceIteratorView/source (%Poly%det_harness!SliceIteratorView.
            (Poly%det_harness!SliceIteratorView. view$)
           )
          ) source!
        ))
        (= (det_harness!SliceIteratorView./SliceIteratorView/remaining (%Poly%det_harness!SliceIteratorView.
           (Poly%det_harness!SliceIteratorView. view$)
          )
         ) source!
       ))
       (= (vstd!seq.Seq.len.? $ (UINT 8) (det_harness!SliceIteratorView./SliceIteratorView/yielded_prefix
          (%Poly%det_harness!SliceIteratorView. (Poly%det_harness!SliceIteratorView. view$))
         )
        ) 0
    ))))
    :pattern ((det_harness!utf8_chunk_partition.? I&. I& iter! source!))
    :qid internal_det_harness!utf8_chunk_partition.?_definition
    :skolemid skolem_internal_det_harness!utf8_chunk_partition.?_definition
))))

;; Function-Axioms det_harness::array_ref_view
(assert
 (fuel_bool_default fuel%det_harness!array_ref_view.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!array_ref_view.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
    (= (det_harness!array_ref_view.? T&. T& N&. N& array!) (vstd!view.View.view.? $ (ARRAY
       T&. T& N&. N&
      ) array!
    ))
    :pattern ((det_harness!array_ref_view.? T&. T& N&. N& array!))
    :qid internal_det_harness!array_ref_view.?_definition
    :skolemid skolem_internal_det_harness!array_ref_view.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
   (=>
    (has_type array! (ARRAY T&. T& N&. N&))
    (has_type (det_harness!array_ref_view.? T&. T& N&. N& array!) (TYPE%vstd!seq.Seq. T&.
      T&
   )))
   :pattern ((det_harness!array_ref_view.? T&. T& N&. N& array!))
   :qid internal_det_harness!array_ref_view.?_pre_post_definition
   :skolemid skolem_internal_det_harness!array_ref_view.?_pre_post_definition
)))

;; Function-Axioms det_harness::array_mut_ref_view
(assert
 (fuel_bool_default fuel%det_harness!array_mut_ref_view.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!array_mut_ref_view.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
    (= (det_harness!array_mut_ref_view.? T&. T& N&. N& array!) (vstd!view.View.view.? $
      (ARRAY T&. T& N&. N&) (mut_ref_current% array!)
    ))
    :pattern ((det_harness!array_mut_ref_view.? T&. T& N&. N& array!))
    :qid internal_det_harness!array_mut_ref_view.?_definition
    :skolemid skolem_internal_det_harness!array_mut_ref_view.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
   (=>
    (has_type array! (MUTREF $ (ARRAY T&. T& N&. N&)))
    (has_type (det_harness!array_mut_ref_view.? T&. T& N&. N& array!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!array_mut_ref_view.? T&. T& N&. N& array!))
   :qid internal_det_harness!array_mut_ref_view.?_pre_post_definition
   :skolemid skolem_internal_det_harness!array_mut_ref_view.?_pre_post_definition
)))

;; Function-Axioms det_harness::array_value_view
(assert
 (fuel_bool_default fuel%det_harness!array_value_view.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!array_value_view.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
    (= (det_harness!array_value_view.? T&. T& N&. N& array!) (vstd!view.View.view.? $ (
       ARRAY T&. T& N&. N&
      ) array!
    ))
    :pattern ((det_harness!array_value_view.? T&. T& N&. N& array!))
    :qid internal_det_harness!array_value_view.?_definition
    :skolemid skolem_internal_det_harness!array_value_view.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (array! Poly)) (!
   (=>
    (has_type array! (ARRAY T&. T& N&. N&))
    (has_type (det_harness!array_value_view.? T&. T& N&. N& array!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!array_value_view.? T&. T& N&. N& array!))
   :qid internal_det_harness!array_value_view.?_pre_post_definition
   :skolemid skolem_internal_det_harness!array_value_view.?_pre_post_definition
)))

;; Function-Axioms det_harness::split_point_in_range
(assert
 (fuel_bool_default fuel%det_harness!split_point_in_range.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!split_point_in_range.)
  (forall ((T&. Dcr) (T& Type) (seq! Poly) (mid! Poly)) (!
    (= (det_harness!split_point_in_range.? T&. T& seq! mid!) (<= (%I mid!) (vstd!seq.Seq.len.?
       T&. T& seq!
    )))
    :pattern ((det_harness!split_point_in_range.? T&. T& seq! mid!))
    :qid internal_det_harness!split_point_in_range.?_definition
    :skolemid skolem_internal_det_harness!split_point_in_range.?_definition
))))

;; Function-Axioms det_harness::slice_fixed_prefix
(assert
 (fuel_bool_default fuel%det_harness!slice_fixed_prefix.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_fixed_prefix.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly)) (!
    (= (det_harness!slice_fixed_prefix.? T&. T& N&. N& seq!) (vstd!seq.Seq.subrange.? T&.
      T& seq! (I 0) (I (const_int N&))
    ))
    :pattern ((det_harness!slice_fixed_prefix.? T&. T& N&. N& seq!))
    :qid internal_det_harness!slice_fixed_prefix.?_definition
    :skolemid skolem_internal_det_harness!slice_fixed_prefix.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly)) (!
   (=>
    (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (det_harness!slice_fixed_prefix.? T&. T& N&. N& seq!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!slice_fixed_prefix.? T&. T& N&. N& seq!))
   :qid internal_det_harness!slice_fixed_prefix.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_fixed_prefix.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_fixed_suffix
(assert
 (fuel_bool_default fuel%det_harness!slice_fixed_suffix.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_fixed_suffix.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly)) (!
    (= (det_harness!slice_fixed_suffix.? T&. T& N&. N& seq!) (vstd!seq.Seq.subrange.? T&.
      T& seq! (I (Sub (vstd!seq.Seq.len.? T&. T& seq!) (const_int N&))) (I (vstd!seq.Seq.len.?
        T&. T& seq!
    ))))
    :pattern ((det_harness!slice_fixed_suffix.? T&. T& N&. N& seq!))
    :qid internal_det_harness!slice_fixed_suffix.?_definition
    :skolemid skolem_internal_det_harness!slice_fixed_suffix.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly)) (!
   (=>
    (has_type seq! (TYPE%vstd!seq.Seq. T&. T&))
    (has_type (det_harness!slice_fixed_suffix.? T&. T& N&. N& seq!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!slice_fixed_suffix.? T&. T& N&. N& seq!))
   :qid internal_det_harness!slice_fixed_suffix.?_pre_post_definition
   :skolemid skolem_internal_det_harness!slice_fixed_suffix.?_pre_post_definition
)))

;; Function-Axioms det_harness::flatten_array_chunks
(assert
 (fuel_bool_default fuel%det_harness!flatten_array_chunks.)
)
(declare-fun %%lambda%%3 (Int Dcr Type Poly Dcr Type Dcr Type Int Dcr Type) %%Function%%)
(assert
 (forall ((%%hole%%0 Int) (%%hole%%1 Dcr) (%%hole%%2 Type) (%%hole%%3 Poly) (%%hole%%4
    Dcr
   ) (%%hole%%5 Type) (%%hole%%6 Dcr) (%%hole%%7 Type) (%%hole%%8 Int) (%%hole%%9 Dcr)
   (%%hole%%10 Type) (i$ Poly)
  ) (!
   (= (%%apply%%0 (%%lambda%%3 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3 %%hole%%4 %%hole%%5
      %%hole%%6 %%hole%%7 %%hole%%8 %%hole%%9 %%hole%%10
     ) i$
    ) (vstd!seq.Seq.index.? %%hole%%9 %%hole%%10 (det_harness!array_value_view.? %%hole%%4
      %%hole%%5 %%hole%%6 %%hole%%7 (vstd!seq.Seq.index.? %%hole%%1 %%hole%%2 %%hole%%3
       (I (EucDiv (%I i$) %%hole%%0))
      )
     ) (I (EucMod (%I i$) %%hole%%8))
   ))
   :pattern ((%%apply%%0 (%%lambda%%3 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3 %%hole%%4
      %%hole%%5 %%hole%%6 %%hole%%7 %%hole%%8 %%hole%%9 %%hole%%10
     ) i$
)))))
(assert
 (=>
  (fuel_bool fuel%det_harness!flatten_array_chunks.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (chunks! Poly)) (!
    (= (det_harness!flatten_array_chunks.? T&. T& N&. N& chunks!) (ite
      (= (const_int N&) 0)
      (vstd!seq.Seq.empty.? T&. T&)
      (vstd!seq.Seq.new.? T&. T& (I (nClip (Mul (vstd!seq.Seq.len.? $ (ARRAY T&. T& N&. N&)
           chunks!
          ) (const_int N&)
        ))
       ) (Poly%fun%1. (mk_fun (%%lambda%%3 (const_int N&) $ (ARRAY T&. T& N&. N&) chunks! T&.
          T& N&. N& (const_int N&) T&. T&
    ))))))
    :pattern ((det_harness!flatten_array_chunks.? T&. T& N&. N& chunks!))
    :qid internal_det_harness!flatten_array_chunks.?_definition
    :skolemid skolem_internal_det_harness!flatten_array_chunks.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (chunks! Poly)) (!
   (=>
    (has_type chunks! (TYPE%vstd!seq.Seq. $ (ARRAY T&. T& N&. N&)))
    (has_type (det_harness!flatten_array_chunks.? T&. T& N&. N& chunks!) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((det_harness!flatten_array_chunks.? T&. T& N&. N& chunks!))
   :qid internal_det_harness!flatten_array_chunks.?_pre_post_definition
   :skolemid skolem_internal_det_harness!flatten_array_chunks.?_pre_post_definition
)))

;; Function-Axioms det_harness::slice_array_chunks_partition
(assert
 (fuel_bool_default fuel%det_harness!slice_array_chunks_partition.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_array_chunks_partition.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly) (chunks! Poly) (remainder!
     Poly
    )
   ) (!
    (= (det_harness!slice_array_chunks_partition.? T&. T& N&. N& seq! chunks! remainder!)
     (and
      (and
       (not (= (const_int N&) 0))
       (< (vstd!seq.Seq.len.? T&. T& remainder!) (const_int N&))
      )
      (= (vstd!seq.Seq.add.? T&. T& (det_harness!flatten_array_chunks.? T&. T& N&. N& chunks!)
        remainder!
       ) seq!
    )))
    :pattern ((det_harness!slice_array_chunks_partition.? T&. T& N&. N& seq! chunks! remainder!))
    :qid internal_det_harness!slice_array_chunks_partition.?_definition
    :skolemid skolem_internal_det_harness!slice_array_chunks_partition.?_definition
))))

;; Function-Axioms det_harness::slice_array_rchunks_partition
(assert
 (fuel_bool_default fuel%det_harness!slice_array_rchunks_partition.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_array_rchunks_partition.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (seq! Poly) (remainder! Poly) (chunks!
     Poly
    )
   ) (!
    (= (det_harness!slice_array_rchunks_partition.? T&. T& N&. N& seq! remainder! chunks!)
     (and
      (and
       (not (= (const_int N&) 0))
       (< (vstd!seq.Seq.len.? T&. T& remainder!) (const_int N&))
      )
      (= (vstd!seq.Seq.add.? T&. T& remainder! (det_harness!flatten_array_chunks.? T&. T&
         N&. N& chunks!
        )
       ) seq!
    )))
    :pattern ((det_harness!slice_array_rchunks_partition.? T&. T& N&. N& seq! remainder!
      chunks!
    ))
    :qid internal_det_harness!slice_array_rchunks_partition.?_definition
    :skolemid skolem_internal_det_harness!slice_array_rchunks_partition.?_definition
))))

;; Function-Axioms det_harness::slice_raw_domain_valid
(assert
 (fuel_bool_default fuel%det_harness!slice_raw_domain_valid.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_raw_domain_valid.)
  (forall ((domain! Poly)) (!
    (= (det_harness!slice_raw_domain_valid.? domain!) (and
      (and
       (and
        (and
         (and
          (and
           (<= 0 (det_harness!SliceRawDomain./SliceRawDomain/len (%Poly%det_harness!SliceRawDomain.
              domain!
           )))
           (det_harness!SliceRawDomain./SliceRawDomain/non_null (%Poly%det_harness!SliceRawDomain.
             domain!
          )))
          (det_harness!SliceRawDomain./SliceRawDomain/aligned (%Poly%det_harness!SliceRawDomain.
            domain!
         )))
         (det_harness!SliceRawDomain./SliceRawDomain/one_allocation (%Poly%det_harness!SliceRawDomain.
           domain!
        )))
        (det_harness!SliceRawDomain./SliceRawDomain/initialized (%Poly%det_harness!SliceRawDomain.
          domain!
       )))
       (det_harness!SliceRawDomain./SliceRawDomain/aliasing_ok (%Poly%det_harness!SliceRawDomain.
         domain!
      )))
      (det_harness!SliceRawDomain./SliceRawDomain/within_isize (%Poly%det_harness!SliceRawDomain.
        domain!
    ))))
    :pattern ((det_harness!slice_raw_domain_valid.? domain!))
    :qid internal_det_harness!slice_raw_domain_valid.?_definition
    :skolemid skolem_internal_det_harness!slice_raw_domain_valid.?_definition
))))

;; Function-Axioms det_harness::slice_from_raw_parts_result
(assert
 (fuel_bool_default fuel%det_harness!slice_from_raw_parts_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_from_raw_parts_result.)
  (forall ((T&. Dcr) (T& Type) (ptr! Poly) (len! Poly) (ret! Poly)) (!
    (= (det_harness!slice_from_raw_parts_result.? T&. T& ptr! len! ret!) (and
      (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) ret!))
       (%I len!)
      )
      (det_harness!slice_start_ptr.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
        ret!
       ) ptr!
    )))
    :pattern ((det_harness!slice_from_raw_parts_result.? T&. T& ptr! len! ret!))
    :qid internal_det_harness!slice_from_raw_parts_result.?_definition
    :skolemid skolem_internal_det_harness!slice_from_raw_parts_result.?_definition
))))

;; Function-Axioms det_harness::slice_from_raw_parts_mut_result
(assert
 (fuel_bool_default fuel%det_harness!slice_from_raw_parts_mut_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_from_raw_parts_mut_result.)
  (forall ((T&. Dcr) (T& Type) (ptr! Poly) (len! Poly) (ret! Poly)) (!
    (= (det_harness!slice_from_raw_parts_mut_result.? T&. T& ptr! len! ret!) (and
      (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) (mut_ref_current%
          ret!
        ))
       ) (%I len!)
      )
      (det_harness!slice_start_mut_ptr.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
        (mut_ref_current% ret!)
       ) ptr!
    )))
    :pattern ((det_harness!slice_from_raw_parts_mut_result.? T&. T& ptr! len! ret!))
    :qid internal_det_harness!slice_from_raw_parts_mut_result.?_definition
    :skolemid skolem_internal_det_harness!slice_from_raw_parts_mut_result.?_definition
))))

;; Function-Axioms det_harness::slice_align_to_result
(assert
 (fuel_bool_default fuel%det_harness!slice_align_to_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_align_to_result.)
  (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (source! Poly) (prefix! Poly) (middle!
     Poly
    ) (suffix! Poly)
   ) (!
    (= (det_harness!slice_align_to_result.? T&. T& U&. U& source! prefix! middle! suffix!)
     (and
      (and
       (and
        (and
         (<= (vstd!seq.Seq.len.? T&. T& prefix!) (vstd!seq.Seq.len.? T&. T& source!))
         (<= (vstd!seq.Seq.len.? T&. T& suffix!) (vstd!seq.Seq.len.? T&. T& source!))
        )
        (= prefix! (vstd!seq.Seq.subrange.? T&. T& source! (I 0) (I (vstd!seq.Seq.len.? T&. T&
            prefix!
       )))))
       (= suffix! (vstd!seq.Seq.subrange.? T&. T& source! (I (Sub (vstd!seq.Seq.len.? T&. T&
            source!
           ) (vstd!seq.Seq.len.? T&. T& suffix!)
          )
         ) (I (vstd!seq.Seq.len.? T&. T& source!))
      )))
      (det_harness!slice_aligned_middle.? T&. T& U&. U& source! prefix! middle! suffix!)
    ))
    :pattern ((det_harness!slice_align_to_result.? T&. T& U&. U& source! prefix! middle!
      suffix!
    ))
    :qid internal_det_harness!slice_align_to_result.?_definition
    :skolemid skolem_internal_det_harness!slice_align_to_result.?_definition
))))

;; Function-Axioms det_harness::slice_align_to_mut_result
(assert
 (fuel_bool_default fuel%det_harness!slice_align_to_mut_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!slice_align_to_mut_result.)
  (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (old_source! Poly) (prefix! Poly)
    (middle! Poly) (suffix! Poly) (final_prefix! Poly) (final_middle! Poly) (final_suffix!
     Poly
    ) (final_source! Poly)
   ) (!
    (= (det_harness!slice_align_to_mut_result.? T&. T& U&. U& old_source! prefix! middle!
      suffix! final_prefix! final_middle! final_suffix! final_source!
     ) (and
      (and
       (and
        (and
         (det_harness!slice_align_to_result.? T&. T& U&. U& old_source! prefix! middle! suffix!)
         (= (vstd!seq.Seq.len.? T&. T& final_source!) (vstd!seq.Seq.len.? T&. T& old_source!))
        )
        (= (vstd!seq.Seq.len.? T&. T& final_prefix!) (vstd!seq.Seq.len.? T&. T& prefix!))
       )
       (= (vstd!seq.Seq.len.? U&. U& final_middle!) (vstd!seq.Seq.len.? U&. U& middle!))
      )
      (= (vstd!seq.Seq.len.? T&. T& final_suffix!) (vstd!seq.Seq.len.? T&. T& suffix!))
    ))
    :pattern ((det_harness!slice_align_to_mut_result.? T&. T& U&. U& old_source! prefix!
      middle! suffix! final_prefix! final_middle! final_suffix! final_source!
    ))
    :qid internal_det_harness!slice_align_to_mut_result.?_definition
    :skolemid skolem_internal_det_harness!slice_align_to_mut_result.?_definition
))))

;; Function-Axioms det_harness::maybe_uninit_relation_well_formed
(assert
 (fuel_bool_default fuel%det_harness!maybe_uninit_relation_well_formed.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!maybe_uninit_relation_well_formed.)
  (forall ((T&. Dcr) (T& Type) (relation! Poly) (len! Poly)) (!
    (= (det_harness!maybe_uninit_relation_well_formed.? T&. T& relation! len!) (and
      (and
       (<= 0 (%I len!))
       (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
           (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
         ))
        ) (%I len!)
      ))
      (= (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
         (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
        )
       ) (%I len!)
    )))
    :pattern ((det_harness!maybe_uninit_relation_well_formed.? T&. T& relation! len!))
    :qid internal_det_harness!maybe_uninit_relation_well_formed.?_definition
    :skolemid skolem_internal_det_harness!maybe_uninit_relation_well_formed.?_definition
))))

;; Function-Axioms det_harness::maybe_uninit_all_initialized
(assert
 (fuel_bool_default fuel%det_harness!maybe_uninit_all_initialized.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!maybe_uninit_all_initialized.)
  (forall ((T&. Dcr) (T& Type) (relation! Poly)) (!
    (= (det_harness!maybe_uninit_all_initialized.? T&. T& relation!) (and
      (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
          (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
        ))
       ) (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
         (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
      )))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
                  (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
             )))))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
              (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
             )
            ) i$
        ))))
        :pattern ((vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. relation!)
           )
          ) i$
        ))
        :qid user_det_harness__maybe_uninit_all_initialized_100
        :skolemid skolem_user_det_harness__maybe_uninit_all_initialized_100
    ))))
    :pattern ((det_harness!maybe_uninit_all_initialized.? T&. T& relation!))
    :qid internal_det_harness!maybe_uninit_all_initialized.?_definition
    :skolemid skolem_internal_det_harness!maybe_uninit_all_initialized.?_definition
))))

;; Function-Axioms det_harness::maybe_uninit_written_from
(assert
 (fuel_bool_default fuel%det_harness!maybe_uninit_written_from.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!maybe_uninit_written_from.)
  (forall ((T&. Dcr) (T& Type) (before! Poly) (after! Poly) (source! Poly)) (!
    (= (det_harness!maybe_uninit_written_from.? T&. T& before! after! source!) (and
      (and
       (and
        (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. before!)
          ))
         ) (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. after!)
        ))))
        (= (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
           (%Poly%det_harness!MaybeUninitSliceRelation. after!)
          )
         ) (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. after!)
       )))))
       (<= (vstd!seq.Seq.len.? T&. T& source!) (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
          (%Poly%det_harness!MaybeUninitSliceRelation. after!)
      ))))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& source!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (and
           (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
               (%Poly%det_harness!MaybeUninitSliceRelation. after!)
              )
             ) i$
           ))
           (= (vstd!seq.Seq.index.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
              (%Poly%det_harness!MaybeUninitSliceRelation. after!)
             ) i$
            ) (vstd!seq.Seq.index.? T&. T& source! i$)
        ))))
        :pattern ((vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. after!)
           )
          ) i$
        ))
        :pattern ((vstd!seq.Seq.index.? T&. T& source! i$))
        :qid user_det_harness__maybe_uninit_written_from_101
        :skolemid skolem_user_det_harness__maybe_uninit_written_from_101
    ))))
    :pattern ((det_harness!maybe_uninit_written_from.? T&. T& before! after! source!))
    :qid internal_det_harness!maybe_uninit_written_from.?_definition
    :skolemid skolem_internal_det_harness!maybe_uninit_written_from.?_definition
))))

;; Function-Axioms det_harness::maybe_uninit_drop_all
(assert
 (fuel_bool_default fuel%det_harness!maybe_uninit_drop_all.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!maybe_uninit_drop_all.)
  (forall ((T&. Dcr) (T& Type) (before! Poly) (after! Poly)) (!
    (= (det_harness!maybe_uninit_drop_all.? T&. T& before! after!) (and
      (and
       (= (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
           (%Poly%det_harness!MaybeUninitSliceRelation. before!)
         ))
        ) (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
           (%Poly%det_harness!MaybeUninitSliceRelation. after!)
       ))))
       (= (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
          (%Poly%det_harness!MaybeUninitSliceRelation. after!)
         )
        ) (vstd!seq.Seq.len.? T&. T& (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/values
          (%Poly%det_harness!MaybeUninitSliceRelation. before!)
      ))))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
                  (%Poly%det_harness!MaybeUninitSliceRelation. after!)
             )))))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (not (%B (vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
               (%Poly%det_harness!MaybeUninitSliceRelation. after!)
              )
             ) i$
        )))))
        :pattern ((vstd!seq.Seq.index.? $ BOOL (Poly%vstd!seq.Seq<bool.>. (det_harness!MaybeUninitSliceRelation./MaybeUninitSliceRelation/initialized
            (%Poly%det_harness!MaybeUninitSliceRelation. after!)
           )
          ) i$
        ))
        :qid user_det_harness__maybe_uninit_drop_all_102
        :skolemid skolem_user_det_harness__maybe_uninit_drop_all_102
    ))))
    :pattern ((det_harness!maybe_uninit_drop_all.? T&. T& before! after!))
    :qid internal_det_harness!maybe_uninit_drop_all.?_definition
    :skolemid skolem_internal_det_harness!maybe_uninit_drop_all.?_definition
))))

;; Function-Axioms det_harness::ascii_is_uppercase
(assert
 (fuel_bool_default fuel%det_harness!ascii_is_uppercase.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_is_uppercase.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_is_uppercase.? byte!) (and
      (<= 65 (%I byte!))
      (<= (%I byte!) 90)
    ))
    :pattern ((det_harness!ascii_is_uppercase.? byte!))
    :qid internal_det_harness!ascii_is_uppercase.?_definition
    :skolemid skolem_internal_det_harness!ascii_is_uppercase.?_definition
))))

;; Function-Axioms det_harness::ascii_is_lowercase
(assert
 (fuel_bool_default fuel%det_harness!ascii_is_lowercase.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_is_lowercase.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_is_lowercase.? byte!) (and
      (<= 97 (%I byte!))
      (<= (%I byte!) 122)
    ))
    :pattern ((det_harness!ascii_is_lowercase.? byte!))
    :qid internal_det_harness!ascii_is_lowercase.?_definition
    :skolemid skolem_internal_det_harness!ascii_is_lowercase.?_definition
))))

;; Function-Axioms det_harness::ascii_lower_byte
(assert
 (fuel_bool_default fuel%det_harness!ascii_lower_byte.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_lower_byte.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_lower_byte.? byte!) (ite
      (det_harness!ascii_is_uppercase.? byte!)
      (uClip 8 (Add (%I byte!) 32))
      (%I byte!)
    ))
    :pattern ((det_harness!ascii_lower_byte.? byte!))
    :qid internal_det_harness!ascii_lower_byte.?_definition
    :skolemid skolem_internal_det_harness!ascii_lower_byte.?_definition
))))
(assert
 (forall ((byte! Poly)) (!
   (=>
    (has_type byte! (UINT 8))
    (uInv 8 (det_harness!ascii_lower_byte.? byte!))
   )
   :pattern ((det_harness!ascii_lower_byte.? byte!))
   :qid internal_det_harness!ascii_lower_byte.?_pre_post_definition
   :skolemid skolem_internal_det_harness!ascii_lower_byte.?_pre_post_definition
)))

;; Function-Axioms det_harness::ascii_upper_byte
(assert
 (fuel_bool_default fuel%det_harness!ascii_upper_byte.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_upper_byte.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_upper_byte.? byte!) (ite
      (det_harness!ascii_is_lowercase.? byte!)
      (uClip 8 (Sub (%I byte!) 32))
      (%I byte!)
    ))
    :pattern ((det_harness!ascii_upper_byte.? byte!))
    :qid internal_det_harness!ascii_upper_byte.?_definition
    :skolemid skolem_internal_det_harness!ascii_upper_byte.?_definition
))))
(assert
 (forall ((byte! Poly)) (!
   (=>
    (has_type byte! (UINT 8))
    (uInv 8 (det_harness!ascii_upper_byte.? byte!))
   )
   :pattern ((det_harness!ascii_upper_byte.? byte!))
   :qid internal_det_harness!ascii_upper_byte.?_pre_post_definition
   :skolemid skolem_internal_det_harness!ascii_upper_byte.?_pre_post_definition
)))

;; Function-Axioms det_harness::ascii_is_byte
(assert
 (fuel_bool_default fuel%det_harness!ascii_is_byte.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_is_byte.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_is_byte.? byte!) (<= (%I byte!) 127))
    :pattern ((det_harness!ascii_is_byte.? byte!))
    :qid internal_det_harness!ascii_is_byte.?_definition
    :skolemid skolem_internal_det_harness!ascii_is_byte.?_definition
))))

;; Function-Axioms det_harness::ascii_is_whitespace
(assert
 (fuel_bool_default fuel%det_harness!ascii_is_whitespace.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_is_whitespace.)
  (forall ((byte! Poly)) (!
    (= (det_harness!ascii_is_whitespace.? byte!) (or
      (or
       (or
        (or
         (or
          (= (%I byte!) 9)
          (= (%I byte!) 10)
         )
         (= (%I byte!) 11)
        )
        (= (%I byte!) 12)
       )
       (= (%I byte!) 13)
      )
      (= (%I byte!) 32)
    ))
    :pattern ((det_harness!ascii_is_whitespace.? byte!))
    :qid internal_det_harness!ascii_is_whitespace.?_definition
    :skolemid skolem_internal_det_harness!ascii_is_whitespace.?_definition
))))

;; Function-Axioms det_harness::ascii_all
(assert
 (fuel_bool_default fuel%det_harness!ascii_all.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_all.)
  (forall ((seq! Poly)) (!
    (= (det_harness!ascii_all.? seq!) (forall ((i$ Poly)) (!
       (=>
        (has_type i$ INT)
        (=>
         (let
          ((tmp%%$ 0))
          (let
           ((tmp%%$1 (%I i$)))
           (let
            ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
            (and
             (<= tmp%%$ tmp%%$1)
             (< tmp%%$1 tmp%%$2)
         ))))
         (det_harness!ascii_is_byte.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
       ))
       :pattern ((vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
       :qid user_det_harness__ascii_all_103
       :skolemid skolem_user_det_harness__ascii_all_103
    )))
    :pattern ((det_harness!ascii_all.? seq!))
    :qid internal_det_harness!ascii_all.?_definition
    :skolemid skolem_internal_det_harness!ascii_all.?_definition
))))

;; Function-Axioms det_harness::ascii_lower_seq
(assert
 (fuel_bool_default fuel%det_harness!ascii_lower_seq.)
)
(declare-fun %%lambda%%4 (Dcr Type Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Dcr) (%%hole%%1 Type) (%%hole%%2 Poly) (i$ Poly)) (!
   (= (%%apply%%0 (%%lambda%%4 %%hole%%0 %%hole%%1 %%hole%%2) i$) (I (det_harness!ascii_lower_byte.?
      (vstd!seq.Seq.index.? %%hole%%0 %%hole%%1 %%hole%%2 i$)
   )))
   :pattern ((%%apply%%0 (%%lambda%%4 %%hole%%0 %%hole%%1 %%hole%%2) i$))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_lower_seq.)
  (forall ((seq! Poly)) (!
    (= (det_harness!ascii_lower_seq.? seq!) (%Poly%vstd!seq.Seq<u8.>. (vstd!seq.Seq.new.?
       $ (UINT 8) (I (vstd!seq.Seq.len.? $ (UINT 8) seq!)) (Poly%fun%1. (mk_fun (%%lambda%%4
          $ (UINT 8) seq!
    ))))))
    :pattern ((det_harness!ascii_lower_seq.? seq!))
    :qid internal_det_harness!ascii_lower_seq.?_definition
    :skolemid skolem_internal_det_harness!ascii_lower_seq.?_definition
))))

;; Function-Axioms det_harness::ascii_upper_seq
(assert
 (fuel_bool_default fuel%det_harness!ascii_upper_seq.)
)
(declare-fun %%lambda%%5 (Dcr Type Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Dcr) (%%hole%%1 Type) (%%hole%%2 Poly) (i$ Poly)) (!
   (= (%%apply%%0 (%%lambda%%5 %%hole%%0 %%hole%%1 %%hole%%2) i$) (I (det_harness!ascii_upper_byte.?
      (vstd!seq.Seq.index.? %%hole%%0 %%hole%%1 %%hole%%2 i$)
   )))
   :pattern ((%%apply%%0 (%%lambda%%5 %%hole%%0 %%hole%%1 %%hole%%2) i$))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_upper_seq.)
  (forall ((seq! Poly)) (!
    (= (det_harness!ascii_upper_seq.? seq!) (%Poly%vstd!seq.Seq<u8.>. (vstd!seq.Seq.new.?
       $ (UINT 8) (I (vstd!seq.Seq.len.? $ (UINT 8) seq!)) (Poly%fun%1. (mk_fun (%%lambda%%5
          $ (UINT 8) seq!
    ))))))
    :pattern ((det_harness!ascii_upper_seq.? seq!))
    :qid internal_det_harness!ascii_upper_seq.?_definition
    :skolemid skolem_internal_det_harness!ascii_upper_seq.?_definition
))))

;; Function-Axioms det_harness::ascii_eq_ignore_case
(assert
 (fuel_bool_default fuel%det_harness!ascii_eq_ignore_case.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_eq_ignore_case.)
  (forall ((left! Poly) (right! Poly)) (!
    (= (det_harness!ascii_eq_ignore_case.? left! right!) (and
      (= (vstd!seq.Seq.len.? $ (UINT 8) left!) (vstd!seq.Seq.len.? $ (UINT 8) right!))
      (forall ((i$ Poly)) (!
        (=>
         (has_type i$ INT)
         (=>
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 (%I i$)))
            (let
             ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) left!)))
             (and
              (<= tmp%%$ tmp%%$1)
              (< tmp%%$1 tmp%%$2)
          ))))
          (= (det_harness!ascii_lower_byte.? (vstd!seq.Seq.index.? $ (UINT 8) left! i$)) (det_harness!ascii_lower_byte.?
            (vstd!seq.Seq.index.? $ (UINT 8) right! i$)
        ))))
        :pattern ((vstd!seq.Seq.index.? $ (UINT 8) left! i$))
        :pattern ((vstd!seq.Seq.index.? $ (UINT 8) right! i$))
        :qid user_det_harness__ascii_eq_ignore_case_104
        :skolemid skolem_user_det_harness__ascii_eq_ignore_case_104
    ))))
    :pattern ((det_harness!ascii_eq_ignore_case.? left! right!))
    :qid internal_det_harness!ascii_eq_ignore_case.?_definition
    :skolemid skolem_internal_det_harness!ascii_eq_ignore_case.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_start_boundary
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_start_boundary.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_start_boundary.)
  (forall ((seq! Poly) (i! Poly)) (!
    (= (det_harness!ascii_trim_start_boundary.? seq! i!) (and
      (and
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (<= tmp%%$1 tmp%%$2)
       ))))
       (forall ((j$ Poly)) (!
         (=>
          (has_type j$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$4 (%I j$)))
             (let
              ((tmp%%$5 (%I i!)))
              (and
               (<= tmp%%$ tmp%%$4)
               (< tmp%%$4 tmp%%$5)
           ))))
           (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! j$))
         ))
         :pattern ((det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! j$)))
         :qid user_det_harness__ascii_trim_start_boundary_105
         :skolemid skolem_user_det_harness__ascii_trim_start_boundary_105
      )))
      (=>
       (< (%I i!) (vstd!seq.Seq.len.? $ (UINT 8) seq!))
       (not (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i!)))
    )))
    :pattern ((det_harness!ascii_trim_start_boundary.? seq! i!))
    :qid internal_det_harness!ascii_trim_start_boundary.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_start_boundary.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_end_boundary
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_end_boundary.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_end_boundary.)
  (forall ((seq! Poly) (i! Poly)) (!
    (= (det_harness!ascii_trim_end_boundary.? seq! i!) (and
      (and
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (<= tmp%%$1 tmp%%$2)
       ))))
       (forall ((j$ Poly)) (!
         (=>
          (has_type j$ INT)
          (=>
           (let
            ((tmp%%$ (%I i!)))
            (let
             ((tmp%%$4 (%I j$)))
             (let
              ((tmp%%$5 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
              (and
               (<= tmp%%$ tmp%%$4)
               (< tmp%%$4 tmp%%$5)
           ))))
           (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! j$))
         ))
         :pattern ((det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! j$)))
         :qid user_det_harness__ascii_trim_end_boundary_106
         :skolemid skolem_user_det_harness__ascii_trim_end_boundary_106
      )))
      (=>
       (< 0 (%I i!))
       (not (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! (I (Sub
            (%I i!) 1
    ))))))))
    :pattern ((det_harness!ascii_trim_end_boundary.? seq! i!))
    :qid internal_det_harness!ascii_trim_end_boundary.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_end_boundary.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_start_index
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_start_index.)
)
(declare-fun %%choose%%0 (Type Poly Poly) Poly)
(assert
 (forall ((%%hole%%0 Type) (%%hole%%1 Poly) (%%hole%%2 Poly)) (!
   (=>
    (exists ((i$ Poly)) (!
      (and
       (has_type i$ %%hole%%0)
       (det_harness!ascii_trim_start_boundary.? %%hole%%1 i$)
      )
      :pattern ((det_harness!ascii_trim_start_boundary.? %%hole%%2 i$))
      :qid user_det_harness__ascii_trim_start_index_107
      :skolemid skolem_user_det_harness__ascii_trim_start_index_107
    ))
    (exists ((i$ Poly)) (!
      (and
       (and
        (has_type i$ %%hole%%0)
        (det_harness!ascii_trim_start_boundary.? %%hole%%1 i$)
       )
       (= (%%choose%%0 %%hole%%0 %%hole%%1 %%hole%%2) i$)
      )
      :pattern ((det_harness!ascii_trim_start_boundary.? %%hole%%2 i$))
   )))
   :pattern ((%%choose%%0 %%hole%%0 %%hole%%1 %%hole%%2))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_start_index.)
  (forall ((seq! Poly)) (!
    (= (det_harness!ascii_trim_start_index.? seq!) (%I (as_type (%%choose%%0 INT seq! seq!)
       INT
    )))
    :pattern ((det_harness!ascii_trim_start_index.? seq!))
    :qid internal_det_harness!ascii_trim_start_index.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_start_index.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_end_index
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_end_index.)
)
(declare-fun %%choose%%1 (Type Poly Poly) Poly)
(assert
 (forall ((%%hole%%0 Type) (%%hole%%1 Poly) (%%hole%%2 Poly)) (!
   (=>
    (exists ((i$ Poly)) (!
      (and
       (has_type i$ %%hole%%0)
       (det_harness!ascii_trim_end_boundary.? %%hole%%1 i$)
      )
      :pattern ((det_harness!ascii_trim_end_boundary.? %%hole%%2 i$))
      :qid user_det_harness__ascii_trim_end_index_108
      :skolemid skolem_user_det_harness__ascii_trim_end_index_108
    ))
    (exists ((i$ Poly)) (!
      (and
       (and
        (has_type i$ %%hole%%0)
        (det_harness!ascii_trim_end_boundary.? %%hole%%1 i$)
       )
       (= (%%choose%%1 %%hole%%0 %%hole%%1 %%hole%%2) i$)
      )
      :pattern ((det_harness!ascii_trim_end_boundary.? %%hole%%2 i$))
   )))
   :pattern ((%%choose%%1 %%hole%%0 %%hole%%1 %%hole%%2))
)))
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_end_index.)
  (forall ((seq! Poly)) (!
    (= (det_harness!ascii_trim_end_index.? seq!) (%I (as_type (%%choose%%1 INT seq! seq!)
       INT
    )))
    :pattern ((det_harness!ascii_trim_end_index.? seq!))
    :qid internal_det_harness!ascii_trim_end_index.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_end_index.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_start_result
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_start_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_start_result.)
  (forall ((seq! Poly) (ret! Poly)) (!
    (= (det_harness!ascii_trim_start_result.? seq! ret!) (and
      (and
       (and
        (let
         ((tmp%%$ 0))
         (let
          ((tmp%%$1 (det_harness!ascii_trim_start_index.? seq!)))
          (let
           ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
           (and
            (<= tmp%%$ tmp%%$1)
            (<= tmp%%$1 tmp%%$2)
        ))))
        (= (vstd!view.View.view.? $slice (SLICE $ (UINT 8)) ret!) (vstd!seq.Seq.subrange.?
          $ (UINT 8) seq! (I (det_harness!ascii_trim_start_index.? seq!)) (I (vstd!seq.Seq.len.?
            $ (UINT 8) seq!
       )))))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ 0))
            (let
             ((tmp%%$4 (%I i$)))
             (let
              ((tmp%%$5 (det_harness!ascii_trim_start_index.? seq!)))
              (and
               (<= tmp%%$ tmp%%$4)
               (< tmp%%$4 tmp%%$5)
           ))))
           (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
         ))
         :pattern ((vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
         :qid user_det_harness__ascii_trim_start_result_109
         :skolemid skolem_user_det_harness__ascii_trim_start_result_109
      )))
      (=>
       (< (det_harness!ascii_trim_start_index.? seq!) (vstd!seq.Seq.len.? $ (UINT 8) seq!))
       (not (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! (I (det_harness!ascii_trim_start_index.?
            seq!
    ))))))))
    :pattern ((det_harness!ascii_trim_start_result.? seq! ret!))
    :qid internal_det_harness!ascii_trim_start_result.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_start_result.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_end_result
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_end_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_end_result.)
  (forall ((seq! Poly) (ret! Poly)) (!
    (= (det_harness!ascii_trim_end_result.? seq! ret!) (and
      (and
       (and
        (let
         ((tmp%%$ 0))
         (let
          ((tmp%%$1 (det_harness!ascii_trim_end_index.? seq!)))
          (let
           ((tmp%%$2 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
           (and
            (<= tmp%%$ tmp%%$1)
            (<= tmp%%$1 tmp%%$2)
        ))))
        (= (vstd!view.View.view.? $slice (SLICE $ (UINT 8)) ret!) (vstd!seq.Seq.subrange.?
          $ (UINT 8) seq! (I 0) (I (det_harness!ascii_trim_end_index.? seq!))
       )))
       (forall ((i$ Poly)) (!
         (=>
          (has_type i$ INT)
          (=>
           (let
            ((tmp%%$ (det_harness!ascii_trim_end_index.? seq!)))
            (let
             ((tmp%%$4 (%I i$)))
             (let
              ((tmp%%$5 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
              (and
               (<= tmp%%$ tmp%%$4)
               (< tmp%%$4 tmp%%$5)
           ))))
           (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
         ))
         :pattern ((vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
         :qid user_det_harness__ascii_trim_end_result_110
         :skolemid skolem_user_det_harness__ascii_trim_end_result_110
      )))
      (=>
       (< 0 (det_harness!ascii_trim_end_index.? seq!))
       (not (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! (I (Sub
            (det_harness!ascii_trim_end_index.? seq!) 1
    ))))))))
    :pattern ((det_harness!ascii_trim_end_result.? seq! ret!))
    :qid internal_det_harness!ascii_trim_end_result.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_end_result.?_definition
))))

;; Function-Axioms det_harness::ascii_trim_result
(assert
 (fuel_bool_default fuel%det_harness!ascii_trim_result.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!ascii_trim_result.)
  (forall ((seq! Poly) (ret! Poly)) (!
    (= (det_harness!ascii_trim_result.? seq! ret!) (let
      ((start$ (det_harness!ascii_trim_start_index.? seq!)))
      (let
       ((end$ (det_harness!ascii_trim_end_index.? seq!)))
       (and
        (and
         (and
          (let
           ((tmp%%$ 0))
           (let
            ((tmp%%$1 start$))
            (let
             ((tmp%%$2 end$))
             (let
              ((tmp%%$3 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
              (and
               (and
                (<= tmp%%$ tmp%%$1)
                (<= tmp%%$1 tmp%%$2)
               )
               (<= tmp%%$2 tmp%%$3)
          )))))
          (= (vstd!view.View.view.? $slice (SLICE $ (UINT 8)) ret!) (vstd!seq.Seq.subrange.?
            $ (UINT 8) seq! (I start$) (I end$)
         )))
         (forall ((i$ Poly)) (!
           (=>
            (has_type i$ INT)
            (=>
             (let
              ((tmp%%$ 0))
              (let
               ((tmp%%$5 (%I i$)))
               (let
                ((tmp%%$6 start$))
                (and
                 (<= tmp%%$ tmp%%$5)
                 (< tmp%%$5 tmp%%$6)
             ))))
             (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
           ))
           :pattern ((vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
           :qid user_det_harness__ascii_trim_result_111
           :skolemid skolem_user_det_harness__ascii_trim_result_111
        )))
        (forall ((i$ Poly)) (!
          (=>
           (has_type i$ INT)
           (=>
            (let
             ((tmp%%$ end$))
             (let
              ((tmp%%$8 (%I i$)))
              (let
               ((tmp%%$9 (vstd!seq.Seq.len.? $ (UINT 8) seq!)))
               (and
                (<= tmp%%$ tmp%%$8)
                (< tmp%%$8 tmp%%$9)
            ))))
            (det_harness!ascii_is_whitespace.? (vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
          ))
          :pattern ((vstd!seq.Seq.index.? $ (UINT 8) seq! i$))
          :qid user_det_harness__ascii_trim_result_112
          :skolemid skolem_user_det_harness__ascii_trim_result_112
    ))))))
    :pattern ((det_harness!ascii_trim_result.? seq! ret!))
    :qid internal_det_harness!ascii_trim_result.?_definition
    :skolemid skolem_internal_det_harness!ascii_trim_result.?_definition
))))

;; Function-Axioms det_harness::det___rust_std_candidate_equal
(assert
 (fuel_bool_default fuel%det_harness!det___rust_std_candidate_equal.)
)
(assert
 (=>
  (fuel_bool fuel%det_harness!det___rust_std_candidate_equal.)
  (forall ((T&. Dcr) (T& Type) (r1! Poly) (r2! Poly)) (!
    (= (det_harness!det___rust_std_candidate_equal.? T&. T& r1! r2!) (and
      (= (is-core!option.Option./Some (%Poly%core!option.Option. r1!)) (is-core!option.Option./Some
        (%Poly%core!option.Option. r2!)
      ))
      (=>
       (is-core!option.Option./Some (%Poly%core!option.Option. r1!))
       (and
        (= (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
            (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
             r1!
          )))
         ) (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
            (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
             r2!
        )))))
        (ext_eq false (SLICE T&. T&) (tuple%2./tuple%2/1 (%Poly%tuple%2. (core!option.Option./Some/0
            (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
             r1!
          )))
         ) (tuple%2./tuple%2/1 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
            (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
             r2!
    )))))))))
    :pattern ((det_harness!det___rust_std_candidate_equal.? T&. T& r1! r2!))
    :qid internal_det_harness!det___rust_std_candidate_equal.?_definition
    :skolemid skolem_internal_det_harness!det___rust_std_candidate_equal.?_definition
))))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%vstd!view.View. (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%vstd!view.View. (CONST_PTR $) (PTR T&. T&)))
   :qid internal_vstd__raw_ptr__impl&__3_trait_impl_definition
   :skolemid skolem_internal_vstd__raw_ptr__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (tr_bound%vstd!view.View. (REF A&.) A&)
   )
   :pattern ((tr_bound%vstd!view.View. (REF A&.) A&))
   :qid internal_vstd__view__impl&__0_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (tr_bound%vstd!view.View. (BOX $ TYPE%alloc!alloc.Global. A&.) A&)
   )
   :pattern ((tr_bound%vstd!view.View. (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_vstd__view__impl&__2_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (tr_bound%vstd!view.View. (RC $ TYPE%alloc!alloc.Global. A&.) A&)
   )
   :pattern ((tr_bound%vstd!view.View. (RC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_vstd__view__impl&__4_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%vstd!view.View. A&. A&)
    )
    (tr_bound%vstd!view.View. (ARC $ TYPE%alloc!alloc.Global. A&.) A&)
   )
   :pattern ((tr_bound%vstd!view.View. (ARC $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_vstd__view__impl&__6_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__6_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%vstd!view.View. $ (TYPE%core!option.Option. T&. T&))
   )
   :pattern ((tr_bound%vstd!view.View. $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_vstd__view__impl&__14_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__14_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (forall ((A0&. Dcr) (A0& Type)) (!
   (=>
    (and
     (sized A0&.)
     (tr_bound%vstd!view.View. A0&. A0&)
    )
    (tr_bound%vstd!view.View. (DST A0&.) (TYPE%tuple%1. A0&. A0&))
   )
   :pattern ((tr_bound%vstd!view.View. (DST A0&.) (TYPE%tuple%1. A0&. A0&)))
   :qid internal_vstd__view__impl&__46_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__46_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A0&. Dcr) (A0& Type) (A1&. Dcr) (A1& Type)) (!
   (=>
    (and
     (sized A0&.)
     (sized A1&.)
     (tr_bound%vstd!view.View. A0&. A0&)
     (tr_bound%vstd!view.View. A1&. A1&)
    )
    (tr_bound%vstd!view.View. (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&))
   )
   :pattern ((tr_bound%vstd!view.View. (DST A1&.) (TYPE%tuple%2. A0&. A0& A1&. A1&)))
   :qid internal_vstd__view__impl&__48_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__48_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!clone.Clone. (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!clone.Clone. (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__15_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__15_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!clone.Clone. (BOX A&. A& $slice) (SLICE T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. (BOX A&. A& $slice) (SLICE T&. T&)))
   :qid internal_alloc__boxed__impl&__16_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__16_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. (BOX $ TYPE%alloc!alloc.Global. $slice) STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&.
      T&
   )))
   :qid internal_core__mem__maybe_uninit__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__mem__maybe_uninit__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!clone.Clone. (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!clone.Clone. (CONST_PTR $) (PTR T&. T&)))
   :qid internal_core__clone__impls__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!clone.Clone. $ (PTR T&. T&))
   :pattern ((tr_bound%core!clone.Clone. $ (PTR T&. T&)))
   :qid internal_core__clone__impls__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!clone.Clone. (REF T&.) T&)
   :pattern ((tr_bound%core!clone.Clone. (REF T&.) T&))
   :qid internal_core__clone__impls__impl&__6_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__6_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!clone.Clone. Idx&. Idx&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!ops.range.Range. Idx&. Idx&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!ops.range.Range. Idx&. Idx&)))
   :qid internal_core__ops__range__impl&__49_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__49_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!ops.range.Bound. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!ops.range.Bound. T&. T&)))
   :qid internal_core__ops__range__impl&__78_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__78_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!clone.Clone. $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (ARRAY T&. T& N&. N&)))
   :qid internal_core__array__impl&__20_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__20_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!clone.Clone. E&. E&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!result.Result. T&. T& E&. E&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!result.Result. T&. T& E&. E&)))
   :qid internal_core__result__impl&__5_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__5_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%alloc!alloc.Global.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!clone.Clone. (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!clone.Clone. (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__35_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__35_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!clone.Clone. (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!clone.Clone. (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__32_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__32_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (sized A&.)
    (tr_bound%core!clone.Clone. (GHOST A&.) A&)
   )
   :pattern ((tr_bound%core!clone.Clone. (GHOST A&.) A&))
   :qid internal_verus_builtin__impl&__7_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__7_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Copy. A&. A&)
    )
    (tr_bound%core!clone.Clone. (TRACKED A&.) A&)
   )
   :pattern ((tr_bound%core!clone.Clone. (TRACKED A&.) A&))
   :qid internal_verus_builtin__impl&__9_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__9_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $slice STRSLICE $slice STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialEq. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialEq. (REF A&.) A& (REF B&.) B&)
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (REF A&.) A& (REF B&.) B&))
   :qid internal_core__cmp__impls__impl&__9_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__9_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialEq. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialEq. (REF A&.) A& $ (MUTREF B&. B&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (REF A&.) A& $ (MUTREF B&. B&)))
   :qid internal_core__cmp__impls__impl&__17_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__17_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. (REF $slice) (SLICE T&. T&) $ (ARRAY U&. U& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (REF $slice) (SLICE T&. T&) $ (ARRAY U&. U&
      N&. N&
   )))
   :qid internal_core__array__equality__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.PartialEq. (CONST_PTR $) (PTR T&. T&) (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.PartialEq. (CONST_PTR $) (PTR T&. T&) (CONST_PTR $) (PTR
      T&. T&
   )))
   :qid internal_core__ptr__const_ptr__impl&__7_trait_impl_definition
   :skolemid skolem_internal_core__ptr__const_ptr__impl&__7_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.PartialEq. $ (PTR T&. T&) $ (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (PTR T&. T&) $ (PTR T&. T&)))
   :qid internal_core__ptr__mut_ptr__impl&__7_trait_impl_definition
   :skolemid skolem_internal_core__ptr__mut_ptr__impl&__7_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ TYPE%core!cmp.Ordering. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ TYPE%tuple%0. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ BOOL $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ CHAR $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ USIZE $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ (UINT 8) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialEq. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialEq. $ (MUTREF A&. A&) $ (MUTREF B&. B&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (MUTREF A&. A&) $ (MUTREF B&. B&)))
   :qid internal_core__cmp__impls__impl&__13_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__13_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialEq. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialEq. $ (MUTREF A&. A&) (REF B&.) B&)
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (MUTREF A&. A&) (REF B&.) B&))
   :qid internal_core__cmp__impls__impl&__18_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__18_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $ (MUTREF $slice (SLICE T&. T&)) $ (ARRAY U&. U& N&.
      N&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (MUTREF $slice (SLICE T&. T&)) $ (ARRAY U&.
      U& N&. N&
   )))
   :qid internal_core__array__equality__impl&__6_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__6_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!cmp.PartialEq. Idx&. Idx& Idx&. Idx&)
    )
    (tr_bound%core!cmp.PartialEq. $ (TYPE%core!ops.range.Range. Idx&. Idx&) $ (TYPE%core!ops.range.Range.
      Idx&. Idx&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (TYPE%core!ops.range.Range. Idx&. Idx&) $
     (TYPE%core!ops.range.Range. Idx&. Idx&)
   ))
   :qid internal_core__ops__range__impl&__52_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__52_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialEq. $ (TYPE%core!ops.range.Bound. T&. T&) $ (TYPE%core!ops.range.Bound.
      T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (TYPE%core!ops.range.Bound. T&. T&) $ (TYPE%core!ops.range.Bound.
      T&. T&
   )))
   :qid internal_core__ops__range__impl&__81_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__81_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $ (ARRAY U&. U& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $ (ARRAY U&. U& N&.
      N&
   )))
   :qid internal_core__array__equality__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $slice (SLICE U&. U&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $slice (SLICE U&. U&)))
   :qid internal_core__array__equality__impl&__1_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) (REF $slice) (SLICE U&. U&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) (REF $slice) (SLICE
      U&. U&
   )))
   :qid internal_core__array__equality__impl&__3_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $ (MUTREF $slice (SLICE U&. U&)))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $ (ARRAY T&. T& N&. N&) $ (MUTREF $slice (SLICE
       U&. U&
   ))))
   :qid internal_core__array__equality__impl&__5_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__5_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $slice (SLICE T&. T&) $ (ARRAY U&. U& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $slice (SLICE T&. T&) $ (ARRAY U&. U& N&. N&)))
   :qid internal_core__array__equality__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (U&. Dcr) (U& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized U&.)
     (tr_bound%core!cmp.PartialEq. T&. T& U&. U&)
    )
    (tr_bound%core!cmp.PartialEq. $slice (SLICE T&. T&) $slice (SLICE U&. U&))
   )
   :pattern ((tr_bound%core!cmp.PartialEq. $slice (SLICE T&. T&) $slice (SLICE U&. U&)))
   :qid internal_core__slice__cmp__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__slice__cmp__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialEq. $ (TYPE%core!option.Option. T&. T&) $ (TYPE%core!option.Option.
      T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (TYPE%core!option.Option. T&. T&) $ (TYPE%core!option.Option.
      T&. T&
   )))
   :qid internal_core__option__impl&__17_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__17_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
     (tr_bound%core!cmp.PartialEq. E&. E& E&. E&)
    )
    (tr_bound%core!cmp.PartialEq. $ (TYPE%core!result.Result. T&. T& E&. E&) $ (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (TYPE%core!result.Result. T&. T& E&. E&)
     $ (TYPE%core!result.Result. T&. T& E&. E&)
   ))
   :qid internal_core__result__impl&__34_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__34_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialEq. (DST T&.) (TYPE%tuple%1. T&. T&) (DST T&.) (TYPE%tuple%1.
      T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. (DST T&.) (TYPE%tuple%1. T&. T&) (DST T&.)
     (TYPE%tuple%1. T&. T&)
   ))
   :qid internal_core__tuple__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((U&. Dcr) (U& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized U&.)
     (sized T&.)
     (tr_bound%core!cmp.PartialEq. U&. U& U&. U&)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialEq. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&) (DST T&.) (TYPE%tuple%2.
      U&. U& T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&) (DST
      T&.
     ) (TYPE%tuple%2. U&. U& T&. T&)
   ))
   :qid internal_core__tuple__impl&__10_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialEq. (BOX A&. A& T&.) T& (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (BOX A&. A& T&.) T& (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__18_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__18_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialEq. (RC A&. A& T&.) T& (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (RC A&. A& T&.) T& (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__44_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__44_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialEq. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialEq. (ARC A&. A& T&.) T& (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialEq. (ARC A&. A& T&.) T& (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__54_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__54_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ INT $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ NAT $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.Eq. (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.Eq. (CONST_PTR $) (PTR T&. T&)))
   :qid internal_core__ptr__const_ptr__impl&__8_trait_impl_definition
   :skolemid skolem_internal_core__ptr__const_ptr__impl&__8_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.Eq. $ (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.Eq. $ (PTR T&. T&)))
   :qid internal_core__ptr__mut_ptr__impl&__8_trait_impl_definition
   :skolemid skolem_internal_core__ptr__mut_ptr__impl&__8_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!cmp.Eq. A&. A&)
    (tr_bound%core!cmp.Eq. (REF A&.) A&)
   )
   :pattern ((tr_bound%core!cmp.Eq. (REF A&.) A&))
   :qid internal_core__cmp__impls__impl&__12_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__12_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!cmp.Eq. A&. A&)
    (tr_bound%core!cmp.Eq. $ (MUTREF A&. A&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (MUTREF A&. A&)))
   :qid internal_core__cmp__impls__impl&__16_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__16_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!cmp.Eq. Idx&. Idx&)
    )
    (tr_bound%core!cmp.Eq. $ (TYPE%core!ops.range.Range. Idx&. Idx&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (TYPE%core!ops.range.Range. Idx&. Idx&)))
   :qid internal_core__ops__range__impl&__47_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__47_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. $ (TYPE%core!ops.range.Bound. T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (TYPE%core!ops.range.Bound. T&. T&)))
   :qid internal_core__ops__range__impl&__79_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__79_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (ARRAY T&. T& N&. N&)))
   :qid internal_core__array__equality__impl&__7_trait_impl_definition
   :skolemid skolem_internal_core__array__equality__impl&__7_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. $ (TYPE%core!option.Option. T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_core__option__impl&__57_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__57_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!cmp.Eq. T&. T&)
     (tr_bound%core!cmp.Eq. E&. E&)
    )
    (tr_bound%core!cmp.Eq. $ (TYPE%core!result.Result. T&. T& E&. E&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (TYPE%core!result.Result. T&. T& E&. E&)))
   :qid internal_core__result__impl&__36_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__36_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. $slice (SLICE T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $slice (SLICE T&. T&)))
   :qid internal_core__slice__cmp__impl&__1_trait_impl_definition
   :skolemid skolem_internal_core__slice__cmp__impl&__1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $slice STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. (DST T&.) (TYPE%tuple%1. T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Eq. (DST T&.) (TYPE%tuple%1. T&. T&)))
   :qid internal_core__tuple__impl&__1_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((U&. Dcr) (U& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized U&.)
     (sized T&.)
     (tr_bound%core!cmp.Eq. U&. U&)
     (tr_bound%core!cmp.Eq. T&. T&)
    )
    (tr_bound%core!cmp.Eq. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Eq. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&)))
   :qid internal_core__tuple__impl&__11_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__11_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Eq. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Eq. (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Eq. (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__21_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__21_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Eq. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Eq. (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Eq. (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__45_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__45_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Eq. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Eq. (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Eq. (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__57_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__57_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.PartialOrd. (CONST_PTR $) (PTR T&. T&) (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.PartialOrd. (CONST_PTR $) (PTR T&. T&) (CONST_PTR $) (
      PTR T&. T&
   )))
   :qid internal_core__ptr__const_ptr__impl&__10_trait_impl_definition
   :skolemid skolem_internal_core__ptr__const_ptr__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.Ord. (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.Ord. (CONST_PTR $) (PTR T&. T&)))
   :qid internal_core__ptr__const_ptr__impl&__9_trait_impl_definition
   :skolemid skolem_internal_core__ptr__const_ptr__impl&__9_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.PartialOrd. $ (PTR T&. T&) $ (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.PartialOrd. $ (PTR T&. T&) $ (PTR T&. T&)))
   :qid internal_core__ptr__mut_ptr__impl&__10_trait_impl_definition
   :skolemid skolem_internal_core__ptr__mut_ptr__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!cmp.Ord. $ (PTR T&. T&))
   :pattern ((tr_bound%core!cmp.Ord. $ (PTR T&. T&)))
   :qid internal_core__ptr__mut_ptr__impl&__9_trait_impl_definition
   :skolemid skolem_internal_core__ptr__mut_ptr__impl&__9_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ TYPE%core!cmp.Ordering. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ TYPE%tuple%0. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ BOOL $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ CHAR $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ USIZE $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ (UINT 8) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialOrd. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialOrd. (REF A&.) A& (REF B&.) B&)
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. (REF A&.) A& (REF B&.) B&))
   :qid internal_core__cmp__impls__impl&__10_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!cmp.Ord. A&. A&)
    (tr_bound%core!cmp.Ord. (REF A&.) A&)
   )
   :pattern ((tr_bound%core!cmp.Ord. (REF A&.) A&))
   :qid internal_core__cmp__impls__impl&__11_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__11_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (B&. Dcr) (B& Type)) (!
   (=>
    (tr_bound%core!cmp.PartialOrd. A&. A& B&. B&)
    (tr_bound%core!cmp.PartialOrd. $ (MUTREF A&. A&) $ (MUTREF B&. B&))
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. $ (MUTREF A&. A&) $ (MUTREF B&. B&)))
   :qid internal_core__cmp__impls__impl&__14_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__14_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!cmp.Ord. A&. A&)
    (tr_bound%core!cmp.Ord. $ (MUTREF A&. A&))
   )
   :pattern ((tr_bound%core!cmp.Ord. $ (MUTREF A&. A&)))
   :qid internal_core__cmp__impls__impl&__15_trait_impl_definition
   :skolemid skolem_internal_core__cmp__impls__impl&__15_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialOrd. $ (ARRAY T&. T& N&. N&) $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. $ (ARRAY T&. T& N&. N&) $ (ARRAY T&. T& N&.
      N&
   )))
   :qid internal_core__array__impl&__17_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__17_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!cmp.Ord. T&. T&)
    )
    (tr_bound%core!cmp.Ord. $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!cmp.Ord. $ (ARRAY T&. T& N&. N&)))
   :qid internal_core__array__impl&__18_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__18_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialOrd. $ (TYPE%core!option.Option. T&. T&) $ (TYPE%core!option.Option.
      T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialOrd. $ (TYPE%core!option.Option. T&. T&) $ (TYPE%core!option.Option.
      T&. T&
   )))
   :qid internal_core__option__impl&__18_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__18_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Ord. T&. T&)
    )
    (tr_bound%core!cmp.Ord. $ (TYPE%core!option.Option. T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Ord. $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_core__option__impl&__19_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__19_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
     (tr_bound%core!cmp.PartialOrd. E&. E& E&. E&)
    )
    (tr_bound%core!cmp.PartialOrd. $ (TYPE%core!result.Result. T&. T& E&. E&) $ (TYPE%core!result.Result.
      T&. T& E&. E&
   )))
   :pattern ((tr_bound%core!cmp.PartialOrd. $ (TYPE%core!result.Result. T&. T& E&. E&)
     $ (TYPE%core!result.Result. T&. T& E&. E&)
   ))
   :qid internal_core__result__impl&__35_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__35_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!cmp.Ord. T&. T&)
     (tr_bound%core!cmp.Ord. E&. E&)
    )
    (tr_bound%core!cmp.Ord. $ (TYPE%core!result.Result. T&. T& E&. E&))
   )
   :pattern ((tr_bound%core!cmp.Ord. $ (TYPE%core!result.Result. T&. T& E&. E&)))
   :qid internal_core__result__impl&__37_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__37_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialOrd. $slice (SLICE T&. T&) $slice (SLICE T&. T&))
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. $slice (SLICE T&. T&) $slice (SLICE T&. T&)))
   :qid internal_core__slice__cmp__impl&__3_trait_impl_definition
   :skolemid skolem_internal_core__slice__cmp__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Ord. T&. T&)
    )
    (tr_bound%core!cmp.Ord. $slice (SLICE T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Ord. $slice (SLICE T&. T&)))
   :qid internal_core__slice__cmp__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__slice__cmp__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $slice STRSLICE $slice STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $slice STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialOrd. (DST T&.) (TYPE%tuple%1. T&. T&) (DST T&.) (TYPE%tuple%1.
      T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialOrd. (DST T&.) (TYPE%tuple%1. T&. T&) (DST T&.)
     (TYPE%tuple%1. T&. T&)
   ))
   :qid internal_core__tuple__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!cmp.Ord. T&. T&)
    )
    (tr_bound%core!cmp.Ord. (DST T&.) (TYPE%tuple%1. T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Ord. (DST T&.) (TYPE%tuple%1. T&. T&)))
   :qid internal_core__tuple__impl&__5_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__5_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((U&. Dcr) (U& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized U&.)
     (sized T&.)
     (tr_bound%core!cmp.PartialOrd. U&. U& U&. U&)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
    )
    (tr_bound%core!cmp.PartialOrd. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&) (DST T&.) (
      TYPE%tuple%2. U&. U& T&. T&
   )))
   :pattern ((tr_bound%core!cmp.PartialOrd. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&) (DST
      T&.
     ) (TYPE%tuple%2. U&. U& T&. T&)
   ))
   :qid internal_core__tuple__impl&__14_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__14_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((U&. Dcr) (U& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized U&.)
     (sized T&.)
     (tr_bound%core!cmp.Ord. U&. U&)
     (tr_bound%core!cmp.Ord. T&. T&)
    )
    (tr_bound%core!cmp.Ord. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&))
   )
   :pattern ((tr_bound%core!cmp.Ord. (DST T&.) (TYPE%tuple%2. U&. U& T&. T&)))
   :qid internal_core__tuple__impl&__15_trait_impl_definition
   :skolemid skolem_internal_core__tuple__impl&__15_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialOrd. (BOX A&. A& T&.) T& (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. (BOX A&. A& T&.) T& (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__19_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__19_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Ord. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Ord. (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Ord. (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__20_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__20_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialOrd. (RC A&. A& T&.) T& (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. (RC A&. A& T&.) T& (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__46_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__46_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Ord. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Ord. (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Ord. (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__47_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__47_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.PartialOrd. T&. T& T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.PartialOrd. (ARC A&. A& T&.) T& (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.PartialOrd. (ARC A&. A& T&.) T& (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__55_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__55_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!cmp.Ord. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!cmp.Ord. (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!cmp.Ord. (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__56_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__56_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ INT $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialOrd. $ NAT $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Ord. $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&. T&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!mem.maybe_uninit.MaybeUninit. T&.
      T&
   )))
   :qid internal_core__mem__maybe_uninit__impl&__16_trait_impl_definition
   :skolemid skolem_internal_core__mem__maybe_uninit__impl&__16_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ TYPE%core!cmp.Ordering.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ CHAR)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!marker.Copy. (CONST_PTR $) (PTR T&. T&))
   :pattern ((tr_bound%core!marker.Copy. (CONST_PTR $) (PTR T&. T&)))
   :qid internal_core__marker__impl&__58_trait_impl_definition
   :skolemid skolem_internal_core__marker__impl&__58_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!marker.Copy. $ (PTR T&. T&))
   :pattern ((tr_bound%core!marker.Copy. $ (PTR T&. T&)))
   :qid internal_core__marker__impl&__59_trait_impl_definition
   :skolemid skolem_internal_core__marker__impl&__59_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!marker.Copy. (REF T&.) T&)
   :pattern ((tr_bound%core!marker.Copy. (REF T&.) T&))
   :qid internal_core__marker__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__marker__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!ops.range.Bound. T&. T&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!ops.range.Bound. T&. T&)))
   :qid internal_core__ops__range__impl&__75_trait_impl_definition
   :skolemid skolem_internal_core__ops__range__impl&__75_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!marker.Copy. $ (ARRAY T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (ARRAY T&. T& N&. N&)))
   :qid internal_core__array__impl&__19_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__19_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!option.Option. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_core__option__impl&__6_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__6_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!option.Option. T&. T&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!option.Option. T&. T&)))
   :qid internal_core__option__impl&__54_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__54_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (E&. Dcr) (E& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized E&.)
     (tr_bound%core!marker.Copy. T&. T&)
     (tr_bound%core!marker.Copy. E&. E&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!result.Result. T&. T& E&. E&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!result.Result. T&. T& E&. E&)))
   :qid internal_core__result__impl&__30_trait_impl_definition
   :skolemid skolem_internal_core__result__impl&__30_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ TYPE%alloc!alloc.Global.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (sized A&.)
    (tr_bound%core!marker.Copy. (GHOST A&.) A&)
   )
   :pattern ((tr_bound%core!marker.Copy. (GHOST A&.) A&))
   :qid internal_verus_builtin__impl&__8_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__8_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Copy. A&. A&)
    )
    (tr_bound%core!marker.Copy. (TRACKED A&.) A&)
   )
   :pattern ((tr_bound%core!marker.Copy. (TRACKED A&.) A&))
   :qid internal_verus_builtin__impl&__10_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ INT)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ NAT)
)

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.Fn. F&. F& A&. A&)
    )
    (tr_bound%core!ops.function.FnOnce. (REF F&.) F& A&. A&)
   )
   :pattern ((tr_bound%core!ops.function.FnOnce. (REF F&.) F& A&. A&))
   :qid internal_core__ops__function__impls__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__ops__function__impls__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.Fn. F&. F& A&. A&)
    )
    (tr_bound%core!ops.function.FnMut. (REF F&.) F& A&. A&)
   )
   :pattern ((tr_bound%core!ops.function.FnMut. (REF F&.) F& A&. A&))
   :qid internal_core__ops__function__impls__impl&__1_trait_impl_definition
   :skolemid skolem_internal_core__ops__function__impls__impl&__1_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.Fn. F&. F& A&. A&)
    )
    (tr_bound%core!ops.function.Fn. (REF F&.) F& A&. A&)
   )
   :pattern ((tr_bound%core!ops.function.Fn. (REF F&.) F& A&. A&))
   :qid internal_core__ops__function__impls__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__ops__function__impls__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized Args&.)
     (sized A&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (tr_bound%core!ops.function.FnOnce. F&. F& Args&. Args&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!ops.function.FnOnce. (BOX A&. A& F&.) F& Args&. Args&)
   )
   :pattern ((tr_bound%core!ops.function.FnOnce. (BOX A&. A& F&.) F& Args&. Args&))
   :qid internal_alloc__boxed__impl&__31_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__31_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized Args&.)
     (sized A&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (tr_bound%core!ops.function.FnMut. F&. F& Args&. Args&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!ops.function.FnMut. (BOX A&. A& F&.) F& Args&. Args&)
   )
   :pattern ((tr_bound%core!ops.function.FnMut. (BOX A&. A& F&.) F& Args&. Args&))
   :qid internal_alloc__boxed__impl&__32_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__32_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Args&. Dcr) (Args& Type) (F&. Dcr) (F& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized Args&.)
     (sized A&.)
     (tr_bound%core!marker.Tuple. Args&. Args&)
     (tr_bound%core!ops.function.Fn. F&. F& Args&. Args&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!ops.function.Fn. (BOX A&. A& F&.) F& Args&. Args&)
   )
   :pattern ((tr_bound%core!ops.function.Fn. (BOX A&. A& F&.) F& Args&. Args&))
   :qid internal_alloc__boxed__impl&__33_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__33_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type) (F&. Dcr) (F& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!marker.Tuple. A&. A&)
     (tr_bound%core!ops.function.FnMut. F&. F& A&. A&)
    )
    (tr_bound%core!ops.function.FnMut. $ (MUTREF F&. F&) A&. A&)
   )
   :pattern ((tr_bound%core!ops.function.FnMut. $ (MUTREF F&. F&) A&. A&))
   :qid internal_core__ops__function__impls__impl&__3_trait_impl_definition
   :skolemid skolem_internal_core__ops__function__impls__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!slice.index.SliceIndex. $ USIZE $slice (SLICE T&. T&))
   )
   :pattern ((tr_bound%core!slice.index.SliceIndex. $ USIZE $slice (SLICE T&. T&)))
   :qid internal_core__slice__index__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__slice__index__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!ops.range.Range. $ USIZE) $slice
     (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!ops.range.Range. $ USIZE)
     $slice (SLICE T&. T&)
   ))
   :qid internal_core__slice__index__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__slice__index__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!ops.range.Range. $ USIZE) $slice
  STRSLICE
))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!slice.index.SliceIndex. (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
       $ USIZE
      ) $ (TYPE%core!ops.range.Bound. $ USIZE)
     ) $slice (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!slice.index.SliceIndex. (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
       $ USIZE
      ) $ (TYPE%core!ops.range.Bound. $ USIZE)
     ) $slice (SLICE T&. T&)
   ))
   :qid internal_core__slice__index__impl&__14_trait_impl_definition
   :skolemid skolem_internal_core__slice__index__impl&__14_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!slice.index.SliceIndex. (DST $) (TYPE%tuple%2. $ (TYPE%core!ops.range.Bound.
    $ USIZE
   ) $ (TYPE%core!ops.range.Bound. $ USIZE)
  ) $slice STRSLICE
))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!alloc.Allocator. A&. A&)
    (tr_bound%core!alloc.Allocator. (REF A&.) A&)
   )
   :pattern ((tr_bound%core!alloc.Allocator. (REF A&.) A&))
   :qid internal_core__alloc__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__alloc__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%core!alloc.Allocator. A&. A&)
    (tr_bound%core!alloc.Allocator. $ (MUTREF A&. A&))
   )
   :pattern ((tr_bound%core!alloc.Allocator. $ (MUTREF A&. A&)))
   :qid internal_core__alloc__impl&__3_trait_impl_definition
   :skolemid skolem_internal_core__alloc__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!alloc.Allocator. $ TYPE%alloc!alloc.Global.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!alloc.Allocator. (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!alloc.Allocator. (BOX A&. A& T&.) T&))
   :qid internal_alloc__boxed__impl&__49_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__49_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!alloc.Allocator. (RC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!alloc.Allocator. (RC A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__115_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__115_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!alloc.Allocator. (ARC A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!alloc.Allocator. (ARC A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__117_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__117_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!clone.Clone. Idx&. Idx&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!range.Range. Idx&. Idx&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!range.Range. Idx&. Idx&)))
   :qid internal_core__range__impl&__35_trait_impl_definition
   :skolemid skolem_internal_core__range__impl&__35_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%core!slice.ascii.EscapeAscii.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (P&. Dcr) (P& Type)) (!
   (=>
    (and
     (and
      (= $ (proj%%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1. (
          REF T&.
         ) T&
      )))
      (= BOOL (proj%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1.
         (REF T&.) T&
     ))))
     (sized P&.)
     (tr_bound%core!clone.Clone. P&. P&)
     (tr_bound%core!ops.function.FnMut. P&. P& (DST (REF T&.)) (TYPE%tuple%1. (REF T&.)
       T&
     ))
     (sized T&.)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Split. T&. T& P&. P&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Split. T&. T& P&. P&)))
   :qid internal_core__slice__iter__impl&__16_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__16_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (P&. Dcr) (P& Type)) (!
   (=>
    (and
     (and
      (= $ (proj%%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1. (
          REF T&.
         ) T&
      )))
      (= BOOL (proj%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1.
         (REF T&.) T&
     ))))
     (sized P&.)
     (tr_bound%core!clone.Clone. P&. P&)
     (tr_bound%core!ops.function.FnMut. P&. P& (DST (REF T&.)) (TYPE%tuple%1. (REF T&.)
       T&
     ))
     (sized T&.)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.SplitInclusive. T&. T& P&. P&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.SplitInclusive. T&. T&
      P&. P&
   )))
   :qid internal_core__slice__iter__impl&__23_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__23_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (P&. Dcr) (P& Type)) (!
   (=>
    (and
     (and
      (= $ (proj%%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1. (
          REF T&.
         ) T&
      )))
      (= BOOL (proj%core!ops.function.FnOnce./Output P&. P& (DST (REF T&.)) (TYPE%tuple%1.
         (REF T&.) T&
     ))))
     (sized P&.)
     (tr_bound%core!clone.Clone. P&. P&)
     (tr_bound%core!ops.function.FnMut. P&. P& (DST (REF T&.)) (TYPE%tuple%1. (REF T&.)
       T&
     ))
     (sized T&.)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RSplit. T&. T& P&. P&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RSplit. T&. T& P&. P&)))
   :qid internal_core__slice__iter__impl&__40_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__40_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Windows. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Windows. T&. T&)))
   :qid internal_core__slice__iter__impl&__61_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__61_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Chunks. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.Chunks. T&. T&)))
   :qid internal_core__slice__iter__impl&__70_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__70_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ChunksExact. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ChunksExact. T&. T&)))
   :qid internal_core__slice__iter__impl&__89_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__89_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ArrayWindows. T&. T& N&. N&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ArrayWindows. T&. T& N&.
      N&
   )))
   :qid internal_core__slice__iter__impl&__108_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__108_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RChunks. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RChunks. T&. T&)))
   :qid internal_core__slice__iter__impl&__117_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__117_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RChunksExact. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.RChunksExact. T&. T&)))
   :qid internal_core__slice__iter__impl&__136_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__136_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (P&. Dcr) (P& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized P&.)
     (tr_bound%core!clone.Clone. P&. P&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ChunkBy. T&. T& P&. P&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!slice.iter.ChunkBy. T&. T& P&. P&)))
   :qid internal_core__slice__iter__impl&__162_trait_impl_definition
   :skolemid skolem_internal_core__slice__iter__impl&__162_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%core!slice.GetDisjointMutError.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%core!str.lossy.Utf8Chunks.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!cmp.PartialEq. Idx&. Idx& Idx&. Idx&)
    )
    (tr_bound%core!cmp.PartialEq. $ (TYPE%core!range.Range. Idx&. Idx&) $ (TYPE%core!range.Range.
      Idx&. Idx&
   )))
   :pattern ((tr_bound%core!cmp.PartialEq. $ (TYPE%core!range.Range. Idx&. Idx&) $ (TYPE%core!range.Range.
      Idx&. Idx&
   )))
   :qid internal_core__range__impl&__38_trait_impl_definition
   :skolemid skolem_internal_core__range__impl&__38_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.PartialEq. $ TYPE%core!slice.GetDisjointMutError. $ TYPE%core!slice.GetDisjointMutError.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!cmp.Eq. Idx&. Idx&)
    )
    (tr_bound%core!cmp.Eq. $ (TYPE%core!range.Range. Idx&. Idx&))
   )
   :pattern ((tr_bound%core!cmp.Eq. $ (TYPE%core!range.Range. Idx&. Idx&)))
   :qid internal_core__range__impl&__39_trait_impl_definition
   :skolemid skolem_internal_core__range__impl&__39_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!cmp.Eq. $ TYPE%core!slice.GetDisjointMutError.)
)

;; Trait-Impl-Axiom
(assert
 (forall ((Idx&. Dcr) (Idx& Type)) (!
   (=>
    (and
     (sized Idx&.)
     (tr_bound%core!marker.Copy. Idx&. Idx&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!range.Range. Idx&. Idx&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!range.Range. Idx&. Idx&)))
   :qid internal_core__range__impl&__33_trait_impl_definition
   :skolemid skolem_internal_core__range__impl&__33_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!range.Range. $ USIZE) $slice (
      SLICE T&. T&
   )))
   :pattern ((tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!range.Range. $ USIZE)
     $slice (SLICE T&. T&)
   ))
   :qid internal_core__slice__index__impl&__5_trait_impl_definition
   :skolemid skolem_internal_core__slice__index__impl&__5_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!slice.index.SliceIndex. $ (TYPE%core!range.Range. $ USIZE) $slice STRSLICE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ (UINT 8)) (DST (
    REF $
   )
  ) (TYPE%tuple%1. (REF $) (UINT 8))
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ (UINT 8)) (DST
   (REF $)
  ) (TYPE%tuple%1. (REF $) (UINT 8))
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ (UINT 8)) (
   DST (REF $)
  ) (TYPE%tuple%1. (REF $) (UINT 8))
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ USIZE) (DST (REF
    $
   )
  ) (TYPE%tuple%1. (REF $) USIZE)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ USIZE) (DST (
    REF $
   )
  ) (TYPE%tuple%1. (REF $) USIZE)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ USIZE) (DST
   (REF $)
  ) (TYPE%tuple%1. (REF $) USIZE)
))

;; Trait-Impl-Axiom
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (and
     (sized Self%&.)
     (tr_bound%core!clone.Clone. Self%&. Self%&)
    )
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. Self%&. Self%&) (
      DST (REF Self%&.)
     ) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. Self%&. Self%&)
     (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :qid internal_core__clone__Clone__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_core__clone__Clone__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (and
     (sized Self%&.)
     (tr_bound%core!clone.Clone. Self%&. Self%&)
    )
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. Self%&. Self%&)
     (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. Self%&.
      Self%&
     ) (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :qid internal_core__clone__Clone__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_core__clone__Clone__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (and
     (sized Self%&.)
     (tr_bound%core!clone.Clone. Self%&. Self%&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. Self%&. Self%&)
     (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. Self%&.
      Self%&
     ) (DST (REF Self%&.)) (TYPE%tuple%1. (REF Self%&.) Self%&)
   ))
   :qid internal_core__clone__Clone__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_core__clone__Clone__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ BOOL) (DST (REF $))
  (TYPE%tuple%1. (REF $) BOOL)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ BOOL) (DST (REF
    $
   )
  ) (TYPE%tuple%1. (REF $) BOOL)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ BOOL) (DST (
    REF $
   )
  ) (TYPE%tuple%1. (REF $) BOOL)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ CHAR) (DST (REF $))
  (TYPE%tuple%1. (REF $) CHAR)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ CHAR) (DST (REF
    $
   )
  ) (TYPE%tuple%1. (REF $) CHAR)
))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ CHAR) (DST (
    REF $
   )
  ) (TYPE%tuple%1. (REF $) CHAR)
))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (REF T&.) T&) (DST
     (REF (REF T&.))
    ) (TYPE%tuple%1. (REF (REF T&.)) T&)
   )
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (REF T&.)
      T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   ))
   :qid internal_core__clone__impls__impl&__6__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__6__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (REF T&.) T&)
    (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   )
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (REF T&.)
      T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   ))
   :qid internal_core__clone__impls__impl&__6__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__6__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (REF T&.) T&)
    (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   )
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (REF T&.)
      T&
     ) (DST (REF (REF T&.))) (TYPE%tuple%1. (REF (REF T&.)) T&)
   ))
   :qid internal_core__clone__impls__impl&__6__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_core__clone__impls__impl&__6__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY T&. T& N&.
       N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY T&.
       T& N&. N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :qid internal_core__array__impl&__20__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__20__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY T&. T&
       N&. N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY
       T&. T& N&. N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :qid internal_core__array__impl&__20__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__20__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY T&. T&
       N&. N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ (ARRAY
       T&. T& N&. N&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (ARRAY T&. T& N&. N&))
   ))
   :qid internal_core__array__impl&__20__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_core__array__impl&__20__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (TRACKED T&.) T&)
     (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (TRACKED T&.)
      T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__9__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__9__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (TRACKED T&.) T&)
     (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (TRACKED
       T&.
      ) T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__9__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__9__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!marker.Copy. T&. T&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (TRACKED T&.)
      T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (TRACKED
       T&.
      ) T&
     ) (DST (REF (TRACKED T&.))) (TYPE%tuple%1. (REF (TRACKED T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__9__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__9__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (GHOST T&.) T&) (
      DST (REF (GHOST T&.))
     ) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (GHOST T&.)
      T&
     ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__7__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__7__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (GHOST T&.) T&)
     (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (GHOST
       T&.
      ) T&
     ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__7__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__7__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (GHOST T&.) T&)
     (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (GHOST
       T&.
      ) T&
     ) (DST (REF (GHOST T&.))) (TYPE%tuple%1. (REF (GHOST T&.)) T&)
   ))
   :qid internal_verus_builtin__impl&__7__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_verus_builtin__impl&__7__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :qid internal_core__option__impl&__6__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__6__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :qid internal_core__option__impl&__6__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__6__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. $ (TYPE%core!option.Option.
       T&. T&
      )
     ) (DST (REF $)) (TYPE%tuple%1. (REF $) (TYPE%core!option.Option. T&. T&))
   ))
   :qid internal_core__option__impl&__6__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_core__option__impl&__6__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (BOX A&. A& T&.) T&)
     (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.Fn. $ (FNDEF%core!clone.Clone.clone. (BOX A&. A&
       T&.
      ) T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :qid internal_alloc__boxed__impl&__15__clone__impl_fndef&__Fn_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__15__clone__impl_fndef&__Fn_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (BOX A&. A& T&.)
      T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnMut. $ (FNDEF%core!clone.Clone.clone. (BOX A&.
       A& T&.
      ) T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :qid internal_alloc__boxed__impl&__15__clone__impl_fndef&__FnMut_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__15__clone__impl_fndef&__FnMut_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (BOX A&. A& T&.)
      T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :pattern ((tr_bound%core!ops.function.FnOnce. $ (FNDEF%core!clone.Clone.clone. (BOX A&.
       A& T&.
      ) T&
     ) (DST (REF (BOX A&. A& T&.))) (TYPE%tuple%1. (REF (BOX A&. A& T&.)) T&)
   ))
   :qid internal_alloc__boxed__impl&__15__clone__impl_fndef&__FnOnce_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__impl&__15__clone__impl_fndef&__FnOnce_trait_impl_definition
)))

;; Function-Specs det_harness::det___rust_std_candidate
(declare-fun ens%det_harness!det___rust_std_candidate. (Dcr Type Bool Int Bool Int
  Int Bool Bool Int Bool Int Int Bool Bool Bool Int Bool Int Int Bool Bool Poly core!option.Option.
  core!option.Option.
 ) Bool
)
(assert
 (forall ((T&. Dcr) (T& Type) (g_slice_leneq! Bool) (k_slice_leneq! Int) (g_slice_lenrng!
    Bool
   ) (k_slice_lenrng_lo! Int) (k_slice_lenrng_hi! Int) (g_r1_is_Some! Bool) (g_r1__Some_0_1_leneq!
    Bool
   ) (k_r1__Some_0_1_leneq! Int) (g_r1__Some_0_1_lenrng! Bool) (k_r1__Some_0_1_lenrng_lo!
    Int
   ) (k_r1__Some_0_1_lenrng_hi! Int) (g_r1_is_None! Bool) (g_r2_is_Some! Bool) (g_r2__Some_0_1_leneq!
    Bool
   ) (k_r2__Some_0_1_leneq! Int) (g_r2__Some_0_1_lenrng! Bool) (k_r2__Some_0_1_lenrng_lo!
    Int
   ) (k_r2__Some_0_1_lenrng_hi! Int) (g_r2_is_None! Bool) (g_neq_tuple! Bool) (slice!
    Poly
   ) (r1! core!option.Option.) (r2! core!option.Option.)
  ) (!
   (= (ens%det_harness!det___rust_std_candidate. T&. T& g_slice_leneq! k_slice_leneq!
     g_slice_lenrng! k_slice_lenrng_lo! k_slice_lenrng_hi! g_r1_is_Some! g_r1__Some_0_1_leneq!
     k_r1__Some_0_1_leneq! g_r1__Some_0_1_lenrng! k_r1__Some_0_1_lenrng_lo! k_r1__Some_0_1_lenrng_hi!
     g_r1_is_None! g_r2_is_Some! g_r2__Some_0_1_leneq! k_r2__Some_0_1_leneq! g_r2__Some_0_1_lenrng!
     k_r2__Some_0_1_lenrng_lo! k_r2__Some_0_1_lenrng_hi! g_r2_is_None! g_neq_tuple! slice!
     r1! r2!
    ) (=>
     (and
      (and
       (and
        (=>
         (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
          0
         )
         (is-core!option.Option./None r1!)
        )
        (=>
         (not (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
           0
         ))
         (and
          (and
           (is-core!option.Option./Some r1!)
           (= (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
               (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
                (Poly%core!option.Option. r1!)
             )))
            ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
             (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
               1
          )))))
          (= (vstd!view.View.view.? $slice (SLICE T&. T&) (tuple%2./tuple%2/1 (%Poly%tuple%2. (
               core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                (SLICE T&. T&)
               ) (%Poly%core!option.Option. (Poly%core!option.Option. r1!))
            )))
           ) (vstd!seq.Seq.subrange.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
            (I 0) (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
                slice!
               )
              ) 1
       )))))))
       (=>
        (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
         0
        )
        (is-core!option.Option./None r2!)
      ))
      (=>
       (not (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
         0
       ))
       (and
        (and
         (is-core!option.Option./Some r2!)
         (= (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
             (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
              (Poly%core!option.Option. r2!)
           )))
          ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
           (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
             1
        )))))
        (= (vstd!view.View.view.? $slice (SLICE T&. T&) (tuple%2./tuple%2/1 (%Poly%tuple%2. (
             core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
              (SLICE T&. T&)
             ) (%Poly%core!option.Option. (Poly%core!option.Option. r2!))
          )))
         ) (vstd!seq.Seq.subrange.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
          (I 0) (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
              slice!
             )
            ) 1
     )))))))
     (det_harness!det___rust_std_candidate_equal.? T&. T& (Poly%core!option.Option. r1!)
      (Poly%core!option.Option. r2!)
   )))
   :pattern ((ens%det_harness!det___rust_std_candidate. T&. T& g_slice_leneq! k_slice_leneq!
     g_slice_lenrng! k_slice_lenrng_lo! k_slice_lenrng_hi! g_r1_is_Some! g_r1__Some_0_1_leneq!
     k_r1__Some_0_1_leneq! g_r1__Some_0_1_lenrng! k_r1__Some_0_1_lenrng_lo! k_r1__Some_0_1_lenrng_hi!
     g_r1_is_None! g_r2_is_Some! g_r2__Some_0_1_leneq! k_r2__Some_0_1_leneq! g_r2__Some_0_1_lenrng!
     k_r2__Some_0_1_lenrng_lo! k_r2__Some_0_1_lenrng_hi! g_r2_is_None! g_neq_tuple! slice!
     r1! r2!
   ))
   :qid internal_ens__det_harness!det___rust_std_candidate._definition
   :skolemid skolem_internal_ens__det_harness!det___rust_std_candidate._definition
)))

;; Function-Def det_harness::det___rust_std_candidate
;; /home/chentianyu/nanvix-rust-std-slice-specgen-2026-08-11/verification/evidence/slice_feedback_determinism/all-20260811T1030Z-adjacent-fnmut/core__slice__split_last/det_harness.rs:1204:7: 1204:600 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const g_slice_leneq! Bool)
 (declare-const k_slice_leneq! Int)
 (declare-const g_slice_lenrng! Bool)
 (declare-const k_slice_lenrng_lo! Int)
 (declare-const k_slice_lenrng_hi! Int)
 (declare-const g_r1_is_Some! Bool)
 (declare-const g_r1__Some_0_1_leneq! Bool)
 (declare-const k_r1__Some_0_1_leneq! Int)
 (declare-const g_r1__Some_0_1_lenrng! Bool)
 (declare-const k_r1__Some_0_1_lenrng_lo! Int)
 (declare-const k_r1__Some_0_1_lenrng_hi! Int)
 (declare-const g_r1_is_None! Bool)
 (declare-const g_r2_is_Some! Bool)
 (declare-const g_r2__Some_0_1_leneq! Bool)
 (declare-const k_r2__Some_0_1_leneq! Int)
 (declare-const g_r2__Some_0_1_lenrng! Bool)
 (declare-const k_r2__Some_0_1_lenrng_lo! Int)
 (declare-const k_r2__Some_0_1_lenrng_hi! Int)
 (declare-const g_r2_is_None! Bool)
 (declare-const g_neq_tuple! Bool)
 (declare-const slice! Poly)
 (declare-const r1! core!option.Option.)
 (declare-const r2! core!option.Option.)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (<= 0 k_slice_leneq!)
 )
 (assert
  (<= 0 k_slice_lenrng_lo!)
 )
 (assert
  (<= 0 k_slice_lenrng_hi!)
 )
 (assert
  (<= 0 k_r1__Some_0_1_leneq!)
 )
 (assert
  (<= 0 k_r1__Some_0_1_lenrng_lo!)
 )
 (assert
  (<= 0 k_r1__Some_0_1_lenrng_hi!)
 )
 (assert
  (<= 0 k_r2__Some_0_1_leneq!)
 )
 (assert
  (<= 0 k_r2__Some_0_1_lenrng_lo!)
 )
 (assert
  (<= 0 k_r2__Some_0_1_lenrng_hi!)
 )
 (assert
  (has_type slice! (SLICE T&. T&))
 )
 (assert
  (has_type (Poly%core!option.Option. r1!) (TYPE%core!option.Option. (DST (REF $slice))
    (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&))
 )))
 (assert
  (has_type (Poly%core!option.Option. r2!) (TYPE%core!option.Option. (DST (REF $slice))
    (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&))
 )))
 (declare-const %%switch_label%%0 Bool)
 (declare-const %%switch_label%%1 Bool)
 (declare-const %%switch_label%%2 Bool)
 (declare-const %%switch_label%%3 Bool)
 (declare-const %%switch_label%%4 Bool)
 (declare-const %%switch_label%%5 Bool)
 (declare-const %%switch_label%%6 Bool)
 (declare-const %%switch_label%%7 Bool)
 (declare-const %%switch_label%%8 Bool)
 (declare-const %%switch_label%%9 Bool)
 (declare-const %%switch_label%%10 Bool)
 ;; postcondition not satisfied
 (declare-const %%location_label%%0 Bool)
 (assert
  (not (or
    (and
     (=>
      g_slice_leneq!
      (=>
       (= (vstd!slice.len%returns_clause_autospec.? T&. T& slice!) k_slice_leneq!)
       %%switch_label%%10
     ))
     (=>
      (not g_slice_leneq!)
      %%switch_label%%10
    ))
    (and
     (not %%switch_label%%10)
     (or
      (and
       (=>
        g_slice_lenrng!
        (=>
         (and
          (>= (vstd!slice.len%returns_clause_autospec.? T&. T& slice!) k_slice_lenrng_lo!)
          (<= (vstd!slice.len%returns_clause_autospec.? T&. T& slice!) k_slice_lenrng_hi!)
         )
         %%switch_label%%9
       ))
       (=>
        (not g_slice_lenrng!)
        %%switch_label%%9
      ))
      (and
       (not %%switch_label%%9)
       (or
        (and
         (=>
          g_r1_is_Some!
          (=>
           (is-core!option.Option./Some r1!)
           %%switch_label%%8
         ))
         (=>
          (not g_r1_is_Some!)
          %%switch_label%%8
        ))
        (and
         (not %%switch_label%%8)
         (or
          (and
           (=>
            g_r1__Some_0_1_leneq!
            (=>
             (is-core!option.Option./Some r1!)
             (=>
              (= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                  (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                    (SLICE T&. T&)
                   ) (%Poly%core!option.Option. (Poly%core!option.Option. r1!))
                )))
               ) k_r1__Some_0_1_leneq!
              )
              %%switch_label%%7
           )))
           (=>
            (not g_r1__Some_0_1_leneq!)
            %%switch_label%%7
          ))
          (and
           (not %%switch_label%%7)
           (or
            (and
             (=>
              g_r1__Some_0_1_lenrng!
              (=>
               (is-core!option.Option./Some r1!)
               (=>
                (and
                 (>= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                     (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                       (SLICE T&. T&)
                      ) (%Poly%core!option.Option. (Poly%core!option.Option. r1!))
                   )))
                  ) k_r1__Some_0_1_lenrng_lo!
                 )
                 (<= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                     (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                       (SLICE T&. T&)
                      ) (%Poly%core!option.Option. (Poly%core!option.Option. r1!))
                   )))
                  ) k_r1__Some_0_1_lenrng_hi!
                ))
                %%switch_label%%6
             )))
             (=>
              (not g_r1__Some_0_1_lenrng!)
              %%switch_label%%6
            ))
            (and
             (not %%switch_label%%6)
             (or
              (and
               (=>
                g_r1_is_None!
                (=>
                 (is-core!option.Option./None r1!)
                 %%switch_label%%5
               ))
               (=>
                (not g_r1_is_None!)
                %%switch_label%%5
              ))
              (and
               (not %%switch_label%%5)
               (or
                (and
                 (=>
                  g_r2_is_Some!
                  (=>
                   (is-core!option.Option./Some r2!)
                   %%switch_label%%4
                 ))
                 (=>
                  (not g_r2_is_Some!)
                  %%switch_label%%4
                ))
                (and
                 (not %%switch_label%%4)
                 (or
                  (and
                   (=>
                    g_r2__Some_0_1_leneq!
                    (=>
                     (is-core!option.Option./Some r2!)
                     (=>
                      (= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                          (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                            (SLICE T&. T&)
                           ) (%Poly%core!option.Option. (Poly%core!option.Option. r2!))
                        )))
                       ) k_r2__Some_0_1_leneq!
                      )
                      %%switch_label%%3
                   )))
                   (=>
                    (not g_r2__Some_0_1_leneq!)
                    %%switch_label%%3
                  ))
                  (and
                   (not %%switch_label%%3)
                   (or
                    (and
                     (=>
                      g_r2__Some_0_1_lenrng!
                      (=>
                       (is-core!option.Option./Some r2!)
                       (=>
                        (and
                         (>= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                             (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                               (SLICE T&. T&)
                              ) (%Poly%core!option.Option. (Poly%core!option.Option. r2!))
                           )))
                          ) k_r2__Some_0_1_lenrng_lo!
                         )
                         (<= (vstd!slice.len%returns_clause_autospec.? T&. T& (tuple%2./tuple%2/1 (%Poly%tuple%2.
                             (core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                               (SLICE T&. T&)
                              ) (%Poly%core!option.Option. (Poly%core!option.Option. r2!))
                           )))
                          ) k_r2__Some_0_1_lenrng_hi!
                        ))
                        %%switch_label%%2
                     )))
                     (=>
                      (not g_r2__Some_0_1_lenrng!)
                      %%switch_label%%2
                    ))
                    (and
                     (not %%switch_label%%2)
                     (or
                      (and
                       (=>
                        g_r2_is_None!
                        (=>
                         (is-core!option.Option./None r2!)
                         %%switch_label%%1
                       ))
                       (=>
                        (not g_r2_is_None!)
                        %%switch_label%%1
                      ))
                      (and
                       (not %%switch_label%%1)
                       (or
                        (and
                         (=>
                          g_neq_tuple!
                          (=>
                           (not (det_harness!det___rust_std_candidate_equal.? T&. T& (Poly%core!option.Option.
                              r1!
                             ) (Poly%core!option.Option. r2!)
                           ))
                           %%switch_label%%0
                         ))
                         (=>
                          (not g_neq_tuple!)
                          %%switch_label%%0
                        ))
                        (and
                         (not %%switch_label%%0)
                         (=>
                          %%location_label%%0
                          (=>
                           (and
                            (and
                             (and
                              (=>
                               (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                                0
                               )
                               (is-core!option.Option./None r1!)
                              )
                              (=>
                               (not (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                                 0
                               ))
                               (and
                                (and
                                 (is-core!option.Option./Some r1!)
                                 (= (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
                                     (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
                                      (Poly%core!option.Option. r1!)
                                   )))
                                  ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
                                   (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                                     1
                                )))))
                                (= (vstd!view.View.view.? $slice (SLICE T&. T&) (tuple%2./tuple%2/1 (%Poly%tuple%2. (
                                     core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                                      (SLICE T&. T&)
                                     ) (%Poly%core!option.Option. (Poly%core!option.Option. r1!))
                                  )))
                                 ) (vstd!seq.Seq.subrange.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
                                  (I 0) (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
                                      slice!
                                     )
                                    ) 1
                             )))))))
                             (=>
                              (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                               0
                              )
                              (is-core!option.Option./None r2!)
                            ))
                            (=>
                             (not (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                               0
                             ))
                             (and
                              (and
                               (is-core!option.Option./Some r2!)
                               (= (tuple%2./tuple%2/0 (%Poly%tuple%2. (core!option.Option./Some/0 (DST (REF $slice))
                                   (TYPE%tuple%2. (REF T&.) T& (REF $slice) (SLICE T&. T&)) (%Poly%core!option.Option.
                                    (Poly%core!option.Option. r2!)
                                 )))
                                ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
                                 (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!))
                                   1
                              )))))
                              (= (vstd!view.View.view.? $slice (SLICE T&. T&) (tuple%2./tuple%2/1 (%Poly%tuple%2. (
                                   core!option.Option./Some/0 (DST (REF $slice)) (TYPE%tuple%2. (REF T&.) T& (REF $slice)
                                    (SLICE T&. T&)
                                   ) (%Poly%core!option.Option. (Poly%core!option.Option. r2!))
                                )))
                               ) (vstd!seq.Seq.subrange.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) slice!)
                                (I 0) (I (Sub (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&)
                                    slice!
                                   )
                                  ) 1
                           )))))))
                           (det_harness!det___rust_std_candidate_equal.? T&. T& (Poly%core!option.Option. r1!)
                            (Poly%core!option.Option. r2!)
 )))))))))))))))))))))))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 180000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)
