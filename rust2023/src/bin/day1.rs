use std::fs::File;
use std::io::BufReader;
use std::io;
use std::io::Read;

fn calibrations(str: &String, matches: Vec<(usize, String)>) -> usize {
    str.lines().map(|text| {
        let first = matches.iter().map(|(val, d)| {
            text.find(d).map(|idx| (idx, val))
        }).filter_map(|o| o).min().map(|(_,x)| x).unwrap_or(&0);
        let last = matches.iter().map(|(val, d)| {
            text.rfind(d).map(|idx| (idx, val))
        }).filter_map(|o| o).max().map(|(_,x)| x).unwrap_or(&0);
        first*10 + last
    }).sum()
}
        
fn part1(str: &String) -> usize {
    calibrations(str, ("0123456789").chars().map(|c| {c.to_string()}).enumerate().collect())
}

fn part2(str: &String) -> usize {
    let mut p1: Vec<(usize, String)> = ("0123456789").chars().map(|c|c.to_string()).enumerate().collect();
    let w = vec!("", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine");
    let mut p2: Vec<(usize, String)> = w.iter().map(|s| s.to_string()).enumerate().skip(1).collect();
    p1.append(&mut p2);
    calibrations(str, p1)
}

fn main() -> io::Result<()> {
    let f = File::open("../2023/1/input.txt")?;
    let mut reader = BufReader::new(f);
    let mut buf = String::new();
    reader.read_to_string(&mut buf)?;

    let sum = part1(&buf);
    println!("Hello, Advent of Code and {sum}!");

    let sum2 = part2(&buf);
    println!("Part 2 would be instead {sum2}!");
    Ok(())
}

#[test]
fn test_part1() {
    let test = String::from(r#"1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"#);
    let result = part1(&test);

    assert_eq!(result, 142)
}

#[test]
fn test_part2() {
    let test = String::from(r#"two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"#);
    let result = part2(&test);
    assert_eq!(result, 281)
}