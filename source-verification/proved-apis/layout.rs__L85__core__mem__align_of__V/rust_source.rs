pub const fn align_of<T>() -> usize {
    <T as SizedTypeProperties>::ALIGN
}
