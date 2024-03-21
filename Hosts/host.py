from sys import argv as args
from app import App
from threading import Thread
from os import getenv

mensagem = ""

def enviando(app : App):
    global mensagem 
    mensagem = input("")

    while mensagem != "sair":
        quem = input("Para qual host quer mandar? ")
        app.send_message_to(mensagem, host[quem])
        mensagem = input("")
        
    
def recebendo_atras(app : App):
    global mensagem

    while mensagem != "sair":
        message = app.receive_message_prev()
        if message != "FOWARDING":
            print(f"-Mensagem recebida: {message}")

def recebendo_frente(app : App):
    global mensagem

    while mensagem != "sair":
        message = app.receive_message_next()
        if message != "FOWARDING":
            print(f"\n-Mensagem recebida: {message}")


id = int(getenv("ID"))
assert id > 0
host = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6}

PREV, NEXT, SRC, DST = 2*[*range(2)]

prefix = "192.168"

ip = [[int,int],[int, int]] # matrix 2x2
ip[SRC][PREV] = f"{prefix}.{(id-2)%6}.3"
ip[SRC][NEXT] = f"{prefix}.{(id-1)%6}.2"
ip[DST][PREV] = f"{prefix}.{(id-2)%6}.2"
ip[DST][NEXT] = f"{prefix}.{(id-1)%6}.3"

print(f"""\
Seus IPs:      {'e '.join(ip[0])}
Seus vizinhos: {'e '.join(ip[1])}\
""")

app = App(id, (ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.167.423")
wait = input("Enter to start")

enviar = Thread(target=enviando, args=[app])
receber_1 = Thread(target=recebendo_frente, args=[app])
receber_2 = Thread(target=recebendo_atras, args=[app])

enviar.start()
receber_1.start()
receber_2.start()


enviar.join()
receber_1.join()
receber_2.join()
app.kill_both()