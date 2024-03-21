from sys import argv as args
from app import App
from threading import Thread
from os import getenv
from time import sleep

id = int(getenv("ID"))
assert id > 0

PREV, NEXT, SRC, DST = 2*[*range(2)]

prefix = "192.168"

ip = [[int,int],[int, int]] # matrix 2x2
ip[SRC][PREV] = f"{prefix}.{(id-2)%6}.3"
ip[SRC][NEXT] = f"{prefix}.{(id-1)%6}.2"
ip[DST][PREV] = f"{prefix}.{(id-2)%6}.2"
ip[DST][NEXT] = f"{prefix}.{(id-1)%6}.3"

print(f"""\
Seus IPs:      {', '.join(ip[0])}
Seus vizinhos: {', '.join(ip[1])}\
""")

app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), f"192.168.{id-1}.4")
wait = input("Espere todos os binds terminarem")

if (id == 1):
    print("enviando mensagem...")
    app.send_message_next("Olá a mensagem chegou?")
    print("mensagem enviada")
elif (id == 2):
    print("recebendo mensagem...")
    mensagem = app.receive_from_prev()
    print(f"mensagem recebida: {mensagem}")

wait = input("Enter to end")
app.kill_both()