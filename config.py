# config.py

# Окно и рендер
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
RENDER_SCALE = SCREEN_WIDTH / DISPLAY_WIDTH  # обычно 2.0

# Тайловая сетка
TILE_SIZE = 16

# Шрифты
FONT_PATH = "data/fonts/PublicPixel-rv0pA.ttf"
FONT_SIZE = 8

# Таймер и FPS
FPS = 60
INITIAL_TIMER = 15*60
TIMER_CYCLE = 61
FPS_TEXT_POS = (2, 2)

# Физика
GRAVITY = 0.1

# Механики игрока
MAX_STAMINA = 360
STAMINA_BAR_WIDTH = 100
STAMINA_BAR_HEIGHT = 10
STAMINA_BAR_POS = (15, 10)
TIMER_TEXT_POS = (15, 35)
TIMER_TEXT_WIDTH = 150

DASH_SPEED = 8          # скорость во время даш-движения
DASH_POWER = 10         # начальная сила даш
DASH_STAMINA_COST = 360

JUMP_VELOCITY = -3
WALL_JUMP_VELOCITY_X = 2
WALL_JUMP_STAMINA_COST = 60
WALL_GRAB_THRESHOLD = 4  # air_time > 4

ANIM_OFFSET = (-3, -3)   # смещение спрайта при рендере

# Цвета
COLOR_BG = (10, 12, 25)
COLOR_TEXT_PRIMARY = (255, 142, 128)
COLOR_TEXT_SECONDARY = (74, 36, 128)
COLOR_STAMINA_FILL = (197, 58, 157)
COLOR_STAMINA_BORDER = (74, 36, 128)

COLOR_UI_TEXT    = (200, 200, 180)  # бежево-серый
COLOR_STAMINA_BG = (30,  30, 50)    # чуть светлее фона
COLOR_STAMINA_FILL = (220, 160, 40) # янтарный
COLOR_STAMINA_BORDER = (100, 60, 30)

COLOR_TIMER_TEXT = (100, 200, 220)  # холодный циан

COLOR_MESSAGEBOX_BG     = COLOR_BG           # фон сообщения
COLOR_MESSAGEBOX_BORDER = COLOR_TEXT_PRIMARY # рамка и текст

# Textbox
TEXTBOX_DEFAULT_HEIGHT = 30
TEXTBOX_DEFAULT_WIDTH = 100
TEXTBOX_PADDING = 10

# Messagebox
MESSAGEBOX_SIZE = (300, 220)
MESSAGEBOX_CHAR_WIDTH = 8
MESSAGEBOX_LINE_WRAP = 270
MESSAGEBOX_LINE_HEIGHT = 12

# Tilemap
NEIGHBOURS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0),
              (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {"surface", "Jumper"}

# Редактор
EDITOR_RENDER_SCALE = 2.0
SCROLL_SPEED = 5

GAZE_RECT_SIZE = (20, 20)        # размер зоны взгляда
GAZE_DEBUG_COLOR = (200, 200, 200)


FIRST_MAP_CAMERA_Y = -250   # пример: сместить камеру на 50 пикселей вверх
LEVEL2_CAMERA_SWITCH_X = 540