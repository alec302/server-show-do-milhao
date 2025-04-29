class Aluno:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email
    
    def entrar(self):
        print(f"Aluno {self.nome} entrou no sistema.")

    def getInfo(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email
        }
    
Alec = Aluno(1, "Alec", "alec.almeidaduarte@gmail.com")
Alec.entrar()