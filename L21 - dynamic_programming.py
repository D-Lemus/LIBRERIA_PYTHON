def binomial(n: int, k: int) -> int:
    """
    Computes the binomial coefficient (n choose k) using dynamic programming.
    
    Args:
        n: The total number of items
        k: The number of items to choose
        
    Returns:
        The binomial coefficient C(n,k)
    """
    # Create a 2D array to store binomial coefficients
    C = [[0 for _ in range(k + 1)] for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1):
        C[i][0] = 1  # C(i,0) = 1
    
    # Fill the table using bottom-up approach
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            # C(i,j) = C(i-1,j-1) + C(i-1,j)
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    
    return C[n][k]


def cut_rod(p: list[int], n: int) -> tuple[list[int], list[int]]:
    """
    Solve the rod-cutting problem using dynamic programming.
    
    Args:
        p: List of prices where p[i] is the price of a rod of length i+1
        n: Length of the rod
        
    Returns:
        A tuple containing:
        - r: List of maximum revenues for rods of length 0 to n
        - s: List of optimal first-cut positions for rods of length 0 to n
    """
    # Initialize arrays for maximum revenues and optimal cuts
    r = [0] * (n + 1)  # r[i] = maximum revenue for rod of length i
    s = [None] * (n + 1)  # s[i] = optimal first-cut position for rod of length i
    
    # Bottom-up calculation of optimal revenue and cuts
    for j in range(1, n + 1):
        q = float('-inf')  # Initialize revenue to negative infinity
        
        # Try each possible first cut position
        for i in range(1, j + 1):
            # Calculate revenue: price of first piece + optimal revenue of remaining rod
            if q < p[i - 1] + r[j - i]:
                q = p[i - 1] + r[j - i]
                s[j] = i  # Record the optimal cut position
        
        r[j] = q  # Store the maximum revenue for rod of length j
    
    return r, s


def lcs(x: str, y: str) -> str:
    """
    Find the longest common subsequence of two strings using dynamic programming.
    
    Args:
        x: First string
        y: Second string
        
    Returns:
        The longest common subsequence as a string
    """
    m = len(x)
    n = len(y)
    
    # Create tables for the lengths and directions
    c = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    b = [['' for _ in range(n + 1)] for _ in range(m + 1)]
    
    # Fill the tables
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'diagonal'  # match, take diagonal value + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'up'  # take value from above
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'left'  # take value from left
    
    # Reconstruct the LCS from the direction table
    result = []
    i, j = m, n
    while i > 0 and j > 0:
        if b[i][j] == 'diagonal':
            result.append(x[i - 1])
            i -= 1
            j -= 1
        elif b[i][j] == 'up':
            i -= 1
        else:  # b[i][j] == 'left'
            j -= 1
    
    # Reverse the result (since we built it backwards)
    return ''.join(reversed(result))


if __name__ == "__main__":
    print(binomial(10, 5))
    # 252
    r, s = cut_rod([1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 10)
    print(r)
    # [0, 1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    print(s)
    # [None, 1, 2, 3, 2, 2, 6, 1, 2, 3, 10]
    print(lcs("ABCBDAB", "BDCABA"))
    # BCBA