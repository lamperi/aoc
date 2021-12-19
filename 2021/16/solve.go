package main

import (
	"log"
	"math/big"
	"os"
	"strconv"
	"strings"
)

type Bitset struct {
	bits *big.Int
	i    int
	len  int
}

func (b *Bitset) reset() {
	b.i = 0
}

func (b *Bitset) readUint8(length int) uint8 {
	if b.i >= b.len {
		log.Fatalf("trying to read out of bounds")
	}
	r := uint8(0)
	for i := 0; i < length; i++ {
		r |= uint8(b.bits.Bit(b.i+i) << (length - i - 1))
	}
	b.i += length
	return r
}

func (b *Bitset) readUint16(length int) uint16 {
	if b.i >= b.len {
		log.Fatalf("trying to read out of bounds")
	}
	r := uint16(0)
	for i := 0; i < length; i++ {
		r |= uint16(b.bits.Bit(b.i+i) << (length - i - 1))
	}
	b.i += length
	return r
}

func (b *Bitset) index() int {
	return b.i
}

func fromHexBytes(hex []byte) (*Bitset, error) {
	hexStr := strings.TrimSpace(strings.ToLower(string(hex)))
	bits := big.NewInt(0)
	for i, c := range hexStr {
		ui, err := strconv.ParseUint(string(c), 16, 8)
		if err != nil {
			return nil, err
		}
		for j := 0; j < 4; j++ {
			idx := 4*i + j
			bit := uint(ui>>(3-j)) & 1
			bits.SetBit(bits, idx, bit)
		}
	}
	return &Bitset{
		bits: bits,
		i:    0,
		len:  len(hexStr) * 4,
	}, nil
}

func parse() (*Bitset, error) {
	bytes, err := os.ReadFile("input.txt")
	if err != nil {
		return nil, err
	}
	bs, err := fromHexBytes(bytes)
	if err != nil {
		return nil, err
	}
	return bs, nil
}

type packet struct {
	version    uint8
	packetType uint8
	value      uint64
	children   []*packet

	numChildren int
	endIndex    int
	curChildren int
}

func (p *packet) countVersionSum() int {
	s := int(p.version)
	for _, c := range p.children {
		s += c.countVersionSum()
	}
	return s
}

// No recursion version
func countVersionSum(p *packet) int {
	s := int(p.version)
	var stack []*packet
	stack = append(stack, p)
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		if top.curChildren < len(top.children) {
			newTop := top.children[top.curChildren]
			s += int(newTop.version)
			stack = append(stack, newTop)
			top.curChildren += 1
		} else {
			stack = stack[:len(stack)-1]
		}
	}
	return s
}

func (p *packet) evaluate() int {
	r := 0
	switch p.packetType {
	case 0:
		for _, c := range p.children {
			r += c.evaluate()
		}
	case 1:
		r = 1
		for _, c := range p.children {
			r *= c.evaluate()
		}
	case 2:
		for i, c := range p.children {
			if i == 0 {
				r = c.evaluate()
			} else {
				v := c.evaluate()
				if v < r {
					r = v
				}
			}
		}
	case 3:
		for i, c := range p.children {
			if i == 0 {
				r = c.evaluate()
			} else {
				v := c.evaluate()
				if v > r {
					r = v
				}
			}
		}
	case 4:
		r = int(p.value)
	case 5:
		if p.children[0].evaluate() > p.children[1].evaluate() {
			r = 1
		}
	case 6:
		if p.children[0].evaluate() < p.children[1].evaluate() {
			r = 1
		}
	case 7:
		if p.children[0].evaluate() == p.children[1].evaluate() {
			r = 1
		}
	}
	return r
}

func readPacket(bs *Bitset) packet {
	v := bs.readUint8(3)
	t := bs.readUint8(3)
	if t == 4 {
		val := uint64(0)
		for ok := true; ok; {
			ok = bs.readUint8(1) == 1
			val = val << 4
			next := bs.readUint8(4)
			val |= uint64(next)
		}
		return packet{
			version:    v,
			packetType: t,
			value:      val,
		}
	} else {
		var children []*packet
		lengthType := bs.readUint8(1)
		if lengthType == 0 {
			totalLength := int(bs.readUint16(15))
			startIndex := bs.index()
			for bs.index() < startIndex+totalLength {
				p := readPacket(bs)
				children = append(children, &p)
			}
		} else {
			numberChild := bs.readUint16(11)
			for i := uint16(0); i < numberChild; i++ {
				p := readPacket(bs)
				children = append(children, &p)
			}
		}
		return packet{
			version:    v,
			packetType: t,
			children:   children,
		}
	}
}

