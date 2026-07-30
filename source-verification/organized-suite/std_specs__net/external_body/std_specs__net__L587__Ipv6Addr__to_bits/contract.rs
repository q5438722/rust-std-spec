pub assume_specification[ Ipv6Addr::to_bits ](address: Ipv6Addr) -> (result: u128)
    ensures
        result as int == (address@[0] as int) * 0x100_0000_0000_0000_0000_0000_0000_0000 + (
        address@[1] as int) * 0x1_0000_0000_0000_0000_0000_0000_0000 + (address@[2] as int)
            * 0x100_0000_0000_0000_0000_0000_0000 + (address@[3] as int)
            * 0x1_0000_0000_0000_0000_0000_0000 + (address@[4] as int)
            * 0x100_0000_0000_0000_0000_0000 + (address@[5] as int) * 0x1_0000_0000_0000_0000_0000
            + (address@[6] as int) * 0x100_0000_0000_0000_0000 + (address@[7] as int)
            * 0x1_0000_0000_0000_0000 + (address@[8] as int) * 0x100_0000_0000_0000 + (
        address@[9] as int) * 0x1_0000_0000_0000 + (address@[10] as int) * 0x100_0000_0000 + (
        address@[11] as int) * 0x1_0000_0000 + (address@[12] as int) * 0x100_0000 + (
        address@[13] as int) * 0x1_0000 + (address@[14] as int) * 0x100 + address@[15] as int,
;
