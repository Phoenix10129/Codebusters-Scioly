from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def alphanumeric_decoder(plaintext_char, key_char):
    res_sum = int(alphabet_list.index(plaintext_char) + int(alphabet_list.index(key_char) // 2))
    res_diff = int(alphabet_list.index(plaintext_char) - int(alphabet_list.index(key_char) // 2))
    
    if alphabet_list.index(plaintext_char) < 13:
        if res_sum < 13:
            res_sum += 13
        return res_sum
    else:
        if res_diff >= 13:
            res_diff -= 13
        return res_diff

def porta_encode(text, key):
    encoded = []
    repeated_key = (key * (len(text) // len(key) + 1))[:len(text)]
    
    for i, char in enumerate(text):
        if char.lower() in alphabet_list:
            key_char = repeated_key[i].lower()
            index = alphanumeric_decoder(char.lower(), key_char)
            encoded_char = alphabet_list[index]
            encoded.append(encoded_char.upper() if char.isupper() else encoded_char)
        else:
            encoded.append(char)  
    return ''.join(encoded)

def get_random_word():
    try:
        response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
        if response.status_code == 200:
            word_data = response.json()
            if isinstance(word_data, list) and len(word_data) > 0:
                return word_data[0]  # Return the random word
        return "defaultkey"
    except Exception as e:
        print(f"Error fetching word: {e}")
        return "defaultkey"

def get_random_quote():
    try:
        response = requests.get('https://zenquotes.io/api/random')
        if response.status_code == 200:
            quote_data = response.json()
            if isinstance(quote_data, list) and len(quote_data) > 0:
                return quote_data[0]['q']  # Return the quote text
        return "Life is what happens when you're busy making other plans."
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Life is what happens when you're busy making other plans."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-encrypted-quote', methods=['GET'])
def get_encrypted_quote():
    key = get_random_word()  # Fetch a random word for the key
    quote = get_random_quote()
    quote_no_spaces = quote.replace(" ", "")  # Remove spaces for encryption

    # Encode the quote using the Porta cipher
    encoded_quote = porta_encode(quote_no_spaces, key)

    # Return the encrypted quote and key to the frontend
    return jsonify({
        'encrypted_quote': encoded_quote,
        'key': key
    })

if __name__ == '__main__':
    app.run(debug=True)
