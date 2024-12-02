use std::io;
use aoc;

fn parse(input: &String) -> Vec<Vec<i32>> {
    input.lines()
    .map(|line| {
        line.split_ascii_whitespace()
            .map(|s| { s.parse::<i32>().unwrap() })
            .collect()
    }).collect()
}

fn is_safe_increasing(report: &Vec<i32>) -> bool {
    report.windows(2).all(|pair| {
        let d = pair[1] - pair[0];
        1 <= d && d <= 3
    })
} 

fn is_safe_report(report: &Vec<i32>) -> bool {
    if is_safe_increasing(report) {
        true
    } else {
        let reversed = report.iter().copied().rev().collect();
        is_safe_increasing(&reversed)
    } 
}

fn part1(input: &String) -> usize {
    let reports = parse(input);
    reports.iter().filter(|&report| { is_safe_report(report) }).count()
}

fn part2(input: &String) -> usize {
    let reports = parse(input);
    reports.iter().filter(|&report| -> bool {
        if is_safe_report(&report) {
            return true
        }
        for index in 1..report.len() {
            let mut clone = report.clone();
            clone.remove(index);
            if is_safe_report(&clone) {
                return true
            }
        }
        false
    }).count()
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

    const TEST_INPUT: &str = r#"7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 2)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 4)
    }
}