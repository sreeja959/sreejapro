from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Atlas URI
MONGO_URI = "mongodb+srv://bsreeja8919:czBnv2lASjTjoGiu@cluster0.p3zrw2k.mongodb.net/portfolio_db?retryWrites=true&w=majority&appName=Cluster0"

# Setup MongoDB connection
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['portfolio_db']
    contacts_collection = db['contacts']
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB Atlas: {e}")
    exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        contact_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'subject': request.form['subject'],
            'message': request.form['message'],
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'read': False
        }
        result = contacts_collection.insert_one(contact_data)

        if result.inserted_id:
            return jsonify({'success': True, 'message': 'Thank you! Your message has been sent.'})
        return jsonify({'success': False, 'message': 'Failed to save message.'}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
