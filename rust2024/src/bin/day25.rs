use std::{io, iter::zip};

fn part1(input: &str) -> u32 {
    let schematics: Vec<_> = input.split("\n\n").collect();
    let mut count = 0;
    for (i, x) in schematics.iter().enumerate() {
        for y in &schematics[i+1..] {
            if zip(x.chars(), y.chars()).all(|(xc, yc)| xc != '#' || yc != '#') {
                count += 1;
            }
        }
    }
    count
}


fn main() -> io::Result<()> {
    let input: String = aoc::get_input()?;
    let ans = part1(&input);
    println!("Part 1: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 3)
    }
}