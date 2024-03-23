# Ring-Network-With-Docker-Containers
Rede de conteineres docker com topologia em anel. Projeto de Infraestrutura de Comunicação do curso de Ciência da Computação da UFPE

## Instruções de uso
1. Clone o repositório;
2. Abra um terminal no diretorio raiz do projeto e execute o comando `docker compose up -d`. Serão criados os containers e as redes, e cada container vai lançar um bash em modo desanexado;
3. Para anexar ao terminal de um nó, utilize o comando `docker attach ring-network-with-docker-containers-host-{L}-1` substitua {L} pela letra do nó (A, B, C, ..., F) para conectar-se a ele;
4. Anexe o terminal do primeiro nó, digite o comando `python host.py`, e os sockets do nó irão fazer bind nos IPs e porta, (NÃO DIGITE ENTER NEM FECHE O TERMINAL);
5. Para cada um dos outros nós, abra um novo terminal (`Ctr+Shift+'` no Vscode) e repita o passo 4;
7. Em outro terminal, anexe ao terminal da autoridade certificadora com o comando `docker attach ring-network-with-docker-containers-auth-1`;
8. Digite o comando `python auth.py`, e os sockets da autoriadade farão bind nos IPs e porta;
9. Volte para os terminais dos nós e digite enter duas vezes para cada um dos terminais;
10. Pront! Agora você pode usar os terminais livremente. Cada terminal é um nó, capaz de enviar e receber mensagens.

### Observação
Em caso de `OS error`, desfaça a rede e os nós com `docker compose down` espere alguns minutos e crie novamente com `docker compose up -d`

## Docker
Tanto os containers quanto as redes são gerados através do arquivo [compose.yaml](./compose.yaml). Não é necessário realizar builds por comando para gerar as imagens, pois desde que haja conexão com a internet, o compose busca as imagens de um repositório remoto e as instala, builds locais tem privilégio sobre as imagens salvas em repositório, porque o compose busca pela tag `latest`.

### Containers
Foram usadas duas imagens baseadas em python:3.10-alpine. uma para os [nós da rede](https://hub.docker.com/r/gust4vossm/hosts), e outra para a [autoridade certificadora](https://hub.docker.com/r/gust4vossm/auth). Ambas as imagens estão disponíveis no repositorio Docker Hub.

### Redes Docker
A rede utilizadé é a rede 192.168.0/16, possuindo 6 subredes para a topologia em anel (route-1, route-2 ... route-6) representando as conexões entre os nós. Cada rota possúi um par de hosts mais a autoridade certificadora, que [está presente em todas as redes](./compose.yaml#L8-L20). Para a máscara das subredes usou se /24 por simplicidade, já que o terceiro e o quarto octeto são usados para subnetid e hostid, respectivamente, facilitando a leitura. A rota n tem o endereço de subrede 192.168.{n-1}.0/24

```yaml
networks: 
    route-1:
        internal: true
        ipam:
            config:
            -   subnet: 192.168.0.0/24
    route-2:
        internal: true
        ipam:
            config:
            -   subnet: 192.168.1.0/24

# (...)

    route-6:
        internal: true
        ipam:
            config:
            -   subnet: 192.168.5.0/24
```
Desta forma, cada nó possui duas interfaces (e portanto, [dois IPs](./compose.yaml#L27#L31)) e só consegue se comunicar com duas subredes, cada qual contendo um nó vizinho e a autoridade certificadora. Já a autoridade certificadora possúi [6 interfaces](./compose.yaml#L8-L20), comunicando se com todos os nós. Para simplificar o entendimento, a autoridade sempre usa 4 como hostid em todas os seus ips e os nós sempre usam 2 e 3 respectivamente, como hostids nos ips de interface anterior e posterior.
