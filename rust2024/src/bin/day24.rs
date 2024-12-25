use std::{collections::{HashMap, HashSet, VecDeque}, fmt, io, str::FromStr};

#[derive(Copy, Clone, Debug)]
enum Op {
    OR,
    AND,
    XOR
}
#[derive(Debug)]
struct InvalidOp;

impl Op {
    fn apply(&self, left: bool, right: bool) -> bool {
        match self {
            Self::OR => left | right,
            Self::AND => left & right,
            Self::XOR => left ^ right
        }
    }
}

#[derive(Debug)]
struct Gate<'a> {
    left: &'a str,
    right: &'a str,
    output: &'a str,
    op: Op
}


impl FromStr for Op {
    type Err = InvalidOp;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "OR"  => Ok(Op::OR),
            "AND" => Ok(Op::AND),
            "XOR" => Ok(Op::XOR),
            _ => Err(InvalidOp),
        }
    }
}

fn parse(input: &str) -> (HashMap<&str, bool>, Vec<Gate<'_>>){
    let (inputs, gates)  = input.split_once("\n\n").unwrap();
    let inputs = inputs.lines().map(|line| {
        let (reg, val) = line.split_once(": ").unwrap();
        (reg, val.parse::<u8>().unwrap() != 0)
    }).collect::<HashMap<_, _>>();
    let gates = gates.lines().map(|line| {
        let mut iter = line.split_ascii_whitespace();
        let left = iter.next().unwrap();
        let op: &str = iter.next().unwrap();
        let right: &str = iter.next().unwrap();
        iter.next().unwrap();
        let output = iter.next().unwrap();
        Gate{
            left,
            right,
            output,
            op: op.parse().unwrap()
        }
    }).collect::<Vec<_>>();
    (inputs, gates)
}

fn run<'a>(mut inputs: HashMap<&'a str, bool>, gates: &Vec<Gate<'a>>) -> HashMap<&'a str, bool>{
    let mut by_input: HashMap<&str, Vec<&Gate<'_>>> = HashMap::new();
    for gate in gates {
        by_input.entry(gate.left)
            .or_insert_with(|| Vec::new())
            .push(gate);
        by_input.entry(gate.right)
            .or_insert_with(|| Vec::new())
            .push(gate);
    }
    let mut outputs = Vec::new();
    let mut queue = VecDeque::from_iter(inputs.keys().copied());
    while let Some(input) = queue.pop_front() {
        match by_input.get_mut(input) {
            Some(gates) => {
                gates.retain(|gate| {
                    let left_bit = inputs.get(gate.left);
                    let right_bit = inputs.get(gate.right);
                    if left_bit.is_some() && right_bit.is_some() {
                        let out_bit = gate.op.apply(*left_bit.unwrap(), *right_bit.unwrap());
                        inputs.insert(gate.output, out_bit);
                        queue.push_back(gate.output);
                        return false
                    }
                    true
                });
                if !gates.is_empty() {
                    queue.push_back(input);
                }
            },
            None => {
                outputs.push(input);
            }
        }
    }
    outputs.iter()
        .map(|output| (*output, *inputs.get(output).unwrap()))
        .collect::<HashMap<&'a str, bool>>()
}

fn output_to_integer(outputs: HashMap<&str, bool>) -> u64 {
    let mut output = 0;
    for z in 0..outputs.len()  {
        let key = fmt::format(format_args!("z{:0>2}", z));
        let bit = (*outputs.get(&*key).unwrap() as u64) << z;
        output |= bit;
    }
    output
}

fn part1(input: &str) -> u64 {
    let (inputs, gates) = parse(input);
    let outputs: HashMap<&str, bool> = run(inputs, &gates);
    output_to_integer(outputs)
}

