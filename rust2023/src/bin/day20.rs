use std::{io, collections::{HashMap, VecDeque, HashSet}};
use aoc;

#[derive(Copy,Clone,PartialEq)]
enum Pulse {
    High,
    Low,
}

enum Module {
    FlipFlop(String, Vec<String>, bool),
    Conjunction(String, Vec<String>, HashMap<String, Pulse>),
    Broadcast(String, Vec<String>),
}

impl<'a> Module {
    fn name(&self) -> &String {
        match &self {
            Module::Broadcast(name, _) => name,
            Module::Conjunction(name, _, _) => name,
            Module::FlipFlop(name, _, _) => name,
        }
    }
    fn targets(&self) -> &Vec<String> {
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
        let targets: Vec<String> = iter.next().unwrap()
            .split(", ")
            .map(|s| s.to_owned())
            .collect::<Vec<_>>();
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
    for i in 0..modules.len() {
        for j in 0..modules.len() {
            if i == j {
                continue
            }
            // https://users.rust-lang.org/t/problem-borrowing-two-elements-of-vec-mutably/21446
            let (module, maybe_source) = {
                if i < j {
                    let (head, tail) = modules.split_at_mut(i+1);
                    let module = &mut head[i];
                    let maybe_source = &tail[j - i - 1];
                    (module, maybe_source)
                } else {
                    let (head, tail) = modules.split_at_mut(j+1);
                    let maybe_source = &head[j];
                    let module = &mut tail[i - j - 1];
                    (module, maybe_source)
                }
            };
            match module {
                Module::Conjunction(module_name, _, ref mut memory) => {
                    let targets = maybe_source.targets();
                    if targets.contains(&module_name) {
                        let name = maybe_source.name();
                        memory.insert(name.to_owned(), Pulse::Low);
                    }
                }
                _ => {},
            }
        }
    }
    modules
}

fn push(modules: &mut HashMap<String, Module>, mut on_signal_received: impl FnMut(&str, Pulse) -> Option<u64>) -> Option<u64> {
    let mut state = VecDeque::new();
    state.push_back((String::from("broadcaster"), Pulse::Low, String::from("push")));
    while !state.is_empty() {
        let (module, pulse, source) = state.pop_front().unwrap();
        
        if let Some(v) = on_signal_received(module.as_str(), pulse) {
            return Some(v)
        }
        if let Some(module) = modules.get_mut(&module) {
            // TODO: what does a module do?
            match module {
                Module::Broadcast(name, targets) => {
                    for target in targets {
                        let target = target.clone();
                        let name = name.clone();
                        state.push_back((target.clone(), pulse, name.clone()));
                    }
                },
                Module::Conjunction(name, targets, ref mut mem) => {
                    mem.insert(source, pulse);
                    let pulse = if mem.values().all(|p| *p == Pulse::High) {
                        Pulse::Low
                    } else {
                        Pulse::High
                    };
                    for target in targets {
                        state.push_back((target.clone(), pulse, name.clone()));
                    }
                },
                Module::FlipFlop(name, targets, ref mut value) => {
                    if pulse != Pulse::High {
                        *value = !*value;
                        let pulse = if * value {
                            Pulse::High
                        } else {
                            Pulse::Low
                        };
                        for target in targets {
                            state.push_back((target.clone(), pulse, name.clone()));
                        }
                    }
                }
            }
        }
    }
    None
}

fn to_map(modules: Vec<Module>) -> HashMap<String, Module> {
    modules.into_iter()
        .map(|m| (m.name().to_owned(), m))
        .collect::<HashMap<_, _>>()
}     

fn part1(input: &String) -> u32 {
    let modules: Vec<Module> = parse_input(input);
    let mut modules = to_map(modules);
    let mut low_pulses = 0;
    let mut high_pulses = 0;
    for _button_press in 0..1000 {
        push(&mut modules, |_module, pulse| {
            match pulse {
                Pulse::High => { high_pulses += 1; }
                Pulse::Low => { low_pulses += 1; }
            }
            None
        }) ;
    }
    low_pulses * high_pulses
}

fn part2(input: &String) -> u64 {
    let modules: Vec<Module> = parse_input(input);
    let mut modules = to_map(modules);

    let mut sources: HashMap<String, Vec<String>> = HashMap::new();
    for entry in modules.iter() {
        for t in entry.1.targets() {
            let e = sources.entry(t.clone()).or_default();
            e.push(entry.1.name().clone());
        }
    }
    let rx: String = String::from("rx");
    let rx_sources: &Vec<String> = sources.get(&rx).unwrap();
    let important_nodes = 
        rx_sources.iter()
        .flat_map(|parent: &String| {
            let parent_sources: &Vec<String> = sources.get(parent).unwrap();
            parent_sources
        })
        .collect::<HashSet<_>>();
    println!("impotant {:?}", important_nodes);

    let mut last_low_pulse = HashMap::new();
    let mut cycles = HashMap::new();
    
    let mut button_press: u64 = 0;
    loop {
        button_press += 1;
        if let Some(ret) = push(&mut modules, |module, pulse| {
            let module = String::from(module);
            if pulse == Pulse::Low && important_nodes.contains(&module) {
                let prev = last_low_pulse.entry(module.clone()).or_default();
                let cycle = button_press - *prev;
                *prev = button_press;
                cycles.entry(module).or_insert(cycle);
                if cycles.len() == important_nodes.len() {
                    return Some(cycles.values().product());
                }
            }
            None
        }) {
            return ret
        }
    }
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
        let result = part1(&test);
        assert_eq!(result, 11687500)
    }
}