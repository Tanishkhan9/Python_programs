import numpy as np

def strassen_matrix_mult(A, B):
    """
    Perform Strassen's matrix multiplication on square matrices A and B.
    Both A and B must be numpy arrays of shape (n, n) where n is a power of 2.
    """
    n = A.shape[0]

    # Base case: 1x1 matrix
    if n == 1:
        return A * B

    # Divide matrices into quadrants
    k = n // 2
    A11, A12, A21, A22 = A[:k, :k], A[:k, k:], A[k:, :k], A[k:, k:]
    B11, B12, B21, B22 = B[:k, :k], B[:k, k:], B[k:, :k], B[k:, k:]

    # Compute the 7 products using Strassen's formula
    M1 = strassen_matrix_mult(A11 + A22, B11 + B22)
    M2 = strassen_matrix_mult(A21 + A22, B11)
    M3 = strassen_matrix_mult(A11, B12 - B22)
    M4 = strassen_matrix_mult(A22, B21 - B11)
    M5 = strassen_matrix_mult(A11 + A12, B22)
    M6 = strassen_matrix_mult(A21 - A11, B11 + B12)
    M7 = strassen_matrix_mult(A12 - A22, B21 + B22)

    # Combine results into final quadrants
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Merge quadrants into a single matrix
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))


# Example usage
if __name__ == "__main__":
    # Example: 4x4 matrices (size must be power of 2)
    A = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])

    B = np.array([[16, 15, 14, 13],
                  [12, 11, 10, 9],
                  [8, 7, 6, 5],
                  [4, 3, 2, 1]])

    print("Matrix A:")
    print(A)
    print("\nMatrix B:")
    print(B)

    C = strassen_matrix_mult(A, B)
    print("\nStrassen Matrix Multiplication Result:")
    print(C)