# Probability model
probabilities = {
    'A': 0.25,
    'B': 0.4,
    'C': 0.15,
    'D': 0.1,
    'E': 0.1
}

# Compute cumulative intervals
cumulative = {}
current = 0.0
for symbol, prob in probabilities.items():
    cumulative[symbol] = (current, current + prob)
    current += prob

# Input binary codeword
binary_code = "01010101101111011011100101"
decimal_value = int(binary_code, 2) / (2 ** len(binary_code))  # Convert binary to fraction

# Decoding process
decoded_string = ""
for _ in range(12):  # Decode 12 characters
    for symbol, (low, high) in cumulative.items():
        if low <= decimal_value < high:
            decoded_string += symbol
            # Update decimal_value for the next iteration
            decimal_value = (decimal_value - low) / (high - low)
            break

print("Decoded string:", decoded_string)
