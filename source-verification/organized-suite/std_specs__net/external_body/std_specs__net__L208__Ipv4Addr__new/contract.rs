pub assume_specification[ Ipv4Addr::new ](a: u8, b: u8, c: u8, d: u8) -> (result: Ipv4Addr)
    ensures
        result@ == seq![a, b, c, d],
;
