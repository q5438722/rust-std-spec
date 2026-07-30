pub assume_specification[ Ipv4Addr::octets ](address: &Ipv4Addr) -> (result: [u8; 4])
    ensures
        result@ == address@,
;
