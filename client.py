from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pypresence import Presence
import time
import os
import json
import socket
import threading
import random
from collections import deque

# Загрузка конфигурации
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except:
    config = {
        "game_mode": "offline",
        "server_ip": "localhost",
        "server_port": 5555,
        "username": "Player",
        "fov": 90,
        "mouse_sensitivity": 40
    }

# Discord RPC инициализация
try:
    RPC = Presence("112233445566778899")
    RPC.connect()
    RPC.update(
        details="Играет в Quadix",
        state="Строит мир",
        large_image="quadix_logo",
        large_text="Quadix Game",
        start=time.time()
    )
except:
    pass

class NetworkManager:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.message_queue = deque()
        self.last_send_time = 0
        self.player_id = ""
        
    def connect(self, host, port):
        try:
            self.socket.connect((host, port))
            self.connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print(f"[CLIENT] Ошибка подключения: {e}")
            return False
    
    def receive_messages(self):
        while self.connected:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                self.message_queue.append(message)
            except:
                self.connected = False
                break
    
    def send(self, message):
        if self.connected and time.time() - self.last_send_time > 0.05:
            try:
                self.socket.send(json.dumps(message).encode('utf-8'))
                self.last_send_time = time.time()
            except:
                self.connected = False
    
    def disconnect(self):
        if self.connected:
            self.connected = False
            self.socket.close()

app = Ursina()

# Отключаем все стандартные overlay-элементы
window.fps_counter.enabled = False
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False

window.title = 'Quadix'
window.icon = 'resources/icon.ico'

# Инициализация сетевого менеджера
network = NetworkManager()
is_online = config.get("game_mode", "offline") == "online"

if is_online:
    server_ip = config.get("server_ip", "localhost")
    server_port = config.get("server_port", 5555)
    if network.connect(server_ip, server_port):
        print("[CLIENT] Успешное подключение к серверу")
    else:
        print("[CLIENT] Не удалось подключиться к серверу, переключение в оффлайн режим")
        is_online = False

class NetworkPlayer(Entity):
    def __init__(self, player_id, username, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture='white_cube',
            color=color.random_color(),
            scale=(0.9, 1.8, 0.9),
            origin_y=-0.5,
            collider='box'
        )
        self.player_id = player_id
        self.username = username
        self.name_tag = Text(
            text=self.username,
            parent=self,
            y=1.2,
            world_scale=10,
            billboard=True,
            color=color.white
        )
        self.last_update_time = time.time()
        
    def update_position(self, new_pos):
        self.position = new_pos
        self.last_update_time = time.time()
        
    def update(self):
        # Если игрок не получал обновлений более 2 секунд, считаем его отключившимся
        if time.time() - self.last_update_time > 2:
            destroy(self.name_tag)
            destroy(self)

network_players = {}

class Voxel(Entity):
    def __init__(self, position=(0,0,0), texture='grass', network_id=None):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            origin_y=0.5,
            scale=1.0,
            collider='box'
        )
        self.highlight = Entity(
            parent=self,
            model='cube',
            color=color.rgba(0, 0, 0, 0.25),
            scale=1.001,
            origin_y=0.49995,
            visible=False
        )
        self.network_id = network_id or f"{time.time()}_{random.randint(0, 10000)}"
    
    def update(self):
        self.highlight.visible = mouse.hovered_entity == self
    
    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity == self:
            self.destroy_block()
        
        if key == 'right mouse down' and mouse.hovered_entity == self:
            self.place_block()
    
    def destroy_block(self):
        destroy(self)
        destroy_sound.play()
        if self in boxes:
            boxes.remove(self)
        
        if is_online:
            network.send({
                'type': 'destroy_block',
                'position': (self.position.x, self.position.y, self.position.z),
                'network_id': self.network_id
            })
    
    def place_block(self):
        new_pos = self.position + mouse.normal
        block_texture = blocks[hotbar_slots[current_texture_index].block_index]
        new_block = Voxel(position=new_pos, texture=block_texture)
        place_sound.play()
        boxes.append(new_block)
        
        if is_online:
            network.send({
                'type': 'place_block',
                'position': (new_pos.x, new_pos.y, new_pos.z),
                'texture': block_texture,
                'network_id': new_block.network_id
            })

# Создаем текстовый объект для дебаг-информации
debug_text = Text(
    position=window.top_left,
    origin=(-0.5, 0.5),
    scale=(1, 1),
    color=color.white,
    background=False,
    visible=False
)

