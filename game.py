import argparse
from copy import copy
from time import sleep, time

import functions
from MachineLearning.Event import Event
from MachineLearning.RandomGamePlayer import RandomGamePlayer
from MachineLearning.RobotGamePlayer import RobotGamePlayer
from MachineLearning.TruthHandler import Recorder
from hazards import *
from scoring import *

parser = argparse.ArgumentParser()
parser.add_argument('--human', action='store_true')
parser.add_argument('--random', action='store_true')
parser.add_argument('--robot', action='store_true')
parser.add_argument('--skip-frames', default=1)
parser.add_argument('--asteroid-count', default=1)
args = parser.parse_args()

threads = []


def playth(sound):
    th = play(sound)
    threads.append(th)


def getAsteroidFromWormhole(white, screenX, screenY):
    mod = 50
    playth("bloop.wav")
    return functions.Asteroid(asteroidImg, screen, random.randint(white.centerX() - mod, white.centerX() + mod),
                              random.randint(white.centerY() - mod, white.centerY() + mod), screenX, screenY, x)


def getAsteroid(screenX, screenY):
    mod = 50
    x = random.randint(-mod, screenX)
    if x > 0:
        return functions.Asteroid(asteroidImg, screen, x, -10, screenX, screenY, x)
    else:
        return functions.Asteroid(asteroidImg, screen, x, random.randint(mod, screenY - mod), screenX, screenY, x)


pygame.init()


def goMenu():
    ############################################
    #        Main Menu
    ############################################
    background_img = pygame.image.load(backgroundImg).convert()
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    spriteGroup = pygame.sprite.Group()
    bimages = [["Hazards/buttons/ib%r.png" % r, "Hazards/buttons/b%r.png" % r] for r in range(1, 7)]
    gamemenu = menu([button(bimages[r], (screenX / 2) - 90, (60 + r * 90)) for r in range(len(bimages))])
    for but in gamemenu.buttonList:
        spriteGroup.add(but)
    pickedMode = True
    gamemenu.bindex = 0
    while not pickedMode:
        spriteGroup.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    gamemenu.revChange()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    gamemenu.change()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    pickedMode = True
            if event.type == pygame.QUIT:
                del background_img
                pygame.display.quit()
                exit(0)
        screen.blit(background_img, (0, 0))
        spriteGroup.draw(screen)
        pygame.display.flip()
    spriteGroup.empty()
    level = gamemenu.bindex + 1
    if level == 6:
        del background_img
        pygame.display.quit()
        exit(0)
    astBool = level == 1 or level == 2 or level == 4 or level == 5
    lazBool = level == 2 or level == 5 or level == 3
    wormBool = level == 5 or level == 4 or level == 3
    return spriteGroup, level, astBool, lazBool, wormBool
    ###########################################


backgroundImg = "stars.png"
spriteImgList = ["ufo/uforotate/ufo{}.png".format(r * 5) for r in range(int(90 / 5))]
spriteImgList.append("ufo/ufodeadsm.png")
asteroidImg = ["Hazards/asteroids/asteroid.png"]
lazerlist = []
shieldImgList = ["ufo/uforotate/ufoshield%r.png" % (r * 5) for r in range(int(90 / 5))]
lazersounds = ["lazers/base laser%s" % s for s in [".wav", "+1.1.wav", "+4.1.wav", "+6.2.wav"]]
blackHoleSprites = ["Hazards/wormholes/black%r.png" % (r * 5) for r in range(int(360 / 5))]
whiteHoleSprites = [im for im in reversed(blackHoleSprites)]

score = 0
screenSizeMult = 1.25
screenX = int(640 * screenSizeMult)
screenY = int(480 * screenSizeMult)
# screenX = 320
# screenY = 240
screen = pygame.display.set_mode((screenX, screenY), 0, 32)
pygame.display.set_caption("UFO Battle")

level = 0

astBool = False
lazBool = False
wormBool = False
old_ufo = None
old_asteroids = None

spriteGroup, level, astBool, lazBool, wormBool = goMenu()

riffPlayed = False
sleep(.5)
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
            spriteImgList = ["psprite.png", "psprite.png", "ufo/ufodeadsm.png"]
            asteroidImg = ["sad2.png"]
            shieldImgList = ["pspriteshield.png" for n in range(len(spriteImgList))]
            backgroundImg = "altBackground.jpg"
            play("happy.wav")
            riffPlayed = True

if not riffPlayed:
    play("riff.wav")

