use std::io;
use regex::Regex;

fn parse(input: &str) -> Vec<[i32; 4]>{
    let regex = Regex::new(r"-?\d+").unwrap();
    input.lines()
        .map(|line|{
            regex.find_iter(line)
                .map(|m| m.as_str().parse::<i32>().unwrap())
                .collect::<Vec<_>>()
                .try_into()
                .unwrap()
        }).collect()
}

fn part1(input: &str) -> u32 {
    let robots = parse(input);
    let (width, height) = if robots.len() < 20 {
        (11, 7)
    } else {
        (101, 103)
    };

    let mut robots = robots.iter().map(|[x,y,vx, vy]| {
        [(x + 100 * vx).rem_euclid(width), (y + 100 * vy).rem_euclid(height)]
    });
    safety_factor(&mut robots, width, height)
}

fn safety_factor(robots: &mut dyn Iterator<Item = [i32; 2]>, width: i32, height: i32) -> u32 {
    let mut quadrants = [0, 0, 0, 0];
    let mx = (width - 1)/2;
    let my = (height - 1)/2;
    for [x,y] in robots {
        if x == mx || y == my {
            continue
        }
        let idx = if x < mx {0} else {1} + if y < my {0} else {2};
        quadrants[idx] += 1;
    }
    quadrants.iter().product()
}

fn part2(input: &str) -> u32 {
    let robots = parse(input);
    let (width, height) = if robots.len() < 20 {
        (11, 7)
    } else {
        (101, 103)
    };

    // It happens so that the picture of the Christmas tree is displayed when
    // the safety factor is the lowest possible (an easter egg). This is due to
    // border of the picture being in the middle of y or x, which greatly reduces
    // the numbers of the product of safety factor. 
    (1..=width*height).map(|t| {
        let mut robots = robots.iter().map(|[x,y,vx, vy]| {
            [(x + t * vx).rem_euclid(width), (y + t * vy).rem_euclid(height)]
        });

        (safety_factor(&mut robots, width, height), t)
    }).min().unwrap().1 as u32
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

    const TEST_INPUT: &str = r#"p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 12)
    }
}