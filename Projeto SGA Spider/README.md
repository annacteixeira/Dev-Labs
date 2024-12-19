# SGA Spider - PUC Minas 🕸

<div align="center">
    <table>
        <tr>
            <td align="center">
                <img alt="pucminas" src="https://github.com/joaopauloaramuni/joaopauloaramuni/blob/main/img/engsoft.png?raw=true" />
            </td>
        </tr>
      <tr>
        <td align="center">
          <img alt="sga-pucminas" src="https://i.ibb.co/BjQsSZT/imagem-2024-12-19-180940465.png" width="600px"/>
        </td>
      </tr>
    </table>
</div>

Este projeto é uma aplicação Python que automatiza a consulta do número máximo de faltas possíveis e realiza o somatório das notas por disciplina para estudantes de Graduação da PUC Minas. Ele utiliza web scraping para acessar o SGA e processar as informações de frequência e notas.



## Funcionalidades

- **Login Automático**: Realiza login no portal do estudante da PUC Minas.
- **Extração de Dados**:
  - Navega até a página de notas e frequência.
  - Extrai informações de disciplinas, faltas e notas.
- **Cálculo Automático**:
  - Soma as notas de cada disciplina, facilitando a visualização do desempenho total.
- **Exportação**:
  - Gera um arquivo `faltas.json` com informações de frequência e notas.

## Requisitos

- Python 3.8 ou superior
- Bibliotecas necessárias:
  - `requests`
  - `beautifulsoup4`
  
Você pode instalar as dependências com o comando:
```bash
pip install requests beautifulsoup4
```

## Como utilizar

### 1. Configuração Inicial
Substitua SUA MATRICULA e SUA SENHA na variável formdata com as credenciais do SGA.

### 2. Execução

Execute o script no terminal
```bash
python sga.py
```

### 3. Saídas
O arquivo ```faltas.json``` será gerado na pasta do projeto contendo as informações das disciplinas.

## Exemplo de Saída

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## Licença
Este projeto é distribuído sob a MIT License.
