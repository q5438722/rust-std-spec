mod source {
    include!(env!("SLICE_ASCII_CASE_SOURCE"));
}

const BOUNDARIES: [u8; 19] = [
    0, 64, 65, 66, 89, 90, 91, 95, 96, 97, 98, 121, 122, 123, 126, 127, 128, 254, 255,
];

fn expected_upper(byte: u8) -> u8 {
    if byte >= 97 && byte <= 122 {
        byte - 32
    } else {
        byte
    }
}

fn expected_lower(byte: u8) -> u8 {
    if byte >= 65 && byte <= 90 {
        byte + 32
    } else {
        byte
    }
}

fn uppercase_bindings() -> [fn(&mut [u8]) -> (); 2] {
    [source::make_ascii_uppercase, <[u8]>::make_ascii_uppercase]
}

fn lowercase_bindings() -> [fn(&mut [u8]) -> (); 2] {
    [source::make_ascii_lowercase, <[u8]>::make_ascii_lowercase]
}

fn check_mapping(input: &[u8], bindings: [fn(&mut [u8]) -> (); 2], map: fn(u8) -> u8) {
    let expected: Vec<u8> = input.iter().copied().map(map).collect();
    for transform in bindings {
        let mut actual = input.to_vec();
        let address = actual.as_ptr();
        let result: () = transform(&mut actual);
        assert_eq!(result, ());
        assert_eq!(actual, expected, "input: {input:?}");
        assert_eq!(actual.len(), input.len());
        assert_eq!(actual.as_ptr(), address);
    }
}

fn check_ordered_sequences(bindings: [fn(&mut [u8]) -> (); 2], map: fn(u8) -> u8) {
    let ascending: Vec<u8> = (0..=255).collect();
    let descending: Vec<u8> = (0..=255).rev().collect();
    let mixed: Vec<u8> = (0..=255u16)
        .flat_map(|byte| [((byte * 73 + 19) % 256) as u8, byte as u8, 0, 255])
        .collect();
    for input in [ascending, descending, mixed] {
        check_mapping(&input, bindings, map);
    }
    check_mapping(b"aZzA09@[`{ Hello, WORLD!\0\x7f\x80\xff", bindings, map);
}

fn check_idempotence(bindings: [fn(&mut [u8]) -> (); 2], map: fn(u8) -> u8) {
    let input: Vec<u8> = (0..=255).collect();
    let expected: Vec<u8> = input.iter().copied().map(map).collect();
    for transform in bindings {
        let mut actual = input.clone();
        for _ in 0..4 {
            transform(&mut actual);
            assert_eq!(actual, expected);
        }
    }
}

fn check_local_subslices(bindings: [fn(&mut [u8]) -> (); 2], map: fn(u8) -> u8) {
    let mut input = vec![97, 90, 0];
    input.extend(0..=255);
    input.extend([255, 122, 65]);
    let length = input.len();
    for transform in bindings {
        for (start, end) in [
            (0, 0),
            (3, 3),
            (length, length),
            (0, 1),
            (length - 1, length),
            (3, length - 3),
            (0, length),
        ] {
            let mut actual = input.clone();
            let mut expected = input.clone();
            for byte in &mut expected[start..end] {
                *byte = map(*byte);
            }
            let address = actual.as_ptr();
            let result: () = transform(&mut actual[start..end]);
            assert_eq!(result, ());
            assert_eq!(actual, expected, "subslice {start}..{end}");
            assert_eq!(&actual[..start], &input[..start]);
            assert_eq!(&actual[end..], &input[end..]);
            assert_eq!(actual.len(), length);
            assert_eq!(actual.as_ptr(), address);
        }
    }
}

#[test]
fn uppercase_function_signature_and_unit_return() {
    for transform in uppercase_bindings() {
        let mut input = BOUNDARIES;
        let result: () = transform(&mut input);
        assert_eq!(result, ());
        assert_eq!(input, BOUNDARIES.map(expected_upper));
    }
}

