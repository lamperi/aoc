use std::fs;
use std::io;

fn part_with_expand(input: &String, expand_factor: usize) -> u64 {
    let lines = input.lines().collect::<Vec<_>>();
    let empty_y_space: Vec<_> = lines.iter()
        .enumerate()
        .filter(|(_y, line)| line.chars().all(|c| c== '.'))
        .map(|(y, _line)| y)
        .collect();

    let line_length = lines[0].len();

    let empty_x_space: Vec<_> = (0..line_length)
        .filter(|x| {
            lines.iter()
                .enumerate()
                .all(|(_y, line)| line.chars().nth(*x).unwrap() == '.')
        }).collect();

    let galaxies = lines.iter()
        .enumerate()
        .flat_map(|(y, line)| {
            line.char_indices().filter_map(move |(x, c)| {
                if c == '#' {
                    Some((y, x))
                } else {
                    None
                }
            })
        }).collect::<Vec<_>>();

    galaxies.iter()
        .enumerate()
        .map(|(idx, (y1, x1))| -> u64 {
            galaxies.iter()
                .skip(idx+1)
                .map(|(y2, x2)| {
                    let max_y = y1.max(y2);
                    let min_y = y1.min(y2);
                    // unwrap_err --> the value wasn't found, but gives the index to insert.
                    let lower = empty_y_space.binary_search(min_y).unwrap_err();
                    let higher = empty_y_space.binary_search(max_y).unwrap_err();
                    let empty_y_count = higher - lower;
                    let y_diff = max_y - min_y + empty_y_count*(expand_factor-1);

                    let max_x = x1.max(x2);
                    let min_x = x1.min(x2);
                    let lower = empty_x_space.binary_search(min_x).unwrap_err();
                    let higher = empty_x_space.binary_search(max_x).unwrap_err();
                    let empty_x_count = higher - lower;
                    let x_diff = max_x - min_x + empty_x_count*(expand_factor-1);

                    (x_diff + y_diff) as u64
                }).sum()
        }).sum()
}

fn part1(input: &String) -> u64 {
    part_with_expand(input, 2)
}

fn part2(input: &String) -> u64 {
    part_with_expand(input, 1000000)
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/11/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 374)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part_with_expand(&test, 10);
        assert_eq!(result, 1030);

        let result = part_with_expand(&test, 100);
        assert_eq!(result, 8010)
    }
}