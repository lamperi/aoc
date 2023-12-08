use std::collections::HashMap;
use std::fs;
use std::io;

fn parse(input: &String) -> (Vec<char>, HashMap<&str, (&str, &str)>) {
    let mut lines = input.lines();
    let inst = lines.next().unwrap().chars().collect::<Vec<_>>();
    // Consume empty line.s
    lines.next();
    let graph = lines.map(|line| {
        let mut parts = line.split(" = ");
        let source = parts.next().unwrap();
        let left_right = parts.next().unwrap();
        let left = &left_right[1..4];
        let right = &left_right[6..9];
        (source, (left, right))
    }).collect::<HashMap<_, _>>();
    (inst, graph)
}

fn search(start_node: &str, inst: &Vec<char>, graph: &HashMap<&str, (&str, &str)>, f: impl Fn(&str) -> bool) -> u32 {
    let mut i = 0;
    let mut node = start_node;
    while !f(node) {
        let inst = inst[i % inst.len()];
        i += 1;
        let entry = graph.get(node).unwrap();
        node = if inst == 'L' { entry.0 } else { entry.1 };
    }
    return i.try_into().unwrap();
}

fn part1(input: &String) -> u32 {
    let (inst, graph) = parse(input);

    search("AAA", &inst, &graph, |n| n == "ZZZ")
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

fn part2(input: &String) -> u64 {
    let (inst, graph) = parse(input);

    // Note that the search always cycles from end to the start.
    let cycles = graph.keys()
        .filter(|node| node.ends_with("A"))
        .map(|node| {
            search(node, &inst, &graph, |n| n.ends_with("Z"))        
        })
        .collect::<Vec<_>>();
    
    cycles.into_iter().fold(1, |acc, cycle| -> u64 {
        let cycle = cycle as u64;
        acc*cycle / gcd(acc, cycle)
    })
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/8/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 2)
    }

const TEST_INPUT2: &str = r#"LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"#;

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT2);
        let result = part2(&test);
        assert_eq!(result, 6)
    }
}