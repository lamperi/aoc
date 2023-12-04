use std::fs;
use std::io;

fn part1(input: &String) -> u32 {
    0
}

fn part2(input: &String) -> u32 {
    0
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/X/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[test]
fn test_part1() {
    let test = r#""#.to_string();
    let result = part1(&test);
    assert_eq!(result, 0)
}

#[test]
fn test_part2() {
    let test = r#""#.to_string();
    let result = part2(&test);
    assert_eq!(result, 0)
}