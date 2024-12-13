use std::io;
use regex::Regex;

type Num = i64;
type Pos2D = (Num, Num);


fn parse(input: &str, shift: Num) -> Vec<(Pos2D, Pos2D, Pos2D)> {
    let machine_regex: Regex = Regex::new(r"Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)").unwrap();
    let v: Result<Vec<_>, _> = input.split("\n\n")
    .map(|block| -> Result<(Pos2D, Pos2D, Pos2D), Box<dyn std::error::Error>> {
        let (_, [ax, ay, bx, by, px, py]) =
            machine_regex.captures(block).ok_or("could not match regex")?.extract();
        let ax = ax.parse::<Num>()?;
        let ay = ay.parse::<Num>()?;
        let bx = bx.parse::<Num>()?;
        let by = by.parse::<Num>()?;
        let px = px.parse::<Num>()? + shift;
        let py = py.parse::<Num>()? + shift;
        Ok(((ax, ay), (bx, by), (px, py)))
    }).collect();
    v.expect("was not able to parse")
}

fn solve(params: &(Pos2D, Pos2D, Pos2D)) -> Num {
    let ((ax, ay), (bx, by), (px, py)) = params;
    let m = (ax * py - ay * px)/(ax * by - ay * bx);
    let n = (px - m * bx)/(ax);
    if n * ax + m *bx == *px && n * ay + m * by == *py {
        3*n + m
    } else {
        0
    }
}

fn part1(input: &str) -> Num {
    parse(input, 0).iter()
        .map(solve)
        .sum()
}

fn part2(input: &str) -> Num {
    parse(input, 10000000000000).iter()
        .map(solve)
        .sum()
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

    const TEST_INPUT: &str = r#"Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 480)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 875318608908)
    }
}