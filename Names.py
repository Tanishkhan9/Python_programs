# Cute Name Combination Generator

def combine_names():
    # Input names
    name1 = input("Enter the first name: ").strip()
    name2 = input("Enter the second name: ").strip()
    
    # Input slicing numbers
    n1 = int(input(f"Enter a slicing number for {name1} (1-{len(name1)}): "))
    n2 = int(input(f"Enter a slicing number for {name2} (1-{len(name2)}): "))
    
    # Generate combinations
    combo1 = name1[:n1] + name2[n2:]
    combo2 = name2[:n2] + name1[n1:]
    combo3 = name1[:n1] + name2[:n2]
    combo4 = name1[n1:] + name2[:n2]
    combo5 = name2[n2:] + name1[:n1]
    
    # Print results
    print("\n✨ Cute Name Combinations ✨")
    print(f"1. {combo1}")
    print(f"2. {combo2}")
    print(f"3. {combo3}")
    print(f"4. {combo4}")
    print(f"5. {combo5}")

# Run the function
combine_names()
