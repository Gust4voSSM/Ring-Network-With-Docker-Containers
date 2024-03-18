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
_ = input("aperte enter para sair\n")
