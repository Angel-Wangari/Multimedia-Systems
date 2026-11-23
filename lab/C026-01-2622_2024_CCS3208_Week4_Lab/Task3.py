model = {"A": (0.0, 0.6), "B": (0.6, 1.0)}

def encode_interval(message, model):
    low, high = 0.0, 1.0
    trace = []
    for symbol in message:
        a, b = model[symbol]
        width = high - low
        low, high = low + width * a, low + width * b
        trace.append((symbol, round(low, 6), round(high, 6)))
    return round(low, 6), round(high, 6), trace

def decode_tag(tag, length, model):
    low, high = 0.0, 1.0
    result = []
    for _ in range(length):
        width = high - low
        for symbol, (a, b) in model.items():
            next_low = low + width * a
            next_high = low + width * b
            if next_low <= tag < next_high:
                result.append(symbol)
                low, high = next_low, next_high
                break
        else:
            raise ValueError("Tag outside modeled intervals")
    return "".join(result)

# --- Base Example (AB) ---
message = "AB"
low, high, trace = encode_interval(message, model)
tag = round((low + high) / 2, 6)
print("Trace:", trace)
print("Final interval:", (low, high), "tag:", tag)
print("Decoded:", decode_tag(tag, len(message), model))

# --- Student Exercise 1: Message "ABA" ---
print("\n--- Exercise 1: ABA ---")
low_aba, high_aba, trace_aba = encode_interval("ABA", model)
tag_aba = round((low_aba + high_aba) / 2, 6)
print("Trace ABA:", trace_aba)
print("Final interval ABA:", (low_aba, high_aba), "Valid tag:", tag_aba)
print("Decoded ABA:", decode_tag(tag_aba, 3, model))

# --- Student Exercises 2 & 3: Three-symbol model and "BA" ---
print("\n--- Exercises 2 & 3: BA ---")
model_3 = {"A": (0.0, 0.5), "B": (0.5, 0.8), "C": (0.8, 1.0)}
low_ba, high_ba, trace_ba = encode_interval("BA", model_3)
tag_ba = round((low_ba + high_ba) / 2, 6)
print("Trace BA:", trace_ba)
print("Final interval BA:", (low_ba, high_ba), "Valid tag:", tag_ba)
print("Decoded BA:", decode_tag(tag_ba, 2, model_3))
