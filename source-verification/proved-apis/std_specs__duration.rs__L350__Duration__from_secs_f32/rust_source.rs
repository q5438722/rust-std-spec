pub fn from_secs_f32(secs: f32) -> Duration {
        match Duration::try_from_secs_f32(secs) {
            Ok(v) => v,
            Err(e) => panic!("{e}"),
        }
    }
