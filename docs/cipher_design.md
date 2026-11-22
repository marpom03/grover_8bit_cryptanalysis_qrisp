# Projekt szyfru 

## 1. Założenia szyfru

Przyjęto następujące założenia:

- 8-bitowy tekst jawny i szyfrogram,
- 8-bitowy klucz główny,
- trzy rundy sieci Feistela,
- odwracalność operacji szyfrowania.

Przestrzeń kluczy zawiera $2^8=256$ wartości, co umożliwia porównanie działania obwodu kwantowego z klasycznym przeszukiwaniem wszystkich kluczy.

## 2. Struktura szyfru

Blok wejściowy $P$ jest dzielony na dwie czterobitowe części:

$$
P=L_0\|R_0
$$

gdzie:
- $L_0$ – starsze cztery bity tekstu jawnego,
- $R_0$ – młodsze cztery bity tekstu jawnego,
- $\|$ – konkatenacja ciągów bitowych.

| Parametr | Wartość |
|---|---|
| Długość bloku | 8 bitów |
| Długość klucza | 8 bitów |
| Liczba rund | 3 |
| Długość połowy bloku | 4 bity |
| Długość podklucza rundy | 4 bity |
| Końcowa dodatkowa zamiana połówek | Nie |

### Schemat działania

```text
          Tekst jawny P (8 bitów)
                    |
                    v
            +---------------+
            | Podział L0, R0|
            +---------------+
                    |
                    v
            +---------------+
     K0 --->| Runda Feistela |
            +---------------+
                    |
                    v
            +---------------+
     K1 --->| Runda Feistela |
            +---------------+
                    |
                    v
            +---------------+
     K2 --->| Runda Feistela |
            +---------------+
                    |
                    v
             Połączenie L3, R3
                    |
                    v
            Szyfrogram C (8 bitów)
```

## 3. Harmonogram klucza

Klucz główny $K$ jest dzielony na dwie czterobitowe części:

$$
K=K_H\|K_L
$$

Podklucze kolejnych rund wyznaczane są następująco:

$$
K_0=K_H
$$

$$
K_1=K_L
$$

$$
K_2=K_H\oplus K_L
$$

gdzie $\oplus$ oznacza bitową operację XOR.

Dla klucza `01101101`:

- $K_H=$ `0110`,
- $K_L=$ `1101`.

| Runda | Podklucz | Wartość binarna |
|---|---|---|
| 1 | $K_0=K_H$ | `0110` |
| 2 | $K_1=K_L$ | `1101` |
| 3 | $K_2=K_H\oplus K_L$ | `1011` |

Harmonogram jest deterministyczny i nie wymaga dodatkowych danych ani losowości.

## 4. Funkcja rundy

Funkcja rundy wykorzystuje cykliczne przesunięcie czterobitowej wartości $R$ o jeden bit w lewo:

$$
\operatorname{ROTL}_4(R,1)=((R\ll1)\lor(R\gg3))\land 15
$$

Funkcję rundy zdefiniowano jako:

$$
F(R,K_i)=\bigl(R\land\operatorname{ROTL}_4(R,1)\bigr)\oplus K_i
$$

gdzie:
- $R$ – prawa połowa bloku w danej rundzie,
- $K_i$ – podklucz danej rundy,
- $\land$ – bitowa operacja AND,
- $\lor$ – bitowa operacja OR,
- $\oplus$ – bitowa operacja XOR.

Nieliniowy składnik funkcji stanowi operacja AND wykonywana na bitach $R$ oraz jego rotacji.

### 4.1. Aktualizacja połówek bloku

W każdej rundzie sieci Feistela wykonywane są operacje:

$$
L_{i+1}=R_i
$$

$$
R_{i+1}=L_i\oplus F(R_i,K_i)
$$

Po trzeciej rundzie szyfrogram powstaje przez połączenie końcowych połówek:

$$
C=L_3\|R_3
$$

Nie wykonuje się dodatkowej zamiany połówek po ostatniej rundzie.

## 5. Przykład szyfrowania

Przyjęto następującą parę wejściową:

| Parametr | Wartość binarna |
|---|---|
| Tekst jawny $P$ | `10110010` |
| Klucz $K$ | `01101101` |
| Początkowe $L_0$ | `1011` |
| Początkowe $R_0$ | `0010` |

Przebieg trzech rund:

