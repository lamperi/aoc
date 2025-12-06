use std::io;

fn parse(input: &str) -> Vec<Vec<&str>> {
    let lines = input.lines().collect::<Vec<_>>();
    
    let column_indices = {
        let mut column_indices = (0..lines.first().unwrap().len())
        .filter(|index| {
            let b = lines.iter().map(|l| l.as_bytes()[*index]).collect::<Vec<_>>();
            lines.iter().all(|l| l.as_bytes()[*index] == b' ')
        }).collect::<Vec<_>>();
        column_indices.push(lines.first().unwrap().len());
        column_indices
    };

    let mut start_index = 0;
    column_indices.iter().map(|end_index| {
        let slice = lines.iter().map(|l| &l[start_index..*end_index]).collect::<Vec<_>>();
        start_index = end_index + 1;
        slice
    }).collect::<Vec<_>>()
}

fn part1(input: &str) -> u64 {
    let matrix = parse(input);
    matrix.iter()
    .map(|transposed| {
        let op = transposed.last().unwrap().trim();
        assert!(op == "*" || op == "+");
        let n = transposed.iter().rev().skip(1).map(|n| {
            n.trim().parse::<u64>().unwrap()
        });
        if op == "+" {
            n.sum::<u64>()
        } else {
            n.product()
        }
    }).sum()
}

fn part2(input: &str) -> u64 {
    let matrix = parse(input);
    matrix.iter()
    .map(|transposed| {
        let op = transposed.last().unwrap().trim();
        let number_lines = transposed.iter().rev().skip(1).rev().copied().collect::<Vec<_>>();
        assert!(op == "*" || op == "+");
        let number_count = transposed.first().unwrap().len();
        let numbers = (0..number_count).map(|index|{
            let mut number = 0;
            number_lines.iter().for_each(|line| {
                let c = &line.as_bytes()[index..index+1];
                let c = str::from_utf8(c).unwrap();
                if c != " " {
                    let digit = c.parse::<u64>().unwrap();
                    number *= 10;
                    number += digit;
                }
            });
            number
        });
        if op == "+" {
            numbers.sum::<u64>()
        } else {
            numbers.product()
        }
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

    const TEST_INPUT: &str = r#"123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  "#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 4277556)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 3263827)
    }
}