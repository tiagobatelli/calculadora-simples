import datetime
import csv
import sys

sys.set_int_max_str_digits(4300)

# Super Calculadora Python - Versão 3 (carregando histórico)

historico = []
memoria = 0
ultimo_resultado = 0

# 🔥 NOVA PARTE — carregar histórico ao iniciar

try:
    with open("historico.txt", "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            historico.append(linha.strip()) #o strip tira as quebras por extenso \n, tendeu?

except FileNotFoundError:
    print("Nenhum histórico anterior encontrado.")

while True:
    print("\n" + "=" * 35)
    print("        SUPER CALCULADORA")
    print("=" * 35)
    print("1 - Somar")
    print("2 - Subtrair")
    print("3 - Multiplicar")
    print("4 - Dividir")
    print("5 - Ver histórico")
    print("6 - Potência")
    print("7 - Raiz quadrada")
    print("8 - Porcentagem")
    print("9 - Resto da divisão")
    print("10 - Guardar resultado na memória (M+)")
    print("11 - Mostrar memória (MR)")
    print("12 - Limpar memória (MC)")
    print("13 - Exportar histórico para CSV")
    print("0 - Sair")
    print("=" * 35)

    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Saindo da calculadora...")
        break

    elif opcao == "5":
        print("\n=== HISTÓRICO ===")

        if len(historico) == 0:
            print("Nenhuma operação ainda.")

        else:
            for i, item in enumerate(historico, start=1):
                print(f"{i}) {item}")

    elif opcao in ["1", "2", "3", "4"]:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))

        if opcao == "1":
            resultado = num1 + num2
            operacao = f"{num1:,.2f} + {num2:,.2f} = {resultado:,.2f}"

        elif opcao == "2":
            resultado = num1 - num2
            operacao = f"{num1:,.2f} - {num2:,.2f} = {resultado:,.2f}"

        elif opcao == "3":

            sys.set_int_max_str_digits(4300)
            resultado = num1 * num2
            operacao = f"{num1:,.2f} * {num2:,.2f} = {resultado:,.2f}"

        elif opcao == "4":
            if num2 == 0:
                print("Erro: divisão por zero!")
                continue
            resultado = num1 / num2
            operacao = f"{num1:,.2f} / {num2:,.2f} = {resultado:,.2f}"

        ultimo_resultado = resultado
        print(f"Resultado: {resultado:,.2f}")
        historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(operacao + "\n")

    elif opcao == "6":

        # Limita a conversão para texto a 4300 dígitos (padrão de segurança do Python)

        # Isso impede que o print() trave seu computador

        sys.set_int_max_str_digits(4300)

        try:

            num1 = float(input("Digite a base: "))

            num2 = float(input("Digite o expoente: "))

            # TRAVA DE SEGURANÇA: Impede expoentes absurdos

            if num2 > 5000:
                print("⚠️ Erro: Expoente muito alto! Para sua segurança, o limite é 5000.")

                continue

            # Tentativa inicial (rápida)

            resultado = num1 ** num2

            operacao = f"{num1:,.2f} ^ {num2:,.2f} = {resultado:,.2f}"

            print(f"Resultado: {resultado:,.2f}")


        except OverflowError:

            try:

                # Se falhar como float, tenta como inteiro (número exato)

                print("Calculando número grande...")

                resultado = int(num1) ** int(num2)

                # O Python vai travar aqui se o número tiver mais de 4300 dígitos

                operacao = f"{int(num1)} ^ {int(num2)} = {resultado}"

                print(f"Resultado: {resultado}")


            except ValueError:

                print("❌ Erro: O resultado é tão grande que o Python não consegue nem exibir na tela!")

                continue

            except Exception as e:

                print(f"❌ Erro inesperado: {e}")

                continue


        except Exception as e:

            print(f"❌ Erro: {e}")

            continue

        # Só salva se der tudo certo

        ultimo_resultado = resultado

        historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:

            arquivo.write(operacao + "\n")

    elif opcao == "7":
        num = float(input("Digite o número: "))

        if num < 0:
            print("Erro: não existe raiz quadrada real de número negativo.")
            continue

        resultado = num ** 0.5
        ultimo_resultado = resultado

        operacao = f"√{num:,.2f} = {resultado:,.2f}"

        print(f"Resultado: {resultado:,.2f}")

        historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(operacao + "\n")

    elif opcao == "8":
        porcentagem = float(input("Digite a porcentagem: "))
        numero = float(input("Digite o número: "))

        resultado = (porcentagem / 100) * numero
        ultimo_resultado = resultado

        operacao = f"{porcentagem:,.2f}% de {numero:,.2f} = {resultado:,.2f}"

        print(f"Resultado: {resultado:,.2f}")

        historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(operacao + "\n")

    elif opcao == "9":
        num1 = int(input("Digite o primeiro número: "))
        num2 = int(input("Digite o segundo número: "))

        if num2 == 0:
            print("Erro: divisão por zero!")
            continue

        resultado = num1 % num2
        ultimo_resultado = resultado

        operacao = f"{num1} % {num2} = {resultado}"

        print(f"Resultado: {resultado:,.2f}")

        historico.append(operacao)

        with open("historico.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(operacao + "\n")

    elif opcao == "10":
        memoria = ultimo_resultado
        print(f"Memória atual: {memoria:,.2f}")

    elif opcao == "11":
        print(f"Memória atual: {memoria:,.2f}")

    elif opcao == "12":
        memoria = 0
        print("Memória limpa!")


    elif opcao == "13":

        if len(historico) == 0:

            print("Nenhum histórico para exportar.")


        else:

            agora = datetime.datetime.now()

            nome_arquivo = f"historico_{agora.strftime('%Y-%m-%d_%H-%M')}.csv"

            with open(nome_arquivo, "w", encoding="utf-8-sig", newline="") as arquivo:

                writer = csv.writer(arquivo, delimiter=";")

                writer.writerow(["Operacao"])

                for item in historico:
                    writer.writerow([item])

            print(f"Histórico exportado para {nome_arquivo}!")

    else:
        print("Opção inválida!")