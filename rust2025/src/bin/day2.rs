use std::io;

fn pipeline(input: &str, filter_fn: fn(value: u64) -> bool) -> u64 {
    input.trim_end().split(',')
    .flat_map(|id_range| {
        let low_hi = id_range.split_once("-");
        match low_hi {
            Some((low, hi)) => {
                let low = low.parse::<u64>();
                let hi = hi.parse::<u64>();
                match (low, hi) {
                    (Ok(low), Ok(hi)) => {
                        low..=hi
                    },
                    _ => std::ops::RangeInclusive::new(1, 0)
                }
            },
            None => std::ops::RangeInclusive::new(1, 0)
        }
    })
    .filter(|v| filter_fn(*v))
    .sum()

}

fn part1(input: &str) -> u64 {
   pipeline(input, |n| {
        match match n {
           0..10 => None,
           10..100 => Some((n/10, n%10)),
           100..1000 => None,
           1000..10000 => Some((n/100, n%100)),
           10000..100000 => None,
           100000..1000000 => Some((n/1000, n%1000)),
           1000000..10000000 => None,
           10000000..100000000 => Some((n/10000, n%10000)),
           100000000..1000000000 => None,
           1000000000..10000000000 => Some((n/100000, n%100000)),
           10000000000..100000000000 => None,
           100000000000..1000000000000 => Some((n/1000000, n%1000000)),
           1000000000000..=u64::MAX => None,
        } {
            Some((first, second)) => first == second,
            None => false
        }
    })
}

fn part2(input: &str) -> u64 {
  pipeline(input, |n| {
        
        let mut k = 10;
        while k < n {
            let mut rest = n/k;
            let part = n%k;
            let mut ok = rest >= part && part*10 >= k;
            while rest > 0 {
                if rest % k != part {
                    ok = false;
                    break;
                }
                rest /= k;
            }
            if ok {
                return true
            }
            k *= 10;
        }
        false
    })
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

    const TEST_INPUT: &str = r#"11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"#;

    #[test]
    fn test_part1() {
        let result = part1(TEST_INPUT);
        assert_eq!(result, 1227775554)
    }

    #[test]
    fn test_part2() {
        let result = part2(TEST_INPUT);
        assert_eq!(result, 4174379265)
    }
}