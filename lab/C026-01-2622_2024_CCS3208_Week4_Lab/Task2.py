from collections import Counter
import heapq
from itertools import count

def huffman_codes(text):
    frequencies = Counter(text)
    serial = count()
    heap = [(f, next(serial), s) for s, f in frequencies.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {text[0]: "0"}
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(serial), (left, right)))
    root = heap[0][2]
    codes = {}
    def walk(node, prefix):
        if isinstance(node, str):
            codes[node] = prefix
        else:
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")
    walk(root, "")
    return codes

def decode_bits(bits, codes):
    reverse = {v: k for k, v in codes.items()}
    output, buffer = [], ""
    for bit in bits:
        buffer += bit
        if buffer in reverse:
            output.append(reverse[buffer])
            buffer = ""
    assert buffer == "", "Incomplete bitstream"
    return "".join(output)

# --- Modification 1: Verify prefix property ---
def is_prefix_free(codes):
    codewords = list(codes.values())
    for i in range(len(codewords)):
        for j in range(len(codewords)):
            if i != j and codewords[j].startswith(codewords[i]):
                return False
    return True

# --- Base example ---
source = "A" * 45 + "B" * 13 + "C" * 12 + "D" * 10
codes = huffman_codes(source)
message = "ABACD"
bits = "".join(codes[ch] for ch in message)
print("Codes:", codes)
print("Encoded:", bits, "length:", len(bits))
print("Decoded:", decode_bits(bits, codes))
assert decode_bits(bits, codes) == message

# --- Running Student Modifications ---
print("\n--- Student Modifications ---")

# 1. Prefix check
print("Prefix-free valid:", is_prefix_free(codes))

# 2. Weighted average code length
freqs = Counter(source)
total_symbols = len(source)
weighted_avg = sum(freqs[s] * len(codes[s]) for s in freqs) / total_symbols
print("Weighted average code length:", weighted_avg, "bits/symbol")

# 3. Encode and decode "AABACAD"
test_msg = "AABACAD"
encoded_test = "".join(codes[ch] for ch in test_msg)
decoded_test = decode_bits(encoded_test, codes)
print("Test message:", test_msg)
print("Encoded AABACAD:", encoded_test)
print("Bit length:", len(encoded_test))
print("Decoded AABACAD:", decoded_test)
assert decoded_test == test_msg
