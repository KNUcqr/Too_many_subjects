import pygame
import sys
import time

# 창 크기 설정
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 650

# 색 설정
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (100, 100, 250)
# 사전에 오류를 방지하기 위해 미리 변수들을 설정한다. (일부 정의 함수에서 잘 실행되도록 하기 위함.)
pygame.display.set_caption("교수님! 과제가 너무 많아요!")
font = None # font 같은 경우는 초반에 불러올 수 없어 None으로 실행한다음 메인 루프에서 조건식을 세워 빠져나오게 만듦.
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
is_openwindow = False


current_stage = 1 # 현재 스테이지
count = 0 # 적들 수
enemies = []
stage_bg = None
# 처음 실행했을 때 타이틀 화면에서 시작하도록 설정한다.
STATE = "start_screen"

# 타이틀 화면
def title_main():
    global STATE, font

    running = True
    pygame.init()

    title_filing = pygame.image.load("title_screen.png")
    title_filing = pygame.transform.scale(title_filing, (WINDOW_WIDTH, WINDOW_HEIGHT))

    start_button = Button_wiget(200, (WINDOW_HEIGHT) / 1.5, 200, 50, "게임 시작") 
    settings_button = Button_wiget(500, (WINDOW_HEIGHT) / 1.5, 200, 50, "설정") 
    quit_button = Button_wiget(800, (WINDOW_HEIGHT) / 1.5, 200, 50, "게임 종료") 

    if font == None: 
        font = pygame.font.Font("HakgyoansimDoldamM.ttf", 32)

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.mouse_click(event):
                STATE = "start"
                running = False

            if settings_button.mouse_click(event):
                STATE = "settings_screen" 
                running = False

            if quit_button.mouse_click(event):
                pygame.quit()
                sys.exit()
        
        screen.blit(title_filing, (0, 0))
        start_button.draw(screen)        
        settings_button.draw(screen)
        quit_button.draw(screen)

        team_font = pygame.font.Font("malgun.ttf", 24)
        team_meaning = team_font.render("Team. 강남대 정복자", True, (255, 255, 255))
        team_rect = team_meaning.get_rect(center = (WINDOW_WIDTH / 1.3, 120)) # 타이틀 제목을 코딩을 일일이 수정하지 않고 가운데로 맞추게 하기 위함.
        screen.blit(team_meaning, team_rect)

        pygame.display.update()
        clock.tick(60)

# 설정 화면
def settings_screen():
    global STATE, font, screen, VolumeController
    running = True
    
    seoijeong_display = pygame.image.load("setting_screen.png")
    seoijeong_display = pygame.transform.scale(seoijeong_display, (WINDOW_WIDTH, WINDOW_HEIGHT))

    font = pygame.font.Font("HakgyoansimDoldamM.ttf", 32)
    back_button = Button_wiget((WINDOW_WIDTH) / 10, (WINDOW_HEIGHT) / 1.5, 200, 50, "뒤로 가기")
    volume = VolumeController((WINDOW_WIDTH) / 2, (WINDOW_HEIGHT) / 1.5, 300, 20, 0, 100, 50)
    expandWindow_checkbox = Clicksquare((WINDOW_WIDTH) / 3, (WINDOW_HEIGHT) / 2.2, 30, "전체 화면", text_color = WHITE)

    # 소리 설정 테스트
    try:
        se = pygame.mixer.Sound("pygame_se.ogg")
    except:
        print("Error: 파일이 존재하지 않거나, 오디오 기기와 접속되어 있지 않습니다.")

    while running:
        screen.fill(WHITE)
        screen.blit(seoijeong_display, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.mouse_click(event):
                STATE = "start_screen"
                running = False

            volume.drag_console(event)

            prev_expandWindow_state = expandWindow_checkbox.is_checked
            expandWindow_checkbox.handle_event(event)

            if expandWindow_checkbox.is_checked != prev_expandWindow_state:
                is_fullscreen = expandWindow_checkbox.is_checked
                if is_fullscreen:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        setting_font = pygame.font.Font("HakgyoansimDoldamM.ttf", 36)
        setting_text = setting_font.render("소리 설정", True, BLACK) 
        screen.blit(setting_text, [400, 200])
        # 볼륨을 조절하는 정도에 따라 테스트 소리가 그 소리에 맞춰 나도록 설정했습니다.
        pygame.mixer.music.set_volume(volume.get_value() / 100)
        se.set_volume(volume.get_value() / 100)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] == 1: # SPACE 키를 누르면 소리가 나오기.
            se.play()

        sori_ttf = pygame.font.Font("HakgyoansimDoldamM.ttf", 22)
        sori_info = sori_ttf.render("[SPACE] 키를 눌러 소리를 테스트 하세요.", True, (0, 255, 255))

        back_button.draw(screen)
        volume.draw(screen)
        expandWindow_checkbox.draw(screen)
        screen.blit(sori_info, [400, 270])

        pygame.display.update()
        clock.tick(60)

