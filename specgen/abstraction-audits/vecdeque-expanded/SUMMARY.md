# Determinism audit: vecdeque.rs

- Targets: 30
- R0 results: `{'unsat': 26, 'unknown': 4}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `VecDeque::<T, A>::index` | ok | unsat | complete |
| `VecDeque::<T, A>::len` | ok | unsat | complete |
| `VecDeque::<T>::new` | ok | unsat | complete |
| `<VecDeque<T> as core::default::Default>::default` | ok | unsat | complete |
| `VecDeque::<T>::with_capacity` | ok | unsat | complete |
| `VecDeque::<T, A>::reserve` | ok | unsat | complete |
| `VecDeque::<T, A>::reserve_exact` | ok | unsat | complete |
| `VecDeque::<T, A>::try_reserve_exact` | ok | unknown | ok_inconclusive |
| `VecDeque::<T, A>::push_back` | ok | unsat | complete |
| `VecDeque::<T, A>::push_front` | ok | unsat | complete |
| `VecDeque::<T, A>::pop_back` | ok | unsat | complete |
| `VecDeque::<T, A>::pop_front` | ok | unsat | complete |
| `VecDeque::<T, A>::is_empty` | ok | unsat | complete |
| `VecDeque::<T, A>::front` | ok | unsat | complete |
| `VecDeque::<T, A>::back` | ok | unsat | complete |
| `VecDeque::<T, A>::get` | ok | unsat | complete |
| `VecDeque::<T, A>::as_slices` | ok | unknown | ok_inconclusive |
| `VecDeque::<T, A>::contains` | ok | unsat | complete |
| `VecDeque::<T, A>::rotate_left` | ok | unsat | complete |
| `VecDeque::<T, A>::rotate_right` | ok | unsat | complete |
| `VecDeque::<T, A>::swap` | ok | unsat | complete |
| `VecDeque::<T, A>::append` | ok | unsat | complete |
| `VecDeque::<T, A>::insert` | ok | unsat | complete |
| `VecDeque::<T, A>::remove` | ok | unsat | complete |
| `VecDeque::<T, A>::clear` | ok | unsat | complete |
| `VecDeque::<T, A>::split_off` | ok | unsat | complete |
| `<VecDeque<T, A> as Clone>::clone` | ok | unknown | ok_inconclusive |
| `VecDeque::<T, A>::truncate` | ok | unsat | complete |
| `VecDeque::<T, A>::resize` | ok | unknown | ok_inconclusive |
| `VecDeque::<T, A>::iter` | ok | unsat | complete |
