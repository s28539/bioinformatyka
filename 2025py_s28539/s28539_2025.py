# generator_fasta.py
# --------------------------------------------------------
# CEL PROGRAMU:
# Program służy do generowania losowej sekwencji DNA,
# zapisania jej do pliku w formacie FASTA oraz prezentacji statystyk.
# Dodatkowo program wstawia imię użytkownika w losowe miejsce sekwencji
# (bez wpływu na statystyki i długość sekwencji).
#
# KONTEKST ZASTOSOWANIA:
# Program może być używany do nauki bioinformatyki, testowania narzędzi analizy DNA
# lub generowania danych symulacyjnych do ćwiczeń algorytmicznych.
# --------------------------------------------------------

import random  # import biblioteki random do generowania liczb losowych
import os  # MODIFIED (dodano os do sprawdzania zapisu pliku i informowania użytkownika)


# Funkcja do generowania sekwencji DNA
def generate_dna_sequence(length):
    # Zwraca ciąg losowych nukleotydów o określonej długości
    return ''.join(random.choices('ACGT', k=length))


# Funkcja do wstawiania imienia w losowym miejscu w sekwencji
def insert_name_in_sequence(sequence, name):
    pos = random.randint(0, len(sequence))  # losowa pozycja
    return sequence[:pos] + name + sequence[pos:], pos  # zwraca nową sekwencję i pozycję imienia


# Funkcja do obliczania statystyk
def calculate_statistics(sequence):
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}  # liczba wystąpień każdego nukleotydu
    total = sum(counts.values())  # łączna liczba nukleotydów
    stats = {nuc: round((count / total) * 100, 2) for nuc, count in counts.items()}  # procentowa zawartość
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    ratio = round(cg / (at+cg), 2) if at > 0 else 'undefined'  # stosunek CG/AT
    return stats, ratio


# Funkcja do zapisu do pliku FASTA
def save_to_fasta(filename, header, sequence_with_name):
    with open(filename, 'w') as file:
        file.write(f">{header}\n")
        # MODIFIED (dodano łamanie sekwencji co 60 znaków dla standardu FASTA):
        # ORIGINAL:
        # for i in range(0, len(sequence_with_name), 60):
        #     file.write(sequence_with_name[i:i+60] + '\n')
        # MODIFIED (standard FASTA dopuszcza 60, zapewniając czytelność):
        for i in range(0, len(sequence_with_name), 60):
            file.write(sequence_with_name[i:i + 60] + '\n')


# Główna funkcja programu
def main():
    # Pobranie danych od użytkownika
    seq_id = input("Podaj ID sekwencji: ").strip()
    description = input("Podaj opis sekwencji: ").strip()

    # MODIFIED (dodano możliwość wpisania imienia użytkownika zamiast wartości na sztywno):
    # ORIGINAL:
    # name = "Mateusz"  # imię użytkownika wstawiane do sekwencji
    # MODIFIED (umożliwienie użytkownikowi podania imienia):
    name = input("Podaj swoje imię (zostanie wstawione do sekwencji): ").strip()

    # MODIFIED (dodano walidację wejścia dla długości sekwencji):
    # ORIGINAL:
    # try:
    #     length = int(input("Podaj długość sekwencji DNA: "))
    # except ValueError:
    #     print("Długość musi być liczbą całkowitą.")
    #     return
    # MODIFIED (dodano walidację, że długość > 0):
    try:
        length = int(input("Podaj długość sekwencji DNA: "))
        if length <= 0:
            raise ValueError
    except ValueError:
        print("Błąd: Podana długość musi być dodatnią liczbą całkowitą.")
        return

    # Generowanie sekwencji
    dna_sequence = generate_dna_sequence(length)

    # Wstawienie imienia
    sequence_with_name, name_pos = insert_name_in_sequence(dna_sequence, name)

    # Obliczanie statystyk tylko z czystej sekwencji DNA
    stats, cg_at_ratio = calculate_statistics(dna_sequence)

    # Utworzenie nagłówka FASTA
    fasta_header = f"{seq_id} {description}"

    # Zapis sekwencji do pliku
    fasta_filename = f"{seq_id}.fasta"
    save_to_fasta(fasta_filename, fasta_header, sequence_with_name)

    # Wyświetlenie statystyk
    print("\nStatystyki sekwencji (bez imienia):")
    for nuc, pct in stats.items():
        print(f"{nuc}: {pct}%")
    print(f"%CG: {cg_at_ratio*100}%")
    print(f"Imię '{name}' zostało wstawione na pozycji: {name_pos}")

    # MODIFIED (dodano potwierdzenie zapisania pliku):
    # ORIGINAL:
    # print(f"Sekwencja została zapisana do pliku: {fasta_filename}")
    # MODIFIED (sprawdzenie czy plik istnieje i komunikat):
    if os.path.exists(fasta_filename):
        print(f"Sekwencja została poprawnie zapisana do pliku: {fasta_filename}")
    else:
        print("Błąd podczas zapisu pliku.")


# Uruchomienie głównej funkcji
if __name__ == "__main__":
    main()
