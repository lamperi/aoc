package main

import (
	"container/ring"
	"fmt"
)

func solve(input []int) int {
	even := ring.New(2)
	even.Value = 3
	odd := even.Next()
	odd.Value = 7
	last := odd

	recipes := 2
	inputMatch := 0
	for {
		cur := even.Value.(int) + odd.Value.(int)
		var iter []int
		if cur >= 10 {
			iter = []int{cur / 10, cur % 10}
		} else {
			iter = []int{cur}
		}
		for index := 0; index < len(iter); index++ {
			nr := ring.New(1)
			nr.Value = iter[index]
			last.Link(nr)
			last = last.Next()
			recipes++

			if last.Value.(int) == input[inputMatch] {
				inputMatch++
				if inputMatch == len(input) {
					return recipes - len(input)
				}
			} else if last.Value.(int) == input[0] {
				inputMatch = 1
				if inputMatch == len(input) {
					return recipes - len(input)
				}
			} else {
				inputMatch = 0
			}
		}

		evenTarget := even.Value.(int) + 1
		for i := 0; i < evenTarget; i++ {
			even = even.Next()
		}
		oddTarget := odd.Value.(int) + 1
		for i := 0; i < oddTarget; i++ {
			odd = odd.Next()
		}
	}
}

func main() {
	fmt.Println(solve([]int{5, 1, 5, 8, 9}), 9)
	fmt.Println(solve([]int{0, 1, 2, 4, 5}), 5)
	fmt.Println(solve([]int{9, 2, 5, 1, 0}), 18)
	fmt.Println(solve([]int{5, 9, 4, 1, 4}), 2018)
	fmt.Println(solve([]int{8, 6, 4, 8, 0, 1}))

}
