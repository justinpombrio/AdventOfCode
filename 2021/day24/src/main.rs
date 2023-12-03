#![feature(if_let_guard)]

use std::fmt;
use std::fs::File;
use std::io::Read;

#[derive(Debug, Clone)]
enum Op {
    Add,
    Mul,
    Div,
    Mod,
    Eql,
}

#[derive(Debug, Clone)]
enum Expr {
    Int(i32),
    Inp(i32),
    Binop(Op, Box<Expr>, Box<Expr>),
}

impl Expr {
    fn add(x: Expr, y: Expr) -> Expr {
        Expr::Binop(Op::Add, Box::new(x), Box::new(y))
    }
    fn mul(x: Expr, y: Expr) -> Expr {
        Expr::Binop(Op::Mul, Box::new(x), Box::new(y))
    }
    fn div(x: Expr, y: Expr) -> Expr {
        Expr::Binop(Op::Div, Box::new(x), Box::new(y))
    }
    fn modulo(x: Expr, y: Expr) -> Expr {
        Expr::Binop(Op::Mod, Box::new(x), Box::new(y))
    }
    fn eql(x: Expr, y: Expr) -> Expr {
        Expr::Binop(Op::Eql, Box::new(x), Box::new(y))
    }
}

fn add(x: Expr, y: Expr) -> Expr {
    use Expr::*;
    use Op::*;

    match (x, y) {
        (Int(x), Int(y)) => Int(x + y),
        (x, Int(y)) => add(Int(y), x),
        (Int(0), y) => y,
        (Int(x), Binop(Add, y, z)) => match *y {
            Int(y) => Expr::add(Int(x + y), *z),
            // TODO: maybe don't give up here?
            y => Expr::div(Int(x), Expr::add(y, *z)),
        },

        // Not general:
        (Int(x), Inp(y)) => Expr::add(Int(x), Inp(y)),
        (Binop(Add, x1, x2), Binop(Add, y1, y2)) => Expr::add(add(*x1, *y1), add(*x2, *y2)),

        (x, y) if x.is_complex() && y.is_complex() => Expr::add(x, y),
        (x, y) => Expr::add(x, y),

        (x, y) => panic!("NYI:  {} + {}", x, y),
    }
}

fn mul(x: Expr, y: Expr) -> Expr {
    use Expr::*;
    use Op::*;

    match (x, y) {
        (Int(x), Int(y)) => Int(x * y),
        (x, Int(y)) => mul(Int(y), x),
        (Int(0), _) => Int(0),
        (Int(1), y) => y,
        // Not general:
        (Int(x), Binop(Mul, y, z)) => Expr::mul(mul(Int(x), *y), *z),
        (Int(x), Binop(Add, y, z)) => Expr::add(mul(Int(x), *y), mul(Int(x), *z)),
        (Int(x), Inp(i)) => Expr::mul(Int(x), Inp(i)),
        // Not general
        (x, Binop(Eq, y, z)) => Expr::mul(x, Binop(Eq, y, z)),
        (x, y) => panic!("NYI:  {} * {}", x, y),
    }
}

fn div(x: Expr, y: Expr) -> Expr {
    use Expr::*;
    use Op::*;

    match (x, y) {
        (Int(x), Int(y)) => Int(x / y),
        (x, Int(1)) => x,
        (x, y) if x.min() >= 0 && x.max() < y.min() => Int(0),
        (Binop(Add, x, y), z) => add(div(*x, z.clone()), div(*y, z)),
        (Binop(Mul, x, y), z) => mul(div(*x, z), *y),
        (Inp(x), y) => Expr::div(Inp(x), y),
        (x, y) => panic!("NYI:  {} / {}", x, y),
    }
}

fn modulo(x: Expr, y: Expr) -> Expr {
    use Expr::*;
    use Op::*;

    match (x, y) {
        (Int(x), Int(y)) => Int(x % y),
        (Int(0), _) => Int(0),
        (x, Int(y)) if x.max() < y => x,
        (Binop(Add, x, y), z) => add(modulo(*x, z.clone()), modulo(*y, z)),
        (Binop(Mul, x, y), z) => {
            println!("({} * {}) % {}", x, y, z);
            modulo(mul(modulo(*x, z.clone()), modulo(*y, z.clone())), z)
        }
        (Binop(Mul, x, y), z) if x.eq(&z) == Some(true) || y.eq(&z) == Some(true) => Int(0),
        (x, y) => panic!("NYI:  {} % {}", x, y),
    }
}

