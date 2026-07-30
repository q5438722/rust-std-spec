# Rust std contract generation with determinism feedback

## Aggregate result

| Metric | Count |
|---|---:|
| `targets` | 27 |
| `initial_add_spec` | 24 |
| `initial_skip` | 3 |
| `final_add_spec` | 18 |
| `final_skip` | 9 |
| `typecheck_passed` | 18 |
| `det_unsat` | 18 |
| `det_sat` | 0 |
| `det_unknown` | 0 |
| `raw_reward` | 18 |
| `guarded_reward` | 18 |
| `semantic_guarded_reward` | 18 |
| `llm_errors` | 0 |
| `static_skips` | 0 |

External `assume_specification` declarations are trusted. A guarded determinism reward means only that the candidate typechecked, avoided the configured vacuity gates, and uniquely determined the modeled outputs. It does not prove the contract sound.

## Feedback transitions

| Transition | Count |
|---|---:|
| `add_spec->add_spec` | 18 |
| `add_spec->skip` | 6 |
| `skip->skip` | 3 |

## Frequent issues

| Issue | Count |
|---|---:|
| `determinism_unsupported_contract_form` | 1 |

## Guarded-deterministic candidates

| Target | Ensures |
|---|---|
| `alloc::collections::LinkedList::contains` | `result <==> list@.contains(*x)` |
| `core::net::IpAddr::to_canonical` | `result@ == match address@ { vstd::std_specs::net::IpAddrView::V4(bytes) => vstd::std_specs::net::IpAddrView::V4(bytes), vstd::std_specs::net::IpAddrView::V6(bytes) => if bytes.len() == 16 && bytes.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] { vstd::std_specs::net::IpAddrView::V4(bytes.subrange(12, 16)) } else { vstd::std_specs::net::IpAddrView::V6(bytes) }, }` |
| `core::net::Ipv4Addr::from_bits` | `result@ == seq![(bits >> 24) as u8, ((bits >> 16) & 0xff) as u8, ((bits >> 8) & 0xff) as u8, (bits & 0xff) as u8,]` |
| `core::net::Ipv4Addr::to_bits` | `result == (((address@[0] as u32) << 24) | ((address@[1] as u32) << 16) | ((address@[2] as u32) << 8) | (address@[3] as u32))` |
| `core::net::Ipv6Addr::from_bits` | `result@ == seq![(((bits >> 120) & 0xffu128) as u8), (((bits >> 112) & 0xffu128) as u8), (((bits >> 104) & 0xffu128) as u8), (((bits >> 96) & 0xffu128) as u8), (((bits >> 88) & 0xffu128) as u8), (((bits >> 80) & 0xffu128) as u8), (((bits >> 72) & 0xffu128) as u8), (((bits >> 64) & 0xffu128) as u8), (((bits >> 56) & 0xffu128) as u8), (((bits >> 48) & 0xffu128) as u8), (((bits >> 40) & 0xffu128) as u8), (((bits >> 32) & 0xffu128) as u8), (((bits >> 24) & 0xffu128) as u8), (((bits >> 16) & 0xffu128) as u8), (((bits >> 8) & 0xffu128) as u8), ((bits & 0xffu128) as u8)]` |
| `core::net::Ipv6Addr::from_segments` | `result@ == seq![
            ((segments@[0] >> 8) & 0xff) as u8,
            (segments@[0] & 0xff) as u8,
            ((segments@[1] >> 8) & 0xff) as u8,
            (segments@[1] & 0xff) as u8,
            ((segments@[2] >> 8) & 0xff) as u8,
            (segments@[2] & 0xff) as u8,
            ((segments@[3] >> 8) & 0xff) as u8,
            (segments@[3] & 0xff) as u8,
            ((segments@[4] >> 8) & 0xff) as u8,
            (segments@[4] & 0xff) as u8,
            ((segments@[5] >> 8) & 0xff) as u8,
            (segments@[5] & 0xff) as u8,
            ((segments@[6] >> 8) & 0xff) as u8,
            (segments@[6] & 0xff) as u8,
            ((segments@[7] >> 8) & 0xff) as u8,
            (segments@[7] & 0xff) as u8,
        ]` |
