use std::cmp::{Ordering, Reverse};
use std::collections::{BinaryHeap, HashSet};
use std::fmt::Debug;
use std::fs;
use std::hash::Hash;
use std::io;
use indexmap::map::Entry;
use indexmap::IndexMap;
use num::Zero;

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

pub fn dijkstra<State, Cost, F1, F2>(init_state: State, is_end: F1, edges: F2) -> Option<Cost>
where
    State: Hash + Ord + Copy,
    Cost: Ord + Copy + Zero,
    F1: Fn(&State) -> bool,
    F2: Fn(&State) -> Vec<(Cost, State)>
{
    let mut heap: BinaryHeap<(Reverse<Cost>, usize)> = BinaryHeap::new();
    // Heap: contains (Reverse(points), state).
    // Reverse is used because BinaryHeap is a max-heap.
    heap.push((Reverse(Zero::zero()), 0));

    // Prune states already visited.
    let mut visited_states: IndexMap<State, (Cost, usize)>  = IndexMap::new();
    visited_states.insert(init_state, (Zero::zero(), 0));

    while let Some((Reverse(cost), index)) = heap.pop() {
        let (node, _) = visited_states.get_index(index).unwrap();
        if is_end(node) {
            return Some(cost)
        }
        for (edge_cost, state) in edges(node) {
            let cost = cost + edge_cost;
            match visited_states.entry(state) {
                Entry::Vacant(v) => {
                    heap.push((Reverse(cost), v.index()));
                    v.insert((cost, index));
                },
                Entry::Occupied(mut o) => {
                    if cost < o.get().0 {
                        o.insert((cost, index));
                        heap.push((Reverse(cost), o.index()));
                    }
                }
            }
        }
    }
    None
}

pub fn dijkstra_equal_paths<State, Cost, F1, F2>(init_state: State, is_end: F1, edges: F2) -> Option<(Cost, Vec<State>)>
where
    State: Hash + Ord + Copy + Debug,
    Cost: Ord + Copy + Zero,
    F1: Fn(&State) -> bool,
    F2: Fn(&State) -> Vec<(Cost, State)>
{
    let mut heap: BinaryHeap<(Reverse<Cost>, usize)> = BinaryHeap::new();
    // Heap: contains (Reverse(points), state).
    // Reverse is used because BinaryHeap is a max-heap.
    heap.push((Reverse(Zero::zero()), 0));

    // Prune states already visited.
    let mut visited_states: IndexMap<State, (Cost, Vec<usize>)>  = IndexMap::new();
    visited_states.insert(init_state, (Zero::zero(), vec![]));
    let mut end_index = HashSet::new();
    let mut end_cost = None;

    while let Some((Reverse(cost), index)) = heap.pop() {
        let (node, _) = visited_states.get_index(index).unwrap();
        if end_cost.is_some_and(|end_cost| end_cost < cost) {
            continue
        }
        if is_end(node) {
            if end_cost.is_none() || end_cost.is_some_and(|end_cost| end_cost > cost) {
                end_index.clear();
                end_cost = Some(cost);
                end_index.insert(index);
            }
            end_index.insert(index);
            continue
        }
        for (edge_cost, state) in edges(node) {
            let cost = cost + edge_cost;
            match visited_states.entry(state) {
                Entry::Vacant(v) => {
                    heap.push((Reverse(cost), v.index()));
                    v.insert((cost, vec![index]));
                },
                Entry::Occupied(mut o) => {
                    match cost.cmp(&o.get().0) {
                        Ordering::Less => {
                            o.insert((cost, vec![index]));
                            heap.push((Reverse(cost), o.index()));
                        },
                        Ordering::Equal => {
                            o.get_mut().1.push(index);
                        },
                        Ordering::Greater => {}
                    }
                }
            }
        }
    }
    end_cost.map(|cost| {
        let mut visited_indices = HashSet::new();
        let mut stack = Vec::new();
        stack.extend(end_index.iter());
        visited_indices.extend(end_index);
        let mut visited_nodes = vec![];
        while let Some(index) = stack.pop() {
            let (node, (_, parents)) = visited_states.get_index(index).unwrap();
            visited_nodes.push(*node);
            for parent in parents {
                if visited_indices.insert(*parent) {
                    stack.push(*parent);
                }
            }
        }
        (cost, visited_nodes)
    })
}