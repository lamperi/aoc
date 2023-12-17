use std::{io, collections::HashSet};
use aoc::{self, CardinalDirection};
use std::collections::BinaryHeap;
use std::cmp::Reverse;

fn parse_input(input: &String) -> Vec<Vec<usize>>{
    input.lines()
        .map(|line| {
            line.chars()
                .map(|c| c.to_digit(10).unwrap() as usize)
                .collect::<Vec<_>>()
        })
        .filter(|v| !v.is_empty())
        .collect::<Vec<_>>()
}

fn solve(input: &String, min_straight: u8, max_straight: u8) -> usize {
    let area = parse_input(input);
    let (h, w) = (area.len(), area[0].len());
    let goal = (area.len()-1, area[0].len()-1);
    let mut states = BinaryHeap::from([
        Reverse((0, (0, 0), CardinalDirection::East, 0)),
        Reverse((0, (0, 0), CardinalDirection::South, 0)),
    ]);
    let mut visited = HashSet::new();
    while !states.is_empty() {
        let (heat, pos, dir, straight) = states.pop().unwrap().0;
        if !visited.insert((pos, dir, straight)) {
            continue
        }
        if pos == goal && min_straight <= straight && straight <= max_straight {
            return heat
        }
        if straight < max_straight {
            let pos = dir.shift(pos);
            if pos.0 < h && pos.1 < w {
                let heat = heat + area[pos.0][pos.1];
                states.push(Reverse((heat, pos, dir, straight + 1)));
            }
        }
        if straight >= min_straight {
            for dir in if dir.is_horizontal() {
                [CardinalDirection::North, CardinalDirection::South]
            } else {
                [CardinalDirection::West, CardinalDirection::East]
            } {
                let pos = dir.shift(pos);
                if pos.0 < h && pos.1 < w {
                    let heat = heat + area[pos.0][pos.1];
                    states.push(Reverse((heat, pos, dir, 1)));
                }
            }
        }
    }
    0
}

fn part1(input: &String) -> usize {
    solve(input, 0, 3)
}

fn part2(input: &String) -> usize {
    solve(input, 4, 10)
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

    const TEST_INPUT: &str = r#"2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 102)
    }

    #[test]
    fn test_part21() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 94)
    }

    #[test]
    fn test_part22() {
        let test = String::from(r#"111111111111
999999999991
999999999991
999999999991
999999999991
"#);
        let result = part2(&test);
        assert_eq!(result, 71)
    }
}