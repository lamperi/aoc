use std::{collections::{HashSet, VecDeque}, io};

use aoc::direction::CardinalDirection;

type Num = i32;
type Pos = (Num, Num);

fn parse(input: &str) -> Vec<Pos> {
    input.lines().map(|line| {
        let (x, y) = line.split_once(',').unwrap();
        (
            x.parse::<Num>().unwrap(),
            y.parse::<Num>().unwrap()
        )
    }).collect::<Vec<_>>()
}

fn bfs<F>(start: Pos, end: Pos, edges: F) -> Option<i32>
where
    F: Fn(&Pos) -> Vec<Pos> {
    let mut queue = VecDeque::new();
    queue.push_back((0, start));
    let mut visited = HashSet::new();
    visited.insert(start);
    while let Some((steps, pos)) = queue.pop_front() {
        if pos == end {
            return Some(steps)
        }
        for next_pos in edges(&pos) {
            if visited.insert(next_pos) {
                queue.push_back((steps+1, next_pos));
            }
        }
    }
    None
}

fn edges(pos: &Pos, corrupted: &HashSet<&Pos>, max_yx: i32) -> Vec<Pos> {
    CardinalDirection::all().iter().filter_map(|dir| {
        let next_pos = dir.shift_i32(*pos);
        if !corrupted.contains(&next_pos)
                && (0..=max_yx).contains(&next_pos.0)
                && (0..=max_yx).contains(&next_pos.1) {
            Some(next_pos)
        } else {
            None
        }
    }).collect::<Vec<Pos>>()
}

fn part1(input: &str) -> i32 {
    let coords = parse(input);
    let (max_yx, first_n) = if coords.len() < 30 {
        (6, 12)
    } else {
        (70, 1024)
    };
    let start = (0, 0);
    let end = (max_yx, max_yx);

    let corrupted = coords.iter().take(first_n).collect::<HashSet<_>>();

    bfs(start, end, move |pos| edges(pos, &corrupted, max_yx)).unwrap()
}

fn part2(input: &str) -> String {
    let coords = parse(input);
    let (max_yx, first_n) = if coords.len() < 30 {
        (6, 12)
    } else {
        (70, 1024)
    };
    let start = (0, 0);
    let end = (max_yx, max_yx);

    let mut lo = first_n;
    let mut hi = coords.len();
    while lo + 1 < hi {
        let mid = (lo + hi) / 2;
        let corrupted = coords.iter().take(mid).collect::<HashSet<_>>();
        if bfs(start, end, move |pos| edges(pos, &corrupted, max_yx)).is_none() {
            hi = mid;
        } else {
            lo = mid;
        }
    }
    let (x,y) = coords[lo];
    format!("{},{}", x, y)
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

    const TEST_INPUT: &str = r#"5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 22)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, "6,1")
    }
}