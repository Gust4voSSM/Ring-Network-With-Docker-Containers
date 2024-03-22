# Ring-Network-With-Docker-Containers
Rede de conteineres docker com topologia em anel. Projeto de Infraestrutura de Comunicação do curso de Ciência da Computação da UFPE

## Instruções de uso

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

*mostrar diagrama*


