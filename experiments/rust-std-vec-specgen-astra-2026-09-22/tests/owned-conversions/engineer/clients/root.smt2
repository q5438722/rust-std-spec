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
   :qid prelude_mut_ref_future_has_type
   :skolemid skolem_prelude_mut_ref_future_has_type
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
   :qid prelude_box_unbox_float
   :skolemid skolem_prelude_box_unbox_float
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
   :qid prelude_has_type_float
   :skolemid skolem_prelude_has_type_float
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
    (has_type x CHAR)
    (charInv (%I x))
   )
   :pattern ((has_type x CHAR))
   :qid prelude_unbox_char
   :skolemid skolem_prelude_unbox_char
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
   :qid prelude_unbox_float
   :skolemid skolem_prelude_unbox_float
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
(declare-const fuel%vstd!std_specs.convert.impl&%6.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%6.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%7.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%7.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%8.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%8.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%9.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%9.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%10.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%10.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%11.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%11.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%12.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%12.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%13.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%13.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%14.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%14.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%15.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%15.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%16.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%16.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%17.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%17.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%18.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%18.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%19.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%19.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%20.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%20.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%21.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%21.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%22.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%22.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%23.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%23.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%24.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%24.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%25.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%25.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%26.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%26.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%27.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%27.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%28.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%28.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%29.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.convert.impl&%29.from_spec. FuelId)
(declare-const fuel%vstd!std_specs.vec.axiom_spec_len. FuelId)
(declare-const fuel%vstd!std_specs.vec.axiom_vec_has_resolved. FuelId)
(declare-const fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%1.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%2.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%3.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%4.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%5.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%6.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%7.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%8.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%9.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%10.is_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.axiom_nonzero_is_not_zero. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.nonzero_spec_get. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%16.obeys_from_spec. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.impl&%16.from_spec. FuelId)
(declare-const fuel%vstd!array.array_view. FuelId)
(declare-const fuel%vstd!array.impl&%0.view. FuelId)
(declare-const fuel%vstd!array.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!array.lemma_array_index. FuelId)
(declare-const fuel%vstd!array.array_len_matches_n. FuelId)
(declare-const fuel%vstd!array.axiom_array_ext_equal. FuelId)
(declare-const fuel%vstd!array.axiom_array_has_resolved. FuelId)
(declare-const fuel%vstd!array.axiom_array_decreases_to_seq. FuelId)
(declare-const fuel%vstd!array.lemma_array_index_decreases. FuelId)
(declare-const fuel%vstd!function.axiom_fn_mut_call_requires. FuelId)
(declare-const fuel%vstd!function.axiom_fn_mut_call_ensures. FuelId)
(declare-const fuel%vstd!raw_ptr.impl&%3.view. FuelId)
(declare-const fuel%vstd!raw_ptr.ptrs_mut_eq. FuelId)
(declare-const fuel%vstd!raw_ptr.ptrs_mut_eq_sized. FuelId)
(declare-const fuel%vstd!seq.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_index_decreases. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_new_len. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_new_index. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_ext_equal. FuelId)
(declare-const fuel%vstd!seq.lemma_seq_ext_equal_deep. FuelId)
(declare-const fuel%vstd!slice.impl&%2.spec_index. FuelId)
(declare-const fuel%vstd!slice.axiom_spec_len. FuelId)
(declare-const fuel%vstd!slice.len%returns_clause_autospec. FuelId)
(declare-const fuel%vstd!slice.axiom_slice_ext_equal. FuelId)
(declare-const fuel%vstd!slice.axiom_slice_has_resolved. FuelId)
(declare-const fuel%vstd!slice.axiom_slice_decreases_to_seq. FuelId)
(declare-const fuel%vstd!slice.lemma_slice_index_decreases. FuelId)
(declare-const fuel%vstd!view.impl&%0.view. FuelId)
(declare-const fuel%vstd!view.impl&%2.view. FuelId)
(declare-const fuel%vstd!view.impl&%4.view. FuelId)
(declare-const fuel%vstd!view.impl&%6.view. FuelId)
(declare-const fuel%vstd!view.impl&%16.view. FuelId)
(declare-const fuel%vstd!view.impl&%18.view. FuelId)
(declare-const fuel%vstd!view.impl&%20.view. FuelId)
(declare-const fuel%vstd!view.impl&%22.view. FuelId)
(declare-const fuel%vstd!view.impl&%24.view. FuelId)
(declare-const fuel%vstd!view.impl&%26.view. FuelId)
(declare-const fuel%vstd!view.impl&%28.view. FuelId)
(declare-const fuel%vstd!view.impl&%30.view. FuelId)
(declare-const fuel%vstd!view.impl&%32.view. FuelId)
(declare-const fuel%vstd!view.impl&%34.view. FuelId)
(declare-const fuel%vstd!view.impl&%36.view. FuelId)
(declare-const fuel%vstd!view.impl&%38.view. FuelId)
(declare-const fuel%vstd!view.impl&%40.view. FuelId)
(declare-const fuel%vstd!view.impl&%42.view. FuelId)
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
(declare-const fuel%vstd!mut_ref.group_mut_ref_axioms. FuelId)
(declare-const fuel%vstd!raw_ptr.group_raw_ptr_axioms. FuelId)
(declare-const fuel%vstd!seq.group_seq_lemmas. FuelId)
(declare-const fuel%vstd!seq_lib.group_filter_ensures. FuelId)
(declare-const fuel%vstd!seq_lib.group_seq_lib_default. FuelId)
(declare-const fuel%vstd!set.group_set_lemmas. FuelId)
(declare-const fuel%vstd!set_lib.group_set_lib_default. FuelId)
(declare-const fuel%vstd!slice.group_slice_axioms. FuelId)
(declare-const fuel%vstd!string.group_string_axioms. FuelId)
(declare-const fuel%vstd!std_specs.bits.group_bits_axioms. FuelId)
(declare-const fuel%vstd!std_specs.control_flow.group_control_flow_axioms. FuelId)
(declare-const fuel%vstd!std_specs.fmt.group_fmt_axioms. FuelId)
(declare-const fuel%vstd!std_specs.iter.group_iter_axioms. FuelId)
(declare-const fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms. FuelId)
(declare-const fuel%vstd!std_specs.btree.group_btree_axioms. FuelId)
(declare-const fuel%vstd!std_specs.hash.group_hash_axioms. FuelId)
(declare-const fuel%vstd!std_specs.range.group_range_axioms. FuelId)
(declare-const fuel%vstd!std_specs.vec.group_vec_axioms. FuelId)
(declare-const fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms. FuelId)
(declare-const fuel%vstd!std_specs.nonzero.group_nonzero_axioms. FuelId)
(declare-const fuel%vstd!group_vstd_default. FuelId)
(assert
 (distinct fuel%vstd!std_specs.convert.impl&%6.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%6.from_spec.
  fuel%vstd!std_specs.convert.impl&%7.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%7.from_spec.
  fuel%vstd!std_specs.convert.impl&%8.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%8.from_spec.
  fuel%vstd!std_specs.convert.impl&%9.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%9.from_spec.
  fuel%vstd!std_specs.convert.impl&%10.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%10.from_spec.
  fuel%vstd!std_specs.convert.impl&%11.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%11.from_spec.
  fuel%vstd!std_specs.convert.impl&%12.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%12.from_spec.
  fuel%vstd!std_specs.convert.impl&%13.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%13.from_spec.
  fuel%vstd!std_specs.convert.impl&%14.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%14.from_spec.
  fuel%vstd!std_specs.convert.impl&%15.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%15.from_spec.
  fuel%vstd!std_specs.convert.impl&%16.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%16.from_spec.
  fuel%vstd!std_specs.convert.impl&%17.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%17.from_spec.
  fuel%vstd!std_specs.convert.impl&%18.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%18.from_spec.
  fuel%vstd!std_specs.convert.impl&%19.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%19.from_spec.
  fuel%vstd!std_specs.convert.impl&%20.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%20.from_spec.
  fuel%vstd!std_specs.convert.impl&%21.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%21.from_spec.
  fuel%vstd!std_specs.convert.impl&%22.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%22.from_spec.
  fuel%vstd!std_specs.convert.impl&%23.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%23.from_spec.
  fuel%vstd!std_specs.convert.impl&%24.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%24.from_spec.
  fuel%vstd!std_specs.convert.impl&%25.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%25.from_spec.
  fuel%vstd!std_specs.convert.impl&%26.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%26.from_spec.
  fuel%vstd!std_specs.convert.impl&%27.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%27.from_spec.
  fuel%vstd!std_specs.convert.impl&%28.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%28.from_spec.
  fuel%vstd!std_specs.convert.impl&%29.obeys_from_spec. fuel%vstd!std_specs.convert.impl&%29.from_spec.
  fuel%vstd!std_specs.vec.axiom_spec_len. fuel%vstd!std_specs.vec.axiom_vec_has_resolved.
  fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view. fuel%vstd!std_specs.nonzero.impl&%1.is_zero.
  fuel%vstd!std_specs.nonzero.impl&%2.is_zero. fuel%vstd!std_specs.nonzero.impl&%3.is_zero.
  fuel%vstd!std_specs.nonzero.impl&%4.is_zero. fuel%vstd!std_specs.nonzero.impl&%5.is_zero.
  fuel%vstd!std_specs.nonzero.impl&%6.is_zero. fuel%vstd!std_specs.nonzero.impl&%7.is_zero.
  fuel%vstd!std_specs.nonzero.impl&%8.is_zero. fuel%vstd!std_specs.nonzero.impl&%9.is_zero.
  fuel%vstd!std_specs.nonzero.impl&%10.is_zero. fuel%vstd!std_specs.nonzero.axiom_nonzero_is_not_zero.
  fuel%vstd!std_specs.nonzero.nonzero_spec_get. fuel%vstd!std_specs.nonzero.impl&%16.obeys_from_spec.
  fuel%vstd!std_specs.nonzero.impl&%16.from_spec. fuel%vstd!array.array_view. fuel%vstd!array.impl&%0.view.
  fuel%vstd!array.impl&%2.spec_index. fuel%vstd!array.lemma_array_index. fuel%vstd!array.array_len_matches_n.
  fuel%vstd!array.axiom_array_ext_equal. fuel%vstd!array.axiom_array_has_resolved.
  fuel%vstd!array.axiom_array_decreases_to_seq. fuel%vstd!array.lemma_array_index_decreases.
  fuel%vstd!function.axiom_fn_mut_call_requires. fuel%vstd!function.axiom_fn_mut_call_ensures.
  fuel%vstd!raw_ptr.impl&%3.view. fuel%vstd!raw_ptr.ptrs_mut_eq. fuel%vstd!raw_ptr.ptrs_mut_eq_sized.
  fuel%vstd!seq.impl&%2.spec_index. fuel%vstd!seq.lemma_seq_index_decreases. fuel%vstd!seq.lemma_seq_new_len.
  fuel%vstd!seq.lemma_seq_new_index. fuel%vstd!seq.lemma_seq_ext_equal. fuel%vstd!seq.lemma_seq_ext_equal_deep.
  fuel%vstd!slice.impl&%2.spec_index. fuel%vstd!slice.axiom_spec_len. fuel%vstd!slice.len%returns_clause_autospec.
  fuel%vstd!slice.axiom_slice_ext_equal. fuel%vstd!slice.axiom_slice_has_resolved.
  fuel%vstd!slice.axiom_slice_decreases_to_seq. fuel%vstd!slice.lemma_slice_index_decreases.
  fuel%vstd!view.impl&%0.view. fuel%vstd!view.impl&%2.view. fuel%vstd!view.impl&%4.view.
  fuel%vstd!view.impl&%6.view. fuel%vstd!view.impl&%16.view. fuel%vstd!view.impl&%18.view.
  fuel%vstd!view.impl&%20.view. fuel%vstd!view.impl&%22.view. fuel%vstd!view.impl&%24.view.
  fuel%vstd!view.impl&%26.view. fuel%vstd!view.impl&%28.view. fuel%vstd!view.impl&%30.view.
  fuel%vstd!view.impl&%32.view. fuel%vstd!view.impl&%34.view. fuel%vstd!view.impl&%36.view.
  fuel%vstd!view.impl&%38.view. fuel%vstd!view.impl&%40.view. fuel%vstd!view.impl&%42.view.
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
  fuel%vstd!map.group_map_lemmas. fuel%vstd!multiset.group_multiset_axioms. fuel%vstd!mut_ref.group_mut_ref_axioms.
  fuel%vstd!raw_ptr.group_raw_ptr_axioms. fuel%vstd!seq.group_seq_lemmas. fuel%vstd!seq_lib.group_filter_ensures.
  fuel%vstd!seq_lib.group_seq_lib_default. fuel%vstd!set.group_set_lemmas. fuel%vstd!set_lib.group_set_lib_default.
  fuel%vstd!slice.group_slice_axioms. fuel%vstd!string.group_string_axioms. fuel%vstd!std_specs.bits.group_bits_axioms.
  fuel%vstd!std_specs.control_flow.group_control_flow_axioms. fuel%vstd!std_specs.fmt.group_fmt_axioms.
  fuel%vstd!std_specs.iter.group_iter_axioms. fuel%vstd!std_specs.manually_drop.group_manually_drop_axioms.
  fuel%vstd!std_specs.btree.group_btree_axioms. fuel%vstd!std_specs.hash.group_hash_axioms.
  fuel%vstd!std_specs.range.group_range_axioms. fuel%vstd!std_specs.vec.group_vec_axioms.
  fuel%vstd!std_specs.vecdeque.group_vec_dequeue_axioms. fuel%vstd!std_specs.nonzero.group_nonzero_axioms.
  fuel%vstd!group_vstd_default.
))
(assert
 (=>
  (fuel_bool_default fuel%vstd!array.group_array_axioms.)
  (and
   (fuel_bool_default fuel%vstd!array.array_len_matches_n.)
   (fuel_bool_default fuel%vstd!array.lemma_array_index.)
   (fuel_bool_default fuel%vstd!array.axiom_array_ext_equal.)
   (fuel_bool_default fuel%vstd!array.axiom_array_has_resolved.)
   (fuel_bool_default fuel%vstd!array.axiom_array_decreases_to_seq.)
   (fuel_bool_default fuel%vstd!array.lemma_array_index_decreases.)
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
   (fuel_bool_default fuel%vstd!seq.lemma_seq_new_len.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_new_index.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal.)
   (fuel_bool_default fuel%vstd!seq.lemma_seq_ext_equal_deep.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!seq_lib.group_seq_lib_default.)
  (fuel_bool_default fuel%vstd!seq_lib.group_filter_ensures.)
))
(assert
 (=>
  (fuel_bool_default fuel%vstd!slice.group_slice_axioms.)
  (and
   (fuel_bool_default fuel%vstd!slice.axiom_spec_len.)
   (fuel_bool_default fuel%vstd!slice.axiom_slice_ext_equal.)
   (fuel_bool_default fuel%vstd!slice.axiom_slice_has_resolved.)
   (fuel_bool_default fuel%vstd!slice.axiom_slice_decreases_to_seq.)
   (fuel_bool_default fuel%vstd!slice.lemma_slice_index_decreases.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!std_specs.vec.group_vec_axioms.)
  (and
   (fuel_bool_default fuel%vstd!std_specs.vec.axiom_spec_len.)
   (fuel_bool_default fuel%vstd!std_specs.vec.axiom_vec_has_resolved.)
   (fuel_bool_default fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view.)
)))
(assert
 (=>
  (fuel_bool_default fuel%vstd!std_specs.nonzero.group_nonzero_axioms.)
  (fuel_bool_default fuel%vstd!std_specs.nonzero.axiom_nonzero_is_not_zero.)
))
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
   (fuel_bool_default fuel%vstd!mut_ref.group_mut_ref_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.range.group_range_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.bits.group_bits_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.control_flow.group_control_flow_axioms.)
   (fuel_bool_default fuel%vstd!std_specs.fmt.group_fmt_axioms.)
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
(declare-fun tr_bound%vstd!view.View. (Dcr Type) Bool)
(declare-fun tr_bound%core!clone.Clone. (Dcr Type) Bool)
(declare-fun tr_bound%core!marker.Copy. (Dcr Type) Bool)
(declare-fun tr_bound%core!convert.From. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%vstd!std_specs.convert.FromSpec. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!marker.Tuple. (Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.FnOnce. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.FnMut. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!ops.function.Fn. (Dcr Type Dcr Type) Bool)
(declare-fun tr_bound%core!alloc.Allocator. (Dcr Type) Bool)
(declare-fun tr_bound%core!num.nonzero.ZeroablePrimitive. (Dcr Type) Bool)
(declare-fun tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. (Dcr Type) Bool)

;; Associated-Type-Decls
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
(declare-sort core!num.nonzero.NonZero<u8.>. 0)
(declare-sort core!num.nonzero.NonZero<u16.>. 0)
(declare-sort core!num.nonzero.NonZero<u32.>. 0)
(declare-sort core!num.nonzero.NonZero<u64.>. 0)
(declare-sort core!num.nonzero.NonZero<u128.>. 0)
(declare-sort core!num.nonzero.NonZero<i8.>. 0)
(declare-sort core!num.nonzero.NonZero<i16.>. 0)
(declare-sort core!num.nonzero.NonZero<i32.>. 0)
(declare-sort core!num.nonzero.NonZero<i64.>. 0)
(declare-sort core!num.nonzero.NonZero<i128.>. 0)
(declare-sort core!num.nonzero.NonZero<usize.>. 0)
(declare-sort core!num.nonzero.NonZero<isize.>. 0)
(declare-sort alloc!alloc.Global. 0)
(declare-sort alloc!vec.Vec<u8./alloc!alloc.Global.>. 0)
(declare-sort vstd!raw_ptr.Provenance. 0)
(declare-sort vstd!seq.Seq<u8.>. 0)
(declare-datatypes ((vstd!raw_ptr.PtrData. 0) (tuple%0. 0)) (((vstd!raw_ptr.PtrData./PtrData
    (vstd!raw_ptr.PtrData./PtrData/?addr Int) (vstd!raw_ptr.PtrData./PtrData/?provenance
     vstd!raw_ptr.Provenance.
    ) (vstd!raw_ptr.PtrData./PtrData/?metadata Poly)
   )
  ) ((tuple%0./tuple%0))
))
(declare-fun vstd!raw_ptr.PtrData./PtrData/addr (vstd!raw_ptr.PtrData.) Int)
(declare-fun vstd!raw_ptr.PtrData./PtrData/provenance (vstd!raw_ptr.PtrData.) vstd!raw_ptr.Provenance.)
(declare-fun vstd!raw_ptr.PtrData./PtrData/metadata (vstd!raw_ptr.PtrData.) Poly)
(declare-fun TYPE%fun%1. (Dcr Type Dcr Type) Type)
(declare-const TYPE%alloc!alloc.Global. Type)
(declare-fun TYPE%alloc!vec.Vec. (Dcr Type Dcr Type) Type)
(declare-fun TYPE%core!num.nonzero.NonZero. (Dcr Type) Type)
(declare-const TYPE%vstd!raw_ptr.Provenance. Type)
(declare-fun TYPE%vstd!raw_ptr.PtrData. (Dcr Type) Type)
(declare-fun TYPE%vstd!seq.Seq. (Dcr Type) Type)
(declare-fun Poly%fun%1. (%%Function%%) Poly)
(declare-fun %Poly%fun%1. (Poly) %%Function%%)
(declare-fun Poly%array%. (%%Function%%) Poly)
(declare-fun %Poly%array%. (Poly) %%Function%%)
(declare-fun Poly%core!num.nonzero.NonZero<u8.>. (core!num.nonzero.NonZero<u8.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<u8.>. (Poly) core!num.nonzero.NonZero<u8.>.)
(declare-fun Poly%core!num.nonzero.NonZero<u16.>. (core!num.nonzero.NonZero<u16.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<u16.>. (Poly) core!num.nonzero.NonZero<u16.>.)
(declare-fun Poly%core!num.nonzero.NonZero<u32.>. (core!num.nonzero.NonZero<u32.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<u32.>. (Poly) core!num.nonzero.NonZero<u32.>.)
(declare-fun Poly%core!num.nonzero.NonZero<u64.>. (core!num.nonzero.NonZero<u64.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<u64.>. (Poly) core!num.nonzero.NonZero<u64.>.)
(declare-fun Poly%core!num.nonzero.NonZero<u128.>. (core!num.nonzero.NonZero<u128.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<u128.>. (Poly) core!num.nonzero.NonZero<u128.>.)
(declare-fun Poly%core!num.nonzero.NonZero<i8.>. (core!num.nonzero.NonZero<i8.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<i8.>. (Poly) core!num.nonzero.NonZero<i8.>.)
(declare-fun Poly%core!num.nonzero.NonZero<i16.>. (core!num.nonzero.NonZero<i16.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<i16.>. (Poly) core!num.nonzero.NonZero<i16.>.)
(declare-fun Poly%core!num.nonzero.NonZero<i32.>. (core!num.nonzero.NonZero<i32.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<i32.>. (Poly) core!num.nonzero.NonZero<i32.>.)
(declare-fun Poly%core!num.nonzero.NonZero<i64.>. (core!num.nonzero.NonZero<i64.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<i64.>. (Poly) core!num.nonzero.NonZero<i64.>.)
(declare-fun Poly%core!num.nonzero.NonZero<i128.>. (core!num.nonzero.NonZero<i128.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<i128.>. (Poly) core!num.nonzero.NonZero<i128.>.)
(declare-fun Poly%core!num.nonzero.NonZero<usize.>. (core!num.nonzero.NonZero<usize.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<usize.>. (Poly) core!num.nonzero.NonZero<usize.>.)
(declare-fun Poly%core!num.nonzero.NonZero<isize.>. (core!num.nonzero.NonZero<isize.>.)
 Poly
)
(declare-fun %Poly%core!num.nonzero.NonZero<isize.>. (Poly) core!num.nonzero.NonZero<isize.>.)
(declare-fun Poly%alloc!alloc.Global. (alloc!alloc.Global.) Poly)
(declare-fun %Poly%alloc!alloc.Global. (Poly) alloc!alloc.Global.)
(declare-fun Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. (alloc!vec.Vec<u8./alloc!alloc.Global.>.)
 Poly
)
(declare-fun %Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. (Poly) alloc!vec.Vec<u8./alloc!alloc.Global.>.)
(declare-fun Poly%vstd!raw_ptr.Provenance. (vstd!raw_ptr.Provenance.) Poly)
(declare-fun %Poly%vstd!raw_ptr.Provenance. (Poly) vstd!raw_ptr.Provenance.)
(declare-fun Poly%vstd!seq.Seq<u8.>. (vstd!seq.Seq<u8.>.) Poly)
(declare-fun %Poly%vstd!seq.Seq<u8.>. (Poly) vstd!seq.Seq<u8.>.)
(declare-fun Poly%vstd!raw_ptr.PtrData. (vstd!raw_ptr.PtrData.) Poly)
(declare-fun %Poly%vstd!raw_ptr.PtrData. (Poly) vstd!raw_ptr.PtrData.)
(declare-fun Poly%tuple%0. (tuple%0.) Poly)
(declare-fun %Poly%tuple%0. (Poly) tuple%0.)
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
 (forall ((x core!num.nonzero.NonZero<u8.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<u8.>. (Poly%core!num.nonzero.NonZero<u8.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<u8.>. x))
   :qid internal_core__num__nonzero__NonZero<u8.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u8.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 8)))
    (= x (Poly%core!num.nonzero.NonZero<u8.>. (%Poly%core!num.nonzero.NonZero<u8.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 8))))
   :qid internal_core__num__nonzero__NonZero<u8.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u8.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u8.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<u8.>. x) (TYPE%core!num.nonzero.NonZero. $
     (UINT 8)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<u8.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (UINT 8)
   )))
   :qid internal_core__num__nonzero__NonZero<u8.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u8.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u16.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<u16.>. (Poly%core!num.nonzero.NonZero<u16.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<u16.>. x))
   :qid internal_core__num__nonzero__NonZero<u16.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u16.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 16)))
    (= x (Poly%core!num.nonzero.NonZero<u16.>. (%Poly%core!num.nonzero.NonZero<u16.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 16))))
   :qid internal_core__num__nonzero__NonZero<u16.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u16.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u16.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<u16.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (UINT 16)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<u16.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (UINT 16)
   )))
   :qid internal_core__num__nonzero__NonZero<u16.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u16.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u32.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<u32.>. (Poly%core!num.nonzero.NonZero<u32.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<u32.>. x))
   :qid internal_core__num__nonzero__NonZero<u32.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u32.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 32)))
    (= x (Poly%core!num.nonzero.NonZero<u32.>. (%Poly%core!num.nonzero.NonZero<u32.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 32))))
   :qid internal_core__num__nonzero__NonZero<u32.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u32.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u32.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<u32.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (UINT 32)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<u32.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (UINT 32)
   )))
   :qid internal_core__num__nonzero__NonZero<u32.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u32.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u64.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<u64.>. (Poly%core!num.nonzero.NonZero<u64.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<u64.>. x))
   :qid internal_core__num__nonzero__NonZero<u64.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u64.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 64)))
    (= x (Poly%core!num.nonzero.NonZero<u64.>. (%Poly%core!num.nonzero.NonZero<u64.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 64))))
   :qid internal_core__num__nonzero__NonZero<u64.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u64.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u64.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<u64.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (UINT 64)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<u64.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (UINT 64)
   )))
   :qid internal_core__num__nonzero__NonZero<u64.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u64.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u128.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<u128.>. (Poly%core!num.nonzero.NonZero<u128.>.
      x
   )))
   :pattern ((Poly%core!num.nonzero.NonZero<u128.>. x))
   :qid internal_core__num__nonzero__NonZero<u128.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u128.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 128)))
    (= x (Poly%core!num.nonzero.NonZero<u128.>. (%Poly%core!num.nonzero.NonZero<u128.>.
       x
   ))))
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (UINT 128))))
   :qid internal_core__num__nonzero__NonZero<u128.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u128.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<u128.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<u128.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (UINT 128)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<u128.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (UINT 128)
   )))
   :qid internal_core__num__nonzero__NonZero<u128.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<u128.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i8.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<i8.>. (Poly%core!num.nonzero.NonZero<i8.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<i8.>. x))
   :qid internal_core__num__nonzero__NonZero<i8.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i8.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 8)))
    (= x (Poly%core!num.nonzero.NonZero<i8.>. (%Poly%core!num.nonzero.NonZero<i8.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 8))))
   :qid internal_core__num__nonzero__NonZero<i8.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i8.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i8.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<i8.>. x) (TYPE%core!num.nonzero.NonZero. $
     (SINT 8)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<i8.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (SINT 8)
   )))
   :qid internal_core__num__nonzero__NonZero<i8.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i8.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i16.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<i16.>. (Poly%core!num.nonzero.NonZero<i16.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<i16.>. x))
   :qid internal_core__num__nonzero__NonZero<i16.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i16.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 16)))
    (= x (Poly%core!num.nonzero.NonZero<i16.>. (%Poly%core!num.nonzero.NonZero<i16.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 16))))
   :qid internal_core__num__nonzero__NonZero<i16.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i16.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i16.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<i16.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (SINT 16)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<i16.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (SINT 16)
   )))
   :qid internal_core__num__nonzero__NonZero<i16.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i16.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i32.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<i32.>. (Poly%core!num.nonzero.NonZero<i32.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<i32.>. x))
   :qid internal_core__num__nonzero__NonZero<i32.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i32.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 32)))
    (= x (Poly%core!num.nonzero.NonZero<i32.>. (%Poly%core!num.nonzero.NonZero<i32.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 32))))
   :qid internal_core__num__nonzero__NonZero<i32.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i32.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i32.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<i32.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (SINT 32)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<i32.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (SINT 32)
   )))
   :qid internal_core__num__nonzero__NonZero<i32.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i32.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i64.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<i64.>. (Poly%core!num.nonzero.NonZero<i64.>. x)))
   :pattern ((Poly%core!num.nonzero.NonZero<i64.>. x))
   :qid internal_core__num__nonzero__NonZero<i64.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i64.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 64)))
    (= x (Poly%core!num.nonzero.NonZero<i64.>. (%Poly%core!num.nonzero.NonZero<i64.>. x)))
   )
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 64))))
   :qid internal_core__num__nonzero__NonZero<i64.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i64.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i64.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<i64.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (SINT 64)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<i64.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (SINT 64)
   )))
   :qid internal_core__num__nonzero__NonZero<i64.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i64.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i128.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<i128.>. (Poly%core!num.nonzero.NonZero<i128.>.
      x
   )))
   :pattern ((Poly%core!num.nonzero.NonZero<i128.>. x))
   :qid internal_core__num__nonzero__NonZero<i128.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i128.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 128)))
    (= x (Poly%core!num.nonzero.NonZero<i128.>. (%Poly%core!num.nonzero.NonZero<i128.>.
       x
   ))))
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ (SINT 128))))
   :qid internal_core__num__nonzero__NonZero<i128.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i128.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<i128.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<i128.>. x) (TYPE%core!num.nonzero.NonZero.
     $ (SINT 128)
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<i128.>. x) (TYPE%core!num.nonzero.NonZero.
      $ (SINT 128)
   )))
   :qid internal_core__num__nonzero__NonZero<i128.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<i128.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<usize.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<usize.>. (Poly%core!num.nonzero.NonZero<usize.>.
      x
   )))
   :pattern ((Poly%core!num.nonzero.NonZero<usize.>. x))
   :qid internal_core__num__nonzero__NonZero<usize.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<usize.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ USIZE))
    (= x (Poly%core!num.nonzero.NonZero<usize.>. (%Poly%core!num.nonzero.NonZero<usize.>.
       x
   ))))
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ USIZE)))
   :qid internal_core__num__nonzero__NonZero<usize.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<usize.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<usize.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<usize.>. x) (TYPE%core!num.nonzero.NonZero.
     $ USIZE
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<usize.>. x) (TYPE%core!num.nonzero.NonZero.
      $ USIZE
   )))
   :qid internal_core__num__nonzero__NonZero<usize.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<usize.>_has_type_always_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<isize.>.)) (!
   (= x (%Poly%core!num.nonzero.NonZero<isize.>. (Poly%core!num.nonzero.NonZero<isize.>.
      x
   )))
   :pattern ((Poly%core!num.nonzero.NonZero<isize.>. x))
   :qid internal_core__num__nonzero__NonZero<isize.>_box_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<isize.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%core!num.nonzero.NonZero. $ ISIZE))
    (= x (Poly%core!num.nonzero.NonZero<isize.>. (%Poly%core!num.nonzero.NonZero<isize.>.
       x
   ))))
   :pattern ((has_type x (TYPE%core!num.nonzero.NonZero. $ ISIZE)))
   :qid internal_core__num__nonzero__NonZero<isize.>_unbox_axiom_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<isize.>_unbox_axiom_definition
)))
(assert
 (forall ((x core!num.nonzero.NonZero<isize.>.)) (!
   (has_type (Poly%core!num.nonzero.NonZero<isize.>. x) (TYPE%core!num.nonzero.NonZero.
     $ ISIZE
   ))
   :pattern ((has_type (Poly%core!num.nonzero.NonZero<isize.>. x) (TYPE%core!num.nonzero.NonZero.
      $ ISIZE
   )))
   :qid internal_core__num__nonzero__NonZero<isize.>_has_type_always_definition
   :skolemid skolem_internal_core__num__nonzero__NonZero<isize.>_has_type_always_definition
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
 (forall ((x alloc!vec.Vec<u8./alloc!alloc.Global.>.)) (!
   (= x (%Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>.
      x
   )))
   :pattern ((Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. x))
   :qid internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_box_axiom_definition
   :skolemid skolem_internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_box_axiom_definition
)))
(assert
 (forall ((x Poly)) (!
   (=>
    (has_type x (TYPE%alloc!vec.Vec. $ (UINT 8) $ TYPE%alloc!alloc.Global.))
    (= x (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. (%Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>.
       x
   ))))
   :pattern ((has_type x (TYPE%alloc!vec.Vec. $ (UINT 8) $ TYPE%alloc!alloc.Global.)))
   :qid internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_unbox_axiom_definition
   :skolemid skolem_internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_unbox_axiom_definition
)))
(assert
 (forall ((x alloc!vec.Vec<u8./alloc!alloc.Global.>.)) (!
   (has_type (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. x) (TYPE%alloc!vec.Vec. $ (
      UINT 8
     ) $ TYPE%alloc!alloc.Global.
   ))
   :pattern ((has_type (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. x) (TYPE%alloc!vec.Vec.
      $ (UINT 8) $ TYPE%alloc!alloc.Global.
   )))
   :qid internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_has_type_always_definition
   :skolemid skolem_internal_alloc__vec__Vec<u8./alloc!alloc.Global.>_has_type_always_definition
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
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (tr_bound%core!convert.From. Self%&. Self%& T&. T&)
    (and
     (sized Self%&.)
     (sized T&.)
   ))
   :pattern ((tr_bound%core!convert.From. Self%&. Self%& T&. T&))
   :qid internal_core__convert__From_trait_type_bounds_definition
   :skolemid skolem_internal_core__convert__From_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (=>
    (tr_bound%vstd!std_specs.convert.FromSpec. Self%&. Self%& T&. T&)
    (and
     (sized Self%&.)
     (tr_bound%core!convert.From. Self%&. Self%& T&. T&)
     (sized T&.)
   ))
   :pattern ((tr_bound%vstd!std_specs.convert.FromSpec. Self%&. Self%& T&. T&))
   :qid internal_vstd__std_specs__convert__FromSpec_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__std_specs__convert__FromSpec_trait_type_bounds_definition
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
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%core!num.nonzero.ZeroablePrimitive. Self%&. Self%&)
    (and
     (sized Self%&.)
     (tr_bound%core!marker.Copy. Self%&. Self%&)
   ))
   :pattern ((tr_bound%core!num.nonzero.ZeroablePrimitive. Self%&. Self%&))
   :qid internal_core__num__nonzero__ZeroablePrimitive_trait_type_bounds_definition
   :skolemid skolem_internal_core__num__nonzero__ZeroablePrimitive_trait_type_bounds_definition
)))
(assert
 (forall ((Self%&. Dcr) (Self%& Type)) (!
   (=>
    (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. Self%&. Self%&)
    (and
     (sized Self%&.)
     (tr_bound%core!marker.Copy. Self%&. Self%&)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. Self%&. Self%&)
   ))
   :pattern ((tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. Self%&. Self%&))
   :qid internal_vstd__std_specs__nonzero__ZeroablePrimitiveSpec_trait_type_bounds_definition
   :skolemid skolem_internal_vstd__std_specs__nonzero__ZeroablePrimitiveSpec_trait_type_bounds_definition
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
   :qid internal_proj____vstd!view.View./V_vstd__array__impl&__0_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__array__impl&__0_assoc_type_impl_true_definition
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
   :qid internal_proj__vstd!view.View./V_vstd__array__impl&__0_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__array__impl&__0_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%%vstd!view.View./V $ (PTR T&. T&)) $)
   :pattern ((proj%%vstd!view.View./V $ (PTR T&. T&)))
   :qid internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%vstd!view.View./V $ (PTR T&. T&)) (TYPE%vstd!raw_ptr.PtrData. T&. T&))
   :pattern ((proj%vstd!view.View./V $ (PTR T&. T&)))
   :qid internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__2_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)) $)
   :pattern ((proj%%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
   :qid internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (= (proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)) (TYPE%vstd!raw_ptr.PtrData.
     T&. T&
   ))
   :pattern ((proj%vstd!view.View./V (CONST_PTR $) (PTR T&. T&)))
   :qid internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__raw_ptr__impl&__3_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%%vstd!view.View./V $slice (SLICE T&. T&)) $)
   )
   :pattern ((proj%%vstd!view.View./V $slice (SLICE T&. T&)))
   :qid internal_proj____vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (= (proj%vstd!view.View./V $slice (SLICE T&. T&)) (TYPE%vstd!seq.Seq. T&. T&))
   )
   :pattern ((proj%vstd!view.View./V $slice (SLICE T&. T&)))
   :qid internal_proj__vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__slice__impl&__0_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%%vstd!view.View./V (REF A&.) A&) (proj%%vstd!view.View./V A&. A&))
   )
   :pattern ((proj%%vstd!view.View./V (REF A&.) A&))
   :qid internal_proj____vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%vstd!view.View./V (REF A&.) A&) (proj%vstd!view.View./V A&. A&))
   )
   :pattern ((proj%vstd!view.View./V (REF A&.) A&))
   :qid internal_proj__vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__0_assoc_type_impl_false_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&) (proj%%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj____vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_true_definition
)))
(assert
 (forall ((A&. Dcr) (A& Type)) (!
   (=>
    (tr_bound%vstd!view.View. A&. A&)
    (= (proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&) (proj%vstd!view.View./V
      A&. A&
   )))
   :pattern ((proj%vstd!view.View./V (BOX $ TYPE%alloc!alloc.Global. A&.) A&))
   :qid internal_proj__vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__2_assoc_type_impl_false_definition
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
   :qid internal_proj____vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_true_definition
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
   :qid internal_proj__vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__4_assoc_type_impl_false_definition
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
   :qid internal_proj____vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_true_definition
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
   :qid internal_proj__vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__6_assoc_type_impl_false_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (= (proj%%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)) $)
   )
   :pattern ((proj%%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
   :qid internal_proj____vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (= (proj%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)) (TYPE%vstd!seq.Seq.
      T&. T&
   )))
   :pattern ((proj%vstd!view.View./V $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
   :qid internal_proj__vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__view__impl&__8_assoc_type_impl_false_definition
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
 (= (proj%%vstd!view.View./V $ (UINT 16)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (UINT 16)) (UINT 16))
)
(assert
 (= (proj%%vstd!view.View./V $ (UINT 32)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (UINT 32)) (UINT 32))
)
(assert
 (= (proj%%vstd!view.View./V $ (UINT 64)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (UINT 64)) (UINT 64))
)
(assert
 (= (proj%%vstd!view.View./V $ (UINT 128)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (UINT 128)) (UINT 128))
)
(assert
 (= (proj%%vstd!view.View./V $ USIZE) $)
)
(assert
 (= (proj%vstd!view.View./V $ USIZE) USIZE)
)
(assert
 (= (proj%%vstd!view.View./V $ (SINT 8)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (SINT 8)) (SINT 8))
)
(assert
 (= (proj%%vstd!view.View./V $ (SINT 16)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (SINT 16)) (SINT 16))
)
(assert
 (= (proj%%vstd!view.View./V $ (SINT 32)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (SINT 32)) (SINT 32))
)
(assert
 (= (proj%%vstd!view.View./V $ (SINT 64)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (SINT 64)) (SINT 64))
)
(assert
 (= (proj%%vstd!view.View./V $ (SINT 128)) $)
)
(assert
 (= (proj%vstd!view.View./V $ (SINT 128)) (SINT 128))
)
(assert
 (= (proj%%vstd!view.View./V $ ISIZE) $)
)
(assert
 (= (proj%vstd!view.View./V $ ISIZE) ISIZE)
)
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (= (proj%%vstd!view.View./V $ (TYPE%core!num.nonzero.NonZero. T&. T&)) T&.)
   )
   :pattern ((proj%%vstd!view.View./V $ (TYPE%core!num.nonzero.NonZero. T&. T&)))
   :qid internal_proj____vstd!view.View./V_vstd__std_specs__nonzero__impl&__11_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____vstd!view.View./V_vstd__std_specs__nonzero__impl&__11_assoc_type_impl_true_definition
)))
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (= (proj%vstd!view.View./V $ (TYPE%core!num.nonzero.NonZero. T&. T&)) T&)
   )
   :pattern ((proj%vstd!view.View./V $ (TYPE%core!num.nonzero.NonZero. T&. T&)))
   :qid internal_proj__vstd!view.View./V_vstd__std_specs__nonzero__impl&__11_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__vstd!view.View./V_vstd__std_specs__nonzero__impl&__11_assoc_type_impl_false_definition
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
   :qid internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_true_definition
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
   :qid internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__2_assoc_type_impl_false_definition
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
   :qid internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_true_definition
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
   :qid internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_core__ops__function__impls__impl&__4_assoc_type_impl_false_definition
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
   :qid internal_proj____core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_true_definition
   :skolemid skolem_internal_proj____core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_true_definition
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
   :qid internal_proj__core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_false_definition
   :skolemid skolem_internal_proj__core!ops.function.FnOnce./Output_alloc__boxed__impl&__31_assoc_type_impl_false_definition
)))

