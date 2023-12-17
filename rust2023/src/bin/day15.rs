use std::io;
use aoc;

fn hash(input: &str) -> u8 {
    let mut h: u16 = 0;
    for c in input.as_bytes() {
        h += *c as u16;
        h *= 17;
        h %= 256;
    }
    h as u8
}

enum Op<'a> {
    Set(&'a str, u8),
    Del(&'a str),
}

fn part1(input: &String) -> u32 {
    let only_line = input.lines().next().unwrap();
    only_line.split(",").map(|s| hash(s) as u32).sum()
}

fn part2(input: &String) -> usize {
    let only_line = input.lines().next().unwrap();
    let mut hash_map: Vec<Vec<(&str, u8)>> = vec![vec![]; 256];
    only_line.split(",").filter_map(|s| match s {
        a if a.contains("=") => {
            let mut i = a.split('=');
            let name = i.next().unwrap();
            let num = i.next().unwrap();
            let num = num.parse::<u8>().unwrap();
            Some(Op::Set(name, num))
        },
        b if b.ends_with("-") => {
            let mut i = b.split('-');
            Some(Op::Del(i.next().unwrap()))
        },
        _ => None,
    }).for_each(|op| {
        match op {
            Op::Set(name, focal_length) => {
                let bucket_num = hash(name);
                let bucket = &mut hash_map[bucket_num as usize];
                let mut found = false;
                for (item_name, item_focal_length) in bucket.iter_mut() {
                    if name == *item_name {
                        *item_focal_length = focal_length;
                        found = true;
                        break;
                    }
                }
                if !found {
                    bucket.push((name, focal_length));
                }
            },
            Op::Del(name) => {
                let bucket_num = hash(name);
                let bucket = &mut hash_map[bucket_num as usize];
                for (index, (item_name, _)) in bucket.iter().enumerate() {
                    if name == *item_name {
                        bucket.remove(index);
                        break
                    }
                }
            },
        }
    });
    hash_map.into_iter()
        .enumerate()
        .flat_map(|(bucket_num, bucket)| {
            bucket.into_iter().enumerate().map(move |(index, (_name, focal_length))| -> usize {
                (bucket_num + 1) * (index + 1) * focal_length as usize
            })
        }).sum()
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

    const TEST_INPUT: &str = r#"rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 1320)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 145)
    }
}