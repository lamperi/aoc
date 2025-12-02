use std::io;

fn part1(input: &str) -> usize {
    let mut dial: i16 = 50;
    input.lines()
    .filter(|line| {
        let direction = &line[0..1];
        let rotation = &line[1..].parse::<i16>().unwrap();
        if direction == "R" {
            dial += rotation;
            dial %= 100;
        } else {
            dial -= rotation;
            dial %= 100;
        }
        dial == 0
    }).count()
}

fn part2(input: &str) -> i16 {
    let mut dial: i16 = 50;
    input.lines()
    .sum(|line| {
        let direction = &line[0..1];
        let rotation = &line[1..].parse::<i16>().unwrap();
        // Treat L as R by inverting dial twice.
        if direction == "L" {
            dial = (100 - dial) % 100;
        }
        dial += rotation;
        let zero_pointed = dial / 100;
        dial %= 100;
        if direction == "L" {
            dial = (100 - dial) % 100;
        }
        zero_pointed
    })
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

    const TEST_INPUT: &str = r#"L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 3)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 6)
    }
}