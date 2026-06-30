import tkinter as tk
from tkinter import messagebox
import os
from engine import CalculadoraEngine

engine = CalculadoraEngine()

# Criar janela
janela = tk.Tk()
janela.title("Calculadora Simples")
janela.geometry("300x500")
janela.configure(bg="#121212")

# Variável global para armazenar operação
acabou_operacao = False

# Função para adicionar número
def clicar_numero(numero):
    global acabou_operacao

    if visor.get() == "Erro":
        visor.delete(0, tk.END)
        visor.insert(0, "0")

    if acabou_operacao:
        visor.delete(0, tk.END)
        visor.insert(0, "0")
        acabou_operacao = False

    atual = visor.get()

    if atual == "0":
        visor.delete(0, tk.END)
        visor.insert(0, str(numero))
    else:
        visor.insert(tk.END, str(numero))

# Função para adicionar operador
def clicar_operador(op):
    global acabou_operacao

    atual = visor.get()

    if atual == "Erro":
        return

    if acabou_operacao:
        acabou_operacao = False

    # evita começar com operador,
    # mas permite "-" e "("
    if atual == "0" and op not in "-(":
        return

    # substitui operador duplicado
    if atual and atual[-1] in "+-*/" and op not in "()":
        visor.delete(len(atual)-1, tk.END)
        visor.insert(tk.END, op)
    else:
        # substitui o 0 inicial ao abrir parêntese
        if atual == "0" and op == "(":
            visor.delete(0, tk.END)
            visor.insert(0, "(")
        else:
            visor.insert(tk.END, op)

# Função para calcular resultado
def calcular():
    global acabou_operacao

    expressao = visor.get()

    # impede calcular vazio
    if not expressao:
        return

    # impede terminar com operador
    if expressao[-1] in "+-*/":
        visor.delete(0, tk.END)
        visor.insert(0, "Erro")
        acabou_operacao = True
        return

    if expressao.count("(") != expressao.count(")"):
        visor.delete(0, tk.END)
        visor.insert(0, "Erro")
        acabou_operacao = True
        return

    resultado = engine.calcular_expressao(expressao)

    if resultado == "Erro":
        visor.delete(0, tk.END)
        visor.insert(0, "Erro")
        acabou_operacao = True
        return

    engine.ultimo_resultado = float(
        str(resultado).replace(",", "")
    )

    visor.delete(0, tk.END)
    visor.insert(0, resultado)

    acabou_operacao = True
# Função limpar
def limpar():
    global acabou_operacao

    visor.delete(0, tk.END)
    visor.insert(0, "0")
    acabou_operacao = False

def clicar_decimal():
    atual = visor.get()

    # pega o último número (depois do último operador)
    partes = atual.split("+")
    partes = partes[-1].split("-")
    partes = partes[-1].split("*")
    partes = partes[-1].split("/")

    ultimo_numero = partes[-1]

    if "." not in ultimo_numero:
        visor.insert(tk.END, ".")
def porcentagem():
    resultado = engine.porcentagem(visor.get())

    visor.delete(0, tk.END)
    visor.insert(0, resultado)


def memoria_mais():
    engine.memoria_mais()

    indicador_memoria.config(
        text="[M]"
    )


def memoria_recall():
    visor.delete(0, tk.END)
    visor.insert(0, engine.memoria_recall())


def memoria_clear():
    engine.memoria_clear()

    indicador_memoria.config(
        text=""
    )

def apagar():
    atual = visor.get()

    if len(atual) > 1:
        visor.delete(len(atual)-1, tk.END)
    else:
        visor.delete(0, tk.END)
        visor.insert(0, "0")

def pressionar_tecla(event):
    tecla = event.char
    tecla_especial = event.keysym

    # números
    if tecla and tecla.isdigit():
        clicar_numero(tecla)

    # operadores
    elif tecla in "+-*/()":
        clicar_operador(tecla)

    # decimal
    elif tecla == ".":
        clicar_decimal()

    # porcentagem
    elif tecla == "%" and visor.get() != "0":
        porcentagem()

    # Enter = calcular
    elif tecla_especial == "Return":
        calcular()

    # Backspace = apagar
    elif tecla_especial == "BackSpace":
        apagar()

    # Esc = limpar
    elif tecla_especial == "Escape":
        limpar()

    # Delete = limpar
    elif tecla_especial == "Delete":
        limpar()

    # C = limpar
    elif tecla and tecla.lower() == "c":
        limpar()

    return "break"

def inserir_ans():
    global acabou_operacao

    valor = str(engine.ultimo_resultado)

    if valor.endswith(".0"):
        valor = valor[:-2]

    atual = visor.get()

    # substitui o zero inicial
    if atual == "0":
        visor.delete(0, tk.END)
        visor.insert(0, valor)

    else:
        # se acabou de calcular, substitui o resultado
        if acabou_operacao:
            visor.delete(0, tk.END)
            acabou_operacao = False

        visor.insert(tk.END, valor)

