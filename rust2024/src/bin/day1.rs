use std::io;

fn parse(input: &str) -> (Vec<i32>, Vec<i32>) {
    input.lines().map(|line| {
        let mut i = line.split_ascii_whitespace();
        let left = i.next().unwrap().parse::<i32>().unwrap();
        let right = i.next().unwrap().parse::<i32>().unwrap();
        (left, right)
    }).unzip()
}

fn part1(input: &str) -> i32 {
    let (mut left, mut right) = parse(input);
    left.sort();
    right.sort();
    left.iter().zip(right.iter()).map(|(l, r)| {
        (l - r).abs()
    }).sum()
}

fn part2(input: &str) -> i32 {
    let (left, right) = parse(input);
    left.iter().map(|l| {
        l * right.iter().filter(|r| {*r == l}).count() as i32
    }).sum()
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

    const TEST_INPUT: &str = r#"3   4
4   3
2   5
1   3
3   9
3   3"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 11)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 31)
    }
}