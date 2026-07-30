pub assume_specification[ IpAddr::to_canonical ](address: &IpAddr) -> (result: IpAddr)
    ensures
        result@ == match address@ {
            IpAddrView::V4(bytes) => IpAddrView::V4(bytes),
            IpAddrView::V6(bytes) => if bytes.len() == 16 && bytes.subrange(0, 12) == Seq::new(
                10,
                |i: int| 0u8,
            ) + seq![0xffu8, 0xffu8] {
                IpAddrView::V4(bytes.subrange(12, 16))
            } else {
                IpAddrView::V6(bytes)
            },
        },
;
