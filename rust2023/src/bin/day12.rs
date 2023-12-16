use std::collections::HashMap;
use std::fs;
use std::io;

fn parse_line(line: &str) -> (&str, Vec<u64>) {
    let mut iter = line.split_whitespace();
    let springs = iter.next().unwrap();
    let damaged_spring_counts = iter.next().unwrap();
    let damaged_spring_counts = damaged_spring_counts.split(",")
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();
    (springs, damaged_spring_counts)
}

fn handle_springs(arg: (String, Vec<u64>)) -> u64 {
    let mut states: HashMap<(u64, usize), u64> = HashMap::new();
    states.insert((0, 0), 1);
    let damaged_spring_counts = arg.1;
    for c in arg.0.chars().chain(".".chars()) {
        let mut new_states: HashMap<(u64, usize), u64> = HashMap::new();
        states.into_iter().for_each(|((current_damage, clues_processed), combinations)| {
            if c == '#' || c == '?' {
                if clues_processed < damaged_spring_counts.len() && current_damage < damaged_spring_counts[clues_processed] {
                    *new_states.entry((current_damage + 1, clues_processed)).or_default() += combinations;
                }
            }
            if c == '.' || c == '?' {
                if current_damage == 0 {
                    *new_states.entry((0, clues_processed)).or_default() += combinations;
                } else if current_damage == damaged_spring_counts[clues_processed] {
                    *new_states.entry((0, clues_processed + 1)).or_default() += combinations;
                }
            }
        });
        states = new_states;
    }
    let k = (0u64, damaged_spring_counts.len());
    states.get(&k).unwrap().to_owned()
}

fn part1(input: &String) -> u64 {
    input.lines()
        .map(parse_line)
        .map(|(s,v)| (s.to_string(), v))
        .map(handle_springs)
        .sum()
}

fn multiply(arg: (&str, Vec<u64>)) -> (String, Vec<u64>) {
    let mut springs = String::new();
    let mut v = Vec::with_capacity(arg.1.len() * 5);
    for i in 1..=5 {
        springs.push_str(arg.0);
        if i < 5 {
            springs.push('?');
        }
        v.extend(arg.1.iter());
    }
    (springs, v)
}

fn part2(input: &String) -> u64 {
    input.lines()
        .map(parse_line)
        .map(multiply)
        .map(handle_springs)
        .sum()

}


fn main() -> io::Result<()> {
    let day = guess_day_from_executable().expect("can't figure out day");
    let path: String = format!("../2023/{day}/input.txt");
    let input: String = fs::read_to_string(path)?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

fn guess_day_from_executable() -> Option<u64> {
    std::env::current_exe().ok()
        .and_then(|bin| {
            bin.file_name()
                .and_then(|b| b.to_str())
                .map(|s| s.to_owned())
        })
        .and_then(|s| s.strip_prefix("day").map(|s| s.to_owned()))
        .map(|s| {
            if let Some(stripped) = s.strip_suffix(".exe") {
                stripped.to_owned()
            } else {
                s
            }
        })
        .and_then(|s| s.parse::<u64>().ok())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 21)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 525152)
    }
}