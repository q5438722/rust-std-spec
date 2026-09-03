Splits the slice into a slice of `N`-element arrays,
starting at the end of the slice,
and a remainder slice with length strictly less than `N`.

The remainder is meaningful in the division sense.  Given
`let (remainder, chunks) = slice.as_rchunks_mut()`, then:
- `remainder.len()` equals `slice.len() % N`,
- `chunks.len()` equals `slice.len() / N`, and
- `slice.len()` equals `chunks.len() * N + remainder.len()`.

You can flatten the chunks back into a slice-of-`T` with [`as_flattened_mut`].

[`as_flattened_mut`]: slice::as_flattened_mut

# Panics

Panics if `N` is zero.

Note that this check is against a const generic parameter, not a runtime
value, and thus a particular monomorphization will either always panic
or it will never panic.

# Examples

```
let v = &mut [0, 0, 0, 0, 0];
let mut count = 1;

let (remainder, chunks) = v.as_rchunks_mut();
remainder[0] = 9;
for chunk in chunks {
*chunk = [count; 2];
count += 1;
}
assert_eq!(v, &[9, 1, 1, 2, 2]);
```
