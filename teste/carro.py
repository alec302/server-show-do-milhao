class Carro:
    def __init__(self, marca, modelo, cor, ano):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
    
    def acelerar(self):
        print(f"O carro {self.marca} {self.modelo} está acelerando VROOOOMMMM.")

    def getInfo(self):
        return {
            "marca": self.marca,
            "modelo": self.modelo,
            "cor": self.cor,
            "ano": self.ano
        }
    
carro = Carro("Volkswagen", "Fusca", "azul", 1970)
carro2 = Carro("Chevrolet", "Corsa", "preto", 2000)

carro2.acelerar()
carro2.getInfo()


print(carro.getInfo())
