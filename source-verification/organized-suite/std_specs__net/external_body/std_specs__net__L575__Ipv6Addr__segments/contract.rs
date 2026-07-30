pub assume_specification[ Ipv6Addr::segments ](address: &Ipv6Addr) -> (result: [u16; 8])
    ensures
        (result@[0] as int) == (address@[0] as int) * 256 + address@[1] as int,
        (result@[1] as int) == (address@[2] as int) * 256 + address@[3] as int,
        (result@[2] as int) == (address@[4] as int) * 256 + address@[5] as int,
        (result@[3] as int) == (address@[6] as int) * 256 + address@[7] as int,
        (result@[4] as int) == (address@[8] as int) * 256 + address@[9] as int,
        (result@[5] as int) == (address@[10] as int) * 256 + address@[11] as int,
        (result@[6] as int) == (address@[12] as int) * 256 + address@[13] as int,
        (result@[7] as int) == (address@[14] as int) * 256 + address@[15] as int,
;
