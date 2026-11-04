# Checkpoint 6 - Sistema de Triagem de Chamados de TI

Trabalho de Pensamento Computacional com Python.

## Integrantes

- Matheus Marques De Souza - RM 573203

## Descrição da solução

O programa lê os chamados do arquivo `dados/chamados.json`, decide a prioridade de cada chamado usando uma árvore de decisão e monta a fila de atendimento.

Ele tem dois menus:

1. **Painel de métricas**: total de chamados, total de usuários afetados, chamados por impacto, chamados por tipo e tempo médio estimado.
2. **Fila de atendimento**: mostra o próximo chamado a ser atendido (com o motivo da escolha) e depois os outros na ordem.

Cada chamado é um dicionário, e todos ficam em uma lista. O código está dividido em funções: leitura do arquivo, árvore de decisão, ordenação da fila, métricas e telas.

## Estratégia para definir a ordem dos chamados

Como o JSON não tem um campo de prioridade, criamos uma em duas etapas.

### 1. Árvore de decisão

Cada chamado responde a algumas perguntas e termina em um nível de prioridade de P1 (mais urgente) a P4:

```
impacto == alto?
├─ sim: tipo é Sistema ou Rede?
│   ├─ sim -> P1 Crítica
│   └─ não: usuários afetados >= 15?
│       ├─ sim -> P1 Crítica
│       └─ não -> P2 Alta
└─ não: impacto == medio?
    ├─ sim: usuários afetados >= 10?
    │   ├─ sim -> P2 Alta
    │   └─ não -> P3 Média
    └─ não (impacto baixo) -> P4 Baixa
```

Por que escolhemos essas perguntas:

- O **impacto** é a primeira pergunta porque é o que mais mostra a gravidade do problema.
- Problemas de **Sistema** e **Rede** com impacto alto vão direto para P1, porque costumam parar vários setores ao mesmo tempo. Um problema de impressora ou de um computador normalmente afeta só uma pessoa.
- Problemas de impacto alto de outros tipos (como Acesso) também viram P1 se afetam **15 usuários ou mais**.
- Um problema de impacto médio que atinge **10 usuários ou mais** (como VPN ou Wi-Fi) sobe para P2, porque atrapalha mais gente.
- Impacto baixo fica sempre em P4 (senha expirada, impressora, instalação de programa).

### 2. Desempate

Quando dois chamados ficam no mesmo nível, a ordem é:

1. o que tem **mais usuários afetados**;
2. se empatar, o que tem **mais setores afetados**;
3. se ainda empatar, o que foi **aberto primeiro** (data e hora).

A ordenação foi feita com **bubble sort**: o programa compara os chamados vizinhos da lista e troca os dois de lugar quando estão fora de ordem. A função `vem_antes` diz qual chamado deve vir primeiro seguindo as regras acima.

### Resultado

Com os 30 chamados do arquivo, ficaram 12 chamados P1, 3 P2, 5 P3 e 10 P4. O primeiro da fila é o **1019 - Banco de dados com lentidão** (impacto alto, tipo Sistema, 50 usuários e 3 setores).

## Como executar

É preciso ter o Python 3 instalado. Não precisa instalar nenhuma biblioteca.

1. Abra o terminal na pasta do projeto (`checkpoint_6`).
2. Rode:

   ```bash
   python main.py
   ```

3. Escolha uma opção no menu: `1` para o painel, `2` para a fila e `0` para sair.

O programa precisa ser executado de dentro da pasta do projeto, porque ele abre o arquivo `dados/chamados.json`.

## Arquivos

- `main.py` - código do sistema
- `dados/chamados.json` - chamados registrados
- `README.md` - documentação

Pedi para o claude revisar o README e ir deixando completo