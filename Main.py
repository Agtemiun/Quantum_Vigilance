import Scripts.entity as Entity
import Scripts.tilemap as TMap
import sys
import config

from Scripts.utils import Animation, Textbox, image_load, images_load, Textbox, Messagebox
import pygame
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Quantum Vigilance")
        self.game_font = pygame.font.Font(config.FONT_PATH , config.FONT_SIZE)
        self.Screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.display = pygame.Surface((config.DISPLAY_WIDTH , config.DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.timer = config.INITIAL_TIMER;
        self.time=0;
        self.camera_shift = [0,0]
        self.assets = {
            'decor': images_load('tiles/decor'),
            'surface': images_load('tiles/surface'),
            'glass': images_load('tiles/glass'),
            'large_decor': images_load('tiles/large_decor'),
            'player':image_load('entities/player.png'),
            'Jumper': images_load('functional_blocks/jumper'),
            'Exit': images_load('functional_blocks/Exit'),
            'player/idle':Animation(images_load("entities/player/idle"),duration=6),
            'player/run':Animation(images_load("entities/player/run"),duration=4),
            'player/jump':Animation(images_load("entities/player/jump"),duration=7)
        }
        self.movement = [0, 0]
        self.tilemap = TMap.Tilemap(self, config.TILE_SIZE)
        self.player = Entity.Player(self,self.tilemap.player_pos,(self.assets['player'].get_width(),self.assets['player'].get_height()))
        self.tilemap.load("data/Maps/map1.json")
        # self.tilemap.camera_info = 'only_x'
        self.next_level= False
        self.player.pos = self.tilemap.player_pos
        self.level = 1;
        self.display.blit(image_load("background.png"),(-50,-30))
    
    def load_next_level(self):
        
        for i in range(0,1800):
            self.Screen.fill(config.COLOR_BG,(320-i,240-i,i,i))
            pygame.display.update()

        self.level+=1
        try:
            self.tilemap.load("data/Maps/map"+str(self.level)+".json")
            self.player.pos = self.tilemap.player_pos
            trans_text = f"[DEBUG] Vertical movement is activated."
            Messagebox(trans_text, (20, 20)).render(self)
            
        except:
            EndMassage = Messagebox("[DEBUG] EOF",(20,20))
            EndMassage.render(self)
        self.next_level =False
    
    def reload(self):
        Deathbox = Textbox((180,240),"[DEBUG] Fatal error",32,120,280)
        self.player.pos = self.tilemap.player_pos
        for i in range(0,1800):
            self.Screen.fill(config.COLOR_BG,(320-i,200-i,i,i))
            Deathbox.render(self.Screen,0)

            pygame.display.update()
            
        self.player.is_death = False
        self.tilemap.load("data/Maps/map"+str(self.level)+".json")
        


    def menu(self):
        menu_pos = 0
        self.display.blit(self.game_font.render("Quantum Vigilance",False,config.COLOR_TEXT_PRIMARY),(10,10))
        start_button = Textbox((20,70),"Start")
        # level_button = Textbox((20,110),"Level_editor")
        exit_button = Textbox((20,150),"Exit")
        while True:
            menu_pos = menu_pos % 2
            menu_elements = ["Start","Exit"]
            start_button.render(self.display,False)
            # level_button.render(self.display,False)
            exit_button.render(self.display,False)
            match menu_pos:
                case 0:
                    start_button.render(self.display, True)
                # case 1:
                #    level_button.render(self.display,True)
                case 1:
                    exit_button .render(self.display, True)

            for event in pygame.event.get():
                match event.type:
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_DOWN:
                                menu_pos+=1
                            case pygame.K_UP:
                                menu_pos-=1
                            case pygame.K_SPACE:
                                match menu_elements[menu_pos]:
                                    case "Start":
                                        self.run()
                                    case "Exit":
                                        pygame.quit()
                                        sys.exit()
            self.Screen.blit(pygame.transform.scale(self.display,self.Screen.get_size()),(0,0))
            pygame.display.update()
    
    def hud(self):
        if self.timer == 0:
            EndMessage = Messagebox("You fail mission and spaceship was completly breoken!!!",(20,20))
            self.player.is_death = True
            self.level = 1
            self.timer = config.INITIAL_TIMER
            EndMessage.render()
        self.time= (self.time+1)%config.TIMER_CYCLE 
        self.timer-=self.time//60
        # новый таймер — в минутах, справа сверху
        minutes = self.timer // 60
        timer_str = f"Battery: {minutes} cells"
        txt_surf = self.game_font.render(timer_str, False, (100, 200, 220))
        # позиция — правый верхний угол с отступом 10px
        tx = config.DISPLAY_WIDTH - txt_surf.get_width() - 10
        ty = 10
        self.display.blit(txt_surf, (tx, ty))
        
        # Стамина: отрисовка заполнения
        # Рисуем единый индикатор: фон + заливка по проценту
        x0, y0 = config.STAMINA_BAR_POS
        W, H  = config.STAMINA_BAR_WIDTH, config.STAMINA_BAR_HEIGHT
        pct   = max(0, min(1, self.player.stamina / config.MAX_STAMINA))
        # фон
        pygame.draw.rect(self.display, (30, 30, 50), (x0, y0, W, H))
        # заливка — янтарный цвет под тёмную пещеру
        fill_w = int(W * pct)
        pygame.draw.rect(self.display, (220, 160,  40), (x0, y0, fill_w, H))
        # граница
        pygame.draw.rect(self.display, (100,  60, 30), (x0, y0, W, H), 2)
        # подпись
        label = self.game_font.render("", False, (200, 200, 180)) # Выносливость
        self.display.blit(label, (x0, y0 - H - 4))
        # Бордер полосы
        pygame.draw.rect(
            self.display,
            config.COLOR_STAMINA_BORDER,
            (
                config.STAMINA_BAR_POS[0],
                config.STAMINA_BAR_POS[1],
                config.STAMINA_BAR_WIDTH,
                config.STAMINA_BAR_HEIGHT
            ),
            1
        )
        # Лейбл «stamina:»
        self.display.blit(
            self.game_font.render("stamina:", False, config.COLOR_STAMINA_BORDER),
            config.STAMINA_BAR_POS
        )
        

    
    def camera_load(self):
        print(f"[DEBUG] level={self.level}, x={self.player.pos[0]:.1f}, thresh={config.LEVEL2_CAMERA_SWITCH_X}")

        if self.level == 2 and self.player.pos[0] > config.LEVEL2_CAMERA_SWITCH_X:
            print("[DEBUG] Switching to only_x")
            self.tilemap.camera_info = "only_x" 
        match self.tilemap.camera_info:
            case "only_x":
                # По X: центрируем на игроке
                self.camera_shift[0] = int(self.player.pos[0]) - self.display.get_width() // 2
                if self.camera_shift[0] < 0:
                    self.camera_shift[0] = 0
                # По Y: фиксируем для первой карты
                if self.level == 1:
                    self.camera_shift[1] = config.FIRST_MAP_CAMERA_Y
                # иначе оставляем предыдущий или нулевой
            case "only_y":
                self.camera_shift[1] = (int(self.player.pos[1])-self.display.get_height()//2)
                if self.camera_shift[1]>0:
                    self.camera_shift[1]=0 
            case "free":
                # Меняем элементы списка, не создаём кортеж
                self.camera_shift[0] = int(self.player.pos[0]) - self.display.get_width()//2
                self.camera_shift[1] = int(self.player.pos[1]) - self.display.get_height()//2
    
    def run(self):
        intro = Messagebox(
            "System boot sequence incomplete—quantum cores unstable. \n"
            "You awaken as VIGIL-9, an autonomous repair drone entombed within the crystalline caverns \n"
            "of Nexus Prime. Sensors detect cascading quantum anomalies as the reactor core spirals toward collapse. \n"
            "Only you can stabilize the core and illuminate these pitch-black depths. Act swiftly, VIGIL-9.\n",
            (20,20)
        )
        intro.render(self)
        intro = Messagebox("X - dash \nArrows keys - move \nEscape - menu" ,(20,20))
        intro.render(self)
        while True:
            if self.next_level:
                self.load_next_level()
            if self.player.is_death:
                self.reload()
            self.display.fill(config.COLOR_BG)
            self.player.update(self.tilemap,self.movement)
            # Для отладки: выводим позицию игрока в консоль
            print(f"Player pos: x={self.player.pos[0]:.1f}, y={self.player.pos[1]:.1f}")

            self.tilemap.render(self.display,self.camera_shift)
            self.player.render(self.display,self.camera_shift)
            self.tilemap.fun_render(self.display, self.camera_shift)
            self.hud()
            self.camera_load()
            ## рассчитываем фокус-прямоугольник взгляда в координатах display
            #cx, cy = self.display.get_width() // 2, self.display.get_height() // 2
            #gaze_rect = pygame.Rect(
            #    cx - config.GAZE_RECT_SIZE[0] // 2,
            #    cy - config.GAZE_RECT_SIZE[1] // 2,
            #    config.GAZE_RECT_SIZE[0],
            #    config.GAZE_RECT_SIZE[1]
            #)
            ## отладочная отрисовка зоны взгляда
            #pygame.draw.rect(self.display, config.GAZE_DEBUG_COLOR, gaze_rect, 1)

            for event in pygame.event.get():
                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    case pygame.KEYDOWN:

                        match event.key:

                            case pygame.K_LEFT:
                                self.movement[0] =-1

                            case pygame.K_RIGHT:
                                self.movement[0] = 1

                            case pygame.K_SPACE:
                                self.player.jump()
                            case pygame.K_x:
                                self.player.Phantom_dash()

                            case pygame.K_DOWN:
                                self.movement[1] = 1
                                
                            case pygame.K_r:
                                self.reload()

                            case pygame.K_ESCAPE:
                                self.menu()
                                
                    case pygame.KEYUP:

                            match event.key:

                                case pygame.K_LEFT:
                                    self.movement[0] = 0

                                case pygame.K_RIGHT:
                                    self.movement[0] = 0     
                                    
            fps = int(self.clock.get_fps())
            fps_text = self.game_font.render(f"FPS: {fps}", False, config.COLOR_TEXT_PRIMARY)
            self.display.blit(fps_text, config.FPS_TEXT_POS)


                
            self.clock.tick(config.FPS)
            self.Screen.blit(pygame.transform.scale(self.display,self.Screen.get_size()),(0,0))
            pygame.display.update()
Game().menu()