func readPacketNoRecursion(bs *Bitset) packet {
	var stack []*packet
	for {
		v := bs.readUint8(3)
		t := bs.readUint8(3)
		packet := &packet{}
		packet.version = v
		packet.packetType = t
		if len(stack) > 0 {
			stack[len(stack)-1].children = append(stack[len(stack)-1].children, packet)
		}
		if t == 4 {
			val := uint64(0)
			for ok := true; ok; {
				ok = bs.readUint8(1) == 1
				val = val << 4
				next := bs.readUint8(4)
				val |= uint64(next)
			}
			packet.value = val
		} else {
			lengthType := bs.readUint8(1)
			if lengthType == 0 {
				packet.endIndex = int(bs.readUint16(15)) + bs.index()
			} else {
				packet.numChildren = int(bs.readUint16(11))
			}
			stack = append(stack, packet)
		}
		for len(stack) > 0 {
			packet = stack[len(stack)-1]
			if packet.numChildren > 0 && len(packet.children) == packet.numChildren {
				stack = stack[:len(stack)-1]
			} else if packet.endIndex > 0 && bs.index() == packet.endIndex {
				stack = stack[:len(stack)-1]
			} else {
				break
			}
		}
		if len(stack) == 0 {
			return *packet
		}
	}
}

func test() {
	// test 1
	bs, _ := fromHexBytes([]byte("D2FE28"))
	p := readPacket(bs)
	if p.value != 2021 {
		log.Fatalf("test packet: %v, expected value=2021", p)
	}
	bs.reset()
	p = readPacketNoRecursion(bs)
	if p.value != 2021 {
		log.Fatalf("test packet: %v, expected value=2021", p)
	}
	// test 2
	bs, _ = fromHexBytes([]byte("8A004A801A8002F478"))
	p = readPacket(bs)
	vs := p.countVersionSum()
	if vs != 16 {
		log.Fatalf("test packet, got vs=%d, want=16", vs)
	}
	bs.reset()
	p = readPacketNoRecursion(bs)
	vs = countVersionSum(&p)
	if vs != 16 {
		log.Fatalf("test packet, got vs=%d, want=16", vs)
	}
	// test 3
	bs, _ = fromHexBytes([]byte("620080001611562C8802118E34"))
	p = readPacket(bs)
	vs = p.countVersionSum()
	if vs != 12 {
		log.Fatalf("test packet, got vs=%d, want=12", vs)
	}
	bs.reset()
	p = readPacketNoRecursion(bs)
	vs = countVersionSum(&p)
	if vs != 12 {
		log.Fatalf("test packet, got vs=%d, want=12", vs)
	}
	// test 4
	bs, _ = fromHexBytes([]byte("C0015000016115A2E0802F182340"))
	p = readPacket(bs)
	vs = p.countVersionSum()
	if vs != 23 {
		log.Fatalf("test packet, got vs=%d, want=23", vs)
	}
	bs.reset()
	p = readPacketNoRecursion(bs)
	vs = countVersionSum(&p)
	if vs != 23 {
		log.Fatalf("test packet, got vs=%d, want=23", vs)
	}
	// test 5
	bs, _ = fromHexBytes([]byte("A0016C880162017C3686B18A3D4780"))
	p = readPacket(bs)
	vs = p.countVersionSum()
	if vs != 31 {
		log.Fatalf("test packet, got vs=%d, want=31", vs)
	}
	bs.reset()
	p = readPacketNoRecursion(bs)
	vs = countVersionSum(&p)
	if vs != 31 {
		log.Fatalf("test packet, got vs=%d, want=31", vs)
	}
}

func main() {
	test()
	bs, err := parse()
	if err != nil {
		log.Fatalf("unable to continue: %v", err)
	}
	p := readPacket(bs)
	log.Printf("version sum: %d", p.countVersionSum())
	log.Printf("version sum: %d", countVersionSum(&p))
	log.Printf("evaluate: %d", p.evaluate())
}