| `core::net::Ipv6Addr::new` | `result@.len() == 16; (result@[0] as u16) == a / 256u16; (result@[1] as u16) == a % 256u16; (result@[2] as u16) == b / 256u16; (result@[3] as u16) == b % 256u16; (result@[4] as u16) == c / 256u16; (result@[5] as u16) == c % 256u16; (result@[6] as u16) == d / 256u16; (result@[7] as u16) == d % 256u16; (result@[8] as u16) == e / 256u16; (result@[9] as u16) == e % 256u16; (result@[10] as u16) == f / 256u16; (result@[11] as u16) == f % 256u16; (result@[12] as u16) == g / 256u16; (result@[13] as u16) == g % 256u16; (result@[14] as u16) == h / 256u16; (result@[15] as u16) == h % 256u16` |
| `core::net::Ipv6Addr::segments` | `(result@[0] as int) == (address@[0] as int) * 256 + (address@[1] as int); (result@[1] as int) == (address@[2] as int) * 256 + (address@[3] as int); (result@[2] as int) == (address@[4] as int) * 256 + (address@[5] as int); (result@[3] as int) == (address@[6] as int) * 256 + (address@[7] as int); (result@[4] as int) == (address@[8] as int) * 256 + (address@[9] as int); (result@[5] as int) == (address@[10] as int) * 256 + (address@[11] as int); (result@[6] as int) == (address@[12] as int) * 256 + (address@[13] as int); (result@[7] as int) == (address@[14] as int) * 256 + (address@[15] as int)` |
| `core::net::Ipv6Addr::to_bits` | `result as int == (address@[0] as int) * 0x100_0000_0000_0000_0000_0000_0000_0000 + (address@[1] as int) * 0x1_0000_0000_0000_0000_0000_0000_0000 + (address@[2] as int) * 0x100_0000_0000_0000_0000_0000_0000 + (address@[3] as int) * 0x1_0000_0000_0000_0000_0000_0000 + (address@[4] as int) * 0x100_0000_0000_0000_0000_0000 + (address@[5] as int) * 0x1_0000_0000_0000_0000_0000 + (address@[6] as int) * 0x100_0000_0000_0000_0000 + (address@[7] as int) * 0x1_0000_0000_0000_0000 + (address@[8] as int) * 0x100_0000_0000_0000 + (address@[9] as int) * 0x1_0000_0000_0000 + (address@[10] as int) * 0x100_0000_0000 + (address@[11] as int) * 0x1_0000_0000 + (address@[12] as int) * 0x100_0000 + (address@[13] as int) * 0x1_0000 + (address@[14] as int) * 0x100 + address@[15] as int` |
| `core::net::Ipv6Addr::to_canonical` | `result@ == if address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] { IpAddrView::V4(address@.subrange(12, 16)) } else { IpAddrView::V6(address@) }` |
| `core::net::Ipv6Addr::to_ipv4` | `(result is Some) <==> (address@.subrange(0, 12) == Seq::new(12, |i: int| 0u8) || address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]); result is Some ==> (result->Some_0)@ == address@.subrange(12, 16)` |
| `core::net::Ipv6Addr::to_ipv4_mapped` | `(result is Some) <==> address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]; result is Some ==> (result->Some_0)@ == address@.subrange(12, 16)` |
| `core::net::SocketAddr::set_ip` | `final(address)@ == match (old(address)@, new_ip@) {
            (SocketAddrView::V4(old_v4), IpAddrView::V4(ip)) =>
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v4.port }),
            (SocketAddrView::V4(old_v4), IpAddrView::V6(ip)) =>
                SocketAddrView::V6(SocketAddrV6View {
                    ip,
                    port: old_v4.port,
                    flowinfo: 0,
                    scope_id: 0,
                }),
            (SocketAddrView::V6(old_v6), IpAddrView::V4(ip)) =>
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v6.port }),
            (SocketAddrView::V6(old_v6), IpAddrView::V6(ip)) =>
                SocketAddrView::V6(SocketAddrV6View {
                    ip,
                    port: old_v6.port,
                    flowinfo: old_v6.flowinfo,
                    scope_id: old_v6.scope_id,
                }),
        }` |