fn eql(x: Expr, y: Expr) -> Expr {
    use Expr::*;

    match (x, y) {
        (Int(x), Int(y)) if x == y => Int(1),
        (Int(_), Int(_)) => Int(0),
        (Int(x), y) => eql(y, Int(x)),
        (x, Int(y)) => {
            if x.min() > y || x.max() < y {
                Int(0)
            } else {
                // TODO: maybe don't give up
                Expr::eql(x, Int(y))
            }
        }
        (x, y) if let Some(b) = x.eq(&y) => Int(if b { 1 } else { 0 }),
        (x, y) if x.is_complex() && y.is_complex() => Expr::eql(x, y),
        (x, y) => panic!("NYI:  {} == {}", x, y),
    }
}

impl Expr {
    fn min(&self) -> i32 {
        use Expr::*;
        use Op::*;

        match self {
            Int(x) => *x,
            Inp(_) => 1,
            Binop(Add, x, y) => x.min() + y.min(),
            Binop(Mul, x, y) if x.min() >= 0 && y.min() >= 0 => x.min() * y.min(),
            Binop(Div, x, y) if x.min() >= 0 && y.min() >= 0 => x.min() / y.max(),
            Binop(Eql, _, _) => 0,
            x => panic!("NYI:  min {}", x),
        }
    }

    fn max(&self) -> i32 {
        use Expr::*;
        use Op::*;

        match self {
            Int(x) => *x,
            Inp(_) => 9,
            Binop(Add, x, y) => x.max() + y.max(),
            Binop(Mul, x, y) if x.max() >= 0 && y.max() >= 0 => x.max() * y.max(),
            Binop(Div, x, y) if x.min() >= 0 && y.min() >= 0 => x.max() / y.min(),
            Binop(Eql, _, _) => 1,
            x => panic!("NYI:  max {}", x),
        }
    }

    fn eq(&self, other: &Expr) -> Option<bool> {
        let (s_min, s_max) = (self.min(), self.max());
        let (o_min, o_max) = (other.min(), other.max());

        if s_min > o_max || s_max < o_min {
            Some(false)
        } else if s_min == s_max && s_min == o_min && s_max == o_max {
            Some(true)
        } else {
            None
        }
    }

    fn is_complex(&self) -> bool {
        self.min() != self.max()
    }
}

impl fmt::Display for Op {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        use Op::*;

        let s = match self {
            Add => "+",
            Mul => "*",
            Div => "/",
            Mod => "%",
            Eql => "==",
        };
        write!(f, "{}", s)
    }
}

impl fmt::Display for Expr {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        use Expr::*;

        match self {
            Int(i) => write!(f, "{}", i),
            Inp(m) => write!(f, "${}", m),
            Binop(Op::Add, x, y) => write!(f, "[{} + {}]", x, y),
            Binop(op, x, y) => write!(f, "({} {} {})", x, op, y),
        }
    }
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "  w: {}", self.w)?;
        writeln!(f, "  x: {}", self.x)?;
        writeln!(f, "  y: {}", self.y)?;
        writeln!(f, "  z: {}", self.z)
    }
}

#[derive(Debug)]
struct State {
    w: Expr,
    x: Expr,
    y: Expr,
    z: Expr,
}

impl State {
    fn get(&self, var: &str) -> &Expr {
        match var {
            "w" => &self.w,
            "x" => &self.x,
            "y" => &self.y,
            "z" => &self.z,
            _ => panic!("invalid var {}", var),
        }
    }

    fn set(&mut self, var: &str, val: Expr) {
        match var {
            "w" => self.w = val,
            "x" => self.x = val,
            "y" => self.y = val,
            "z" => self.z = val,
            _ => panic!("invalid var {}", var),
        }
    }
}

fn main() {
    use Expr::*;

    let mut file = File::open("input.txt").unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();

    let mut state = State {
        w: Int(0),
        x: Int(0),
        y: Int(0),
        z: Int(0),
    };
    let mut model_index = 0;
    for (i, line) in contents.lines().enumerate() {
        let mut parts = line.split(" ").collect::<Vec<_>>();
        if parts.len() == 2 {
            parts.push("");
        }
        let op = parts[0];
        let dest = parts[1];
        println!("{}: {} {} {}", i, op, parts[1], parts[2]);

        if op == "inp" {
            state.set(dest, Inp(model_index));
            model_index += 1;
            println!("{}", state);
            continue;
        }

        let a = state.get(dest).clone();
        let b = if parts[2].len() == 1 && "wxyz".contains(parts[2]) {
            state.get(parts[2]).to_owned()
        } else {
            Int(parts[2].parse().unwrap())
        };

        let result = match op {
            "add" => add(a, b),
            "mul" => mul(a, b),
            "div" => div(a, b),
            "mod" => modulo(a, b),
            "eql" => eql(a, b),
            _ => panic!("bad op"),
        };
        state.set(dest, result);
        println!("{}", state);
    }
}