# 버튼
class Button_wiget:
    def __init__(self, x, y, width, height, text): 
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.hover_color = (150, 150, 150)
    # 마우스의 위치를 이용해 버튼을 클릭할 수 있도록 함.
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos): 
            return True
        return False
# 게임 내 설정 화면에서도 볼륨을 조절하여 사용자들이 원하는 사운드로 플레이할 수 있다.
class VolumeController:
    def __init__(self, x, y ,width, height, min_value, max_value, default_value):
        self.rect = pygame.Rect(400, 250, width, height)
        self.min_volume = min_value
        self.max_volume = max_value
        self.value = default_value
        self.handle_rect = pygame.Rect(400, 250, 20, height)
        self.color = GRAY
        self.handle_color = BLUE
        self.dragging = False

    def drag_console(self, event):
        mouse_x, _ = pygame.mouse.get_pos()
        # 마우스로 볼륨바를 클릭하여 드래그하거나 땠을 때 활성, 비활성화가 되도록 설정한다.
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if self.dragging:
            self.handle_rect.x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.handle_rect.width))
            self.value = self.min_volume + (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width) * (self.max_volume - self.min_volume)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)

    def get_value(self):
        return self.value

# 체크박스
class Clicksquare:
    def __init__(self,x, y, size, text, text_color = BLACK):
        self.rect = pygame.Rect(x, y, size, size)
        self.is_checked = False # 처음 실행 할 때에는 당연히 창 모드로 실행한다.
        self.text = text
        self.text_color = text_color
        self.color = BLACK
        self.check_color = BLACK
        self.font = pygame.font.Font("HakgyoansimDoldamM.ttf", 28)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2) # 버튼을 누를 때 나타나는 표시 이 때 표시간격을 2로 설정한다.
        if self.is_checked:
           pygame.draw.rect(screen, self.check_color, self.rect.inflate(-10, -10))

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(midleft = (self.rect.right + 10, self.rect.centery))
        screen.blit(text_surface, text_rect) 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_checked = not self.is_checked