def clear_entry():
    global acabou_operacao

    atual = visor.get()

    # se acabou de calcular, limpa tudo
    if acabou_operacao:
        visor.delete(0, tk.END)
        visor.insert(0, "0")
        acabou_operacao = False
        return

    # procura o último operador
    ultimo_operador = -1

    for operador in "+-*/":
        pos = atual.rfind(operador)

        if pos > ultimo_operador:
            ultimo_operador = pos

    # se não tiver operador, limpa tudo
    if ultimo_operador == -1:
        novo_texto = "0"
    else:
        # mantém apenas até o operador
        novo_texto = atual[:ultimo_operador + 1]

    visor.delete(0, tk.END)
    visor.insert(0, novo_texto)

def exportar_historico():

    nome_arquivo = engine.exportar_csv()

    if nome_arquivo == "Nenhum histórico":
        messagebox.showwarning(
            "Aviso",
            "Nenhum histórico para exportar."
        )

    else:
        messagebox.showinfo(
            "Sucesso",
            f"Histórico exportado como:\n{nome_arquivo}"
        )

def abrir_historico():

    janela_historico = tk.Toplevel(janela)

    janela_historico.title("Histórico")

    janela_historico.geometry("300x500")

    janela_historico.configure(bg="#121212")

    titulo = tk.Label(
        janela_historico,
        text="Histórico",
        font=("Segoe UI", 18, "bold"),
        bg="#121212",
        fg="white"
    )

    titulo.pack(pady=10)

    scrollbar = tk.Scrollbar(janela_historico)

    caixa_historico = tk.Text(
        janela_historico,
        font=("Consolas", 12),
        bg="#1E1E1E",
        fg="white",
        bd=0,
        height=15,
        yscrollcommand=scrollbar.set
    )

    scrollbar.config(command=caixa_historico.yview)

    scrollbar.pack(side="right", fill="y")

    caixa_historico.pack(
        expand=True,
        fill="both",
        padx=10,
        pady=(10, 0)
    )

    def limpar_historico():

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja apagar todo o histórico?"
        )

        if confirmar:
            engine.historico.clear()

            with open("historico.txt", "w", encoding="utf-8") as arquivo:
                pass

            caixa_historico.delete("1.0", tk.END)

            messagebox.showinfo(
                "Sucesso",
                "Histórico apagado com sucesso!"
            )

    botao_limpar_historico = tk.Button(
        janela_historico,
        text="🗑 Limpar Histórico",
        font=("Segoe UI", 12, "bold"),
        bg="#D32F2F",
        fg="white",
        bd=0,
        relief="flat",
        activebackground="#FF5252",
        command=limpar_historico
    )

    botao_limpar_historico.pack(
        fill="x",
        padx=10,
        pady=10
    )

    botao_exportar = tk.Button(
        janela_historico,
        text="📁 Exportar CSV",
        font=("Segoe UI", 12, "bold"),
        bg="#1976D2",
        fg="white",
        bd=0,
        relief="flat",
        activebackground="#2196F3",
        command=exportar_historico
    )

    botao_exportar.pack(
        fill="x",
        padx=10,
        pady=(0, 10)
    )

    for item in engine.historico:
        caixa_historico.insert(tk.END, item + "\n")

indicador_memoria = tk.Label(
    janela,
    text="",
    font=("Segoe UI", 12, "bold"),
    bg="#121212",
    fg="#00E676",
    anchor="e"
)

indicador_memoria.pack(
    fill="x",
    padx=10,
    pady=(5, 0)
)

# Criar visor
visor = tk.Entry(
    janela,
    font=("Segoe UI", 28),
    bd=0,
    justify="right",
    bg="#121212",
    fg="white",
    insertbackground="white"
)

visor.insert(0, "0")

# remove foco/cursor do Entry
visor.bind("<FocusIn>", lambda e: janela.focus())

visor.pack(fill="both", padx=5, pady=5)

# paleta de cores
cor_fundo = "#121212"
cor_numero = "#1E1E1E"
cor_operador = "#FF9500"
cor_igual = "#00C853"
cor_limpar = "#D32F2F"
cor_texto = "white"

# Frame dos botões
frame_botoes = tk.Frame(janela, bg=cor_fundo)
frame_botoes.pack(expand=True, fill="both", padx=5, pady=5)

frame_botoes.grid_columnconfigure(0, weight=1)
frame_botoes.grid_columnconfigure(1, weight=1)
frame_botoes.grid_columnconfigure(2, weight=1)
frame_botoes.grid_columnconfigure(3, weight=1)

for i in range(7):
    frame_botoes.grid_rowconfigure(i, weight=1, uniform="linha")

for i in range(4):
    frame_botoes.grid_columnconfigure(i, weight=1, uniform="coluna")

# Botões numéricos
botoes = [
    ("7", 7), ("8", 8), ("9", 9),
    ("4", 4), ("5", 5), ("6", 6),
    ("1", 1), ("2", 2), ("3", 3),
]

linha = 2
coluna = 0