fn part2(input: &str) -> String {
    let (_inputs, gates) = parse(input);

    let by_output = gates.iter().map(|gate| {
        (gate.output, gate)
    }).collect::<HashMap<_, _>>();

    let mut found_bad_gates = HashSet::new();
    for gate in by_output.values() {
        let left = by_output.get(gate.left);
        let right = by_output.get(gate.right);
        let left_type = left.map(|g| g.op);
        let right_type = right.map(|g| g.op);
        match (gate.op, left_type, right_type) {
            // Gate which exists right after inputs.
            (Op::AND, None, None) | (Op::XOR, None, None) => {
                assert!(gate.left.starts_with("x") || gate.left.starts_with("y"));
                if gate.output.starts_with("z") && gate.output != "z00" {
                    found_bad_gates.insert(gate.output);
                }
            }
            // This should only exist for z01.
            (Op::XOR, Some(Op::AND), Some(Op::XOR)) |
            (Op::XOR, Some(Op::XOR), Some(Op::AND)) => {
                assert_eq!(gate.output, "z01");
            }
            (Op::AND, Some(Op::XOR), Some(Op::OR)) |
            (Op::AND, Some(Op::OR), Some(Op::XOR)) => {
                // This gate comes 41 times.
                if gate.output.starts_with("z") {
                    found_bad_gates.insert(gate.output);
                }
            }
            // This should only exist after first input.
            (Op::AND, Some(Op::XOR), Some(Op::AND)) => {
                let parent: &&Gate<'_> = &by_output[gate.right];
                assert!(parent.left == "x00" || parent.left == "y00");
                assert!(parent.right == "x00" || parent.right == "y00");
            }
            (Op::AND, Some(Op::AND), Some(Op::XOR)) => {
                let parent: &&Gate<'_> = &by_output[gate.left];
                assert!(parent.left == "x00" || parent.left == "y00");
                assert!(parent.right == "x00" || parent.right == "y00");
            }
            (Op::AND, Some(_), Some(Op::OR)) => {
                found_bad_gates.insert(gate.left);
            }
            (Op::AND, Some(Op::OR), Some(_)) => {
                found_bad_gates.insert(gate.right);
            }
            (Op::AND, Some(Op::XOR), Some(Op::XOR)) |
            (Op::AND, Some(Op::AND), Some(Op::AND)) => {
                // Bad gate! But cannot know which parent is bad.
            }
            (Op::OR, Some(Op::AND), Some(Op::AND)) => {
                // This gate comes 41 times.
                if gate.output.starts_with("z") && gate.output != "z45" {
                    found_bad_gates.insert(gate.output);
                }
            }
            (Op::OR, Some(Op::AND), Some(_)) => {
                found_bad_gates.insert(gate.right);
            }
            (Op::OR, Some(_), Some(Op::AND)) => {
                found_bad_gates.insert(gate.left);
            }
            (Op::XOR, Some(Op::OR), Some(Op::XOR)) |
            (Op::XOR, Some(Op::XOR), Some(Op::OR)) => {
                // This gate comes 41 times.
                if !gate.output.starts_with("z") {
                    found_bad_gates.insert(gate.output);
                }
            }
            (Op::XOR, Some(Op::XOR), Some(Op::XOR)) |
            (Op::XOR, Some(Op::OR), Some(Op::OR))
            => {
                // One parent is bad but cannot know which one.
            }
            (Op::XOR, Some(Op::OR), Some(_)) => {
                found_bad_gates.insert(gate.right);
            }
            (Op::XOR, Some(_), Some(Op::OR)) => {
                found_bad_gates.insert(gate.left);
            }
            _ => {
                panic!("node {} of type {:?} has left parent {} of {:?} and right parent {} of {:?}", gate.output, gate.op, gate.left, left_type, gate.right, right_type);
            }
        }
    }
    let mut bad_gates = Vec::from_iter(found_bad_gates);
    bad_gates.sort();
    return bad_gates.join(",")
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

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 2024)
    }

    const TEST_INPUT: &str = r#"x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"#;


}