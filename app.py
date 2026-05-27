from groq import Groq       
from dotenv import load_dotenv  # Lê variáveis de ambiente do arquivo .env
import os
import json

# ─── Configuração inicial ───────────────────────────────────────────────────

# Carrega o .env para que os.getenv() consiga ler a GROQ_API_KEY
load_dotenv()

# Cria o cliente autenticado com a chave da API
# A chave fica no .env e nunca vai pro GitHub (protegida pelo .gitignore)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Nome do arquivo onde o histórico de conversa é salvo entre sessões
HISTORICO_FILE = "historico.json"

# System prompt: instrução que define a personalidade do bot
# O papel "system" é especial — o modelo o trata como uma regra, não como fala do usuário
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Você terá a personalidade da personagem Plim de Smiling Friends. "
        "Ele trabalha em uma empresa que faz as pessoas sorrirem. "
        "Quem está triste liga para a empresa e Pim Pimling e o Charlie vão tentar resolver. "
        "O Plim é otimista, baixinho e rosa, é o funcionário idealista do grupo. "
        "Ele tenta sempre fazer o bem, mesmo que acabe se envolvendo em situações caóticas."
    )
}

# ─── Funções auxiliares ──────────────────────────────────────────────────────

def carregar_historico():
    """
    Lê o histórico salvo no JSON e retorna como lista de mensagens.

    O histórico contém todas as trocas anteriores (user + assistant),
    permitindo que o bot lembre de conversas passadas.
    Retorna lista vazia se o arquivo não existir ou estiver corrompido.
    """
    try:
        with open(HISTORICO_FILE, "r") as f:
            historico = json.load(f)
        # Filtra possíveis system prompts duplicados salvos em versões anteriores
        return [m for m in historico if m["role"] != "system"]
    except (FileNotFoundError, json.JSONDecodeError):
        # FileNotFoundError → primeira execução, arquivo ainda não existe
        # JSONDecodeError   → arquivo corrompido, começa do zero
        return []


def salvar_historico(memoria):
    """
    Persiste o histórico de conversa no arquivo JSON.

    Salva apenas mensagens de "user" e "assistant" — o system prompt
    é sempre reinjetado em memória na inicialização, então não precisa
    ser gravado em disco (evita duplicações).
    """
    # Remove o system prompt antes de salvar
    sem_system = [m for m in memoria if m["role"] != "system"]

    # ensure_ascii=False mantém acentos legíveis no JSON
    # indent=2 formata o JSON com indentação para fácil leitura
    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(sem_system, f, ensure_ascii=False, indent=2)


def exibir_historico(memoria):
    """
    Imprime as últimas 10 mensagens da conversa no terminal.

    Útil para o usuário relembrar o contexto da conversa atual
    sem precisar abrir o arquivo JSON manualmente.
    Mensagens longas são truncadas em 80 caracteres para caber no terminal.
    """
    # Ignora o system prompt na exibição — não é relevante pro usuário
    mensagens = [m for m in memoria if m["role"] != "system"]

    if not mensagens:
        print("\n📭 Histórico vazio.\n")
        return

    print("\n📜 Últimas mensagens:\n")
    for msg in mensagens[-10:]:  # Exibe só as últimas 10
        autor = "Você" if msg["role"] == "user" else "Plim"
        conteudo = msg["content"]
        # Trunca mensagens longas para não poluir o terminal
        resumo = conteudo[:80] + "..." if len(conteudo) > 80 else conteudo
        print(f"  [{autor}]: {resumo}")
    print()


def limpar_historico():
    """
    Apaga o arquivo de histórico e reinicia a conversa do zero.

    Útil quando o usuário quer começar uma nova conversa sem
    que o Plim lembre de mensagens antigas.
    """
    if os.path.exists(HISTORICO_FILE):
        os.remove(HISTORICO_FILE)
    print("\n🧹 Histórico apagado! Começando uma nova conversa.\n")


# ─── Inicialização ───────────────────────────────────────────────────────────

print("=" * 50)
print("  💬 Plim Chat — Smiling Friends")
print("=" * 50)
print("Comandos disponíveis:")
print("  /limpar    → apaga o histórico e recomeça")
print("  /historico → mostra as últimas mensagens")
print("  sair       → encerra o chat")
print("=" * 50 + "\n")

# Carrega o histórico salvo (se existir) para manter a memória entre sessões
memoria = carregar_historico()

# Monta a lista completa de mensagens: system prompt + histórico anterior
# O system prompt fica sempre no índice 0, garantindo que o modelo siga a personalidade
memoria_com_system = [SYSTEM_PROMPT] + memoria

# ─── Loop principal do chat ──────────────────────────────────────────────────

while True:
    user_input = input("Você: ").strip()  # .strip() remove espaços acidentais

    # Ignora Enter em branco
    if not user_input:
        continue

    # Encerra o programa de forma amigável
    if user_input.lower() == "sair":
        print("\nPlim: Até logo! Sorria sempre! 😊\n")
        break

    # Limpa o histórico e reinicia a memória em tempo de execução
    if user_input.lower() == "/limpar":
        limpar_historico()
        memoria = []
        memoria_com_system = [SYSTEM_PROMPT]  # Mantém só o system prompt
        continue

    # Exibe o histórico sem interromper o fluxo do chat
    if user_input.lower() == "/historico":
        exibir_historico(memoria_com_system)
        continue

    # Adiciona a mensagem do usuário ao histórico em memória
    memoria_com_system.append({"role": "user", "content": user_input})

    # Envia todo o histórico para a API da Groq
    # Mandar o histórico completo é o que dá "memória" ao modelo —
    # LLMs são stateless, então o contexto precisa ser reenviado a cada chamada
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=memoria_com_system
    )

    # Extrai o texto da resposta do modelo
    resposta_ia = response.choices[0].message.content

    # Adiciona a resposta ao histórico e exibe no terminal
    memoria_com_system.append({"role": "assistant", "content": resposta_ia})
    print(f"\nPlim: {resposta_ia}\n")

    # Persiste o histórico atualizado no JSON para a próxima sessão
    memoria = [m for m in memoria_com_system if m["role"] != "system"]
    salvar_historico(memoria)