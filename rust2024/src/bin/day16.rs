use std::{cmp::Ordering, collections::{BinaryHeap, HashMap, HashSet}, io};
use std::cmp::Reverse;
use aoc::CardinalDirection;
use std::collections::hash_map::Entry;

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

fn edges(state: &State, walls: &HashSet<Pos2D>) -> Vec<(u32, State)> {
    let (pos, dir) = *state;
    [
        (1, (dir.shift(pos), dir)),
        (1000, (pos, dir.turn_left())),
        (1000, (pos, dir.turn_right()))
    ].into_iter()
    .filter(|(_, (pos, _))| !walls.contains(pos))
    .collect::<Vec<_>>()
}

fn part1(input: &str) -> u32 {
    let (start, end, walls) = parse(input);

    aoc::dijkstra((start, CardinalDirection::East),
    |state| state.0 == end,
    |state| edges(state, &walls)).unwrap()
}

fn part2(input: &str) -> usize {
    let (start, end, walls) = parse(input);
    aoc::dijkstra_equal_paths((start, CardinalDirection::East),
    |state| state.0 == end,
    |state| edges(state, &walls))
    .map(|(_cost, nodes)| {
        nodes.iter()
            .map(|state| state.0)
            .collect::<HashSet<_>>().len()
    })
    .unwrap()
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
    fn test_part1_hamatti() {
        let result = part1(HAMATTI_TEST_INPUT);
        assert_eq!(result, 4021)
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

    #[test]
    fn test_part2_hamatti() {
        let result = part2(HAMATTI_TEST_INPUT);
        assert_eq!(result, 22)
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

const HAMATTI_TEST_INPUT: &str = r"####################
####.##########.####
##..............####
##.#.##.#######.####
#..#.##.....#...#..#
##.#.######.#.#.#.##
##....#...........E#
##.####.#####.###.##
#.........###.#...##
##.####.#.###.#.####
#S.#################
####################";

}