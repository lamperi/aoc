use std::collections::HashSet;
use std::fs;
use std::io;
use std::collections::VecDeque;


#[derive(Clone,Copy,Debug,Eq,Hash,PartialEq,PartialOrd)]
struct Coordinate {
    y: usize,
    x: usize,
}

enum Dir {
    North,
    West,
    South,
    East,
}

impl Dir {
    fn opposite(&self) -> Self {
        match &self {
            Dir::North => Self::South,
            Dir::South => Self::North,
            Dir::West =>  Self::East,
            Dir::East =>  Self::West,
        }
    }
}

impl Coordinate {
    fn adjacent(&self) -> impl Iterator<Item = (Coordinate, Dir)> {
        let mut adj = Vec::with_capacity(4);
        adj.push((Self{y: self.y+1, x: self.x}, Dir::South));
        adj.push((Self{y: self.y, x: self.x+1}, Dir::East));
        if let Some(x) = self.x.checked_sub(1) {
            adj.push((Self{y: self.y, x}, Dir::West))
        }
        if let Some(y) = self.y.checked_sub(1) {
            adj.push((Self{y, x: self.x}, Dir::North))
        }
        adj.into_iter()
    }
    fn on(&self, area: &Vec<Vec<char>>) -> Option<char> {
        area.get(self.y)
            .and_then(|v| v.get(self.x))
            .map(|c| *c)
    }
}

fn connects_to(c: char, dir: &Dir) -> bool {
    match dir {
        Dir::North => c == '|' || c == 'L' || c == 'J' || c == 'S',
        Dir::South => c == '|' || c == 'F' || c == '7' || c == 'S',
        Dir::West =>  c == '-' || c == 'J' || c == '7' || c == 'S',
        Dir::East =>  c == '-' || c == 'L' || c == 'F' || c == 'S',
    }
}

fn indexable(input: &String) -> Vec<Vec<char>> {
    input.lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect::<Vec<_>>()
}

fn path(area: &Vec<Vec<char>>) -> HashSet<Coordinate> {
    let start = area.iter()
        .enumerate()
        .filter_map(|(y, line)| {
            line.iter().position(|&c| c == 'S').map(|x| Coordinate{y, x})
        }).next().expect("must have start");
    assert!(start.on(&area).unwrap() == 'S');
    
    let mut queue = VecDeque::from([start]);
    let mut visited = HashSet::from([start]);
    while !queue.is_empty() {
        let coord = queue.pop_front().unwrap();
        let coord_char = coord.on(&area).unwrap();
        for (adj, dir) in coord.adjacent() {
            if !connects_to(coord_char, &dir) {
                continue
            }
            let adj_c = adj.on(&area);
            if adj_c.is_none() {
                continue
            }
            if !connects_to(adj_c.unwrap(), &dir.opposite()) {
                continue
            }
            if visited.insert(adj) {
                queue.push_back(adj);
            }
            
        }
    }   
    visited

}

fn part1(input: &String) -> u32 {
    let area = indexable(input);
    let path = path(&area);
    (path.len() / 2).try_into().unwrap()
}


fn part2(input: &String) -> u32 {
    let area = indexable(input);
    let path = path(&area);
    let sum: usize = area.windows(2).enumerate().map(|(y, slice)| {
        let top = &slice[0];
        let bottom = &slice[1];
        let mut inside = false;
        let c = top.iter().zip(bottom.iter()).enumerate().filter(|(x, (top, bottom))| {
            let is_path = path.contains(&Coordinate { y: y+1, x: *x});
            if path.contains(&Coordinate{y, x: *x}) && is_path {
                if connects_to(**bottom, &Dir::North) && connects_to(**top, &Dir::South) {
                    inside = !inside;
                }
            }
            inside && !is_path
        })
        .count();
        c
    }).sum();
    sum as u32
}


fn main() -> io::Result<()> {
    let input: String = fs::read_to_string("../2023/10/input.txt")?;
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
        let test: String = String::from(r#".....
.S-7.
.|.|.
.L-J.
....."#);
        let result = part1(&test);
        assert_eq!(result, 4)
    }

    #[test]
    fn test_part2a() {
        let test: String = String::from(r#"...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."#);
        let result = part2(&test);
        assert_eq!(result, 4)
    }

    #[test]
    fn test_part2b() {
        let test = String::from(r#".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."#);
        let result = part2(&test);
        assert_eq!(result, 8)
    }

    #[test]
    fn test_part2c() {
        let test = String::from(r#"FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"#);
        let result = part2(&test);
        assert_eq!(result, 10)
    }
}