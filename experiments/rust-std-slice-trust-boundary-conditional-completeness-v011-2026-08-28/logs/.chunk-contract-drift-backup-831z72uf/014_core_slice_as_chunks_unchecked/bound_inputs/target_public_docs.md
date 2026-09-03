Splits the slice into a slice of `N`-element arrays,
assuming that there's no remainder.

This is the inverse operation to [`as_flattened`].

[`as_flattened`]: slice::as_flattened

As this is `unsafe`, consider whether you could use [`as_chunks`] or
[`as_rchunks`] instead, perhaps via something like
`if let (chunks, []) = slice.as_chunks()` or
`let (chunks, []) = slice.as_chunks() else { unreachable!() };`.

[`as_chunks`]: slice::as_chunks
[`as_rchunks`]: slice::as_rchunks

# Safety

This may only be called when
- The slice splits exactly into `N`-element chunks (aka `self.len() % N == 0`).
- `N != 0`.

# Examples

```
let slice: &[char] = &['l', 'o', 'r', 'e', 'm', '!'];
let chunks: &[[char; 1]] =
// SAFETY: 1-element chunks never have remainder
unsafe { slice.as_chunks_unchecked() };
assert_eq!(chunks, &[['l'], ['o'], ['r'], ['e'], ['m'], ['!']]);
let chunks: &[[char; 3]] =
// SAFETY: The slice length (6) is a multiple of 3
unsafe { slice.as_chunks_unchecked() };
assert_eq!(chunks, &[['l', 'o', 'r'], ['e', 'm', '!']]);

// These would be unsound:
// let chunks: &[[_; 5]] = slice.as_chunks_unchecked() // The slice length is not a multiple of 5
// let chunks: &[[_; 0]] = slice.as_chunks_unchecked() // Zero-length chunks are never allowed
```
