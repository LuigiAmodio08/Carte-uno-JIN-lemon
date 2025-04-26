class Giocatore:
    def __init__(self, nome):
        self.nome = nome
        self.mano = [] 

    def pesca(self, mazzo, num=1):
        """Il giocatore pesca una o più carte dal mazzo."""
        for _ in range(num):
            carta_pescata = mazzo.pesca_carta()
            if carta_pescata:
                self.mano.append(carta_pescata)

    def mostra_mano(self):
        """Mostra le carte in mano al giocatore."""
        return [str(carta) for carta in self.mano]