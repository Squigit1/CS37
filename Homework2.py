import string
from collections import Counter
import math

def process_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()

    # Normalize text: make lowercase and remove special characters except spaces
    text = text.lower()
    text = ''.join(char if char in string.ascii_lowercase + ' ' else '' for char in text)

    # Add "$" after every word
    words = text.split()
    text_with_dollars = "$ ".join(words) + "$"

    return text_with_dollars

def calculate_probability_distribution(text):
    # Count occurrences of each letter and $
    counts = Counter(text)

    # Calculate total characters to compute probabilities
    total_characters = sum(counts.values())

    # Create a probability distribution
    probabilities = {char: count / total_characters for char, count in counts.items()}

    return probabilities

def calculate_mean_length(probabilities_source, probabilities_target):
    mean_length = 0
    for char, prob_target in probabilities_target.items():
        prob_source = probabilities_source.get(char, 0)
        if prob_source > 0:
            mean_length += -prob_target * math.log2(prob_source)
    return mean_length

def calculate_entropy(probabilities):
    entropy = 0
    for prob in probabilities.values():
        if prob > 0:
            entropy += -prob * math.log2(prob)
    return entropy

def main():
    shakespeare_path = "shakespeare.txt"
    holmes_path = "holmes.txt"

    # Step 1: Process Shakespeare text to add "$" after every word
    shakespeare_text = process_file(shakespeare_path)

    # Step 2: Calculate the probability distribution for Shakespeare text
    shakespeare_probabilities = calculate_probability_distribution(shakespeare_text)

    # Step 3: Process Holmes text
    holmes_text = process_file(holmes_path)

    # Step 4: Calculate the probability distribution for Holmes text
    holmes_probabilities = calculate_probability_distribution(holmes_text)

    # Step 5: Calculate the mean length of the encoding scheme for both texts
    mean_length_shakespeare = calculate_mean_length(shakespeare_probabilities, shakespeare_probabilities)
    mean_length_holmes = calculate_mean_length(shakespeare_probabilities, holmes_probabilities)

    # Step 6: Calculate the empirical entropy of both texts
    entropy_shakespeare = calculate_entropy(shakespeare_probabilities)
    entropy_holmes = calculate_entropy(holmes_probabilities)

    print(f"\nMean length of the encoding scheme for Shakespeare text: {mean_length_shakespeare:.6f}")
    print(f"Mean length of the encoding scheme for Holmes text: {mean_length_holmes:.6f}")
    print(f"\nEmpirical entropy of Shakespeare text: {entropy_shakespeare:.6f}")
    print(f"Empirical entropy of Holmes text: {entropy_holmes:.6f}")

if __name__ == "__main__":
    main()