    pub fn split_off<'a, R: OneSidedRange<usize>>(
        self: &mut &'a Self,
        range: R,
    ) -> Option<&'a Self> {
        let (direction, split_index) = split_point_of(range)?;
        if split_index > self.len() {
            return None;
        }
        let (front, back) = self.split_at(split_index);
        match direction {
            Direction::Front => {
                *self = back;
                Some(front)
            }
            Direction::Back => {
                *self = front;
                Some(back)
            }
        }
    }
