use std::fs;
use std::io;
use std::result::Result;

fn parse_numbers(line: &str) -> Vec<i32> {
    line.split_ascii_whitespace()
        .map(|s| s.parse::<i32>())
        .collect::<Result<Vec<_>, _>>().unwrap()
}

fn predict(numbers: Vec<i32>) -> i32 {
    let mut levels = vec![numbers];
    while levels.last().unwrap().len() > 1 {
        let level = levels.last().unwrap()
            .windows(2)
            .map(|s| s[1] - s[0])
            .collect::<Vec<_>>();
        levels.push(level);
    }
    levels.reverse();
    levels.iter().fold(Default::default(), |acc, level| {
        acc + *level.last().unwrap()
    })
}

fn part1(input: &String) -> i32 {
    input.lines()
        .map(parse_numbers)
        .map(predict)
        .sum()
}

fn part2(input: &String) -> i32 {
    input.lines()
        .map(parse_numbers)
        .map(|mut v| { v.reverse(); v })
        .map(predict)
        .sum()
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/9/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 114)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 2)
    }
}