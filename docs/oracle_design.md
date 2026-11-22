# Projekt docelowej wyroczni kwantowej

## 1. Definicja wyroczni

Wyrocznia będzie identyfikować klucze 8-bitowego szyfru, które dla znanego tekstu jawnego $P$ generują oczekiwany szyfrogram $C$.

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
- $P$ – znany tekst jawny,
- $C$ – oczekiwany szyfrogram,
- $E_K(P)$ – wynik szyfrowania tekstu $P$ kluczem $K$.

Wyrocznia realizuje operację zmiany fazy:

$$
O_f|K\rangle = (-1)^{f(K)}|K\rangle
$$

Klucze spełniające warunek $E_K(P)=C$ zostają oznaczone zmianą fazy o 180°, natomiast pozostałe stany nie ulegają zmianie.

Wyrocznia nie wymaga znajomości poszukiwanego klucza ani wykonywania pomiarów rejestru kwantowego.

## 2. Struktura wyroczni

Przewiduje się wykorzystanie następujących rejestrów:

| Rejestr | Rozmiar | Przeznaczenie |
|---|---|---|
| `key` | 8 kubitów | Reprezentacja kandydatów na klucz |
| `ciphertext` | Zależny od szyfru | Przechowywanie wyniku szyfrowania |
| `ancilla` | Zależny od implementacji | Kubity pomocnicze |

Rozmiar rejestru `ciphertext` zostanie określony po ustaleniu długości bloku szyfru. Nie zakłada się, że 8-bitowy klucz musi oznaczać również 8-bitowy blok danych.

### Schemat działania

```text
       Rejestr klucza |K>
                |
                v
    +-----------------------+
    | Odwracalne szyfrowanie|
    |       E_K(P)          |
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
    | Odwrócenie obliczeń   |
    +-----------------------+
                |
                v
       (-1)^f(K) |K>
```

## 3. Sposób weryfikacji klucza

Wyrocznia będzie realizowana w czterech etapach.

### 3.1. Szyfrowanie

Odwracalny obwód kwantowy oblicza szyfrogram dla kluczy reprezentowanych przez rejestr `key`.

$$
|K\rangle|0\rangle
\xrightarrow{U_E}
|K\rangle|E_K(P)\rangle
$$

### 3.2. Porównanie szyfrogramu

Otrzymany wynik zostaje porównany z oczekiwaną wartością $C$.

Porównanie można zrealizować za pomocą operacji kontrolowanych:

1. Odwrócenie bramką X tych bitów rejestru wyniku, którym odpowiada `0` we wzorcu $C$.
2. Zastosowanie wielokrotnie kontrolowanej operacji fazowej, aktywnej wyłącznie przy zgodności wszystkich bitów.
3. Ponowne zastosowanie odpowiednich bramek X w celu przywrócenia rejestru.

### 3.3. Oznaczenie poprawnego klucza

Jeśli wynik szyfrowania jest zgodny z oczekiwanym szyfrogramem, amplituda odpowiadającego mu klucza zmienia znak:

$$
|K\rangle \rightarrow -|K\rangle
$$

W przeciwnym przypadku faza pozostaje bez zmian.

### 3.4. Uncomputation

Po zmianie fazy obliczenia szyfrowania zostają odwrócone.

$$
(-1)^{f(K)}|K\rangle|E_K(P)\rangle
\xrightarrow{U_E^\dagger}
(-1)^{f(K)}|K\rangle|0\rangle
$$

Rejestry pomocnicze wracają do stanów początkowych, natomiast oznaczenie fazowe poprawnych kluczy zostaje zachowane.

## 4. Integracja z implementacją szyfru

Wyrocznia będzie wykorzystywać odwracalny obwód szyfrujący przygotowany w ramach równoległej części projektu.

Proponowany schemat integracji:

```python
def oracle(key, plaintext, expected_ciphertext):

    # 1. Obliczenie szyfrogramu
    #    z użyciem odwracalnego obwodu kwantowego

    # 2. Porównanie wyniku z expected_ciphertext

    # 3. Warunkowa zmiana fazy

    # 4. Odwrócenie obliczeń szyfrowania
    #    i przywrócenie rejestrów pomocniczych
```

Powyższy fragment przedstawia planowaną strukturę funkcji.

Po ustaleniu specyfikacji szyfru konieczne będzie określenie:

- długości bloku tekstu jawnego i szyfrogramu,
- interfejsu odwracalnej funkcji szyfrującej,
- sposobu reprezentacji i indeksowania bitów,
- liczby oraz przeznaczenia kubitów pomocniczych.

## 5. Weryfikacja poprawności wyroczni

Poprawność implementacji zostanie sprawdzona poprzez porównanie jej działania z klasycznym przeszukiwaniem przestrzeni kluczy (*brute force*).

Planowane testy obejmują:

1. **Zgodność szyfrowania** - porównanie wyników kwantowego obwodu szyfrującego z implementacją klasyczną.
2. **Poprawność oznaczania kluczy** – sprawdzenie, czy zmiana fazy dotyczy dokładnie kluczy spełniających warunek $E_K(P)=C$.
3. **Odwracalność obliczeń** – weryfikację przywrócenia rejestrów pomocniczych do stanów początkowych.
4. **Wiele poprawnych kluczy** – sprawdzenie, czy wyrocznia oznacza wszystkie klucze spełniające warunek.
5. **Integrację z Groverem** – porównanie wyników wyszukiwania kwantowego z rezultatami klasycznego brute force.

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