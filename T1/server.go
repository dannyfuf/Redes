package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
)

func main() {
	port := ":50001"
	buffer_size := 1024
	s, err := net.ResolveUDPAddr("udp4", port)
	if err != nil {
		fmt.Println(err)
		return
	}
	connection, err := net.ListenUDP("udp4", s)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer connection.Close()
	buffer := make([]byte, buffer_size)

	var randomIndex int
	var pick string
	game_options := [3]string{"piedra", "papel", "tijera"}
	for {
		n, addr, err := connection.ReadFromUDP(buffer)
		if string(buffer[0:n]) == "REQCON" {
			randInt := rand.Intn(100)
			if randInt%2 == 0 {
				
				// New socket for game
				n_port := rand.Intn(10000)
				tmp := 50000+n_port
				port_game := ":"+strconv.Itoa(tmp)
				
				fmt.Printf("Game Port: %s", port_game)
				_, err = connection.WriteToUDP([]byte("TRUE,"+port_game), addr)
				
				s1, err1 := net.ResolveUDPAddr("udp4", port_game)
				if err1 != nil {
					fmt.Println(err1)
					return
				}
				connection_game, err1 := net.ListenUDP("udp4", s1)
				if err1 != nil {
					fmt.Println(err1)
					return
				}
				defer connection_game.Close()
				buffer_game := make([]byte, buffer_size)
				//------------------------------------------
				if err != nil {
					fmt.Println(err)
					return
				}
				for{
					n_game, addr_game, err_game := connection_game.ReadFromUDP(buffer_game)
					if string(buffer_game[0:n_game]) == "REQPLAY" {
						randomIndex = rand.Intn(1000)%3
						pick = game_options[randomIndex]
						fmt.Printf("Jugada: %s \n", pick)
						_, err_game = connection_game.WriteToUDP([]byte(pick), addr_game)
						if err != nil {
							fmt.Println(err_game)
							return
						}
					} else {
						fmt.Println("Partida Terminada\n")
						break
					}

				}
			} else {
				fmt.Println("Servidor no disponible\n")
				_, err = connection.WriteToUDP([]byte("FALSE"), addr)
				if err != nil {
					fmt.Println(err)
					return
				}
			}
		} else if string(buffer[0:n]) == "CLOSE" {
			fmt.Println("Apagando servidor\n")
			break
		}
	}
}
