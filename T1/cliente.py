import socket
import pickle

def read_option():
	valid_options = ["piedra", "papel", "tijera"]
	print("===========================\n")
	print(f'Las opciones validas son {valid_options[0]}, {valid_options[1]} y {valid_options[2]}\n')
	option = ""
	while option not in valid_options:
	    option = input("Ingrese la jugada: ")
	    if option not in valid_options:
	        print("Opción Inválida intentalo de nuevo")
	return option

def cliente(cliente_socket, action):
	flag = True
	while flag:
		cliente_socket.send(action.encode(encoding="utf-8", errors="ignore"))
		response = cliente_socket.recv(1024)
		print(response)
		if response.decode("utf-8") == "TRUE":
			print("El servidor está disponible\n")
			print("Comenzando el juego\n")
			while True:
				option = read_option()
				print(f"\nUsted jugó {option}")
				cliente_socket.send(option.encode(encoding="utf-8", errors="ignore"))
				response = cliente_socket.recv(1024)
				d_response = pickle.loads(response)
				print(f'El bot jugó: {d_response["bot"]}\n')
				if d_response["round_winner"] == "empate":
					print("Esta ronda fue empate")
				else:
					print(f'El ganador de esta ronda fue {d_response["round_winner"]}')

				print(f'El marcador actual es jugador: {d_response["score_board"]["cliente"]}, bot: {d_response["score_board"]["bot"]}\n')

				if d_response["score_board"]["cliente"] == 3:
					print('El ganador de esta partida fue usted')
					flag = False
					break
				elif d_response["score_board"]["bot"] == 3:
					print('El ganador de esta partida fue el bot')
					flag = False
					break

		elif response.decode("utf-8") == "CLOSE":
			print("Apagando servidor\n")
			break
		else:
			print("El servidor no está disponible\n")
			break


# Intermediate server connection
host = "LocalHost"
port = 50000
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente_socket.connect((host, port))

while True:
	print("------------------------------------")
	print("Juagar cachipún?\n")
	print("1. Si\n2. No\n3.Terminar ejecución")
	inicio = input("Ingresa la opción: ")
	if inicio == '1':#falta hacer la consulta de disponibilidad del server al intermedio
	    cliente(cliente_socket, "REQCON")
	elif inicio == '2':
		continue
	elif inicio == '3':
		cliente(cliente_socket, "CLOSE")
		break
	else:
		print("Ingresa una opcioón válida\n")
    