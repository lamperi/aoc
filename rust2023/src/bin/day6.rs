use std::fs;
use std::io;

fn part1(input: &String) -> u32 {
    let mut lines = input.split("\n").into_iter();
    let times = lines.next().unwrap().split_ascii_whitespace().skip(1).flat_map(|s| s.parse::<u32>());
    let distances = lines.next().unwrap().split_ascii_whitespace().skip(1).flat_map(|s| s.parse::<u32>());

    let times = times.collect::<Vec<_>>();
    let distances = distances.collect::<Vec<_>>();
    println!("times {times:?} distances {distances:?}");
    let times = times.into_iter();
    let distances = distances.into_iter();
    times.zip(distances).map(|(time, distance)| -> u32 {
        (1..time).map(|t| t*(time-t)).filter(|d| *d > distance).count().try_into().expect("cannot fit u32")
    }).product()
}

fn part2(input: &String) -> u32 {
    let mut lines = input.split("\n").into_iter();
    let time = lines.next().unwrap().split_ascii_whitespace().skip(1).collect::<String>().parse::<u64>().unwrap();
    let distance = lines.next().unwrap().split_ascii_whitespace().skip(1).collect::<String>().parse::<u64>().unwrap();

    (1..time)
        .map(|t| t*(time-t))
        .filter(|d| *d > distance)
        .count()
        .try_into().unwrap()
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/6/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"Time:      7  15   30
    Distance:  9  40  200"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 288)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 71503)
    }
}