use std::{io, collections::HashMap};
use aoc;
use std::collections::hash_map::Entry;

#[derive(Copy,Clone,Eq,PartialEq)]
enum Block {
    Rock,
    Wall,
    Empty,
}

enum CardinalDirection {
    North,
    South,
    West,
    East,
}
impl CardinalDirection {
    fn dy(&self) -> i8 {
        match self {
            CardinalDirection::North => -1,
            CardinalDirection::South => 1,
            _ => 0,
        }
    }
    fn dx(&self) -> i8 {
        match self {
            CardinalDirection::West => -1,
            CardinalDirection::East => 1,
            _ => 0,
        }
    }
}

fn parse_block(c: char) -> Block {
    match c {
        'O' => Block::Rock,
        '#' => Block::Wall,
        _ => Block::Empty
    }
}

fn parse_input(input: &String) -> Vec<Vec<Block>>{
    input.lines()
        .map(|line| line.chars().map(parse_block).collect::<Vec<_>>())
        .collect::<Vec<_>>()
}

fn tilt(platform: &mut Vec<Vec<Block>>, dir: CardinalDirection) {
    let h = platform.len();
    let w = platform[0].len();

    let y_range: Box<dyn Iterator<Item = usize>> = match dir {
        CardinalDirection::South => Box::new((0..h).rev()),
        _ => Box::new(0..h),
    };
    for y in y_range {
        let x_range: Box<dyn Iterator<Item = usize>> = match dir {
            CardinalDirection::East => Box::new((0..w).rev()),
            _ => Box::new(0..w),
        };
        for x in x_range {
            if platform[y][x] == Block::Rock {
                let mut yy = y as i8;
                let mut xx = x as i8;
                yy += dir.dy();
                xx += dir.dx();
                while 0 <= yy && yy < h as i8 && 0 <= xx && xx < w as i8 && platform[yy as usize][xx as usize] == Block::Empty {
                    yy += dir.dy();
                    xx += dir.dx();
                }
                yy -= dir.dy();
                xx -= dir.dx();
                if yy != y as i8 || xx != x as i8 {
                    platform[y][x] = Block::Empty;
                    platform[yy as usize][xx as usize] = Block::Rock;
                }
            }
        }
    }
}

fn load(platform: &Vec<Vec<Block>>) -> usize {
    platform.iter().enumerate().flat_map(|(y, row)| {
        row.iter().filter_map(move |b| match b {
            Block::Rock => Some(y),
            _ => None
        })
    })
    .map(|y| platform.len() - y)
    .sum()
}

fn encode(platform: &Vec<Vec<Block>>) -> String {
    platform.iter().enumerate().flat_map(|(y, row)| {
        row.iter().enumerate().filter_map(move |(x, b)| match b {
            Block::Rock => Some((y,x)),
            _ => None
        })
        .map(|(y,x)| format!("{y},{x},"))
    }).collect::<String>()
}

fn part1(input: &String) -> usize {
    let mut platform = parse_input(input);
    tilt(&mut platform, CardinalDirection::North);
    load(&platform)
}

fn part2(input: &String) -> usize {
    let mut platform = parse_input(input);
    let goal = 1_000_000_000;
    let mut seen: HashMap<_, usize> = HashMap::new();
    let mut loads: Vec<usize> = Vec::new();
    loads.push(load(&platform));

    for i in 0..goal {
        let state = encode(&platform);
        let entry = seen.entry(state);
        if let Entry::Occupied(occ_entry) = &entry {
            let last_seen = occ_entry.get();
            let cycle = i - last_seen;
            let index = (goal - last_seen) % cycle + last_seen;
            return loads[index];
        }
        entry.or_insert(i);

        tilt(&mut platform, CardinalDirection::North);
        tilt(&mut platform, CardinalDirection::West);
        tilt(&mut platform, CardinalDirection::South);
        tilt(&mut platform, CardinalDirection::East);
        loads.push(load(&platform));
    }
    0 // TODO: can this happen?
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

    const TEST_INPUT: &str = r#"O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 136)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 64)
    }
}