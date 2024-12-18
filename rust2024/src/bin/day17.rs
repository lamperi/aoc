use std::io;

type Num = u64;
type Opcode = u8;

type Register = [Num; 3];
type Program = Vec<u8>;

const ADV: Opcode = 0;
const BXL: Opcode = 1;
const BST: Opcode = 2;
const JNZ: Opcode = 3;
const BXC: Opcode = 4;
const OUT: Opcode = 5;
const BDV: Opcode = 6;
const CDV: Opcode = 7;


fn parse(input: &str) -> (Register, Program){
    let (register_input, program_input) = input.split_once("\n\n").unwrap();
    let registers: Register = register_input.lines().map(|line| {
        line.split_ascii_whitespace().last().and_then(|number| number.parse::<Num>().ok())
    }).collect::<Option<Vec<_>>>().unwrap().try_into().unwrap();
    let program: Program = program_input.split_ascii_whitespace()
        .last().unwrap().split(',').map(|number| {
            number.parse::<Opcode>().ok()
        }).collect::<Option<Vec<Opcode>>>().unwrap();
    (registers, program)
}

fn run(register: Register, program: &Program) -> Vec<Num> {
    let [mut a, mut b, mut c] = register;
    let mut op_ptr = 0;
    let literal = |arg: &Opcode| -> Num { *arg as Num };
    let combo = |arg: &Opcode, a: &Num, b: &Num, c: &Num| -> Num {
        match *arg {
            0..=3 => *arg as u64,
            4 => *a,
            5 => *b,
            6 => *c,
            _ => panic!("invalid argument to combo: {}", arg)
        }
    };
    let mut out = Vec::new();
    while let (Some(op), Some(arg)) = (program.get(op_ptr), program.get(op_ptr + 1)) {
        match *op {
            ADV => {
                a >>= combo(arg, &a, &b, &c);
            },
            BXL => {
                b ^= literal(arg);
            },
            BST => {
                b = combo(arg, &a, &b, &c).rem_euclid(8);
            },
            JNZ => {
                if a != 0 {
                    op_ptr = literal(arg) as usize;
                    continue
                }
            },
            BXC => {
                b ^= c;
            },
            OUT => {
                out.push(combo(arg, &a, &b, &c).rem_euclid(8));
            },
            BDV => {
                b = a >> combo(arg, &a, &b, &c);
            },
            CDV => {
                c = a >> combo(arg, &a, &b, &c);
            }
            _ => { panic!("invalid opcode") }
        }
        op_ptr += 2;
    }
    out
}

fn part1(input: &str) -> String {
    let (register, program) = parse(input);
    let out = run(register, &program);
    out.iter().map(|n| n.to_string()).collect::<Vec<_>>().join(",")
}

fn part2(input: &str) -> Num {
    let (_register, program) = parse(input);
    
    let mut stack = Vec::from([0]);
    let mut all_solutions = Vec::new();
    while let Some(a) = stack.pop() {
        for next_three_bits in (0..(1<<3)).rev() {
            let a = (a << 3) | next_three_bits;
            let out = run([a, 0, 0], &program);
            if out[0] == program[program.len() - out.len()] as u64 {
                if out.len() == program.len() {
                    all_solutions.push(a);
                } else if a != 0 {
                    stack.push(a);
                }
            }
        }
    }
    *all_solutions.iter().min().unwrap()
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

    const TEST_INPUT: &str = r#"Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, "4,6,3,5,6,3,5,2,1,0")
    }

    #[test]
    fn test_part2() {
        let input = r#"Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"#;
        let result = part2(input);
        assert_eq!(result, 117440)
    }
}