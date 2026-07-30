# Determinism audit: capacity.rs

- Targets: 25
- R0 results: `{'unsat': 19, 'unknown': 6}`

| Target | Status | R0 | Classification |
|---|---|---|---|
| `Vec::<T, A>::capacity` | ok | unsat | complete |
| `Vec::<T, A>::reserve_exact` | ok | unsat | complete |
| `Vec::<T, A>::try_reserve_exact` | ok | unknown | ok_inconclusive |
| `Vec::<T, A>::shrink_to_fit` | ok | unsat | complete |
| `Vec::<T, A>::shrink_to` | ok | unsat | complete |
| `String::capacity` | ok | unsat | complete |
| `String::with_capacity` | ok | unsat | complete |
| `String::reserve` | ok | unsat | complete |
| `String::reserve_exact` | ok | unsat | complete |
| `String::try_reserve` | ok | unknown | ok_inconclusive |
| `String::try_reserve_exact` | ok | unknown | ok_inconclusive |
| `String::shrink_to_fit` | ok | unsat | complete |
| `String::shrink_to` | ok | unsat | complete |
| `VecDeque::<T, A>::capacity` | ok | unsat | complete |
| `VecDeque::<T, A>::try_reserve` | ok | unknown | ok_inconclusive |
| `VecDeque::<T, A>::shrink_to_fit` | ok | unsat | complete |
| `VecDeque::<T, A>::shrink_to` | ok | unsat | complete |
| `BinaryHeap::<T, A>::capacity` | ok | unsat | complete |
| `BinaryHeap::<T>::with_capacity` | ok | unsat | complete |
| `BinaryHeap::<T, A>::reserve` | ok | unsat | complete |
| `BinaryHeap::<T, A>::reserve_exact` | ok | unsat | complete |
| `BinaryHeap::<T, A>::try_reserve` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::try_reserve_exact` | ok | unknown | ok_inconclusive |
| `BinaryHeap::<T, A>::shrink_to_fit` | ok | unsat | complete |
| `BinaryHeap::<T, A>::shrink_to` | ok | unsat | complete |
