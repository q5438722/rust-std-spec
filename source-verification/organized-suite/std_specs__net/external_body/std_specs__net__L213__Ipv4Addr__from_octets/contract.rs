pub assume_specification[ Ipv4Addr::from_octets ](octets: [u8; 4]) -> (result: Ipv4Addr)
    ensures
        result@ == octets@,
;
