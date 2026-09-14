import threading

# ============================================================
# CONJUNTOS
# ============================================================

CVR = {2}       # Conjunto Valores Revelados
CSP = set()     # Conjunto Série Passiva
CPCN = set()    # Conjunto Pontos de Corrosão Novos
CPCA = set()    # Conjunto Pontos de Corrosão Antigos

parar = threading.Event()


# ============================================================
# REALIZA UMA OPERAÇÃO
# ============================================================

def realizar_operacao(p_antigo, primeira_operacao=False):

    global CVR, CSP, CPCN, CPCA

    # --------------------------------------------------------
    # 1. Determina P novo
    # --------------------------------------------------------

    valores = sorted(CVR)

    if primeira_operacao:
        # Primeira operação:
        # CVR = {2}
        # P = 2 × 2
        p_novo = 4

    else:
        # Produto dos dois maiores valores do CVR
        maior = valores[-1]
        segundo_maior = valores[-2]

        p_novo = maior * segundo_maior

    # --------------------------------------------------------
    # 2. CSP recebe os valores entre P antigo e P novo
    # --------------------------------------------------------

    for numero in range(p_antigo + 1, p_novo + 1):

        if numero != 1:
            CSP.add(numero)

    # --------------------------------------------------------
    # 3. Metade de P
    #
    # Essa metade determina quais elementos do CVR podem
    # ser utilizados como divisores.
    # --------------------------------------------------------

    metade = p_novo // 2

    # --------------------------------------------------------
    # 4. GERA OS PONTOS DE CORROSÃO
    #
    # Para cada valor do CVR <= P/2:
    #
    #     quantidade = P // valor
    #
    # São gerados todos os múltiplos:
    #
    #     valor × 1
    #     valor × 2
    #     ...
    #     valor × quantidade
    #
    # Portanto, os múltiplos chegam até P.
    # --------------------------------------------------------

    for valor in sorted(CVR):

        if valor <= metade:

            quantidade = p_novo // valor

            for multiplicador in range(1, quantidade + 1):

                produto = valor * multiplicador

                CPCN.add(produto)

    # --------------------------------------------------------
    # 5. Remove do CPCN os pontos que já pertencem ao CPCA
    #
    # Essa remoção é definitiva.
    # CPCN não é zerado.
    # --------------------------------------------------------

    CPCN -= CPCA

    # --------------------------------------------------------
    # 6. Remove do CSP os pontos de corrosão
    # --------------------------------------------------------

    CSP -= CPCN

    # --------------------------------------------------------
    # 7. O que sobrou do CSP é revelado e entra no CVR
    # --------------------------------------------------------

    novos_valores = CSP - CVR

    if novos_valores:

        CVR.update(novos_valores)

        print(
            ", ".join(map(str, sorted(novos_valores))),
            flush=True
        )

    # --------------------------------------------------------
    # 8. CSP é zerado ao final da operação
    # --------------------------------------------------------

    CSP.clear()

    # --------------------------------------------------------
    # 9. CPCN é integrado ao CPCA
    #
    # CPCN continua existindo.
    # --------------------------------------------------------

    CPCA.update(CPCN)

    return p_novo


# ============================================================
# EXECUÇÃO
# ============================================================

def executar():

    p_antigo = 0
    primeira_operacao = True

    while not parar.is_set():

        p_novo = realizar_operacao(
            p_antigo,
            primeira_operacao
        )

        p_antigo = p_novo
        primeira_operacao = False


# ============================================================
# AGUARDA ENTER
# ============================================================

def esperar_enter():

    input()
    parar.set()


# ============================================================
# INÍCIO
# ============================================================

print("Digite /start para iniciar:")

comando = input().strip()

if comando == "/start":

    print("\nPrograma iniciado.")

    # O 2 já existe inicialmente no CVR,
    # então ele é o primeiro valor revelado.
    print("2", flush=True)

    print("Pressione ENTER para encerrar.\n")

    thread_enter = threading.Thread(
        target=esperar_enter,
        daemon=True
    )

    thread_enter.start()

    executar()

    print("\nPrograma encerrado.")

else:

    print("Comando inválido.")
    print("O comando correto é /start.")