;; Function-Decl vstd::seq::Seq::len
(declare-fun vstd!seq.Seq.len.? (Dcr Type Poly) Int)

;; Function-Decl vstd::seq::Seq::index
(declare-fun vstd!seq.Seq.index.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::impl&%2::spec_index
(declare-fun vstd!seq.impl&%2.spec_index.? (Dcr Type Poly Poly) Poly)

;; Function-Decl vstd::seq::Seq::new
(declare-fun vstd!seq.Seq.new.? (Dcr Type Poly Poly) Poly)

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

;; Function-Decl vstd::std_specs::vec::spec_vec_len
(declare-fun vstd!std_specs.vec.spec_vec_len.? (Dcr Type Dcr Type Poly) Int)

;; Function-Decl vstd::std_specs::nonzero::ZeroablePrimitiveSpec::is_zero
(declare-fun vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? (Dcr Type Poly)
 Poly
)
(declare-fun vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero%default%.? (Dcr Type
  Poly
 ) Poly
)

;; Function-Decl vstd::std_specs::convert::FromSpec::obeys_from_spec
(declare-fun vstd!std_specs.convert.FromSpec.obeys_from_spec.? (Dcr Type Dcr Type)
 Poly
)
(declare-fun vstd!std_specs.convert.FromSpec.obeys_from_spec%default%.? (Dcr Type Dcr
  Type
 ) Poly
)

;; Function-Decl vstd::std_specs::convert::FromSpec::from_spec
(declare-fun vstd!std_specs.convert.FromSpec.from_spec.? (Dcr Type Dcr Type Poly)
 Poly
)
(declare-fun vstd!std_specs.convert.FromSpec.from_spec%default%.? (Dcr Type Dcr Type
  Poly
 ) Poly
)

;; Function-Decl vstd::std_specs::nonzero::nonzero_spec_get
(declare-fun vstd!std_specs.nonzero.nonzero_spec_get.? (Dcr Type Poly) Poly)

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
    :qid user_vstd__seq__lemma_seq_new_len_0
    :skolemid skolem_user_vstd__seq__lemma_seq_new_len_0
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
    :qid user_vstd__seq__lemma_seq_new_index_0
    :skolemid skolem_user_vstd__seq__lemma_seq_new_index_0
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
          :qid user_vstd__seq__lemma_seq_ext_equal_0
          :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_0
    ))))))
    :pattern ((ext_eq false (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
    :qid user_vstd__seq__lemma_seq_ext_equal_1
    :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_1
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
          :qid user_vstd__seq__lemma_seq_ext_equal_deep_0
          :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_0
    ))))))
    :pattern ((ext_eq true (TYPE%vstd!seq.Seq. A&. A&) s1! s2!))
    :qid user_vstd__seq__lemma_seq_ext_equal_deep_1
    :skolemid skolem_user_vstd__seq__lemma_seq_ext_equal_deep_1
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
    :qid user_vstd__function__axiom_fn_mut_call_requires_0
    :skolemid skolem_user_vstd__function__axiom_fn_mut_call_requires_0
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
    :qid user_vstd__function__axiom_fn_mut_call_ensures_0
    :skolemid skolem_user_vstd__function__axiom_fn_mut_call_ensures_0
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
    :qid user_vstd__slice__axiom_spec_len_0
    :skolemid skolem_user_vstd__slice__axiom_spec_len_0
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
(declare-const %%global_location_label%%2 Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (= (req%vstd!slice.SliceAdditionalSpecFns.spec_index. Self%&. Self%& T&. T& self! i!)
    (=>
     %%global_location_label%%2
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
    :qid internal_vstd!slice.impl&__2.spec_index.?_definition
    :skolemid skolem_internal_vstd!slice.impl&__2.spec_index.?_definition
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
          :qid user_vstd__slice__axiom_slice_ext_equal_0
          :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_0
    ))))))
    :pattern ((ext_eq false (SLICE T&. T&) a1! a2!))
    :qid user_vstd__slice__axiom_slice_ext_equal_1
    :skolemid skolem_user_vstd__slice__axiom_slice_ext_equal_1
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
    :qid user_vstd__slice__axiom_slice_has_resolved_0
    :skolemid skolem_user_vstd__slice__axiom_slice_has_resolved_0
))))

