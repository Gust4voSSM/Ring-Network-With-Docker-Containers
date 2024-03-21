from sys import argv as args
from app import App
from threading import Thread
from os import getenv

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
mensagem = ""

if(id == host['A']):
    mensagem = "Olá, a mensagem chegou?"
    app.send_message_to(mensagem, host['C'])
    print(f"mensagem enviada {mensagem}")

elif (id == host['B']):
    mensagem = app.receive_message_prev()
    print(f"mensagem recebida {mensagem}")

elif (id == host['C']):
    mensagem = app.receive_message_prev()
    print(f"mensagem recebida {mensagem}")

app.kill_both()