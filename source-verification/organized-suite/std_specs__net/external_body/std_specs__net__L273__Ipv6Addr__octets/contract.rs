pub assume_specification[ Ipv6Addr::octets ](address: &Ipv6Addr) -> (result: [u8; 16])
    ensures
        result@ == address@,
;
