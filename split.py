def split_text(input_text, max_length=65):
    words = input_text.split()  # Split input text by spaces
    result = []
    current_chunk = ""

    for word in words:
        # Check if adding the next word exceeds the max length
        if len(current_chunk) + len(word) + 1 <= max_length:
            if current_chunk:
                current_chunk += " " + word  # Add word with space if not the first word
            else:
                current_chunk = word  # Add word directly if it's the first
        else:
            result.append(current_chunk)  # Save the current chunk
            current_chunk = word  # Start a new chunk with the current word

    # Append the last chunk
    if current_chunk:
        result.append(current_chunk)

    return result


def main():
    # Take input from the user
    input_text = input("Enter your text: ")

    # Split the text into chunks
    chunks = split_text(input_text)

    # Display the result in the desired format
    print("[", end="")
    print(", ".join(f'"{chunk}"' for chunk in chunks), end="")
    print("]")


if __name__ == "__main__":
    main()
