pub assume_specification[ Ipv4Addr::to_ipv6_mapped ](address: &Ipv4Addr) -> (result: Ipv6Addr)
    ensures
        result@ == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8] + address@,
;