def update_debug_info():
    current_block = blocks[hotbar_slots[current_texture_index].block_index]
    network_status = "ONLINE" if is_online and network.connected else "OFFLINE"
    players_count = len(network_players)
    
    debug_text.text = (
        f"FPS: {round(1/time.dt)}\n"
        f"Координаты: {round(player.x, 1), round(player.y, 1), round(player.z, 1)}\n"
        f"Объектов: {len(scene.entities)}\n"
        f"Скорость: {round(player.speed, 1)}\n"
        f"Режим полета: {'ВКЛ' if player.flying else 'ВЫКЛ'}\n"
        f"Высота камеры: {round(player.camera_pivot.y, 2)}\n"
        f"Блок в руке: {current_block}\n"
        f"Сеть: {network_status}\n"
        f"Игроков онлайн: {players_count}"
    )

# Настройки игрока
player = FirstPersonController(
    height=1.8,
    jump_height=1.25,
    mouse_sensitivity=Vec2(config.get("mouse_sensitivity", 40), config.get("mouse_sensitivity", 40))
)
player.camera_pivot.y = 1.7
player.network_id = f"player_{random.randint(1000, 9999)}"
player.last_network_update = 0

# Настройки окна
window.color = color.hex("#87CEEB")
window.title = 'Quadix'
window.borderless = False

# Настройки зума
default_fov = config.get("fov", 90)
zoom_fov = 30
zooming = False

# Настройки приседания
sneak_amount = 0.2
original_camera_y = player.camera_pivot.y
is_sneaking = False

Texture.default_path = './resources/'
Audio.default_path = './resources/'
place_sound = Audio('place_block.mp3', autoplay=False)
destroy_sound = Audio('destroy_block.mp3', autoplay=False)

blocks = ['grass', 'stone', 'dirt', 'planks', 'log', 'leaves', 'emerald_ore', 'dern', 'furnace', 'cooper_ore', 'aluminum_ore', 'gold_ore', 'iron_ore']
current_texture_index = 0

# Хотбар
hotbar_slots = []
for i in range(9):
    slot = Entity(
        parent=camera.ui,
        model='quad',
        texture=blocks[i % len(blocks)],
        scale=(0.05, 0.05),
        x=-0.4 + i * 0.08,
        y=-0.45,
        z=-1
    )
    slot.block_index = i % len(blocks)
    hotbar_slots.append(slot)

selector = Entity(
    parent=camera.ui,
    model='quad',
    color=color.white,
    scale=(0.055, 0.055),
    x=-0.4 + current_texture_index * 0.08,
    y=-0.45,
    z=-0.9
)

# Инвентарь
inventory_bg = Entity(
    parent=camera.ui,
    model='quad',
    color=color.color(0, 0, 0.1, 0.8),
    scale=(0.5, 0.6),
    position=(0, 0, -0.5),
    visible=False
)

# Предварительная загрузка инвентаря для предотвращения мерцания
inventory_bg.enabled = False

inventory_slots = []
for i, block in enumerate(blocks):
    row = i // 5
    col = i % 5
    x = -0.2 + col * 0.1
    y = 0.2 - row * 0.1
    
    slot = Button(
        parent=inventory_bg,
        model='quad',
        texture=block,
        scale=(0.09 , 0.075),
        position=(x, y, -0.1),
        color=color.white,
        origin=(0, 0)  
    )
    slot.block_index = i
    inventory_slots.append(slot)

player.flying = False
player.sprint_speed = 10
player.sneak_speed = 2
player.normal_speed = 5
player.fly_speed = 5

# Создаем платформу 
platform_position = (15, 0, 15)
boxes = []
for i in range(30):
    for j in range(30):
        box = Voxel(
            position=(platform_position[0] + j - 15, platform_position[1], platform_position[2] + i - 15),
            texture='grass'
        )
        boxes.append(box)

def respawn_player():
    player.position = (platform_position[0], platform_position[1] + 2, platform_position[2])
    player.velocity_y = 0

def toggle_fullscreen():
    if window.fullscreen:
        window.fullscreen = False
        window.borderless = False
        window.size = (1280, 720)
        window.position = (0, 0)
    else:
        window.fullscreen = True
        window.borderless = True

def toggle_inventory():
    inventory_bg.visible = not inventory_bg.visible
    inventory_bg.enabled = inventory_bg.visible
    mouse.locked = not inventory_bg.visible
    player.enabled = not inventory_bg.visible

def select_block_from_inventory():
    if mouse.hovered_entity in inventory_slots:
        clicked_block_index = mouse.hovered_entity.block_index
        hotbar_slots[current_texture_index].texture = blocks[clicked_block_index]
        hotbar_slots[current_texture_index].block_index = clicked_block_index

def update_rpc_status():
    try:
        current_block = blocks[hotbar_slots[current_texture_index].block_index]
        RPC.update(
            details=f"Текущий блок: {current_block}",
            state="File: Quadix.py",
            large_image="quadix_logo",
            large_text=current_block,
            start=time.time()
        )
    except:
        pass