;; Broadcast vstd::slice::axiom_slice_decreases_to_seq
(assert
 (=>
  (fuel_bool fuel%vstd!slice.axiom_slice_decreases_to_seq.)
  (forall ((T&. Dcr) (T& Type) (s! Poly)) (!
    (=>
     (has_type s! (SLICE T&. T&))
     (=>
      (sized T&.)
      (height_lt (height (vstd!view.View.view.? $slice (SLICE T&. T&) s!)) (height s!))
    ))
    :pattern ((height (vstd!view.View.view.? $slice (SLICE T&. T&) s!)))
    :qid user_vstd__slice__axiom_slice_decreases_to_seq_0
    :skolemid skolem_user_vstd__slice__axiom_slice_decreases_to_seq_0
))))

;; Broadcast vstd::slice::lemma_slice_index_decreases
(assert
 (=>
  (fuel_bool fuel%vstd!slice.lemma_slice_index_decreases.)
  (forall ((T&. Dcr) (T& Type) (s! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type s! (SLICE T&. T&))
      (has_type i! INT)
     )
     (=>
      (and
       (sized T&.)
       (let
        ((tmp%%$ 0))
        (let
         ((tmp%%$1 (%I i!)))
         (let
          ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $slice (SLICE T&. T&) s!))))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (height_lt (height (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&.
           T&
          ) s!
         ) i!
        )
       ) (height s!)
    )))
    :pattern ((height (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $slice (SLICE T&.
         T&
        ) s!
       ) i!
    )))
    :qid user_vstd__slice__lemma_slice_index_decreases_0
    :skolemid skolem_user_vstd__slice__lemma_slice_index_decreases_0
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
    :qid internal_vstd!array.impl&__0.view.?_definition
    :skolemid skolem_internal_vstd!array.impl&__0.view.?_definition
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
    :qid user_vstd__array__array_len_matches_n_0
    :skolemid skolem_user_vstd__array__array_len_matches_n_0
))))

