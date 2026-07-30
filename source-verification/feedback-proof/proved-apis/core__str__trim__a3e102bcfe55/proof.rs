#![allow(dead_code)]
#![feature(pattern)]

use core::str::pattern::{DoubleEndedSearcher, Pattern};
use vstd::prelude::*;

verus! {

pub open spec fn is_whitespace(c: char) -> bool {
    let code = c as nat;
    (code >= 0x0009 && 0x000d >= code)
        || code == 0x0020
        || code == 0x0085
        || code == 0x00a0
        || code == 0x1680
        || (code >= 0x2000 && 0x200a >= code)
        || code == 0x2028
        || code == 0x2029
        || code == 0x202f
        || code == 0x205f
        || code == 0x3000
}

#[verifier::external_trait_specification]
#[verifier::external_trait_extension(PatternSpec via PatternSpecImpl)]
pub trait ExPattern: Sized {
    type ExternalTraitSpecificationFor: Pattern;

    spec fn predicate_requires(&self, c: char) -> bool;

    spec fn predicate_ensures(&self, c: char, result: bool) -> bool;
}

impl<F> PatternSpecImpl for F
where
    F: FnMut(char) -> bool + Copy,
{
    open spec fn predicate_requires(&self, c: char) -> bool {
        (*self).requires((c,))
    }

    open spec fn predicate_ensures(&self, c: char, result: bool) -> bool {
        (*self).ensures((c,), result)
    }
}

proof fn lemma_fn_pattern_spec<F>(f: F, c: char, result: bool)
where
    F: FnMut(char) -> bool + Copy,
    ensures
        PatternSpec::predicate_requires(&f, c) == f.requires((c,)),
        PatternSpec::predicate_ensures(&f, c, result) == f.ensures((c,), result),
{
    assert(PatternSpec::predicate_requires(&f, c) == f.requires((c,)));
    assert(PatternSpec::predicate_ensures(&f, c, result) == f.ensures((c,), result));
}

pub open spec fn pattern_has_result<P: Pattern>(pat: &P, c: char) -> bool {
    exists|result: bool| pat.predicate_ensures(c, result)
}

pub open spec fn pattern_result<P: Pattern>(pat: &P, c: char) -> bool
    recommends
        pattern_has_result(pat, c),
{
    choose|result: bool| pat.predicate_ensures(c, result)
}

pub open spec fn trim_by<P: Pattern>(chars: Seq<char>, pat: &P) -> Seq<char> {
    chars.fold_left(
        (Seq::<char>::empty(), Seq::<char>::empty()),
        |state: (Seq<char>, Seq<char>), c: char| {
            if pattern_result(pat, c) {
                if state.0.len() == 0 {
                    state
                } else {
                    (state.0, state.1.push(c))
                }
            } else {
                ((state.0 + state.1).push(c), Seq::<char>::empty())
            }
        },
    ).0
}

proof fn lemma_trim_by_whitespace<P: Pattern>(chars: Seq<char>, pat: &P)
    requires
        forall|c: char| #[trigger] pattern_has_result(pat, c),
        forall|c: char| #[trigger] pattern_result(pat, c) == is_whitespace(c),
    ensures
        chars.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            |state: (Seq<char>, Seq<char>), c: char| {
                if pattern_result(pat, c) {
                    if state.0.len() == 0 {
                        state
                    } else {
                        (state.0, state.1.push(c))
                    }
                } else {
                    ((state.0 + state.1).push(c), Seq::<char>::empty())
                }
            },
        ) == chars.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            |state: (Seq<char>, Seq<char>), c: char| {
                let code = c as nat;
                if (code >= 0x0009 && 0x000d >= code)
                    || code == 0x0020
                    || code == 0x0085
                    || code == 0x00a0
                    || code == 0x1680
                    || (code >= 0x2000 && 0x200a >= code)
                    || code == 0x2028
                    || code == 0x2029
                    || code == 0x202f
                    || code == 0x205f
                    || code == 0x3000
                {
                    if state.0.len() == 0 {
                        state
                    } else {
                        (state.0, state.1.push(c))
                    }
                } else {
                    ((state.0 + state.1).push(c), Seq::<char>::empty())
                }
            },
        ),
    decreases
        chars.len(),
{
    reveal(is_whitespace);
    reveal_with_fuel(Seq::fold_left, 2);
    if chars.len() > 0 {
        lemma_trim_by_whitespace(chars.drop_last(), pat);
        assert(pattern_result(pat, chars.last()) == is_whitespace(chars.last()));
    }
}

