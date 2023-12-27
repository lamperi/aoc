use std::{io, collections::HashSet};
use aoc::{self, CardinalDirection};

fn parse_input<'a>(input: &'a str) -> (Vec<Vec<char>>, usize, usize, (usize, usize)) {
    let mut start = None;
    let area = input.lines()
        .enumerate()
        .map(|(y, line)| -> Vec<_> {
            line.char_indices()
            .map(|(x, c)| {
                if c == 'S' {
                    start = Some((y,x));
                }
                c
            }).collect::<Vec<_>>()
        }).collect::<Vec<_>>();
    let height = area.len();
    let width = area.first().unwrap().len();
    (area, height, width, start.unwrap())
}

fn naive_solve(input: &str, steps: u32) -> u32 {
    let (area, _height, _width, start) = parse_input(input);
    let get_tile = |y: usize, x: usize| -> char {
        match area.get(y) {
            Some(v) => {
                match v.get(x) {
                    Some(c) => *c,
                    None => '#',
                }
            },
            None => '#',
        }
    };
    let init = {
        let mut init = HashSet::new();
        init.insert(start);
        init
    };
    let parity = steps % 2;
    let reachable = 0;
    let mut visited = HashSet::new();
    (1..=steps).fold((init, reachable), |(prev, mut reachable), step| {
        (prev.iter().flat_map(|loc| {
            let v = CardinalDirection::all()
                .iter()
                .map(|cardinal| cardinal.shift(*loc))
                .filter(|adj| visited.insert(*adj))
                .filter(|adj| {
                    let tile = get_tile(adj.0, adj.1);
                    tile == 'S' || tile == '.'
                } )
                .collect::<Vec<_>>();
            if step % 2 == parity {
                reachable += v.len() as i64;
            }
            v
        }).collect::<HashSet<_>>(), reachable)
    }).1 as u32
}

fn part1(input: &String) -> u32 {
    naive_solve(input.as_str(), 64)
}

fn improved_solve(input: &str, steps: u32) -> u64 {
    let (area, height, width, start) = parse_input(input);
    let get_tile = |y: usize, x: usize| -> char {
        match area.get(y) {
            Some(v) => {
                match v.get(x) {
                    Some(c) => *c,
                    None => '#',
                }
            },
            None => '#',
        }
    };
    assert_eq!(height, width);
    let start = (start.0 as i32, start.1 as i32);
    let mut locations = HashSet::new();
    locations.insert(start);
    
    // Linear solving.
    let parity = steps % 2;
    let mut reachable = 0;
    let mut alt_reachable = 0;
    let mut visited = HashSet::new();

    // Cycle detection: 
    // Theory is that the growth of the reachable states grows 
    // with constant increments.
    let cycle_offset = steps % height as u32;
    let mut a = None;
    let mut b = None;
    let mut c = None;

    for step in 1..=steps {
        locations = locations.into_iter().flat_map(|loc| {
            let v = CardinalDirection::all()
                .iter()
                .map(|cardinal| cardinal.shift_i32(loc))
                .filter(|adj| visited.insert(*adj))
                .filter(|adj| {
                    let y = adj.0.rem_euclid(height as i32);
                    let x = adj.1.rem_euclid(width as i32);
                    let tile = get_tile(y as usize, x as usize);
                    tile == 'S' || tile == '.'
                } )
                .collect::<Vec<_>>();
            if step % 2 == parity {
                reachable += v.len() as i64;
            } else {
                alt_reachable += v.len() as i64;
            }
            v
        }).collect::<HashSet<_>>();

        if (step.wrapping_sub(cycle_offset)) % height as u32 == 0 {
            let prev_len = if step % 2 == parity { reachable } else { alt_reachable };
            let prev_c = c;
            let prev_b = b;
            let prev_a = a;
            a = Some(prev_len);
            b = prev_a.map(|prev_a| a.unwrap() - prev_a);
            c = prev_b.map(|prev_b| b.unwrap() - prev_b);
            let d = prev_c.map(|prev_c| c.unwrap() - prev_c);
            if d.is_some_and(|d| d == 0) {
                let steps_left: i64 = (steps - step) as i64;
                let cycles_left = steps_left / height as i64;
                let res = a.unwrap()
                    + cycles_left * (
                        2 * b.unwrap()
                        + (cycles_left + 1) * c.unwrap()
                    ) / 2;
                return res as u64;
            }
        }
    }
    reachable as u64
}

fn part2(input: &String) -> u64 {
    improved_solve(input.as_str(), 26501365)
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

    const TEST_INPUT: &str = r#"...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = naive_solve(&test, 6);
        assert_eq!(result, 16)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = improved_solve(&test, 6);
        assert_eq!(result, 16);

        let result = improved_solve(&test, 50);
        assert_eq!(result, 1594);

        let result = improved_solve(&test, 100);
        assert_eq!(result, 6536);

        let result = improved_solve(&test, 110);
        assert_eq!(result, 7934);

        let result = improved_solve(&test, 111);
        assert_eq!(result, 8078);

        let result = improved_solve(&test, 112);
        assert_eq!(result, 8242);
    }

    #[test]
     fn test_part2_larger_steps() {
        let test = String::from(TEST_INPUT);
        let result = improved_solve(&test, 500);
        assert_eq!(result, 167004);

        let result = improved_solve(&test, 1000);
        assert_eq!(result, 668697);

        let result = improved_solve(&test, 5000);
        assert_eq!(result, 16733044);
    }
}