| `core::time::Duration::as_secs_f32` | `result == vstd::float::ieee_float_cast::<u64, f32>((duration@ / vstd::std_specs::duration::nanos_per_second()) as u64) + vstd::float::ieee_float_cast::<u32, f32>((duration@ % vstd::std_specs::duration::nanos_per_second()) as u32) / vstd::float::ieee_float_cast::<u32, f32>(1_000_000_000u32)` |
| `core::time::Duration::as_secs_f64` | `result == vstd::float::ieee_float_cast::<u64, f64>((duration@ / vstd::std_specs::duration::nanos_per_second()) as u64) + vstd::float::ieee_float_cast::<u32, f64>((duration@ % vstd::std_specs::duration::nanos_per_second()) as u32) / vstd::float::ieee_float_cast::<u32, f64>(1_000_000_000u32)` |
| `core::time::Duration::mul_f64` | `result@ == if rhs == 0.0f64 { 0 } else { duration@ }` |
| `core::time::Duration::from_secs_f32` | `result@ == { let bits = secs.to_bits_abs_spec() as nat; let exponent = bits / 0x80_0000; let mantissa = bits % 0x80_0000; let significand = if exponent == 0 { mantissa } else { 0x80_0000 + mantissa }; let numerator = if exponent < 150 { 1_000_000_000 * significand } else { 1_000_000_000 * significand * pow2((exponent - 150) as nat) }; let denominator = if exponent < 150 { if exponent == 0 { pow2(149) } else { pow2((150 - exponent) as nat) } } else { 1 }; let quotient = numerator / denominator; let remainder = numerator % denominator; if remainder * 2 < denominator { quotient } else if remainder * 2 > denominator || quotient % 2 == 1 { quotient + 1 } else { quotient } }` |
| `core::time::Duration::from_secs_f64` | `result@ == { let bits = secs.to_bits_abs_spec() as nat; let exponent = bits / 0x10_0000_0000_0000; let mantissa = bits % 0x10_0000_0000_0000; let significand = if exponent == 0 { mantissa } else { 0x10_0000_0000_0000 + mantissa }; let numerator = if exponent < 1075 { 1_000_000_000 * significand } else { 1_000_000_000 * significand * pow2((exponent - 1075) as nat) }; let denominator = if exponent < 1075 { if exponent == 0 { pow2(1074) } else { pow2((1075 - exponent) as nat) } } else { 1 }; let quotient = numerator / denominator; let remainder = numerator % denominator; if remainder * 2 < denominator { quotient } else if remainder * 2 > denominator || quotient % 2 == 1 { quotient + 1 } else { quotient } }` |

## Semantic-gated candidates

18 of 18 guarded-deterministic candidates pass the pilot-derived semantic postprocessing gates.

| Target | Ensures |
|---|---|
| `alloc::collections::LinkedList::contains` | `result <==> list@.contains(*x)` |
| `core::net::IpAddr::to_canonical` | `result@ == match address@ { vstd::std_specs::net::IpAddrView::V4(bytes) => vstd::std_specs::net::IpAddrView::V4(bytes), vstd::std_specs::net::IpAddrView::V6(bytes) => if bytes.len() == 16 && bytes.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] { vstd::std_specs::net::IpAddrView::V4(bytes.subrange(12, 16)) } else { vstd::std_specs::net::IpAddrView::V6(bytes) }, }` |
| `core::net::Ipv4Addr::from_bits` | `result@ == seq![(bits >> 24) as u8, ((bits >> 16) & 0xff) as u8, ((bits >> 8) & 0xff) as u8, (bits & 0xff) as u8,]` |
| `core::net::Ipv4Addr::to_bits` | `result == (((address@[0] as u32) << 24) | ((address@[1] as u32) << 16) | ((address@[2] as u32) << 8) | (address@[3] as u32))` |
| `core::net::Ipv6Addr::from_bits` | `result@ == seq![(((bits >> 120) & 0xffu128) as u8), (((bits >> 112) & 0xffu128) as u8), (((bits >> 104) & 0xffu128) as u8), (((bits >> 96) & 0xffu128) as u8), (((bits >> 88) & 0xffu128) as u8), (((bits >> 80) & 0xffu128) as u8), (((bits >> 72) & 0xffu128) as u8), (((bits >> 64) & 0xffu128) as u8), (((bits >> 56) & 0xffu128) as u8), (((bits >> 48) & 0xffu128) as u8), (((bits >> 40) & 0xffu128) as u8), (((bits >> 32) & 0xffu128) as u8), (((bits >> 24) & 0xffu128) as u8), (((bits >> 16) & 0xffu128) as u8), (((bits >> 8) & 0xffu128) as u8), ((bits & 0xffu128) as u8)]` |
| `core::net::Ipv6Addr::from_segments` | `result@ == seq![
            ((segments@[0] >> 8) & 0xff) as u8,
            (segments@[0] & 0xff) as u8,
            ((segments@[1] >> 8) & 0xff) as u8,
            (segments@[1] & 0xff) as u8,
            ((segments@[2] >> 8) & 0xff) as u8,
            (segments@[2] & 0xff) as u8,
            ((segments@[3] >> 8) & 0xff) as u8,
            (segments@[3] & 0xff) as u8,
            ((segments@[4] >> 8) & 0xff) as u8,
            (segments@[4] & 0xff) as u8,
            ((segments@[5] >> 8) & 0xff) as u8,
            (segments@[5] & 0xff) as u8,
            ((segments@[6] >> 8) & 0xff) as u8,
            (segments@[6] & 0xff) as u8,
            ((segments@[7] >> 8) & 0xff) as u8,
            (segments@[7] & 0xff) as u8,
        ]` |
