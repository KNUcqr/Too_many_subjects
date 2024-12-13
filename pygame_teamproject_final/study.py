import pygame
import random
import time
import sys
import math

pygame.init()

SCREEN_WIDTH = 1200  # 화면 너비
SCREEN_HEIGHT = 650  # 화면 높이
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (100, 100, 250)

is_openwindow = False
STATE = "start_screen"
clock = pygame.time.Clock()

font = pygame.font.SysFont("Pretendard Medium", 24)
pygame.mixer.music.load("8bit_adventure.ogg")
# 볼륨 조절 (0.0 ~ 1.0)
pygame.mixer.music.set_volume(0.5)

def title_main(): #타이틀 화면
    global STATE, font

    running = True
    pygame.init()

    title_filing = pygame.image.load("title_screen.png")
    title_filing = pygame.transform.scale(title_filing, (SCREEN_WIDTH, SCREEN_HEIGHT))

    start_button = Button_wiget(200, (SCREEN_HEIGHT) / 1.5, 200, 50, "게임 시작") 
    settings_button = Button_wiget(500, (SCREEN_HEIGHT) / 1.5, 200, 50, "설정") 
    quit_button = Button_wiget(800, (SCREEN_HEIGHT) / 1.5, 200, 50, "게임 종료") 

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
        team_rect = team_meaning.get_rect(center = (SCREEN_WIDTH / 1.3, 120)) # 타이틀 제목을 코딩을 일일이 수정하지 않고 가운데로 맞추게 하기 위함.
        screen.blit(team_meaning, team_rect)

        pygame.display.update()
        clock.tick(60)
def settings_screen(): # 설정 화면
    global STATE, font, screen, VolumeController
    running = True
    
    seoijeong_display = pygame.image.load("setting_screen.png")
    seoijeong_display = pygame.transform.scale(seoijeong_display, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font("HakgyoansimDoldamM.ttf", 32)
    back_button = Button_wiget((SCREEN_WIDTH) / 10, (SCREEN_HEIGHT) / 1.5, 200, 50, "뒤로 가기")
    volume = VolumeController((SCREEN_WIDTH) / 2, (SCREEN_HEIGHT) / 1.5, 300, 20, 0, 100, 50)
    expandWindow_checkbox = Clicksquare((SCREEN_WIDTH) / 3, (SCREEN_HEIGHT) / 2.2, 30, "전체 화면", text_color = WHITE)

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
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        setting_font = pygame.font.Font("HakgyoansimDoldamM.ttf", 36)
        setting_text = setting_font.render("소리 설정", True, BLACK) 
        screen.blit(setting_text, [400, 200])
        # 볼륨을 조절하는 정도에 따라 테스트 소리가 그 소리에 맞춰 나도록 설정했습니다.
        pygame.mixer.music.set_volume(volume.get_value() / 100) # define VolumeController의 get_value()값을 여기에 돌려준다.
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
def game_end(): #게임 오버
    global STATE, font
    running = True
    mission_failed = pygame.image.load("mission_failed.png")
    mission_failed = pygame.transform.scale(mission_failed, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font = pygame.font.Font("HakgyoansimDoldamM.ttf", 32)

    retry_button = Button_wiget(200, (SCREEN_HEIGHT) / 1.3, 300, 50, "Retry?")
    give_up = Button_wiget(700, (SCREEN_HEIGHT) / 1.3, 300, 50, "타이틀로 돌아가기")

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
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

class Button_wiget: # 버튼
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
    
class VolumeController: # 게임 내 설정 화면에서도 볼륨을 조절하여 사용자들이 원하는 사운드로 플레이할 수 있다.
    def __init__(self, x, y ,width, height, min_value, max_value, default_value):
        self.rect = pygame.Rect(400, 250, width, height)
        self.min_volume = min_value
        self.max_volume = max_value
        self.value = default_value
        self.handle_rect = pygame.Rect(400, 250, 20, height)
        self.color = GRAY
        self.handle_color = BLUE
        self.dragging = False

    # 마우스 이벤트를 받는 드래그
    def drag_console(self, event):
        mouse_x, _ = pygame.mouse.get_pos() # 드래그 중일 때 핸들 위치 값 업데이트
        # 마우스로 볼륨바를 클릭하여 드래그하거나 땠을 때 활성화한다.
        if event.type == pygame.MOUSEBUTTONDOWN and self.handle_rect.collidepoint(event.pos):
            self.dragging = True
        # 마우스를 땠을 때 비활성화한다.
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if self.dragging:
            # 핸들의 x 좌표를 마우스 x 좌표에 맞추되 슬라이더 영역을 벗어나지 않는다.
            self.handle_rect.x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.handle_rect.width)) 
            # 핸들의 위치를 최솟값 ~ 최대값 사이로 설정한다.
            self.value = self.min_volume + (self.handle_rect.x - self.rect.x) / (self.rect.width - self.handle_rect.width) * (self.max_volume - self.min_volume)

    def draw(self, screen): # 슬라이드 바 나타내기
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.handle_color, self.handle_rect)
    # 볼륨 값을 반환한다.
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
        self.check_color = BLACK # 활성화 되었을 때에는 검정색으로 칠한다.
        self.font = pygame.font.Font("HakgyoansimDoldamM.ttf", 28)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2) # 버튼을 누를 때 나타나는 표시 이 때 테두리 두께를 2로 설정한다.
        if self.is_checked:
           # 원래 사각형보다 10픽셀 줄어든 사각형을 만들어 내부에 색을 채워넣어 체크
           pygame.draw.rect(screen, self.check_color, self.rect.inflate(-10, -10))

        text_surface = self.font.render(self.text, True, BLACK)
        # 텍스트 사각형을 체크박스 오른쪽 약간 떨어진 위치에 수직 중심이 맞춰지도록 설정
        text_rect = text_surface.get_rect(midleft = (self.rect.right + 10, self.rect.centery))
        screen.blit(text_surface, text_rect) 

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 마우스 클릭 좌표가 체크 박스에 들어갔는가?
            if self.rect.collidepoint(event.pos):
                self.is_checked = not self.is_checked # 체크가 되어있지 않다면 체크, 체크되었다면 체크 해제
 
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, speed, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx
        self.dy = dy
        self.speed = speed

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.kill()
class FallingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
class Kakaotalk(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, direction_facing):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
        
        # 방향에 맞는 이미지 설정
        if direction_facing == "left":
            self.image = pygame.image.load("katalk.png")  # 왼쪽을 바라볼 때 발사체 이미지
        else:
            self.image = pygame.image.load("katalk.png")  # 오른쪽을 바라볼 때 발사체 이미지
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5 * direction  # 방향에 맞는 속도 설정

    def update(self):
        self.rect.x += self.speed

