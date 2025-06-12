import socket
import json

HOST = '0.0.0.0'
PORT = 5000

with open('playbooks.json') as f:
    playbooks = json.load(f)

def handle_client(conn):
    conn.sendall(b"Bienvenue sur le SOC Playbook Server\nTape 'list' pour voir les playbooks\n")
    while True:
        conn.sendall(b"\n> ")
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        if data.lower() == 'list':
            response = "\n".join(f"{pb['id']}. {pb['type']} - {pb['severity']}" for pb in playbooks)
        elif data.isdigit():
            found = next((pb for pb in playbooks if pb['id'] == int(data)), None)
            if found:
                response = f"\n{found['type']}:\n" + "\n".join(f"- {s}" for s in found['steps'])
            else:
                response = "Playbook introuvable."
        elif data.lower() in ['exit', 'quit']:
            conn.sendall(b"A bientôt !\n")
            break
        else:
            response = "Commande inconnue. Tape 'list' ou un ID."

        conn.sendall(response.encode())

    conn.close()

# Serveur TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Serveur lancé sur {PORT}")
    while True:
        conn, addr = s.accept()
        print(f"[+] Connexion depuis {addr}")
        handle_client(conn)
