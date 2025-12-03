use std::{cmp::Reverse, io};

fn pipeline(input: &str, n_digits: usize) -> u64 {
    input.lines()
    .map(|line| {
        line.chars().map(|c| c.to_digit(10).unwrap()).collect::<Vec<_>>()
    })
    .map(|battery_bank| {
        let mut joltage: u64 = 0;
        let mut index = 0;
        (0..n_digits).rev().for_each(|d| {
            let subbank = &battery_bank[index..battery_bank.len()-d];
            let (subindex, digit) = subbank.iter().enumerate()
            // min_by_key returns *first* matching element, while max_by_key returns *last*.
            // Thus, we need to use min_by_key and Reverse() here.
            .min_by_key(|(_, v)| Reverse(*v)).unwrap();
            index += 1 + subindex;
            joltage *= 10;
            joltage += u64::from(*digit);
        });
        joltage
    }).sum()
}

fn part1(input: &str) -> u64 {
    pipeline(input, 2)
}

fn part2(input: &str) -> u64 {
    pipeline(input, 12)

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

    const TEST_INPUT: &str = r#"987654321111111
811111111111119
234234234234278
818181911112111"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 357)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 3121910778619)
    }
}