;; Function-Specs vstd::array::ArrayAdditionalSpecFns::spec_index
(declare-fun req%vstd!array.ArrayAdditionalSpecFns.spec_index. (Dcr Type Dcr Type Poly
  Poly
 ) Bool
)
(declare-const %%global_location_label%%3 Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (self! Poly) (i! Poly)) (
   !
   (= (req%vstd!array.ArrayAdditionalSpecFns.spec_index. Self%&. Self%& T&. T& self! i!)
    (=>
     %%global_location_label%%3
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
    :qid internal_vstd!array.impl&__2.spec_index.?_definition
    :skolemid skolem_internal_vstd!array.impl&__2.spec_index.?_definition
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
    :qid user_vstd__array__lemma_array_index_0
    :skolemid skolem_user_vstd__array__lemma_array_index_0
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
         :qid user_vstd__array__axiom_array_ext_equal_0
         :skolemid skolem_user_vstd__array__axiom_array_ext_equal_0
    )))))
    :pattern ((ext_eq false (ARRAY T&. T& N&. N&) a1! a2!))
    :qid user_vstd__array__axiom_array_ext_equal_1
    :skolemid skolem_user_vstd__array__axiom_array_ext_equal_1
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
    :qid user_vstd__array__axiom_array_has_resolved_0
    :skolemid skolem_user_vstd__array__axiom_array_has_resolved_0
))))