| Runda | $L_i$ | $R_i$ | $K_i$ | $F(R_i,K_i)$ | $L_{i+1}$ | $R_{i+1}$ |
|---|---|---|---|---|---|---|
| 1 | `1011` | `0010` | `0110` | `0110` | `0010` | `1101` |
| 2 | `0010` | `1101` | `1101` | `0100` | `1101` | `0110` |
| 3 | `1101` | `0110` | `1011` | `1111` | `0110` | `0010` |

Wynik szyfrowania:

$$
E_{01101101}(10110010)=01100010
$$

Otrzymany szyfrogram `01100010` stanowi referencyjną wartość wykorzystywaną w testach implementacji.

## 6. Deszyfrowanie

Sieć Feistela umożliwia odwrócenie szyfrowania bez konieczności odwracania samej funkcji $F$.

Dla stanu po rundzie $(L_{i+1},R_{i+1})$ poprzednie wartości oblicza się według wzorów:

$$
R_i=L_{i+1}
$$

$$
L_i=R_{i+1}\oplus F(L_{i+1},K_i)
$$

Deszyfrowanie wykorzystuje podklucze w odwrotnej kolejności: $K_2$, $K_1$, $K_0$.

Dla przyjętego przykładu:

$$
D_{01101101}(01100010)=10110010
$$

## 7. Implementacja klasyczna

Referencyjna implementacja szyfru znajduje się w pliku `src/cipher.py`.

| Funkcja | Przeznaczenie |
|---|---|
| `rotl4()` | Cykliczne przesunięcie czterobitowej wartości |
| `round_function()` | Obliczenie funkcji $F(R,K_i)$ |
| `generate_round_keys()` | Wyznaczenie trzech podkluczy |
| `encrypt()` | Szyfrowanie ośmiobitowego bloku |
| `decrypt()` | Odszyfrowanie ośmiobitowego bloku |

Dane wejściowe są reprezentowane jako liczby całkowite z zakresu od 0 do 255. W dokumentacji i przykładach wartości bloków oraz kluczy zapisywane są jako ośmiobitowe ciągi binarne.

Przykładowe uruchomienie:

```bash
uv run python src/cipher.py
```

Oczekiwane wartości:

```text
Plaintext:   10110010
Key:         01101101
Ciphertext:  01100010
Decrypted:   10110010
```

## 8. Implementacja kwantowa

Implementacja kwantowa znajduje się w pliku `src/quantum_cipher.py` i wykorzystuje bibliotekę Qrisp.

W obwodzie stosowane są dwa czterokubitowe rejestry reprezentujące połówki bloku oraz, w wariancie z kwantowym kluczem, dodatkowy ośmiokubitowy rejestr `key_register`.

| Operacja szyfru | Realizacja kwantowa |
|---|---|
| XOR ze stałą | Bramki X |
| XOR z bitem klucza | Bramki CNOT (`cx`) |
| Nieliniowa operacja AND i XOR do celu | Bramki wielokrotnie kontrolowane X (`mcx`) |
| Zamiana połówek Feistela | Logiczna zamiana odwołań do rejestrów |

### 8.1. Szyfrowanie ze stałym kluczem

Funkcja `quantum_encrypt(plaintext, key)` realizuje trzy rundy  dla określonego tekstu jawnego i klucza.

Wynik otrzymywany w dwóch czterokubitowych rejestrach można porównać z rezultatem klasycznej funkcji `encrypt()`.

### 8.2. Szyfrowanie z kwantowym rejestrem klucza

Funkcja `quantum_encrypt_with_key(plaintext, key_register)` wykorzystuje klucz zapisany w rejestrze kwantowym.

Dla równomiernej superpozycji 256 kluczy stan początkowy ma postać:

$$
\frac{1}{16}\sum_{k=0}^{255}|k\rangle|P\rangle
$$

Po szyfrowaniu otrzymujemy:

$$
\frac{1}{16}\sum_{k=0}^{255}|k\rangle|E_k(P)\rangle
$$

Oznacza to, że wynik szyfrowania pozostaje powiązany z odpowiednią wartością klucza, bez pomiaru rejestru w trakcie obliczeń.

### 8.3. Odwracanie obliczeń

Funkcja `quantum_decrypt_with_key(left, right, key_register)` odwraca rundy szyfrowania z wykorzystaniem tego samego rejestru klucza.


## Źródła

1. Grover, L. K. (1996). *A Fast Quantum Mechanical Algorithm for Database Search*.  
   https://arxiv.org/abs/quant-ph/9605043

2. Qrisp – *Documentation*.  
   https://qrisp.eu/

3. Qrisp – *Grover's Algorithm*.  
   https://qrisp.eu/reference/Algorithms/Grover.html

