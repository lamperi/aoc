use std::io;
use std::collections::HashMap;
use aoc::{self, EightDirection};

fn to_map(input: &String) -> HashMap<(usize, usize), char> {
    input.split("\n")
        .enumerate()
        .flat_map(|(y, line)| {
            line.chars().enumerate()
                .map(move |(x, c) | {
                    ((y, x), c)
                })
        })
        .collect()
}

fn part1(input: &String) -> usize {
    let area = to_map(input);
    area.iter()
        .filter(|(_, &c)| { c == 'X'})
        .map(|(&coord, _)| {
            EightDirection::eight_directions().iter()
                .filter(|dir| {
                    "MAS".chars().scan(coord, |pos, c| {
                        let next_pos = dir.shift(*pos);
                        *pos = next_pos;
                        Some((next_pos, c))
                    }).all(|(pos, c)| {
                        match area.get(&pos) {
                            Some(&a) => a == c,
                            None => false,
                        }
                    })
                }).count()
        }).sum()
}

fn part2(input: &String) -> usize {
    let area = to_map(input);
    area.iter()
        .filter(|(_, &c)| { c == 'A'})
        .filter(|(&coord, _)| {
            let a1 = [EightDirection::NorthWest, EightDirection::SouthEast];
            let a2 = [EightDirection::NorthEast, EightDirection::SouthWest];
            [a1, a2].iter()
                .all(|dirs| {
                    let c1 = dirs[0].shift(coord);
                    let c2 = dirs[1].shift(coord);
                    match (area.get(&c1), area.get(&c2)) {
                        (Some('M'), Some('S')) | (Some('S'), Some('M')) => true,
                        _ => false
                    }
                })
        })
        .count()
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

    const TEST_INPUT: &str = r#"MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 18)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 9)
    }
}