use std::{collections::{HashMap, HashSet}, io};

type Pos = (usize, usize);

fn parse(input: &str) -> Option<(Pos, HashSet<Pos>, usize)> {
    let mut start = None;
    let mut splitters = HashSet::new();
    let mut height = 0;
    input.lines().enumerate()
    .for_each(|(y, line)| {
        line.chars().enumerate().for_each(|(x, c)| {
            match c {
                'S' => start = Some((y, x)),
                '^' => { splitters.insert((y, x)); }
                _ => {}
            };
        });
        height = y;
    });
    let start = start?;
    Some((start, splitters, height))
}


fn part1(input: &str) -> u64 {
    let (start, splitters, height) = parse(input).unwrap();
    let mut beams = HashSet::new();
    beams.insert(start);
    let mut splits = 0;
    (0..height).for_each(|_| {
        beams = beams.iter().flat_map(|beam|{
            let (y,x) = beam;
            let next_pos = (y+1, *x);
            if splitters.contains(&next_pos) {
                splits += 1;
                let left = (y+1, x-1);
                let right = (y+1, x+1);
                vec![left, right]
            } else {
                vec![next_pos]
            }
        }).collect::<HashSet<_>>();
    });
    splits
}

fn part2(input: &str) -> u64 {
    let (start, splitters, height) = parse(input).unwrap();
    let mut beams = HashMap::new();
    beams.insert(start, 1);
    let mut splits = 0;
    (0..height).for_each(|_| {
        let mut new_beams = HashMap::new();
        beams.iter().flat_map(|(beam, possibilities)|{
            let (y,x) = beam;
            let next_pos = (y+1, *x);
            if splitters.contains(&next_pos) {
                splits += 1;
                let left = (y+1, x-1);
                let right = (y+1, x+1);
                vec![(left, *possibilities), (right, *possibilities)]
            } else {
                vec![(next_pos, *possibilities)]
            }
        }).for_each(|(pos, count)| {
            *new_beams.entry(pos).or_default() += count;
        });
        beams = new_beams;
    });
    beams.values().sum()
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

    const TEST_INPUT: &str = r#".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 21)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 40)
    }
}