;; Broadcast vstd::array::axiom_array_decreases_to_seq
(assert
 (=>
  (fuel_bool fuel%vstd!array.axiom_array_decreases_to_seq.)
  (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (a! Poly)) (!
    (=>
     (has_type a! (ARRAY T&. T& N&. N&))
     (=>
      (and
       (sized T&.)
       (uInv SZ (const_int N&))
      )
      (height_lt (height (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a!)) (height a!))
    ))
    :pattern ((height (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a!)))
    :qid user_vstd__array__axiom_array_decreases_to_seq_0
    :skolemid skolem_user_vstd__array__axiom_array_decreases_to_seq_0
))))

;; Broadcast vstd::array::lemma_array_index_decreases
(assert
 (=>
  (fuel_bool fuel%vstd!array.lemma_array_index_decreases.)
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
          ((tmp%%$2 (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) a!))))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
      )))))
      (height_lt (height (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T&
           N&. N&
          ) a!
         ) i!
        )
       ) (height a!)
    )))
    :pattern ((height (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T&
         N&. N&
        ) a!
       ) i!
    )))
    :qid user_vstd__array__lemma_array_index_decreases_0
    :skolemid skolem_user_vstd__array__lemma_array_index_decreases_0
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
    :qid user_vstd__raw_ptr__ptrs_mut_eq_0
    :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_0
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
    :qid user_vstd__raw_ptr__ptrs_mut_eq_sized_0
    :skolemid skolem_user_vstd__raw_ptr__ptrs_mut_eq_sized_0
))))

;; Function-Axioms vstd::std_specs::vec::spec_vec_len
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (v! Poly)) (!
   (=>
    (has_type v! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
    (uInv SZ (vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!))
   )
   :pattern ((vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!))
   :qid internal_vstd!std_specs.vec.spec_vec_len.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.vec.spec_vec_len.?_pre_post_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%vstd!view.View. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&))
   )
   :pattern ((tr_bound%vstd!view.View. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
   :qid internal_vstd__view__impl&__8_trait_impl_definition
   :skolemid skolem_internal_vstd__view__impl&__8_trait_impl_definition
)))

;; Broadcast vstd::std_specs::vec::axiom_spec_len
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.vec.axiom_spec_len.)
  (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (v! Poly)) (!
    (=>
     (has_type v! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
     (=>
      (and
       (and
        (sized T&.)
        (sized A&.)
       )
       (tr_bound%core!alloc.Allocator. A&. A&)
      )
      (= (vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!) (vstd!seq.Seq.len.? T&. T&
        (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) v!)
    ))))
    :pattern ((vstd!std_specs.vec.spec_vec_len.? T&. T& A&. A& v!))
    :qid user_vstd__std_specs__vec__axiom_spec_len_0
    :skolemid skolem_user_vstd__std_specs__vec__axiom_spec_len_0
))))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!alloc.Allocator. $ TYPE%alloc!alloc.Global.)
)

;; Broadcast vstd::std_specs::vec::axiom_vec_has_resolved
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.vec.axiom_vec_has_resolved.)
  (forall ((T&. Dcr) (T& Type) (vec! Poly) (i! Poly)) (!
    (=>
     (and
      (has_type vec! (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.))
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
          ((tmp%%$2 (vstd!std_specs.vec.spec_vec_len.? T&. T& $ TYPE%alloc!alloc.Global. vec!)))
          (and
           (<= tmp%%$ tmp%%$1)
           (< tmp%%$1 tmp%%$2)
       ))))
       (=>
        (has_resolved $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.) vec!)
        (has_resolved T&. T& (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec.
            T&. T& $ TYPE%alloc!alloc.Global.
           ) vec!
          ) i!
    ))))))
    :pattern ((has_resolved $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.) vec!)
     (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $
        TYPE%alloc!alloc.Global.
       ) vec!
      ) i!
    ))
    :qid user_vstd__std_specs__vec__axiom_vec_has_resolved_0
    :skolemid skolem_user_vstd__std_specs__vec__axiom_vec_has_resolved_0
))))

;; Broadcast vstd::std_specs::vec::axiom_vec_decreases_to_view
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.vec.axiom_vec_decreases_to_view.)
  (forall ((T&. Dcr) (T& Type) (v! Poly)) (!
    (=>
     (has_type v! (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.))
     (=>
      (sized T&.)
      (height_lt (height (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
         v!
        )
       ) (height v!)
    )))
    :pattern ((height (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
       v!
    )))
    :qid user_vstd__std_specs__vec__axiom_vec_decreases_to_view_0
    :skolemid skolem_user_vstd__std_specs__vec__axiom_vec_decreases_to_view_0
))))

;; Function-Axioms vstd::std_specs::nonzero::ZeroablePrimitiveSpec::is_zero
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (self! Poly)) (!
   (=>
    (has_type self! Self%&)
    (has_type (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? Self%&. Self%& self!)
     BOOL
   ))
   :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? Self%&. Self%& self!))
   :qid internal_vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.?_pre_post_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((VERUS_SPEC__A&. Dcr) (VERUS_SPEC__A& Type)) (!
   (=>
    (and
     (sized VERUS_SPEC__A&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. VERUS_SPEC__A&. VERUS_SPEC__A&)
    )
    (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. VERUS_SPEC__A&. VERUS_SPEC__A&)
   )
   :pattern ((tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. VERUS_SPEC__A&. VERUS_SPEC__A&))
   :qid internal_vstd__std_specs__nonzero__impl&__17_trait_impl_definition
   :skolemid skolem_internal_vstd__std_specs__nonzero__impl&__17_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (tr_bound%vstd!view.View. $ (TYPE%core!num.nonzero.NonZero. T&. T&))
   )
   :pattern ((tr_bound%vstd!view.View. $ (TYPE%core!num.nonzero.NonZero. T&. T&)))
   :qid internal_vstd__std_specs__nonzero__impl&__11_trait_impl_definition
   :skolemid skolem_internal_vstd__std_specs__nonzero__impl&__11_trait_impl_definition
)))

;; Broadcast vstd::std_specs::nonzero::axiom_nonzero_is_not_zero
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.axiom_nonzero_is_not_zero.)
  (forall ((T&. Dcr) (T& Type) (n! Poly)) (!
    (=>
     (has_type n! (TYPE%core!num.nonzero.NonZero. T&. T&))
     (=>
      (and
       (sized T&.)
       (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
      )
      (not (%B (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? T&. T& (vstd!view.View.view.?
          $ (TYPE%core!num.nonzero.NonZero. T&. T&) n!
    ))))))
    :pattern ((vstd!view.View.view.? $ (TYPE%core!num.nonzero.NonZero. T&. T&) n!))
    :qid user_vstd__std_specs__nonzero__axiom_nonzero_is_not_zero_0
    :skolemid skolem_user_vstd__std_specs__nonzero__axiom_nonzero_is_not_zero_0
))))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Tuple. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ TYPE%tuple%0.)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ TYPE%tuple%0.)
)

;; Function-Axioms vstd::std_specs::convert::FromSpec::obeys_from_spec
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type)) (!
   (has_type (vstd!std_specs.convert.FromSpec.obeys_from_spec.? Self%&. Self%& T&. T&)
    BOOL
   )
   :pattern ((vstd!std_specs.convert.FromSpec.obeys_from_spec.? Self%&. Self%& T&. T&))
   :qid internal_vstd!std_specs.convert.FromSpec.obeys_from_spec.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.convert.FromSpec.obeys_from_spec.?_pre_post_definition
)))

;; Function-Axioms vstd::std_specs::convert::FromSpec::from_spec
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (v! Poly)) (!
   (=>
    (has_type v! T&)
    (has_type (vstd!std_specs.convert.FromSpec.from_spec.? Self%&. Self%& T&. T& v!) Self%&)
   )
   :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? Self%&. Self%& T&. T& v!))
   :qid internal_vstd!std_specs.convert.FromSpec.from_spec.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.convert.FromSpec.from_spec.?_pre_post_definition
)))

;; Function-Specs core::convert::From::from
(declare-fun ens%core!convert.From.from. (Dcr Type Dcr Type Poly Poly) Bool)
(assert
 (forall ((Self%&. Dcr) (Self%& Type) (T&. Dcr) (T& Type) (v! Poly) (ret! Poly)) (!
   (= (ens%core!convert.From.from. Self%&. Self%& T&. T& v! ret!) (and
     (has_type ret! Self%&)
     (=>
      (%B (vstd!std_specs.convert.FromSpec.obeys_from_spec.? Self%&. Self%& T&. T&))
      (= ret! (vstd!std_specs.convert.FromSpec.from_spec.? Self%&. Self%& T&. T& v!))
   )))
   :pattern ((ens%core!convert.From.from. Self%&. Self%& T&. T& v! ret!))
   :qid internal_ens__core!convert.From.from._definition
   :skolemid skolem_internal_ens__core!convert.From.from._definition
)))

;; Function-Specs alloc::vec::impl&%37::from
(declare-fun ens%alloc!vec.impl&%37.from. (Dcr Type Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (s! Poly) (result! Poly)) (!
   (= (ens%alloc!vec.impl&%37.from. T&. T& N&. N& s! result!) (and
     (ens%core!convert.From.from. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
      $ (ARRAY T&. T& N&. N&) s! result!
     )
     (= (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
       result!
      ) (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) s!)
   )))
   :pattern ((ens%alloc!vec.impl&%37.from. T&. T& N&. N& s! result!))
   :qid internal_ens__alloc!vec.impl&__37.from._definition
   :skolemid skolem_internal_ens__alloc!vec.impl&__37.from._definition
)))

;; Function-Specs alloc::vec::impl&%39::from
(declare-fun ens%alloc!vec.impl&%39.from. (Dcr Type Dcr Type Poly Poly) Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (s! Poly) (result! Poly)) (!
   (= (ens%alloc!vec.impl&%39.from. T&. T& A&. A& s! result!) (and
     (ens%core!convert.From.from. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) (BOX A&. A& $slice)
      (SLICE T&. T&) s! result!
     )
     (= (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) result!) (vstd!view.View.view.?
       $slice (SLICE T&. T&) s!
   ))))
   :pattern ((ens%alloc!vec.impl&%39.from. T&. T& A&. A& s! result!))
   :qid internal_ens__alloc!vec.impl&__39.from._definition
   :skolemid skolem_internal_ens__alloc!vec.impl&__39.from._definition
)))