for texto, numero in botoes:

    botao = tk.Button(
        frame_botoes,
        text=texto,
        font=("Segoe UI", 16, "bold"),
        command=lambda n=numero: clicar_numero(n)
    )

    botao.grid(row=linha, column=coluna, sticky="nsew", padx=5, pady=5)

    coluna += 1

    if coluna > 2:
        coluna = 0
        linha += 1

# Botões de operação
operadores = [
    ("+", "+"),
    ("-", "-"),
    ("×", "*"),
    ("÷", "/")
]

linha = 2
coluna = 0

for texto, op in operadores:
    botao = tk.Button(
        frame_botoes,
        text=texto,
        font=("Segoe UI", 16, "bold"),
        bg=cor_operador,
        fg="white",
        bd=0,
        relief="flat",
        highlightthickness=0,
        activebackground="#ffaa33",
        command=lambda o=op: clicar_operador(o)
    )
    botao.grid(row=linha, column=3, sticky="nsew", padx=5, pady=5)  # ← padx/pady adicionados
    linha += 1

#Botão igual
botao_igual = tk.Button(
    frame_botoes,
    text="=",
    font=("Segoe UI", 16, "bold"),
    bg=cor_igual,
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#00E676",
    command=calcular
)
botao_igual.grid(row=6, column=1, sticky="nsew")

#Botão limpar
botao_limpar = tk.Button(
    frame_botoes,
    text="C",
    font=("Segoe UI", 16, "bold"),
    bg=cor_limpar,
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#FF5252",
    command=limpar
)
botao_limpar.grid(row=6, column=0, sticky="nsew")

#botão decimal
botao_ponto = tk.Button(
    frame_botoes,
    text=".",
    font=("Segoe UI", 16, "bold"),
    bg=cor_numero,
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#2A2A2A",
    command=clicar_decimal
)

botao_ponto.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)  # ← padx/pady adicionados

#botão porcentagem
botao_porcentagem = tk.Button(
    frame_botoes,
    text="%",
    font=("Segoe UI", 16, "bold"),
    bg=cor_operador,
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#ffaa33",
    command=porcentagem
)

botao_porcentagem.grid(row=6, column=2, sticky="nsew")

#botão zero
botao_zero = tk.Button(
    frame_botoes,
    text="0",
    font=("Segoe UI", 16, "bold"),
    bg=cor_numero,
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#2A2A2A",
    command=lambda: clicar_numero(0)
)

botao_zero.grid(row=5, column=0, columnspan=2, sticky="nsew", padx = 5, pady = 5)

botao_backspace = tk.Button(
    frame_botoes,
    text="⌫",
    font=("Segoe UI", 16, "bold"),
    bg="#444444",
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#666666",
    command=apagar,
    padx=10,
    pady=10
)

botao_backspace.grid(row=6, column=3, sticky="nsew")

# ===== LINHA SUPERIOR =====

# Histórico
botao_historico = tk.Button(
    frame_botoes,
    text="📜",
    font=("Segoe UI", 16),
    bg="#444444",
    fg="white",
    bd=0,
    relief="flat",
    highlightthickness=0,
    activebackground="#666666",
    command=abrir_historico
)

botao_historico.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=5,
    pady=5
)

# (
botao_abre_parentese = tk.Button(
    frame_botoes,
    text="(",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=lambda: clicar_operador("(")
)

botao_abre_parentese.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=5,
    pady=5
)

# )
botao_fecha_parentese = tk.Button(
    frame_botoes,
    text=")",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=lambda: clicar_operador(")")
)

botao_fecha_parentese.grid(
    row=0,
    column=2,
    sticky="nsew",
    padx=5,
    pady=5
)

# M+
botao_mmais = tk.Button(
    frame_botoes,
    text="M+",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=memoria_mais
)

botao_mmais.grid(
    row=0,
    column=3,
    sticky="nsew",
    padx=5,
    pady=5
)

# MR
botao_mr = tk.Button(
    frame_botoes,
    text="MR",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=memoria_recall
)

botao_mr.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=5,
    pady=5
)

# MC
botao_mc = tk.Button(
    frame_botoes,
    text="MC",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=memoria_clear
)

botao_mc.grid(
    row=1,
    column=1,
    sticky="nsew",
    padx=5,
    pady=5
)

# CE
botao_ce = tk.Button(
    frame_botoes,
    text="CE",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=clear_entry
)

botao_ce.grid(
    row=1,
    column=2,
    sticky="nsew",
    padx=5,
    pady=5
)

# Ans
botao_ans = tk.Button(
    frame_botoes,
    text="Ans",
    font=("Segoe UI", 12, "bold"),
    bg="#555555",
    fg="white",
    bd=0,
    relief="flat",
    activebackground="#777777",
    command=inserir_ans
)

botao_ans.grid(
    row=1,
    column=3,
    sticky="nsew",
    padx=5,
    pady=5
)

janela.bind_all("<Key>", pressionar_tecla)

# Rodar
janela.mainloop()
