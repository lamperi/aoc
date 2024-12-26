use std::{cmp::{Ordering, Reverse}, collections::{BinaryHeap, HashSet}, fmt::Debug, hash::Hash};

use indexmap::{map::Entry, IndexMap};
use num::Zero;


pub fn dijkstra<State, Cost, F1, F2>(init_state: State, is_end: F1, edges: F2) -> Option<Cost>
where
    State: Hash + Ord + Copy,
    Cost: Ord + Copy + Zero,
    F1: Fn(&State) -> bool,
    F2: Fn(&State) -> Vec<(Cost, State)>
{
    let mut heap: BinaryHeap<(Reverse<Cost>, usize)> = BinaryHeap::new();
    // Heap: contains (Reverse(points), state).
    // Reverse is used because BinaryHeap is a max-heap.
    heap.push((Reverse(Zero::zero()), 0));

    // Prune states already visited.
    let mut visited_states: IndexMap<State, (Cost, usize)>  = IndexMap::new();
    visited_states.insert(init_state, (Zero::zero(), 0));

    while let Some((Reverse(cost), index)) = heap.pop() {
        let (node, _) = visited_states.get_index(index).unwrap();
        if is_end(node) {
            return Some(cost)
        }
        for (edge_cost, state) in edges(node) {
            let cost = cost + edge_cost;
            match visited_states.entry(state) {
                Entry::Vacant(v) => {
                    heap.push((Reverse(cost), v.index()));
                    v.insert((cost, index));
                },
                Entry::Occupied(mut o) => {
                    if cost < o.get().0 {
                        o.insert((cost, index));
                        heap.push((Reverse(cost), o.index()));
                    }
                }
            }
        }
    }
    None
}

pub fn dijkstra_equal_paths<State, Cost, F1, F2>(init_state: State, is_end: F1, edges: F2) -> Option<(Cost, Vec<State>)>
where
    State: Hash + Ord + Copy + Debug,
    Cost: Ord + Copy + Zero,
    F1: Fn(&State) -> bool,
    F2: Fn(&State) -> Vec<(Cost, State)>
{
    let mut heap: BinaryHeap<(Reverse<Cost>, usize)> = BinaryHeap::new();
    // Heap: contains (Reverse(points), state).
    // Reverse is used because BinaryHeap is a max-heap.
    heap.push((Reverse(Zero::zero()), 0));

    // Prune states already visited.
    let mut visited_states: IndexMap<State, (Cost, Vec<usize>)>  = IndexMap::new();
    visited_states.insert(init_state, (Zero::zero(), vec![]));
    let mut end_index = HashSet::new();
    let mut end_cost = None;

    while let Some((Reverse(cost), index)) = heap.pop() {
        let (node, _) = visited_states.get_index(index).unwrap();
        if end_cost.is_some_and(|end_cost| end_cost < cost) {
            continue
        }
        if is_end(node) {
            if end_cost.is_none() || end_cost.is_some_and(|end_cost| end_cost > cost) {
                end_index.clear();
                end_cost = Some(cost);
                end_index.insert(index);
            }
            end_index.insert(index);
            continue
        }
        for (edge_cost, state) in edges(node) {
            let cost = cost + edge_cost;
            match visited_states.entry(state) {
                Entry::Vacant(v) => {
                    heap.push((Reverse(cost), v.index()));
                    v.insert((cost, vec![index]));
                },
                Entry::Occupied(mut o) => {
                    match cost.cmp(&o.get().0) {
                        Ordering::Less => {
                            o.insert((cost, vec![index]));
                            heap.push((Reverse(cost), o.index()));
                        },
                        Ordering::Equal => {
                            o.get_mut().1.push(index);
                        },
                        Ordering::Greater => {}
                    }
                }
            }
        }
    }
    end_cost.map(|cost| {
        let mut visited_indices = HashSet::new();
        let mut stack = Vec::new();
        stack.extend(end_index.iter());
        visited_indices.extend(end_index);
        let mut visited_nodes = vec![];
        while let Some(index) = stack.pop() {
            let (node, (_, parents)) = visited_states.get_index(index).unwrap();
            visited_nodes.push(*node);
            for parent in parents {
                if visited_indices.insert(*parent) {
                    stack.push(*parent);
                }
            }
        }
        (cost, visited_nodes)
    })
}