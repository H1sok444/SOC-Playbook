import socket
import json

HOST = '0.0.0.0'
PORT = 5000

with open('playbooks.json', 'r', encoding='utf-8') as f:
    playbooks = json.load(f)

def handle_client(conn):
    conn.sendall(b"Bienvenue sur le SOC Playbook Server\nTape 'list' pour voir les playbooks\n")
    while True:
        conn.sendall(b"\n> ")
        data = conn.recv(1024).decode().strip()
        if not data:
            break
        if data.lower() == 'list':
            response = "\n".join(f"{pb['id']}. {pb['name']} (PrioritÃ©: {pb['severity']})" for pb in playbooks)
        elif data.isdigit():
            found = next((pb for pb in playbooks if pb['id'] == int(data)), None)
            if found:
                playbook_data = found['data']
                response = f"\n--- {playbook_data['title']} ---\n"
                response += f"Description: {playbook_data['description']}\n"
                response += f"SIDs AssociÃ©s: {', '.join(map(str, playbook_data['sids']))}\n\n"
                for step in playbook_data['steps']:
                    response += f"{step['phase']}:\n"
                    for action in step['actions']:
                        response += f"  - {action}\n"
            else:
                response = "Playbook introuvable."
        elif data.lower() in ['exit', 'quit']:
            conn.sendall("Ã€ bientÃ´t !\n".encode('utf-8'))
            break
        else:
            response = "Commande inconnue. Tape 'list' ou un ID."

        conn.sendall(response.encode('utf-8'))

    conn.close()

# Serveur TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Serveur lancÃ© sur {PORT}")
    while True:
        conn, addr = s.accept()
        print(f"[+] Connexion depuis {addr}")
        handle_client(conn)
