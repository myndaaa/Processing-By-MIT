CANVAS_SIZE = 600
TILE_SIZE = 30
ROWS, COLS = CANVAS_SIZE // TILE_SIZE, CANVAS_SIZE // TILE_SIZE
TEXTSIZE = 20

score = 0
game_over = False
game = None

def setup():
    global game, apple_image, banana_image, head_up_image, head_left_image
    size(CANVAS_SIZE, CANVAS_SIZE)
    
    apple_image = loadImage("data/apple.png")
    banana_image = loadImage("data/banana.png")
    head_up_image = loadImage("data/head_up.png")
    head_left_image = loadImage("data/head_left.png")
    
    if apple_image is None or banana_image is None or head_up_image is None or head_left_image is None:
        apple_image = createImage(TILE_SIZE, TILE_SIZE, RGB)
        banana_image = createImage(TILE_SIZE, TILE_SIZE, RGB)
        head_up_image = createImage(TILE_SIZE, TILE_SIZE, RGB)
        head_left_image = createImage(TILE_SIZE, TILE_SIZE, RGB)
        
        apple_image.loadPixels()
        for i in range(apple_image.width * apple_image.height):
            apple_image.pixels[i] = color(255, 0, 0)
        apple_image.updatePixels()

        banana_image.loadPixels()
        for i in range(banana_image.width * banana_image.height):
            banana_image.pixels[i] = color(255, 255, 0)
        banana_image.updatePixels()

        head_up_image.loadPixels()
        for i in range(head_up_image.width * head_up_image.height):
            head_up_image.pixels[i] = color(255, 255, 0)
        head_up_image.updatePixels()

        head_left_image.loadPixels()
        for i in range(head_left_image.width * head_left_image.height):
            head_left_image.pixels[i] = color(255, 255, 0)
        head_left_image.updatePixels()

    game = Game()

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake)
    
    def reset(self):
        global score, game_over
        score = 0
        game_over = False
        self.snake = Snake()
        self.food = Food(self.snake)
    
    def update(self):
        if not game_over:
            self.snake.move()
            self.check_collisions()
    
    def display(self):
        background(203)
        self.snake.display()
        self.food.display()
        fill(0)
        textSize(TEXTSIZE)
        text("Score: " + str(score), CANVAS_SIZE - 100, 30)
    
    def check_collisions(self):
        global score, game_over
        if self.snake.head_pos() == self.food.pos:
            food_color = color(255, 0, 0) if self.food.image == apple_image else color(255, 255, 0)
            self.snake.grow(food_color)
            score += 1
            self.food = Food(self.snake)
        if self.snake.hit_wall() or self.snake.hit_self():
            game_over = True
    
    def show_game_over(self):
        textSize(TEXTSIZE)
        fill(0)
        text("Game Over!", CANVAS_SIZE // 2 - 50, CANVAS_SIZE // 2)
        text("Final Score: " + str(score), CANVAS_SIZE // 2 - 60, CANVAS_SIZE // 2 + 30)
        text("Click to Restart", CANVAS_SIZE // 2 - 60, CANVAS_SIZE // 2 + 60)

class Snake:
    def __init__(self):
        self.body = [
            SnakeElement(COLS // 2, ROWS // 2, color(80, 152, 32)),
            SnakeElement(COLS // 2 - 1, ROWS // 2, color(80, 152, 32)),
            SnakeElement(COLS // 2 - 2, ROWS // 2, color(80, 152, 32))
        ]
        self.direction = (1, 0)

    def head_pos(self):
        return (self.body[0].x, self.body[0].y)
    
    def move(self):
        if game_over:
            return

        dx, dy = self.direction
        head_x, head_y = self.head_pos()

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += dx
        self.body[0].y += dy

    def grow(self, food_color):
        last_segment = self.body[-1]
        new_segment = SnakeElement(last_segment.x, last_segment.y, food_color)
        self.body.append(new_segment)

    def change_direction(self, new_direction):
        opposite_dir = (-self.direction[0], -self.direction[1])
        if new_direction != opposite_dir:
            self.direction = new_direction

    def hit_wall(self):
        x, y = self.head_pos()
        return x < 0 or x >= COLS or y < 0 or y >= ROWS
    
    def hit_self(self):
        head = self.head_pos()
        return any(e.pos() == head for e in self.body[1:])
    
    def display(self):
        for i, elem in enumerate(self.body):
            if i == 0:
                elem.display(self.direction)
            else:
                elem.display()

class SnakeElement:
    def __init__(self, x, y, color_value):
        self.x = x
        self.y = y
        self.color = color_value

    def pos(self):
        return (self.x, self.y)
    
    def display(self, direction=None):
        fill(self.color)
        noStroke()
        if direction:
            if direction == (0, -1):
                image(head_up_image, self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            elif direction == (0, 1):
                pushMatrix()
                translate(self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE)
                scale(-1, 1)
                image(head_up_image, 0, 0, TILE_SIZE, TILE_SIZE)
                popMatrix()
            elif direction == (-1, 0):
                image(head_left_image, self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            elif direction == (1, 0):
                pushMatrix()
                translate(self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE)
                scale(-1, 1)
                image(head_left_image, 0, 0, TILE_SIZE, TILE_SIZE)
                popMatrix()
        else:
            ellipse(self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

class Food:
    def __init__(self, snake):
        self.pos = self.random_position(snake)
        self.color = color(255, 0, 0) if random(2) < 1 else color(255, 255, 0)
        self.image = apple_image if self.color == color(255, 0, 0) else banana_image
    
    def random_position(self, snake):
        while True:
            x, y = int(random(COLS)), int(random(ROWS))
            if (x, y) not in [e.pos() for e in snake.body]:
                return (x, y)
    
    def display(self):
        image(self.image, self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE)

def draw():
    if frameCount % 10 == 0:
        game.update()
    game.display()
    if game_over:
        game.show_game_over()

def keyPressed():
    if keyCode == UP:
        game.snake.change_direction((0, -1))
    elif keyCode == DOWN:
        game.snake.change_direction((0, 1))
    elif keyCode == LEFT:
        game.snake.change_direction((-1, 0))
    elif keyCode == RIGHT:
        game.snake.change_direction((1, 0))

def mousePressed():
    global game_over
    if game_over:
        game.reset()
