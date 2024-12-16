use std::fs;
use std::io;

fn guess_day_from_executable() -> io::Result<u8> {
    let path = std::env::current_exe()?;
    let num = path.file_name()
        .and_then(|b| b.to_str())
        .map(|s| s.to_owned())
        .and_then(|s| s.strip_prefix("day").map(|s| s.to_owned()))
        .map(|s| {
            if let Some(stripped) = s.strip_suffix(".exe") {
                stripped.to_owned()
            } else {
                s
            }
        })
        .and_then(|s| s.parse::<u8>().ok())
        .unwrap_or_default();
    Ok(num)
}

pub fn get_input() -> io::Result<String> {
    let day = guess_day_from_executable()?;
    let path: String = format!("../2024/{day}/input.txt");
    let input: String = fs::read_to_string(path)?;
    Ok(input)
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
pub enum CardinalDirection {
    North,
    West,
    South,
    East,
}

impl CardinalDirection {
    pub fn all() -> Vec<Self> {
        vec![Self::North, Self::West, Self::South, Self::East]
    }

    pub fn is_horizontal(&self) -> bool {
        matches!(self, Self::West | Self::East)
    }
    pub fn is_vertical(&self) -> bool {
        matches!(self, Self::North | Self::South)
    }
    pub fn turn_right(&self) -> Self {
        match self {
            Self::North => Self::East,
            Self::East => Self::South,
            Self::South => Self::West,
            Self::West => Self::North
        }
    }
    pub fn turn_left(&self) -> Self {
        match self {
            Self::North => Self::West,
            Self::West => Self::South,
            Self::South => Self::East,
            Self::East => Self::North
        }
    }
    pub fn dy(&self) -> i8 {
        match self {
            CardinalDirection::North => -1,
            CardinalDirection::South => 1,
            _ => 0,
        }
    }
    pub fn dx(&self) -> i8 {
        match self {
            CardinalDirection::West => -1,
            CardinalDirection::East => 1,
            _ => 0,
        }
    }

    pub fn shift(&self, pos: (usize, usize)) -> (usize, usize) {
        let y = pos.0.wrapping_add_signed(self.dy().into());
        let x = pos.1.wrapping_add_signed(self.dx().into());
        (y, x)
    }

    pub fn shift_i32(&self, pos: (i32, i32)) -> (i32, i32) {
        let y = pos.0.wrapping_add(self.dy().into());
        let x = pos.1.wrapping_add(self.dx().into());
        (y, x)
    }
    

}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
pub enum EightDirection {
    North,
    NorthWest,
    West,
    SouthWest,
    South,
    SouthEast,
    East,
    NorthEast,
}

impl EightDirection {
    pub fn cardinal_directions() -> Vec<Self> {
        vec![Self::North, Self::West, Self::South, Self::East]
    }

    pub fn eight_directions() -> Vec<Self> {
        vec![
            Self::North, Self::NorthWest, Self::West, Self::SouthWest,
            Self::South, Self::SouthEast, Self::East, Self::NorthEast]
    }

    pub fn is_horizontal(&self) -> bool {
        matches!(self, Self::West | Self::East)
    }
    pub fn is_vertical(&self) -> bool {
        matches!(self, Self::North | Self::South)
    }
    pub fn is_diagonal(&self) -> bool {
        matches!(self, Self::NorthWest | Self::NorthEast | Self::SouthWest | Self::SouthEast)
    }
    pub fn dy(&self) -> i8 {
        match self {
            Self::North | Self::NorthWest | Self::NorthEast => -1,
            Self::South | Self::SouthWest | Self::SouthEast => 1,
            _ => 0,
        }
    }
    pub fn dx(&self) -> i8 {
        match self {
            Self::West | Self::NorthWest | Self::SouthWest  => -1,
            Self::East | Self::NorthEast | Self::SouthEast => 1,
            _ => 0,
        }
    }

    pub fn shift(&self, pos: (usize, usize)) -> (usize, usize) {
        let y = pos.0.wrapping_add_signed(self.dy().into());
        let x = pos.1.wrapping_add_signed(self.dx().into());
        (y, x)
    }

    pub fn shift_i32(&self, pos: (i32, i32)) -> (i32, i32) {
        let y = pos.0.wrapping_add(self.dy().into());
        let x = pos.1.wrapping_add(self.dx().into());
        (y, x)
    }

}