use std::{io, collections::{HashMap, VecDeque}};
use aoc;

enum Pulse {
    High,
    Low,
}

enum Module<'a> {
    FlipFlop(String, Vec<&'a str>, bool),
    Conjunction(String, Vec<&'a str>, HashMap<&'a str, Pulse>),
    Broadcast(String, Vec<&'a str>),
}

impl<'a> Module<'a> {
    fn name(&self) -> &String {
        match &self {
            Module::Broadcast(name, _) => name,
            Module::Conjunction(name, _, _) => name,
            Module::FlipFlop(name, _, _) => name,
        }
    }
    fn targets(&self) -> &Vec<&str> {
        match &self {
            Module::Broadcast(_, targets) => targets,
            Module::Conjunction(_, targets, _) => targets,
            Module::FlipFlop(_, targets, _) => targets,
        }
    }
}

fn parse_input(input: &String) -> Vec<Module> {
    let mut modules = input.lines().map(|line| {
        let mut iter = line.split(" -> ");
        let module = iter.next().unwrap();
        let targets: Vec<&str> = iter.next().unwrap().split(", ").collect::<Vec<_>>();
        let mut chars = module.chars().peekable();
        match chars.peek().unwrap() {
            '&' => {
                let name = chars.skip(1).collect::<String>();
                Module::Conjunction(name, targets, HashMap::new())
            },
            '%' => {
                let name = chars.skip(1).collect::<String>();
                Module::FlipFlop(name, targets, false)
            }
            _ => {
                let name = chars.collect::<String>();
                Module::Broadcast(name, targets)
            }
        }
    }).collect::<Vec<_>>();
    for module in modules.iter_mut() {
        match module {
            Module::Conjunction(module_name, _, ref mut memory) => {
                for maybe_source in modules.iter() {
                    let targets = maybe_source.targets();
                    if targets.contains(&module_name.as_str()) {
                        let name = maybe_source.name();
                        memory.insert(name.as_str(),Pulse::Low);
                    }
                }
            }
            _ => {},
        }
    }
    modules
}

fn push<'a>(modules: &mut HashMap<&String, &Module<'a>>, mut on_signal_received: impl FnMut(&str, Pulse) -> Option<u64>) -> Option<u64> {
    let mut state = VecDeque::new();
    state.push_back(("broadcaster", Pulse::Low, "push"));
    while !state.is_empty() {
        let (module, pulse, source) = state.pop_front().unwrap();
        
        if let Some(v) = on_signal_received(module, pulse) {
            return Some(v)
        }

        // TODO: what does a module do?
    }
    None
}

fn part1(input: &String) -> u32 {
    let modules = parse_input(input);
    let mut modules = modules.iter().map(|m| (m.name(), m)).collect::<HashMap<_, _>>();
    let mut low_pulses = 0;
    let mut high_pulses = 0;
    for button_press in 1..1000 {
        push(&mut modules, |module, pulse| {
            match pulse {
                Pulse::High => { high_pulses += 1; }
                Pulse::Low => { low_pulses += 1; }
            }
            None
        }) ;
    }
    low_pulses * high_pulses
}

fn part2(input: &String) -> u32 {
    0
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
    fn test_part1a() {
        let test = String::from(r#"broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"#);
        let result = part1(&test);
        assert_eq!(result, 32000000)
    }

    #[test]
    fn test_part1b() {
        let test = String::from(r#"broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"#);
        let result = part2(&test);
        assert_eq!(result, 11687500)
    }
}