use std::{io, collections::{HashSet, VecDeque}};
use aoc;
use aoc::CardinalDirection;

enum Block {
    Empty,
    VerticalSplitter,  // |
    HorizontalSpitter, // -
    ForwardMirror, // /
    BackwardMirror, // \
}

fn parse_block(c: char) -> Block {
    match c {
        '|' => Block::VerticalSplitter,
        '-' => Block::HorizontalSpitter,
        '/' => Block::ForwardMirror,
        '\\' => Block::BackwardMirror,
        _ => Block::Empty,
    }
}

fn parse_input(input: &String) -> Vec<Vec<Block>>{
    input.lines()
        .map(|line| line.chars().map(parse_block).collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

fn energize(area: &Vec<Vec<Block>>, pos: (usize, usize), dir: CardinalDirection) -> usize {
    let mut states = VecDeque::from([(pos, dir)]);
    let mut energized = HashSet::from([(pos, dir)]);
    while !states.is_empty() {
        let (pos, dir) = states.pop_front().unwrap();
        if pos.0 >= area.len() || pos.1 >= area[pos.0].len() {
            continue
        }
        let mut dirs = Vec::with_capacity(2);
        match area[pos.0][pos.1] {
            Block::BackwardMirror => {
                dirs.push(match dir {
                    CardinalDirection::East => CardinalDirection::South,
                    CardinalDirection::South => CardinalDirection::East,
                    CardinalDirection::North => CardinalDirection::West,
                    CardinalDirection::West => CardinalDirection::North,
                });
            },
            Block::ForwardMirror => {
                dirs.push(match dir {
                    CardinalDirection::West => CardinalDirection::South,
                    CardinalDirection::South => CardinalDirection::West,
                    CardinalDirection::North => CardinalDirection::East,
                    CardinalDirection::East => CardinalDirection::North,
                });
            },
            Block::VerticalSplitter if dir.is_horizontal() => {
                dirs.push(CardinalDirection::North);
                dirs.push(CardinalDirection::South);
            },
            Block::HorizontalSpitter if dir.is_vertical() => {
                dirs.push(CardinalDirection::West);
                dirs.push(CardinalDirection::East);
            },
            _ => {
                dirs.push(dir);
            },
        }
        for dir in dirs {
            let y = pos.0.wrapping_add_signed(dir.dy().into());
            let x = pos.1.wrapping_add_signed(dir.dx().into());
            if y < area.len() && x < area[y].len() {
                let state = ((y,x), dir);
                if energized.insert(state.clone()) {
                    states.push_back(state);
                }
            }
        }
    }
    energized.into_iter()
        .map(|(pos, _dir)| pos)
        .collect::<HashSet<(usize, usize)>>()
        .len()
}

fn part1(input: &String) -> usize {
    let area = parse_input(input);
    energize(&area, (0, 0), CardinalDirection::East)
}

fn part2(input: &String) -> usize {
    let area = parse_input(input);
    let mut all_starts = Vec::new();
    let h = area.len();
    let w = area[0].len();
    for x in 0..w {
        all_starts.push(((0, x), CardinalDirection::South));
        all_starts.push(((h-1, x), CardinalDirection::North));
    }
    for y in 1..(h-1) {
        all_starts.push(((y, 0), CardinalDirection::East));
        all_starts.push(((y, w-1), CardinalDirection::West));
    }
    all_starts.into_iter().map(|(pos, dir)| {
        energize(&area, pos, dir)
    }).max().unwrap()
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

    const TEST_INPUT: &str = r#".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 46)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 51)
    }
}