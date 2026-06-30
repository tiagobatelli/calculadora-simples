# Bibliotecas padrão do Python
import datetime # para gerar o timestamp no nome do arquivo CSV
import csv # para escrever o arquivo de exportação

class CalculadoraEngine:
    """
    Motor principal da calculadora.
    Gerencia cálculos, histórico persistente e memória.
    """

    def __init__(self):
        """Inicializa a engine com histórico vazio, memória zerada e carrega o histórico salvo."""

        self.historico = []
        self.memoria = 0
        self.ultimo_resultado = 0

        self.carregar_historico()

    def carregar_historico(self):
        """Lê o arquivo historico.txt e carrega as operações anteriores na lista de histórico."""

        try:
            with open("historico.txt", "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    self.historico.append(linha.strip())
        except FileNotFoundError:
            pass

    def salvar_operacao(self, operacao):
        """Adiciona a operação ao histórico em memória e a persiste no arquivo historico.txt."""

        self.historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(operacao + "\n")

    def calcular_expressao(self, expressao):
        """
        Avalia uma expressão matemática como string.
        Suporta +, -, *, /, ** e parênteses.
        Retorna o resultado como string ou 'Erro' se inválido.
        """

        try:
            expressao = expressao.replace("×", "*").replace("÷", "/")

            resultado = eval(expressao, {"__builtins__": None}, {})

            # salva o resultado real para memória
            self.ultimo_resultado = float(resultado)

            operacao = f"{expressao} = {resultado:.2f}"
            self.salvar_operacao(operacao)

            if resultado == int(resultado):
                return str(int(resultado))
            else:
                return f"{resultado:.6f}".rstrip("0").rstrip(".")

        except:
            return "Erro"

    def porcentagem(self, valor):
        """Divide o valor por 100 e retorna como string formatada."""

        try:
            resultado = float(valor) / 100
            self.ultimo_resultado = resultado

            if resultado == int(resultado):
                return f"{int(resultado):,}"
            else:
                return f"{resultado:,.6f}".rstrip('0').rstrip('.')

        except:
            return "Erro"

    def memoria_mais(self):
        """Adiciona o último resultado à memória acumulada."""

        self.memoria += self.ultimo_resultado

    def memoria_recall(self):
        """Retorna o valor atual da memória como string."""

        if self.memoria == int(self.memoria):
            return str(int(self.memoria))

        return str(self.memoria)

    def memoria_clear(self):
        """Zera a memória."""

        self.memoria = 0

    def exportar_csv(self):
        """
        Exporta o histórico para um arquivo CSV com timestamp no nome.
        Retorna o nome do arquivo criado ou 'Nenhum histórico' se vazio.
        """

        if len(self.historico) == 0:
            return "Nenhum histórico"

        agora = datetime.datetime.now()
        nome_arquivo = f"historico_{agora.strftime('%Y-%m-%d_%H-%M')}.csv"

        with open(nome_arquivo, "w", encoding="utf-8-sig", newline="") as arquivo:
            writer = csv.writer(arquivo, delimiter=";")
            writer.writerow(["Operacao"])

            for item in self.historico:
                writer.writerow([item])

        return nome_arquivo