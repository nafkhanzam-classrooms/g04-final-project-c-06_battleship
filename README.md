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
  * [Penejelasan message_handler.py](#penejelasan-message_handlerpy) belom
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
  * [Penjelasan **init**.py](#penjelasan-__init__py)

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
(belum)

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
(Belom)

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

#### Penejelasan client_handler.py

#### Penejelasan config.py

#### Penejelasan database.py

#### Penejelasan game_room.py

#### Penejelasan logger.py

#### Penejelasan main.py

#### Penejelasan matchmaking.py

#### Penejelasan ranking_service.py

#### Penejelasan replay_service.py

#### Penejelasan response_builder.py

#### Penejelasan room_manager.py

#### Penejelasan socket_server.py


### Folder server/handlers
#### Penjelasan auth_handler.py

#### Penjelasan game_handler.py

#### Penjelasan leaderboard_handler.py

#### Penjelasan matchmaking_handler.py

#### Penjelasan placement_handler.py

#### Penjelasan replay_handler.py

#### Penjelasan room_handler.py

#### Penjelasan __init__.py

### Folder shared/
#### Penjelasan constants.py

#### Penjelasan message_type.py

#### Penjelasan serializer.py




## Screenshot Hasil
