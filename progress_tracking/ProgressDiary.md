- fill up the base cover letters using xml tags
- make the forms talk with the base cover letter

# Qual é o principal objetivo agora?
- Ter uma versão rodando
O que precisamos para isso?
## Dia 2024-01-17
- Criar a estrutura com css e zaz DONE
- Fazer o main funcionar com essa estrutura DONE
- Fazer a segunda página que faz o xml aparecer DONE
- usar um xml falso para teste DONEs
## O que mais?
- Bem, os próximos passos envolvem de fato usar o gpt
- Pegar minha nova chave
- Editar o arquivo gpt-app, seja lá como ele chama agora
- fazer o run falar com ele!
- Está bem geral, mas a gente começa daí depois
## Dia 2024-01-18
### O que fazer?
- Já criei e testei uma nova key DONE
- quero que as opções de base sejam baseadas nos nomes dos arquivos do diretório ``base_cover_letters/`` DONE
- onde eu devo criar o objeto? -> models.py
- E onde eu devo ler o arquivo? -> no próprio models!
- E depois bora pro gpt
## Dia 2024-01-23
- Terminei o uso do Flask-WTF com uma classe que já faz um pos processamento
- O próximo passo realmente é o gpt
- Nossa, foram muitas horas com essa coisa de forms! Talvez eu devesse ter ficado com a versão mais pedestre. Mas gostei
## Dia 2024-01-24
- Uh lah lah
- Ok, qual é de plano pra hoje?
- Eu quero fazer o processamento
- Eu fiquei meio perdido e fiz um prompt. Mas pensando, eu quero agora ver o pdf.
- Depois quero introduzir a página intermediária para poder modificar o texto antes do pdf.
## Dia 2024-0125
- Hoje vai rolar o pdf.
- vou olhar o latex primeiro
- E o propmt que eu tenho deve funcionar
- Quero colocar meu endereço. Como não deixar no github
## jj
- Lembrar o prompt de que vai ser em latex, para evitar o problema com o C#?
## Dia 2024-01-28
- Meu Deus, já é dia 28
- Tá, o que eu quero fazer hoje?
- Tenho o problema do tex com símbolos como % e #
- Quero resolver o problema do endereço
- Quero um página que mostra o texto numa box
- Vou começar pelo problema do endereço
- Ok! consertei o endereço. Demorou tipo 1h30, como foi chato isso
- O próximo passo é colocar numa box
- Também quero fazer um GptMixin
- Transformei o gpt num mixin, foi fácil, 15 min
- Agora quero criar uma página com uma box que contém a letter pra ser copiada e colada
---
- Ok, isso foi um terror. Não rolou nem fudendo. Mas acho que agora descobri como fazer.
- Vai ser tudo dentro da mesma função, no /, e vai ter 2 submits. Acho que isso vai funcionar bem.
## Dia 2024-02-06
- Eu quero agora criar o copy to clipboard button
