pub fn key(&self) -> &K {
        match *self {
            Occupied(ref entry) => entry.key(),
            Vacant(ref entry) => entry.key(),
        }
    }
