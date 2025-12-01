use std::{collections::{HashSet, VecDeque}, io};
use aoc::direction::Direction;

fn parse(input: &str) -> (Vec<Vec<u8>>, Vec<(usize, usize)>) {
    let mut starts = Vec::new();
    let topology = input.lines().enumerate().map(|(y,line)| {
        line.chars().enumerate()
            .inspect(|(x, c)| {
                if *c == '0' {
                    starts.push((y, *x));
                }
            })
            .map(|(_, c)| c.to_digit(10)
                .expect("char must be [0-9]") as u8)
            .collect()
    }).collect();
    (topology, starts)
}

fn topology_search(input: &str) -> (usize, u32) {
    let (topology, starts) = parse(input);
    starts.iter()
        .map(move |start| {
            let mut peaks = HashSet::new();
            let mut paths = 0;
            let mut deq = VecDeque::from([(*start, 0)]);
            while let Some((pos, height)) = deq.pop_front() {
                for dir in Direction::cardinal_directions() {
                    let new_pos = dir.shift(pos);
                    let neighbor_height = topology.get(new_pos.0).and_then(|line| line.get(new_pos.1)).copied();
                    if let Some(neighbor_height) = neighbor_height {
                        if height + 1 == neighbor_height {
                            if neighbor_height == 9 {
                                peaks.insert(new_pos);
                                paths += 1;
                            } else {
                                deq.push_back((new_pos, neighbor_height));
                            }
                        }
                    }
                }
            }
            (peaks.len(), paths)
        }).fold((0, 0), |(peaks, paths), (item_peaks, item_paths)|
            (peaks + item_peaks, paths + item_paths)
        )
}

fn part1(input: &str) -> usize {
    topology_search(input).0
}

fn part2(input: &str) -> u32 {
    topology_search(input).1
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

    const TEST_INPUT: &str = r#"89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 36)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 81)
    }
}