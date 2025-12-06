use std::{error::{self, Error}, fmt, io, iter};

#[derive(Debug,Clone)]
struct InvalidInput;
impl fmt::Display for InvalidInput {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "unable to parse AoC input")
    }
}
impl error::Error for InvalidInput {}

type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

fn parse(input: &str) -> Result<(Vec<std::ops::RangeInclusive<u64>>, Vec<u64>)> {
    let (ranges, ids) = input.split_once("\n\n").ok_or(InvalidInput)?;
    let ranges: std::result::Result<Vec<std::ops::RangeInclusive<u64>>, Box<dyn Error>> = ranges.lines().map(|line| {
        let (lo, hi) = line.split_once('-').ok_or(InvalidInput)?;
        let lo = lo.parse::<u64>()?;
        let hi = hi.parse::<u64>()?;
        Ok(std::ops::RangeInclusive::new(lo, hi))
    }).collect::<Result<Vec<_>>>();
    let ids = ids.lines()
    .map(|line| line.parse::<u64>().map_err(|e| e.into()))
    .collect::<Result<Vec<_>>>();
    Ok((ranges?, ids?))
}

fn part1(input: &str) -> Result<usize> {
    let (ranges, ids) = parse(input)?;
    Ok(ids.iter()
    .filter(|id| {
        ranges.iter().any(|r| r.contains(id))
    }).count())
}

fn part2(input: &str) -> Result<u64> {
    let (mut ranges, _) = parse(input)?;
    let mut j = 0;
    while j < ranges.len() {
        loop {
            let r = ranges[j].clone();
            let mut merged = false;
            for (k, r2) in ranges.iter().enumerate().skip(j+1) {
                if r.start() <= r2.start() && r.end() >= r2.start() || r2.start() <= r.start() && r2.end() >= r.start() {
                    let new_r = std::ops::RangeInclusive::new(
                        *r.start().min(r2.start()), *r.end().max(r2.end()));
                    ranges[j] = new_r;
                    ranges.remove(k);
                    merged = true;
                    break;
                }
            }
            if !merged {
                break
            }
        }
        j += 1;
    }
    Ok(ranges.iter().map(|r| r.end() - r.start() + 1).sum())
}

fn main() -> Result<()> {
    let input: String = aoc::get_input()?;
    let ans = part1(&input)?;
    println!("Part 1: {ans}");

    let ans = part2(&input)?;
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"3-5
10-14
16-20
12-18

1
5
8
11
17
32"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT).unwrap();
        assert_eq!(result, 3)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT).unwrap();
        assert_eq!(result, 14)
    }
}