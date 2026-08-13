    pub fn split_off_mut<'a, R: OneSidedRange<usize>>(
        self: &mut &'a mut Self,
        range: R,
    ) -> Option<&'a mut Self> {
        let (direction, split_index) = split_point_of(range)?;
        if split_index > self.len() {
            return None;
        }
        let (front, back) = mem::take(self).split_at_mut(split_index);
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
