import time
import matplotlib.pyplot as plt

# Example algorithms with different time complexities

def constant_algo(n):
    return 1   # O(1)

def linear_algo(n):
    s = 0
    for i in range(n):
        s += i
    return s   # O(n)

def quadratic_algo(n):
    s = 0
    for i in range(n):
        for j in range(n):
            s += i + j
    return s   # O(n^2)

def cubic_algo(n):
    s = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                s += i + j + k
    return s   # O(n^3)

# Measure runtime for different input sizes
def measure_time(func, n):
    start = time.time()
    func(n)
    end = time.time()
    return (end - start) * 1000  # in ms

if __name__ == "__main__":
    input_sizes = [10, 50, 100, 200]

    algorithms = {
        "O(1) Constant": constant_algo,
        "O(n) Linear": linear_algo,
        "O(n^2) Quadratic": quadratic_algo,
        "O(n^3) Cubic": cubic_algo,
    }

    results = {name: [] for name in algorithms}

    for n in input_sizes:
        for name, func in algorithms.items():
            t = measure_time(func, n)
            results[name].append(t)

    # Print results
    print("Execution times (ms):")
    for name, times in results.items():
        print(f"{name}: {times}")

    # Plot results
    for name, times in results.items():
        plt.plot(input_sizes, times, marker='o', label=name)

    plt.xlabel("Input size (n)")
    plt.ylabel("Execution time (ms)")
    plt.title("Asymptotic Notation Demonstration")
    plt.legend()
    plt.show()