| `core::net::Ipv6Addr::new` | `result@.len() == 16; (result@[0] as u16) == a / 256u16; (result@[1] as u16) == a % 256u16; (result@[2] as u16) == b / 256u16; (result@[3] as u16) == b % 256u16; (result@[4] as u16) == c / 256u16; (result@[5] as u16) == c % 256u16; (result@[6] as u16) == d / 256u16; (result@[7] as u16) == d % 256u16; (result@[8] as u16) == e / 256u16; (result@[9] as u16) == e % 256u16; (result@[10] as u16) == f / 256u16; (result@[11] as u16) == f % 256u16; (result@[12] as u16) == g / 256u16; (result@[13] as u16) == g % 256u16; (result@[14] as u16) == h / 256u16; (result@[15] as u16) == h % 256u16` |
| `core::net::Ipv6Addr::segments` | `(result@[0] as int) == (address@[0] as int) * 256 + (address@[1] as int); (result@[1] as int) == (address@[2] as int) * 256 + (address@[3] as int); (result@[2] as int) == (address@[4] as int) * 256 + (address@[5] as int); (result@[3] as int) == (address@[6] as int) * 256 + (address@[7] as int); (result@[4] as int) == (address@[8] as int) * 256 + (address@[9] as int); (result@[5] as int) == (address@[10] as int) * 256 + (address@[11] as int); (result@[6] as int) == (address@[12] as int) * 256 + (address@[13] as int); (result@[7] as int) == (address@[14] as int) * 256 + (address@[15] as int)` |
| `core::net::Ipv6Addr::to_bits` | `result as int == (address@[0] as int) * 0x100_0000_0000_0000_0000_0000_0000_0000 + (address@[1] as int) * 0x1_0000_0000_0000_0000_0000_0000_0000 + (address@[2] as int) * 0x100_0000_0000_0000_0000_0000_0000 + (address@[3] as int) * 0x1_0000_0000_0000_0000_0000_0000 + (address@[4] as int) * 0x100_0000_0000_0000_0000_0000 + (address@[5] as int) * 0x1_0000_0000_0000_0000_0000 + (address@[6] as int) * 0x100_0000_0000_0000_0000 + (address@[7] as int) * 0x1_0000_0000_0000_0000 + (address@[8] as int) * 0x100_0000_0000_0000 + (address@[9] as int) * 0x1_0000_0000_0000 + (address@[10] as int) * 0x100_0000_0000 + (address@[11] as int) * 0x1_0000_0000 + (address@[12] as int) * 0x100_0000 + (address@[13] as int) * 0x1_0000 + (address@[14] as int) * 0x100 + address@[15] as int` |
| `core::net::Ipv6Addr::to_canonical` | `result@ == if address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] { IpAddrView::V4(address@.subrange(12, 16)) } else { IpAddrView::V6(address@) }` |
| `core::net::Ipv6Addr::to_ipv4` | `(result is Some) <==> (address@.subrange(0, 12) == Seq::new(12, |i: int| 0u8) || address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]); result is Some ==> (result->Some_0)@ == address@.subrange(12, 16)` |
| `core::net::Ipv6Addr::to_ipv4_mapped` | `(result is Some) <==> address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]; result is Some ==> (result->Some_0)@ == address@.subrange(12, 16)` |
| `core::net::SocketAddr::set_ip` | `final(address)@ == match (old(address)@, new_ip@) {
            (SocketAddrView::V4(old_v4), IpAddrView::V4(ip)) =>
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v4.port }),
            (SocketAddrView::V4(old_v4), IpAddrView::V6(ip)) =>
                SocketAddrView::V6(SocketAddrV6View {
                    ip,
                    port: old_v4.port,
                    flowinfo: 0,
                    scope_id: 0,
                }),
            (SocketAddrView::V6(old_v6), IpAddrView::V4(ip)) =>
                SocketAddrView::V4(SocketAddrV4View { ip, port: old_v6.port }),
            (SocketAddrView::V6(old_v6), IpAddrView::V6(ip)) =>
                SocketAddrView::V6(SocketAddrV6View {
                    ip,
                    port: old_v6.port,
                    flowinfo: old_v6.flowinfo,
                    scope_id: old_v6.scope_id,
                }),
        }` |
