[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/90Mprfp5)
# Network Programming - Final Project [G04]

## Anggota Kelompok
| Nama | NRP | Kelas |
| --------------------------------| -----------| ------- |
| Alfianz Rizqia Ilahi Loven Kary | 5025241164 | Kelas C |
| Aqil Syafiq Dzaky               | 5025241200 | Kelas C |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```

```
---
## Daftar Isi

* [Struktur Directory](#struktur-directory)

* [Folder client/](#folder-client)

  * [Penjelasan app.py](#penjelasan-apppy)
  * [Penejelasan assets.py](#penejelasan-assetspy)
  * [Penejelasan audio.py](#penejelasan-audiopy)
  * [Penejelasan event_handler.py](#penejelasan-event_handlerpy) belom
  * [Penejelasan game_logic.py](#penejelasan-game_logicpy)
  * [Penejelasan main.py](#penejelasan-mainpy)
  * [Penejelasan network_client.py](#penejelasan-network_clientpy) 
  * [Penejelasan message_handler.py](#penejelasan-message_handlerpy)
  * [Penejelasan screens.py](#penejelasan-screenspy) belom
  * [Penejelasan state.py](#penejelasan-statepy)

* [Folder Server/](#folder-server)

  * [Penejelasan auth_service.py](#penejelasan-auth_servicepy)
  * [Penejelasan client_handler.py](#penejelasan-client_handlerpy)
  * [Penejelasan config.py](#penejelasan-configpy)
  * [Penejelasan database.py](#penejelasan-databasepy)
  * [Penejelasan game_room.py](#penejelasan-game_roompy)
  * [Penejelasan logger.py](#penejelasan-loggerpy)
  * [Penejelasan main.py](#penejelasan-mainpy-1)
  * [Penejelasan matchmaking.py](#penejelasan-matchmakingpy)
  * [Penejelasan ranking_service.py](#penejelasan-ranking_servicepy)
  * [Penejelasan replay_service.py](#penejelasan-replay_servicepy)
  * [Penejelasan response_builder.py](#penejelasan-response_builderpy)
  * [Penejelasan room_manager.py](#penejelasan-room_managerpy)
  * [Penejelasan socket_server.py](#penejelasan-socket_serverpy)

* [Folder server/handlers](#folder-serverhandlers)

  * [Penjelasan auth_handler.py](#penjelasan-auth_handlerpy)
  * [Penjelasan game_handler.py](#penjelasan-game_handlerpy)
  * [Penjelasan leaderboard_handler.py](#penjelasan-leaderboard_handlerpy)
  * [Penjelasan matchmaking_handler.py](#penjelasan-matchmaking_handlerpy)
  * [Penjelasan placement_handler.py](#penjelasan-placement_handlerpy)
  * [Penjelasan replay_handler.py](#penjelasan-replay_handlerpy)
  * [Penjelasan room_handler.py](#penjelasan-room_handlerpy)

* [Folder shared/](#folder-shared)

  * [Penjelasan constants.py](#penjelasan-constantspy)
  * [Penjelasan message_type.py](#penjelasan-message_typepy)
  * [Penjelasan serializer.py](#penjelasan-serializerpy)

* [Screenshot Hasil](#screenshot-hasil)

---
## Penjelasan Program
### Struktur Directory
```
Project/
├── client/
│   ├── app.py
│   ├── assets.py
│   ├── audio.py
│   ├── event_handler.py
│   ├── game_logic.py
│   ├── main.py
│   ├── message_handler.py
│   ├── network_client.py
│   ├── screens.py
│   ├── state.py
│   ├── __init__.py
│   │
│   ├── assets/
│   │   ├── backgrounds/
│   │   │   └── main_bg.jpg
│   │   ├── fonts/
│   │   │   ├── JollyRoger-Regular.ttf
│   │   │   ├── PirataOne-Regular.ttf
│   │   │   └── Windlass.ttf
│   │   ├── music/
│   │   │   ├── battle_music.mp3
│   │   │   ├── battle_music_secret.mp3
│   │   │   ├── kode_berhasil.mp3
│   │   │   ├── main_music.mp3
│   │   │   └── main_music_secret.mp3
│   │   └── ships/
│   │       ├── battle_ship.png
│   │       ├── cyber_ship.png
│   │       ├── pirate_boat.png
│   │       ├── steel_ship.png
│   │       └── wooden_boat.png
│   │
│   └── ui/
│       ├── components.py
│       ├── theme.py
│       ├── ui_config.py
│       └── __init__.py
│
├── server/
│   ├── auth_service.py
│   ├── client_handler.py
│   ├── config.py
│   ├── database.py
│   ├── game_room.py
│   ├── logger.py
│   ├── main.py
│   ├── matchmaking.py
│   ├── ranking_service.py
│   ├── replay_service.py
│   ├── response_builder.py
│   ├── room_manager.py
│   ├── socket_server.py
│   │
│   └── handlers/
│       ├── auth_handler.py
│       ├── game_handler.py
│       ├── leaderboard_handler.py
│       ├── matchmaking_handler.py
│       ├── placement_handler.py
│       ├── replay_handler.py
│       ├── room_handler.py
│       └── __init__.py
│
├── shared
│   ├── constants.py
│   ├── message_type.py
│   └── serializer.py
│
├── data/
│   ├── battleship.db
│   └── replays/
│       └── <file replay pertandingan (*.json)>
│
├── logs/
│   └── server.log
│
└── tests/
    ├── load_test.py
    └── protocol_test.py
```

Folder `client/` berisi seluruh komponen antarmuka dan logika sisi klien yang berjalan di mesin pemain. Subfolder `assets/` menyimpan seluruh aset non-kode seperti gambar kapal, font, dan file musik. Subfolder `ui/` berisi modul pendukung tampilan.

Folder `server/` berisi komponen utama server yang mengelola koneksi, autentikasi, pertandingan, dan penyimpanan data. Subfolder `handlers/` berisi handler spesifik untuk setiap jenis pesan yang diterima dari klien.

Folder `shared/` berisi modul yang digunakan bersama oleh server maupun klien, seperti konstanta permainan, tipe pesan, dan serializer.

Folder `data/` menyimpan database SQLite dan file JSON replay pertandingan. 

Folder `logs/` menyimpan log aktivitas server. 

Folder `tests/` berisi skrip pengujian protokol dan uji beban.

### Folder client/
#### Penjelasan app.py
File `app.py` pada folder `client/` berfungsi sebagai pusat aplikasi klien yang menginisialisasi Pygame, mendefinisikan seluruh variabel state global, membuat semua elemen UI, serta menghubungkan modul-modul klien menjadi satu program yang berjalan.

---

##### Mekanisme bind_module_functions

```
def bind_module_functions(module):
    for name in dir(module):
        value = getattr(module, name)
        if callable(value):
            value = type(value)(value.__code__, globals(), ...)
            globals()[name] = value

bind_module_functions(client_game_logic)
bind_module_functions(client_screens)
bind_module_functions(client_message_handler)
bind_module_functions(client_event_handler)
```

Bagian ini digunakan untuk menyuntikkan semua fungsi dari modul-modul klien ke dalam namespace global `app.py`. Teknik ini memungkinkan fungsi di modul-modul terpisah seperti `game_logic`, `screens`, `message_handler`, dan `event_handler` dapat saling mengakses variabel state global yang didefinisikan di `app.py` tanpa perlu melewatkannya sebagai argumen.

---

##### Inisialisasi State dan UI

```
screen_state = "TITLE"
placed_ships = []
local_board = [[CELL_EMPTY ...]]
enemy_board = [[CELL_EMPTY ...]]
leaderboard_data = []
replay_list = []
is_spectator = False

username_input = TextInput(...)
login_button = Button(...)
quick_play_button = Button(...)
game_forfeit_button = Button(...)
# ... dan puluhan elemen UI lainnya
```

Bagian ini digunakan untuk mendefinisikan seluruh variabel state permainan seperti state layar aktif, data papan, data sesi, dan data fitur, serta menginisialisasi semua objek UI yang digunakan di berbagai layar.

---

##### Inisialisasi dan Koneksi

```
client = NetworkClient()
client.on_message = handle_server_message

try:
    client.connect()
except ConnectionRefusedError:
    print("Server belum jalan. Jalankan: python -m server.main")
    pygame.quit()
    sys.exit()

run_loop()
```

Bagian ini digunakan untuk menghubungkan klien ke server, menetapkan callback penerimaan pesan ke fungsi `handle_server_message`, dan memulai game loop utama.

---

##### Ringkasan

`app.py` pada folder `client/` berfungsi sebagai inti aplikasi klien yang menginisialisasi seluruh komponen Pygame, mendefinisikan state global, memuat modul-modul fungsional, dan menjalankan loop permainan.

---
#### Penejelasan assets.py
File `assets.py` pada folder `client/` berfungsi sebagai modul pemuat aset visual yang digunakan oleh antarmuka permainan.

---

##### Fungsi load_font dan load_ship_images

```
def load_font(path, size, fallback="arial"):
    try:
        return pygame.font.Font(path, size)
    except FileNotFoundError:
        return pygame.font.SysFont(fallback, size)

def load_ship_images():
    images = {}
    for ship in SHIPS:
        images[ship["name"]] = pygame.image.load(image_path).convert_alpha()
    return images
```

Fungsi `load_font` digunakan untuk memuat font kustom dari file TTF dengan fallback ke font sistem apabila file tidak ditemukan. Fungsi `load_ship_images` digunakan untuk memuat semua gambar kapal dari path yang didefinisikan di `constants.py` dengan penanganan error apabila file tidak tersedia.

---

##### Ringkasan

`assets.py` pada folder `client/` berfungsi sebagai modul pemuat aset yang menangani inisialisasi font dan gambar kapal dengan mekanisme fallback agar program tetap berjalan meski aset tidak lengkap.

#### Penejelasan audio.py
File `audio.py` pada folder `client/` berfungsi untuk mengelola pemutaran musik latar dan efek suara selama permainan berlangsung.

---

##### Fungsi switch_music_if_needed dan get_music_type_for_state

```
def get_music_type_for_state(state):
    battle_states = ["GAME", "GAME_OVER", "SPECTATOR", "SPECTATOR_RESULT", "REPLAY_VIEWER"]
    if state in battle_states:
        return "BATTLE"
    return "MAIN"

def switch_music_if_needed():
    target_music_type = get_music_type_for_state(screen_state)
    if current_music_type == target_music_type:
        apply_music_volume()
        return
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
```

Fungsi `get_music_type_for_state` digunakan untuk menentukan jenis musik yang sesuai berdasarkan state layar saat ini, membedakan antara musik menu utama dan musik pertempuran. Fungsi `switch_music_if_needed` digunakan untuk mengganti musik secara otomatis ketika state layar berubah tanpa memuat ulang apabila jenis musik belum berubah.

---

#### Fungsi handle_easter_key dan trigger_easter_code

```
def handle_easter_key(event):
    easter_code_buffer = (easter_code_buffer + char.upper())[-7:]
    if easter_code_buffer == "HESOYAM":
        trigger_easter_code()

def trigger_easter_code():
    easter_pending_secret_state = not secret_music_enabled
    easter_popup_open = True
    play_easter_sound()
```

Fungsi `handle_easter_key` digunakan untuk mendeteksi pengetikan kode rahasia tertentu di layar menu utama dengan menyimpan riwayat 7 karakter terakhir yang diketik. Fungsi `trigger_easter_code` digunakan untuk mengaktifkan mode musik rahasia dan menampilkan popup konfirmasi apabila kode yang benar dimasukkan.

---

##### Ringkasan

`audio.py` pada folder `client/` berfungsi sebagai manajer audio yang menangani pergantian musik latar sesuai state permainan, pengaturan volume, dan sebuah easter egg berupa musik rahasia yang dapat diaktifkan melalui kode tertentu.

---

#### Penejelasan event_handler.py
File `event_handler.py` berfungsi sebagai modul pengendali event utama pada sisi klien yang menangani input keyboard, mouse, transisi state layar, pengiriman aksi ke server, serta pemanggilan fungsi render setiap frame.

---

##### Fungsi run_loop

```
def run_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and screen_state == "TITLE":
                screen_state = "AUTH"
                status_text = "Please login or register"
            if screen_state == "AUTH":
                username_input.handle_event(event)
                password_input.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ...
                elif event.key == pygame.K_p and session_id:
                    ...
            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_state == "MAIN_MENU":
                    ...
                elif screen_state == "GAME":
                    ...

        current_time = pygame.time.get_ticks()
        if session_id and latency_auto_enabled and current_time - last_ping_time >= PING_INTERVAL_MS:
            client.send({"type": PING, "session_id": session_id, "payload": {"sent_at": current_time}})

        if screen_state == "TITLE":
            draw_title_screen()
        elif screen_state == "AUTH":
            draw_auth_screen()
        elif screen_state == "GAME":
            draw_game()

        pygame.display.flip()
        clock.tick(60)
```

Fungsi `run_loop` digunakan sebagai loop utama aplikasi klien yang terus-menerus membaca event dari `pygame`, memproses interaksi pengguna sesuai `screen_state`, mengirimkan perintah ke server, memperbarui fitur seperti auto ping, lalu merender layar yang sesuai pada setiap frame. Fungsi ini juga menangani perpindahan antar menu, kontrol placement, aksi permainan, mode spectator, replay, leaderboard, settings, serta penutupan aplikasi secara bersih ketika loop berakhir.

---

##### Ringkasan

`event_handler.py` berfungsi sebagai pusat kendali interaksi pengguna di sisi klien yang menghubungkan input pemain, perubahan state aplikasi, komunikasi aksi ke server, dan proses rendering layar secara real-time.

---

#### Penejelasan game_logic.py
File `game_logic.py` pada folder `client/` berfungsi untuk menyimpan seluruh logika permainan sisi klien, mulai dari pengelolaan penempatan kapal, validasi input, pengiriman aksi ke server, hingga pemrosesan data replay.

---

##### Fungsi place_ship_at_grid dan can_place_ship

```
def can_place_ship(cells):
    for cell in cells:
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return False
        if local_board[y][x] == CELL_SHIP:
            return False
    return True

def place_ship_at_grid(grid_x, grid_y):
    cells = get_ship_cells(grid_x, grid_y, ship, orientation)
    if not can_place_ship(cells):
        status_text = "Invalid placement"
        return
    # tandai sel di local_board sebagai CELL_SHIP
```

Fungsi `can_place_ship` digunakan untuk memvalidasi apakah kapal dapat ditempatkan pada sel-sel tertentu tanpa keluar batas atau bertumpang tindih. Fungsi `place_ship_at_grid` digunakan untuk menempatkan kapal di papan lokal berdasarkan koordinat grid yang dipilih pemain.

---

##### Fungsi reset_game_state dan send_login_from_auth

```
def reset_game_state():
    placed_ships = []
    local_board = [[CELL_EMPTY ...]]
    enemy_board = [[CELL_EMPTY ...]]
    current_turn_session_id = None
    winner_session_id = None

def send_login_from_auth():
    valid, message = validate_auth_input()
    client.send({"type": LOGIN, "payload": {"username": ..., "password": ...}})
```

Fungsi `reset_game_state` digunakan untuk mengatur ulang semua variabel state permainan ke kondisi awal sebelum pertandingan baru dimulai. Fungsi `send_login_from_auth` digunakan untuk memvalidasi input form autentikasi lalu mengirimkan pesan LOGIN ke server.

---

#### Fungsi build_replay_board dan apply_replay_events

```
def apply_replay_events(board_1, board_2, replay, step_index):
    for event in events[:step_index]:
        target_board = board_2 if shooter == player_1 else board_1
        if result == "HIT":
            target_board[y][x] = CELL_HIT
        elif result == "MISS":
            target_board[y][x] = CELL_MISS

def build_replay_board(replay, side, step_index):
    board_1 = build_board_from_ships(ships_1)
    apply_replay_events(board_1, board_2, replay, step_index)
    return board_1 if side == 1 else board_2
```

Fungsi `apply_replay_events` digunakan untuk memutar ulang event tembakan dari data replay hingga langkah tertentu ke papan rekonstruksi. Fungsi `build_replay_board` digunakan untuk membangun tampilan papan pada frame replay tertentu dengan menggabungkan posisi kapal awal dan event yang sudah terjadi.

---

##### Ringkasan

`game_logic.py` pada folder `client/` berfungsi sebagai pusat logika sisi klien yang mengelola interaksi pemain dengan papan, komunikasi ke server, dan pemrosesan data untuk fitur replay.

---
#### Penejelasan main.py
File `main.py` pada folder `client/` berfungsi sebagai titik masuk eksekusi aplikasi klien.

---

##### Entry Point

```
import client.app  # noqa: F401
```

Bagian ini digunakan untuk menjalankan klien dengan mengimpor `client.app` yang secara otomatis mengeksekusi seluruh inisialisasi dan game loop. Program dijalankan dengan perintah `python -m client.main` dari direktori root proyek.

---

##### Ringkasan

`main.py` pada folder `client/` berfungsi sebagai titik awal eksekusi yang menginisialisasi modul `app` untuk menjalankan aplikasi klien.

---

#### Penejelasan message_handler.py 
File `message_handler.py` berfungsi sebagai modul pemroses pesan dari server yang memperbarui state klien berdasarkan tipe pesan, baik untuk autentikasi, room, permainan, spectator, replay, leaderboard, maupun error.

---

##### Fungsi handle_server_message

```python
def handle_server_message(message):
    if message["type"] == LOGIN_SUCCESS:
        session_id = message["session_id"]
        username = message["payload"]["username"]
        status_text = "Login success"
        screen_state = "MAIN_MENU"
    elif message["type"] == ROOM_LIST_DATA:
        available_rooms = message["payload"].get("rooms", [])
        room_browser_status = f"Loaded {len(available_rooms)} room(s)"
        screen_state = "ROOM_BROWSER"
    elif message["type"] == PLACEMENT_START:
        reset_game_state()
        status_text = f"Place ship: {SHIPS[current_ship_index]['name']}"
        screen_state = "PLACEMENT"
    elif message["type"] == FIRE_RESULT:
        if payload["result"] == "HIT":
            enemy_board[y][x] = CELL_HIT
        else:
            enemy_board[y][x] = CELL_MISS
    elif message["type"] == GAME_OVER:
        winner_session_id = message["payload"]["winner_session_id"]
        status_text = message["payload"].get("message", "Game over")
        screen_state = "GAME_OVER"
```

Fungsi `handle_server_message` digunakan untuk membaca setiap pesan yang diterima klien dari server dan menyesuaikan state aplikasi berdasarkan nilai `type` pada pesan tersebut. Fungsi ini menangani alur autentikasi, pembuatan dan masuk room, pembaruan status room, awal placement, hasil pengiriman kapal, awal permainan, update spectator, hasil tembakan, pergantian giliran, replay, leaderboard, latency check melalui `PONG`, hingga penanganan pesan error.

---

##### Bagian penanganan room dan spectator

```python
elif message["type"] == ROOM_UPDATED:
    room = message["payload"]["room"]
    current_spectator_count = room.get("spectator_count", current_spectator_count)
    players = room.get("players", [])

elif message["type"] == SPECTATOR_JOINED:
    is_spectator = True
    spectator_player_1 = message["payload"]["player_1"]
    spectator_player_2 = message["payload"]["player_2"]
    spectator_board_1 = message["payload"]["player_1_board"]
    spectator_board_2 = message["payload"]["player_2_board"]

elif message["type"] == SPECTATOR_UPDATE:
    spectator_board_1 = message["payload"]["player_1_board"]
    spectator_board_2 = message["payload"]["player_2_board"]
    if message["payload"].get("winner_session_id"):
        open_replay_for_current_room("SPECTATOR_RESULT")
```

Bagian ini digunakan untuk memperbarui informasi room dan spectator secara dinamis. Ketika komposisi room berubah, klien menyesuaikan informasi lawan, jumlah spectator, dan tampilan layar. Ketika spectator bergabung atau menerima update pertandingan, klien memperbarui data papan kedua pemain, status pertandingan, dan dapat langsung membuka alur replay jika permainan telah selesai.

---

##### Bagian penanganan replay dan leaderboard

```python
elif message["type"] == REPLAY_LIST_DATA:
    replay_list = message["payload"]["replays"]
    screen_state = "REPLAY_LIST"

elif message["type"] == REPLAY_DETAIL_DATA:
    selected_replay = message["payload"]["replay"]
    if replay_source_state == "GAME_OVER":
        replay_step_index = 0
        screen_state = "REPLAY_VIEWER"
    elif replay_source_state == "SPECTATOR_RESULT":
        screen_state = "SPECTATOR_RESULT"

elif message["type"] == LEADERBOARD_DATA:
    leaderboard_data = message["payload"]["leaderboard"]
    screen_state = "LEADERBOARD"
```

Bagian ini digunakan untuk memuat data replay dan leaderboard dari server ke state klien. Data replay dapat diarahkan ke tampilan detail atau viewer tergantung asal navigasi, sedangkan data leaderboard digunakan untuk membuka halaman peringkat pemain pada antarmuka klien.

---

##### Ringkasan

`message_handler.py` berfungsi sebagai pusat sinkronisasi state klien terhadap respons server dengan memetakan setiap tipe pesan ke pembaruan data, perubahan layar, dan status permainan yang sesuai.

---

#### Penejelasan network_client.py
File `network_client.py` pada folder `client/` berfungsi sebagai modul koneksi jaringan sisi klien yang menangani pengiriman dan penerimaan pesan dari server melalui TCP.

---

##### Fungsi connect dan listen

```
def connect(self):
    self.socket.connect((self.host, self.port))
    self.connected = True
    thread = threading.Thread(target=self.listen, daemon=True)
    thread.start()

def listen(self):
    while self.connected:
        data = self.socket.recv(4096)
        self.buffer += data.decode("utf-8")

        while "\n" in self.buffer:
            raw_message, self.buffer = self.buffer.split("\n", 1)
            message = decode_message(raw_message)
            if self.on_message:
                self.on_message(message)
```

Fungsi `connect` digunakan untuk membuka koneksi TCP ke server dan menjalankan loop penerimaan pesan dalam thread daemon terpisah agar tidak memblokir thread utama. Fungsi `listen` digunakan untuk terus-menerus membaca data dari socket, memisahkan pesan berbasis delimiter newline, lalu meneruskan setiap pesan ke callback `on_message`.

---

##### Fungsi send dan close

```
def send(self, message):
    self.socket.sendall(encode_message(message))

def close(self):
    self.connected = False
    self.socket.close()
```

Fungsi `send` digunakan untuk mengirimkan pesan dictionary ke server dalam format JSON. Fungsi `close` digunakan untuk memutuskan koneksi secara bersih.

---

##### Ringkasan

`network_client.py` pada folder `client/` berfungsi sebagai lapisan jaringan sisi klien yang mengelola koneksi TCP, pengiriman pesan, dan penerimaan pesan secara asinkron melalui threading.

---

#### Penejelasan screens.py
(Belom)

#### Penejelasan state.py
File `state.py` pada folder `client/` berfungsi sebagai modul helper untuk inisialisasi state papan permainan.

---

##### Fungsi create_empty_board

```
def create_empty_board():
    return [[CELL_EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
```

Fungsi ini digunakan untuk menghasilkan papan kosong berukuran `BOARD_SIZE` x `BOARD_SIZE` yang dapat digunakan sebagai papan lokal maupun papan lawan di sisi klien.

---

##### Ringkasan

`state.py` pada folder `client/` berfungsi sebagai penyedia fungsi inisialisasi state papan yang digunakan oleh komponen klien lainnya.

---

### Folder Server/
#### Penejelasan auth_service.py
File `auth_service.py` pada folder `server/` berfungsi untuk menangani logika bisnis autentikasi pengguna, meliputi registrasi dan login dengan validasi serta hashing password.

---

#### Fungsi hash_password

```python
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
```

Fungsi ini digunakan untuk mengubah password plaintext menjadi hash SHA-256 sebelum disimpan ke database, sehingga password tidak tersimpan dalam bentuk teks biasa.

---

#### Fungsi register_user

```
def register_user(username, password):
    username = username.strip()

    if not username:
        return False, "Username wajib diisi"
    if len(username) < 3:
        return False, "Username minimal 3 karakter"
    if len(password) < 4:
        return False, "Password minimal 4 karakter"

    # ... cek duplikasi lalu INSERT ke database
    ensure_player(username)
    return True, "Register berhasil"
```

Fungsi ini digunakan untuk memvalidasi input registrasi, memeriksa apakah username sudah digunakan, lalu menyimpan akun baru ke tabel `users` sekaligus menginisialisasi data statistik pemain melalui `ensure_player`.

---

##### Fungsi login_user

```
def login_user(username, password):
    # ... ambil password_hash dari database
    if stored_password_hash != hash_password(password):
        return False, "Password salah"

    ensure_player(username)
    return True, "Login berhasil"
```

Fungsi ini digunakan untuk memverifikasi kredensial login dengan membandingkan hash password yang dimasukkan terhadap hash yang tersimpan di database, lalu mengembalikan status berhasil atau pesan error yang sesuai.

---

##### Ringkasan

`auth_service.py` pada folder `server/` berfungsi sebagai lapisan logika autentikasi yang mengelola registrasi dan login pengguna dengan validasi input dan keamanan penyimpanan password berbasis SHA-256.

---

#### Penejelasan client_handler.py
File `client_handler.py` pada folder `server/` berfungsi sebagai handler utama per koneksi klien yang membaca pesan masuk, memetakannya ke handler yang tepat, dan mengelola siklus hidup sesi klien.

---

##### Constructor dan Variabel Kelas

```python
class ClientHandler:
    active_usernames = {}
    active_lock = threading.Lock()

    def __init__(self, client_socket, address, logger, matchmaking):
        self.buffer = ""
        self.username = None
        self.session_id = None
        self.room_id = None
```

Variabel kelas `active_usernames` digunakan sebagai registry bersama untuk mencegah login ganda dari username yang sama, dilindungi oleh `active_lock`. Variabel instance menyimpan state sesi klien saat ini.

---

##### Fungsi handle

```
def handle(self):
    self.client_socket.settimeout(300)

    try:
        while True:
            data = self.client_socket.recv(4096)
            self.buffer += data.decode("utf-8")

            while "\n" in self.buffer:
                raw_message, self.buffer = self.buffer.split("\n", 1)
                self.process_message(raw_message)

    finally:
        if self.room_id:
            room_handler.handle_leave_room(self)
        auth_handler.unregister_active_user(self)
        self.client_socket.close()
```

Fungsi ini digunakan untuk membaca data dari socket secara terus-menerus menggunakan teknik buffering berbasis delimiter newline, memisahkan pesan-pesan yang masuk, dan memastikan klien dikeluarkan dari room serta dideregistrasi apabila koneksi terputus.

---

##### Fungsi process_message

```
def process_message(self, raw_message):
    message = decode_message(raw_message)
    message_type = message.get("type")

    if message_type == LOGIN:
        auth_handler.handle_login(self, message)
    elif message_type == MATCHMAKE:
        matchmaking_handler.handle_matchmake(self)
    elif message_type == FIRE:
        game_handler.handle_fire(self, message)
    # ... dan seterusnya untuk semua tipe pesan
```

Fungsi ini digunakan sebagai router pesan yang mendekode JSON masuk dan mendelegasikannya ke handler yang sesuai berdasarkan field `type`, sehingga logika setiap fitur terpisah dalam modul handler masing-masing.

---

##### Fungsi handle_rematch_request

```
def handle_rematch_request(self):
    room = self.matchmaking.room_manager.get_room(self.room_id)

    if room.status in ["IN_GAME", "WAITING_PLACEMENT"]:
        self.send_error("Cannot rematch before game over")
        return

    success, info = room.reset_for_rematch_request(self.session_id)
    # ... kirim notifikasi REMATCH_WAITING ke pemain
```

Fungsi ini digunakan untuk menangani permintaan rematch setelah pertandingan selesai, dengan memeriksa status room dan mereset state room agar pemain lawan dapat bergabung kembali.

---

##### Ringkasan

`client_handler.py` pada folder `server/` berfungsi sebagai handler sesi per klien yang mengelola pembacaan pesan, routing ke handler fitur, dan pembersihan sesi saat klien terputus.

---

#### Penejelasan config.py
File `config.py` pada folder `server/` berfungsi sebagai penyimpan konfigurasi jaringan sisi server.

---

##### Konfigurasi Server

```
HOST = "0.0.0.0"
PORT = 5000
BUFFER_SIZE = 4096
```

Bagian ini digunakan untuk mendefinisikan alamat binding server di semua antarmuka jaringan, port yang digunakan, serta ukuran buffer penerimaan data per paket.

---

##### Ringkasan

`config.py` pada folder `server/` berfungsi sebagai titik konfigurasi terpusat untuk parameter jaringan server.

---


#### Penejelasan database.py
File `database.py` pada folder `server/` berfungsi untuk mengelola koneksi dan inisialisasi database SQLite yang menyimpan data pengguna dan statistik pemain.

---

##### Fungsi get_connection dan init_database

```
def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            username TEXT PRIMARY KEY,
            total_match INTEGER DEFAULT 0,
            win INTEGER DEFAULT 0,
            lose INTEGER DEFAULT 0,
            hit_count INTEGER DEFAULT 0,
            miss_count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
```

Fungsi `get_connection` digunakan untuk membuka koneksi ke file database SQLite di path `data/battleship.db`, sekaligus memastikan folder `data/` telah tersedia. Fungsi `init_database` digunakan untuk membuat dua tabel yaitu `users` untuk menyimpan kredensial akun dan `players` untuk menyimpan statistik pertandingan, dengan opsi `CREATE TABLE IF NOT EXISTS` agar tidak menimpa data yang sudah ada.

---

##### Ringkasan

`database.py` pada folder `server/` berfungsi sebagai lapisan akses data yang menyediakan koneksi dan skema awal database SQLite untuk sistem autentikasi dan peringkat pemain.

---

#### Penejelasan game_room.py
File `game_room.py` pada folder `server/` berfungsi sebagai representasi satu room pertandingan yang menyimpan seluruh state permainan, termasuk papan, giliran, status, dan logika tembak-menembak.

---

##### Constructor

```
def __init__(self, room_id, player_1, player_2=None, room_name=None, password=""):
    self.room_id = room_id
    self.players = [player_1]
    self.spectators = []
    self.status = "WAITING_OPPONENT" if player_2 is None else "WAITING_PLACEMENT"
    self.boards = {player_1["session_id"]: self.create_empty_board()}
    self.shots = {player_1["session_id"]: self.create_empty_board()}
    self.ready_players = set()
    self.current_turn = None
    self.winner = None
    self.turn_number = 0
    self.ship_layouts = {}
```

Bagian ini digunakan untuk menginisialisasi room dengan data pemain, papan kosong untuk setiap pemain, serta status awal yang bergantung pada apakah pemain kedua sudah ada atau belum.

---

##### Fungsi place_ships

```
def place_ships(self, session_id, ships):
    board = self.create_empty_board()

    for ship in ships:
        cells = ship.get("cells", [])
        for cell in cells:
            if not self.is_inside_board(x, y):
                return False, "Ship cell is outside board"
            if board[y][x] == CELL_SHIP:
                return False, "Ships overlap"
        # tandai sel sebagai CELL_SHIP
    self.boards[session_id] = board
    self.ship_layouts[session_id] = ships
    return True, "Ships placed successfully"
```

Fungsi ini digunakan untuk memvalidasi dan menyimpan penempatan kapal dari seorang pemain ke papannya, dengan pengecekan batas papan dan tumpang tindih antar kapal.

---

##### Fungsi fire

```
def fire(self, shooter_session_id, x, y):
    if shooter_session_id != self.current_turn:
        return False, "Not your turn", None

    opponent_board = self.boards[opponent_session_id]

    if opponent_board[y][x] == CELL_SHIP:
        result = "HIT"
        opponent_board[y][x] = CELL_HIT
    else:
        result = "MISS"
        shooter_shots[y][x] = CELL_MISS

    if self.is_all_ships_destroyed(opponent_session_id):
        self.status = "FINISHED"
        self.winner = shooter_session_id

    self.current_turn = opponent_session_id
    self.turn_number += 1
    return True, "Fire processed", fire_data
```

Fungsi ini digunakan untuk memproses tembakan dari pemain yang sedang bergiliran, memvalidasi koordinat dan giliran, memperbarui papan lawan, serta menentukan apakah permainan berakhir apabila semua kapal lawan telah hancur.

---

#### Fungsi set_ready dan reset_for_rematch_request

```
def set_ready(self, session_id):
    self.ready_players.add(session_id)
    if len(self.ready_players) == 2:
        self.status = "IN_GAME"
        self.current_turn = self.players[0]["session_id"]
        return True
    return False

def reset_for_rematch_request(self, session_id):
    # reset papan, giliran, ready_players untuk main ulang
    self.status = "WAITING_OPPONENT"
    return True, "Waiting for rematch opponent"
```

Fungsi `set_ready` digunakan untuk menandai pemain siap bermain dan secara otomatis memulai permainan apabila kedua pemain sudah siap. Fungsi `reset_for_rematch_request` digunakan untuk mengatur ulang seluruh state room sehingga siap menerima permintaan rematch.

---

##### Ringkasan

`game_room.py` pada folder `server/` berfungsi sebagai inti logika permainan yang menyimpan dan memproses seluruh state satu sesi pertandingan battleship dari fase penempatan hingga selesai.

---

#### Penejelasan logger.py
File `logger.py` pada folder `server/` berfungsi untuk menginisialisasi sistem pencatatan log aktivitas server ke dalam file.

---

##### Fungsi setup_logger

```
def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/server.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    return logging.getLogger("battleship-server")
```

Fungsi ini digunakan untuk membuat folder `logs/` apabila belum ada, mengatur format log yang menyertakan waktu dan level, serta mengembalikan instance logger yang siap dipakai oleh komponen server lainnya.

---

##### Ringkasan

`logger.py` pada folder `server/` berfungsi sebagai penyedia logger terpusat yang mencatat seluruh aktivitas server ke file `logs/server.log`.

---

#### Penejelasan main.py
File `main.py` pada folder `server/` berfungsi sebagai titik masuk eksekusi server.

---

##### Entry Point

```
from server.socket_server import SocketServer

if __name__ == "__main__":
    server = SocketServer()
    server.start()
```

Bagian ini digunakan untuk menginisialisasi dan menjalankan server. Program dijalankan dengan perintah `python -m server.main` dari direktori root proyek.

---

##### Ringkasan

`main.py` pada folder `server/` berfungsi sebagai titik awal program yang menginisialisasi dan menjalankan `SocketServer`.

---

#### Penejelasan matchmaking.py
File `matchmaking.py` pada folder `server/` berfungsi untuk mengelola logika antrian matchmaking otomatis antar pemain yang mencari pertandingan.

---

##### Fungsi join_queue

```
def join_queue(self, player):
    waiting_room = self.room_manager.get_waiting_room()

    if waiting_room is None:
        room = self.room_manager.create_waiting_room(player)
        return room, False

    success, info = waiting_room.add_player(player)

    if not success:
        room = self.room_manager.create_waiting_room(player)
        return room, False

    return waiting_room, True
```

Fungsi ini digunakan untuk memasukkan pemain ke dalam antrian matchmaking dengan memeriksa apakah sudah ada room yang sedang menunggu lawan. Apabila ada, pemain langsung digabungkan sehingga pertandingan dimulai dan fungsi mengembalikan flag `True`. Apabila belum ada, room baru dibuat dan pemain menunggu dengan flag `False`.

---

##### Ringkasan

`matchmaking.py` pada folder `server/` berfungsi sebagai logika antrian otomatis yang mencocokkan dua pemain ke dalam satu room pertandingan secara efisien.

---

#### Penejelasan ranking_service.py
File `ranking_service.py` pada folder `server/` berfungsi untuk mengelola data statistik pertandingan pemain, mencakup pencatatan hasil pertandingan, akurasi tembakan, dan pengambilan data leaderboard.

---

##### Fungsi ensure_player

```python
def ensure_player(username):
    cursor.execute("""
        INSERT OR IGNORE INTO players (username)
        VALUES (?)
    """, (username,))
```

Fungsi ini digunakan untuk memastikan data pemain sudah ada di tabel `players`, dan apabila belum ada maka akan dibuat secara otomatis dengan nilai statistik awal nol.

---

##### Fungsi record_match_result

```
def record_match_result(winner_username, loser_username):
    # UPDATE players SET total_match+1, win+1 WHERE username = winner
    # UPDATE players SET total_match+1, lose+1 WHERE username = loser
```

Fungsi ini digunakan untuk mencatat hasil akhir pertandingan dengan menambahkan satu pada kolom `win` pemenang dan kolom `lose` pada yang kalah, serta menambah jumlah total pertandingan keduanya.

---

##### Fungsi record_shot

```
def record_shot(username, result):
    if result == "HIT":
        # UPDATE hit_count + 1
    elif result == "MISS":
        # UPDATE miss_count + 1
```

Fungsi ini digunakan untuk mencatat setiap tembakan yang dilakukan pemain sehingga akurasi dapat dihitung dari rasio `hit_count` terhadap total tembakan.

---

##### Fungsi get_leaderboard

```
def get_leaderboard(limit=10):
    cursor.execute("""
        SELECT username, total_match, win, lose, hit_count, miss_count
        FROM players
        ORDER BY win DESC, hit_count DESC, total_match DESC
        LIMIT ?
    """, (limit,))
```

Fungsi ini digunakan untuk mengambil daftar pemain teratas dari database dan diurutkan berdasarkan jumlah kemenangan, jumlah hit, dan total pertandingan, kemudian menghitung `win_rate` dalam persen sebelum dikembalikan sebagai list dictionary.

---

##### Ringkasan

`ranking_service.py` pada folder `server/` berfungsi sebagai lapisan pengelolaan statistik pemain yang mencatat hasil pertandingan dan akurasi tembakan serta menyediakan data leaderboard yang terurut.

---

#### Penejelasan replay_service.py
File `replay_service.py` pada folder `server/` berfungsi untuk mengelola pencatatan dan pengambilan data replay pertandingan dalam format JSON.

---

##### Fungsi create_replay

```
def create_replay(room_id, player_1, player_2):
    replay = {
        "room_id": room_id,
        "player_1": player_1,
        "player_2": player_2,
        "started_at": datetime.now().isoformat(),
        "finished_at": None,
        "winner": None,
        "player_1_ships": [],
        "player_2_ships": [],
        "events": []
    }
    save_replay(room_id, replay)
    return replay
```

Fungsi ini digunakan untuk membuat objek replay baru saat pertandingan dimulai, berisi metadata pertandingan dan daftar event yang masih kosong, lalu menyimpannya sebagai file JSON dengan nama sesuai `room_id`.

---

##### Fungsi add_fire_event dan add_forfeit_event

```
def add_fire_event(room_id, shooter, x, y, result, turn_number):
    replay["events"].append({
        "turn": turn_number,
        "shooter": shooter,
        "action": "FIRE",
        "x": x, "y": y, "result": result,
        "timestamp": datetime.now().isoformat()
    })

def add_forfeit_event(room_id, loser, winner):
    replay["events"].append({
        "action": "FORFEIT",
        "result": "FORFEIT",
        "winner": winner, ...
    })
```

Fungsi `add_fire_event` digunakan untuk mencatat setiap tembakan beserta koordinat, hasil, dan nomor giliran ke dalam daftar event replay. Fungsi `add_forfeit_event` digunakan untuk mencatat kejadian menyerah sebagai event akhir pertandingan.

---

##### Fungsi finish_replay dan get_replay_list

```
def finish_replay(room_id, winner):
    replay["winner"] = winner
    replay["finished_at"] = datetime.now().isoformat()
    save_replay(room_id, replay)

def get_replay_list():
    # membaca semua file .json di folder replays/
    # mengembalikan ringkasan tiap pertandingan
```

Fungsi `finish_replay` digunakan untuk mengunci replay dengan mencatat pemenang dan waktu selesai pertandingan. Fungsi `get_replay_list` digunakan untuk membaca semua file replay yang ada dan mengembalikannya sebagai daftar ringkasan yang diurutkan dari yang terbaru.

---

##### Ringkasan

`replay_service.py` pada folder `server/` berfungsi sebagai sistem pencatatan pertandingan berbasis file JSON yang merekam setiap aksi dalam permainan sehingga pertandingan dapat diputar ulang di kemudian hari.

---

#### Penejelasan response_builder.py
File `response_builder.py` pada folder `server/` berfungsi sebagai factory function untuk membangun struktur pesan respons yang konsisten sebelum dikirimkan ke klien.

---

##### Fungsi ok, failed, dan error

```
def ok(message_type, payload=None, room_id=None, session_id=None):
    return {
        "type": message_type,
        "status": "OK",
        "payload": payload or {}
    }

def failed(message_type, message, room_id=None):
    return {
        "type": message_type,
        "status": "ERROR",
        "payload": {"message": message}
    }

def error(message):
    return {
        "type": "ERROR",
        "status": "ERROR",
        "payload": {"message": message}
    }
```

Fungsi `ok` digunakan untuk membangun respons sukses dengan tipe pesan dan payload yang diberikan. Fungsi `failed` digunakan untuk membangun respons error yang mempertahankan tipe pesan aslinya sehingga klien dapat mengetahui operasi mana yang gagal. Fungsi `error` digunakan untuk respons error umum tanpa konteks tipe pesan spesifik.

---

##### Fungsi room_payload

```
def room_payload(message_type, room, message="", room_id=None):
    return ok(
        message_type,
        room_id=room_id or room.room_id,
        payload={
            "room": room.get_public_info(),
            "message": message
        }
    )
```

Fungsi ini digunakan sebagai shortcut untuk membangun respons yang menyertakan informasi publik sebuah room, dipakai secara konsisten di berbagai handler yang berkaitan dengan room.

---

##### Ringkasan

`response_builder.py` pada folder `server/` berfungsi sebagai pembangun struktur respons terpusat yang memastikan format pesan dari server selalu konsisten kepada semua klien.

---

#### Penejelasan room_manager.py
File `room_manager.py` pada folder `server/` berfungsi untuk mengelola seluruh siklus hidup room permainan, mulai dari pembuatan, pencarian, penggabungan pemain, hingga penghapusan room.

---

##### Fungsi create_waiting_room dan create_manual_room

```
def create_waiting_room(self, player_1):
    room_id = str(uuid.uuid4())[:8]
    room = GameRoom(room_id=room_id, player_1=player_1, ...)
    self.rooms[room_id] = room
    return room

def create_manual_room(self, player_1, room_name, password=""):
    # sama seperti create_waiting_room, dengan nama dan password custom
```

Fungsi `create_waiting_room` digunakan untuk membuat room baru dengan ID acak 8 karakter untuk antrian matchmaking otomatis. Fungsi `create_manual_room` digunakan untuk membuat room dengan nama dan password kustom yang dapat diakses pemain lain melalui daftar room.

---

##### Fungsi join_room_as_player dan join_room_as_spectator

```
def join_room_as_player(self, room_id, player, password=""):
    room = self.get_room(room_id)
    if not room.is_password_valid(password):
        return False, "Wrong room password", None
    success, info = room.add_player(player)
    return True, info, room

def join_room_as_spectator(self, room_id, spectator, password=""):
    room.add_spectator(spectator)
    return True, "Joined as spectator", room
```

Fungsi `join_room_as_player` digunakan untuk memproses permintaan bergabung sebagai pemain dengan memvalidasi password dan kapasitas room. Fungsi `join_room_as_spectator` digunakan untuk menambahkan pengguna sebagai penonton tanpa batasan jumlah.

---

##### Fungsi get_room_list dan remove_user_from_room

```
def get_room_list(self):
    return [
        room.get_public_info()
        for room in self.rooms.values()
        if room.status in ["WAITING_OPPONENT", "WAITING_PLACEMENT", "IN_GAME"]
        and len(room.players) > 0
    ]

def remove_user_from_room(self, room_id, session_id):
    room.remove_user(session_id)
    if room.status == "EMPTY" or (len(room.players) == 0 ...):
        del self.rooms[room_id]
        return None
    return room
```

Fungsi `get_room_list` digunakan untuk mengambil daftar room aktif yang dapat ditampilkan kepada pemain di browser room. Fungsi `remove_user_from_room` digunakan untuk mengeluarkan pengguna dari room dan secara otomatis menghapus room apabila sudah tidak ada pemain tersisa.

---

##### Ringkasan

`room_manager.py` pada folder `server/` berfungsi sebagai manajer terpusat seluruh room yang aktif, mengelola pembuatan, pencarian, penggabungan pemain, dan pembersihan room secara otomatis.

---

#### Penejelasan socket_server.py
File `socket_server.py` pada folder `server/` berfungsi sebagai titik masuk utama server yang menerima koneksi klien masuk dan mendelegasikannya ke handler masing-masing.

---

##### Constructor

```
def __init__(self):
    init_database()
    self.logger = setup_logger()
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.room_manager = RoomManager()
    self.matchmaking = Matchmaking(self.room_manager)
```

Bagian ini digunakan untuk menginisialisasi database, logger, socket server, serta objek `RoomManager` dan `Matchmaking` yang akan digunakan bersama oleh semua handler klien.

---

##### Fungsi start

```
def start(self):
    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind((HOST, PORT))
    self.server_socket.listen()

    while True:
        client_socket, address = self.server_socket.accept()

        handler = ClientHandler(
            client_socket=client_socket,
            address=address,
            logger=self.logger,
            matchmaking=self.matchmaking
        )

        thread = threading.Thread(target=handler.handle, daemon=True)
        thread.start()
```

Fungsi ini digunakan untuk menjalankan loop penerimaan koneksi klien secara terus-menerus, di mana setiap koneksi yang masuk akan dibuatkan objek `ClientHandler` baru dan dijalankan dalam thread daemon tersendiri agar server dapat melayani banyak klien secara bersamaan.

---

##### Ringkasan

`socket_server.py` pada folder `server/` berfungsi sebagai titik masuk server berbasis TCP yang menerima koneksi klien dan mendistribusikannya ke handler individual melalui threading.

---


### Folder server/handlers
##### Penjelasan auth_handler.py
File `auth_handler.py` pada folder `server/handlers/` berfungsi untuk menangani permintaan autentikasi klien yaitu login dan registrasi, termasuk pengelolaan sesi aktif.

---

##### Fungsi handle_login

```
def handle_login(handler, message):
    username = message.get("payload", {}).get("username", "").strip()
    password = message.get("payload", {}).get("password", "")

    success, info = login_user(username, password)

    with handler.__class__.active_lock:
        if username already active and not same handler:
            handler.send(failed(LOGIN_FAILED, "Username sedang online"))
            return

        handler.username = username
        handler.session_id = str(uuid.uuid4())
        handler.__class__.active_usernames[handler.username] = handler

    handler.send(ok(LOGIN_SUCCESS, session_id=handler.session_id, ...))
```

Fungsi ini digunakan untuk memproses login dengan memanggil `login_user` dari `auth_service`, mencegah login ganda pada username yang sama menggunakan lock thread, dan menetapkan `session_id` unik berbasis UUID untuk sesi klien yang berhasil login.

---

##### Fungsi handle_register dan unregister_active_user

```
def handle_register(handler, message):
    success, info = register_user(username, password)
    handler.send(ok(REGISTER_SUCCESS, ...))

def unregister_active_user(handler):
    with handler.__class__.active_lock:
        if active_handler is handler:
            del handler.__class__.active_usernames[handler.username]
```

Fungsi `handle_register` digunakan untuk memproses permintaan registrasi akun baru dan mengirimkan respons berhasil atau gagal. Fungsi `unregister_active_user` digunakan untuk menghapus entri username dari registry sesi aktif saat klien terputus.

---

##### Ringkasan

`auth_handler.py` pada folder `server/handlers/` berfungsi sebagai handler autentikasi yang memproses login dan registrasi klien serta mengelola daftar sesi aktif untuk mencegah duplikasi akun yang sedang online.

---

#### Penjelasan game_handler.py
File `game_handler.py` pada folder `server/handlers/` berfungsi untuk menangani aksi-aksi inti selama pertandingan berlangsung, yaitu tembakan dan menyerah.

---

##### Fungsi handle_fire

```
def handle_fire(handler, message):
    x, y = payload.get("x"), payload.get("y")
    success, info, fire_data = room.fire(handler.session_id, x, y)

    record_shot(handler.username, fire_data["result"])
    add_fire_event(room_id, shooter, x, y, result, turn_number)

    handler.send({"type": FIRE_RESULT, "payload": fire_data})
    opponent_handler.send({"type": OPPONENT_FIRE_RESULT, "payload": fire_data})

    if fire_data["winner_session_id"]:
        record_match_result(winner, loser)
        finish_replay(room_id, winner)
        # kirim GAME_OVER ke semua pemain
    else:
        # kirim TURN_UPDATE ke semua pemain
```

Fungsi ini digunakan untuk memproses tembakan pemain dengan memvalidasinya melalui `GameRoom.fire`, mencatat statistik tembakan dan event replay, lalu mendistribusikan hasil tembakan ke penembak, lawan, dan penonton. Apabila ada pemenang, pencatatan hasil pertandingan dan pengiriman `GAME_OVER` dilakukan secara otomatis.

---

##### Fungsi handle_forfeit

```
def handle_forfeit(handler):
    winner_player = opponent
    loser_player = get_current_player_data(handler, room)

    room.status = "FINISHED"
    record_match_result(winner, loser)
    add_forfeit_event(room_id, loser, winner)
    finish_replay(room_id, winner)

    for player in room.players:
        player_handler.send({"type": GAME_OVER, ...})
```

Fungsi ini digunakan untuk menangani kejadian menyerah oleh seorang pemain, secara otomatis menetapkan lawan sebagai pemenang, mencatat hasil ke database dan replay, lalu mengirimkan notifikasi `GAME_OVER` ke semua pihak.

---

##### Ringkasan

`game_handler.py` pada folder `server/handlers/` berfungsi sebagai handler inti pertandingan yang memproses tembakan dan menyerah sambil mengintegrasikan pencatatan statistik, replay, dan distribusi notifikasi ke semua pemain dan penonton.

---

#### Penjelasan leaderboard_handler.py
File `leaderboard_handler.py` pada folder `server/handlers/` berfungsi untuk menangani permintaan pengambilan data leaderboard dari klien.

---

##### Fungsi handle_get_leaderboard

```
def handle_get_leaderboard(handler):
    leaderboard = get_leaderboard()

    handler.send(ok(
        LEADERBOARD_DATA,
        payload={"leaderboard": leaderboard}
    ))
```

Fungsi ini digunakan untuk mengambil data peringkat pemain dari `ranking_service` dan mengirimkannya langsung ke klien yang meminta, tanpa memerlukan autentikasi karena leaderboard bersifat publik.

---

##### Ringkasan

`leaderboard_handler.py` pada folder `server/handlers/` berfungsi sebagai handler pengambilan data peringkat yang meneruskan permintaan leaderboard dari klien ke layanan ranking dan mengembalikan hasilnya.

#### Penjelasan matchmaking_handler.py
File `matchmaking_handler.py` pada folder `server/handlers/` berfungsi untuk menangani permintaan matchmaking otomatis antar pemain yang mencari pertandingan tanpa membuat room manual.

---

##### Fungsi handle_matchmake

```
def handle_matchmake(handler):
    if not handler.session_id:
        handler.send_error("You must login first")
        return

    player = {
        "username": handler.username,
        "session_id": handler.session_id,
        "handler": handler
    }

    room, is_matched = handler.matchmaking.join_queue(player)
    handler.room_id = room.room_id

    if not is_matched:
        handler.send({"type": ROOM_WAITING_CREATED, ...})
        return

    for index, player_data in enumerate(players):
        player_handler.send({
            "type": MATCH_FOUND,
            "payload": {
                "player_index": index + 1,
                "opponent_username": opponent["username"],
            }
        })

    create_replay(room_id=room_id, ...)
```

Fungsi ini digunakan untuk memasukkan pemain ke antrian matchmaking dan menangani dua skenario: apabila belum ada lawan maka pemain menunggu dengan respons `ROOM_WAITING_CREATED`, dan apabila lawan ditemukan maka kedua pemain diberitahu melalui `MATCH_FOUND` beserta data lawan dan indeks pemain masing-masing, serta replay pertandingan dibuat secara otomatis.

---

##### Ringkasan

`matchmaking_handler.py` pada folder `server/handlers/` berfungsi sebagai handler antrian matchmaking yang mencocokkan dua pemain secara otomatis dan menginisialisasi sesi pertandingan baru.

---
#### Penjelasan placement_handler.py
File `placement_handler.py` pada folder `server/handlers/` berfungsi untuk menangani fase penempatan kapal sebelum permainan dimulai, mulai dari sinyal mulai penempatan hingga konfirmasi siap bermain.

---

##### Fungsi handle_start_placement

```
def handle_start_placement(handler):
    room.status = "WAITING_PLACEMENT"
    send_placement_start_to_room(handler, room)
```

Fungsi ini digunakan untuk memulai fase penempatan kapal dengan mengubah status room dan mengirimkan sinyal `PLACEMENT_START` ke semua pemain dan penonton di room tersebut beserta informasi lawan masing-masing.

---

##### Fungsi handle_place_ships

```
def handle_place_ships(handler, message):
    ships = message.get("payload", {}).get("ships", [])
    success, info = room.place_ships(handler.session_id, ships)

    handler.send({"type": PLACE_SHIPS_SUCCESS, ...})
```

Fungsi ini digunakan untuk menerima data penempatan kapal dari klien, meneruskannya ke logika validasi di `GameRoom`, lalu memberikan konfirmasi berhasil atau pesan error kepada pemain.

---

##### Fungsi handle_ready

```
def handle_ready(handler, message):
    game_started = room.set_ready(handler.session_id)

    if not game_started:
        handler.send({"type": WAITING_OPPONENT_READY, ...})
        return

    for player in room.players:
        player["handler"].send({"type": GAME_START, "payload": {"first_turn_session_id": room.current_turn}})

    save_ship_layouts(...)
    # kirim SPECTATOR_UPDATE ke penonton
```

Fungsi ini digunakan untuk menandai pemain sebagai siap dan apabila kedua pemain sudah siap maka permainan dimulai, sinyal `GAME_START` dikirim ke semua pemain beserta informasi giliran pertama, layout kapal disimpan ke replay, dan penonton mendapatkan pembaruan state awal.

---

##### Ringkasan

`placement_handler.py` pada folder `server/handlers/` berfungsi sebagai handler fase penempatan kapal yang mengkoordinasikan transisi dari persiapan ke permainan setelah kedua pemain menyerahkan posisi kapal dan menyatakan siap.

---

#### Penjelasan replay_handler.py
File `replay_handler.py` pada folder `server/handlers/` berfungsi untuk menangani permintaan pengambilan data replay pertandingan dari klien.

---

##### Fungsi handle_get_replay_list dan handle_get_replay_detail

```
def handle_get_replay_list(handler):
    handler.send(ok(
        REPLAY_LIST_DATA,
        payload={"replays": get_replay_list()}
    ))

def handle_get_replay_detail(handler, message):
    room_id = message.get("payload", {}).get("room_id")
    replay = get_replay(room_id)

    handler.send(ok(
        REPLAY_DETAIL_DATA,
        payload={"replay": replay}
    ))
```

Fungsi `handle_get_replay_list` digunakan untuk mengirimkan daftar ringkasan semua replay yang tersimpan kepada klien. Fungsi `handle_get_replay_detail` digunakan untuk mengambil dan mengirimkan data replay lengkap berdasarkan `room_id` yang diminta, termasuk semua event tembakan untuk keperluan pemutaran ulang di klien.

---

##### Ringkasan

`replay_handler.py` pada folder `server/handlers/` berfungsi sebagai handler pengambilan data replay yang menyediakan akses ke riwayat pertandingan baik dalam bentuk daftar maupun detail lengkap.

---

#### Penjelasan room_handler.py
File `room_handler.py` pada folder `server/handlers/` berfungsi untuk menangani seluruh operasi pengelolaan room secara manual, meliputi pembuatan, pencarian daftar, bergabung sebagai pemain atau penonton, dan meninggalkan room.

---

##### Fungsi handle_create_room

```
def handle_create_room(handler, message):
    room_name = payload.get("room_name", "").strip()
    password = payload.get("password", "")

    room = handler.matchmaking.room_manager.create_manual_room(
        player_1=player, room_name=room_name, password=password
    )

    handler.room_id = room.room_id
    handler.send(room_payload(CREATE_ROOM_SUCCESS, room, ...))
```

Fungsi ini digunakan untuk membuat room manual dengan nama dan password opsional, lalu mengirimkan konfirmasi beserta informasi publik room kepada pembuatnya.

---

##### Fungsi handle_join_room

```
def handle_join_room(handler, message):
    mode = payload.get("mode", "PLAYER")

    if mode == "SPECTATOR":
        success, info, room = join_room_as_spectator(...)
        handler.send(ok(SPECTATOR_JOINED, payload=build_spectator_payload(room)))
        return

    success, info, room = join_room_as_player(...)

    if len(room.players) == 2:
        notify_match_found(handler, room)
    else:
        handler.send(room_payload(JOIN_ROOM_SUCCESS, room, ...))
```

Fungsi ini digunakan untuk menangani permintaan bergabung ke room berdasarkan mode yang diminta. Apabila mode `SPECTATOR`, klien bergabung sebagai penonton dan menerima snapshot state permainan saat ini. Apabila sebagai pemain dan room sudah penuh dua orang, pertandingan langsung dimulai melalui `notify_match_found`.

---

##### Fungsi notify_room_updated dan handle_leave_room

```
def notify_room_updated(handler, room):
    for player in room.players:
        player["handler"].send({"type": ROOM_UPDATED, ...})
    for spectator in room.spectators:
        spectator["handler"].send({"type": ROOM_UPDATED, ...})

def handle_leave_room(handler):
    room = room_manager.remove_user_from_room(old_room_id, handler.session_id)
    if room:
        notify_room_updated(handler, room)
```

Fungsi `notify_room_updated` digunakan untuk menyiarkan pembaruan informasi room ke semua pemain dan penonton yang ada di dalamnya. Fungsi `handle_leave_room` digunakan untuk mengeluarkan pemain dari room dan memberitahu pengguna lain yang tersisa.

---

##### Ringkasan

`room_handler.py` pada folder `server/handlers/` berfungsi sebagai handler pengelolaan room yang menangani pembuatan, penggabungan, dan keluarnya pengguna dari room baik sebagai pemain maupun penonton.

---


### Folder shared/
#### Penjelasan constants.py
File `constants.py` pada folder `shared/` berfungsi sebagai tempat penyimpanan konstanta global yang digunakan bersama oleh server dan klien, mencakup konfigurasi jaringan, ukuran papan, dan data kapal.

---

##### Konfigurasi Jaringan dan Papan

```
HOST = "127.0.0.1"
PORT = 5000

BOARD_SIZE = 10

CELL_EMPTY = 0
CELL_SHIP = 1
CELL_HIT = 2
CELL_MISS = 3
```

Bagian ini digunakan untuk mendefinisikan alamat dan port koneksi klien ke server, ukuran papan permainan sebesar 10x10, serta nilai numerik yang merepresentasikan status setiap sel pada papan yaitu kosong, berisi kapal, kena tembak, atau meleset.

---

##### Konfigurasi Data Kapal

```
SHIPS = [
    {"name": "Wooden Boat", "width": 1, "height": 2, ...},
    {"name": "Pirate Boat", "width": 2, "height": 2, ...},
    {"name": "Battle Ship", "width": 2, "height": 4, ...},
    {"name": "Steel Ship",  "width": 1, "height": 3, ...},
    {"name": "Cyber Ship",  "width": 1, "height": 3, ...},
]
```

Bagian ini digunakan untuk mendefinisikan daftar kapal yang tersedia dalam permainan beserta dimensi dan path gambarnya, sehingga dapat digunakan oleh klien saat fase penempatan kapal maupun pemuatan aset visual.

---

##### Ringkasan

`constants.py` pada folder `shared/` berfungsi sebagai sumber kebenaran tunggal untuk konfigurasi dan konstanta permainan yang dipakai bersama antara server dan klien.

---

#### Penjelasan message_type.py
File `message_type.py` pada folder `shared/` berfungsi sebagai kamus tipe pesan yang mendefinisikan seluruh string konstan yang digunakan dalam komunikasi antara klien dan server.

---

##### Definisi Tipe Pesan

```
LOGIN = "LOGIN"
LOGIN_SUCCESS = "LOGIN_SUCCESS"
LOGIN_FAILED = "LOGIN_FAILED"

MATCHMAKE = "MATCHMAKE"
MATCH_FOUND = "MATCH_FOUND"

FIRE = "FIRE"
FIRE_RESULT = "FIRE_RESULT"
OPPONENT_FIRE_RESULT = "OPPONENT_FIRE_RESULT"
GAME_OVER = "GAME_OVER"

# ... dan seterusnya
```

Bagian ini digunakan untuk mendefinisikan semua tipe pesan yang mungkin dikirimkan atau diterima dalam sesi permainan, mencakup alur autentikasi, matchmaking, pengelolaan room, penempatan kapal, permainan, hingga fitur replay dan leaderboard, sehingga server dan klien memiliki referensi tipe pesan yang konsisten.

---

##### Ringkasan

`message_type.py` pada folder `shared/` berfungsi sebagai protokol komunikasi terpusat yang memastikan konsistensi tipe pesan antara server dan klien di seluruh siklus permainan.

---

#### Penjelasan serializer.py
File `serializer.py` pada folder `shared/` berfungsi sebagai modul encoder dan decoder pesan JSON yang digunakan oleh server maupun klien untuk mengirim dan menerima data melalui socket TCP.

---

##### Fungsi encode_message dan decode_message

```
def encode_message(message: dict) -> bytes:
    return (json.dumps(message) + "\n").encode("utf-8")

def decode_message(raw_message: str) -> dict:
    return json.loads(raw_message)
```

Fungsi `encode_message` digunakan untuk mengubah dictionary Python menjadi bytes JSON yang diakhiri karakter newline (`\n`) sebagai delimiter, sehingga penerima dapat mengetahui batas akhir satu pesan. Fungsi `decode_message` digunakan untuk mengurai string JSON yang diterima menjadi dictionary Python kembali.

---

##### Ringkasan

`serializer.py` pada folder `shared/` berfungsi sebagai lapisan protokol framing yang memungkinkan pengiriman dan penerimaan pesan berbasis JSON secara andal melalui koneksi TCP streaming.

---


## Screenshot Hasil
