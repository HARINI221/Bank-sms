import twilio.twiml.messaging_response
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import re

app = Flask(__name__)

# Placeholder for expenses data
expenses = []

def categorize_message(message):
    # Example categorization logic
    categories = {
        'food': ['restaurant', 'cafe', 'food'],
        'transport': ['uber', 'taxi', 'bus'],
        'groceries': ['supermarket', 'grocery']
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if re.search(keyword, message, re.IGNORECASE):
                return category
    return 'other'

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    category = categorize_message(msg)
    
    # Store expense data
    expenses.append({'message': msg, 'category': category})

    # Save to CSV
    df = pd.DataFrame(expenses)
    df.to_csv('expenses.csv', index=False)
    
    # Respond to the message
    resp = MessagingResponse()
    resp.message(f"Expense categorized as: {category}")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
