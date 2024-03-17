import tkinter as tk
from tkinter import messagebox

def create_location_array(size):
    return [6] * size

def remove_duplicates(arr):
    unique_arr = []
    for item in arr:
        if item not in unique_arr:
            unique_arr.append(item)
    return unique_arr

def check_element(value, arr):
    return value not in arr

def convert_key_to_int(key):
    return [ord(char) for char in key]

def fill_matrix(text_int, matrix):
    used_chars = set()
    letter = 97  # 'a' ASCII value
    for i in range(5):
        for j in range(5):
            if text_int:
                char = text_int.pop(0)
                if char not in used_chars and char != 106:
                    matrix[i][j] = char
                    used_chars.add(char)
                else:
                    while letter in used_chars or letter == 106:
                        letter += 1
                    matrix[i][j] = letter
                    used_chars.add(letter)
                    letter += 1
            elif letter not in used_chars and letter != 106:
                matrix[i][j] = letter
                used_chars.add(letter)
                letter += 1
            else:
                while letter in used_chars or letter == 106:
                    letter += 1
                matrix[i][j] = letter
                used_chars.add(letter)
                letter += 1

def remove_spaces_and_j(arr):
    i = 0
    while i < len(arr):
        if arr[i] == 32:
            del arr[i]
        elif arr[i] == 106:  # 'j' ASCII value
            arr[i] = 105  # 'i' ASCII value
            i += 1
        else:
            i += 1
    return arr

def ensure_even_length(arr):
    if len(arr) % 2 != 0:
        arr.append(97)  # 'a' ASCII value

def create_ciphertext(location, matrix):
    ciphertext = []
    for i in range(0, len(location), 4):
        row1, col1 = location[i], location[i + 1]
        row2, col2 = location[i + 2], location[i + 3]
        if row1 == row2:
            col1 = (col1 + 1) % 5
            col2 = (col2 + 1) % 5
            ciphertext.append(matrix[row1][col1])
            ciphertext.append(matrix[row2][col2])
        elif col1 == col2:
            row1 = (row1 + 1) % 5
            row2 = (row2 + 1) % 5
            ciphertext.append(matrix[row1][col1])
            ciphertext.append(matrix[row2][col2])
        else:
            col1, col2 = col2, col1
            ciphertext.append(matrix[row1][col1])
            ciphertext.append(matrix[row2][col2])
    return ciphertext

def on_click():
    matrix = [[0 for _ in range(5)] for _ in range(5)]
    text_int = []

    key = entry_key.get()
    plaintext = entry_plaintext.get()

    key_int = convert_key_to_int(key)
    key_int = remove_duplicates(key_int)
    fill_matrix(key_int, matrix)

    for char in plaintext:
        text_int.append(ord(char))

    remove_spaces_and_j(text_int)
    ensure_even_length(text_int)

    location_size = len(text_int) * 2
    location = create_location_array(location_size)

    for i in range(len(text_int)):
        row, col = search_matrix(matrix, text_int[i])
        save_row_col(location, i * 2, row, col)

    ciphertext = create_ciphertext(location, matrix)
    entry_ciphertext.delete(0, tk.END)
    entry_ciphertext.insert(0, ''.join([chr(char) for char in ciphertext]))

def search_matrix(matrix, value):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == value:
                return i, j
    return -1, -1

def save_row_col(arr, index, row, col):
    if index % 2 == 0:
        arr[index] = row
        arr[index + 1] = col

root = tk.Tk()
root.title("Playfair Cipher")

label_key = tk.Label(root, text="Khóa mã hóa:")
label_key.grid(row=0, column=0, padx=5, pady=5)

entry_key = tk.Entry(root)
entry_key.grid(row=0, column=1, padx=5, pady=5)

label_plaintext = tk.Label(root, text="Bản rõ:")
label_plaintext.grid(row=1, column=0, padx=5, pady=5)

entry_plaintext = tk.Entry(root)
entry_plaintext.grid(row=1, column=1, padx=5, pady=5)

label_ciphertext = tk.Label(root, text="Bản mã:")
label_ciphertext.grid(row=2, column=0, padx=5, pady=5)

entry_ciphertext = tk.Entry(root)
entry_ciphertext.grid(row=2, column=1, padx=5, pady=5)

button_encrypt = tk.Button(root, text="Mã hóa", command=on_click)
button_encrypt.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
