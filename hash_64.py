#Implement a simple hashing algorithm of your own. Combining the components learnt.
#(Rotation, Shift bits, permutation, Substitution) Ensure Determinism, Pre Image Resistance

def custom_hash(input_string: str) -> str:
    
    hash_state = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
    
    # Prepare the input data: convert string to bytes.
    # Padding: We ensure the data is a multiple of 8 bytes so we can process it in chunks.
    data = input_string.encode('utf-8')
    pad_len = 8 - (len(data) % 8)
    data += bytes([pad_len] * pad_len) # PKCS#7 standard padding
    
    # Process the input data block by block (8 bytes at a time)
    for i in range(0, len(data), 8):
        block = list(data[i:i+8])
        
        # --- 2. Substitution ---
        for j in range(8):
            block[j] = (block[j] * 31 + 17) % 256
            
        # --- 3. Bit Shift ---
        for j in range(8):
            block[j] = (block[j] << 1) & 0xFF 
            
        # --- 4. Rotation (Circular Shift) ---
        for j in range(8):
            block[j] = ((block[j] >> 3) | (block[j] << 5)) & 0xFF
            
        # --- 5. Permutation ---
        block = [
            block[7], block[0], block[5], block[6], 
            block[3], block[2], block[1], block[4]
        ]
        
        # --- Mix into State ---
        # XOR the processed block into our running hash_state.
        for j in range(8):
            hash_state[j] ^= block[j]
            # Extra rotation on the state to further mix
            hash_state[j] = ((hash_state[j] << 2) | (hash_state[j] >> 6)) & 0xFF

    return "".join(f"{b:02x}" for b in hash_state)
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input("Enter your message: ")
        
    print(f"Input:  '{text}'")
    print(f"Output: {custom_hash(text)}")