# 플레이어
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "right"
        self.frame_count = 0
        self.frame_delay = 5
        self.frame_index = 0
        HP = 100
        attack_damage = 10

        self.attacking = False
        self.attack_frame = 0
        self.attack_skill = 0
        self.attack_time = 0
        self.attack_wait_time = 1
        
        self.damaging = False
        self.damage_count = 0
        self.jump_count = 0

        self.man_r = [
            pygame.image.load("man1_r.png"),
            pygame.image.load("man_walk1_r.png"),
            pygame.image.load("man_walk2_r.png"),
            pygame.image.load("man_walk3_r.png")
        ]
        self.man_l = [
            pygame.image.load("man1_l.png"),
            pygame.image.load("man_walk1_l.png"),
            pygame.image.load("man_walk2_l.png"),
            pygame.image.load("man_walk3_l.png")
        ]
        self.man_attack_r = [
            pygame.image.load("man_attack1_r.png"),
            pygame.image.load("man_attack2_r.png"),
            pygame.image.load("man_attack3_r.png"),
            pygame.image.load("man_attack4_r.png"),
            pygame.image.load("man_attack5_r.png"),
            pygame.image.load("man_attack6_r.png")
        ]
        self.man_attack_l = [
            pygame.image.load("man_attack1_l.png"),
            pygame.image.load("man_attack2_l.png"),
            pygame.image.load("man_attack3_l.png"),
            pygame.image.load("man_attack4_l.png"),
            pygame.image.load("man_attack5_l.png"),
            pygame.image.load("man_attack6_l.png")
        ]
        self.man_damage_r = [
            pygame.image.load("man_damage1_r.png"),
            pygame.image.load("man_damage2_r.png")
        ]
        self.man_damage_l = [
            pygame.image.load("man_damage1_l.png"),
            pygame.image.load("man_damage2_l.png")
        ]

        self.rect_man = self.man_r[0].get_rect()
        self.rect_man.center = (self.x, self.y)
        self.rect_man.topleft = (self.x, self.y)

        self.man_width, self.man_height = self.man_r[0].get_size()
        self.damage_speed = 8
        self.se = pygame.mixer.Sound("hsound.ogg")

    def move(self, keys):  # 기본 움직임
        dx = 0
        dy = 0
        movespeed = 5
        key_pressed = False

        if not self.damaging:
            if keys[pygame.K_LEFT]:
                dx = -movespeed
                self.direction = "left"
                key_pressed = True
            if keys[pygame.K_RIGHT]:
                dx = movespeed
                self.direction = "right"
                key_pressed = True
            if keys[pygame.K_UP]:
                dy = -movespeed
                key_pressed = True
            if keys[pygame.K_DOWN]:
                dy = movespeed
                key_pressed = True

        if self.x + dx < 0:  # 움직임 제한
            dx = -self.x
        if self.y + dy < 0:
            dy = -self.y
        if self.x + dx > 1050:
            dx = 0
        if self.y + dy > 450:
            dy = 0

        self.x += dx  # 움직임 업데이트
        self.y += dy
        self.rect_man.topleft = (self.x, self.y)

        return key_pressed  # key_pressed 값을 반환

    def attack(self, screen):
        current_time = time.time()
        attacking_rect = pygame.Rect(
            self.x + (self.man_width if self.direction == "right" else -self.man_width),  # x 위치 계산
            self.y,  # y 위치 그대로
            self.man_width,  # 캐릭터와 동일한 너비
            self.man_height  # 캐릭터와 동일한 높이
        )
        pygame.draw.rect(screen, (0, 255, 0), attacking_rect)  # 내부를 채운 초록색 네모
        if current_time - self.attack_time <= self.attack_wait_time:
            self.attack_skill = (self.attack_skill + 1) % 3
        else:
            self.attack_skill = 0
        self.attacking = True
        self.attack_frame = 0  # 공격 시작 시 프레임을 0으로 초기화
        self.attack_time = current_time
        self.se.play()

    def handle_damage(self):
        self.damaging = True
        self.jump_count = 0
        self.damage_count = 0

    def update_damage(self):
        if self.jump_count < 10:
            self.y -= self.damage_speed
            self.x += -2 if self.direction == "right" else 2
        elif self.jump_count < 20:
            self.y += self.damage_speed // 2
        else:
            self.y += self.damage_speed + 5
            self.damaging = False
        self.jump_count += 1

    def animation_frame(self, key_pressed):
        if not self.attacking and not self.damaging:
            if key_pressed:
                self.frame_count += 1
                if self.frame_count >= self.frame_delay:
                    self.frame_count = 0
                    self.frame_index = (self.frame_index + 1) % 3 + 1
            else:
                self.frame_index = 0
        elif self.attacking:
            total_attack_frames = 2  # 각 공격마다 2개의 프레임 (12, 34, 56)
            # 공격 프레임을 처리하는 부분 수정
            attack_index = self.attack_skill * total_attack_frames + (self.attack_frame // self.frame_delay)
            if self.attack_frame // self.frame_delay >= total_attack_frames:  # 공격 프레임 종료
                self.attacking = False
                self.attack_frame = 0
            self.attack_frame += 1

    def draw(self, screen):
        if self.direction == "right":
            if self.attacking:
                attack_index = self.attack_skill * 2 + self.attack_frame // self.frame_delay
                screen.blit(self.man_attack_r[min(attack_index, len(self.man_attack_r) - 1)], [self.x, self.y])
            elif self.damaging:
                screen.blit(self.man_damage_r[self.damage_count], [self.x, self.y])
            else:
                screen.blit(self.man_r[self.frame_index], [self.x, self.y])
        elif self.direction == "left":
            if self.attacking:
                attack_index = self.attack_skill * 2 + self.attack_frame // self.frame_delay
                screen.blit(self.man_attack_l[min(attack_index, len(self.man_attack_l) - 1)], [self.x, self.y])
            elif self.damaging:
                screen.blit(self.man_damage_l[self.damage_count], [self.x, self.y])
            else:
                screen.blit(self.man_l[self.frame_index], [self.x, self.y])
# 게임 시작
def game_play():
    global STATE, count, current_stage
    pygame.init()
    pygame.display.set_caption("교수님! 과제가 너무 많아요!")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    bg_image = pygame.image.load("bg1.png")
    stage_info = pygame.font.Font("malgun.ttf", 24)
    stage_text = stage_info.render("Stage : " + str(current_stage), True, BLACK) 
    screen.blit(stage_text, [600, 400])
    player = Player(150, 250)
    # player2 = Player(300, 250)

    # 스테이지 배경 설정
    def draw_bg():
        scale_bg = pygame.transform.scale(bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scale_bg, [0, 0])

    # 스테이지를 로드
    load_stage(current_stage)

    while True:
        fake_religious_man = pygame.image.load("boss_walk1_r.png")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and not player.attacking:
                    player.attack(screen)
                if event.key == pygame.K_x and not player.damaging:
                    player.handle_damage()

                if event.key == pygame.K_n:
                    if count > 0:
                        enemies.pop()
                        count -= 1
        stage_info = pygame.font.Font("malgun.ttf", 24)
        stage_text = stage_info.render("Stage : " + str(current_stage), True, WHITE) # report : 현재 스테이지 상황을 표시해야 하는 데 나오지 않음
        screen.blit(stage_text, [600, 400])

        keys = pygame.key.get_pressed()
        key_pressed = player.move(keys)

        if player.damaging:
            player.update_damage()

        player.animation_frame(key_pressed)

        draw_bg()
        player.draw(screen)
        # player2.draw(screen)

        for (ex, ey) in enemies:
            screen.blit(fake_religious_man, (ex, ey))
        if count == 0: # 적을 모두 물리쳤다면
            clear_font = pygame.font.Font("malgun.ttf", 40)
            clear_info = clear_font.render("Go! --->", True, (255, 255, 255))
            clear_rect = clear_info.get_rect(center = (WINDOW_WIDTH / 2, 100))
            screen.blit(clear_info, clear_rect)
            # 플레이어의 x 좌표 위치가 900 이상 도달한다면 (현재 문제 제기가 된 부분)
            if player.x > 900:
                current_stage += 1
                load_stage(current_stage)
                player.x, player.y = 150, 250

        pygame.display.update()
        clock.tick(60)

def load_stage(stage_number):
    global count, enemies, stage_bg

    # 스테이지 별마다 적들 개체 수 설정
    if stage_number == 1:
        count = 5
        enemies = [(200 + i * 60, 300) for i in range(count)]
    elif stage_number == 2:
        count = 8
        enemies = [(200 + i * 60, 300) for i in range(count)]
        stage_bg = pygame.image.load("next_stage.png")

# 게임 오버
def game_end():
    global STATE, font
    running = True
    mission_failed = pygame.image.load("mission_failed.png")
    mission_failed = pygame.transform.scale(mission_failed, (WINDOW_WIDTH, WINDOW_HEIGHT))

    font = pygame.font.Font("HakgyoansimDoldamM.ttf", 32)

    retry_button = Button_wiget(200, (WINDOW_HEIGHT) / 1.3, 300, 50, "Retry?")
    give_up = Button_wiget(700, (WINDOW_HEIGHT) / 1.3, 300, 50, "타이틀로 돌아가기")

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if retry_button.mouse_click(event):
                STATE = "start"
                running = False
            if give_up.mouse_click(event):
                STATE = "start_screen"
                running = False
        screen.blit(mission_failed, (0, 0))
        retry_button.draw(screen)
        give_up.draw(screen)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    title_main()

    while True: # 화면 전환 여부
        if STATE == "start_screen":
            title_main()
        elif STATE == "settings_screen":
            settings_screen()
        elif STATE == "start": # 여기서 부터 본격적으로 게임이 시작된다.
            game_play()
        elif STATE == "game_over": # 게임 오버
            game_end()