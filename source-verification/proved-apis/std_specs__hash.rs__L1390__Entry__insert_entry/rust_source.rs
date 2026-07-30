pub fn insert_entry(self, value: V) -> OccupiedEntry<'a, K, V, A> {
        match self {
            Occupied(mut entry) => {
                entry.insert(value);
                entry
            }
            Vacant(entry) => entry.insert_entry(value),
        }
    }
