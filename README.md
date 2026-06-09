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
- [Struktur Directory](#struktur-directory)
  
- [Folder client/](#folder-client)
  
    - [Penjelasan app.py]()
    - [Penjelasan assets.py]()
    - [Penejelasan audio.py]()
    - [Penejelasan event_handler.py]()
    - [Penejelasan game_logic.py]()
    - [Penejelasan main.py]()
    - [Penejelasan message_handler.py]()
    - [Penejelasan network_client.py]()
    - [Penejelasan screens.py]()
    - [Penejelasan state.py]()
      
- [Folder Server/]()

    - [Penejelasan auth_service.py]()
    - [Penejelasan client_handler.py]()
    - [Penejelasan config.py]()
    - [Penejelasan database.py]()
    - [Penejelasan game_room.py]()
    - [Penejelasan logger.py]()
    - [Penejelasan main.py]()
    - [Penejelasan matchmaking.py]()
    - [Penejelasan ranking_service.py]()
    - [Penejelasan replay_service.py]()
    - [Penejelasan response_builder.py]()
    - [Penejelasan room_manager.py]()
    - [Penejelasan socket_server.py]()
    
- Folder server/handlers

    - Penjelasan auth_handler.py
    - Penjelasan game_handler.py
    - Penjelasan leaderboard_handler.py
    - Penjelasan matchmaking_handler.py
    - Penjelasan placement_handler.py
    - Penjelasan replay_handler.py
    - Penjelasan room_handler.py
    - Penjelasan __init__.py
    
- Folder shared/

    - Penjelasan constants.py
    - Penjelasan message_type.py
    - Penjelasan serializer.py
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

#### Penejelasan event_handler.py

#### Penejelasan game_logic.py

#### Penejelasan main.py

#### Penejelasan message_handler.py

#### Penejelasan network_client.py

#### Penejelasan screens.py

#### Penejelasan state.py


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
