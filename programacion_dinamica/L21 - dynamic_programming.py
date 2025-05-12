from itertools import combinations
from math import factorial


def binomial_list(n: int, k: int) -> int:
    return len(list(combinations(range(n),k)))

def binomial_math(n: int, k: int) -> int:
    return factorial(n) // (factorial(k) * factorial(n-k))

def binomial(n: int, k: int) -> int:
    if k > n:
        return 0

    table = [[0] * (k + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        table[i][0] = 1  # C(i, 0) = 1
        for j in range(1, min(i, k) + 1):
            if j == i:
                table[i][j] = 1  # C(i, i) = 1
            else:
                table[i][j] = table[i - 1][j] + table[i - 1][j - 1]

    return table[n][k]

    

def binomial_recursiva(n: int, k: int) -> int:
    if k == n or k == 0:
        return 1
    if k > n:
        return 0
    return binomial_recursiva(n-1,k-1) + binomial_recursiva(n-1,k)


def change( n:int, coins: list[int]) -> dict[int,int]:
    
    assert 1 in coins, "Moneda da 1 peso necesaria para solucion"
    
    k = len(coins)
    
    # 1.- definir estructuras/tablas
    
    d = [[None for _ in range(n+1)] for _ in range(k)]
    
    # 2.- Identificar casos triviales
    
    for j in range (n+1):
        d[0][j] = j
        
    for i in range(k):
        d[i][0] = 0
    
    # 3.- Recursion
    for i in range(1,k):
        for j in range(1,n+1):
           
            m_i = coins[i]
            
            if j < m_i:
                d[i][j] = d[i-1][j]
            else:
                d[i][j] = min(d[i-1][j],1+d[i][j-m_i])
    
    solution = {c: 0 for c in coins}
    i = k - 1 
    j = n
    q = d[i][j]
    
    while i != 0:
        up = d[i-1][j]
        if up == q:
            i -= 1
        else:
            m_i = coins[i]
            j -= m_i
            solution[m_i] += 1
        q =d[i][j]
        
    solution[1] = j
    
    return solution

def cut_rod(p: list[int], n: int) -> tuple[list[int], list[int]]:
    dp = [0] * (n + 1)      # dp[i] = máxima ganancia para longitud i
    cuts = [0] * (n + 1)    # cuts[i] = mejor primer corte para longitud i

    for j in range(1, n + 1):
        max_val = float('-inf')
        for i in range(1, j + 1):
            if p[i - 1] + dp[j - i] > max_val:
                max_val = p[i - 1] + dp[j - i]
                cuts[j] = i
        dp[j] = max_val

    return dp, cuts

def lcs(x: str, y: str) -> str:
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Construcción de la tabla dp
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstrucción de la subsecuencia
    i, j = m, n
    lcs_result = []
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            lcs_result.append(x[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(lcs_result))



if __name__ == "__main__":
    print(binomial(10, 5))
    # 252
    r, s = cut_rod([1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 10)
    print(r)
    #[0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    print(s)
    #[None, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10]
    print(lcs("ABCBDAB", "BDCABA"))
    # BCBA
