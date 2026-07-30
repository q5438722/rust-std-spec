# Determinism audit: collections_extra.rs

- Targets: 23
- R0 results: `{'unsat': 18, 'unknown': 5}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `BinaryHeap::<T>::new` | ok | unsat | complete |
| `BinaryHeap::<T, A>::len` | ok | unsat | complete |
| `BinaryHeap::<T, A>::is_empty` | ok | unsat | complete |
| `BinaryHeap::<T, A>::clear` | ok | unsat | complete |
| `BinaryHeap::<T, A>::push` | ok | unsat | complete |
| `BinaryHeap::<T, A>::append` | ok | unsat | complete |
| `BinaryHeap::<T, A>::pop` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::peek` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::as_slice` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::into_vec` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::into_sorted_vec` | ok | unknown | ok_inconclusive |
| `LinkedList::<T>::new` | ok | unsat | complete |
| `LinkedList::<T, A>::len` | ok | unsat | complete |
| `LinkedList::<T, A>::is_empty` | ok | unsat | complete |
| `LinkedList::<T, A>::clear` | ok | unsat | complete |
| `LinkedList::<T, A>::push_front` | ok | unsat | complete |
| `LinkedList::<T, A>::push_back` | ok | unsat | complete |
| `LinkedList::<T, A>::pop_front` | ok | unsat | complete |
| `LinkedList::<T, A>::pop_back` | ok | unsat | complete |
| `LinkedList::<T, A>::front` | ok | unsat | complete |
| `LinkedList::<T, A>::back` | ok | unsat | complete |
| `LinkedList::<T>::append` | ok | unsat | complete |
| `LinkedList::<T, A>::split_off` | ok | unsat | complete |
