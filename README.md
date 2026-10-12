# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Nome do projeto

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/thiago-bernardo-dos-santos-43a904280/">Thiago Bernardo dos Santos - RM576903</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Tutor</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/inova-fusca">Nome do Coordenador</a>


## 📜 Descrição

### Contexto do agronegócio

O agronegócio reúne todas as atividades econômicas ligadas à produção e à comercialização de produtos agrícolas, da fabricação de insumos e máquinas até a distribuição ao consumidor final. É um dos setores que mais geram empregos no Brasil, base da *supply chain* e também um dos que mais investem em inovação e tecnologia, como inteligência artificial, geolocalização e sistemas de gestão. Nesse cenário crescem as *agrotechs*, startups que desenvolvem ferramentas para que o produtor monitore seu negócio e decida com base em dados.

### A dor escolhida: perdas na colheita da cana-de-açúcar

O Brasil é líder mundial na produção de cana-de-açúcar, com cerca de 620 milhões de toneladas por safra. Apesar do volume, as perdas na colheita são muito altas. Segundo a SOCICANA, podem chegar a **15% na colheita mecanizada**, enquanto na colheita manual raramente passam de **5%**. Considerando a área plantada em São Paulo, isso representa um prejuízo milionário por ano para o setor. Muitos produtores, porém, não registram nem quantificam essas perdas por talhão, e sem esse dado não sabem onde estão perdendo dinheiro nem o que corrigir.

### A solução: CanaSafe

O CanaSafe é uma aplicação em Python, executada via prompt de comando, que ajuda o produtor a medir, entender e reduzir as perdas da colheita. O sistema:

1. **Registra** cada colheita: talhão, safra, área, produtividade, tipo de colheita (manual ou mecânica) e percentual de perda medido;
2. **Calcula** a perda em toneladas e em reais;
3. **Classifica** a perda como *adequada*, *atenção* ou *crítica*, comparando com o limite de cada tipo de colheita;
4. **Recomenda** ações de melhoria: planejamento do plantio à colheita, definição do momento ideal de colheita, calibragem das colhedoras e treinamento dos operadores;
5. **Armazena** os dados em banco **Oracle**, permite **exportar e ler JSON** e gera um **relatório em TXT**.

### Inovação

O diferencial é transformar o dado bruto em diagnóstico e plano de ação por talhão. Em vez de só guardar números, o sistema aponta o nível de risco e o que fazer, apoiando a decisão do produtor, como uma agrotech faz com suas ferramentas.

### Conteúdos de Python aplicados

A solução usa subalgoritmos (funções e procedimentos com passagem de parâmetros), estruturas de dados (lista, tupla, dicionário e tabela de memória), manipulação de arquivos texto e JSON e conexão com banco Oracle. Todas as entradas do usuário são validadas, para impedir tipos indesejados e proteger a integridade da base de dados, e os resultados são exibidos em tabelas organizadas para facilitar a leitura.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens (logo da FIAP).

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto. Neste projeto, as credenciais do Oracle não ficam em arquivo: são informadas no terminal ou por variáveis de ambiente.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Aqui está o `create_tables.sql`, com o comando de criação da tabela `COLHEITA_CANA` no Oracle (o programa também cria a tabela automaticamente na primeira execução).

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto:
  - `main.py`: menu e fluxo principal. **É o arquivo que deve ser executado.**
  - `regras.py`: cálculo das perdas, classificação (adequada, atenção, crítica) e recomendações.
  - `entrada.py`: leitura e validação dos dados digitados pelo usuário.
  - `db.py`: conexão com o Oracle e operações de inserir, listar, atualizar e remover.
  - `arquivos.py`: manipulação de arquivos JSON e TXT.
  - `requirements.txt`: dependências do projeto.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Pré-requisitos

- **Python** 3.11 ou superior
- **Biblioteca** `oracledb` (instalada pelo `requirements.txt`)
- **Banco de dados Oracle** com usuário e senha fornecidos pela FIAP
- **Rede** com acesso ao servidor Oracle (a FIAP pode exigir VPN ou rede da faculdade)
- **IDE** (opcional): Visual Studio Code ou outra de sua preferência

### Passo a passo

1. **Baixe o código** clonando o repositório:
   ```bash
   git clone https://github.com/thiagobernardosantos/fiap-agro-canasafe.git
   ```

2. **Entre na pasta do código-fonte:**
   ```bash
   cd fiap-agro-canasafe/src
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Opcional) Configure as credenciais do Oracle** por variáveis de ambiente. Se pular esta etapa, o programa pede usuário e senha no terminal.

   Windows (CMD):
   ```bash
   set ORACLE_USER=seu_usuario
   set ORACLE_PASSWORD=sua_senha
   set ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
   ```

   Linux/macOS:
   ```bash
   export ORACLE_USER=seu_usuario
   export ORACLE_PASSWORD=sua_senha
   export ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
   ```

5. **Execute o programa:**
   ```bash
   python main.py
   ```

6. **Use o menu** para registrar colheitas, listar, atualizar, remover, gerar o relatório (TXT) e exportar ou ler o JSON.

### Exemplo de teste

Na opção **1 - Registrar colheita**, informe: talhão `T01`, safra `2025/26`, área `10`, produtividade `100`, tipo `MECANICA` e perda `20`. O resultado esperado é uma perda de **200 t (≈ R$ 30.000,00)**, status **ATENCAO** e as recomendações de melhoria.

### Observações

- Na primeira execução, a tabela `COLHEITA_CANA` é criada automaticamente.
- Os arquivos `dados_colheita.json` e `relatorio_perdas.txt` são gerados na pasta em que o programa é executado.
- O preço de referência da tonelada (R$ 150) pode ser alterado em `src/regras.py`.



## 🗃 Histórico de lançamentos

* 0.1.0 - 12/10/2026
    *

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


