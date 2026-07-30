pub assume_specification[ Ipv6Addr::to_canonical ](address: &Ipv6Addr) -> (result: IpAddr)
    ensures
        result@ == if address@.subrange(0, 12) == Seq::new(10, |i: int| 0u8) + seq![
            0xffu8,
            0xffu8,
        ] {
            IpAddrView::V4(address@.subrange(12, 16))
        } else {
            IpAddrView::V6(address@)
        },
;
