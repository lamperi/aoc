use std::{collections::{HashMap}, io};

type Coord = (u64, u64, u64);

fn parse(input: &str) -> Vec<Coord> {
    input.lines()
    .map(|line|{
        let mut iter = line.split(",");
        let x = iter.next().map(|x| x.parse::<u64>());
        let y = iter.next().map(|x| x.parse::<u64>());
        let z = iter.next().map(|x| x.parse::<u64>());
        (x, y, z)
    })
    .map(|(x, y, z)| (x.unwrap(), y.unwrap(), z.unwrap()))
    .map(|(x, y, z)| (x.unwrap(), y.unwrap(), z.unwrap()))
    .collect()
}

fn compute_distances(coords: &[Coord]) -> Vec<(u64, usize, usize)> {
    let mut v = coords.iter().enumerate()
    .flat_map(move |(i, c1)| {
        coords.iter().enumerate().skip(i+1)
        .map(move |(j, c2)| {
            let (x1, y1, z1) = c1;
            let (x2, y2, z2) = c2;
            let xd = x1.max(x2) - x1.min(x2);
            let yd = y1.max(y2) - y1.min(y2);
            let zd = z1.max(z2) - z1.min(z2);
            let d = xd*xd + yd*yd + zd*zd;
            (d, i, j)
        })
    }).collect::<Vec<_>>();
    v.sort();
    v
}

enum Solution {
    Part1(u64),
    Part2(u64)
}

fn connect_boxes(coords: &[Coord], distances: &[(u64, usize, usize)], n: usize) -> Solution {
    let mut junction: HashMap<usize, i32> = HashMap::new();
    let mut junction_id = 1;
    let mut connections = 0;
    let part2sol = distances.iter().take(n)
    .map(|(_, i, j)| {
        match (junction.contains_key(i), junction.contains_key(j)) {
            (true, true) => {
                let update_key = junction[j];
                let into_key = junction[i];
                for (_, v) in junction.iter_mut() {
                    if update_key == *v {
                        *v = into_key;
                    }
                }
            },
            (true, false) => {
                junction.insert(*j,  junction[i]);
                connections += 1;
            },
            (false, true) => {
                junction.insert(*i,  junction[j]);
                connections += 1;
            },
            (false, false) => {
                junction.insert(*i,  junction_id);
                junction.insert(*j,  junction_id);
                junction_id += 1;
                connections += 2;
            }
        }
        if connections == coords.len() {
            let x1 = coords[*i].0;
            let x2 = coords[*j].0;
            Some(x1*x2)
        } else {
            None
        }
    }).find(|e| e.is_some()).flatten();
    match part2sol {
        Some(x) => {
            Solution::Part2(x.into())
        }
        None => {
            let mut counter: HashMap<i32, u64> = HashMap::new();
            junction.iter().for_each(|(_, v)| {
                *counter.entry(*v).or_default() += 1
            });
            let mut v = counter.values().copied().collect::<Vec<_>> ();
            v.sort();
            Solution::Part1(v.iter().rev().take(3).product())
        }
    }
}

fn part1(input: &str) -> u64 {
    let coords = parse(input);
    let distances = compute_distances(&coords);
    let run_connections = if coords.len() > 20 { 1000 } else { 10 };
    let solution = connect_boxes(&coords, &distances, run_connections);
    match solution {
        Solution::Part1(ans) => ans,
        _ => panic!("Computed wrong solution in part 1!")
    }
}

fn part2(input: &str) -> u64 {
    let coords = parse(input);
    let distances = compute_distances(&coords);
    let solution = connect_boxes(&coords, &distances, distances.len());
    match solution {
        Solution::Part2(ans) => ans,
        _ => panic!("Computed wrong solution in part 2!")
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

    const TEST_INPUT: &str = r#"162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 40)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 25272)
    }
}