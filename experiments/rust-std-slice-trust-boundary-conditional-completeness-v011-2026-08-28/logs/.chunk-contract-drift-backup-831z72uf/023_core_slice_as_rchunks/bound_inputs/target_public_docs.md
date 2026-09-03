Splits the slice into a slice of `N`-element arrays,
starting at the end of the slice,
and a remainder slice with length strictly less than `N`.

The remainder is meaningful in the division sense.  Given
`let (remainder, chunks) = slice.as_rchunks()`, then:
- `remainder.len()` equals `slice.len() % N`,
- `chunks.len()` equals `slice.len() / N`, and
- `slice.len()` equals `chunks.len() * N + remainder.len()`.

You can flatten the chunks back into a slice-of-`T` with [`as_flattened`].

[`as_flattened`]: slice::as_flattened

# Panics

Panics if `N` is zero.

Note that this check is against a const generic parameter, not a runtime
value, and thus a particular monomorphization will either always panic
or it will never panic.

# Examples

```
let slice = ['l', 'o', 'r', 'e', 'm'];
let (remainder, chunks) = slice.as_rchunks();
assert_eq!(remainder, &['l']);
assert_eq!(chunks, &[['o', 'r'], ['e', 'm']]);
```
