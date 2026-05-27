# 💬 Plim Chat — Groq + LLaMA 3.3

Chatbot conversacional com IA desenvolvido em Python, usando a API da Groq com o modelo LLaMA 3.3. O bot assume a personalidade do **Plim**, personagem de *Smiling Friends* — otimista, simpático e sempre pronto pra te animar.

---

## 🖥️ Preview

```
==================================================
  💬 Plim Chat — Smiling Friends
==================================================
Comandos disponíveis:
  /limpar    → apaga o histórico e recomeça
  /historico → mostra as últimas mensagens
  sair       → encerra o chat
==================================================

Você: oi, tô me sentindo mal hoje
Plim: Oi! Eu sou o Plim e estou aqui pra te ajudar a sorrir! 
      Me conta o que aconteceu... 😊
```

---

## ✨ Funcionalidades

- 🧠 **Memória persistente** — lembra tudo que foi dito em sessões anteriores
- 🎭 **Personalidade customizada** — o Plim responde com o jeito único do personagem
- 🧹 **`/limpar`** — reseta o histórico e começa uma conversa nova
- 📜 **`/historico`** — exibe as últimas 10 mensagens da conversa
- 🔐 **Variáveis de ambiente** — chave da API protegida com `.env`

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| [Groq API](https://console.groq.com) | Inferência rápida com LLaMA 3.3 70B |
| python-dotenv | Gerenciamento de variáveis de ambiente |

---

## 🚀 Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/groq-chat.git
cd groq-chat
```

**2. Instale as dependências**
```bash
pip install groq python-dotenv
```

**3. Configure sua chave da API**

Crie um arquivo `.env` na raiz do projeto:
```
GROQ_API_KEY=sua_chave_aqui
```
> Você pode gerar sua chave gratuitamente em [console.groq.com](https://console.groq.com)

**4. Rode o projeto**
```bash
python app.py
```

---

## 📁 Estrutura do projeto

```
groq-chat/
├── app.py            # Lógica principal do chatbot
├── historico.json    # Histórico de mensagens (gerado automaticamente)
├── .env              # Chave da API (não commitado)
├── .gitignore
└── README.md
```

---

## 💡 Como funciona

1. O usuário digita uma mensagem no terminal
2. A mensagem é adicionada ao histórico de conversa
3. O histórico completo é enviado para a API da Groq (com o system prompt do Plim)
4. A resposta é exibida no terminal e salva no `historico.json`
5. Na próxima sessão, o histórico é carregado automaticamente — o Plim lembra de você!