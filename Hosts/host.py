from sys import argv as args
from app import App
from threading import Thread
from os import getenv

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


if(id == 1):
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.0.4")
    wait = input("Espere todos os binds terminarem")
    '''
    wait = input("Binds finalizados")
    app.server_sockets[ip[SRC][NEXT]].sendto("Oi testando".encode(), (ip[DST][NEXT], 8000))
    print("enviado")
    '''
    print("enviando mensagem...")
    app.send_message_next("Olá a mensagem chegou?")
    print("mensagem enviada")
    

elif (id == 2):
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.1.4")
    wait = input("Espere todos os binds terminarem")
    '''
    wait = input("Binds finalizados")
    messagem, a = app.server_sockets[ip[SRC][PREV]].recvfrom(4096)
    print(messagem.decode())
    print("recebida")
    '''

    print("recebendo mensagem...")
    mensagem = app.receive_from_prev()
    print(f"mensagem recebida: {mensagem}")
    

elif (id == 3):
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.2.4")
    wait = input("Espere todos os binds terminarem")

elif (id == 4):
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.3.4")
    wait = input("Espere todos os binds terminarem")

elif (id == 5):
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.4.4")
    wait = input("Espere todos os binds terminarem")

else:   
    app = App((ip[SRC][PREV], ip[SRC][NEXT]), (ip[DST][PREV], ip[DST][NEXT]), "192.168.5.4")
    wait = input("Espere todos os binds terminarem")

wait = input("Enter to end")
app.kill_both()