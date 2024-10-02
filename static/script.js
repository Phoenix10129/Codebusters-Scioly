document.addEventListener('DOMContentLoaded', function () {
    fetch('/get-encrypted-quote')
        .then(response => response.json())
        .then(data => {
            const ciphertext = data.encrypted_quote.split(''); // Split into individual characters
            const ciphertextContainer = document.getElementById('ciphertext');
            const plaintextContainer = document.getElementById('plaintext');

            // Create letterboxes for ciphertext
            ciphertext.forEach(char => {
                const letterbox = document.createElement('div');
                letterbox.classList.add('letterbox');
                letterbox.innerText = char;
                ciphertextContainer.appendChild(letterbox);
            });

            // Create input boxes for plaintext
            ciphertext.forEach(() => {
                const inputBox = document.createElement('input');
                inputBox.type = 'text';
                inputBox.maxLength = 1; // Limit to 1 character per box
                plaintextContainer.appendChild(inputBox);
            });
        });

    // Check button functionality
    document.getElementById('submit-btn').addEventListener('click', function () {
        const originalQuote = "Your original quote"; // Replace with the actual original quote if needed
        const userInput = Array.from(document.querySelectorAll('#plaintext input')).map(input => input.value.toLowerCase()).join('');
        
        // Send original quote to terminal for testing
        console.log(originalQuote); 

        // Check if userInput matches original quote
        const resultElement = document.getElementById('result');
        if (userInput === originalQuote.replace(/\s+/g, '').toLowerCase()) { // Compare without spaces
            resultElement.innerText = "Correct!";
            resultElement.className = "correct";
        } else {
            resultElement.innerText = "Incorrect, try again.";
            resultElement.className = "incorrect";
        }
    });
});
