pub const fn size_of<T>() -> usize {
    <T as SizedTypeProperties>::SIZE
}
