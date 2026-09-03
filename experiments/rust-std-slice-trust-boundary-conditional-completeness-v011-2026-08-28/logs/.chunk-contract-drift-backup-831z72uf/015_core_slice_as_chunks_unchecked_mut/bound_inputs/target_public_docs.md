Splits the slice into a slice of `N`-element arrays,
assuming that there's no remainder.

This is the inverse operation to [`as_flattened_mut`].

[`as_flattened_mut`]: slice::as_flattened_mut

As this is `unsafe`, consider whether you could use [`as_chunks_mut`] or
[`as_rchunks_mut`] instead, perhaps via something like
`if let (chunks, []) = slice.as_chunks_mut()` or
`let (chunks, []) = slice.as_chunks_mut() else { unreachable!() };`.

[`as_chunks_mut`]: slice::as_chunks_mut
[`as_rchunks_mut`]: slice::as_rchunks_mut

# Safety

This may only be called when
- The slice splits exactly into `N`-element chunks (aka `self.len() % N == 0`).
- `N != 0`.

# Examples

```
let slice: &mut [char] = &mut ['l', 'o', 'r', 'e', 'm', '!'];
let chunks: &mut [[char; 1]] =
// SAFETY: 1-element chunks never have remainder
unsafe { slice.as_chunks_unchecked_mut() };
chunks[0] = ['L'];
assert_eq!(chunks, &[['L'], ['o'], ['r'], ['e'], ['m'], ['!']]);
let chunks: &mut [[char; 3]] =
// SAFETY: The slice length (6) is a multiple of 3
unsafe { slice.as_chunks_unchecked_mut() };
chunks[1] = ['a', 'x', '?'];
assert_eq!(slice, &['L', 'o', 'r', 'a', 'x', '?']);

// These would be unsound:
// let chunks: &[[_; 5]] = slice.as_chunks_unchecked_mut() // The slice length is not a multiple of 5
// let chunks: &[[_; 0]] = slice.as_chunks_unchecked_mut() // Zero-length chunks are never allowed
```
