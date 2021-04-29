import pygame, numpy,sys #import libraries for program

class Snake():
    body = [] #stores the body parts
    moves={} #stores coords for changes in direction
    head = None #head
    x = 0 #x direction
    y = 0 #y direction
    pos =0 #position
    m_flag =0 #prevent movement to right if going left and viceversa
    u_flag =0 #prevent movement to up if going down and viceversa
    game_over = False #boolean to check if game is over
    
    def __init__(self, pos):
        self.head = Square(pos) #snake head
        self.body.append(self.head) #first square == head of snake/body
        self.x = 1 #direction of snake
        self.y = 0
        self.game_over = False #is it over?

    def paint(self): #draw the snake body
        for i,part in enumerate(self.body): #returns iterator and the object
            if i == 0: #head of snake
                part.paint(1)
            else: #body of the snake
                part.paint()

    def end_game(self): #announce game is over
        self.game_over = True

    def grow(self):
        x = self.body[-1].x #save current direction, otherwise body part separates
        y = self.body[-1].y
        #create a new body part for the snake, and check which direction it must go
        if self.body[-1].x == 1 and self.body[-1].y == 0: #snake moving R
            self.body.append(Square((self.body[-1].pos[0]-1,self.body[-1].pos[1]))) #place it one square before the (now) previous tail
        elif self.body[-1].x == -1 and self.body[-1].y == 0: #L
            self.body.append(Square((self.body[-1].pos[0]+1,self.body[-1].pos[1])))
        elif self.body[-1].x == 0 and self.body[-1].y == 1: #D
            self.body.append(Square((self.body[-1].pos[0],self.body[-1].pos[1]-1)))
        elif self.body[-1].x == 0 and self.body[-1].y == -1: #U
            self.body.append(Square((self.body[-1].pos[0],self.body[-1].pos[1]+1)))

        self.body[-1].x = x #give the direction it should go
        self.body[-1].y = y

    #Check which direction we should change to according to pressed key
    def change_dir(self,key):
        global use_head_ima
        if key == pygame.K_LEFT and self.m_flag ==0:
            # 180 
            use_head_ima = pygame.transform.rotate(head_ima, 180)
            self.x = -1 #change direction
            self.y = 0
            self.m_flag = 1 #restrict movement in the opposite direction
            self.u_flag = 0 #pos[0] == x, pos[1] ==y
            self.moves[self.head.pos[:]] = [self.x, self.y] #add move for all to follow e.g. current pos=> (2,0) = (0,-1)
        elif key == pygame.K_RIGHT and self.m_flag ==0:
            # 0
            use_head_ima = pygame.transform.rotate(head_ima, 0)
            self.x = 1
            self.y = 0
            self.m_flag =1
            self.u_flag = 0
            self.moves[self.head.pos[:]] = [self.x, self.y]
        elif key == pygame.K_UP and self.u_flag ==0:
            # 90
            use_head_ima = pygame.transform.rotate(head_ima, 90)
            self.x = 0
            self.y = -1
            self.u_flag = 1
            self.m_flag = 0
            self.moves[self.head.pos[:]] = [self.x, self.y]
        elif key == pygame.K_DOWN and self.u_flag ==0:
            #270
            use_head_ima = pygame.transform.rotate(head_ima, 270)
            self.x = 0
            self.y = 1
            self.u_flag =1
            self.m_flag = 0
            self.moves[self.head.pos[:]] = [self.x, self.y]
            
    def advance(self,speed):
        for count, body_part in enumerate(self.body): #check each part of the snake
            place = body_part.pos[:] #get part position
            if place in self.moves: #check if it is in the movement dict
                move = self.moves[place] #it is, then move the part in that direction
                body_part.move(move[0],move[1],speed)
                if count == len(self.body)-1:
                    popped=self.moves.pop(place)
            else: #check if it is hitting the end of the screen
                if body_part.x == -1 and body_part.pos[0] <= 0:
                    self.end_game()
                elif body_part.x == 1 and body_part.pos[0] >= ROWS-1:
                    self.end_game()
                elif body_part.y == 1 and body_part.pos[1] >= ROWS-1:
                    self.end_game()
                elif body_part.y == -1 and body_part.pos[1] <= 0:
                    self.end_game()
                else: #snake moves
                    body_part.move(body_part.x,body_part.y,speed)

