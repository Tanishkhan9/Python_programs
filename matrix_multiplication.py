import numpy as np

def classic_matrix_multiplication(A, B):
    """
    Normal matrix multiplication using triple loop
    A: m x n matrix
    B: n x p matrix
    Returns: m x p result matrix
    """
    m, n = A.shape
    nB, p = B.shape

    if n != nB:
        raise ValueError("Number of columns of A must match number of rows of B")

    # Create a result matrix filled with zeros
    C = np.zeros((m, p), dtype=int)

    # Triple nested loop for multiplication
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C


# Example usage
if __name__ == "__main__":
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    print("Matrix A:\n", A)
    print("Matrix B:\n", B)

    C = classic_matrix_multiplication(A, B)
    print("Result of Normal Matrix Multiplication:\n", C)