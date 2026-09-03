/// Trait for types that form a [total order](https://en.wikipedia.org/wiki/Total_order).
///
/// Implementations must be consistent with the [`PartialOrd`] implementation, and ensure `max`,
/// `min`, and `clamp` are consistent with `cmp`:
///
/// - `partial_cmp(a, b) == Some(cmp(a, b))`.
/// - `max(a, b) == max_by(a, b, cmp)` (ensured by the default implementation).
/// - `min(a, b) == min_by(a, b, cmp)` (ensured by the default implementation).
/// - For `a.clamp(min, max)`, see the [method docs](#method.clamp) (ensured by the default
///   implementation).
///
/// Violating these requirements is a logic error. The behavior resulting from a logic error is not
/// specified, but users of the trait must ensure that such logic errors do *not* result in
/// undefined behavior. This means that `unsafe` code **must not** rely on the correctness of these
/// methods.
///
/// ## Corollaries
///
/// From the above and the requirements of `PartialOrd`, it follows that for all `a`, `b` and `c`:
///
/// - exactly one of `a < b`, `a == b` or `a > b` is true; and
/// - `<` is transitive: `a < b` and `b < c` implies `a < c`. The same must hold for both `==` and
///   `>`.
///
/// Mathematically speaking, the `<` operator defines a strict [weak order]. In cases where `==`
/// conforms to mathematical equality, it also defines a strict [total order].
///
/// [weak order]: https://en.wikipedia.org/wiki/Weak_ordering
/// [total order]: https://en.wikipedia.org/wiki/Total_order
