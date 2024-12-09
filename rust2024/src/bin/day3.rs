use std::io;
use regex::Regex;

fn part1(input: &str) -> u32 {
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
    re.captures_iter(input).map(|c| {
        let (_, [a, b]) = c.extract();
        a.parse::<u32>().unwrap() * b.parse::<u32>().unwrap()
    }).sum()
}

fn part2(input: &str) -> u32 {
    let re = Regex::new(r"(mul|do|don't)\((\d+)?,?(\d+)?\)").unwrap();
    re.captures_iter(input).map(|c| {
        let cmd = c.get(1).unwrap().as_str();
        let a = c.get(2).map(|s| s.as_str().parse::<u32>().unwrap());
        let b = c.get(3).map(|s| s.as_str().parse::<u32>().unwrap());
        (cmd, a, b)
    }).fold((true, 0), |(enabled, sum), parsed| {
        match parsed {
            ("mul", Some(a), Some(b)) if enabled => (enabled, sum + a * b),
            ("mul", _, _) => (enabled, sum),
            ("do", _, _) => (true, sum),
            ("don't", _, _) => (false, sum),
            _ => panic!("{:?}",parsed),
        }
    }).1
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

    const TEST_INPUT: &str = r#"xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"#;
    const TEST_INPUT2: &str = r#"xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 161)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT2);
        let result = part2(&test);
        assert_eq!(result, 48)
    }
}