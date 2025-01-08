# -*- coding: utf-8 -*-
"""
Created on Mon dic  2 16:58:28 2024

@author: montismattia
"""
import hashlib

class Prodotto:
    def __init__(self, nome, prezzo, quantità_disponibile):
        # Inizializza le proprietà del prodotto
        self.nome = nome  # Nome del prodotto
        self.prezzo = prezzo  # Prezzo del prodotto
        self.quantità_disponibile = quantità_disponibile  # Quantità disponibile nel magazzino

    def __str__(self):
        # Rappresentazione in stringa del prodotto
        return f"{self.nome} - €{self.prezzo} (Disponibili: {self.quantità_disponibile})"

class Magazzino:
    def __init__(self):
        # Dizionario per memorizzare gli articoli disponibili nel magazzino
        # Struttura: {nome: [prezzo, quantità_disponibile]}
        self.articoli = {}

    def aggiungi_articolo(self, prodotto):
        # Aggiunge un prodotto al magazzino o aggiorna la quantità se già esistente
        nome_lower = prodotto.nome.lower()
        if nome_lower in self.articoli:
            # Se il prodotto esiste, aumenta la quantità
            self.articoli[nome_lower][1] += prodotto.quantità_disponibile
        else:
            # Altrimenti, aggiungi un nuovo prodotto al magazzino
            self.articoli[nome_lower] = [prodotto.prezzo, prodotto.quantità_disponibile]

    def elimina_articolo(self, nome_prodotto):
        # Rimuove un prodotto dal magazzino in base al nome
        nome_lower = nome_prodotto.lower()
        if nome_lower in self.articoli:
            prezzo, quantita = self.articoli[nome_lower]
            if quantita == 0:
                # Rimuovi completamente se la quantità è zero
                del self.articoli[nome_lower]
                print(f"Articolo {nome_prodotto} rimosso dal magazzino poiché la quantità è pari a 0.")
            else:
                print(f"L'articolo {nome_prodotto} ha attualmente {quantita} unità disponibili.")
                try:
                    quantità_da_eliminare = int(input("Inserisci il numero di unità da eliminare: "))
                    if quantità_da_eliminare > quantita:
                        print("Errore: non puoi eliminare più unità di quelle disponibili.")
                    elif quantità_da_eliminare == quantita:
                        # Rimuovi completamente l'articolo
                        del self.articoli[nome_lower]
                        print(f"Rimosso completamente l'articolo {nome_prodotto} dal magazzino.")
                    else:
                        # Riduci la quantità disponibile
                        self.articoli[nome_lower][1] -= quantità_da_eliminare
                        print(f"Rimosse {quantità_da_eliminare} unità di {nome_prodotto}. Restano {self.articoli[nome_lower][1]} unità.")
                except ValueError:
                    print("Errore: devi inserire un numero valido.")
        else:
            print(f"Articolo {nome_prodotto} non trovato nel magazzino.")

    def mostra_prodotti(self):
        # Mostra tutti i prodotti disponibili nel magazzino
        if not self.articoli:
            print("Il magazzino è vuoto.")
        else:
            for nome, (prezzo, quantita) in self.articoli.items():
                print(f"{nome} - €{prezzo} (Disponibili: {quantita})")

class Carrello:
    def __init__(self, magazzino):
        # Dizionario per memorizzare i prodotti nel carrello
        # Struttura: {nome: [prezzo, quantità]}
        self.prodotti = {}
        self.magazzino = magazzino  # Riferimento al magazzino

    def aggiungi_prodotto(self, nome_prodotto, quantita):
        # Aggiunge un prodotto al carrello se disponibile nel magazzino
        nome_lower = nome_prodotto.lower()
        if nome_lower in self.magazzino.articoli and quantita <= self.magazzino.articoli[nome_lower][1]:
            if nome_lower in self.prodotti:
                # Se già nel carrello, aumenta la quantità
                self.prodotti[nome_lower][1] += quantita
            else:
                # Altrimenti, aggiungi il prodotto al carrello
                prezzo = self.magazzino.articoli[nome_lower][0]
                self.prodotti[nome_lower] = [prezzo, quantita]
            # Riduci la quantità disponibile nel magazzino
            self.magazzino.articoli[nome_lower][1] -= quantita
            print(f"Aggiunto {quantita} di {nome_prodotto} al carrello.")
        else:
            print(f"Non ci sono abbastanza {nome_prodotto} disponibili nel magazzino.")

    def rimuovi_prodotto(self, nome_prodotto):
        # Rimuove un prodotto dal carrello e ripristina la quantità nel magazzino
        nome_lower = nome_prodotto.lower()
        if nome_lower in self.prodotti:
            quantita = self.prodotti[nome_lower][1]
            if nome_lower in self.magazzino.articoli:
                # Aggiungi di nuovo al magazzino
                self.magazzino.articoli[nome_lower][1] += quantita
            else:
                # Se non esiste più nel magazzino, ricrea l'articolo
                prezzo = self.prodotti[nome_lower][0]
                self.magazzino.articoli[nome_lower] = [prezzo, quantita]
            # Rimuovi dal carrello
            del self.prodotti[nome_lower]
            print(f"Rimosso {quantita} di {nome_prodotto} dal carrello.")
        else:
            print(f"{nome_prodotto} non presente nel carrello.")

    def mostra_totale(self):
        # Calcola e mostra il totale dei prodotti nel carrello
        tot = 0
        if not self.prodotti:
            print("Totale: 0€, carrello vuoto!")
        else:
            for prezzo, quantita in self.prodotti.values():
                tot += prezzo * quantita  # Prezzo * Quantità
            print(f"Totale: €{tot:.2f}")
        return tot

    def __str__(self):
        # Rappresentazione in stringa del contenuto del carrello
        if not self.prodotti:
            return "Il carrello è vuoto."
        else:
            return "\n".join([f"{quantita}x {nome} (€{prezzo} ciascuno)"
                              for nome, (prezzo, quantita) in self.prodotti.items()])

