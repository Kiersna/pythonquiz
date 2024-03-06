import random
import os

def wyswietlanie():
    print("1. Zagraj w quiz")
    print("2. Wyswietl ranking")
    print("3. Resetuj ranking")
    print("0. Zakoncz quiz.")

def wczytaj_pytania(nazwa_pliku):
    pytania = []
    with open(nazwa_pliku, 'r') as plik:
        linie = plik.readlines()
        liczba_linii = len(linie)
        for i in range(0, liczba_linii, 6):
            if i + 5 < liczba_linii:
                pytanie = linie[i].strip()
                opcje = [linia.strip() for linia in linie[i+1:i+5]]
                odpowiedz = linie[i+5].strip()
                pytania.append((pytanie, opcje, odpowiedz))
    return pytania

def wyswietl_pytanie(pytanie, opcje):
    print(pytanie)
    for i in range(len(opcje)):
        opcja = opcje[i]
        print(opcja)

def sprawdz_odpowiedz(odpowiedz, poprawna_odpowiedz):
    return odpowiedz.lower() == poprawna_odpowiedz.lower()

def sprawdz_nick(nick):
    with open("ranking.txt", 'r') as plik:
        linie = plik.readlines()
        liczba_linii = len(linie)
        for i in range(0, liczba_linii, 2):
            if linie[i] == nick:
                return True
        return False

def dopisz_do_rankingu(nick, procent):
    with open("ranking.txt", 'a') as plik:
        plik.seek(0, 2)  # Przejdź na koniec pliku
        #if plik.tell() != 0:  # Sprawdź, czy plik nie jest pusty
        #    plik.write('\n')  # Jeśli nie jest pusty, dodaj nową linię przed zapisaniem
        plik.write(nick + '\n')
        plik.write(str(procent) + '\n')

def is_empty_file():
    with open("ranking.txt", 'r') as file:
        return not bool(file.read())

def wypisz_ranking():
    with open("ranking.txt", 'r') as plik:
        if is_empty_file():
            print("Ranking jest pusty!")
        else:
            print("Ranking:")
            dane = []
            linie = plik.readlines()
            for i in range(0, len(linie), 2):
                nick = linie[i].strip()
                procent = float(linie[i+1].strip())
                dane.append((nick, procent))
            
            # Sortowanie danych względem procentu malejąco
            dane.sort(key=lambda x: x[1], reverse=True)
            
            for nick, procent in dane:
                print(f"{nick}: {procent}%")

def resetuj_ranking():
    with open("ranking.txt", 'w') as plik:
        plik.write("")
    print("Ranking został zresetowany!")

def main():
    nazwa_pliku = "quiz.txt"
    nick = input("Podaj swoj nick: ")
    if(sprawdz_nick(nick)):
        while(sprawdz_nick(nick)):
            nick = input("Taki nick juz istnieje. Podaj inny nick: ")
    liczba_pytan_do_wyboru = 0
    while(liczba_pytan_do_wyboru == 0):
        try:
            liczba_pytan_do_wyboru = int(input("Ile pytań chcesz w quizie (od 1 do 10): "))
        except:
            print("musisz podac liczbe!")
    
    if not (1 <= liczba_pytan_do_wyboru <= 10):
        print("Podano nieprawidłową liczbę pytań. Quiz zacznie się z domyśl ną liczbą pytań (5).")
        liczba_pytan_do_wyboru = 5  
    
    pytania = wczytaj_pytania(nazwa_pliku)
    wybrane_pytania = random.sample(pytania, liczba_pytan_do_wyboru)
    
    liczba_punktow = 0
    index = 1
    for pytanie, opcje, poprawna_odpowiedz in wybrane_pytania:
        wyswietl_pytanie(pytanie, opcje)
        odpowiedz_uzytkownika = input("Odpowiedź: ")
        odpowiedz_uzytkownika = odpowiedz_uzytkownika.lower()
        while odpowiedz_uzytkownika not in {'a', 'b', 'c', 'd'}:
            odpowiedz_uzytkownika = input("Podales niepoprawnie odpowiedz! Podaj ponownie. Odpowiedź: ")
            odpowiedz_uzytkownika = odpowiedz_uzytkownika.lower()
        if sprawdz_odpowiedz(odpowiedz_uzytkownika, poprawna_odpowiedz):
            print("Poprawna odpowiedź!")
            print("----------------------------------------------")
            liczba_punktow += 1
        else:
            print(f"Niepoprawna odpowiedź. Poprawna odpowiedz to: {poprawna_odpowiedz}")
            print("----------------------------------------------")
        index += 1

    procent = round((liczba_punktow / liczba_pytan_do_wyboru)*100, 2)
    print(f"Zdobyłeś {liczba_punktow} punktów z {liczba_pytan_do_wyboru} pytań. Jest to {procent}% poprawnych odpowiedzi")
    dopisz_do_rankingu(nick, procent)

wybor = -1
while wybor != 0:
    wybor = -1
    wyswietlanie()
    try:
        wybor = int(input("Wybierz liczbę: "))
    except:
        print("musisz podac liczbe!")
    if wybor == 0:
        print("Zakończono quiz")
        exit()
    elif wybor == 1:
        main()
    elif wybor == 2:
        wypisz_ranking()
    elif wybor == 3:
        resetuj_ranking()
    else:
        print("Zły wybór. Wybierz coś innego.")