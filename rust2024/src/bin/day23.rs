use std::{collections::{HashMap, HashSet}, io};

type Graph<'a> = HashMap<&'a str, HashSet<&'a str>>;

struct BiGraph<'a> {
    connections: Graph<'a>
}
impl <'a> BiGraph<'a> {
    fn new() -> Self {
        Self{connections: Graph::new()}
    }
    fn connect(&mut self, a: &'a str, b: &'a str) {
        self.connections.entry(a).or_default().insert(b);
        self.connections.entry(b).or_default().insert(a);
    }
    fn nodes(&self) -> impl Iterator<Item = &&'a str> {
        self.connections.keys()
    }
}

impl <'a> FromIterator<(&'a str, &'a str)> for BiGraph<'a> {
    fn from_iter<T: IntoIterator<Item = (&'a str, &'a str)>>(iter: T) -> Self {
        let mut c = BiGraph::new();
        for (a,b) in iter {
            c.connect(a, b);
        }
        c
    }
}

fn parse(input: &str) -> BiGraph {
    input.lines()
        .map(|line|  {
            line.split_once('-')
        })
        .collect::<Option<_>>().unwrap()
}

fn part1(input: &str) -> u32 {
    let g = parse(input);
    g.nodes()
    .map(|a| {
        let mut x = 0;
        for b in &g.connections[a] {
            for c in &g.connections[a] {
                if a < b && b < c
                && (a.starts_with('t') || b.starts_with('t') || c.starts_with('t'))
                && g.connections[b].contains(c) {
                    x += 1;
                }
            }
        }
        x
    }
    ).sum()
}

fn find_largest_clique<'a>(candidates: &[&'a str], clique: &HashSet<&'a str>, g: &BiGraph) -> HashSet<&'a str> {
    candidates.iter().enumerate()
        .filter(|(_i, node)| g.connections[**node].is_superset(clique))
        .map(|(i, node)| {
            let next_candidates = &candidates[i+1..];
            let mut next_clique = clique.clone();
            next_clique.insert(*node);
            find_largest_clique(next_candidates, &next_clique, g)
        })
        .max_by_key(|s| s.len()).unwrap_or_else(|| clique.clone())
}

fn part2(input: &str) -> String {
    let g = parse(input);
    let mut visited = HashSet::new();
    g.nodes()
    .map(|node| {
        let connections = g.connections[*node].iter()
            .filter(|n| !visited.contains(n))
            .copied().collect::<Vec<_>>();
        visited.insert(node);
        let clique = HashSet::from([*node]);
        find_largest_clique(&connections, &clique, &g)
    })
    .max_by_key(|item| item.len())
    .map(|v| {
        let mut v = v.iter().map(|s| s.to_string()).collect::<Vec<_>>();
        v.sort();
        v.join(",")
    }).unwrap()
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

    const TEST_INPUT: &str = r#"kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 7)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, "co,de,ka,ta")
    }
}