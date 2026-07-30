pub assume_specification<'a>[ Location::file_as_c_str ](location: &Location<'a>) -> (result:
    &'a core::ffi::CStr)
    ensures
        result@ == encode_utf8(location@.file),
;
