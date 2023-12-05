use std::fs;
use std::io;

#[derive(Debug)]
struct Interval {
    start: u64,
    length: u64,
}

struct MapInterval {
    dest_start: u64,
    source_start: u64,
    length: u64,
}

impl MapInterval {
    fn source_end(&self) -> u64 {
        self.source_start + self.length
    }

    fn dest_end(&self) -> u64 {
        self.dest_start + self.length
    }

    fn map(&self, value: u64) -> Option<u64> {
        if value >= self.source_start && value < self.source_end() {
            Some(value + self.dest_start - self.source_start)
        } else {
            None
        }
    }
}

fn part1(input: &String) -> u64 {
    let mut sections: std::str::Split<'_, &str> = input.split("\n\n");
    let seeds = sections.next().expect("missing seeds: section");
    let seeds = seeds
        .split_whitespace()
        .skip(1)
        .map(|s| s.parse::<u64>().expect("seed should be unsigned integer"))
        .collect::<Vec<_>>();
    let mappings = sections.map(|s| {
            let mut lines = s.split("\n");
            let map_name = lines.next().unwrap();
            let map_intervals = lines.filter(|line| line.len() > 0).filter_map(|line| {
                let items = line
                    .split_whitespace()
                    .map(|s| s.parse::<u64>().expect("mapping should contain unsigned integer"))
                    .collect::<Vec<_>>();
                // We never return None.
                assert_eq!(items.len(), 3);
                if let [dest_start, source_start, length] = &items[..] {
                    Some(MapInterval{dest_start: *dest_start, source_start: *source_start, length: *length})
                } else {
                    None
                }
        }).collect::<Vec<_>>();
        (map_name, map_intervals)
    }).collect::<Vec<_>>();

    seeds.into_iter().map(|seed| {
        mappings.iter().fold(vec![seed], |seeds, (_map_name, map_intervals)| {
            let mapped = seeds.iter().flat_map(|seed| {
                map_intervals.iter().filter_map(|map_interval| -> Option<u64> {
                    map_interval.map(*seed)
                })
            }).collect::<Vec<_>>();
            if mapped.len() == 0 { seeds } else { mapped }
        }).into_iter().min().unwrap()
    }).min().expect("no seeds")
}

fn part2(input: &String) -> u64 {
    0
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/5/input.txt")?;
    let ans = part1(&input);
    println!("Part 1: {ans}");

    let ans = part2(&input);
    println!("Part 2: {ans}");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    const TEST_INPUT: &str = r#"seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"#;

    #[test]
    fn test_part1() {
        let test = String::from(TEST_INPUT);
        let result = part1(&test);
        assert_eq!(result, 35)
    }

    #[test]
    fn test_part2() {
        let test = String::from(TEST_INPUT);
        let result = part2(&test);
        //assert_eq!(result, 46)
    }
}