#![feature(ptr_metadata)]
#![allow(dead_code)]

mod source {
    include!(env!("SLICE_NATIVE_SOURCE"));
}

fn first_cannot_escape() -> Option<&'static String> {
    let local = [String::from("local")];
    source::first(&local)
}

fn last_cannot_escape() -> Option<&'static String> {
    let local = [String::from("local")];
    source::last(&local)
}

fn split_first_cannot_escape() -> Option<(&'static String, &'static [String])> {
    let local = [String::from("local")];
    source::split_first(&local)
}

fn split_last_cannot_escape() -> Option<(&'static String, &'static [String])> {
    let local = [String::from("local")];
    source::split_last(&local)
}
