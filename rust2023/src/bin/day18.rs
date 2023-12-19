use std::io;
use aoc;

fn parse_input(input: &String) -> Vec<(char, i64)> {
    input.lines().map(|line| {
        let mut iter = line.split_whitespace();
        let dir = iter.next().unwrap().chars().next().unwrap();
        let n = iter.next().unwrap().parse::<i64>().unwrap();
        (dir, n)
    }).collect::<Vec<_>> ()
}

fn parse_swapped_input(input: &String) -> Vec<(char, i64)> {
    input.lines().map(|line| {
        let iter = line.split_whitespace();
        let color = iter.skip(2).next().unwrap();
        let x: &[_] = &['(', ')', '#'];
        let color = color.trim_matches(x);
        let mut chars = color.chars();
        let dir = match chars.next_back().unwrap() {
            '0' => 'R', '1' => 'D', '2' => 'L', '3' => 'U', _ => '#',
        };
        let n = i64::from_str_radix(chars.as_str(), 16).unwrap();
        (dir, n)
    }).collect::<Vec<_>>()
}

fn instructions_to_cubic_meters(inst: Vec<(char, i64)>) -> i64 {
    let mut pos = (-100, -200);
    let mut corners = Vec::new();
    corners.push(pos);
    for (d, n) in inst {
        let (dy, dx) = match d {
            'R' => ( 0,  1),
            'D' => ( 1,  0),
            'L' => ( 0, -1),
            'U' => (-1,  0),
            _   => ( 0,  0),
        };
        pos = (pos.0 + dy * n, pos.1 + dx * n);
        corners.push(pos);
    }
    assert_eq!(corners.first(), corners.last());

    let (area, perimeter) = corners.windows(2).fold((0, 0),|(area, perimeter), corners| {
        let i = corners[0];
        let j = corners[1];
        (
            area + (i.0 + j.0) * (i.1 - j.1),
            perimeter + (j.0 - i.0).abs() + (j.1 - i.1).abs(),
        )
    });
    (area.abs() + perimeter)/2 + 1

}

fn part1(input: &String) -> i64 {
    let inst = parse_input(input);
    instructions_to_cubic_meters(inst)
}

fn part2(input: &String) -> i64 {
    let inst = parse_swapped_input(input);
    instructions_to_cubic_meters(inst)
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

    const TEST_INPUT: &str = r#"R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 62)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 952408144115)
    }
}