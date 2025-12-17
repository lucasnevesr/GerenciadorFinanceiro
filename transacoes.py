

class Transacao:
    def __init__(self, tipo, valor, data, categoria):
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def __str__(self):
        return (
            f"Valor: R$ {self.valor:.2f} | Data: {self.data}| Tipo: {self.tipo.upper()} | Categoria: {self.categoria}")