#body parts and food class
class Square():
    x = 0
    y = 0
    pos = None
    def __init__(self, pos):
        self.pos = pos
        self.x = 1
        self.y = 0

    def move(self, x, y,speed):
        self.x = x*speed
        self.y = y*speed
        self.pos = (self.pos[0] + self.x, self.pos[1] + self.y)

    #display the square on the screen
    def paint(self, h=0):
        siz = WINSIZE//ROWS #mantain proportion to square grid
        x = self.pos[0]
        y = self.pos[1]
        #check if it is the head, the body, or an apple
        if h == 1:
            screen.blit(use_head_ima, (x*siz,y*siz))
        elif h == 2:
            screen.blit(apple_ima, (x*siz,y*siz))
        elif h == 3:
            screen.blit(mouse_ima,(x+siz,y*siz))
        else:
            screen.blit(body_ima, (x*siz+1,y*siz+1))


def food(snek):
    flag =0
    while 1:
        x,y = numpy.random.randint(1,ROWS-1,2) #generate random coordinates

        for part in snek.body: #check coordinates are not used by body
            if part.pos != (x,y):
                flag =1
                break
        if flag == 1:
            break
    print(x)
    return x,y
        
#draw game grid. Primarily for testing.
def paint_grid( ):
    inbtwn = WINSIZE // ROWS #spacing between
    x = 0
    y = 0
    for i in range(ROWS):
        x += inbtwn
        y += inbtwn
        #draw rectangles, two lines
        pygame.draw.line(screen, 0, (x,0), (x,WINSIZE))
        pygame.draw.line(screen, 0, (0,y), (WINSIZE,y))

#paint score
def paint_score():
    score_screen = FONT.render('Score: %s' % (score), True, (0,255,255)) #text
    score_rect = score_screen.get_rect() #square to display the score
    score_rect.topleft = (WINSIZE - 120, 10) #position of the square in the screen
    screen.blit(score_screen, score_rect) #paint

#paint game over screen
def game_over():
    game_screen = FONT.render('Game Over Score: %s' %(score), True, (255,255,255)) #holds text
    game_rect = game_screen.get_rect() #create rectangle to display text
    game_rect.center = (WINSIZE / 2, WINSIZE/2) #position the rectangle
    screen.blit(game_screen, game_rect) #paint

#####################################################################################################
WINSIZE = 600 #square window size for game
ROWS = 20
global points, speed
points = 1
speed =1
pygame.init() #initialize
screen = pygame.display.set_mode((WINSIZE, WINSIZE)) #create window screen for game
clock = pygame.time.Clock() #create clock object
pygame.time.delay(1000) #delay start of game
snek = Snake((3,3)) #create snake object
foo = Square(food(snek)) #create initial food
FONT = pygame.font.Font('freesansbold.ttf', 18)
#font to be used for score and game over text
pygame.display.set_caption('PySnek') #window title
head_ima = pygame.image.load("./head.png") #load images/sprites
body_ima = pygame.image.load("./body.png")
use_head_ima = head_ima
power_on = Square(food(snek))
apple_ima = pygame.image.load("./apple.png")
mouse_ima = pygame.image.load("./mouse.png")
song = pygame.mixer.music.load("./theme.mp3")
score =0 #initialize score
pygame.mixer.music.play(loops=-1)
power_on = None
angle = 180
pu_start =0
while True:
    #showGameOverScreen()
    
    if snek.game_over == False:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit pygame
                pygame.quit() 
                sys.exit() #quit game
            if event.type == pygame.KEYDOWN: #user is pressing key
                snek.change_dir(event.key)
        snek.advance(speed) #move snek
        screen.fill((204, 193, 112)) #background white
        snek.paint()
        foo.paint(2)            
        
        if snek.body[0].pos == foo.pos: #snake is eating the food
            snek.grow() # add square to snake's body
            foo = Square(food(snek)) # create new food
            score +=points # increase score

        for part in snek.body[1:]: # check the body of the snake to check if it hits itself
            if part.pos == snek.body[0].pos:
                snek.end_game() #finis game
    
        #paint_plot()
        paint_score()
    else:
        pygame.mixer.music.fadeout(4000)
        #game is finished
        screen.fill((0,0,0)) #paint screen black
        game_over() #write game over text
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit pygame
                pygame.quit() 
                sys.exit() #close window
    clock.tick(10) # run at x frames per second     
    pygame.display.update() #refresh screen

########################################################################################################  
