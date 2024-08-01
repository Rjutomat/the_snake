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
ANTI_EYE_COLOR = (102, 250, 3)

# Константа направлений
DIRECTIONS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
    (LEFT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}
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

    def __init__(
            self,
            positions=[MIDDLE_OF_SCREEN],
            body_color=ANTI_EYE_COLOR) -> None:
        self.position = positions
        self.body_color = body_color

    def paint_square(self,
                     position,
                     color,
                     border_color=BORDER_COLOR):
        """Метод отрисовки одного квадрата объекта."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Заготовка метода для дочерних классов."""
        raise NotImplementedError("Не определен наследуемый метод draw.")


class Apple(GameObject):
    """Определение дочернего от GameObject класса."""

    def __init__(self, snake_positions=[MIDDLE_OF_SCREEN]):
        super().__init__()
        self.position = self.randomize_position(snake_positions)

    def draw(self):
        """Определение метода отрисовки на поле."""
        self.paint_square(position=self.position, color=APPLE_COLOR)

    def randomize_position(self, occupied_positions):
        """
        Метод рандомизации позиции объекта класса на
        поле с учётом занятых клеток.
        """
        self.position = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        if self.position not in occupied_positions:
            return self.position


class Snake(GameObject):
    """Определение дочернего от GameObject класса."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self, new_direction):
        """Метод обновления направления объекта класса."""
        self.direction = new_direction

    def move(self):
        """Метод движения и изменения движения объекта класса."""
        head_position = self.get_head_position()
        new_head_position = ((head_position[0] + self.direction[0] * GRID_SIZE)
                             % SCREEN_WIDTH,
                             (head_position[1] + self.direction[1] * GRID_SIZE)
                             % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.get_last()
            del self.last

    def get_last(self):
        self.last = self.positions[-1]
        return self.last

    def snake_body(self):
        """
        Метод определения списка координат объекта
        класса без учёта первого элемента.
        """
        return self.positions[1:]

    def draw(self):
        """Метод отрисовки объекта класса и зарисовки хвоста"""
        self.paint_square(self.get_head_position(), SNAKE_COLOR)
        if self.get_last():
            self.paint_square(self.last, BOARD_BACKGROUND_COLOR)

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


def handle_keys(game_object):
    """Метод считывания и обработки ввода пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            new_direction = DIRECTIONS.get((game_object.direction, pg.KEYDOWN),
                                           game_object.direction)
            game_object.direction = game_object.update_direction(new_direction)


def main():
    """Функция main"""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.snake_body():
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