total_frames = 0
scores = []
while True:
    # print("Starting game")
    # print(score)

    background_img = pygame.image.load(backgroundImg).convert()
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    count = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    #    font = pygame.font.Font("impact.ttf", 20)

    # set up sprites
    ufo = functions.Projectile(spriteImgList, screen, screenX / 2, screenY / 2, screenX, screenY)
    ufo.getShieldSprites(shieldImgList)
    if astBool:
        asteroids = [
            functions.Asteroid(asteroidImg, screen, random.randint(50, screenX - 50), random.randint(50, screenY - 50),
                               screenX, screenY, x) for x in range(int(args.asteroid_count))]
    else:
        asteroids = []
    spriteGroup.add(ufo)
    #    spriteGroup = pygame.sprite.Group(cat)
    for a in asteroids:
        spriteGroup.add(a)

    L = False
    R = False
    U = False
    D = False
    collisionCount = 0
    lose = False
    skip = False

    lazerthresh = 400
    asteroidthresh = 1000
    gameRestart = False

    ################### Initialize startup shield
    ufo.shields = 3
    ufo.shielded = 0

    timemult = 1000
    framerate = 90
    beginningTime = time()
    endTime = beginningTime
    oldTime = time()

    highScore = getHighScore(level - 1)
    ###################################################################################
    ########### MAIN GAME LOOP BEGINS AFTER THIS LINE OF #################'s
    ######################################################################
    score = 0

    if wormBool:
        holeMag = .2
        black = blackhole(blackHoleSprites, 100, 100, 90, 90, holeMag)
        white = blackhole(whiteHoleSprites, 600, 400, 90, 90, -holeMag)
        spriteGroup.add(black)
        spriteGroup.add(white)
        worm = wormhole(black, white)
        wormholes = [worm]
    else:
        wormholes = []

    total_frames = 0
    while True:
        # fix framerate
        newtime = time()
        #    print newtime-oldTime
        if (newtime - oldTime) < (1.0 / framerate):
            if args.human:
                continue
        else:
            oldTime = newtime
        keys = pygame.key.get_pressed()
        #    cat.acc = functions.vector(0,0)
        if not args.human:
            L = False
            U = False
            D = False
            R = False

        #projectiles = copy(asteroids)
        #projectiles.append(ufo)
        #gamestate = Recorder.get_game_state(projectiles)
        gamestate = Recorder.get_grid_game_state(ufo, asteroids, screenX, screenY)
        old_ufo = copy(ufo)
        old_asteroids = copy(asteroids)

        if args.human:
            eventsource = pygame.event.get()
        if args.robot:
            eventsource = RobotGamePlayer.get(gamestate)
        if args.random:
            eventsource = RandomGamePlayer.get(gamestate)

        if not lose:
            total_frames += 1

        for event in eventsource:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    L = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    R = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    U = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    D = True
                if event.key == pygame.K_RCTRL or event.key == pygame.K_e:
                    threads.append(ufo.startShield())
                if event.key == pygame.K_SPACE:
                    lose = False
                    for thread in threads:
                        thread.join()
                    gameRestart = True
                if event.key == pygame.K_m:
                    spriteGroup, level, astBool, lazBool, wormBool = goMenu()
                    gameRestart = True
            if args.human:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        L = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        R = False
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        U = False
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        D = False
            if event.type == pygame.QUIT:
                if score > getHighScore(level - 1):
                    setHighScore(score, level - 1)
                del background_img
                for thread in threads:
                    thread.join()
                pygame.display.quit()
                exit(0)
                ################################
        if gameRestart:
            break
        ################################

        vel = .5
        if L:
            ufo.state[0, 1] = -vel
        elif R:
            ufo.state[0, 1] = vel
        else:
            ufo.state[0, 1] = 0
        if U:
            ufo.state[1, 1] = -vel
        elif D:
            ufo.state[1, 1] = vel
        else:
            ufo.state[1, 1] = 0
        #accel = .13
        #if ufo.speed() < ufo.maxSpeed / 1.5:
        #    if L:
        #        ufo.state[0, 2] = -accel
        #    if U:
        #        ufo.state[1, 2] = -accel
        #    if D:
        #        ufo.state[1, 2] = accel
        #    if R:
        #        ufo.state[0, 2] = accel
        #else:
        #    if L:
        #        ufo.state[0, 2] = -accel / 2.0
        #    if U:
        #        ufo.state[1, 2] = -accel / 2.0
        #    if D:
        #        ufo.state[1, 2] = accel / 2.0
        #    if R:
        #        ufo.state[0, 2] = accel / 2.0

            #####################################################
            #                   Black Hole Collisions
            #####################################################
        wormAffectDist = 150
        for worm in wormholes:
            if dist(ufo, worm.black.centerX(), worm.black.centerY()) < wormAffectDist:
                worm.black.alterAcc(ufo)
            if dist(ufo, worm.white.centerX(), worm.white.centerY()) < wormAffectDist:
                worm.white.alterAcc(ufo)
            if pygame.sprite.collide_rect(ufo, worm.black):
                threads.append(worm.teleport(worm.black, ufo))

                #####################################################
        spriteGroup.update()
        for a in asteroids:
            a.setAccX(0)
            a.setAccY(0)
            for worm in wormholes:
                if dist(a, worm.black.centerX(), worm.black.centerY()) < wormAffectDist:
                    worm.black.alterAcc(a)
                if dist(a, worm.white.centerX(), worm.white.centerY()) < wormAffectDist:
                    worm.white.alterAcc(a)
                if pygame.sprite.collide_rect(a, worm.black):
                    worm.teleport(worm.black, a)
            if a.debounce == 0:
                if pygame.sprite.collide_rect(ufo, a) and not lose:
                    a.reverse()
                    a.debounce = 30
                    collisionCount += 1
                    if not ufo.isShielded():
                        playth("explosion.wav")
                        lose = True
                        ufo.kill()
                for b in asteroids:
                    if b is not a:
                        if pygame.sprite.collide_rect(a, b):
                            #                            print "collision detected"
                            if a.colldebounce <= 0 or b.colldebounce <= 0:
                                tempX = a.getVelX()
                                tempY = a.getVelY()
                                a.setVelX(b.getVelX())
                                a.setVelY(b.getVelY())
                                b.setVelX(tempX + random.uniform(-.3, .3))
                                b.setVelY(tempY + random.uniform(-.3, .3))
        for l in lazerlist:
            if pygame.sprite.collide_rect(ufo, l) and not lose and not l.charging:
                if not ufo.isShielded():
                    lose = True
                    ufo.kill()
                    playth("explosion.wav")
                    print("u sploded")
            if not l.charging and not l.playedbzz:
                threads.append(l.playSound())
                if random.randint(0, 2) == 0 and l.adjs < 2:
                    laz = l.getAdjLazer("")
                    lazerlist.append(laz)
                    spriteGroup.add(laz)
                    threads.append(lazerlist[-1].playChSound())

        if score > asteroidthresh and astBool:
            asteroidthresh += 1000
            # if wormBool:
            #    asteroids.append(getAsteroidFromWormhole(wormholes[0].white, screenX, screenY))
            #    spriteGroup.add(asteroids[-1])
            # else:
            #    asteroids.append(getAsteroid(screenX, screenY))
            #    spriteGroup.add(asteroids[-1])

        if score > lazerthresh and lazBool:
            lazerthresh += 400
            borders = 30
            bordermod = 150
            if random.randint(0, 10) % 2 == 0:
                lazX = random.randint(int(ufo.X() - bordermod), int(ufo.X() + bordermod))
                if lazX < borders:
                    lazX = borders
                if lazX > screenX - borders:
                    lazX = borders
                laz = lazer(lazX, random.choice(lazersounds), 150)
            else:
                lazY = random.randint(int(ufo.Y() - bordermod), int(ufo.Y() + bordermod))
                if lazY < borders:
                    lazY = borders
                if lazY > screenY - borders:
                    lazY = borders
                laz = hlazer(lazY, random.choice(lazersounds), 150)
            lazerlist.append(laz)
            threads.append(laz.playChSound())
            spriteGroup.add(laz)

        screen.blit(background_img, (0, 0))

        score = total_frames
        scoreString = "Score: %r" % (score)
        highScoreString = "High Score: %r" % highScore
        if len(scores) > 0:
            average_score = sum(scores) / len(scores)
            averageScoreString = 'Average: {:.1f}'.format(average_score) + ' '
            lenScoreString = 'i: ' + str(len(scores)) + '  '
        else:
            averageScoreString = ''
            lenScoreString = ''
        lineLength = 90
        spacesString = "".join([" " for sp in range(
            lineLength - (len(scoreString) + len(lenScoreString) + len(averageScoreString) + len(highScoreString)))])
        scoreString = scoreString + spacesString + lenScoreString + averageScoreString + highScoreString
        colcount = font.render(scoreString, 1, (255, 255, 255))

        if not args.robot:
            if args.human:
                if L:
                    eventsource.append(Event.get_left())
                if R:
                    eventsource.append(Event.get_right())
                if U:
                    eventsource.append(Event.get_up())
                if D:
                    eventsource.append(Event.get_down())
            if len(eventsource) == 0:
                eventsource.append(Event.do_nothing())
            projectiles = copy(asteroids)
            projectiles.append(ufo)
            Recorder.record(ufo, asteroids, screenX, screenY, projectiles, eventsource, lose, args)

        if args.human and score > 10000:
            lose = True

        if lose:
            print(score)
            scores.append(score)
            average_score = sum(scores) / len(scores)
            print('Average: ' + str(average_score))
            if score > getHighScore(level - 1):
                colcount = font.render(
                    "HIGH SCORE! Score: %r          Press Spacebar to try again or M for the menu" % (score), 1,
                    (255, 255, 0))
            else:
                colcount = font.render(
                    "You lose! Score: %r          Press Spacebar to try again or M for the menu" % (score), 1,
                    (100, 100, 100))
            if True:  # not args.human:
                lose = False
                for thread in threads:
                    thread.join()
                gameRestart = True
                total_frames = 0
        else:
            endTime = time()

        if score % int(args.skip_frames) == 0 or lose:
            screen.blit(colcount, (5, 5))
            spriteGroup.draw(screen)
            pygame.display.flip()

    ######################################################## restarting game
    if score > getHighScore(level - 1):
        setHighScore(score, level - 1)
    score = 0
    lazerlist = []
    lose = False
    spriteGroup.empty()