class Player: # 플레이어
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "right"
        self.frame_count = 0
        self.frame_delay = 5
        self.frame_index = 0
        self.HP = 100

        self.attacking = False # 공격 상태
        self.attack_frame = 0
        self.attack_skill = 0
        self.attack_time = 0
        self.attack_wait_time = 1

        self.damaging = False #데미지 상태
        self.damage_count = 0
        self.jump_count = 0

        self.is_stunned = False  # 스턴 상태 초기화
        self.speed_factor = 1.0  # 이동 속도 계수 초기화

        self.slowed = False
        self.slowed_start_time = 0

        self.man_r = [
            pygame.image.load("man1_r.png"),
            pygame.image.load("man_walk1_r.png"),
            pygame.image.load("man_walk2_r.png"),
            pygame.image.load("man_walk3_r.png"),
            pygame.image.load("man1_status.png")
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
        self.rect_man.topleft = (self.x, self.y)

        self.man_width, self.man_height = self.man_r[0].get_size()
        self.damage_speed = 8
        self.se1 = pygame.mixer.Sound("hsound.ogg")
        self.se2 = pygame.mixer.Sound("damage.ogg")

    def move(self, keys):  # 움직임
        if self.is_stunned:  # 스턴 상태일 때는 움직이지 않음
            return False
        
        dx = 0
        dy = 0
        slowspeed = 2
        movespeed = slowspeed if self.slowed else 5 * getattr(self, 'speed_factor', 1.0)  # 이동 속도에 speed_factor 적용
# 움직임 속도
        key_pressed = False

        if not self.damaging: # 방향키로 이동 적용
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

        if self.x + dx < 0: # 움직임 제한
            dx = -self.x
        if self.y + dy < 0:
            dy = -self.y
        if self.x + dx > 1050:
            dx = 0
        if self.y + dy > 450:
            dy = 0

        self.x += dx # 움직임 업데이트
        self.y += dy
        self.rect_man.topleft = (self.x, self.y)

        if self.slowed and time.time() - self.slowed_start_time > 1:
            self.slowed = False

        return key_pressed # 값 반환

    def hit_by_kakaotalk(self): #주인공이 원거리 공격에 맞았을 때 체력 감소와 슬로우 효과 처리.
        self.slowed = True  # 슬로우 상태 활성화
        self.slowed_start_time = time.time()  # 슬로우 시작 시간 기록
        self.HP -= self.HP * 0.03  # 체력을 3%감소
        self.damaging = True
        self.jump_count = 0
        self.damage_count = 0
        if self.HP < 0:  # 체력이 0 아래로 내려가지 않도록 제한
            self.HP = 0

    def attack(self, screen, enemies): # 공격
        current_time = time.time()
        attacking_rect = pygame.Rect(
            self.x + (self.man_width if self.direction == "right" else -self.man_width),
            self.y,
            self.man_width // 2,
            self.man_height,
        )
        #pygame.draw.rect(screen, (0, 255, 0), attacking_rect) 사정거리 확인 - 주석 해제시 초록색으로 확인 가능

        for enemy in enemies:
            if attacking_rect.colliderect(enemy.rect):
                knockback_dir = (1 if self.direction == "right" else -1, 0)
                enemy.take_damage(knockback_dir)
                self.se2.play()

        if current_time - self.attack_time <= self.attack_wait_time:
            self.attack_skill = (self.attack_skill + 1) % 3
        else:
            self.attack_skill = 0
        self.attacking = True
        self.attack_frame = 0
        self.attack_time = current_time
        self.se1.play()

    def get_hit(self): #(테스트용)데미지 받기 - X를 통한 테스트
        global STATE
        self.damaging = True
        self.jump_count = 0
        self.damage_count = 0
        self.HP -= 10
        if self.HP <= 0:
            print("사망")
            game_end()
            

    def damage_jump(self): #데미지시 넉백
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
            total_attack_frames = 2
            attack_index = self.attack_skill * total_attack_frames + (
                self.attack_frame // self.frame_delay
            )
            if self.attack_frame // self.frame_delay >= total_attack_frames:
                self.attacking = False
                self.attack_frame = 0
            self.attack_frame += 1

    def draw(self, screen): # 애니매이션 프레임 출력
        if self.direction == "right":
            if self.attacking:
                attack_index = (
                    self.attack_skill * 2 + self.attack_frame // self.frame_delay
                )
                screen.blit(
                    self.man_attack_r[
                        min(attack_index, len(self.man_attack_r) - 1)
                    ],
                    [self.x, self.y],
                )
            elif self.damaging:
                screen.blit(self.man_damage_r[self.damage_count], [self.x, self.y])
            else:
                screen.blit(self.man_r[self.frame_index], [self.x, self.y])
        elif self.direction == "left":
            if self.attacking:
                attack_index = self.attack_skill * 2 + self.attack_frame // self.frame_delay
                screen.blit(
                    self.man_attack_l[
                        min(attack_index, len(self.man_attack_l) - 1)
                    ],
                    [self.x, self.y],
                )
            elif self.damaging:
                screen.blit(self.man_damage_l[self.damage_count], [self.x, self.y])
            else:
                screen.blit(self.man_l[self.frame_index], [self.x, self.y])
    
    def draw_HP(self):
        pygame.draw.rect(screen, RED, (10, 170, 150, 20)) # 체력 바탕
        pygame.draw.rect(screen, GREEN, (10, 170, 150 * (self.HP / 100), 20)) # 남은 체력
        screen.blit(self.man_r[4], [10, 10]) # 플레이어 프로필 출력

    def handle_projectile_hit(self, projectiles): # 보스 관련 속성
        for projectile in projectiles:
            if self.rect_man.colliderect(projectile.rect):
                self.HP -= 5
                self.damaging = True
                self.jump_count = 0
                self.damage_count = 0
                self.slow_down(1.0)
                projectile.kill()

    def handle_falling_object_hit(self, falling_objects):
        for obj in falling_objects:
            if self.rect_man.colliderect(obj.rect):
                self.HP -= 15
                self.damaging = True
                self.jump_count = 0
                self.damage_count = 0
                self.stun(1.0)
                obj.kill()

    def slow_down(self, duration):
        self.speed_factor = 0.5
        pygame.time.set_timer(pygame.USEREVENT + 1, int(duration * 1000))

    def stun(self, duration):
        self.is_stunned = True
        pygame.time.set_timer(pygame.USEREVENT + 2, int(duration * 1000))

    def reset_slow(self):
        self.speed_factor = 1.0

    def reset_stun(self):
        self.is_stunned = False

class CultMember(pygame.sprite.Sprite): # 빌런1 사이비
    def __init__(self, x, y):
        super().__init__()
        self.image_left = [
            pygame.image.load("vil1_walk1_l.png"),
            pygame.image.load("vil1_walk2_l.png"),
            pygame.image.load("vil1_walk3_l.png"),
        ]
        self.image_right = [
            pygame.image.load("vil1_walk1_r.png"),
            pygame.image.load("vil1_walk2_r.png"),
            pygame.image.load("vil1_walk3_r.png"),
        ]

        # 넉백 이미지 (왼쪽, 오른쪽)
        self.knockback_left = [
            pygame.image.load("vil1_knockback1_r.png"),
            pygame.image.load("vil1_knockback2_r.png")
        ]
        self.knockback_right = [
            pygame.image.load("vil1_knockback1_l.png"),
            pygame.image.load("vil1_knockback2_l.png")
        ]
        
        # 죽음 이미지 (왼쪽, 오른쪽)
        self.dead_left = [
            pygame.image.load("vil1_dead1_l.png"),
            pygame.image.load("vil1_dead2_l.png")
        ]
        self.dead_right = [
            pygame.image.load("vil1_dead1_r.png"),
            pygame.image.load("vil1_dead2_r.png")
        ]

        self.rect = self.image_left[0].get_rect()
        self.rect.center = (x, y)

        self.max_health = 100
        self.health = self.max_health
        self.health_bar_length = 80

        self.speed = 2
        self.last_hit_time = time.time()
        self.direction_change_time = time.time()
        self.direction = random.choice(
            ["left", "right", "up-left", "up-right", "down-left", "down-right"]
        )

        self.animation_frame = 0
        self.animation_speed = 0.1
        self.last_animation_time = time.time()

        self.image = self.image_left[0]

        # 넉백 관련 속성
        self.knockback = False
        self.knockback_timer = 0
        self.knockback_duration = 0.5
        self.knockback_direction = (0, 0)
        self.knockback_speed = 3
        self.knockback_count = 0

        # 죽음 관련 속성
        self.dead = False
        self.dead_timer = 0
        self.dead_duration = 1  # 죽은 이미지가 1초 동안 유지됨

    def move(self):
        if self.knockback:
            self.update_knockback()
        elif self.dead:
            self.update_death()
        else:
            if time.time() - self.direction_change_time >= 3:
                self.direction = random.choice(
                    ["left", "right", "up-left", "up-right", "down-left", "down-right"]
                )
                self.direction_change_time = time.time()

            if self.direction == "left":
                self.rect.x -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "right":
                self.rect.x += self.speed
                self.update_animation(self.image_right)
            elif self.direction == "up-left":
                self.rect.x -= self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "up-right":
                self.rect.x += self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_right)
            elif self.direction == "down-left":
                self.rect.x -= self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_left)
            elif self.direction == "down-right":
                self.rect.x += self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_right)

            # 경계 조건 체크
            if self.rect.left < 0:
                self.rect.left = 0
                if "left" in self.direction:
                    self.direction = self.direction.replace("left", "right")
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                if "right" in self.direction:
                    self.direction = self.direction.replace("right", "left")
            if self.rect.top < 0:
                self.rect.top = 0
                if "up" in self.direction:
                    self.direction = self.direction.replace("up", "down")
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                if "down" in self.direction:
                    self.direction = self.direction.replace("down", "up")

    def update_knockback(self):
        if time.time() - self.knockback_timer >= self.knockback_duration:
            self.knockback = False
        else:
            if self.knockback_direction[0] < 0:
                self.update_animation(self.knockback_left)
            else:
                self.update_animation(self.knockback_right)
            self.rect.x += self.knockback_direction[0] * self.knockback_speed
            self.rect.y += self.knockback_direction[1] * self.knockback_speed

    def update_death(self):
        if time.time() - self.dead_timer >= self.dead_duration:
            self.kill()
        else:
            if self.direction == 'left':
                self.update_animation(self.dead_left)
            elif self.direction == 'right':
                self.update_animation(self.dead_right)

    def update_animation(self, direction_images):
        if time.time() - self.last_animation_time >= self.animation_speed:
            self.animation_frame += 1
            if self.animation_frame >= len(direction_images):
                self.animation_frame = 0
            self.image = direction_images[self.animation_frame]
            self.last_animation_time = time.time()


    def take_damage(self, knockback_dir):
        damage = self.max_health * 0.1
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.dead = True
            self.dead_timer = time.time()

        self.last_hit_time = time.time()

        # 넉백 설정 - 3번 맞으면 넉백
        self.knockback_timer = time.time()
        self.knockback_direction = knockback_dir
        self.knockback_count += 1
        if self.knockback_count >= 3:
            self.knockback = True
            self.knockback_count = 0

    def regenerate_health(self):
        if time.time() - self.last_hit_time >= 5 and self.health < self.max_health:
            self.health += self.max_health * 0.05
            if self.health > self.max_health:
                self.health = self.max_health

    def draw_health_bar(self):
        pygame.draw.rect(screen, RED, (self.rect.centerx - self.health_bar_length // 2, self.rect.top - 10, self.health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - self.health_bar_length // 2, self.rect.top - 10, self.health_bar_length * (self.health / self.max_health), 5))
class Teammate(pygame.sprite.Sprite): # 빌런2 진상팀원
    def __init__(self, x, y):
        super().__init__()
        self.image_left = [
            pygame.image.load("vil2_walk1_l.png"),
            pygame.image.load("vil2_walk2_l.png"),
            pygame.image.load("vil2_walk3_l.png"),
        ]
        self.image_right = [
            pygame.image.load("vil2_walk1_r.png"),
            pygame.image.load("vil2_walk2_r.png"),
            pygame.image.load("vil2_walk3_r.png"),
        ]

        # 넉백 이미지 (왼쪽, 오른쪽)
        self.knockback_left = [
            pygame.image.load("vil2_knockback1_r.png"),
            pygame.image.load("vil2_knockback2_r.png")
        ]
        self.knockback_right = [
            pygame.image.load("vil2_knockback1_l.png"),
            pygame.image.load("vil2_knockback2_l.png")
        ]
        
        # 죽음 이미지 (왼쪽, 오른쪽)
        self.dead_left = [
            pygame.image.load("vil2_dead1_l.png"),
            pygame.image.load("vil2_dead2_l.png")
        ]
        self.dead_right = [
            pygame.image.load("vil2_dead1_r.png"),
            pygame.image.load("vil2_dead2_r.png")
        ]

        self.rect = self.image_left[0].get_rect()
        self.rect.center = (x, y)

        self.max_health = 100
        self.health = self.max_health
        self.health_bar_length = 80

        self.speed = 1
        self.last_hit_time = time.time()
        self.direction_change_time = time.time()
        self.direction = random.choice(
            ["left", "right", "up-left", "up-right", "down-left", "down-right"]
        )

        self.animation_frame = 0
        self.animation_speed = 0.1
        self.last_animation_time = time.time()

        self.image = self.image_left[0]

        # 넉백 관련 속성
        self.knockback = False
        self.knockback_timer = 0
        self.knockback_duration = 0.5
        self.knockback_direction = (0, 0)
        self.knockback_speed = 5
        self.knockback_count = 0

        # 죽음 관련 속성
        self.dead = False
        self.dead_timer = 0
        self.dead_duration = 1  # 죽은 이미지가 1초 동안 유지됨
        
        # 원거리 공격 발사 타이머 초기화
        self.kakaotalk_timer = time.time()

    def shoot(self, kakaotalks):
        if time.time() - self.kakaotalk_timer > 3:  # 3초마다 발사
            direction = random.choice([-1, 1])  # 랜덤으로 왼쪽(-1) 또는 오른쪽(1)으로 발사
            direction_facing = "left" if self.direction == "left" else "right"  # 적이 바라보는 방향 확인
            kakaotalk = Kakaotalk(self.rect.centerx, self.rect.centery, direction, direction_facing)
            kakaotalks.add(kakaotalk)
            self.kakaotalk_timer = time.time()


    def move(self):
        if self.knockback:
            self.update_knockback()
        elif self.dead:
            self.update_death()
        else:
            if time.time() - self.direction_change_time >= 3:
                self.direction = random.choice(
                    ["left", "right", "up-left", "up-right", "down-left", "down-right"]
                )
                self.direction_change_time = time.time()

            if self.direction == "left":
                self.rect.x -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "right":
                self.rect.x += self.speed
                self.update_animation(self.image_right)
            elif self.direction == "up-left":
                self.rect.x -= self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "up-right":
                self.rect.x += self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_right)
            elif self.direction == "down-left":
                self.rect.x -= self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_left)
            elif self.direction == "down-right":
                self.rect.x += self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_right)

            # 경계 조건 체크
            if self.rect.left < 0:
                self.rect.left = 0
                if "left" in self.direction:
                    self.direction = self.direction.replace("left", "right")
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                if "right" in self.direction:
                    self.direction = self.direction.replace("right", "left")
            if self.rect.top < 0:
                self.rect.top = 0
                if "up" in self.direction:
                    self.direction = self.direction.replace("up", "down")
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                if "down" in self.direction:
                    self.direction = self.direction.replace("down", "up")

    def update_knockback(self):
        if time.time() - self.knockback_timer >= self.knockback_duration:
            self.knockback = False
        else:
            if self.knockback_direction[0] < 0:
                self.update_animation(self.knockback_left)
            else:
                self.update_animation(self.knockback_right)
            self.rect.x += self.knockback_direction[0] * self.knockback_speed
            self.rect.y += self.knockback_direction[1] * self.knockback_speed

    def update_death(self):
        if time.time() - self.dead_timer >= self.dead_duration:
            self.kill()
        else:
            if self.direction == 'left':
                self.update_animation(self.dead_left)
            elif self.direction == 'right':
                self.update_animation(self.dead_right)

    def update_animation(self, direction_images):
        if time.time() - self.last_animation_time >= self.animation_speed:
            self.animation_frame += 1
            if self.animation_frame >= len(direction_images):
                self.animation_frame = 0
            self.image = direction_images[self.animation_frame]
            self.last_animation_time = time.time()


    def take_damage(self, knockback_dir):
        damage = self.max_health * 0.1
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.dead = True
            self.dead_timer = time.time()

        self.last_hit_time = time.time()

        # 넉백 설정 - 3번 맞으면 넉백
        self.knockback_timer = time.time()
        self.knockback_direction = knockback_dir
        self.knockback_count += 1
        if self.knockback_count >= 3:
            self.knockback = True
            self.knockback_count = 0

    def regenerate_health(self):
        if time.time() - self.last_hit_time >= 5 and self.health < self.max_health:
            self.health += self.max_health * 0.05
            if self.health > self.max_health:
                self.health = self.max_health

    def draw_health_bar(self):
        pygame.draw.rect(screen, RED, (self.rect.centerx - self.health_bar_length // 2, self.rect.top - 10, self.health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - self.health_bar_length // 2, self.rect.top- 10, self.health_bar_length * (self.health / self.max_health), 5))
class Boss(pygame.sprite.Sprite): #보스 교수님
    def __init__(self, x, y):
        super().__init__()
        self.image_left = [
            pygame.image.load("boss_walk1_l.png"),
            pygame.image.load("boss_walk2_l.png")
        ]
        self.image_right = [
            pygame.image.load("boss_walk1_r.png"),
            pygame.image.load("boss_walk2_r.png")
        ]

        # 넉백 이미지 (왼쪽, 오른쪽)
        self.knockback_left = [
            pygame.image.load("boss_damage1_r.png")
        ]
        self.knockback_right = [
            pygame.image.load("boss_damage1_l.png")
        ]

        self.rect = self.image_left[0].get_rect()
        self.rect.center = (x, y)

        self.max_health = 400
        self.health = self.max_health
        self.health_bar_length = 80

        self.speed = 2
        self.last_hit_time = time.time()
        self.direction_change_time = time.time()
        self.direction = random.choice(
            ["left", "right", "up-left", "up-right", "down-left", "down-right"]
        )

        self.animation_frame = 0
        self.animation_speed = 0.1
        self.last_animation_time = time.time()

        self.image = self.image_left[0]

        # 넉백 관련 속성
        self.knockback = False
        self.knockback_timer = 0
        self.knockback_duration = 0.5
        self.knockback_direction = (0, 0)
        self.knockback_speed = 15
        self.knockback_count = 0

        # 죽음 관련 속성
        self.dead = False
        self.dead_timer = 0
        self.dead_duration = 1  # 죽은 이미지가 1초 동안 유지됨

    def move(self):
        if self.knockback:
            self.update_knockback()
        elif self.dead:
            self.update_death()
        else:
            if time.time() - self.direction_change_time >= 3:
                self.direction = random.choice(
                    ["left", "right", "up-left", "up-right", "down-left", "down-right"]
                )
                self.direction_change_time = time.time()

            if self.direction == "left":
                self.rect.x -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "right":
                self.rect.x += self.speed
                self.update_animation(self.image_right)
            elif self.direction == "up-left":
                self.rect.x -= self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_left)
            elif self.direction == "up-right":
                self.rect.x += self.speed
                self.rect.y -= self.speed
                self.update_animation(self.image_right)
            elif self.direction == "down-left":
                self.rect.x -= self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_left)
            elif self.direction == "down-right":
                self.rect.x += self.speed
                self.rect.y += self.speed
                self.update_animation(self.image_right)

            # 경계 조건 체크
            if self.rect.left < 0:
                self.rect.left = 0
                if "left" in self.direction:
                    self.direction = self.direction.replace("left", "right")
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                if "right" in self.direction:
                    self.direction = self.direction.replace("right", "left")
            if self.rect.top < 0:
                self.rect.top = 0
                if "up" in self.direction:
                    self.direction = self.direction.replace("up", "down")
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                if "down" in self.direction:
                    self.direction = self.direction.replace("down", "up")

    def update_knockback(self):
        if time.time() - self.knockback_timer >= self.knockback_duration:
            self.knockback = False
        else:
            if self.knockback_direction[0] < 0:
                self.update_animation(self.knockback_left)
            else:
                self.update_animation(self.knockback_right)
            self.rect.x += self.knockback_direction[0] * self.knockback_speed
            self.rect.y += self.knockback_direction[1] * self.knockback_speed

    def update_death(self):
        if time.time() - self.dead_timer >= self.dead_duration:
            self.kill()
        else:
            if self.direction == 'left':
                self.update_animation(self.dead_left)
            elif self.direction == 'right':
                self.update_animation(self.dead_right)

    def update_animation(self, direction_images):
        if time.time() - self.last_animation_time >= self.animation_speed:
            self.animation_frame += 1
            if self.animation_frame >= len(direction_images):
                self.animation_frame = 0
            self.image = direction_images[self.animation_frame]
            self.last_animation_time = time.time()


    def take_damage(self, knockback_dir):
        damage = 10
        self.health -= damage
        if self.health < 0:
            self.health = 0
            self.dead = True
            self.dead_timer = time.time()

        self.last_hit_time = time.time()

        # 넉백 설정 - 3번 맞으면 넉백
        self.knockback_timer = time.time()
        self.knockback_direction = knockback_dir
        self.knockback_count += 1
        if self.knockback_count >= 5:
            self.knockback = True
            self.health -= 30
            self.knockback_count = 0

    def draw_health_bar(self):
        pygame.draw.rect(screen, RED, (self.rect.centerx - self.health_bar_length // 2, self.rect.top - 10, self.health_bar_length, 5))
        pygame.draw.rect(screen, GREEN, (self.rect.centerx - self.health_bar_length // 2, self.rect.top - 10, self.health_bar_length * (self.health / self.max_health), 5))
        
    def ranged_attack(self, projectiles_group, player):
        # 부채꼴 공격: 중심 각도를 주인공 방향으로 설정
        num_projectiles = 4  # 서적 개수
        spread_angle = math.pi / 2  # 부채꼴 각도 (45도)
        angle_step = spread_angle / (num_projectiles - 1)  # 각 서적 간 각도 차이

        # 주인공 방향 계산
        dx = player.rect_man.centerx - self.rect.centerx
        dy = player.rect_man.centery - self.rect.centery
        base_angle = math.atan2(dy, dx)  # 중심 각도 (주인공 방향)

        for i in range(num_projectiles):
            # 각 서적의 각도 계산
            angle = base_angle - (spread_angle / 2) + (i * angle_step)
            dx = math.cos(angle)  # x 축 방향
            dy = math.sin(angle)  # y 축 방향

            # 투사체 생성
            projectile = Projectile(
                self.rect.centerx,
                self.rect.centery,
                dx,
                dy,
                4,  # 속도
                "book.png"
            )
            projectiles_group.add(projectile)

    def drop_assignments(self, falling_objects_group):
    # 피사체 개수와 간격 설정
        num_objects = 4  # 피사체 개수
        spacing = SCREEN_WIDTH // num_objects  # 간격 계산

        for i in range(num_objects):
            x = i * spacing + spacing // 2  # 간격에 따라 위치 설정
            falling_object = FallingObject(x, -50, 5, "assignment.png")
            falling_objects_group.add(falling_object)

class SpeechBubble: # 말풍선 출력
    def __init__(self, cult_member, message):
        self.cult_member = cult_member
        self.message = message
        self.start_time = time.time()
        self.duration = 1.5  # 말풍선 표시 시간 (초)

    def draw(self):
        if time.time() - self.start_time <= self.duration:
            # 말풍선 크기와 위치 설정
            bubble_width = 300
            bubble_height = 30
            bubble_rect = pygame.Rect(0, 0, bubble_width, bubble_height)
            bubble_rect.midbottom = (self.cult_member.rect.centerx, self.cult_member.rect.top - 15)

            # 말풍선이 화면 밖으로 나가지 않도록 조정
            if bubble_rect.left < 0:
                bubble_rect.left = 0
            if bubble_rect.right > SCREEN_WIDTH:
                bubble_rect.right = SCREEN_WIDTH
            if bubble_rect.top < 0:
                bubble_rect.top = 0

            # 말풍선 디자인 (둥근 사각형)
            pygame.draw.rect(screen, WHITE, bubble_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, bubble_rect, 2, border_radius=10)

            # 텍스트 렌더링
            text_surface = font.render(self.message, True, BLACK)
            text_rect = text_surface.get_rect(center=bubble_rect.center)
            screen.blit(text_surface, text_rect)

            return True
        return False

#전역 변수
projectiles = pygame.sprite.Group() #보스 스테이지 전용
falling_objects = pygame.sprite.Group()

kakaotalks = pygame.sprite.Group()
teammates = pygame.sprite.Group()

defeated_enemies = 0
last_ranged_attack = time.time()
last_falling_attack = time.time()
start_index = 0

def game_play():
    pygame.init() # 기본 설정
    pygame.display.set_caption("교수님! 과제가 너무 많아요!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    bg1_image = pygame.image.load("bg1.png")
    bg2_image = pygame.image.load("bg2.png")
    loading1_image = pygame.image.load("loading1.png")
    loading2_image = pygame.image.load("loading2.png")
    loading3_image = pygame.image.load("loading3.png")
    loading4_image = pygame.image.load("Bossloading.png")
    loading5_image = pygame.image.load("CLEAR.png")
    player = Player(150, 250)
    # 음악 재생 (무한 반복: loops=-1)
    pygame.mixer.music.play(loops=-1)

    def draw_bg(num): # 배경 출력 함수
        if num == 1:
            scale_bg = pygame.transform.scale(bg1_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 2:
            scale_bg = pygame.transform.scale(bg2_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 3:
            scale_bg = pygame.transform.scale(loading1_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 4:
            scale_bg = pygame.transform.scale(loading2_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 5:
            scale_bg = pygame.transform.scale(loading3_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 6:
            scale_bg = pygame.transform.scale(loading4_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])
        if num == 7:
            scale_bg = pygame.transform.scale(loading5_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scale_bg, [0, 0])

    cult_members = pygame.sprite.Group() # 적 배치
    for _ in range(3):
        cult_member = CultMember(
            random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)
        )
        cult_members.add(cult_member)

    teammates = pygame.sprite.Group() # 적2 배치
    for _ in range(3):
        teammate = Teammate(
            random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)
        )
        teammates.add(teammate)

    professors = pygame.sprite.Group() # 보스 적배치
    professor = Boss( 
        random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)
    )
    professors.add(professor)

    bubbles = [] # 말풍선
    clock = pygame.time.Clock()

    def stage1():
        global defeated_enemies, start_index
        draw_bg(1)
        # 말풍선 생성
        if len(cult_members) > 0 and random.random() < 0.01:  # cult_members가 비어 있지 않으면 (이거 없으면 적 다 죽였을때 오류남)
                target = random.choice(cult_members.sprites())
                message = random.choice(["설문조사 부탁드려용~ㅎ", "잠깐 시간 가능하세용?", "무료 상담 해드립니다^&^"])
                bubbles.append(SpeechBubble(target, message))

        # 말풍선 업데이트
        for bubble in bubbles[:]:
            if not bubble.draw():
                bubbles.remove(bubble)

        for cult_member in cult_members: # 적 출력
            cult_member.move()
            cult_member.regenerate_health()
            cult_member.draw_health_bar()

        for cult_member in list(cult_members):
            cult_member.move()
            cult_member.regenerate_health()
            cult_member.draw_health_bar()

            # 체력이 0 이하인 적 제거
            if cult_member.health <= 0:
                cult_members.remove(cult_member)
                defeated_enemies += 1  # 처치한 적 수 증가
                print(f"처치한 적의 수: {defeated_enemies}")  # 출력
                if defeated_enemies >= 3:  # 3명 이상 처치 시
                    start_index = 2
                    defeated_enemies = 0
                    player.x, player.y = 150, 250

        # 남아있는 적 화면에 그리기
        cult_members.draw(screen)
    def stage2():
        global defeated_enemies, start_index, kakaotalks
        draw_bg(1)
        # 말풍선 생성
        if len(teammates) > 0 and random.random() < 0.01:  # teammates가 비어 있지 않으면 (이거 없으면 적 다 죽였을때 오류남)
                target = random.choice(teammates.sprites())
                message = random.choice(["제가 시간이 없네요.. ㅋ", "제가 이걸 꼭 해야 되요?", "무임승차 개꿀~"])
                bubbles.append(SpeechBubble(target, message))

        # 말풍선 업데이트
        for bubble in bubbles[:]:
            if not bubble.draw():
                bubbles.remove(bubble)

        for teammate in teammates:
            teammate.move()
            teammate.regenerate_health()
            teammate.draw_health_bar()

        for teammate in list(teammates):
            teammate.move()
            teammate.regenerate_health()
            teammate.draw_health_bar()

            # 체력이 0 이하인 적 제거
            if teammate.health <= 0:
                teammates.remove(teammate)
                defeated_enemies += 1  # 처치한 적 수 증가
                print(f"처치한 적의 수: {defeated_enemies}")  # 출력
                if defeated_enemies >= 3:  # 3명 이상 처치 시 CLEAR 출력
                    print("CLEAR")
                    start_index = 4
                    defeated_enemies = 0

        # Cult members shoot kakaotalks
        for teammate in teammates:
            teammate.shoot(kakaotalks)
                    
         # Update kakaotalks
        kakaotalks.update()

        # Check collision between player and kakaotalks
        for kakaotalk in kakaotalks:
            if kakaotalk.rect.colliderect(player.rect_man):
                player.hit_by_kakaotalk()
                kakaotalk.kill()
                
        kakaotalks.draw(screen)

        # 남아있는 적 화면에 그리기
        teammates.draw(screen)
    def stageboss():
        global defeated_enemies, last_ranged_attack, last_falling_attack, projectiles, falling_objects, start_index
        current_time = time.time()

        draw_bg(2)
        # 말풍선 생성
        if len(professors) > 0 and random.random() < 0.01:  # 무작위 확률로 말풍선 나오게 하기 #보스 말풍선
            target = random.choice(professors.sprites())
            message = random.choice(["과제를 내도록 하겠습니다.", "이렇게 과제를 하면 F입니다.", "충분히 할만한 과제의 양입니다."])
            bubbles.append(SpeechBubble(target, message))

        # 말풍선 업뎃
        for bubble in bubbles[:]:
            if not bubble.draw():
                bubbles.remove(bubble)

        for professor in list(professors):
            professor.move()
            professor.draw_health_bar()

            if current_time - last_ranged_attack > 5:
                professor.ranged_attack(projectiles, player)
                last_ranged_attack = current_time

            if current_time - last_falling_attack > 10:
                professor.drop_assignments(falling_objects)
                last_falling_attack = current_time

            if professor.health <= 0:
                professors.remove(professor)
                defeated_enemies += 1
                if defeated_enemies >= 1:
                    print("CLEAR")
                    start_index = 7
                    defeated_enemies = 0
                    
        projectiles.update()
        falling_objects.update()

        player.handle_projectile_hit(projectiles)
        player.handle_falling_object_hit(falling_objects)

        projectiles.draw(screen)
        falling_objects.draw(screen)
        professors.draw(screen)
    def loading(num): #비효율적인 코드지만 해결 방법이 없어서 이대로 놔둔 코드
        global start_index

        # 시작 시간 저장
        start_time = pygame.time.get_ticks() / 1000  # 밀리초를 초로 변환

        running = True
        while running:
            draw_bg(num)

            # 현재 시간 계산
            current_time = pygame.time.get_ticks() / 1000
            if current_time - start_time >= 5:  # 5초가 지났는지 확인
                start_index += 1
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)


    while True:
        if start_index == 0:
            loading(3)
        if start_index == 1: 
            stage1()
        if start_index == 2:
            loading(4)
        if start_index == 3:
            stage2()
        if start_index == 4:
            loading(5)
        if start_index == 5:
            loading(6)
        if start_index == 6:
            stageboss()
        if start_index == 7:
            loading(7)
        if start_index == 8:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        for event in pygame.event.get(): # 종류 코드
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: #키를 누른다면 작동 공격과 피격
                if event.key == pygame.K_z and not player.attacking:
                    if start_index == 1: 
                        player.attack(screen, cult_members) #피격 대상 설정
                    elif start_index == 3:
                        player.attack(screen, teammates)
                    elif start_index == 6:
                        player.attack(screen, professors)
                if event.key == pygame.K_x and not player.damaging: #데미지 테스트를 위한 코드
                    player.get_hit()
            if event.type == pygame.USEREVENT + 1:  # 이동속도 복구
                player.reset_slow()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            if event.type == pygame.USEREVENT + 2:  # 스턴 복구
                player.reset_stun()
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)

        keys = pygame.key.get_pressed()
        key_pressed = player.move(keys) #애니매이션 적용 위해 필요

        if player.damaging: #데미지 받으면 넉백
            player.damage_jump()

        player.animation_frame(key_pressed)

        player.draw(screen)

        # 적 상태 업데이트 및 제거
        player.draw_HP()
        if player.HP <= 0:
            game_end()

        pygame.display.flip()
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