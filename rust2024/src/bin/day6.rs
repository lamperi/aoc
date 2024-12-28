use std::{collections::{BTreeSet, HashSet}, io};
use aoc::{direction::CardinalDirection, grid::Grid, pos::Pos2D};

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
                    assert!(*get_coord(topology, next_pos).unwrap() == '.');
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

fn has_cycle(start: &Pos2D<usize>, rows: &Vec<BTreeSet<usize>>, columns: &Vec<BTreeSet<usize>>, height: usize, width: usize) -> bool {
    let mut state = Some((*start, CardinalDirection::North));
    let mut seen : HashSet<(Pos2D<usize>, CardinalDirection)> = HashSet::new();
    seen.insert(state.unwrap());
    while let Some((pos, dir)) = state {
        match dir {
            CardinalDirection::North => {
                let mut rng  = columns[pos.x].range(0..pos.y);
                if let Some(block_y) = rng.next_back() {
                    let next_pos = Pos2D{y: block_y + 1, x: pos.x};
                    state = Some((next_pos, dir.turn_right()));
                } else {
                    state = None;

                }
            }
            CardinalDirection::South => {
                let mut rng = columns[pos.x].range(pos.y+1..height);
                if let Some(block_y) = rng.next() {
                    let next_pos = Pos2D{y: block_y - 1, x: pos.x};
                    state = Some((next_pos, dir.turn_right()));
                } else {
                    state = None;
                }
            }
            CardinalDirection::West => {
                let mut rng = rows[pos.y].range(0..pos.x);
                if let Some(block_x) = rng.next_back() {
                    let next_pos = Pos2D{y: pos.y, x: block_x + 1};
                    state = Some((next_pos, dir.turn_right()));

                } else {
                    state = None;
                }
            }
            CardinalDirection::East => {
                let mut rng = rows[pos.y].range(pos.x..width);
                if let Some(block_x) = rng.next() {
                    let next_pos = Pos2D{y: pos.y, x: block_x - 1};
                    state = Some((next_pos, dir.turn_right()));
                } else {
                    state = None;
                }
            }
        }
        if state.is_some() {
            if !seen.insert(state.unwrap()) {
                return true
            }
        }
    }
    false
}

fn part2(input: &str) -> usize {
    let grid = Grid::new(input).unwrap();
    let start_pos = grid.find(b'^').unwrap();

    let mut rows: Vec<BTreeSet<usize>> = vec![BTreeSet::new(); grid.height];
    let mut columns: Vec<BTreeSet<usize>> = vec![BTreeSet::new(); grid.width];
    grid.find_all(b'#').for_each(|pos| {
        rows[pos.y].insert(pos.x);
        columns[pos.x].insert(pos.y);
    });

    let (topology, start) = parse(input);
    let visited = get_path(&topology, start);
    let mut loop_possibilities = 0;
    for v in visited {
        if v == start {
            continue
        }
        rows[v.0].insert(v.1);
        columns[v.1].insert(v.0);

        if has_cycle(&start_pos, &rows, &columns, grid.height, grid.width) {
            loop_possibilities += 1;
        }

        rows[v.0].remove(&v.1);
        columns[v.1].remove(&v.0);
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