| `core::time::Duration::as_secs_f32` | `result == vstd::float::ieee_float_cast::<u64, f32>((duration@ / vstd::std_specs::duration::nanos_per_second()) as u64) + vstd::float::ieee_float_cast::<u32, f32>((duration@ % vstd::std_specs::duration::nanos_per_second()) as u32) / vstd::float::ieee_float_cast::<u32, f32>(1_000_000_000u32)` |
| `core::time::Duration::as_secs_f64` | `result == vstd::float::ieee_float_cast::<u64, f64>((duration@ / vstd::std_specs::duration::nanos_per_second()) as u64) + vstd::float::ieee_float_cast::<u32, f64>((duration@ % vstd::std_specs::duration::nanos_per_second()) as u32) / vstd::float::ieee_float_cast::<u32, f64>(1_000_000_000u32)` |
| `core::time::Duration::mul_f64` | `result@ == if rhs == 0.0f64 { 0 } else { duration@ }` |
| `core::time::Duration::from_secs_f32` | `result@ == { let bits = secs.to_bits_abs_spec() as nat; let exponent = bits / 0x80_0000; let mantissa = bits % 0x80_0000; let significand = if exponent == 0 { mantissa } else { 0x80_0000 + mantissa }; let numerator = if exponent < 150 { 1_000_000_000 * significand } else { 1_000_000_000 * significand * pow2((exponent - 150) as nat) }; let denominator = if exponent < 150 { if exponent == 0 { pow2(149) } else { pow2((150 - exponent) as nat) } } else { 1 }; let quotient = numerator / denominator; let remainder = numerator % denominator; if remainder * 2 < denominator { quotient } else if remainder * 2 > denominator || quotient % 2 == 1 { quotient + 1 } else { quotient } }` |
| `core::time::Duration::from_secs_f64` | `result@ == { let bits = secs.to_bits_abs_spec() as nat; let exponent = bits / 0x10_0000_0000_0000; let mantissa = bits % 0x10_0000_0000_0000; let significand = if exponent == 0 { mantissa } else { 0x10_0000_0000_0000 + mantissa }; let numerator = if exponent < 1075 { 1_000_000_000 * significand } else { 1_000_000_000 * significand * pow2((exponent - 1075) as nat) }; let denominator = if exponent < 1075 { if exponent == 0 { pow2(1074) } else { pow2((1075 - exponent) as nat) } } else { 1 }; let quotient = numerator / denominator; let remainder = numerator % denominator; if remainder * 2 < denominator { quotient } else if remainder * 2 > denominator || quotient % 2 == 1 { quotient + 1 } else { quotient } }` |

## Per-target result

| Target | Initial | Final | Typecheck | R0 | Guarded | Semantic | Issues |
|---|---|---|---:|---|---:|---:|---|
| `alloc::collections::BinaryHeap::peek_mut` | add_spec | skip | 0 |  | 0 | 0 |  |
| `alloc::collections::LinkedList::contains` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `alloc::ffi::CString::new` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::net::IpAddr::to_canonical` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv4Addr::from_bits` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv4Addr::to_bits` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::from_bits` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::from_segments` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::new` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::segments` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::to_bits` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::to_canonical` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::to_ipv4` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::Ipv6Addr::to_ipv4_mapped` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::net::SocketAddr::set_ip` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::time::Duration::as_secs_f32` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::time::Duration::as_secs_f64` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::time::Duration::div_duration_f32` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::div_duration_f64` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::div_f32` | skip | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::div_f64` | skip | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::mul_f32` | skip | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::mul_f64` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::time::Duration::try_from_secs_f32` | add_spec | skip | 0 |  | 0 | 0 |  |
| `core::time::Duration::try_from_secs_f64` | add_spec | skip | 0 |  | 0 | 0 | determinism_unsupported_contract_form |
| `core::time::Duration::from_secs_f32` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
| `core::time::Duration::from_secs_f64` | add_spec | add_spec | 1 | unsat | 1 | 1 |  |
