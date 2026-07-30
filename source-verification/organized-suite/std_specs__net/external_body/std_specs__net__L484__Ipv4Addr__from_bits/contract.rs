pub assume_specification[ Ipv4Addr::from_bits ](bits: u32) -> (result: Ipv4Addr)
    ensures
        result@ == seq![
            (bits >> 24) as u8,
            ((bits >> 16) & 0xff) as u8,
            ((bits >> 8) & 0xff) as u8,
            (bits & 0xff) as u8,
        ],
;
