use std::cell::Cell;
use std::cmp::Ordering;
use std::env;
use std::rc::Rc;

fn event(state: &Cell<u32>, name: &str) {
    let before = state.get();
    state.set(before + 1);
    eprintln!("event={name} state={before}->{}", before + 1);
}

#[derive(Eq)]
struct Key {
    name: &'static str,
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
        event(&self.state, &format!("drop-{}", self.name));
        if self.panic_in_drop {
            panic!("drop-{}-panic", self.name);
        }
    }
}

fn run(scenario: &str) {
    let state = Rc::new(Cell::new(0));
    let left = 10;
    let right = 20;
    let mut key_calls = 0_u32;
    let mut f = |value: &i32| {
        key_calls += 1;
        let name = if *value == left { "left" } else { "right" };
        event(&state, &format!("key-{name}"));
        if scenario == "first-key-panic" && name == "left" {
            panic!("first-key-panic");
        }
        if (
            scenario == "second-key-panic"
                || scenario == "second-key-panic-left-drop-panic"
        ) && name == "right"
        {
            panic!("second-key-panic");
        }
        Key {
            name,
            rank: *value,
            state: Rc::clone(&state),
            panic_in_lt: (
                scenario == "ord-lt-panic"
                    || scenario == "ord-lt-panic-right-drop-panic"
                    || scenario == "ord-lt-panic-left-drop-panic"
            ) && name == "left",
            panic_in_drop: match scenario {
                "right-drop-panic" => name == "right",
                "left-drop-panic" => name == "left",
                "ord-lt-panic-right-drop-panic" => name == "right",
                "ord-lt-panic-left-drop-panic" => name == "left",
                "right-drop-panic-left-drop-panic" => true,
                "second-key-panic-left-drop-panic" => name == "left",
                _ => false,
            },
        }
    };

    let result = f(&left).lt(&f(&right));
    event(&state, &format!("result-{result}"));
}

fn main() {
    std::panic::set_hook(Box::new(|info| {
        eprintln!("panic-hook={info}");
    }));
    let scenario = env::args().nth(1).expect("scenario argument");
    run(&scenario);
}
