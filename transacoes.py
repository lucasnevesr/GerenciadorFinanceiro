import datetime

class Transacao:
    def __init__(self, tipo, valor, data, categoria, forma_pgto):
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.categoria = categoria
        self.forma_pgto = forma_pgto  # novo atributo

    def __str__(self):
        return (f"Valor: R$ {self.valor:.2f} | Data: {self.data}| Tipo: {self.tipo.upper()} | Categoria: {self.categoria} | Forma de Pagamento ou Recebimento: {self.forma_pgto}")

    @staticmethod
    def from_dict(dados):

        return Transacao(
            dados["tipo"],
            dados["valor"],
            dados["data"].date() if isinstance(dados["data"], datetime.datetime) else dados["data"],
            dados["categoria"],
            dados["forma_pgto"]   # novo elemento
        )