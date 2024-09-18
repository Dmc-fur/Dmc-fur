import pgzrun
import pygame
import random
import math
import os
import time

# 定义游戏相关属性
TITLE = '回来吧牢羊' 
WIDTH = 600
HEIGHT = 720

# 自定义游戏常量
T_WIDTH = 60
T_HEIGHT = 66
# 下方牌堆的位置
DOCK = Rect((90, 564), (T_WIDTH*7, T_HEIGHT))

# 上方的所有牌
tiles = []
# 牌堆里的牌
docks = []

# 游戏状态
game_state = 'start'  # 初始状态为开始页面

# 定义按钮
start_button = Rect((WIDTH // 2 - 75, HEIGHT // 2 - 37), (150, 75))
mute_button = Rect((WIDTH - 100, 20), (80, 40))
leaderboard_button = Rect((WIDTH // 2 - 75, HEIGHT // 2 + 50), (150, 75))
return_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 100))

# 静音状态
is_muted = False

# 计时器
start_time = None
time_limit = 301  # 5分钟

# 排行榜
leaderboard = []
completion_times = []
completion_time = 0

music.play('misty memoty_piano version')

import random

def install():
    global tiles,docks
    tiles = []
    docks = []  #之前因为docks未在此处初始化，导致重新游玩时会直接进入失败界面

    # 初始化牌组，12*12张牌随机打乱
    ts = list(range(1, 13)) * 12
    random.shuffle(ts)
    n = 0

    for k in range(7):  # 7层
        for i in range(7 - k):  # 每层减1行
            for j in range(7 - k):
                t = ts[n]  # 获取排种类
                n += 1
                tile = Actor(f'tile{t}')  # 使用tileX图片创建Actor对象
                tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9  # 设定位置
                tile.tag = t  # 记录种类
                tile.layer = k  # 记录层级
                tile.status = 1 if k == 6 else 0  # 除了最顶层，状态都设置为0（不可点）这里是个简化实现
                tiles.append(tile)
    
    for i in range(4):  # 剩余的4张牌放下面（保证通关并给予容错）
        t = ts[n]
        n += 1
        tile = Actor(f'tile{t}')
        tile.pos = 210 + i * tile.width, 516
        tile.tag = t
        tile.layer = 0
        tile.status = 1
        tiles.append(tile)


def reset_game():
    global game_state, start_time
    install()
    game_state = 'start'
    start_time = None




# 游戏帧绘制函数
def draw():
    screen.clear()
    if game_state == 'start':
        screen.blit('start_screen', (0, 0))  # 绘制开始页面背景
        screen.draw.filled_rect(start_button, 'white')  # 绘制按钮背景
        screen.draw.text('START', center=start_button.center, color='black')  # 绘制按钮文字
        screen.draw.filled_rect(mute_button, 'white')  # 绘制静音按钮背景
        screen.draw.text('MUTE' if not is_muted else 'UNMUTE', center=mute_button.center, color='black')  # 绘制静音按钮文字
        screen.draw.filled_rect(leaderboard_button, 'white')  # 绘制排行榜按钮背景
        screen.draw.text('LEADERBOARD', center=leaderboard_button.center, color='black')  # 绘制排行榜按钮文字
    
    elif game_state == 'playing':
        screen.blit('back', (0, 0))      #背景图

        undo_button = Rect((WIDTH - 100, HEIGHT - 50), (80, 30))    #撤销按钮
        screen.draw.filled_rect(undo_button, 'white')
        screen.draw.text('REMOVE', center=undo_button.center, color='gray')

        for tile in tiles:
            #绘制上方牌组
            tile.draw()
            if tile.status == 0:
                screen.blit('mask', tile.topleft)     #给不可点击的块添加遮罩
        for i, tile in enumerate(docks):
            #绘制排队，先调整一下位置（因为可能有牌被消掉）
            tile.left = (DOCK.x + i * T_WIDTH)
            tile.top = DOCK.y
            tile.draw()

        # 绘制计时器
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        screen.draw.text(f'Time: {int(remaining_time)}', (25, 25), color='red', fontsize=32)#fontsize是字体大小参数

        # 超过7张，失败
        if len(docks) >= 7 or remaining_time <= 0:
            screen.blit('gameover', (0, 0))
            screen.draw.filled_rect(return_button, 'white')  # 绘制返回按钮背景
            screen.draw.text('Click twice to return', center=return_button.center, color='black')  # 绘制返回按钮文字
    
    elif game_state == 'victory':
        screen.blit('win', (0, 0))
        screen.draw.filled_rect(return_button, 'white')  # 绘制返回按钮背景
        screen.draw.text('Congrets!!\nClick twice to return', center=return_button.center, color='blue')

    elif game_state == 'leaderboard':   #可以显示从小到大排序的历史记录表，记录玩家的最快速度
        screen.clear()
        screen.draw.text('Leaderboard', (WIDTH // 2 - 75, 50), color='white', fontsize=40)
        for i, record in enumerate(sorted(completion_times)):
            screen.draw.text(f'{i + 1}. {record:.2f} seconds', (WIDTH // 2 - 75, 100 + i * 30), color='white',fontsize=30)
        screen.draw.filled_rect(return_button, 'white')  # 绘制返回按钮背景
        screen.draw.text('RETURN', center=return_button.center, color='black')  # 绘制返回按钮文字
        screen.draw.text




def update_timer(): ##实现计时器功能
    global game_state
    if game_state == 'playing':
        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)
        if remaining_time <= 0:
            game_state = 'gameover'
clock.schedule_interval(update_timer, 1.0)  # 每1.0秒调用一次 update_timer




#       实现撤销上一个操作的功能
# 初始化一个变量来存储被移除的元素
last_removed_tiles = None

#flag = 0

def remove_tile(tile):  #储存
    global last_removed_tile, last_removed_tile_pos,last_below_tile
    #global flag

    #flag = 1

    last_removed_tile = tile
    last_removed_tile_pos = tile.pos

    #for below_tile in tiles:
    #    if below_tile.layer == tile.layer - 1 and below_tile.collidepoint(tile.pos):
    #        last_below_tile[flag] = below_tile
    #        flag = flag+1
    #        below_tile.status = 1  # 设置为可点击


    #tiles.remove(tile)
    #docks.append(tile)

def restore_last_removed_tile():    #恢复
    global last_removed_tile, last_removed_tile_pos,last_below_tile,flag
    if last_removed_tile:
        docks.remove(last_removed_tile)
        last_removed_tile.pos = last_removed_tile_pos
        last_removed_tile.status = 1    #保证上一个移除的元素返回后可以点击
        tiles.append(last_removed_tile)
        #while flag>0:
        #    last_below_tile[flag].status = 0  # 设置为不可点击
        #    flag = flag -1
        last_removed_tile = None
        last_removed_tile_pos = None
        last_below_tile = None





def on_mouse_down(pos):
    global docks, game_state, is_muted, start_time
    
    if game_state == 'start':
        if start_button.collidepoint(pos):
            reset_game()
            game_state = 'playing'  # 点击开始按钮时，进入游戏
            start_time = time.time()  # 开始计时
        elif mute_button.collidepoint(pos):
            is_muted = not is_muted
            if is_muted:
                music.pause()
            else:
                music.unpause()
        elif leaderboard_button.collidepoint(pos):
            game_state = 'leaderboard'
        return
    
    elif game_state == 'playing':

        game_state = 'victory'  #调试用
        

        undo_button = Rect((WIDTH - 100, HEIGHT - 50), (80, 30))



        if undo_button.collidepoint(pos):   #加入撤销功能
            restore_last_removed_tile()
            
        elif len(tiles) == 0:  # 游戏结束，成功
            game_state == 'victory'
            return
        elif len(docks) >= 7:   ##游戏失败.  remaining_time<=0的情况不需要考虑，因为每时每刻都在自动更新
            game_state = 'gameover'
            return
        
        for tile in reversed(tiles):  # 逆序循环是为了先判断上方的牌，如果点击了就直接跳出，避免重复判定
            if tile.status == 1 and tile.collidepoint(pos):
                # 状态1可点，并且鼠标在范围内
                tile.status = 2
                tiles.remove(tile)
                diff = [t for t in docks if t.tag != tile.tag]  # 获取牌堆内不相同的牌
                if len(docks) - len(diff) < 2:  # 如果相同的牌数量<2，就加进牌堆
                    remove_tile(tile)   #储存这个加进牌堆的东西
                    docks.append(tile)
                else:  # 否则用不相同的牌替换牌堆（即消除相同的牌）
                    #remove_tile(None)   #因为发生了消去操作，所以不允许返回？但这个代码会导致消去时程序崩溃，因而消去时不能按返回按键
                    docks = diff
                for down in tiles:  # 遍历所有的牌
                    if down.layer == tile.layer - 1 and down.colliderect(tile):  # 如果在此牌的下一层，并且有重叠
                        for up in tiles:  # 那就再反过来判断这种被覆盖的牌，是否还有其他牌覆盖它
                            if up.layer == down.layer + 1 and up.colliderect(down):  # 如果有就跳出
                                break
                        else:  # 如果全都没有，说明它变成了可点状态
                            down.status = 1
                return
            
    elif game_state == 'leaderboard':
        if return_button.collidepoint(pos):
            game_state = 'start'
    elif game_state == 'gameover':
        if pos: #这里不知道为什么要点击两次才能返回，于是直接把判定范围改成了全屏，这样点按两次也能够自然返回
            reset_game()
    elif game_state == 'victory':
        completion_time = time.time() - start_time
        completion_times.append(completion_time)
        if pos:
            reset_game()


pgzrun.go()
