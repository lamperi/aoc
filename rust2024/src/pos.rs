use num::traits::WrappingAdd;

use crate::direction::CardinalDirection;

#[derive(Debug,PartialEq,Eq,Copy,Clone,Hash)]
pub struct Pos2D<T> {
    pub x: T,
    pub y: T,
}

impl <T> std::ops::Add for Pos2D<T> 
where T: WrappingAdd {
    type Output = Self;

    fn add(self, rhs: Self) -> Self {
        Pos2D { x: self.x.wrapping_add(&rhs.x), y: self.y.wrapping_add(&rhs.y) }
    }
}

impl std::ops::Add<CardinalDirection> for Pos2D<usize> {
    type Output = Self;

    fn add(self, rhs: CardinalDirection) -> Self {
        Pos2D {
            x: self.x.wrapping_add_signed(rhs.dx().into()),
            y: self.y.wrapping_add_signed(rhs.dy().into())
        }
    }
}

impl std::ops::AddAssign<CardinalDirection> for Pos2D<usize> {
    fn add_assign(&mut self, rhs: CardinalDirection) {
        self.x = self.x.wrapping_add_signed(rhs.dx().into());
        self.y = self.y.wrapping_add_signed(rhs.dy().into());
    }
}