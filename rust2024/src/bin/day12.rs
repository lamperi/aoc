use std::{collections::HashSet, io};

use aoc::EightDirection;

type Pos = (usize, usize);

fn parse(input: &str) -> Vec<Vec<char>> {
    let topology: Vec<Vec<_>> = input.lines().enumerate().map(|(_,line)| {
        line.chars().enumerate()
            .map(|(_, c)| c)
            .collect()
    }).collect();
    topology
}

fn dfs(topology: &[Vec<char>], pos: Pos, plot: char, visited_plots: &mut HashSet<Pos>) -> (u32, HashSet<(Pos, EightDirection)>) {
    visited_plots.insert(pos);
    let mut stack = vec![pos];
    let mut area = 0;
    let mut perimeter = HashSet::new();
    while let Some(pos) = stack.pop() {
        area += 1;
        for dir in EightDirection::cardinal_directions() {
            let neighbor_pos = dir.shift(pos);
            if let Some(neighbor_plot) = topology.get(neighbor_pos.0).and_then(|line| line.get(neighbor_pos.1)) {
                if *neighbor_plot == plot {
                    if visited_plots.insert(neighbor_pos) {
                        stack.push(neighbor_pos);
                    }
                } else {
                    perimeter.insert((pos, dir));
                }
            } else {
                perimeter.insert((pos, dir));
            }
        }
    }
    (area, perimeter)
}

fn count_sides(perimeter: &mut HashSet<(Pos, EightDirection)>) -> u32 {
    let mut sides = 0;
    while let Some(edge) = perimeter.iter().next().cloned() {
        sides += 1;
        perimeter.remove(&edge);
        let (pos, dir) = &edge;
        let dirs = if dir.is_horizontal() {
            [EightDirection::North, EightDirection::South]
        } else {
            [EightDirection::West, EightDirection::East]
        };
        
        for edge_dir in dirs {
            let mut v = Vec::new();
            let mut next_pos = edge_dir.shift(*pos);
            while perimeter.remove(&(next_pos, *dir)) {
                v.push(next_pos);
                next_pos = edge_dir.shift(next_pos);
            }
            //println!("processed a side to {:?} starting from {:?} containing {:?}", dir, edge, v);
        }
    }
    sides
}

fn part1(input: &str) -> u32 {
    let topology = parse(input);
    let mut visited_plots: HashSet<Pos> = HashSet::new();
    let mut total_price = 0;
    for (y, line) in topology.iter().enumerate() {
        for (x, plot) in line.iter().enumerate() {
            let pos = (y, x);
            if visited_plots.contains(&pos) {
                continue
            }
            let (area, perimeter) = dfs(&topology, pos, *plot, &mut visited_plots);
            let perimeter = perimeter.len() as u32;
            //println!("plot {} area {} perimeter {}, price {}", plot, area, perimeter.len(), area*perimeter.len() as u32);
            total_price += area*perimeter;
        }
    }
    total_price
}

fn part2(input: &str) -> u32 {
    let topology = parse(input);
    let mut visited_plots: HashSet<Pos> = HashSet::new();
    let mut total_price = 0;
    for (y, line) in topology.iter().enumerate() {
        for (x, plot) in line.iter().enumerate() {
            let pos = (y, x);
            if visited_plots.contains(&pos) {
                continue
            }
            let (area, mut perimeter) = dfs(&topology, pos, *plot, &mut visited_plots);
            let sides = count_sides(&mut perimeter);
            //println!("plot {} area {} sides {}, price {}", plot, area, sides, area*sides);
            total_price += area*sides;
        }
    }
    total_price
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

    const TEST_INPUT: &str = r#"RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 1930)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 1206)
    }
}