use std::io;

type Num = u64;

fn parse(input: &str) -> Vec<(Num, Vec<Num>)> {
    input.lines()
    .map(|line|{
        let (target, operands) = line.split_once(": ").expect("split by ': '");
        let target = target.parse::<Num>().expect("target is a number");
        let operands: Result<Vec<_>, _> = operands.split_whitespace().map(|s| s.parse::<Num>()).collect();
        let operands = operands.expect("operands are numbers");
        (target, operands)
    })
    .collect()
}

fn part1(input: &str) -> Num {
    parse(input).iter()
        .filter(|(target, operands)| {
            let len = operands.len();
            let mut stack = vec![(operands[0], 1)];
            while let Some((v, index)) = stack.pop() {
                if index == len && v == *target {
                    return true
                }
                if index < len && v <= *target {
                    let n = operands[index];
                    stack.push((v * n, index + 1));
                    stack.push((v + n, index + 1));
                }
            }
            false
        })
        .map(|(target,_ )| target)
        .sum()
}

fn part2(input: &str) -> Num {
    parse(input).iter()
        .filter(|(target, operands)| {
            fn concat(v: Num, n: Num) -> Num {
                if n < 10 { 10*v + n}
                else if n  < 100 { 100*v + n }
                else if n < 1000 {1000*v + n }
                else if n < 10000 { 10000*v + n }
                else { panic!("not enough cases") }
            }
            let len = operands.len();
            let mut stack = vec![(operands[0], 1)];
            while let Some((v, index)) = stack.pop() {
                if index == len && v == *target { 
                    return true
                }
                if index < len && v <= *target {
                    let n = operands[index];
                    stack.push((concat(v, n), index + 1));
                    stack.push((v * n, index + 1));
                    stack.push((v + n, index + 1));
                }
            }
            false
        })
        .map(|(target,_ )| target)
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

    const TEST_INPUT: &str = r#"190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 3749)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 11387)
    }
}