#[verifier::when_used_as_spec(is_whitespace)]
pub assume_specification[ char::is_whitespace ](c: char) -> (result: bool)
    ensures
        result == is_whitespace(c),
;

#[verifier::allow(undeclared_external_trait)]
pub assume_specification<P>[ str::trim_matches ](
    s: &str,
    pat: P,
) -> (res: &str)
where
    P: Pattern,
    for<'a> P::Searcher<'a>: DoubleEndedSearcher<'a>,
    requires
        forall|c: char| pat.predicate_requires(c),
        forall|c: char, left: bool, right: bool|
            pat.predicate_ensures(c, left)
                && pat.predicate_ensures(c, right) ==> left == right,
    ensures
        forall|c: char| #[trigger] pattern_has_result(&pat, c),
        res@ == trim_by(s@, &pat),
;

pub fn source_core_str_trim(s: &str) -> (res: &str)
    ensures
        res@ == s@.fold_left(
            (Seq::<char>::empty(), Seq::<char>::empty()),
            |state: (Seq<char>, Seq<char>), c: char| {
                let code = c as nat;
                if (code >= 0x0009 && 0x000d >= code)
                    || code == 0x0020
                    || code == 0x0085
                    || code == 0x00a0
                    || code == 0x1680
                    || (code >= 0x2000 && 0x200a >= code)
                    || code == 0x2028
                    || code == 0x2029
                    || code == 0x202f
                    || code == 0x205f
                    || code == 0x3000
                {
                    if state.0.len() == 0 {
                        state
                    } else {
                        (state.0, state.1.push(c))
                    }
                } else {
                    ((state.0 + state.1).push(c), Seq::<char>::empty())
                }
            },
        ).0,
{
    proof {
        assert forall|c: char, result: bool|
            char::is_whitespace.ensures((c,), result) implies
                result == is_whitespace(c) by {}
        assert forall|c: char| char::is_whitespace.requires((c,)) by {}
        assert forall|c: char, left: bool, right: bool|
            char::is_whitespace.ensures((c,), left)
                && char::is_whitespace.ensures((c,), right) implies left == right by {}
        assert forall|c: char|
            PatternSpec::predicate_requires(&char::is_whitespace, c) by {
            lemma_fn_pattern_spec(char::is_whitespace, c, false);
            assert(char::is_whitespace.requires((c,)));
        }
        assert forall|c: char, left: bool, right: bool|
            PatternSpec::predicate_ensures(&char::is_whitespace, c, left)
                && PatternSpec::predicate_ensures(&char::is_whitespace, c, right)
                implies left == right by {
            lemma_fn_pattern_spec(char::is_whitespace, c, left);
            lemma_fn_pattern_spec(char::is_whitespace, c, right);
            assert(char::is_whitespace.ensures((c,), left));
            assert(char::is_whitespace.ensures((c,), right));
        }
    }
    let res = s.trim_matches(char::is_whitespace);
    proof {
        assert forall|c: char| #[trigger] pattern_result(&char::is_whitespace, c)
            == is_whitespace(c) by {
            assert(pattern_has_result(&char::is_whitespace, c));
            let result = choose|result: bool|
                PatternSpec::predicate_ensures(&char::is_whitespace, c, result);
            lemma_fn_pattern_spec(char::is_whitespace, c, result);
            assert(char::is_whitespace.ensures((c,), result));
        }
        lemma_trim_by_whitespace(s@, &char::is_whitespace);
        reveal(trim_by);
    }
    res
}

} // verus!

fn main() {}