#[test]
fn lowercase_function_signature_and_unit_return() {
    for transform in lowercase_bindings() {
        let mut input = BOUNDARIES;
        let result: () = transform(&mut input);
        assert_eq!(result, ());
        assert_eq!(input, BOUNDARIES.map(expected_lower));
    }
}

#[test]
fn uppercase_all_256_one_byte_inputs() {
    for byte in 0..=255 {
        check_mapping(&[byte], uppercase_bindings(), expected_upper);
    }
}

#[test]
fn lowercase_all_256_one_byte_inputs() {
    for byte in 0..=255 {
        check_mapping(&[byte], lowercase_bindings(), expected_lower);
    }
}

#[test]
fn empty_slices() {
    check_mapping(&[], uppercase_bindings(), expected_upper);
    check_mapping(&[], lowercase_bindings(), expected_lower);
}

#[test]
fn uppercase_mixed_ordered_sequences() {
    check_ordered_sequences(uppercase_bindings(), expected_upper);
}

#[test]
fn lowercase_mixed_ordered_sequences() {
    check_ordered_sequences(lowercase_bindings(), expected_lower);
}

#[test]
fn uppercase_boundaries_and_adjacent_punctuation() {
    check_mapping(&BOUNDARIES, uppercase_bindings(), expected_upper);
}

#[test]
fn lowercase_boundaries_and_adjacent_punctuation() {
    check_mapping(&BOUNDARIES, lowercase_bindings(), expected_lower);
}

#[test]
fn every_non_ascii_byte_is_unchanged() {
    let input: Vec<u8> = (128..=255).collect();
    for transform in uppercase_bindings().into_iter().chain(lowercase_bindings()) {
        let mut actual = input.clone();
        transform(&mut actual);
        assert_eq!(actual, input);
        transform(&mut actual);
        assert_eq!(actual, input);
    }
}

#[test]
fn uppercase_is_idempotent() {
    check_idempotence(uppercase_bindings(), expected_upper);
}

#[test]
fn lowercase_is_idempotent() {
    check_idempotence(lowercase_bindings(), expected_lower);
}

#[test]
fn alternating_transformations_follow_numeric_maps() {
    for uppercase in uppercase_bindings() {
        for lowercase in lowercase_bindings() {
            let mut actual: Vec<u8> = (0..=255).collect();
            let mut expected = actual.clone();
            for _ in 0..4 {
                uppercase(&mut actual);
                expected = expected.into_iter().map(expected_upper).collect();
                assert_eq!(actual, expected);
                lowercase(&mut actual);
                expected = expected.into_iter().map(expected_lower).collect();
                assert_eq!(actual, expected);
            }
        }
    }
}

#[test]
fn uppercase_subslice_mutation_is_local() {
    check_local_subslices(uppercase_bindings(), expected_upper);
}

#[test]
fn lowercase_subslice_mutation_is_local() {
    check_local_subslices(lowercase_bindings(), expected_lower);
}

#[test]
fn uppercase_calls_are_stable_const() {
    const SOURCE: [u8; 19] = {
        let mut input = BOUNDARIES;
        let _: () = source::make_ascii_uppercase(&mut input);
        input
    };
    const PUBLIC: [u8; 19] = {
        let mut input = BOUNDARIES;
        let _: () = <[u8]>::make_ascii_uppercase(&mut input);
        input
    };
    let expected = BOUNDARIES.map(expected_upper);
    assert_eq!(SOURCE, expected);
    assert_eq!(PUBLIC, expected);
}

#[test]
fn lowercase_calls_are_stable_const() {
    const SOURCE: [u8; 19] = {
        let mut input = BOUNDARIES;
        let _: () = source::make_ascii_lowercase(&mut input);
        input
    };
    const PUBLIC: [u8; 19] = {
        let mut input = BOUNDARIES;
        let _: () = <[u8]>::make_ascii_lowercase(&mut input);
        input
    };
    let expected = BOUNDARIES.map(expected_lower);
    assert_eq!(SOURCE, expected);
    assert_eq!(PUBLIC, expected);
}
