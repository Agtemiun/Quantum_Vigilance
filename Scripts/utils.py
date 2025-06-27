import pygame
import os
import config

BASE_IMG_PATH='data/images/'

def image_load(path):
    img = pygame.image.load(BASE_IMG_PATH+path)
    img.set_colorkey((0,0,0))
    return img

def images_load(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH+path)):
        images.append(image_load(path+"/"+img_name))
    return images 
class Textbox:

    def __init__(self,pos,text,text_size=config.FONT_SIZE,height=config.TEXTBOX_DEFAULT_HEIGHT,widht=config.TEXTBOX_DEFAULT_WIDTH):
        self.font = pygame.font.Font(config.FONT_PATH,text_size)
        self.text = self.font.render(text,False,(255,142,128))
        self.active_text = self.font.render(text,False,(74,36,128))
        self.textbox_pos = list(pos)
        self.size = (height,widht)

    def render(self,screen,active):
        if active:
            pygame.draw.rect(screen,(255,142,128),(self.textbox_pos[0]-10,self.textbox_pos[1]-10,self.size[1],self.size[0]))
            pygame.draw.rect(screen,(74,36,128),(self.textbox_pos[0]-10,self.textbox_pos[1]-10,self.size[1],self.size[0]),3)
            screen.blit(self.active_text,self.textbox_pos)
        else:
            pygame.draw.rect(screen,(5,31,57),(self.textbox_pos[0]-10,self.textbox_pos[1]-10,self.size[1],self.size[0]))
            pygame.draw.rect(screen,(255,142,128),(self.textbox_pos[0]-10,self.textbox_pos[1]-10,self.size[1],self.size[0]),3)
            screen.blit(self.text,self.textbox_pos)
            
class Messagebox():
    def __init__(self, text, pos):
        self.text = text
        self.size = config.MESSAGEBOX_SIZE
        self.textbox_pos = pos
        self.font = pygame.font.Font(config.FONT_PATH, config.FONT_SIZE)

    def render(self, game):
        # Фон
        pygame.draw.rect(
            game.display,
            config.COLOR_MESSAGEBOX_BG,
            (
                self.textbox_pos[0] - config.TEXTBOX_PADDING,
                self.textbox_pos[1] - config.TEXTBOX_PADDING,
                self.size[0],
                self.size[1]
            )
        )
        # Рамка
        pygame.draw.rect(
            game.display,
            config.COLOR_MESSAGEBOX_BORDER,
            (
                self.textbox_pos[0] - config.TEXTBOX_PADDING,
                self.textbox_pos[1] - config.TEXTBOX_PADDING,
                self.size[0],
                self.size[1]
            ),
            3
        )

        x_shift = 0
        y_shift = 0
        for char in self.text:
            x_shift += config.MESSAGEBOX_CHAR_WIDTH
            if x_shift > config.MESSAGEBOX_LINE_WRAP:
                y_shift += config.MESSAGEBOX_LINE_HEIGHT
                x_shift = 0

            glyph = self.font.render(char, False, config.COLOR_MESSAGEBOX_BORDER)
            game.display.blit(
                glyph,
                (self.textbox_pos[0] + x_shift, self.textbox_pos[1] + y_shift)
            )
            # Анимация «печати»
            game.Screen.blit(
                pygame.transform.scale(game.display, game.Screen.get_size()),
                (0, 0)
            )
            pygame.display.update()

        # Ждём пробела
        exit_dialog = False
        while not exit_dialog:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    exit_dialog = True


class Animation:
    def __init__(self,images, duration=5, loop=True):
        self.images = images
        self.loop = loop
        self.duration = duration
        self.done = False
        self.frame = 0
    def copy(self):
        return Animation(self.images,self.duration,self.loop)
    
    def update(self):
        if self.loop:
            self.frame=(self.frame +1)%(self.duration*len(self.images))
        else:
            self.frame = min(self.frame+1,self.duration*len(self.images)-1)
            if self.frame>= self.duration * len(self.images)-1:
                self.done = True  

    def img(self):
        return self.images[int(self.frame/self.duration)]
    
    
