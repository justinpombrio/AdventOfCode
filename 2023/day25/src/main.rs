use std::env;
use std::fmt;
use std::fs;

type Node = usize;

struct Graph {
    nodes: Vec<String>,
    size: usize,
    edges: Vec<Vec<bool>>,
    outgoing: Vec<Vec<usize>>,
    edge_list: Vec<(usize, usize)>,
}

impl Graph {
    fn new() -> Graph {
        Graph {
            nodes: Vec::new(),
            size: 0,
            edges: Vec::new(),
            outgoing: Vec::new(),
            edge_list: Vec::new(),
        }
    }

    fn add_node(&mut self, node: &str) {
        if self.nodes.contains(&node.to_owned()) {
            return;
        }
        self.nodes.push(node.to_owned());
        self.outgoing.push(Vec::new());
        self.size += 1;
        for connections in &mut self.edges {
            connections.push(false);
        }
        self.edges.push(vec![false; self.size]);
    }

    fn add_edge(&mut self, start: &str, end: &str) {
        let i = self.nodes.iter().position(|x| x == start).unwrap();
        let j = self.nodes.iter().position(|x| x == end).unwrap();
        self.edges[i][j] = true;
        self.edges[j][i] = true;
        self.outgoing[i].push(j);
        self.outgoing[j].push(i);
        self.edge_list.push((i, j));
    }

    fn flood(&self, start: Node, cut: [(Node, Node); 3]) -> usize {
        let mut flooded = vec![false; self.size];
        let mut num_flooded = 0;
        let mut frontier = vec![start];
        while let Some(node) = frontier.pop() {
            if !flooded[node] {
                flooded[node] = true;
                num_flooded += 1;
                for connection in &self.outgoing[node] {
                    if !cut.contains(&(node, *connection)) && !cut.contains(&(*connection, node)) {
                        frontier.push(*connection);
                    }
                }
            }
        }
        num_flooded
    }
}

impl fmt::Display for Graph {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        writeln!(f, "Graph:")?;
        for node in &self.nodes {
            writeln!(f, "  node {}", node)?;
        }
        for i in 0..self.size {
            for j in i + 1..self.size {
                if self.edges[i][j] {
                    writeln!(f, "  edge {} -> {}", self.nodes[i], self.nodes[j])?;
                }
            }
        }
        Ok(())
    }
}

fn main() {
    let filename = env::args().nth(1).expect("Needs input filename arg");
    let input = fs::read_to_string(filename).unwrap();
    let mut graph = Graph::new();
    for line in input.split("\n") {
        if line == "" {
            continue;
        }
        let parts = line.split(": ").collect::<Vec<_>>();
        let node = &parts[0];
        let connections = parts[1].split(" ").collect::<Vec<_>>();
        graph.add_node(node);
        for connection in connections {
            graph.add_node(connection);
            graph.add_edge(node, connection);
        }
    }
    println!("{}", graph);

    let n = graph.edge_list.len();
    for i in 0..n {
        println!("iter {}/{}", i, n);
        let edge_i = graph.edge_list[i];
        for j in i + 1..n {
            println!("  subiter {}/{}", j, n);
            let edge_j = graph.edge_list[j];
            for k in j + 1..n {
                let edge_k = graph.edge_list[k];
                let cut = [edge_i, edge_j, edge_k];
                let flooded = graph.flood(0, cut);
                if flooded < graph.size {
                    println!("Found! {}", flooded);
                    println!("Solution: {}", flooded * (graph.size - flooded));
                    return;
                }
            }
        }
    }
}
