use std::collections::HashMap;
use std::fs;
use std::io;

fn score(c: char) -> u8 {
    match c {
        'A' => 14,
        'K' => 13,
        'Q' => 12,
        'J' => 11,
        'T' => 10,
        n => n.to_string().parse::<u8>().expect(format!("should be number: {n}").as_str())
    }
}

fn part1(input: &String) -> u32 {
    let mut vec: Vec<(Vec<u8>, u32)> = input.lines().map(|line| {
        let mut iter = line.split_whitespace();
        let cards = iter.next().unwrap();
        let cards = cards.chars().map(score).collect::<Vec<_>>();
        let score = iter.next().unwrap().parse::<u32>().unwrap();
        (cards, score)
    }).collect::<Vec<_>>();
    vec.sort_by_key(|(cards, _)| {
        let mut map = HashMap::new();
        for v in cards {
            *map.entry(v).or_insert(0) += 1;
        }
        let mut values = map.values().map(|i| *i).collect::<Vec<_>>();
        values.sort();
        values.reverse();
        (values, cards.clone())
    });
    vec.iter().enumerate().map(|(idx, (_cards, score))| {
        let multiplier: u32 = (idx+1).try_into().unwrap();
        multiplier * score
    }).sum()
}

fn part2(input: &String) -> u32 {
    let mut vec: Vec<(Vec<u8>, u32)> = input.lines().map(|line| {
        let mut iter = line.split_whitespace();
        let cards = iter.next().unwrap();
        let cards = cards.chars().map(score).map(|score| if score == 11 { 1 } else { score }).collect::<Vec<_>>();
        let score = iter.next().unwrap().parse::<u32>().unwrap();
        (cards, score)
    }).collect::<Vec<_>>();
    vec.sort_by_key(|(cards, _)| {
        let mut map = HashMap::new();
        for v in cards {
            *map.entry(v).or_insert(0) += 1;
        }
        /* Part 2 */
        if let Some((_, jokers)) = map.remove_entry(&1) {
            if let Some((key, _)) = map.iter().max_by_key(|(_, count)| *count) {
                map.entry(key).and_modify(|v| { *v += jokers });
            } else {
                // There is nothing left after jokers, just insert something.
                map.entry(&1).or_insert(5);
            }
        }
        let mut values = map.values().map(|i| *i).collect::<Vec<_>>();
        values.sort();
        values.reverse();
        (values, cards.clone())
    });
    vec.iter().enumerate().map(|(idx, (_cards, score))| {
        let multiplier: u32 = (idx+1).try_into().unwrap();
        multiplier * score
    }).sum()
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/7/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 6440)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 5905)
    }
}