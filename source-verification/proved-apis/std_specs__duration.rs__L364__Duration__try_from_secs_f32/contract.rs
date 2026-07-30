pub assume_specification[ Duration::try_from_secs_f32 ](secs: f32) -> (result: Result<
    Duration,
    TryFromFloatSecsError,
>)
    ensures
        duration_secs_f32_valid(secs) ==> (result matches Ok(value) && value@
            == duration_from_secs_f32_nanos(secs)),
        !duration_secs_f32_valid(secs) ==> (result matches Err(error) && error@
            == if duration_secs_f32_is_negative(secs) {
            TryFromFloatSecsErrorView::Negative
        } else {
            TryFromFloatSecsErrorView::OverflowOrNan
        }),
;
