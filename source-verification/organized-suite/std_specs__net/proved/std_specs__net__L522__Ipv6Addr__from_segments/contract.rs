pub assume_specification[ Ipv6Addr::from_segments ](segments: [u16; 8]) -> (result: Ipv6Addr)
    ensures
        result@ == seq![
            ((segments@[0] >> 8) & 0xff) as u8,
            (segments@[0] & 0xff) as u8,
            ((segments@[1] >> 8) & 0xff) as u8,
            (segments@[1] & 0xff) as u8,
            ((segments@[2] >> 8) & 0xff) as u8,
            (segments@[2] & 0xff) as u8,
            ((segments@[3] >> 8) & 0xff) as u8,
            (segments@[3] & 0xff) as u8,
            ((segments@[4] >> 8) & 0xff) as u8,
            (segments@[4] & 0xff) as u8,
            ((segments@[5] >> 8) & 0xff) as u8,
            (segments@[5] & 0xff) as u8,
            ((segments@[6] >> 8) & 0xff) as u8,
            (segments@[6] & 0xff) as u8,
            ((segments@[7] >> 8) & 0xff) as u8,
            (segments@[7] & 0xff) as u8,
        ],
;