;; Function-Axioms vstd::std_specs::convert::impl&%6::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%6.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%6.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 16) $ (UINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%6::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%6.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%6.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 16) $ (UINT 8) v!) (I (uClip
       16 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 16) $ (UINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__6.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__6.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%7::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%7.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%7.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 32) $ (UINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%7::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%7.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%7.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 32) $ (UINT 8) v!) (I (uClip
       32 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 32) $ (UINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__7.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__7.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%8::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%8.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%8.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 64) $ (UINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%8::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%8.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%8.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 8) v!) (I (uClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__8.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__8.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%9::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%9.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%9.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ USIZE $ (UINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%9::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%9.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%9.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ USIZE $ (UINT 8) v!) (I (uClip SZ
       (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ USIZE $ (UINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__9.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__9.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%10::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%10.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%10.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 128) $ (UINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%10::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%10.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%10.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 8) v!) (I (uClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__10.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__10.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%11::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%11.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%11.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 32) $ (UINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%11::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%11.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%11.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 32) $ (UINT 16) v!) (I (uClip
       32 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 32) $ (UINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__11.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__11.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%12::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%12.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%12.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 64) $ (UINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%12::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%12.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%12.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 16) v!) (I (uClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__12.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__12.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%13::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%13.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%13.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ USIZE $ (UINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%13::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%13.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%13.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ USIZE $ (UINT 16) v!) (I (uClip SZ
       (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ USIZE $ (UINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__13.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__13.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%14::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%14.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%14.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 128) $ (UINT 16)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%14::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%14.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%14.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 16) v!) (I (uClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__14.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__14.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%15::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%15.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%15.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 64) $ (UINT 32)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%15::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%15.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%15.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 32) v!) (I (uClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 64) $ (UINT 32) v!))
    :qid internal_vstd!std_specs.convert.impl&__15.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__15.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%16::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%16.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%16.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 128) $ (UINT 32)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%16::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%16.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%16.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 32) v!) (I (uClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 32) v!))
    :qid internal_vstd!std_specs.convert.impl&__16.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__16.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%17::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%17.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%17.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (UINT 128) $ (UINT 64)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%17::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%17.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%17.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 64) v!) (I (uClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (UINT 128) $ (UINT 64) v!))
    :qid internal_vstd!std_specs.convert.impl&__17.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__17.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%18::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%18.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%18.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 16) $ (SINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%18::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%18.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%18.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 16) $ (SINT 8) v!) (I (iClip
       16 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 16) $ (SINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__18.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__18.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%19::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%19.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%19.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 32) $ (SINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%19::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%19.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%19.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 32) $ (SINT 8) v!) (I (iClip
       32 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 32) $ (SINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__19.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__19.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%20::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%20.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%20.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 64) $ (SINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%20::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%20.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%20.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 8) v!) (I (iClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__20.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__20.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%21::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%21.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%21.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ ISIZE $ (SINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%21::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%21.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%21.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ ISIZE $ (SINT 8) v!) (I (iClip SZ
       (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ ISIZE $ (SINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__21.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__21.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%22::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%22.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%22.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 128) $ (SINT 8)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%22::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%22.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%22.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 8) v!) (I (iClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 8) v!))
    :qid internal_vstd!std_specs.convert.impl&__22.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__22.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%23::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%23.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%23.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 32) $ (SINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%23::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%23.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%23.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 32) $ (SINT 16) v!) (I (iClip
       32 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 32) $ (SINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__23.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__23.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%24::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%24.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%24.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 64) $ (SINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%24::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%24.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%24.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 16) v!) (I (iClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__24.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__24.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%25::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%25.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%25.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ ISIZE $ (SINT 16)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%25::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%25.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%25.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ ISIZE $ (SINT 16) v!) (I (iClip SZ
       (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ ISIZE $ (SINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__25.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__25.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%26::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%26.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%26.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 128) $ (SINT 16)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%26::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%26.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%26.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 16) v!) (I (iClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 16) v!))
    :qid internal_vstd!std_specs.convert.impl&__26.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__26.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%27::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%27.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%27.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 64) $ (SINT 32)) (B true))
))

;; Function-Axioms vstd::std_specs::convert::impl&%27::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%27.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%27.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 32) v!) (I (iClip
       64 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 64) $ (SINT 32) v!))
    :qid internal_vstd!std_specs.convert.impl&__27.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__27.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%28::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%28.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%28.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 128) $ (SINT 32)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%28::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%28.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%28.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 32) v!) (I (iClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 32) v!))
    :qid internal_vstd!std_specs.convert.impl&__28.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__28.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::convert::impl&%29::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%29.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%29.obeys_from_spec.)
  (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? $ (SINT 128) $ (SINT 64)) (B
    true
))))

;; Function-Axioms vstd::std_specs::convert::impl&%29::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.convert.impl&%29.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.convert.impl&%29.from_spec.)
  (forall ((v! Poly)) (!
    (= (vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 64) v!) (I (iClip
       128 (%I v!)
    )))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? $ (SINT 128) $ (SINT 64) v!))
    :qid internal_vstd!std_specs.convert.impl&__29.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.convert.impl&__29.from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%1::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%1.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%1.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 8) self!) (B (= (
        %I self!
       ) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 8) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__1.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__1.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%2::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%2.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%2.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 16) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 16) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__2.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__2.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%3::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%3.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%3.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 32) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 32) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__3.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__3.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%4::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%4.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%4.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 64) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (UINT 64) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__4.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__4.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%5::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%5.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%5.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ USIZE self!) (B (= (%I self!)
       0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ USIZE self!))
    :qid internal_vstd!std_specs.nonzero.impl&__5.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__5.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%6::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%6.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%6.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 8) self!) (B (= (
        %I self!
       ) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 8) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__6.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__6.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%7::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%7.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%7.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 16) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 16) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__7.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__7.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%8::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%8.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%8.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 32) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 32) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__8.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__8.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%9::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%9.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%9.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 64) self!) (B (=
       (%I self!) 0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ (SINT 64) self!))
    :qid internal_vstd!std_specs.nonzero.impl&__9.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__9.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%10::is_zero
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%10.is_zero.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%10.is_zero.)
  (forall ((self! Poly)) (!
    (= (vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ ISIZE self!) (B (= (%I self!)
       0
    )))
    :pattern ((vstd!std_specs.nonzero.ZeroablePrimitiveSpec.is_zero.? $ ISIZE self!))
    :qid internal_vstd!std_specs.nonzero.impl&__10.is_zero.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__10.is_zero.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::nonzero_spec_get
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.nonzero_spec_get.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.nonzero_spec_get.)
  (forall ((T&. Dcr) (T& Type) (n! Poly)) (!
    (= (vstd!std_specs.nonzero.nonzero_spec_get.? T&. T& n!) (vstd!view.View.view.? $ (
       TYPE%core!num.nonzero.NonZero. T&. T&
      ) n!
    ))
    :pattern ((vstd!std_specs.nonzero.nonzero_spec_get.? T&. T& n!))
    :qid internal_vstd!std_specs.nonzero.nonzero_spec_get.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.nonzero_spec_get.?_definition
))))
(assert
 (forall ((T&. Dcr) (T& Type) (n! Poly)) (!
   (=>
    (has_type n! (TYPE%core!num.nonzero.NonZero. T&. T&))
    (has_type (vstd!std_specs.nonzero.nonzero_spec_get.? T&. T& n!) T&)
   )
   :pattern ((vstd!std_specs.nonzero.nonzero_spec_get.? T&. T& n!))
   :qid internal_vstd!std_specs.nonzero.nonzero_spec_get.?_pre_post_definition
   :skolemid skolem_internal_vstd!std_specs.nonzero.nonzero_spec_get.?_pre_post_definition
)))

;; Function-Axioms vstd::std_specs::nonzero::impl&%16::obeys_from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%16.obeys_from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%16.obeys_from_spec.)
  (forall ((T&. Dcr) (T& Type)) (!
    (=>
     (and
      (sized T&.)
      (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
     )
     (= (vstd!std_specs.convert.FromSpec.obeys_from_spec.? T&. T& $ (TYPE%core!num.nonzero.NonZero.
        T&. T&
       )
      ) (B true)
    ))
    :pattern ((vstd!std_specs.convert.FromSpec.obeys_from_spec.? T&. T& $ (TYPE%core!num.nonzero.NonZero.
       T&. T&
    )))
    :qid internal_vstd!std_specs.nonzero.impl&__16.obeys_from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__16.obeys_from_spec.?_definition
))))

;; Function-Axioms vstd::std_specs::nonzero::impl&%16::from_spec
(assert
 (fuel_bool_default fuel%vstd!std_specs.nonzero.impl&%16.from_spec.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!std_specs.nonzero.impl&%16.from_spec.)
  (forall ((T&. Dcr) (T& Type) (nz! Poly)) (!
    (=>
     (and
      (sized T&.)
      (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
     )
     (= (vstd!std_specs.convert.FromSpec.from_spec.? T&. T& $ (TYPE%core!num.nonzero.NonZero.
        T&. T&
       ) nz!
      ) (vstd!view.View.view.? $ (TYPE%core!num.nonzero.NonZero. T&. T&) nz!)
    ))
    :pattern ((vstd!std_specs.convert.FromSpec.from_spec.? T&. T& $ (TYPE%core!num.nonzero.NonZero.
       T&. T&
      ) nz!
    ))
    :qid internal_vstd!std_specs.nonzero.impl&__16.from_spec.?_definition
    :skolemid skolem_internal_vstd!std_specs.nonzero.impl&__16.from_spec.?_definition
))))

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
    :qid internal_vstd!raw_ptr.impl&__3.view.?_definition
    :skolemid skolem_internal_vstd!raw_ptr.impl&__3.view.?_definition
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
    :qid internal_vstd!view.impl&__0.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__0.view.?_definition
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
    :qid internal_vstd!view.impl&__2.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__2.view.?_definition
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
    :qid internal_vstd!view.impl&__4.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__4.view.?_definition
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
    :qid internal_vstd!view.impl&__6.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__6.view.?_definition
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
    :qid internal_vstd!view.impl&__16.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__16.view.?_definition
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
    :qid internal_vstd!view.impl&__18.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__18.view.?_definition
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
    :qid internal_vstd!view.impl&__20.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__20.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%22::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%22.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%22.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (UINT 16) self!) self!)
    :pattern ((vstd!view.View.view.? $ (UINT 16) self!))
    :qid internal_vstd!view.impl&__22.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__22.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%24::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%24.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%24.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (UINT 32) self!) self!)
    :pattern ((vstd!view.View.view.? $ (UINT 32) self!))
    :qid internal_vstd!view.impl&__24.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__24.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%26::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%26.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%26.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (UINT 64) self!) self!)
    :pattern ((vstd!view.View.view.? $ (UINT 64) self!))
    :qid internal_vstd!view.impl&__26.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__26.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%28::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%28.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%28.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (UINT 128) self!) self!)
    :pattern ((vstd!view.View.view.? $ (UINT 128) self!))
    :qid internal_vstd!view.impl&__28.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__28.view.?_definition
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
    :qid internal_vstd!view.impl&__30.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__30.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%32::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%32.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%32.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (SINT 8) self!) self!)
    :pattern ((vstd!view.View.view.? $ (SINT 8) self!))
    :qid internal_vstd!view.impl&__32.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__32.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%34::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%34.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%34.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (SINT 16) self!) self!)
    :pattern ((vstd!view.View.view.? $ (SINT 16) self!))
    :qid internal_vstd!view.impl&__34.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__34.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%36::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%36.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%36.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (SINT 32) self!) self!)
    :pattern ((vstd!view.View.view.? $ (SINT 32) self!))
    :qid internal_vstd!view.impl&__36.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__36.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%38::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%38.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%38.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (SINT 64) self!) self!)
    :pattern ((vstd!view.View.view.? $ (SINT 64) self!))
    :qid internal_vstd!view.impl&__38.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__38.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%40::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%40.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%40.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ (SINT 128) self!) self!)
    :pattern ((vstd!view.View.view.? $ (SINT 128) self!))
    :qid internal_vstd!view.impl&__40.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__40.view.?_definition
))))

