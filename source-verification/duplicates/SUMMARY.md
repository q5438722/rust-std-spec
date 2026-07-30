# Duplicate direct-contract records

- Direct records: **539**
- Canonical API paths: **447**
- Extra records after path deduplication: **92**
- Paths with more than one record: **33**

A duplicate path usually does not mean duplicated Rust code. Contract records
retain concrete impl type, bounds, cfg variant, and source location, while
canonical API paths intentionally collapse them.

Largest examples:

- `core::clone::Clone::clone`: 18 records
- `core::default::Default::default`: 16 records
- `core::cmp::PartialEq::eq`: 9 records
- `core::ops::RangeBounds::end_bound`: 7 records
- `core::ops::RangeBounds::start_bound`: 7 records
- `core::iter::IntoIterator::into_iter`: 5 records
- `core::cmp::PartialEq::ne`: 4 records
- `core::cmp::PartialOrd::partial_cmp`: 4 records
- `core::cmp::PartialOrd::ge`: 3 records
- `core::cmp::PartialOrd::gt`: 3 records
- `core::cmp::PartialOrd::le`: 3 records
- `core::cmp::PartialOrd::lt`: 3 records
- `core::ops::Deref::deref`: 3 records
- `alloc::collections::BTreeMap::contains_key`: 2 records
- `alloc::collections::BTreeMap::get`: 2 records
