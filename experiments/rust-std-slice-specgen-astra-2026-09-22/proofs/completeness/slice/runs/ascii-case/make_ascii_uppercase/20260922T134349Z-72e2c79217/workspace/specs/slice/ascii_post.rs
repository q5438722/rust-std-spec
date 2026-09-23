use vstd::prelude::*;

verus! {

pub open spec fn uppercase_byte(byte: u8) -> u8 {
    if b'a' <= byte <= b'z' { (byte - 32) as u8 } else { byte }
}

pub open spec fn lowercase_byte(byte: u8) -> u8 {
    if b'A' <= byte <= b'Z' { (byte + 32) as u8 } else { byte }
}

pub open spec fn uppercase_post(initial: Seq<u8>, result: Seq<u8>) -> bool {
    result =~= initial.map_values(|byte: u8| uppercase_byte(byte))
}

pub open spec fn lowercase_post(initial: Seq<u8>, result: Seq<u8>) -> bool {
    result =~= initial.map_values(|byte: u8| lowercase_byte(byte))
}

}
