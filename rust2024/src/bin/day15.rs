use std::{collections::{hash_map::Entry, HashMap, HashSet}, io};
use aoc::{direction::CardinalDirection, grid::Grid, pos::Pos2D};

struct Box {
    id: usize,
    pos: Pos2D<usize>,
    width: usize
}

impl Box {
    fn all_pos(&self) -> impl Iterator<Item = Pos2D<usize>> + '_ {
        (0..self.width).into_iter()
            .map(|x| self.pos + Pos2D{y: 0, x})
    }

    fn all_pos_after_move(&self, dir: CardinalDirection) -> impl Iterator<Item = Pos2D<usize>> + '_ {
        (0..self.width).into_iter()
            .map(move |x| (self.pos + Pos2D{y: 0, x}) + dir)
    }

    fn move_to(&mut self, dir: CardinalDirection) {
        self.pos += dir;
    } 
}

// This routine can be used to print the grid.
#[allow(dead_code)]
fn print_state(pos: Pos2D<usize>, grid: &Grid<'_>, boxes: &Vec<Box>) {
    let mut s = String::new();
    let boxes = boxes.iter().flat_map(|b| b.all_pos()).collect::<HashSet<_>>();
    for y in 0..grid.height {
        for x in 0..grid.width {
            let grid_pos = Pos2D{y, x};
            if pos == grid_pos {
                s += "@";
            } else if boxes.contains(&grid_pos) {
                s += "O";
            } else {
                match grid.get_pos(&grid_pos) as char {
                    '#' => { s. push('#'); }
                    _ => { s.push('.') }
                }
            }
        }
        s.push('\n');
    }
    println!("{}", s);
}

fn common(moves: &str, grid: Grid<'_>, mut boxes: Vec<Box>) -> usize {
    let mut pos = grid.find(b'@').unwrap();
    let mut boxgrid = boxes.iter()
        .flat_map(|b| b.all_pos().map(move |pos| (pos, b.id)))
        .collect::<HashMap<_, _>>();

    let move_to_dir = HashMap::from([
        ('v', CardinalDirection::South),
        ('^', CardinalDirection::North),
        ('<', CardinalDirection::West),
        ('>', CardinalDirection::East)
    ]);
    
    for mov in moves.chars() {
        if mov == '\n' { continue }
        let dir = *move_to_dir.get(&mov).unwrap();
        let mut colliding_pos = vec![pos + dir];
        let mut collides_wall = false;
        let mut moved_boxes: HashSet<usize> = HashSet::new();
        while !collides_wall && !colliding_pos.is_empty(){
            let mut colliding_boxes: Vec<&Box> = Vec::new();
            for pos in &colliding_pos {
                if grid.get_pos(pos) == b'#' {
                    collides_wall = true;
                    break
                }
                if let Entry::Occupied(colliding) = boxgrid.entry(*pos) {
                    let id = *colliding.get();
                    if moved_boxes.insert(id) {
                        colliding_boxes.push(boxes.get(id).unwrap());
                    }
                }
            }
            colliding_pos.clear();
            let next_pos = colliding_boxes.iter()
                .flat_map(|b| b.all_pos_after_move(dir));
            colliding_pos.extend(
                next_pos
            );
        }
        if !collides_wall {
            pos += dir;
            for b in &moved_boxes {
                let b = boxes.get_mut(*b).unwrap();
                for p in b.all_pos() {
                    boxgrid.remove(&p);
                }
            }
            for b in &moved_boxes {
                boxes.get_mut(*b).unwrap().move_to(dir);
            }
            for b in &moved_boxes {
                let b = boxes.get_mut(*b).unwrap();
                for p in b.all_pos() {
                    boxgrid.insert(p, b.id);
                }
            }
        }
    }
    boxes.iter().map(|b| b.pos.y * 100 + b.pos.x).sum()
}

fn part1(input: &str) -> usize {
    let (grid, moves) = input.split_once("\n\n").unwrap();
    let grid = Grid::new(grid).unwrap();
    let boxes = grid.find_all(b'O')
        .enumerate()
        .map(|(id, pos)|Box{pos, id, width: 1}).collect::<Vec<_>>();
    common(moves, grid, boxes)
}


fn part2(input: &str) -> usize {
    let (grid, moves) = input.split_once("\n\n").unwrap();
    // Duplicate grid width.
    let grid = grid
        .replace('#', "##")
        .replace('.', "..")
        .replace('O', "O.")
        .replace('@', "@.");
    let grid = Grid::new(grid.as_str()).unwrap();
    let boxes = grid.find_all(b'O')
        .enumerate()
        .map(|(id, pos)|Box{pos, id, width: 2}).collect::<Vec<_>>();
    common(moves, grid, boxes)
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

    const SMALL_TEST_INPUT: &str = r#"########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"#;

    const LARGE_TEST_INPUT: &str = r#"##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"#;

    #[test]
    fn test_part1_small() {
        let result = part1(SMALL_TEST_INPUT);
        assert_eq!(result, 2028)
    }

    #[test]
    fn test_part1_large() {
        let result = part1(LARGE_TEST_INPUT);
        assert_eq!(result, 10092)
    }

    #[test]
    fn test_part2() {
        let result = part2(LARGE_TEST_INPUT);
        assert_eq!(result, 9021)
    }
}