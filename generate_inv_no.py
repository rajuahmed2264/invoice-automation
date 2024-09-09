import hashlib
import datetime
import random


def inv_num_generator(payment_number, payment_date, store_name):

    combined_string = f"{payment_number}{payment_date}{store_name}"

    # Generate a SHA-256 hash from the combined string
    hash_object = hashlib.sha256(combined_string.encode())
    hash_hex = hash_object.hexdigest()

    # Take the first 10 characters of the hash and convert to an integer
    hash_part = hash_hex
    result = int(hash_part, 16)
    result = str(result)
    if len(result) >=30:

      # Convert hex to integer
        random_index = random.randint(10, len(result) - 10)
        result = result[random_index: random_index+10]
    # Ensure the result is within the desired range of 10 digits
    else:
        result = result % (10**10)  # Keep only the last 10 digits

    return result
