Splits the slice into a slice of `N`-element arrays,
starting at the beginning of the slice,
and a remainder slice with length strictly less than `N`.

The remainder is meaningful in the division sense.  Given
`let (chunks, remainder) = slice.as_chunks()`, then:
- `chunks.len()` equals `slice.len() / N`,
- `remainder.len()` equals `slice.len() % N`, and
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
let (chunks, remainder) = slice.as_chunks();
assert_eq!(chunks, &[['l', 'o'], ['r', 'e']]);
assert_eq!(remainder, &['m']);
```

If you expect the slice to be an exact multiple, you can combine
`let`-`else` with an empty slice pattern:
```
let slice = ['R', 'u', 's', 't'];
let (chunks, []) = slice.as_chunks::<2>() else {
panic!("slice didn't have even length")
};
assert_eq!(chunks, &[['R', 'u'], ['s', 't']]);
```
