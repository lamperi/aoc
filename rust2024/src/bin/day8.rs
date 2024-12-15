use std::{collections::{HashMap, HashSet}, io};

type Pos2D = (usize, usize);
type AntennaMap = HashMap<char, Vec<Pos2D>>;

fn add(pos1: &Pos2D, pos2: &Pos2D) -> Pos2D {
    (pos1.0.wrapping_add(pos2.0), pos1.1.wrapping_add(pos2.1))
}
fn sub(pos1: &Pos2D, pos2: &Pos2D) -> Pos2D {
    (pos1.0.wrapping_sub(pos2.0), pos1.1.wrapping_sub(pos2.1))
}

fn parse(input: &str) -> (AntennaMap, Pos2D) {
    let mut antennas: AntennaMap = HashMap::new();
    let max_yx = input.lines().enumerate().map(|(y,line)| {
        line.chars().enumerate()
            .inspect(|(x, c)| {
                if *c != '.' {
                    antennas.entry(*c).or_default().push((y,*x));
                }
            }) 
            .map(|(x, _)| (y, x))
            .max().unwrap()
    }).max().unwrap();
    (antennas, max_yx)
}

fn part1(input: &str) -> usize {
    let (antennas, (max_y, max_x)) = parse(input);
    antennas.values()
        .flat_map(|values| {
            let mut antinodes = Vec::new();
            for pos1 in values {
                for pos2 in values {
                    if pos1 == pos2 {
                        continue
                    }
                    let d = sub(pos1, pos2);
                    let antinode = add(pos1, &d);
                    if (0..=max_y).contains(&antinode.0) && (0..=max_x).contains(&antinode.1) {
                        antinodes.push(antinode);
                    }
                    let antinode = sub(pos2, &d);
                    if (0..=max_y).contains(&antinode.0) && (0..=max_x).contains(&antinode.1) {
                        antinodes.push(antinode);
                    }
                }
            }
            antinodes
        })
        .collect::<HashSet<_>>().len()
}

fn part2(input: &str) -> usize {
    let (antennas, (max_y, max_x)) = parse(input);
    antennas.values()
        .flat_map(|values| {
            let mut antinodes = Vec::new();
            for pos1 in values {
                for pos2 in values {
                    if pos1 == pos2 {
                        continue
                    }
                    let d = sub(pos1, pos2);
                    let mut antinode = *pos1;
                    while (0..=max_y).contains(&antinode.0) && (0..=max_x).contains(&antinode.1) {
                        antinodes.push(antinode);
                        antinode = add(&antinode, &d)
                    }
                    let mut antinode = *pos2;
                    while (0..=max_y).contains(&antinode.0) && (0..=max_x).contains(&antinode.1) {
                        antinodes.push(antinode);
                        antinode = sub(&antinode, &d)
                    }
                }
            }
            antinodes
        })
        .collect::<HashSet<_>>().len()
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

    const TEST_INPUT: &str = r#"............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 14)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 34)
    }
}