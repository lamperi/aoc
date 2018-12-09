package main

import (
	"container/list"
	"fmt"
)

func solve(players, maxMarble int) int {
	var marbles list.List
	scores := make([]int, players)
	marbles.PushBack(0)
	it := marbles.Front()
	for marble := 1; marble <= maxMarble; marble++ {
		if marble%23 == 0 {
			for i := 0; i < 7; i++ {
				it = it.Prev()
				if it == nil {
					it = marbles.Back()
				}
			}
			remove := it
			it = it.Next()
			if it == nil {
				it = marbles.Front()
			}
			popped := marbles.Remove(remove).(int)
			p := marble % players
			scores[p] = scores[p] + marble + popped
		} else {
			for i := 0; i < 2; i++ {
				it = it.Next()
				if it == nil {
					it = marbles.Front()
				}
			}
			it = marbles.InsertBefore(marble, it)
		}
	}
	max := 0
	for _, score := range scores {
		if score > max {
			max = score
		}
	}
	return max
}

func main() {
	fmt.Println(solve(9, 25))

	fmt.Println(solve(10, 1618), 8317)
	fmt.Println(solve(13, 7999), 146373)
	fmt.Println(solve(17, 1104), 2764)
	fmt.Println(solve(21, 6111), 54718)
	fmt.Println(solve(30, 5807), 37305)

	fmt.Println(solve(435, 71184))
	fmt.Println(solve(435, 7118400))

}
