import socket
from random import choice
import pickle

# Parametros: dos strings correspondientes a las jugadas del cliente y del bot respectivamente
# Return: 0 si es empate, 1 si gana el cliente y 2 si gana el bot
def cachipun(jugada1, jugada2):
    jugadas = {
            "piedra": {"papel": 2, "tijera": 1, "piedra": 0},
            "papel": {"papel": 0, "tijera": 2, "piedra": 1},
            "tijera": {"papel": 1, "tijera": 0, "piedra": 2}
            }
    return jugadas[jugada1][jugada2]

def bot_req_game():
    #bot connection
    host = "LocalHost"
    bot_port = 50001
    bot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        bot_socket.connect((host, bot_port))
        bot_socket.send("REQCON".encode(encoding="utf-8", errors="ignore"))
        response = bot_socket.recv(1024)
        bot_socket.close()
        return response.decode("utf-8")
    except:
        print("Error al conectar a go")

def shut_down_bot():
    host = "LocalHost"
    bot_port = 50001
    bot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bot_socket.connect((host, bot_port))
    bot_socket.send("CLOSE".encode(encoding="utf-8", errors="ignore"))

def game(active_client, game_port):
    print("Iniciando partida\n")
    host = "LocalHost"
    bot_port = int(game_port[1:])
    bot_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bot_socket.connect((host, bot_port))

    score_board = {"cliente": 0, "bot": 0}

    while True:
        winner = ["empate", "usted", "el bot"]
        client_option = active_client.recv(1024)
        print("Cliente: ", client_option.decode("utf-8"))

        bot_socket.send("REQPLAY".encode(encoding="utf-8", errors="ignore"))
        response = bot_socket.recv(1024)
        print("Bot: ", response.decode("utf-8"))

        win = cachipun(client_option.decode("utf-8"), response.decode("utf-8"))
        if win == 1:
            score_board["cliente"] += 1
        elif win == 2:
            score_board["bot"] += 1

        msg = f"{response.decode('utf-8')},{winner[win]},cliente:{score_board['cliente']};bot:{score_board['bot']}"
        
        print(msg)
        active_client.send(msg.encode(encoding="utf-8", errors="ignore"))
        if 3 in score_board.values():
            bot_socket.send("ENDPLAY".encode(encoding="utf-8", errors="ignore"))
            break


def client_socket():
    host = "LocalHost"

    client_port = 50000

    #intermediate server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind((host, client_port))
    client_socket.listen(1)
    active_client, address = client_socket.accept()
    while True:
        client_option = active_client.recv(1024)

        if client_option.decode("utf-8") == "REQCON":
            bot_status = bot_req_game().split(",")
            if bot_status[0] == "TRUE":
                print("Servidor cachipún disponible\n")
                print(bot_status[1])
                active_client.send(bot_status[0].encode(encoding="utf-8", errors="ignore"))
                game(active_client, bot_status[1])
            else:
                print("Servidor no disponible\n")
                active_client.send(bot_status[0].encode(encoding="utf-8", errors="ignore"))

        elif client_option.decode("utf-8") == "CLOSE":
            active_client.send(client_option)
            active_client.close()
            shut_down_bot()
            print("Apagando servidor\n")
            exit()

client_socket()

