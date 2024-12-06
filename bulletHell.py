  
""" platformer """

import pygame, simpleGE, random


class Bullet(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("bullet.png")
        self.setSize(25,25)
        self.reset()
        
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(5,8)
        self.dx = random.randint(-4,8)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class LblHealth(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Health: 3"
        self.center = (320, 30)

class Player(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.walkAnim = simpleGE.SpriteSheet("characterWalk.png", (64, 64), 4, 9, 0.1)
        self.walkAnim.startCol = 1
        self.animRow = 2
        self.moveSpeed = 2
        self.position = (50, 400)
        self.setSize(30, 30)
        self.inAir = True
        self.health = 3
    def process(self):
        walking = False
        
        if self.y > 450:
            self.inAir = False
            self.y = 450
            self.dy = 0 
        
        if self.inAir:
            self.addForce(.2, 270)
        
        if self.scene.isKeyPressed(pygame.K_UP):
            self.animRow = 8
            walking = True
            if not self.inAir:
                self.addForce(6, 90)
                self.inAir = True
                
        if self.isKeyPressed(pygame.K_LEFT):
            self.animRow = 9
            self.x -= 5
            walking = True
        if self.isKeyPressed(pygame.K_RIGHT):
            self.animRow = 11 
            self.x += 5
            walking = True

        if walking:        
            self.copyImage(self.walkAnim.getNext(self.animRow))
        else:
            self.copyImage(self.walkAnim.getCellImage(0, self.animRow))
            
        self.inAir = True
        for platform in self.scene.platforms:
            if self.collidesWith(platform):                
                if self.dy > 0:
                        self.bottom = platform.top
                        self.dy = 0
                        self.inAir = False

        
class Platform(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.colorRect("#FF000000", (250, 45))
       
    def update(self):
        super().update()
        
            
class Block(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.setImage("blocks.png")
        self.setSize(250, 45)
        



class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center = (500, 30)
        
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)



class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("mountain.jpg")
        
        self.lblScore = LblScore()
        self.lblTime = LblTime()
        self.lblHealth = LblHealth()  
        self.score = 0
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 40
        self.bulletSound = simpleGE.Sound("explosion.wav")
        
        self.player = Player(self)
        self.bullet = []
        self.numBullets = 15
        for i in range(self.numBullets):
            self.bullet.append(Bullet(self))
            
        self.platforms = [Platform(self, (330, 360)),
                          Platform(self, (330, 130)),
                          Platform(self, (30, 245)),
                          Platform(self, (590, 245)),
                          Platform(self, (100, 470)),
                          Platform(self, (360, 470)),
                          Platform(self, (630, 470))]
        
        self.blocks = [Block(self, (330, 360)),
                       Block(self, (330, 130)),
                       Block(self, (30, 245)),
                       Block(self, (590, 245)),
                       Block(self, (100, 470)),
                       Block(self, (350, 470)),
                       Block(self, (600, 470))]
        
        self.sprites = [self.platforms,
                        self.bullet,
                        self.lblTime,
                        self.lblScore,
                        self.lblHealth,  
                        self.player,
                        self.blocks]

    def process(self):
        for bullet in self.bullet:
            if self.player.collidesWith(bullet):
                self.bulletSound.play()
                bullet.reset()
                self.player.health -= 1  
                self.lblHealth.text = f"Health: {self.player.health}"  
                if self.player.health <= 0:  
                    self.stop()

        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            self.stop()
        
        if self.timer.getTimeLeft() > 0:
            self.score += 1
            self.lblScore.text = f"Score: {self.score}"
            
        
            
        
  
            
            
class Instructions(simpleGE.Scene):
    def __init__(self, score):
        super().__init__()
        self.setImage("startScreen.jpg")
        
        self.response = "Play"
        
        self.instructions = simpleGE.MultiLabel()
        self.instructions.textLines = [
        "Your Goal Is To Avoid The Bullets.",
        "Move with the left, right and up arrow keys",
        "Survival is the Name",
        "Who Can Get The Highest Score",
        " ",
        "Good Luck!"]
        
        self.instructions.center = (320, 240)
        self.instructions.size = (500, 250)
        self.instructions.bgColor = ("#FF000000")
        
        self.prevScore = score
        self.lblScore = simpleGE.Label()
        self.lblScore.text = f"Last score: {self.prevScore}"
        self.lblScore.center = (320, 400)
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play (up)"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit (down)"
        self.btnQuit.center = (550, 400)
        
        self.sprites = [self.instructions,
                        self.lblScore,
                        self.btnQuit,
                        self.btnPlay]
        
    def process(self):
        
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()

        
        if self.isKeyPressed(pygame.K_UP):
            self.response = "Play"
            self.stop()
        if self.isKeyPressed(pygame.K_DOWN):
            self.response = "Quit"
            self.stop()

def main():
    keepGoing = True
    score = 0
    while keepGoing:
        
        instructions = Instructions(score)
        instructions.start()
                
        if instructions.response == "Play":    
            game = Game()
            game.start()
            score = game.score
        else:
            keepGoing = False
            
            
if __name__ == "__main__":
    main()            
              
            
