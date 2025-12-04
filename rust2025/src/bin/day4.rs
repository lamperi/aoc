use std::io;
use aoc::grid::Grid;

fn part1(input: &str) -> usize {
    let grid = Grid::new(input).unwrap();
    grid.find_all(b'@')
    .filter(|pos| {
        grid.neighbors8(pos)
        .iter().filter(|n| grid.get_pos(n) == b'@')
        .count() < 4
    })
    .count()
}

fn part2(input: &str) -> usize {
    let mut grid = Grid::new(input).unwrap();
    let mut all_accessible = 0;
    loop {
        let accessible = grid.find_all(b'@')
        .filter(|pos| {
            grid.neighbors8(pos)
            .iter().filter(|n| grid.get_pos(n) == b'@')
            .count() < 4
        })
        .collect::<Vec<_>>();
        if accessible.is_empty() {
            break
        }
        accessible.iter().for_each(|a| {
            grid.update(a, b'.');
        });
        all_accessible += accessible.len();
    }
    all_accessible
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

    const TEST_INPUT: &str = r#"..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 13)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 43)
    }
}