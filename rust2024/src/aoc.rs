use std::fs;
use std::io;

fn guess_day_from_executable() -> io::Result<u8> {
    let path = std::env::current_exe()?;
    let num = path.file_name()
        .and_then(|b| b.to_str())
        .map(|s| s.to_owned())
        .and_then(|s| s.strip_prefix("day").map(|s| s.to_owned()))
        .map(|s| {
            if let Some(stripped) = s.strip_suffix(".exe") {
                stripped.to_owned()
            } else {
                s
            }
        })
        .and_then(|s| s.parse::<u8>().ok())
        .unwrap_or_default();
    Ok(num)
}

pub fn get_input() -> io::Result<String> {
    let day = guess_day_from_executable()?;
    let path: String = format!("../2024/{day}/input.txt");
    let input: String = fs::read_to_string(path)?;
    Ok(input)
}
