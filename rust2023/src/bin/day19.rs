use std::{io, collections::{HashMap, VecDeque}};
use aoc;

#[derive(Debug)]
enum WorkflowRule {
    LargerThan{category: String, value: u64, target_workflow: String},
    SmallerThan{category: String, value: u64, target_workflow: String},
    Always{target_workflow: String},
}

fn parse_workflows(workflows_str: &str) -> HashMap<&str, Vec<WorkflowRule>> {
    workflows_str.lines().map(|line| -> (&str, Vec<WorkflowRule>) {
        let chars= &['{', '}', ','];
        let mut iter = line.split(chars);
        let workflow_name = iter.next().unwrap();
        let rules = iter
            .filter(|rule| !rule.is_empty())
            .map(|rule| -> WorkflowRule {
                let mut iter = rule.split_inclusive(&['>', '<', ':'][..]);
                let first = iter.next().unwrap();
                match first.chars().last().unwrap() {
                    '>'|'<' => {
                        let op = first.chars().last().unwrap();
                        let category = &first[0..first.len()-1];
                        let val = iter.next().unwrap();
                        let val = val[0..val.len()-1].parse::<u64>().unwrap();
                        let target = iter.next().unwrap();
                        if op == '>' {
                            WorkflowRule::LargerThan{
                                category: String::from(category),
                                value: val,
                                target_workflow: String::from(target)}
                        } else {
                            WorkflowRule::SmallerThan{
                                category: String::from(category),
                                value: val,
                                target_workflow: String::from(target)}
                        }
                    }
                    _ => {
                        WorkflowRule::Always{target_workflow: String::from(first)}
                    }
                }
            }).collect::<Vec<_>>();
        (workflow_name, rules)
    }).collect::<HashMap<_, _>>()
}

fn parse_parts(parts_str: &str) -> Vec<Vec<u64>> {
    parts_str.lines().map(|line| -> Vec<_> {
        line.trim_matches(&['{', '}'][..]).split(',').map(|part| -> (&str, u64) {
            let mut iter = part.split('=');
            let category = iter.next().unwrap();
            let rating = iter.next().unwrap().parse::<u64>().unwrap();
            (category, rating)
        })
        .map(|pair| pair.1)
        .collect::<Vec<_>>()
    }).collect::<Vec<_>>()
}

fn parse_input(input: &String) -> (HashMap<&str, Vec<WorkflowRule>>, Vec<Vec<u64>>) {
    let mut iter = input.split("\n\n");
    let workflows_str = iter.next().unwrap();
    let parts_str = iter.next().unwrap();
    (
        parse_workflows(workflows_str),
        parse_parts(parts_str),
    )
}

fn part1(input: &String) -> u64 {
    let (workflows, parts) = parse_input(input);

    parts.iter().map(|part| {
        let mut workflow_name = String::from("in");
        while workflow_name != "A" && workflow_name != "R" {
            let workflow = &workflows[workflow_name.as_str()];
            for rule in workflow {
                let target = match rule {
                    WorkflowRule::LargerThan { category, value, target_workflow } => {
                        let index = "xmas".find(category.as_str()).unwrap();
                        if part[index] > *value {
                            Some(target_workflow)
                        } else {
                            None
                        }
                    },
                    WorkflowRule::SmallerThan { category, value, target_workflow } => {
                        let index = "xmas".find(category.as_str()).unwrap();
                        if part[index] < *value {
                            Some(target_workflow)
                        } else {
                            None
                        }
                    },
                    WorkflowRule::Always { target_workflow } => {
                        Some(target_workflow)
                    }
                };
                if let Some(target_workflow) = target {
                    workflow_name = target_workflow.to_string();
                    break;
                }
            }
        }
        if workflow_name == "A" {
            part.iter().sum()
        } else {
            0
        }
    }).sum()
}

fn swap(ranges: [(u64, u64); 4], index: usize, replacement: (u64, u64)) -> [(u64, u64); 4] {
    let mut ranges = ranges.clone();
    ranges[index] = replacement;
    ranges
}

fn part2(input: &String) -> u64 {
    let (workflows, _) = parse_input(input);
    let mut states = VecDeque::new();
    let mut accepted = 0;
    states.push_back((String::from("in"), 0, [(1, 4000), (1, 4000), (1, 4000), (1, 4000)]));
    while !states.is_empty() {
        let (workflow_name, rule_index, ranges) = states.pop_front().unwrap();
        if workflow_name == "A" {
            accepted += ranges.iter().map(|r| r.1 - r.0 + 1).product::<u64>();
            continue
        } else if workflow_name == "R" {
            continue
        }
        let workflow = &workflows[workflow_name.as_str()];
        let rule = &workflow[rule_index];
        match rule {
            WorkflowRule::SmallerThan { category, value, target_workflow } => {
                let index = "xmas".find(category.as_str()).unwrap();
                let r = ranges[index];
                if r.0 < *value && *value <= r.1 {
                    let lower = (r.0, value-1);
                    let upper = (*value, r.1);
                    let mut lower_ranges = ranges.clone();
                    lower_ranges[index] = lower;
                    states.push_back((target_workflow.to_owned(), 0, swap(ranges, index, lower)));
                    states.push_back((workflow_name, rule_index + 1, swap(ranges, index, upper)));
                } else {
                    states.push_back((workflow_name, rule_index + 1, ranges))
                }
            },
            WorkflowRule::LargerThan { category, value, target_workflow } => {
                let index = "xmas".find(category.as_str()).unwrap();
                let r = ranges[index];
                if r.0 <= *value && *value < r.1 {
                    let lower = (r.0, *value);
                    let upper = (value+1, r.1);
                    states.push_back((workflow_name, rule_index + 1, swap(ranges, index, lower)));
                    states.push_back((target_workflow.to_owned(), 0, swap(ranges, index, upper)));
                } else {
                    states.push_back((workflow_name, rule_index + 1, ranges))
                }

            },
            WorkflowRule::Always { target_workflow } => {
                states.push_back((target_workflow.to_owned(), 0, ranges))
            }
        };
    }
    accepted
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

    const TEST_INPUT: &str = r#"px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 19114)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        assert_eq!(result, 167409079868000)
    }
}