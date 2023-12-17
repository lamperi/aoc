use std::io;
use aoc;

fn part1(input: &String) -> u32 {
    0
}

fn part2(input: &String) -> u32 {
    0
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

    const TEST_INPUT: &str = r#""#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 0)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 0)
    }
}