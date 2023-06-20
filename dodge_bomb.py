import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
accs = [a for a in range(1, 11)]

def check_bound(rect:pg.Rect) -> tuple[bool,bool]:
    yoko,tate = True,True
    if rect.left<0 or WIDTH<rect.right: 
        yoko = False
    if rect.top<0 or HEIGHT<rect.bottom:
        tate=False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kl_img = pg.image.load("ex02/fig/8.png")
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kf_img =  pg.transform.flip(kk_img, True, False)
    kl_img = pg.transform.rotozoom(kl_img, 0, 2.0)
    clock = pg.time.Clock()
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey([0,0,0])
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    bd_rct = bd_img.get_rect()
    bd_rct.center = x,y
    bd_imgs=[]
    for r in range(1, 11):
        bd_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bd_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bd_img.set_colorkey([0,0,0])
        bd_imgs.append(bd_img)
    vx, vy = 5,5

#移動方向に応じてキャラの角度を変更
    kk_img_dic = {
    (0,-5):  pg.transform.rotozoom(kf_img, 90, 1.0),
    (5,-5):  pg.transform.rotozoom(kf_img, 45, 1.0),
    (5,0):  pg.transform.rotozoom(kf_img, 0, 1.0),
    (5,5):  pg.transform.rotozoom(kf_img, 315, 1.0),
    (0,5):  pg.transform.rotozoom(kf_img, 270, 1.0),
    (-5,5):  pg.transform.rotozoom(kk_img, 45, 1.0),
    (-5,0):  pg.transform.rotozoom(kk_img, 0, 1.0),
    (-5,-5):  pg.transform.rotozoom(kk_img, 315, 1.0),
    (0,0):kk_img
}
    tmr = 0
    lose = False
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bd_rct):  # 練習５
            lose = True
            screen.blit(kl_img, [100,100])
            pg.time.wait(1000)
            print("ゲームオーバー")
            return   # ゲームオーバー 
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):#壁の衝突
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)] #時間とともに加速
        bd_img = bd_imgs[min(tmr//500, 9)] #時間とともに拡大
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img_dic[sum_mv[0],sum_mv[1]], kk_rct)
        bd_rct.move_ip(avx,avy)#加速度に合わせて移動
        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向に画面外だったら
            vx *= -1
        if not tate:  # 縦方向に範囲外だったら
            vy *= -1
        screen.blit(bd_img,bd_rct)
        
        pg.display.update()
        tmr += 1
        print(tmr)
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()