use std::{collections::HashSet, io};
use aoc::direction::CardinalDirection;

fn parse(input: &str) -> (Vec<Vec<char>>, (usize, usize)) {
    let mut start= (0, 0);
    let topology: Vec<Vec<_>> = input.lines().enumerate().map(|(y,line)| {
        line.chars().enumerate()
            .inspect(|(x, c)| {
                if *c == '^' {
                    start = (y,*x);
                }
            }) 
            .map(|(_, c)| if c == '^' { '.' } else { c })
            .collect()
    }).collect();
    (topology, start)
}

fn get_coord(topology: &[Vec<char>], pos: (usize, usize)) -> Option<&char> {
    topology.get(pos.0).and_then(|v| v.get(pos.1))
}

fn get_path(topology: &[Vec<char>], start: (usize, usize)) -> HashSet<(usize, usize)> {
    let mut pos = start;
    let mut dir = CardinalDirection::North;
    let mut visited = HashSet::new();
    loop {
        visited.insert(pos);
        let mut next_pos = dir.shift(pos);
        match get_coord(topology, next_pos) {
            Some(c) => {
                if *c == '#' {
                    dir = dir.turn_right();
                    next_pos = dir.shift(pos);
                    assert!(*get_coord(topology, next_pos).unwrap() == '.')
                }
                pos = next_pos;
            },
            None => {
                break
            }
        }
    }
    visited
}

fn part1(input: &str) -> u32 {
    let (topology, start) = parse(input);
    get_path(&topology, start).len() as u32
}

fn is_cycle_path(topology: &[Vec<char>], start: (usize, usize)) -> bool {
    let mut pos = start;
    let mut dir = CardinalDirection::North;
    let mut visited = HashSet::new();
    loop {
        if !visited.insert((pos, dir)) {
            return true
        }
        let mut next_pos = dir.shift(pos);
        match get_coord(topology, next_pos) {
            Some(c) => {
                if *c == '#' {
                    dir = dir.turn_right();
                    next_pos = dir.shift(pos);
                    match get_coord(topology, next_pos) {
                        Some(c) => {
                            if *c == '#' {
                                dir = dir.turn_right();
                                next_pos = dir.shift(pos);
                                assert!(*get_coord(topology, next_pos).unwrap() == '.')
                            }
                        },
                        None => {
                            return false
                        },
                    }
                }
                pos = next_pos;
            },
            None => {
                return false
            }
        }
    }
}


fn part2(input: &str) -> u32 {
    let (mut topology, start) = parse(input);
    let visited = get_path(&topology, start);
    let mut loop_possibilities = 0;
    for v in visited {
        if v == start {
            continue
        }
        topology[v.0][v.1] = '#';

        if is_cycle_path(&topology, start) {
            loop_possibilities += 1;
        }

        topology[v.0][v.1] = '.';
    }
    loop_possibilities
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

    const TEST_INPUT: &str = r#"....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 41)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 6)
    }
}