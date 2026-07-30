pub assume_specification[ Ipv6Addr::to_ipv4 ](address: &Ipv6Addr) -> (result: Option<Ipv4Addr>)
    ensures
        (result is Some) <==> (address@.subrange(0, 12) == Seq::new(12, |i: int| 0u8)
            || address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![0xffu8, 0xffu8]),
        result is Some ==> result->Some_0@ == address@.subrange(12, 16),
;
