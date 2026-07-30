pub assume_specification[ Ipv6Addr::from_octets ](octets: [u8; 16]) -> (result: Ipv6Addr)
    ensures
        result@ == octets@,
;
