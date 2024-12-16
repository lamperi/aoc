use std::{collections::{BinaryHeap, HashMap, HashSet}, io};
use std::cmp::Reverse;
use aoc::CardinalDirection;

type Pos2D = (usize, usize);
type State = (Pos2D, CardinalDirection);

fn parse(input: &str) -> (Pos2D, Pos2D, HashSet<Pos2D>) {
    let mut start: Option<Pos2D> = None;
    let mut end: Option<Pos2D> = None;
    let mut walls = HashSet::new();
    for (y, line) in input.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == 'S' {
                start = Some((y,x));
            } else if c == 'E' {
                end = Some((y,x));
            } else if c == '#' {
                walls.insert((y,x));
            }
        }
    }
    (start.expect("start not found"),
    end.expect("end not found"),
    walls)
}

fn part1(input: &str) -> u32 {
    let (start, end, walls) = parse(input);
    // Heap: contains (Reverse(points), state)
    // where state is (position, direction).
    // Reverse is used because BinaryHeap is a max-heap.
    let mut heap = BinaryHeap::new();
    heap.push((Reverse(0), (start, CardinalDirection::East)));
    // Prune states already visited.
    let mut visited_states = HashSet::new();
    visited_states.insert((start, CardinalDirection::East));
    while let Some((Reverse(points), (pos, dir))) = heap.pop() {
        let next_pos = dir.shift(pos);
        if next_pos == end {
            return points + 1
        }
        for (next_points, state) in [
                (points+1, (next_pos, dir)),
                (points+1000, (pos, dir.turn_left())),
                (points+1000, (pos, dir.turn_right()))] {
            if !walls.contains(&state.0) && visited_states.insert(state) {
                heap.push((Reverse(next_points), state));
            }
        }
    }
    0
}

fn part2(input: &str) -> usize {
    let (start, end, walls) = parse(input);
    // Heap: contains (Reverse(points), state)
    // where state is (position, direction).
    // Reverse is used because BinaryHeap is a max-heap.
    let init_state = (start, CardinalDirection::East);
    let mut heap = BinaryHeap::new();
    heap.push((Reverse(0), (init_state)));
    // Prune states already visited. Allow to revisit a state which was previously visited with the same or higher score.
    let mut visited_states = HashSet::new();
    visited_states.insert(init_state);
    // Contains all cells in the best paths to a state.
    let mut best_path: HashMap<State,(i32, HashSet<Pos2D>)> = HashMap::new();
    best_path.insert(init_state, (0, HashSet::from([start])));

    while let Some((Reverse(points), (pos, dir))) = heap.pop() {
        let next_pos = dir.shift(pos);
        for (points, state) in [
                (points+1, (next_pos, dir)),
                (points+1000, (pos, dir.turn_left())),
                (points+1000, (pos, dir.turn_right()))] {
            let (_, prev_path) = &best_path[&(pos, dir)];
            let mut prev_path = prev_path.clone();
            if let Some((exist_points, exist_path)) = best_path.get_mut(&state) {
                if points == *exist_points {
                    exist_path.extend(prev_path);
                }
            } else {
                prev_path.insert(state.0);
                best_path.insert(state, (points, prev_path));
            }
            if next_pos == end {
                continue;
            }
            if !walls.contains(&state.0) && visited_states.insert(state) {
                heap.push((Reverse(points), state));
            }
        }
    }
    let mut tiles_in_best_path = HashSet::new();
    let mut best_path_len = None;
    for ((pos, _), (points, path)) in best_path {
        if pos != end {
            continue
        }
        if best_path_len.map_or(true, |v| v > points) {
            best_path_len = Some(points);
            tiles_in_best_path.clear();
            tiles_in_best_path.extend(path);
        } else if best_path_len.unwrap() == points {
            tiles_in_best_path.extend(path);
        }
    }
    tiles_in_best_path.len()
}

fn main() -> io::Result<()> {
    let input: String = aoc::get_input()?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 7036)
    }

    #[test]
    fn test_part1_large() {
        let result = part1(LARGE_TEST_INPUT);
        assert_eq!(result, 11048)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 45)
    }

    #[test]
    fn test_part2_large() {
        let result = part2(LARGE_TEST_INPUT);
        assert_eq!(result, 64)
    }

    const TEST_INPUT: &str = r#"###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"#;

const LARGE_TEST_INPUT: &str = r#"#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"#;

}