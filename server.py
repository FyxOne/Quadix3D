import socket
import threading
import json
import time
from collections import defaultdict

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        self.clients = {}
        self.players = {}
        self.world = defaultdict(dict)  # Хранение блоков мира
        self.running = True
        
        print(f"[SERVER] Сервер запущен на {host}:{port}")

    def broadcast(self, message, exclude=None):
        """Отправка сообщения всем клиентам"""
        if exclude is None:
            exclude = []
        for client_id, client in list(self.clients.items()):
            if client_id not in exclude:
                try:
                    client.send(json.dumps(message).encode('utf-8'))
                except:
                    self.remove_client(client_id)

    def handle_client(self, client, address):
        """Обработка подключения клиента"""
        client_id = f"{address[0]}:{address[1]}"
        self.clients[client_id] = client
        print(f"[SERVER] Подключен клиент {client_id}")

        try:
            while self.running:
                data = client.recv(4096)
                if not data:
                    break

                message = json.loads(data.decode('utf-8'))
                self.process_message(client_id, message)

        except Exception as e:
            print(f"[SERVER] Ошибка с клиентом {client_id}: {e}")
        finally:
            self.remove_client(client_id)

    def process_message(self, client_id, message):
        """Обработка входящих сообщений"""
        msg_type = message.get('type')

        if msg_type == 'join':
            # Новый игрок присоединился
            username = message.get('username', 'Player')
            self.players[client_id] = {
                'username': username,
                'position': message.get('position', [0, 0, 0]),
                'last_update': time.time()
            }
            # Отправляем новому игроку текущее состояние мира
            init_data = {
                'type': 'init',
                'players': self.players,
                'world': self.world
            }
            self.clients[client_id].send(json.dumps(init_data).encode('utf-8'))
            # Оповещаем других игроков
            self.broadcast({
                'type': 'player_joined',
                'player_id': client_id,
                'username': username,
                'position': message.get('position', [0, 0, 0])
            }, exclude=[client_id])

        elif msg_type == 'move':
            # Обновление позиции игрока
            if client_id in self.players:
                self.players[client_id]['position'] = message['position']
                self.players[client_id]['last_update'] = time.time()
                # Пересылаем обновление другим игрокам
                self.broadcast({
                    'type': 'player_moved',
                    'player_id': client_id,
                    'position': message['position']
                }, exclude=[client_id])

        elif msg_type == 'place_block':
            # Размещение блока
            pos = tuple(message['position'])
            self.world[pos] = {
                'texture': message['texture'],
                'network_id': message['network_id']
            }
            self.broadcast(message)

        elif msg_type == 'destroy_block':
            # Удаление блока
            pos = tuple(message['position'])
            if pos in self.world:
                del self.world[pos]
            self.broadcast(message)

    def remove_client(self, client_id):
        """Удаление отключившегося клиента"""
        if client_id in self.clients:
            self.clients[client_id].close()
            del self.clients[client_id]
            if client_id in self.players:
                self.broadcast({
                    'type': 'player_left',
                    'player_id': client_id
                })
                del self.players[client_id]
            print(f"[SERVER] Клиент {client_id} отключен")

    def start(self):
        """Запуск сервера"""
        print("[SERVER] Ожидание подключений...")
        try:
            while self.running:
                client, address = self.server.accept()
                threading.Thread(target=self.handle_client, args=(client, address)).start()
        except KeyboardInterrupt:
            print("[SERVER] Остановка сервера...")
            self.running = False
            self.server.close()

if __name__ == "__main__":
    config = {}
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except:
        pass

    server = GameServer(
        host=config.get('server_ip', '0.0.0.0'),
        port=config.get('server_port', 5555)
    )
    server.start()