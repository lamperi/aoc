use std::{collections::HashSet, io};

fn parse(input: &str) -> (HashSet<&str>, Vec<&str>, usize) {
    let (patterns, designs) = input.split_once("\n\n").unwrap();
    let patterns: HashSet<&str> = patterns.split(", ").collect();
    let designs = designs.lines().collect();
    let max_pattern = patterns.iter().map(|d| d.len()).max().unwrap();
    (patterns, designs, max_pattern)
}

fn dp(design: &str, patterns: &HashSet<&str>, max_pattern: usize) -> u64 {
    let mut dp = vec![0; design.len()+1];
    dp[0] += 1;
    for i in 1..=design.len() {
        let prefix = &design[..i];
        for pat_len in 1..=max_pattern {
            if pat_len <= i && patterns.contains(&prefix[i - pat_len..]) {
                dp[i] += dp[i - pat_len];
            }
        }
    }
    dp[design.len()]
}

fn common(input: &str) -> (u64, u64) {
    let (patterns, designs, max_pattern) = parse(input);
    designs.iter()
        .fold((0, 0), |(p1, p2), design| {
            let s = dp(design, &patterns, max_pattern);
            if s > 0 {
                (p1 + 1, p2 + s)
            } else {
                (p1, p2)
            }
        })
}

fn part1(input: &str) -> u64 {
    common(input).0
}

fn part2(input: &str) -> u64 {
    common(input).1
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

    const TEST_INPUT: &str = r#"r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 6)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 16)
    }
}