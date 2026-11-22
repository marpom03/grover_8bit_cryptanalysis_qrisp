# Projekt docelowej wyroczni kwantowej

## 1. Definicja wyroczni

Wyrocznia będzie identyfikować klucze 8-bitowego szyfru blokowego MiniFeistel-8, które dla znanego tekstu jawnego $P$ generują oczekiwany szyfrogram $C$.

Warunek poprawności klucza:

$$
f(K) =
\begin{cases}
1 & \text{gdy } E_K(P) = C \\
0 & \text{w przeciwnym przypadku}
\end{cases}
$$

gdzie:
- $K$ – kandydat na 8-bitowy klucz,
- $P$ – znany 8-bitowy tekst jawny,
- $C$ – oczekiwany 8-bitowy szyfrogram,
- $E_K(P)$ – wynik szyfrowania tekstu $P$ kluczem $K$.

Wyrocznia realizuje operację zmiany fazy:

$$
O_f|K\rangle = (-1)^{f(K)}|K\rangle
$$

Klucze spełniające warunek $E_K(P)=C$ zostają oznaczone zmianą fazy o 180°, natomiast pozostałe stany nie ulegają zmianie.

Wyrocznia nie wymaga znajomości poszukiwanego klucza ani wykonywania pomiarów rejestru kwantowego.

## 2. Struktura wyroczni

Wyrocznia będzie wykorzystywać następujące rejestry kwantowe:

| Rejestr | Rozmiar | Przeznaczenie |
|---|---|---|
| `key_register` | 8 kubitów | Reprezentacja kandydatów na klucz |
| `left` | 4 kubity | Lewa połowa bloku MiniFeistel-8 |
| `right` | 4 kubity | Prawa połowa bloku MiniFeistel-8 |
| `ancilla` (opcjonalny) | Zależny od implementacji | Kubity pomocnicze wykorzystywane podczas porównywania i oznaczania stanów |

Rejestry `left` i `right` reprezentują łącznie 8-bitowy blok danych. Po wykonaniu szyfrowania przechowują odpowiednio starsze i młodsze cztery bity szyfrogramu.

Rejestr `key_register` będzie reprezentowany przez `QuantumFloat(8)`, zgodnie z implementacją kwantowego szyfru.

### Schemat działania

```text
          key_register (8 kubitów)
                    |
                    v
        +-----------------------+
        | Odwracalne szyfrowanie|
        |     MiniFeistel-8     |
        +-----------------------+
                    |
                    v
        +-----------------------+
        | left (4 kubity)       |
        | right (4 kubity)      |
        +-----------------------+
                    |
                    v
        +-----------------------+
        | Porównanie wyniku     |
        | z szyfrogramem C      |
        +-----------------------+
                    |
                    v
        +-----------------------+
        | Warunkowa zmiana fazy |
        +-----------------------+
                    |
                    v
        +-----------------------+
        | Uncomputation         |
        | Odwrócenie szyfrowania|
        +-----------------------+
                    |
                    v
           (-1)^f(K) |K>
```

## 3. Sposób weryfikacji klucza

Wyrocznia będzie realizowana w czterech etapach.

### 3.1. Szyfrowanie

Odwracalny obwód MiniFeistel-8 oblicza szyfrogram dla kluczy reprezentowanych przez rejestr `key_register`.

$$
|K\rangle|P\rangle
\xrightarrow{U_E}
|K\rangle|E_K(P)\rangle
$$

Dla podziału bloku na dwie czterobitowe połowy:

$$
|K\rangle|L_0\rangle|R_0\rangle
\xrightarrow{U_E}
|K\rangle|L_3\rangle|R_3\rangle
$$

Obliczenia będą wykonywane za pomocą funkcji:

```python
quantum_encrypt_with_key(plaintext, key_register)
```

Funkcja zwraca rejestry `left` oraz `right`, zawierające wynik trzech rund szyfrowania.

### 3.2. Porównanie szyfrogramu

Otrzymany szyfrogram zostaje porównany z oczekiwaną wartością $C$.

Dla przykładowych danych:

```text
P = 10110010 (0xB2)
C = 01100010 (0x62)
```

Oczekiwany szyfrogram dzielony jest na dwie części:

```text
C_left  = 0110
C_right = 0010
```

Porównanie można zrealizować za pomocą operacji kontrolowanych:

1. Odwrócenie bramką X tych kubitów rejestrów `left` i `right`, którym odpowiada `0` we wzorcu oczekiwanego szyfrogramu.
2. Zastosowanie wielokrotnie kontrolowanej operacji fazowej, aktywnej wyłącznie wtedy, gdy wszystkie osiem kubitów odpowiada wartości `1`.
3. Ponowne zastosowanie odpowiednich bramek X w celu przywrócenia rejestrów szyfrogramu.

