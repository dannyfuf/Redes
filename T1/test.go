package main

import (
	"fmt"
	"strconv"
)

func main() {
	//game_options := [3]string{"piedra", "papel", "tijera"}
	//s1 := rand.NewSource(time.Now().UnixNano())
    //r1 := rand.New(s1)
	//fmt.Println(r1.Intn(100))
	//fmt.Println(r1.Intn(100))
	//fmt.Println(r1.Intn(100))
	//randomIndex := rand.Intn(len(game_options))
	//pick := game_options[randomIndex]
	//fmt.Println(pick)
	s := 123
	a := ":"+strconv.Itoa(s)
	fmt.Println(a)
}
