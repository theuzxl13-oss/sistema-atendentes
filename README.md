# Painel Futturis — sistema de atendimento, vendas e estoque

Aplicação web interna (Streamlit) para o atendimento de balcão de uma loja de materiais de
construção: controle de estoque, registro de vendas com baixa automática, trocas/devoluções,
relatórios de faturamento e cadastro de atendentes — tudo com permissões diferentes por cargo.

Pensado para rodar num computador da loja e ser aberto pelo navegador pelos próprios atendentes.

## Funcionalidades

- **Login por atendente**, com cargo e local associados a cada usuário.
- **Permissões por cargo**: um `Vendedor` só vê as abas de Vendas e Trocas; cargos administrativos
  (`Desenvolvedor`, `Gerente`, `Dono`) também veem Cadastro de Produto, Estoque, Relatórios e
  Cadastro de Atendentes.
- **Estoque**: cadastro de produtos por categoria (materiais básicos, ferramentas, acabamento),
  com preço e quantidade.
- **Vendas**: seleciona o produto, informa a quantidade (limitada ao estoque disponível), calcula
  o total e, ao confirmar, já dá baixa automática no estoque.
- **Trocas/devoluções**: registro do produto devolvido, quantidade e motivo.
- **Relatórios**: histórico de vendas filtrado por período, com faturamento total do intervalo.
- **Cadastro de atendentes**: cria novos usuários com cargo e local/filial.
- Foto de perfil do atendente (upload simples, fica só na sessão do navegador).

## Como rodar

Requer Python e as dependências do `requirements.txt` instaladas.

```bash
pip install -r requirements.txt
streamlit run novo_app.py
```

No Windows, o script [`iniciar_sistema.bat`](iniciar_sistema.bat) faz isso automaticamente e abre
o navegador. Na primeira execução, o app cria o arquivo `sistema.db` (SQLite) com 4 usuários e 3
produtos de exemplo:

| Usuário | Senha | Cargo |
|---|---|---|
| `marcelo` | `123` | Desenvolvedor |
| `matheus` | `123` | Desenvolvedor |
| `vendedor1` | `123` | Vendedor |
| `dono` | `123` | Dono |

## Stack técnica

- **Streamlit** para a interface (tudo roda em Python, sem HTML/JS separado).
- **SQLite** como banco de dados local (`sistema.db`), com tabelas de usuários, produtos, vendas e
  trocas.
- **pandas** para montar as tabelas exibidas (estoque, relatórios, lista de atendentes).

## Estrutura

```
novo_app.py         # aplicação principal (login, abas, todas as telas)
main.py             # vazio (não é o ponto de entrada — use novo_app.py)
iniciar_sistema.bat # atalho para rodar no Windows
sistema.db          # banco SQLite (criado/atualizado automaticamente ao rodar)
```

## Possíveis melhorias

- Senhas ficam em texto puro no banco — o ideal seria salvar um hash (ex: `bcrypt`) em vez da
  senha literal.
- `oi.py` é um script avulso (jogo de apostas em número) sem relação com o painel — dava pra
  remover ou mover para uma pasta separada de estudos.
- `requirements.txt` está salvo com um encoding que intercala espaços entre os caracteres —
  vale regerar com `pip freeze > requirements.txt` a partir de um terminal UTF-8.
- `main.py` está vazio; ou remove, ou vira de fato o ponto de entrada do projeto.
