from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MIDDLE_OF_SCREEN = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета объектов
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Определение родительских атрибутов классов."""

    def __init__(self, position=MIDDLE_OF_SCREEN,
                 body_color=APPLE_COLOR) -> None:
        self.position = position
        self.body_color = body_color

    def paint_square(self, position):
        """Метод отрисовки одного квадрата объекта"""
        color = self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Заготовка метода для дочерних классов."""
        raise NotImplementedError


class Apple(GameObject):
    """Определение дочернего от GameObject класса."""

    def __init__(self):
        super().__init__()
        self.snake_positions = Snake().positions
        self.position = randomise_position(self, Snake().positions)

    def draw(self):
        """Определение метода отрисовки на поле."""
        self.paint_square(position=self.position)


class Snake(GameObject):
    """Определение дочернего от GameObject класса."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()
        self.directions = {
            (LEFT, pg.K_UP): UP,
            (RIGHT, pg.K_UP): UP,
            (RIGHT, pg.K_DOWN): DOWN,
            (LEFT, pg.K_DOWN): DOWN,
            (UP, pg.K_LEFT): LEFT,
            (DOWN, pg.K_LEFT): LEFT,
            (UP, pg.K_RIGHT): RIGHT,
            (DOWN, pg.K_RIGHT): RIGHT
        }

    def update_direction(self, keydown):
        """Метод обновления направления объекта класса."""
        self.new_direction = self.directions.get((self.direction, keydown),
                                                 self.direction)
        self.direction = self.new_direction

    def move(self):
        """Метод движения и изменения движения объекта класса."""
        head_position = self.get_head_position()
        new_head_position = ((head_position[0] + self.direction[0] * GRID_SIZE)
                             % SCREEN_WIDTH,
                             (head_position[1] + self.direction[1] * GRID_SIZE)
                             % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            del self.positions[-1]

    def snake_body(self):
        """
        Метод определения списка координат объекта
        класса без учёта первого элемента.
        """
        return self.positions[1::]

    def draw(self):
        """Метод отрисовки объекта класса и зарисовки хвоста"""
        for position in self.snake_body():
            GameObject.paint_square(self, position)
        GameObject.paint_square(self, self.get_head_position())
        if self.last:
            GameObject.paint_square(self, self.last)

    def get_head_position(self):
        """Метод определения координат первого элемента"""
        return self.positions[0]

    def reset(self):
        """Метод определения исходного"""
        """состояния объекта класса"""
        self.length = 1
        self.positions = [MIDDLE_OF_SCREEN]
        self.direction = choice([UP, LEFT, RIGHT, DOWN])
        self.last = None
        self.head_position = self.get_head_position()


def handle_keys(game_object):
    """Метод считывания и обработки ввода пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            game_object.update_direction(event.key)


def randomise_position(game_object, positions):
    """
    Метод определяет рандомную новую и тсартовую
    позицию яблока с учётом занятых клеток
    """
    progress = True
    while progress:
        game_object.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                                randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        if game_object.position not in positions:
            progress = False
            return game_object.position
        else:
            continue


def main():
    """Функция main"""
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 5
            randomise_position(apple, snake.positions)
        if snake.get_head_position() in snake.snake_body():
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
