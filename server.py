import hashlib
import json
import os
from time import time
from flask import Flask, jsonify, request

class TadyCoin:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.file_path = 'blockchain.json'
    
        if not self.load_from_file():
            self.create_block(nonce=100, previous_hash='1')

    def save_to_file(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def load_from_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.chain = json.load(f)
            return True
        return False

    def create_block(self, nonce, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        self.save_to_file()
        return block

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.get_last_block()['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_nonce):
        nonce = 0
        while self.valid_proof(last_nonce, nonce) is False:
            nonce += 1
        return nonce

    @staticmethod
    def valid_proof(last_nonce, nonce):
        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_chain_valid(self):
        last_block = self.chain[0]
        current_index = 1

        while current_index < len(self.chain):
            block = self.chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['nonce'], block['nonce']):
                return False
            last_block = block
            current_index += 1
        return True

# --- FLASK REST API ---
app = Flask(__name__)
blockchain = TadyCoin()

@app.route('/', methods=['GET'])
def home():
    return "Tady Coin server běží! API endpointy: /blocks, /mine, /validate", 200

@app.route('/transaction', methods=['POST'])
def new_transaction():
    values = request.get_json()
    if not values or not all(k in values for k in ['from', 'to', 'amount']):
        return 'Chybí hodnoty', 400
    index = blockchain.add_transaction(values['from'], values['to'], values['amount'])
    return jsonify({'message': f'Transakce bude přidána do bloku {index}'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_last_block()
    last_nonce = last_block['nonce']
    
    nonce = blockchain.proof_of_work(last_nonce)
    blockchain.add_transaction(sender="0", recipient="Těžař", amount=1)
    
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)

    return jsonify({
        'message': 'Nový blok vytěžen a uložen!',
        'block': block
    }), 200

@app.route('/blocks', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain, 'length': len(blockchain.chain)}), 200

@app.route('/validate', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({
        'is_valid': is_valid, 
        'message': 'V POŘÁDKU' if is_valid else 'NARUŠENO! Data byla změněna.'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)