# Hash della password preimpostata per l'accesso dipendente
HASH_PASSWORD_DIPENDENTE = hashlib.sha256("securepassword".encode()).hexdigest()

def verifica_password(password_inserita):
    """
    Verifica la password inserita confrontandola con l'hash preimpostato.
    """
    hash_inserita = hashlib.sha256(password_inserita.encode()).hexdigest()
    return hash_inserita == HASH_PASSWORD_DIPENDENTE

def login_magazzino():
    """
    Esegue il login per l'accesso come dipendente
    """
    print("\n--- Accesso dipendente ---")
    nome_utente = input("Inserisci il nome utente: ")
    password = input("Inserisci password: ")

    if verifica_password(password):
        print(f"Benvenuto, {nome_utente}. Accesso al magazzino consentito.")
        return True
    else:
        print("Accesso negato. Utente o password errati.")
        return False

def dipendente_o_cliente():
    """
    Funzione principale per gestire l'interazione con clienti e dipendenti.
    """
    print("Login dipendente del magazzino o login cliente?")
    print("1. Dipendente")
    print("2. Cliente")

    scelta = input("Inserisci il tipo di profilo: ")

    if scelta == "1":
        if login_magazzino():
            # Interazione per dipendente
            while True:
                print("\nCosa vuoi fare nel magazzino?")
                print("1. Mostrare i prodotti disponibili")
                print("2. Aggiungere un prodotto al magazzino")
                print("3. Eliminare un prodotto dal magazzino")
                print("4. Esci")

                scelta_dipendente = input("Inserisci il numero dell'azione: ")

                if scelta_dipendente == "1":
                    print("\nProdotti disponibili nel magazzino:")
                    magazzino.mostra_prodotti()

                elif scelta_dipendente == "2":
                    nome_prodotto = input("\nInserisci il nome del prodotto da aggiungere: ")
                    prezzo = float(input("Inserisci il prezzo del prodotto: "))
                    quantità = int(input("Inserisci la quantità del prodotto: "))
                    prodotto = Prodotto(nome_prodotto, prezzo, quantità)
                    magazzino.aggiungi_articolo(prodotto)

                elif scelta_dipendente == "3":
                    nome_prodotto = input("\nInserisci il nome del prodotto da eliminare: ")
                    magazzino.elimina_articolo(nome_prodotto)

                elif scelta_dipendente == "4":
                    print("Uscita... Grazie per aver utilizzato il sistema di gestione del magazzino!")
                    break
                else:
                    print("Scelta non valida. Riprova.")
        else:
            print("Tornando al menu principale...")

    elif scelta == "2":
        # Interazione per cliente
        while True:
            print("\nCosa vuoi fare come cliente?")
            print("1. Mostrare i prodotti disponibili")
            print("2. Aggiungere un prodotto al carrello")
            print("3. Rimuovere un prodotto dal carrello")
            print("4. Visualizzare il totale del carrello")
            print("5. Esci")

            scelta_cliente = input("Inserisci il numero dell'azione: ")

            if scelta_cliente == "1":
                print("\nProdotti disponibili nel magazzino:")
                magazzino.mostra_prodotti()

            elif scelta_cliente == "2":
                nome_prodotto = input("\nInserisci il nome del prodotto da aggiungere: ")
                quantita = int(input("Inserisci la quantità da aggiungere: "))
                carrello.aggiungi_prodotto(nome_prodotto, quantita)

            elif scelta_cliente == "3":
                nome_prodotto = input("\nInserisci il nome del prodotto da rimuovere: ")
                carrello.rimuovi_prodotto(nome_prodotto)

            elif scelta_cliente == "4":
                print("\nCalcolando il totale del carrello:")
                carrello.mostra_totale()

            elif scelta_cliente == "5":
                print("Uscita... Grazie per aver visitato il nostro negozio!")
                break
            else:
                print("Scelta non valida. Riprova.")
    else:
        print("Scelta non valida. Tornando al menu principale...")

            


# Test
if __name__ == "__main__":
    magazzino = Magazzino()
    carrello = Carrello(magazzino)

    prodotti_iniziali = [
        Prodotto("Apple", 1.5, 100),
        Prodotto("Banana", 0.9, 150),
        Prodotto("Arancia", 2.0, 80),
        Prodotto("Pera", 1.2, 50),
    ]

    for prodotto in prodotti_iniziali:
        magazzino.aggiungi_articolo(prodotto)

    dipendente_o_cliente()