Operacje porównywania nie wymagają wykonywania pomiaru.

### 3.3. Oznaczenie poprawnego klucza

Jeżeli wynik szyfrowania jest zgodny z oczekiwanym szyfrogramem, amplituda odpowiadającego mu klucza zmienia znak:

$$
|K\rangle \rightarrow -|K\rangle
$$

W przeciwnym przypadku faza pozostaje bez zmian.

Oznaczenie realizowane jest za pomocą kontrolowanej operacji fazowej.

### 3.4. Uncomputation

Po oznaczeniu poprawnych kluczy obliczenia szyfrowania zostają odwrócone.

$$
(-1)^{f(K)}|K\rangle|E_K(P)\rangle
\xrightarrow{U_E^\dagger}
(-1)^{f(K)}|K\rangle|P\rangle
$$

Wykorzystana zostanie funkcja:

```python
quantum_decrypt_with_key(left, right, key_register)
```

Po odwróceniu obliczeń rejestry `left` i `right` wracają do wartości początkowego tekstu jawnego, natomiast zmiana fazy poprawnych kluczy zostaje zachowana.

Przed kolejnym wykorzystaniem wyroczni rejestry pomocnicze muszą zostać odpowiednio przywrócone do stanu początkowego i zwolnione.

## 4. Integracja z implementacją szyfru

Wyrocznia będzie wykorzystywać odwracalny obwód szyfrujący zaimplementowany w pliku `src/quantum_cipher.py`.

Najważniejsze funkcje:

| Funkcja | Przeznaczenie |
|---|---|
| `quantum_encrypt_with_key()` | Szyfrowanie z kwantowym rejestrem klucza |
| `quantum_decrypt_with_key()` | Odwracanie obliczeń szyfrowania |

Proponowany schemat integracji:

```python
def oracle(key_register, plaintext, expected_ciphertext):

    # 1. Encrypt plaintext using the quantum key register
    left, right = quantum_encrypt_with_key(
        plaintext,
        key_register,
    )

    # 2. Compare left and right registers
    #    with expected_ciphertext

    # 3. Apply a phase flip to matching key states

    # 4. Reverse encryption without measurement
    left, right = quantum_decrypt_with_key(
        left,
        right,
        key_register,
    )

    # 5. Restore and release auxiliary registers
```


Na etapie implementacji konieczne będzie opracowanie operacji porównywania 8-bitowego szyfrogramu z oczekiwaną wartością, realizacji warunkowej zmiany fazy oraz sposobu zarządzania rejestrami pomocniczymi.

## 5. Weryfikacja poprawności wyroczni

Poprawność implementacji zostanie sprawdzona poprzez porównanie jej działania z klasycznym przeszukiwaniem przestrzeni kluczy (*brute force*).

Planowane testy obejmują:

1. **Zgodność szyfrowania** – porównanie wyników kwantowego obwodu szyfrującego z implementacją klasyczną.
2. **Poprawność oznaczania kluczy** – sprawdzenie, czy zmiana fazy dotyczy dokładnie kluczy spełniających warunek $E_K(P)=C$.
3. **Odwracalność obliczeń** – weryfikację przywrócenia rejestrów pomocniczych do stanów początkowych.
4. **Wiele poprawnych kluczy** – sprawdzenie, czy wyrocznia oznacza wszystkie klucze spełniające warunek.
5. **Integrację z Groverem** – porównanie wyników wyszukiwania kwantowego z rezultatami klasycznego brute force.

Dla referencyjnej pary:

```text
Plaintext:  0xB2
Ciphertext: 0x62
```

klasyczny brute force wskazuje klucz:

```text
0x6D
```

Wynik ten będzie stanowił punkt odniesienia podczas weryfikacji wyroczni.

Jeżeli jedna para tekst jawny–szyfrogram nie pozwoli na jednoznaczne wskazanie klucza, przewiduje się rozszerzenie warunku weryfikacji na kilka znanych par:

$$
f(K)=1
\iff
\forall i,\ E_K(P_i)=C_i
$$

## Źródła

1. Grover, L. K. (1996). *A Fast Quantum Mechanical Algorithm for Database Search*.  
   https://arxiv.org/abs/quant-ph/9605043

2. Qrisp – *Grover's Algorithm*.  
   https://qrisp.eu/reference/Algorithms/Grover.html

3. Qrisp – *ControlEnvironment*.  
   https://qrisp.eu/reference/Quantum%20Environments/ControlEnvironment.html

4. Qrisp – *ConjugationEnvironment*.  
   https://qrisp.eu/reference/Quantum%20Environments/ConjugationEnvironment.html

5. Qrisp – *Uncomputation*.  
   https://qrisp.eu/reference/Core/Uncomputation.html