;; Function-Axioms vstd::view::impl&%42::view
(assert
 (fuel_bool_default fuel%vstd!view.impl&%42.view.)
)
(assert
 (=>
  (fuel_bool fuel%vstd!view.impl&%42.view.)
  (forall ((self! Poly)) (!
    (= (vstd!view.View.view.? $ ISIZE self!) self!)
    :pattern ((vstd!view.View.view.? $ ISIZE self!))
    :qid internal_vstd!view.impl&__42.view.?_definition
    :skolemid skolem_internal_vstd!view.impl&__42.view.?_definition
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
 (tr_bound%vstd!view.View. $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (UINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ (SINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!view.View. $ ISIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 16) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 16) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 32) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 32) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 64) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 64) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ USIZE $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ USIZE $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 128) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 128) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 32) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 32) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 64) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 64) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ USIZE $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ USIZE $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 128) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 128) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 64) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 64) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 128) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 128) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 128) $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (UINT 128) $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 16) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 16) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 32) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 32) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 64) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ ISIZE $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ ISIZE $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 128) $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 32) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 32) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 64) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ ISIZE $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ ISIZE $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 128) $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 64) $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 128) $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.convert.FromSpec. $ (SINT 128) $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ USIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (SINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (SINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (SINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ (SINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ ISIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ ISIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ ISIZE)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%vstd!std_specs.nonzero.ZeroablePrimitiveSpec. $ ISIZE)
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (tr_bound%core!convert.From. T&. T& $ (TYPE%core!num.nonzero.NonZero. T&. T&))
   )
   :pattern ((tr_bound%core!convert.From. T&. T& $ (TYPE%core!num.nonzero.NonZero. T&.
      T&
   )))
   :qid internal_core__num__nonzero__impl&__10_trait_impl_definition
   :skolemid skolem_internal_core__num__nonzero__impl&__10_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (tr_bound%vstd!std_specs.convert.FromSpec. T&. T& $ (TYPE%core!num.nonzero.NonZero.
      T&. T&
   )))
   :pattern ((tr_bound%vstd!std_specs.convert.FromSpec. T&. T& $ (TYPE%core!num.nonzero.NonZero.
      T&. T&
   )))
   :qid internal_vstd__std_specs__nonzero__impl&__16_trait_impl_definition
   :skolemid skolem_internal_vstd__std_specs__nonzero__impl&__16_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (UINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (UINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (UINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ (SINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ (SINT 128))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!num.nonzero.ZeroablePrimitive. $ (SINT 128))
)

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
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%core!num.nonzero.NonZero. T&. T&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%core!num.nonzero.NonZero. T&. T&)))
   :qid internal_core__num__nonzero__impl&__0_trait_impl_definition
   :skolemid skolem_internal_core__num__nonzero__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!clone.Clone. $ BOOL)
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
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!clone.Clone. T&. T&)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!clone.Clone. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&))
   )
   :pattern ((tr_bound%core!clone.Clone. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&)))
   :qid internal_alloc__vec__impl&__12_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__12_trait_impl_definition
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
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!convert.From. T&. T& T&. T&)
   )
   :pattern ((tr_bound%core!convert.From. T&. T& T&. T&))
   :qid internal_core__convert__impl&__4_trait_impl_definition
   :skolemid skolem_internal_core__convert__impl&__4_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. T&.) T& T&. T&)
   )
   :pattern ((tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. T&.) T& T&.
     T&
   ))
   :qid internal_alloc__boxed__convert__impl&__0_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__convert__impl&__0_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     (REF $slice) (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) (REF $slice) (SLICE T&. T&)
   ))
   :qid internal_alloc__boxed__convert__impl&__2_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__convert__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (MUTREF $slice (SLICE T&. T&))
   ))
   :pattern ((tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (MUTREF $slice (SLICE T&. T&))
   ))
   :qid internal_alloc__boxed__convert__impl&__3_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__convert__impl&__3_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (ARRAY T&. T& N&. N&)
   ))
   :pattern ((tr_bound%core!convert.From. (BOX $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (ARRAY T&. T& N&. N&)
   ))
   :qid internal_alloc__boxed__convert__impl&__9_trait_impl_definition
   :skolemid skolem_internal_alloc__boxed__convert__impl&__9_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!convert.From. (BOX A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :pattern ((tr_bound%core!convert.From. (BOX A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :qid internal_alloc__vec__impl&__40_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__40_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. T&.) T& T&. T&)
   )
   :pattern ((tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. T&.) T& T&.
     T&
   ))
   :qid internal_alloc__sync__impl&__68_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__68_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (ARRAY T&. T& N&. N&)
   ))
   :pattern ((tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (ARRAY T&. T& N&. N&)
   ))
   :qid internal_alloc__sync__impl&__69_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__69_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     (REF $slice) (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) (REF $slice) (SLICE T&. T&)
   ))
   :qid internal_alloc__sync__impl&__70_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__70_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (MUTREF $slice (SLICE T&. T&))
   ))
   :pattern ((tr_bound%core!convert.From. (ARC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (MUTREF $slice (SLICE T&. T&))
   ))
   :qid internal_alloc__sync__impl&__71_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__71_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!convert.From. (ARC A&. A& T&.) T& (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!convert.From. (ARC A&. A& T&.) T& (BOX A&. A& T&.) T&))
   :qid internal_alloc__sync__impl&__75_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__75_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
     (tr_bound%core!clone.Clone. A&. A&)
    )
    (tr_bound%core!convert.From. (ARC A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :pattern ((tr_bound%core!convert.From. (ARC A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :qid internal_alloc__sync__impl&__76_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__76_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (sized T&.)
    (tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. T&.) T& T&. T&)
   )
   :pattern ((tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. T&.) T& T&. T&))
   :qid internal_alloc__rc__impl&__53_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__53_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (ARRAY T&. T& N&. N&)
   ))
   :pattern ((tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (ARRAY T&. T& N&. N&)
   ))
   :qid internal_alloc__rc__impl&__54_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__54_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     (REF $slice) (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) (REF $slice) (SLICE T&. T&)
   ))
   :qid internal_alloc__rc__impl&__55_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__55_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE T&. T&)
     $ (MUTREF $slice (SLICE T&. T&))
   ))
   :pattern ((tr_bound%core!convert.From. (RC $ TYPE%alloc!alloc.Global. $slice) (SLICE
      T&. T&
     ) $ (MUTREF $slice (SLICE T&. T&))
   ))
   :qid internal_alloc__rc__impl&__56_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__56_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!convert.From. (RC A&. A& T&.) T& (BOX A&. A& T&.) T&)
   )
   :pattern ((tr_bound%core!convert.From. (RC A&. A& T&.) T& (BOX A&. A& T&.) T&))
   :qid internal_alloc__rc__impl&__60_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__60_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!convert.From. (RC A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :pattern ((tr_bound%core!convert.From. (RC A&. A& $slice) (SLICE T&. T&) $ (TYPE%alloc!vec.Vec.
      T&. T& A&. A&
   )))
   :qid internal_alloc__rc__impl&__61_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__61_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 16)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ USIZE) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ USIZE) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (UINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 64)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 16)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ ISIZE) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ ISIZE) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (SINT 64)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 16)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ ISIZE) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 8)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 32)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 16)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 64)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 32)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (TYPE%core!num.nonzero.NonZero. $ (SINT 128)) $ (TYPE%core!num.nonzero.NonZero.
   $ (UINT 64)
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ USIZE $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 8) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 16) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 32) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 64) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (UINT 128) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 8) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 16) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 16) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 32) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 32) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 32) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 64) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (UINT 16))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (UINT 32))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ (SINT 128) $ (UINT 64))
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ ISIZE $ BOOL)
)

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!convert.From. $ ISIZE $ (UINT 8))
)

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     (REF $slice) (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     (REF $slice) (SLICE T&. T&)
   ))
   :qid internal_alloc__vec__impl&__33_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__33_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!clone.Clone. T&. T&)
    )
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (MUTREF $slice (SLICE T&. T&))
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (MUTREF $slice (SLICE T&. T&))
   ))
   :qid internal_alloc__vec__impl&__34_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__34_trait_impl_definition
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
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     (REF $) (ARRAY T&. T& N&. N&)
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     (REF $) (ARRAY T&. T& N&. N&)
   ))
   :qid internal_alloc__vec__impl&__35_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__35_trait_impl_definition
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
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (MUTREF $ (ARRAY T&. T& N&. N&))
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (MUTREF $ (ARRAY T&. T& N&. N&))
   ))
   :qid internal_alloc__vec__impl&__36_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__36_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type)) (!
   (=>
    (and
     (sized T&.)
     (uInv SZ (const_int N&))
    )
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (ARRAY T&. T& N&. N&)
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
     $ (ARRAY T&. T& N&. N&)
   ))
   :qid internal_alloc__vec__impl&__37_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__37_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized A&.)
     (tr_bound%core!alloc.Allocator. A&. A&)
    )
    (tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) (BOX A&. A& $slice)
     (SLICE T&. T&)
   ))
   :pattern ((tr_bound%core!convert.From. $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) (BOX A&.
      A& $slice
     ) (SLICE T&. T&)
   ))
   :qid internal_alloc__vec__impl&__39_trait_impl_definition
   :skolemid skolem_internal_alloc__vec__impl&__39_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type)) (!
   (=>
    (and
     (sized T&.)
     (tr_bound%core!num.nonzero.ZeroablePrimitive. T&. T&)
    )
    (tr_bound%core!marker.Copy. $ (TYPE%core!num.nonzero.NonZero. T&. T&))
   )
   :pattern ((tr_bound%core!marker.Copy. $ (TYPE%core!num.nonzero.NonZero. T&. T&)))
   :qid internal_core__num__nonzero__impl&__2_trait_impl_definition
   :skolemid skolem_internal_core__num__nonzero__impl&__2_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (tr_bound%core!marker.Copy. $ BOOL)
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
   :qid internal_alloc__rc__impl&__116_trait_impl_definition
   :skolemid skolem_internal_alloc__rc__impl&__116_trait_impl_definition
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
   :qid internal_alloc__sync__impl&__118_trait_impl_definition
   :skolemid skolem_internal_alloc__sync__impl&__118_trait_impl_definition
)))

;; Trait-Impl-Axiom
(assert
 (forall ((T&. Dcr) (T& Type) (VERUS_SPEC__A&. Dcr) (VERUS_SPEC__A& Type)) (!
   (=>
    (and
     (sized T&.)
     (sized VERUS_SPEC__A&.)
     (tr_bound%core!convert.From. VERUS_SPEC__A&. VERUS_SPEC__A& T&. T&)
    )
    (tr_bound%vstd!std_specs.convert.FromSpec. VERUS_SPEC__A&. VERUS_SPEC__A& T&. T&)
   )
   :pattern ((tr_bound%vstd!std_specs.convert.FromSpec. VERUS_SPEC__A&. VERUS_SPEC__A&
     T&. T&
   ))
   :qid internal_vstd__std_specs__convert__impl&__2_trait_impl_definition
   :skolemid skolem_internal_vstd__std_specs__convert__impl&__2_trait_impl_definition
)))

;; Function-Specs owned_conversion_clients::array_client
(declare-fun ens%owned_conversion_clients!array_client. (Dcr Type Dcr Type %%Function%%
  Poly
 ) Bool
)
(assert
 (forall ((T&. Dcr) (T& Type) (N&. Dcr) (N& Type) (s! %%Function%%) (result! Poly))
  (!
   (= (ens%owned_conversion_clients!array_client. T&. T& N&. N& s! result!) (and
     (has_type result! (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.))
     (= (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.)
       result!
      ) (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) (Poly%array%. s!))
   )))
   :pattern ((ens%owned_conversion_clients!array_client. T&. T& N&. N& s! result!))
   :qid internal_ens__owned_conversion_clients!array_client._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!array_client._definition
)))

;; Function-Def owned_conversion_clients::array_client
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:12:1: 12:69 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const N&. Dcr)
 (declare-const N& Type)
 (declare-const result! Poly)
 (declare-const s! %%Function%%)
 (declare-const tmp%1 Poly)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (uInv SZ (const_int N&))
 )
 (assert
  (has_type (Poly%array%. s!) (ARRAY T&. T& N&. N&))
 )
 ;; postcondition not satisfied
 (declare-const %%location_label%%0 Bool)
 (assert
  (not (=>
    (ens%alloc!vec.impl&%37.from. T&. T& N&. N& (Poly%array%. s!) tmp%1)
    (=>
     (= result! tmp%1)
     (=>
      %%location_label%%0
      (ext_eq false (TYPE%vstd!seq.Seq. T&. T&) (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec.
         T&. T& $ TYPE%alloc!alloc.Global.
        ) result!
       ) (vstd!view.View.view.? $ (ARRAY T&. T& N&. N&) (Poly%array%. s!))
 ))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)

;; Function-Specs owned_conversion_clients::boxed_client
(declare-fun ens%owned_conversion_clients!boxed_client. (Dcr Type Dcr Type Poly Poly)
 Bool
)
(assert
 (forall ((T&. Dcr) (T& Type) (A&. Dcr) (A& Type) (s! Poly) (result! Poly)) (!
   (= (ens%owned_conversion_clients!boxed_client. T&. T& A&. A& s! result!) (and
     (has_type result! (TYPE%alloc!vec.Vec. T&. T& A&. A&))
     (= (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& A&. A&) result!) (vstd!view.View.view.?
       $slice (SLICE T&. T&) s!
   ))))
   :pattern ((ens%owned_conversion_clients!boxed_client. T&. T& A&. A& s! result!))
   :qid internal_ens__owned_conversion_clients!boxed_client._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!boxed_client._definition
)))

;; Function-Def owned_conversion_clients::boxed_client
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:19:1: 19:75 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const A&. Dcr)
 (declare-const A& Type)
 (declare-const result! Poly)
 (declare-const s! Poly)
 (declare-const tmp%1 Poly)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (sized A&.)
 )
 (assert
  (tr_bound%core!alloc.Allocator. A&. A&)
 )
 (assert
  (has_type s! (SLICE T&. T&))
 )
 ;; postcondition not satisfied
 (declare-const %%location_label%%0 Bool)
 (assert
  (not (=>
    (ens%alloc!vec.impl&%39.from. T&. T& A&. A& s! tmp%1)
    (=>
     (= result! tmp%1)
     (=>
      %%location_label%%0
      (ext_eq false (TYPE%vstd!seq.Seq. T&. T&) (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec.
         T&. T& A&. A&
        ) result!
       ) (vstd!view.View.view.? $slice (SLICE T&. T&) s!)
 ))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)

;; Function-Specs owned_conversion_clients::empty_array_client
(declare-fun ens%owned_conversion_clients!empty_array_client. (Dcr Type %%Function%%
  Poly
 ) Bool
)
(assert
 (forall ((T&. Dcr) (T& Type) (s! %%Function%%) (result! Poly)) (!
   (= (ens%owned_conversion_clients!empty_array_client. T&. T& s! result!) (and
     (has_type result! (TYPE%alloc!vec.Vec. T&. T& $ TYPE%alloc!alloc.Global.))
     (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $
         TYPE%alloc!alloc.Global.
        ) result!
       )
      ) 0
   )))
   :pattern ((ens%owned_conversion_clients!empty_array_client. T&. T& s! result!))
   :qid internal_ens__owned_conversion_clients!empty_array_client._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!empty_array_client._definition
)))

