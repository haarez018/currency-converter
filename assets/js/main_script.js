document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('conversion-form');
    const resultContainer = document.getElementById('result-container');
    const resultText = document.getElementById('result-text');
    const convertBtn = document.getElementById('convert-btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        // Get values from the form
        const amount = document.getElementById('amount').value;
        const fromCurrency = document.getElementById('from-currency').value;
        const toCurrency = document.getElementById('to-currency').value;
        
        // Show loading state on button
        convertBtn.textContent = 'Converting...';
        convertBtn.disabled = true;

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    amount: amount,
                    from_currency: fromCurrency,
                    to_currency: toCurrency,
                }),
            });

            const data = await response.json();

            if (data.success) {
                // Display the result
                resultText.textContent = `${data.converted_amount.toLocaleString()} ${data.to_currency}`;
                resultContainer.classList.remove('hidden');
            } else {
                // Display an error message
                resultText.textContent = `Error: ${data.message}`;
                resultContainer.classList.remove('hidden');
            }
        } catch (error) {
            // Handle network or other errors
            resultText.textContent = 'An unexpected error occurred. Please try again.';
            resultContainer.classList.remove('hidden');
        } finally {
            // Restore button state
            convertBtn.textContent = 'Convert';
            convertBtn.disabled = false;
        }
    });
});