# Ring-Network-With-Docker-Containers
Rede de conteineres docker com topologia em anel. Projeto de Infraestrutura de Comunicação do curso de Ciência da Computação da UFPE

## Docker
Tanto os containers quanto as redes são gerados através do arquivo [compose.yaml](./compose.yaml). Não é necessário realizar builds por comando para gerar as imagens, pois desde que haja conexão com a internet, o compose busca as imagens de um repositório remoto e as instala, builds locais tem privilégio sobre as imagens salvas em repositório, porque o compose busca pela tag `latest`.

### Containres
Foram usadas duas imagens baseadas em python:3.10-alpine. uma para os [nós da rede](https://hub.docker.com/r/gust4vossm/hosts), e outra para a [autoridade certificadora](https://hub.docker.com/r/gust4vossm/auth). Ambas as imagens estão disponíveis no repositorio Docker Hub.

### Redes Docker
Para a rede em topologia de anel foram criadas 6 subredes (route-1, route-2 ... route-6) representando as conexões entre os nós. Cada rota possúi um par de hosts mais a autoridade certificadora, que [está presente em todas as redes](./compose.yaml#L8-L20)

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

    route-5:
        internal: true
        ipam:
            config:
            -   subnet: 192.168.4.0/24
    route-6:
        internal: true
        ipam:
            config:
            -   subnet: 192.168.5.0/24

```
