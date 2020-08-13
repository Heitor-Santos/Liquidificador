# Liquidificador


Basicamente, a aplicação serve para gerar várias versões da mesma prova para dificultar que os alunos colem.
E obviamente, enquanto estudante, isso é falta de consciência de classe :(

## Configurando
Para executar essa aplicação, é necessário ter python instalado, isso pode ser feito com o seguinte comando:

    sudo apt-get install python3

Depois de fazer o download da aplicação, digite o seguinte comando na pasta que a contém:
  
    python3 app.py

## Observações: 
A aplicação foi toda baseada em python-docx, que é um módulo um tanto quanto rudimentar e carente de muitas funcionalidades.
Para maximizar a chance do Liquidificador funcionar, siga as seguintes diretrizes:
- Mantenha apenas uma alternativa em cada parágrafo
- Cada alternativa deve começar com uma letra seguida de ")" ou "." ou "-". Ex: a), B), c), d., e-
- Evite itens na forma "I-,II-,III-", o primeiro pode ser visto como uma alternativa

## Pendências
- Ainda não foram testadas imagens ou tabelas (apesar de que teoricamente imagens devem funcionar)
- O texto pode perder parte do seu estilo (ficar com fonte ou tamanho diferente do original)


