use std::cell::Cell;
use std::cmp::Ordering;
use std::env;
use std::rc::Rc;

fn event(state: &Cell<u32>, name: &str) {
    let before = state.get();
    state.set(before + 1);
    eprintln!("event={name} state={before}->{}", before + 1);
}

struct Element {
    id: i32,
    interior: Cell<i32>,
}

#[derive(Eq)]
struct Key {
    slot: &'static str,
    rank: i32,
    state: Rc<Cell<u32>>,
    panic_in_lt: bool,
    panic_in_drop: bool,
}

impl PartialEq for Key {
    fn eq(&self, other: &Self) -> bool {
        self.rank == other.rank
    }
}

impl PartialOrd for Key {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.rank.cmp(&other.rank))
    }

    fn lt(&self, other: &Self) -> bool {
        event(&self.state, "ord-lt");
        if self.panic_in_lt {
            panic!("ord-lt-panic");
        }
        self.rank < other.rank
    }
}

impl Ord for Key {
    fn cmp(&self, other: &Self) -> Ordering {
        self.rank.cmp(&other.rank)
    }
}

impl Drop for Key {
    fn drop(&mut self) {
        event(&self.state, &format!("drop-key-{}", self.slot));
        if self.panic_in_drop {
            panic!("drop-key-{}-panic", self.slot);
        }
    }
}

struct FunctionDrop {
    state: Rc<Cell<u32>>,
    panic_on_drop: bool,
}

impl Drop for FunctionDrop {
    fn drop(&mut self) {
        event(&self.state, "drop-f");
        if self.panic_on_drop {
            panic!("drop-f-panic");
        }
    }
}

fn run_zst() {
    struct Zst;
    let state = Rc::new(Cell::new(0));
    let guard = FunctionDrop {
        state: Rc::clone(&state),
        panic_on_drop: false,
    };
    let mut values = [Zst, Zst, Zst];
    values.sort_unstable_by_key(move |_| {
        let _keep = &guard;
        0_i32
    });
    event(&state, "target-return");
}

fn run(scenario: &'static str) {
    if scenario == "zst" {
        run_zst();
        return;
    }

    let state = Rc::new(Cell::new(0));
    let observer = Rc::clone(&state);
    let calls = Rc::new(Cell::new(0_u32));
    let call_observer = Rc::clone(&calls);
    let guard = FunctionDrop {
        state: Rc::clone(&state),
        panic_on_drop: matches!(
            scenario,
            "f-drop-panic" | "key-panic-f-drop-double-panic"
        ),
    };
    let mut values = match scenario {
        "trivial" | "f-drop-panic" => Vec::new(),
        _ => vec![
            Element {
                id: 2,
                interior: Cell::new(0),
            },
            Element {
                id: 1,
                interior: Cell::new(0),
            },
        ],
    };

    values.sort_unstable_by_key(move |value| {
        let _keep = &guard;
        let call = calls.get();
        calls.set(call + 1);
        let slot = if call % 2 == 0 { "left" } else { "right" };
        event(&state, &format!("key-{slot}"));
        value.interior.set(value.interior.get() + 1);
        if scenario == "interior-mutation" {
            eprintln!(
                "interior id={} value={}",
                value.id,
                value.interior.get()
            );
        }
        if matches!(
            scenario,
            "left-key-panic" | "key-panic-f-drop-double-panic"
        ) && slot == "left"
        {
            panic!("left-key-panic");
        }
        if scenario == "right-key-panic" && slot == "right" {
            panic!("right-key-panic");
        }
        let duplicate_rank = if scenario == "duplicate-equal-keys" {
            0
        } else {
            value.id
        };
        Key {
            slot,
            rank: duplicate_rank,
            state: Rc::clone(&state),
            panic_in_lt: scenario.starts_with("ord-lt-panic")
                && slot == "left",
            panic_in_drop: match scenario {
                "right-drop-panic" => slot == "right",
                "left-drop-panic" => slot == "left",
                "ord-lt-panic-right-drop-double-panic" => slot == "right",
                "right-left-drop-double-panic" => true,
                _ => false,
            },
        }
    });

    event(&observer, "target-return");
    eprintln!("key-calls={}", call_observer.get());
}

fn main() {
    std::panic::set_hook(Box::new(|info| {
        eprintln!("panic-hook={info}");
    }));
    let scenario = env::args().nth(1).expect("scenario argument");
    run(Box::leak(scenario.into_boxed_str()));
}
