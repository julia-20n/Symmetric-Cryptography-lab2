import re
from collections import Counter
import matplotlib.pyplot as plt
from tabulate import tabulate

def load_text(filename):
    with open(filename, "r", encoding="utf-8", errors="replace") as file:
        text = file.read().lower()
    text = text.replace("ё", "е")
    text = re.sub(r'[^а-я]', '', text)
    return text


def encrypt_vigenere(text, key):
    alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
    key = key.lower()
    result = []
    key_indices = [alphabet.index(k) for k in key]

    for i, char in enumerate(text):
        if char in alphabet:
            t_i = alphabet.index(char)
            k_i = key_indices[i % len(key)]
            result.append(alphabet[(t_i + k_i) % len(alphabet)])
    return ''.join(result)

def index_of_coincidence(text):
    freqs = Counter(text)
    N = len(text)
    if N <= 1:
        return 0
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))

def run_vigenere_ic_analysis(filename):
    text = load_text(filename)
    print(f"Довжина відкритого тексту: {len(text)} символів")

    ic_plain = index_of_coincidence(text)
    print(f"\nІндекс відповідності для відкритого тексту: {ic_plain:.10f}\n")

    key_examples = {
        2: "да", 3: "нет", 4: "мир", 5: "земля",
        10: "безопасный", 11: "информация",
        12: "криптография", 13: "шифрование",
        14: "распределение", 15: "программировать",
        16: "математическиекоды", 17: "открытыетексты",
        18: "перехватсигналов", 19: "университетский",
        20: "криптографический"
    }

    results = []
    for r in list(range(2, 6)) + list(range(10, 21)):
        key = key_examples[r]
        encrypted = encrypt_vigenere(text, key)
        ic_encrypted = index_of_coincidence(encrypted)
        print(f"Ключ довжини {r} ({key}):")
        print(f"Зашифрований текст:\n{encrypted}")
        print(f"Індекс відповідності: {ic_encrypted:.10f}\n")
        results.append((r, ic_encrypted))

    headers = ["Довжина ключа (r)", "Індекс відповідності"]
    table_data = [[r, f"{ic:.10f}"] for r, ic in results]
    print(tabulate([headers] + table_data, headers="firstrow", tablefmt="grid"))

    lengths, ics = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, ics, marker='o', label='Індекс відповідності')
    plt.axhline(y=ic_plain, color='red', linestyle='--', label='IВ відкритого тексту')
    plt.title('Індекс відповідності для різних довжин ключа (r)')
    plt.xlabel('Довжина ключа (r)')
    plt.ylabel('Індекс відповідності')
    plt.xticks(lengths)
    plt.grid()
    plt.legend()
    plt.show()

file_path = "text.txt"
run_vigenere_ic_analysis(file_path)