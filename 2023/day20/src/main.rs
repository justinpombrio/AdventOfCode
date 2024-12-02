use std::collections::{HashMap, VecDeque};
use std::env;
use std::fmt;
use std::fs;

type ModId = usize;

#[derive(Debug, Clone, PartialEq, Eq)]
enum Op {
    Noop,
    Broadcast,
    FlipFlop,
    Conj,
}

#[derive(Debug, Clone)]
struct Mod {
    op: Op,
    dests: Vec<ModId>,
}

#[derive(Debug, Clone)]
struct ModSet {
    name_to_module: HashMap<String, ModId>,
    modules: Vec<Mod>,
}

#[derive(Debug, Clone)]
struct Pulse {
    src: ModId,
    value: bool,
    dest: ModId,
}

#[derive(Debug, Clone)]
struct State {
    modset: ModSet,
    low_count: usize,
    high_count: usize,
    pulses: VecDeque<Pulse>,
    flip_flops: Vec<bool>,
    conjs: Vec<Vec<(ModId, bool)>>,
}

impl fmt::Display for State {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "STATE DUMP")?;

        writeln!(f, "  Low:  {}", self.low_count)?;
        writeln!(f, "  High: {}", self.high_count)?;

        write!(f, "  Flip flops: ")?;
        for (i, module) in self.modset.modules.iter().enumerate() {
            if module.op == Op::FlipFlop {
                if self.flip_flops[i] {
                    write!(f, "1")?;
                } else {
                    write!(f, "0")?;
                }
            }
        }
        writeln!(f)?;

        writeln!(f, "  Conjunctions:")?;
        for conj in &self.conjs {
            if !conj.is_empty() {
                write!(f, "    * ")?;
                for (_, value) in conj {
                    if *value {
                        write!(f, "1")?;
                    } else {
                        write!(f, "0")?;
                    }
                }
                writeln!(f)?;
            }
        }
        Ok(())
    }
}

impl fmt::Display for Op {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let label = match self {
            Op::Noop => "!",
            Op::Broadcast => "",
            Op::FlipFlop => "%",
            Op::Conj => "&",
        };
        write!(f, "{}", label)
    }
}

impl fmt::Display for Pulse {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let value = if self.value { "high" } else { "low" };
        write!(f, "{} -{}-> {}", self.src, value, self.dest)
    }
}

impl State {
    fn new(modset: &ModSet) -> State {
        let mut flip_flops = Vec::new();
        flip_flops.resize(modset.modules.len(), false);

        let mut conjs = Vec::new();
        conjs.resize(modset.modules.len(), Vec::new());

        for (id, module) in modset.modules.iter().enumerate() {
            for dest in &module.dests {
                if modset.modules[*dest].op == Op::Conj {
                    conjs[*dest].push((id, false));
                }
            }
        }

        State {
            modset: modset.clone(),
            low_count: 0,
            high_count: 0,
            pulses: VecDeque::new(),
            flip_flops,
            conjs,
        }
    }

    fn exec(&mut self, button_presses: usize) -> usize {
        let broadcast = self.modset.lookup_id("broadcaster");
        let rx = self.modset.lookup_id("rx");

        for i in 0..button_presses {
            if i % 10_000_000 == 0 {
                println!("Iteration: {}", i);
            }
            if i % 100_000_000 == 0 {
                println!("{}", self);
            }
            self.pulses.push_back(Pulse {
                src: broadcast, // dummy
                value: false,
                dest: broadcast,
            });

            while let Some(pulse) = self.pulses.pop_front() {
                if pulse.dest == rx && pulse.value == false {
                    println!("Found! {}", i);
                    return 0;
                }
                match pulse.value {
                    false => self.low_count += 1,
                    true => self.high_count += 1,
                }
                let module = &self.modset.modules[pulse.dest];
                let value = match module.op {
                    Op::Noop => None,
                    Op::Broadcast => Some(pulse.value),
                    Op::FlipFlop => {
                        if pulse.value == false {
                            let new_value = !self.flip_flops[pulse.dest];
                            self.flip_flops[pulse.dest] = new_value;
                            Some(new_value)
                        } else {
                            None
                        }
                    }
                    Op::Conj => {
                        for (mod_id, value) in &mut self.conjs[pulse.dest] {
                            if *mod_id == pulse.src {
                                *value = pulse.value;
                            }
                        }
                        Some(!self.conjs[pulse.dest].iter().all(|(_, v)| *v))
                    }
                };

                if let Some(value) = value {
                    for dest in &module.dests {
                        self.pulses.push_back(Pulse {
                            src: pulse.dest,
                            value,
                            dest: *dest,
                        });
                    }
                }
            }
        }

        self.low_count * self.high_count
    }
}

impl ModSet {
    fn new() -> ModSet {
        ModSet {
            name_to_module: HashMap::new(),
            modules: Vec::new(),
        }
    }

    fn lookup_id(&mut self, mod_name: &str) -> ModId {
        match self.name_to_module.get(mod_name) {
            Some(id) => *id,
            None => {
                let id = self.modules.len();
                self.name_to_module.insert(mod_name.to_owned(), id);
                self.modules.push(Mod {
                    op: Op::Noop,
                    dests: Vec::new(),
                });
                id
            }
        }
    }

    fn add_module(&mut self, mod_name: &str, module: Mod) {
        let id = self.lookup_id(mod_name);
        self.modules[id] = module;
    }
}

fn parse_modules(input: String) -> ModSet {
    let mut modset = ModSet::new();

    for line in input.split("\n") {
        if line.is_empty() {
            continue;
        }
        let src_and_dst = line.split(" -> ").collect::<Vec<_>>();
        let src = src_and_dst[0];
        let dst = src_and_dst[1];
        let dests = dst
            .split(", ")
            .map(|mod_name| modset.lookup_id(mod_name))
            .collect::<Vec<ModId>>();
        match &src[0..1] {
            "%" => modset.add_module(
                &src[1..],
                Mod {
                    op: Op::FlipFlop,
                    dests,
                },
            ),
            "&" => modset.add_module(
                &src[1..],
                Mod {
                    op: Op::Conj,
                    dests,
                },
            ),
            "b" => modset.add_module(
                src,
                Mod {
                    op: Op::Broadcast,
                    dests,
                },
            ),
            _ => unreachable!(),
        }
    }
    modset
}

fn main() {
    let command_line_args = env::args().collect::<Vec<_>>();
    let file_contents = fs::read_to_string(&command_line_args[1]).unwrap();
    let modset = parse_modules(file_contents);
    println!("{:#?}", modset);
    let mut state = State::new(&modset);
    println!("{:#?}", state);
    let count = state.exec(1000_000_000_000);
    println!("Count: {}", count);
}
