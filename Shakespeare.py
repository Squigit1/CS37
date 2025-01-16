# Ethan Baird
# January 15, 2025
# Frequncies for Shakespeare


from collections import Counter, defaultdict
import string
import os
import math

# Function to process text and count bigrams
def count_double_letter_substrings(file_path):
    # Initialize a counter for bigrams
    bigram_counter = Counter()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Remove punctuation and convert to lowercase
                cleaned_line = line.translate(str.maketrans('', '', string.punctuation)).lower()
                
                # Split into words and process each word
                for word in cleaned_line.split():
                    # Count bigrams in the word
                    for i in range(len(word) - 1):
                        bigram = word[i:i+2]  # Get the two-letter substring
                        if bigram.isalpha():  # Ensure only alphabetic bigrams are counted
                            bigram_counter[bigram] += 1

        return bigram_counter

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

# Function to calculate letter percentages
def calculate_letter_percentages(bigram_counter):
    first_char_counts = Counter()
    second_char_counts = Counter()

    # Count occurrences of each letter as first or second in bigrams
    for bigram, count in bigram_counter.items():
        if bigram[0].isalpha():  # Ensure first character is alphabetic
            first_char_counts[bigram[0]] += count
        if bigram[1].isalpha():  # Ensure second character is alphabetic
            second_char_counts[bigram[1]] += count

    # Calculate percentages
    total_first = sum(first_char_counts.values())
    total_second = sum(second_char_counts.values())

    first_char_percentages = {char: (count / total_first) for char, count in first_char_counts.items()}
    second_char_percentages = {char: (count / total_second) for char, count in second_char_counts.items()}

    return first_char_percentages, second_char_percentages


# Function to calculate entropy
def calculate_entropy(percentages):
    entropy = 0
    for p in percentages.values():
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

# Function to calculate conditional entropy H(Y|X)
def calculate_conditional_entropy(bigram_counter, first_char_counts):
    conditional_entropy = 0
    total_bigrams = sum(bigram_counter.values())

    for bigram, count in bigram_counter.items():
        p_xy = count / total_bigrams
        p_x = first_char_counts[bigram[0]] / total_bigrams
        conditional_entropy -= p_xy * math.log2(p_xy / p_x)

    return conditional_entropy

# Path to the file
file_path = os.path.expanduser("~/Desktop/CS37/shakespeare.txt")

# Count the bigrams
bigram_counts = count_double_letter_substrings(file_path)

if bigram_counts:
    # Calculate percentages
    first_char_percentages, second_char_percentages = calculate_letter_percentages(bigram_counts)

    # Calculate entropy
    first_entropy = calculate_entropy(first_char_percentages)
    second_entropy = calculate_entropy(second_char_percentages)

    # Calculate conditional entropy H(Y|X)
    first_char_counts = Counter({char: int(p * sum(bigram_counts.values())) for char, p in first_char_percentages.items()})
    conditional_entropy = calculate_conditional_entropy(bigram_counts, first_char_counts)

    # Display the percentages
    print("Percentage of each letter as the first character in bigrams:")
    for char, percentage in sorted(first_char_percentages.items()):
        print(f"{char}: {percentage * 100:.2f}%")

    print("\nPercentage of each letter as the second character in bigrams:")
    for char, percentage in sorted(second_char_percentages.items()):
        print(f"{char}: {percentage * 100:.2f}%")

    # Display entropy
    print(f"\nEntropy of the H(X): {first_entropy:.4f}")
    print(f"Entropy of the H(Y): {second_entropy:.4f}")
    print(f"Conditional entropy H(Y|X): {conditional_entropy:.4f}")
    print(f"Mutual Information I(X:Y): {second_entropy-conditional_entropy:.4f}")
