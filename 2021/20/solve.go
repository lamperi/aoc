package main

import (
	"log"
	"os"
	"strings"
)

type point struct {
	y int
	x int
}
type problem struct {
	enchancement []uint8
	image        map[point]uint8
	maxPoint     point
}

func parse(bytes []byte) *problem {
	lines := strings.Split(string(bytes), "\n")
	image := make(map[point]uint8)
	for y, line := range lines[2:] {
		for x, c := range line {
			if c == '#' {
				image[point{y, x}] = uint8(1)
			}
		}
	}
	enchancement := make([]uint8, len(lines[0]))
	for i, c := range lines[0] {
		if c == '#' {
			enchancement[i] = uint8(1)
		}
	}
	return &problem{
		enchancement: enchancement,
		image:        image,
		maxPoint:     point{y: len(lines) - 2, x: len(lines[2])},
	}
}

func parseFromFile() (*problem, error) {
	bytes, err := os.ReadFile("2021/20/input.txt")
	if err != nil {
		return nil, err
	}
	prob := parse(bytes)
	return prob, nil
}

func runImage(prob problem, maxT int) uint32 {
	defaultFill := uint8(0)
	for t := 0; t < maxT; t++ {
		image := make(map[point]uint8)
		for y := 0; y < prob.maxPoint.y+2; y++ {
			for x := 0; x < prob.maxPoint.x+2; x++ {
				val := uint16(0)
				shift := uint16(8)
				for yd := -2; yd <= 0; yd++ {
					for xd := -2; xd <= 0; xd++ {
						v, exist := prob.image[point{y: y + yd, x: x + xd}]
						if !exist {
							v = defaultFill
						}
						val |= uint16(v) << shift
						shift -= 1
					}
				}
				if val != uint16(defaultFill) {
					image[point{y, x}] = prob.enchancement[val]
				}
			}
		}
		if prob.enchancement[0] == 1 {
			if defaultFill == 0 {
				defaultFill = 1
			} else {
				defaultFill = 0
			}
		}
		prob.image = image
		prob.maxPoint.y += 2
		prob.maxPoint.x += 2
	}
	s := uint32(0)
	for _, c := range prob.image {
		s += uint32(c)
	}
	log.Printf("after t=%d we have %d lit pixels", maxT, s)
	return s

}

const testBytes = `..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###`

func main() {
	test := parse([]byte(testBytes))
	runImage(*test, 2)
	runImage(*test, 50)

	prob, err := parseFromFile()
	if err != nil {
		log.Fatalf("failed to parse input: %v", err)
	}
	runImage(*prob, 2)
	runImage(*prob, 50)
}
