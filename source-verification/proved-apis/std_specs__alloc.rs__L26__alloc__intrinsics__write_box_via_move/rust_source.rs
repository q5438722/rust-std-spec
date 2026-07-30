pub fn write_box_via_move<T>(b: Box<MaybeUninit<T>>, x: T) -> Box<MaybeUninit<T>>;