;; Function-Def owned_conversion_clients::empty_array_client
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:27:1: 27:59 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const result! Poly)
 (declare-const s! %%Function%%)
 (declare-const tmp%1 Poly)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (has_type (Poly%array%. s!) (ARRAY T&. T& $ (CONST_INT 0)))
 )
 ;; postcondition not satisfied
 (declare-const %%location_label%%0 Bool)
 (assert
  (not (=>
    (ens%alloc!vec.impl&%37.from. T&. T& $ (CONST_INT 0) (Poly%array%. s!) tmp%1)
    (=>
     (= result! tmp%1)
     (=>
      %%location_label%%0
      (= (vstd!seq.Seq.len.? T&. T& (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec. T&. T& $
          TYPE%alloc!alloc.Global.
         ) result!
        )
       ) 0
 ))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)

;; Function-Specs owned_conversion_clients::duplicate_order_client
(declare-fun ens%owned_conversion_clients!duplicate_order_client. (Int alloc!vec.Vec<u8./alloc!alloc.Global.>.)
 Bool
)
(declare-fun %%array%%0 (Poly Poly Poly Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Poly) (%%hole%%1 Poly) (%%hole%%2 Poly) (%%hole%%3 Poly)) (!
   (let
    ((%%x%% (%%array%%0 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3)))
    (and
     (= (%%apply%%1 %%x%% 0) %%hole%%0)
     (= (%%apply%%1 %%x%% 1) %%hole%%1)
     (= (%%apply%%1 %%x%% 2) %%hole%%2)
     (= (%%apply%%1 %%x%% 3) %%hole%%3)
   ))
   :pattern ((%%array%%0 %%hole%%0 %%hole%%1 %%hole%%2 %%hole%%3))
   :qid __AIR_ARRAY_QID__
   :skolemid skolem___AIR_ARRAY_QID__
)))
(assert
 (forall ((no%param Int) (result! alloc!vec.Vec<u8./alloc!alloc.Global.>.)) (!
   (= (ens%owned_conversion_clients!duplicate_order_client. no%param result!) (= (vstd!view.View.view.?
      $ (TYPE%alloc!vec.Vec. $ (UINT 8) $ TYPE%alloc!alloc.Global.) (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>.
       result!
      )
     ) (vstd!view.View.view.? $ (ARRAY $ (UINT 8) $ (CONST_INT 4)) (array_new $ (UINT 8)
       4 (%%array%%0 (I 8) (I 3) (I 8) (I 1))
   ))))
   :pattern ((ens%owned_conversion_clients!duplicate_order_client. no%param result!))
   :qid internal_ens__owned_conversion_clients!duplicate_order_client._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!duplicate_order_client._definition
)))

;; Function-Def owned_conversion_clients::duplicate_order_client
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:35:1: 35:52 (#0)
(push)
 (get-info :all-statistics)
 (declare-const result! alloc!vec.Vec<u8./alloc!alloc.Global.>.)
 (declare-const no%param Int)
 (declare-const tmp%1 Poly)
 (declare-const tmp%2 Poly)
 (assert
  fuel_defaults
 )
 ;; postcondition not satisfied
 (declare-const %%location_label%%0 Bool)
 (assert
  (not (=>
    (= tmp%2 (array_new $ (UINT 8) 4 (%%array%%0 (I 8) (I 3) (I 8) (I 1))))
    (=>
     (ens%alloc!vec.impl&%37.from. $ (UINT 8) $ (CONST_INT 4) tmp%2 tmp%1)
     (=>
      (= result! (%Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. tmp%1))
      (=>
       %%location_label%%0
       (ext_eq false (TYPE%vstd!seq.Seq. $ (UINT 8)) (vstd!view.View.view.? $ (TYPE%alloc!vec.Vec.
          $ (UINT 8) $ TYPE%alloc!alloc.Global.
         ) (Poly%alloc!vec.Vec<u8./alloc!alloc.Global.>. result!)
        ) (vstd!view.View.view.? $ (ARRAY $ (UINT 8) $ (CONST_INT 4)) (array_new $ (UINT 8)
          4 (%%array%%0 (I 8) (I 3) (I 8) (I 1))
 )))))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)

;; Function-Specs owned_conversion_clients::order_is_observable
(declare-fun req%owned_conversion_clients!order_is_observable. (Dcr Type Poly Poly)
 Bool
)
(declare-const %%global_location_label%%4 Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (first! Poly) (second! Poly)) (!
   (= (req%owned_conversion_clients!order_is_observable. T&. T& first! second!) (=>
     %%global_location_label%%4
     (not (= first! second!))
   ))
   :pattern ((req%owned_conversion_clients!order_is_observable. T&. T& first! second!))
   :qid internal_req__owned_conversion_clients!order_is_observable._definition
   :skolemid skolem_internal_req__owned_conversion_clients!order_is_observable._definition
)))
(declare-fun ens%owned_conversion_clients!order_is_observable. (Dcr Type Poly Poly)
 Bool
)
(declare-fun %%array%%1 (Poly Poly Poly) %%Function%%)
(assert
 (forall ((%%hole%%0 Poly) (%%hole%%1 Poly) (%%hole%%2 Poly)) (!
   (let
    ((%%x%% (%%array%%1 %%hole%%0 %%hole%%1 %%hole%%2)))
    (and
     (= (%%apply%%1 %%x%% 0) %%hole%%0)
     (= (%%apply%%1 %%x%% 1) %%hole%%1)
     (= (%%apply%%1 %%x%% 2) %%hole%%2)
   ))
   :pattern ((%%array%%1 %%hole%%0 %%hole%%1 %%hole%%2))
   :qid __AIR_ARRAY_QID__
   :skolemid skolem___AIR_ARRAY_QID__
)))
(assert
 (forall ((T&. Dcr) (T& Type) (first! Poly) (second! Poly)) (!
   (= (ens%owned_conversion_clients!order_is_observable. T&. T& first! second!) (not (
      = (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (%%array%%1
         first! second! first!
       ))
      ) (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (%%array%%1
         second! first! first!
   ))))))
   :pattern ((ens%owned_conversion_clients!order_is_observable. T&. T& first! second!))
   :qid internal_ens__owned_conversion_clients!order_is_observable._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!order_is_observable._definition
)))

;; Function-Def owned_conversion_clients::order_is_observable
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:42:1: 42:57 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const first! Poly)
 (declare-const second! Poly)
 (declare-const tmp%1 Bool)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (has_type first! T&)
 )
 (assert
  (has_type second! T&)
 )
 (assert
  (not (= first! second!))
 )
 ;; assertion failed
 (declare-const %%location_label%%0 Bool)
 ;; postcondition not satisfied
 (declare-const %%location_label%%1 Bool)
 (assert
  (not (=>
    (= tmp%1 (not (= (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& $
          (CONST_INT 3)
         ) (array_new T&. T& 3 (%%array%%1 first! second! first!))
        ) (I 0)
       ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3))
         (array_new T&. T& 3 (%%array%%1 second! first! first!))
        ) (I 0)
    ))))
    (and
     (=>
      %%location_label%%0
      tmp%1
     )
     (=>
      tmp%1
      (=>
       %%location_label%%1
       (not (= (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (
            %%array%%1 first! second! first!
          ))
         ) (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (%%array%%1
            second! first! first!
 )))))))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)

;; Function-Specs owned_conversion_clients::interior_element_is_observable
(declare-fun req%owned_conversion_clients!interior_element_is_observable. (Dcr Type
  Poly Poly Poly
 ) Bool
)
(declare-const %%global_location_label%%5 Bool)
(assert
 (forall ((T&. Dcr) (T& Type) (outer! Poly) (first! Poly) (second! Poly)) (!
   (= (req%owned_conversion_clients!interior_element_is_observable. T&. T& outer! first!
     second!
    ) (=>
     %%global_location_label%%5
     (not (= first! second!))
   ))
   :pattern ((req%owned_conversion_clients!interior_element_is_observable. T&. T& outer!
     first! second!
   ))
   :qid internal_req__owned_conversion_clients!interior_element_is_observable._definition
   :skolemid skolem_internal_req__owned_conversion_clients!interior_element_is_observable._definition
)))
(declare-fun ens%owned_conversion_clients!interior_element_is_observable. (Dcr Type
  Poly Poly Poly
 ) Bool
)
(assert
 (forall ((T&. Dcr) (T& Type) (outer! Poly) (first! Poly) (second! Poly)) (!
   (= (ens%owned_conversion_clients!interior_element_is_observable. T&. T& outer! first!
     second!
    ) (not (= (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3
        (%%array%%1 outer! first! outer!)
       )
      ) (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (%%array%%1
         outer! second! outer!
   ))))))
   :pattern ((ens%owned_conversion_clients!interior_element_is_observable. T&. T& outer!
     first! second!
   ))
   :qid internal_ens__owned_conversion_clients!interior_element_is_observable._definition
   :skolemid skolem_internal_ens__owned_conversion_clients!interior_element_is_observable._definition
)))

;; Function-Def owned_conversion_clients::interior_element_is_observable
;; /home/chentianyu/rust-std-vec-specgen-astra-2026-09-22/tests/owned_conversion_clients.rs:51:1: 51:78 (#0)
(push)
 (get-info :all-statistics)
 (declare-const T&. Dcr)
 (declare-const T& Type)
 (declare-const outer! Poly)
 (declare-const first! Poly)
 (declare-const second! Poly)
 (declare-const tmp%1 Bool)
 (assert
  fuel_defaults
 )
 (assert
  (sized T&.)
 )
 (assert
  (has_type outer! T&)
 )
 (assert
  (has_type first! T&)
 )
 (assert
  (has_type second! T&)
 )
 (assert
  (not (= first! second!))
 )
 ;; assertion failed
 (declare-const %%location_label%%0 Bool)
 ;; postcondition not satisfied
 (declare-const %%location_label%%1 Bool)
 (assert
  (not (=>
    (= tmp%1 (not (= (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& $
          (CONST_INT 3)
         ) (array_new T&. T& 3 (%%array%%1 outer! first! outer!))
        ) (I 1)
       ) (vstd!seq.Seq.index.? T&. T& (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3))
         (array_new T&. T& 3 (%%array%%1 outer! second! outer!))
        ) (I 1)
    ))))
    (and
     (=>
      %%location_label%%0
      tmp%1
     )
     (=>
      tmp%1
      (=>
       %%location_label%%1
       (not (= (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (
            %%array%%1 outer! first! outer!
          ))
         ) (vstd!view.View.view.? $ (ARRAY T&. T& $ (CONST_INT 3)) (array_new T&. T& 3 (%%array%%1
            outer! second! outer!
 )))))))))))
 (get-info :all-statistics)
 (get-info :version)
 (set-option :rlimit 30000000)
 (check-sat)
 (set-option :rlimit 0)
 (get-info :all-statistics)
(pop)
