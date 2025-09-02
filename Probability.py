# Example: Students and Sports
# A: Student plays Football
# B: Student plays Basketball

# Probabilities
P_A = 0.7      # P(A): Probability student plays football
P_B = 0.6      # P(B): Probability student plays basketball
P_A_and_B = 0.4  # P(A ∩ B): Probability student plays both

# Joint Probability
print("Joint Probability P(A ∩ B):", P_A_and_B)

# Marginal Probability
print("Marginal Probability P(A):", P_A)
print("Marginal Probability P(B):", P_B)

# Conditional Probability
P_A_given_B = P_A_and_B / P_B
P_B_given_A = P_A_and_B / P_A

print("Conditional Probability P(A | B):", round(P_A_given_B, 2))
print("Conditional Probability P(B | A):", round(P_B_given_A, 2))
