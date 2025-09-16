import os
from flask import Flask, render_template, request, jsonify
import requests

# The 'template_folder' has been updated to 'templates'
app = Flask(__name__, template_folder='templates', static_folder='assets')

# Replace with your actual API key
API_KEY = "6c6bdd76bb444714e9475c64"
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/')
def home():
    """Renders the main page."""
    # This will now look for 'converter_page.html' inside the 'templates' folder
    return render_template('converter_page.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Handles the currency conversion logic."""
    try:
        data = request.get_json()
        from_currency = data['from_currency']
        to_currency = data['to_currency']
        amount = float(data['amount'])

        # Fetching the latest conversion rates for the 'from' currency
        response = requests.get(API_URL + from_currency)
        response.raise_for_status()
        
        rates_data = response.json()

        if rates_data.get('result') == 'success':
            conversion_rate = rates_data['conversion_rates'].get(to_currency)
            if conversion_rate:
                converted_amount = round(amount * conversion_rate, 2)
                result = {
                    'success': True,
                    'converted_amount': converted_amount,
                    'to_currency': to_currency
                }
                return jsonify(result)
            else:
                return jsonify({'success': False, 'message': 'Invalid target currency.'}), 400
        else:
            error_message = rates_data.get('error-type', 'Unknown API error')
            return jsonify({'success': False, 'message': f'API Error: {error_message}'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'success': False, 'message': f'Network error: {e}'}), 500
    except (ValueError, KeyError) as e:
        return jsonify({'success': False, 'message': f'Invalid input: {e}'}), 400

if __name__ == '__main__':
    app.run(debug=True)