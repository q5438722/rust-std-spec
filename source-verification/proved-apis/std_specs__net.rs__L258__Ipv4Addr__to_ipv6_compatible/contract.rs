pub assume_specification[ Ipv4Addr::to_ipv6_compatible ](address: &Ipv4Addr) -> (result: Ipv6Addr)
    ensures
        result@ == Seq::new(12, |i: int| 0u8) + address@,
;
