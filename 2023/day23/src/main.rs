use std::env;
use std::fmt;
use std::fs;

type Pos = (i32, i32);

#[derive(Clone)]
struct Path {
    grid: Vec<Vec<bool>>,
    path: Vec<Pos>,
    start: Pos,
    end: Pos,
}

impl Path {
    fn new(input: &str) -> Path {
        let mut grid = vec![Vec::new()];
        for ch in input.chars() {
            match ch {
                '.' | '<' | '>' | 'v' | '^' => grid.last_mut().unwrap().push(false),
                '#' => grid.last_mut().unwrap().push(true),
                '\n' => grid.push(Vec::new()),
                _ => unreachable!(),
            }
        }
        grid.pop(); // trailing newline
        let start = (0, 1);
        let end = ((grid.len() - 1) as i32, (grid[0].len() - 2) as i32);
        let mut path = Path {
            grid,
            path: Vec::new(),
            start,
            end,
        };
        path.extend(start);
        path
    }

    fn len(&self) -> usize {
        self.path.len() - 1
    }

    fn valid(&self, pos: Pos) -> bool {
        pos.0 >= 0
            && pos.1 >= 0
            && pos.0 < self.grid.len() as i32
            && pos.1 < self.grid[0].len() as i32
    }

    fn valid_next_steps(&self) -> Vec<Pos> {
        let mut steps = Vec::new();
        let (r, c) = self.path.last().unwrap();
        let (r, c) = (*r, *c);
        for (r, c) in [(r, c + 1), (r, c - 1), (r - 1, c), (r + 1, c)] {
            if self.valid((r, c)) && !self.grid[r as usize][c as usize] {
                steps.push((r, c));
            }
        }
        steps
    }

    fn extend(&mut self, step: Pos) {
        let (r, c) = step;
        self.grid[r as usize][c as usize] = true;
        self.path.push((r, c));
    }
}

impl fmt::Display for Path {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for (r, row) in self.grid.iter().enumerate() {
            for (c, cell) in row.iter().enumerate() {
                if self.path.contains(&(r as i32, c as i32)) {
                    write!(f, "o")?;
                } else if self.grid[r][c] {
                    write!(f, "#")?;
                } else {
                    write!(f, ".")?;
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

fn solve(path: Path) -> usize {
    let mut frontier = vec![path];
    let mut i = 0u64;
    let mut longest_len = 0;
    while let Some(mut path) = frontier.pop() {
        i += 1;

        if *path.path.last().unwrap() == path.end {
            if path.len() > longest_len {
                longest_len = path.len()
            }
            continue;
        }

        if i % 100000000 == 0 {
            println!("{}", path);
            println!("Iteration: {}", i);
            println!("Path len: {}", path.len());
            println!("Frontier size: {}", frontier.len());
            println!("Longest len: {}", longest_len);
            println!();
        }

        let mut next_steps = path.valid_next_steps();
        if let Some(step) = next_steps.pop() {
            for step in next_steps {
                let mut new_path = path.clone();
                new_path.extend(step);
                frontier.push(new_path);
            }
            path.extend(step);
            frontier.push(path);
        }
    }
    longest_len
}

fn main() {
    let filename = env::args().nth(1).expect("Needs input filename arg");
    let input = fs::read_to_string(filename).unwrap();
    let path = Path::new(&input);
    println!("{}", path);
    println!("LONGEST LENGTH: {}", solve(path));
}
