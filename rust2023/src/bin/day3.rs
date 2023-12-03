use std::fs;
use std::io;

fn find_numbers(input: &String) -> Vec<(u32, usize, usize, usize)> {
    let mut words: Vec<(u32, usize, usize, usize)> = Vec::new();
    for (y, line) in input.lines().enumerate() {
        let mut cur: Option<String> = None;
        let mut x0: usize = 0;
        for (x, c) in line.chars().enumerate() {
            if c.is_digit(10) {
                match cur {
                    Some(ref mut s) => {
                        s.push(c);
                    },
                    None => {
                        let mut s = String::new();
                        s.reserve_exact(3);
                        s.push(c);
                        cur = Some(s);
                        x0 = x;
                    }
                }
            } else {
                if let Some(ref s) = cur {
                    words.push((s.parse::<u32>().unwrap(), y, x0, x));
                    cur = None;
                }
            }
        }
        if let Some(ref s) = cur {
            words.push((s.parse::<u32>().unwrap(), y, x0, line.len()))
        }
    }
    words
}

fn neighbors_symbol(input: &String, y: usize, x0: usize, x1: usize) -> bool {
    let min_y = if y == 0 { y } else { y-1 };
    for y in min_y..= (y+1) {
        let min_x = if x0 == 0 { x0 } else { x0-1 };
        for x in min_x..=x1 {
            if let Some(line) = input.lines().nth(y) {
                if let Some(char) = line.chars().nth(x) {
                    if !char.is_digit(10) && char != '.' {
                        return true
                    }
                }
            }
        }
    }
    false
}

fn part1(input: &String) -> u32 {
    let numbers: Vec<(u32, usize, usize, usize)> = find_numbers(input);
    numbers.iter().map(|(val, y, x0, x1)| {
        if neighbors_symbol(input, *y, *x0, *x1) { 
            println!("{val}: y={y}, x0={x0}, x1={x1}");
            *val
        } else { 0 }
    }).sum()
}

fn part2(input: &String) -> u32 {
    let numbers: Vec<(u32, usize, usize, usize)> = find_numbers(input);
    input.lines().enumerate()
    .flat_map(|(y, line)| {
        line.chars().enumerate()
        .map(move |(x, c)| {
            (y, x, c)
        })
    })
    .filter(|(_, _, c)| *c == '*')
    .map(|(y, x, _)| {
        numbers.iter().filter(|(_, y0, x0, x1)| -> bool {
            *y0 <= y + 1 && y <= y0 + 1 && *x0 <= x + 1 && x <= *x1
        }).collect::<Vec<_>>()
    })
    .filter(|v| v.len() == 2)
    .map(|v| v.first().unwrap().0 * v.last().unwrap().0).sum()
}


fn main() -> io::Result<()> {
    let buf: String = fs::read_to_string("../2023/3/input.txt")?;
    let sum = part1(&buf);
    println!("Part 1: {sum}");

    let sum = part2(&buf);
    println!("Part 2: {sum}");
    Ok(())
}

#[test]
fn test_part1() {
    let test = r#"467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."#.to_string();
    let result = part1(&test);
    assert_eq!(result, 4361)

}

#[test]
fn test_part2() {
    let test = r#"467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."#.to_string();
    let result = part2(&test);
    assert_eq!(result, 467835)
}