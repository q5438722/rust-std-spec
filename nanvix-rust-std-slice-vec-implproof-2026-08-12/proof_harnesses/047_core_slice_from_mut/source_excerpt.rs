pub const fn from_mut<T>(s: &mut T) -> &mut [T] {
    array::from_mut(s)
}
