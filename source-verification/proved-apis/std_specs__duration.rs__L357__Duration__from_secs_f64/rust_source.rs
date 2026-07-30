pub fn from_secs_f64(secs: f64) -> Duration {
        match Duration::try_from_secs_f64(secs) {
            Ok(v) => v,
            Err(e) => panic!("{e}"),
        }
    }
