import sys

n = input("Mande um numero: ")


try:
    n = int(n)
except ValueError:
    sys.exit(print("Isso não é um número inteiro."))

    





