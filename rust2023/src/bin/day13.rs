use std::io;
use aoc;

fn vertical_line(mirror: &Vec<Vec<char>>, x: usize) -> String {
    let mut s = String::new();
    for v in mirror.iter() {
        s.push(v[x]);
    }
    s
}

fn horizontal_line(mirror: &Vec<Vec<char>>, y: usize) -> String {
    let mut s = String::new();
    for c in mirror[y].iter() {
        s.push(*c);
    }
    s
}

fn cracks(s1: String, s2: String) -> usize {
    s1.chars()
        .zip(s2.chars())
        .filter(|(c1, c2)| c1 != c2)
        .count()
}

fn find_line(mirror: &Vec<Vec<char>>, length: usize, line_getter: fn(&Vec<Vec<char>>, usize) -> String , expected_cracks: usize) -> Option<usize> {
    for z in 0..length-1 {
        let mut z0 = z;
        let mut z1 = z+1;
        let mut total_cracks = 0;
        while z1 < length {
            total_cracks += cracks(line_getter(mirror, z0), line_getter(mirror, z1));
            if total_cracks > expected_cracks {
                break
            }
            if z0 == 0 {
                break
            }
            z0 -= 1;
            z1 += 1;
        }
        if total_cracks == expected_cracks {
            return Some(z);
        }
    }
    None
}

fn handle_mirror(mirror: &str, expected_cracks: usize) -> usize {
    let mirror = mirror.lines()
        .map(|line| line.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    if let Some(y) = find_line(&mirror, mirror.len(), horizontal_line, expected_cracks) {
        100 * (y + 1)
    } else {
        if let Some(x) = find_line(&mirror, mirror[0].len(), vertical_line, expected_cracks) {
            x + 1
        } else {
            assert!(false);
            0
        }
    }
}

fn part1(input: &String) -> usize {
    input.split("\n\n")
        .map(|mirror| handle_mirror(mirror, 0))
        .sum()
}

fn part2(input: &String) -> usize {
    input.split("\n\n")
        .map(|mirror| handle_mirror(mirror, 1))
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

    const TEST_INPUT: &str = r#"#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 405)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 400)
    }
}