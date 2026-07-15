import random

def jogo_aposta():
    print("Bem-vindo ao jogo de aposta com números!")
    saldo = int(input('Digite o valor que você quer depositar: R$'))

    while saldo > 0:
        print(f"\nSeu saldo atual é: R${saldo}")
        aposta = float(input("Quanto você deseja apostar? R$"))

        if aposta > saldo:
            print("Você não tem saldo suficiente para essa aposta!")
            continue

        numero_aleatorio = random.randint(1, 3)  # O número que o jogador precisa adivinhar
        palpite = int(input("Adivinhe um número entre 1 e 3: "))

        if palpite == numero_aleatorio:
            print(f"Parabéns! Você acertou o número, que era {numero_aleatorio}.")
            ganho = aposta * 2  # O jogador ganha o dobro da aposta
            saldo += ganho
            print(f"Você ganhou R${ganho}! Seu novo saldo é: R${saldo}")
        else:

            print(f"Você errou! O número correto era {numero_aleatorio}.")
            saldo -= aposta  # O jogador perde a aposta
            print(f"Você perdeu R${aposta}. Seu novo saldo é: R${saldo}")

        if saldo <= 0:
            print("Você ficou sem saldo! Fim de jogo.")
            break

        # Pergunta se o jogador quer continuar ou sacar
        opcao = input("Você deseja (C)ontinuar jogando ou (S)acar seu saldo? ").strip().lower()
        if opcao == 's':
            print(f"\nVocê sacou R${saldo}. Fim de jogo!")
            break
        elif opcao != 'c':
            print("Opção inválida. Continuando o jogo...")

# Iniciar o jogo
jogo_aposta()