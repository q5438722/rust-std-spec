pub assume_specification[ Ipv4Addr::to_bits ](address: Ipv4Addr) -> (result: u32)
    ensures
        result == (((address@[0] as u32) << 24) | ((address@[1] as u32) << 16) | ((
        address@[2] as u32) << 8) | (address@[3] as u32)),
;
