import urllib.request
import urllib.error
import json

BASE_URL = 'http://localhost:5000'

def http_request(path, method='GET', body=None):
    url = f"{BASE_URL}{path}"
    headers = {'Content-Type': 'application/json'} if body else {}
    data = json.dumps(body).encode('utf-8') if body else None
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f" Chyba připojení: {e.reason}")
        return None

def run_demo():
    print('Spouštím Tady Coin klientské demo...\n')

    print('1. Odesílám transakci: Alice -> Bob (Množství: 100)')
    http_request('/transaction', method='POST', body={'from': 'Alice', 'to': 'Bob', 'amount': 100})

    print('2. Odesílám transakci: Bob -> Charlie (Množství: 20)')
    http_request('/transaction', method='POST', body={'from': 'Bob', 'to': 'Charlie', 'amount': 20})

    print('\n  3. Těžím nový blok a ukládám do JSONu...')
    mine_msg = http_request('/mine', method='GET')
    if mine_msg:
        print(f" Vytěženo! Blok {mine_msg['block']['index']} uložen.")

    print('\n 4. Ověřuji integritu blockchainu...')
    validation = http_request('/validate', method='GET')
    if validation:
        print(f"Výsledek: {validation['message']}")

if __name__ == '__main__':
    run_demo()