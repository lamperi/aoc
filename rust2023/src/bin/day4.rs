use std::fs;
use std::io;
use std::collections::HashSet;

fn parse_into_wins_per_game(input: &String) -> impl Iterator<Item = usize> + '_ {
    input.lines().map(|line| {
        let (winning_numbers, my_numbers) = line.split_once(": ")
            .expect("line is missing :")
            .1.split_once(" | ")
            .expect("line is missing |");
        let winning_numbers = winning_numbers.split_whitespace()
            .map(|s| s.parse::<u32>().expect("unable to parse number"))
            .collect::<HashSet<_>>();
        let my_numbers = my_numbers.split_whitespace()
            .map(|s| s.parse::<u32>().expect("unable to parse number"))
            .collect::<HashSet<_>>();
        my_numbers.intersection(&winning_numbers).count()
    })
}

fn part1(input: &String) -> u32 {
    parse_into_wins_per_game(input)
    .filter(|c| *c != 0)
    .map(|c| -> u32 { 1 << (c-1) })
    .sum()
}

fn part2(input: &String) -> u32 {
    let wins_per_game = parse_into_wins_per_game(input).enumerate().collect::<Vec<_>>();
    let mut accumulated_wins = vec![0; wins_per_game.len()];
    for (idx, wins) in wins_per_game.into_iter().rev() {
        accumulated_wins[idx] = 1;
        for jdx in idx+1..=idx+wins {
            accumulated_wins[idx] += accumulated_wins[jdx]
        }
    }
    accumulated_wins.iter().sum()
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/4/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[test]
fn test_part1() {
    let test = r#"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"#.to_string();
    let result = part1(&test);
    assert_eq!(result, 13)
}

#[test]
fn test_part2() {
    let test = r#"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"#.to_string();
    let result = part2(&test);
    assert_eq!(result, 30)
}