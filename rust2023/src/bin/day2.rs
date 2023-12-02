use std::fs::File;
use std::io::BufReader;
use std::io;
use std::io::Read;

fn part1(input: &String) -> u32 {
    input.lines().map(|line| {
        let mut i = line.split(": ");
        let game_id = i.next().unwrap().split_ascii_whitespace().skip(1).next().unwrap().parse::<u32>().unwrap();
        let mut sets = i.next().unwrap().split("; ");
        sets.all(|set| {
            set.split(",").all(|count_cube| -> bool
            {
                let mut i = count_cube.split_ascii_whitespace();
                let count = i.next().unwrap().parse::<u32>().unwrap();
                let color = i.next().unwrap();
                match (count, color) {
                    (count, "red") if count <= 12 => true,
                    (count, "blue") if count <= 13 => true,
                    (count, "green") if count <= 14 => true,
                    _ => false
                }
            })
        }).then_some(game_id).unwrap_or_default()
    }).sum()
}

fn part2(input: &String) -> u32 {
    input.lines().map(|line| {
        let mut i = line.split(": ");
        i.next(); // Discard
        let sets = i.next().unwrap().split("; ");
        sets.fold([0, 0, 0], |acc, set|  {
            set.split(",").fold(acc, |acc, count_cube| {
                let mut i = count_cube.split_ascii_whitespace();
                let count = i.next().unwrap().parse::<u32>().unwrap();
                let color = i.next().unwrap();
                match (count, color) {
                    (count, "red") if count > acc[0] => [count, acc[1], acc[2]],
                    (count, "blue") if count > acc[1] => [acc[0], count, acc[2]],
                    (count, "green") if count > acc[2] => [acc[0], acc[1], count],
                    _ => acc
                }
            })
        }).iter().product::<u32>()
    }).sum()
}

fn main() -> io::Result<()> {
    let f = File::open("../2023/2/input.txt")?;
    let mut reader = BufReader::new(f);
    let mut buf = String::new();
    reader.read_to_string(&mut buf)?;
    let sum = part1(&buf);
    println!("Part 1: {sum}");

    let sum = part2(&buf);
    println!("Part 2: {sum}");
    Ok(())
}

#[test]
fn test_part1() {
    let test = r#"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"#.to_string();
    let result = part1(&test);
    assert_eq!(result, 8)
}

#[test]
fn test_part2() {
    let test = r#"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"#.to_string();
    let result = part2(&test);
    assert_eq!(result, 2286)
}