def process_network_messages():
    while network.message_queue:
        message = network.message_queue.popleft()
        msg_type = message.get('type')
        
        if msg_type == 'init':
            # Инициализация игрового мира
            for player_id, player_data in message.get('players', {}).items():
                if player_id != network.player_id and player_id not in network_players:
                    network_players[player_id] = NetworkPlayer(
                        player_id=player_id,
                        username=player_data['username'],
                        position=player_data['position']
                    )
            
            for pos, block_data in message.get('world', {}).items():
                pos_tuple = tuple(pos)
                if not any(b.position == pos_tuple for b in boxes):
                    Voxel(
                        position=pos_tuple,
                        texture=block_data['texture'],
                        network_id=block_data['network_id']
                    )
        
        elif msg_type == 'player_joined':
            if message['player_id'] != network.player_id and message['player_id'] not in network_players:
                network_players[message['player_id']] = NetworkPlayer(
                    player_id=message['player_id'],
                    username=message['username'],
                    position=message['position']
                )
        
        elif msg_type == 'player_moved':
            if message['player_id'] in network_players:
                network_players[message['player_id']].update_position(message['position'])
        
        elif msg_type == 'player_left':
            if message['player_id'] in network_players:
                destroy(network_players[message['player_id']])
                destroy(network_players[message['player_id']].name_tag)
                del network_players[message['player_id']]
        
        elif msg_type == 'place_block':
            pos = message['position']
            if not any(b.position == pos for b in boxes):
                Voxel(
                    position=pos,
                    texture=message['texture'],
                    network_id=message['network_id']
                )
        
        elif msg_type == 'destroy_block':
            for box in boxes:
                if box.position == tuple(message['position']):
                    destroy(box)
                    if box in boxes:
                        boxes.remove(box)
                    break

def update():
    global zooming, is_sneaking, current_texture_index
    
    # Обработка сетевых сообщений
    if is_online:
        process_network_messages()
        
        # Отправка обновления позиции игрока (не чаще 10 раз в секунду)
        if time.time() - player.last_network_update > 0.1:
            network.send({
                'type': 'move',
                'position': [player.x, player.y, player.z]
            })
            player.last_network_update = time.time()
    
    # Обновляем дебаг-информацию
    update_debug_info()
    
    selector.x = -0.4 + current_texture_index * 0.08
    
    # Управление скоростью и приседанием
    if held_keys['control']:
        player.speed = player.sprint_speed
        if is_sneaking:
            is_sneaking = False
            player.camera_pivot.y = original_camera_y
    elif held_keys['shift'] and not player.flying:
        player.speed = player.sneak_speed
        if not is_sneaking:
            is_sneaking = True
            player.camera_pivot.y = original_camera_y - sneak_amount
    else:
        player.speed = player.normal_speed
        if is_sneaking:
            is_sneaking = False
            player.camera_pivot.y = original_camera_y

    if time.time() % 15 < time.dt:
        update_rpc_status()
    
    # Управление зумом
    if held_keys['c']:
        if not zooming:
            zooming = True
            camera.fov = zoom_fov
    else:
        if zooming:
            zooming = False
            camera.fov = default_fov
    
    # Управление полетом
    if player.flying:
        if held_keys['space']:
            player.y += player.fly_speed * time.dt
        if held_keys['shift']:
            player.y -= player.fly_speed * time.dt

def input(key):
    global current_texture_index
    
    if key == 'f3':
        debug_text.visible = not debug_text.visible
    
    if key == 'f11':
        toggle_fullscreen()
    
    if key == 'e':
        toggle_inventory()
    
    if key in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        current_texture_index = int(key) - 1
    
    if key == 'scroll down':
        current_texture_index = (current_texture_index + 1) % 9
    if key == 'scroll up':
        current_texture_index = (current_texture_index - 1) % 9
    if key == 'escape':
        if inventory_bg.visible:
            toggle_inventory()
        else:
            application.quit()
    if key == 'v':
        player.flying = not player.flying
        player.gravity = 0 if player.flying else 1.0
        if not player.flying and is_sneaking:
            player.camera_pivot.y = original_camera_y
    if key == 'r':
        respawn_player()
    
    # Выбор блока из инвентаря
    if key == 'left mouse down' and inventory_bg.visible:
        select_block_from_inventory()

# Предзагрузка инвентаря
inventory_bg.enabled = True
inventory_bg.visible = False

# При подключении к серверу отправляем информацию о себе
if is_online and network.connected:
    network.player_id = player.network_id
    network.send({
        'type': 'join',
        'username': config.get("username", "Player"),
        'position': [player.x, player.y, player.z]
    })

# Завершение работы
def on_exit():
    try:
        RPC.close()
    except:
        pass
    if is_online:
        network.disconnect()

app.on_exit = on_exit
respawn_player()
app.run()