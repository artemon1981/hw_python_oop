class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.action * self.LEN_STEP / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: int, weight: int) -> None:
        super().__init__(action, duration, weight)
        self.distance = Training.get_distance(self)
        self.speed = Training.get_mean_speed(self)
        self.calories = Running.get_spent_calories(self)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.speed
                 + self.CALORIES_MEAN_SPEED_SHIFT
                 )
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_KEF = 0.035
    SECOND_KEF = 0.029
    KMH_MS = 0.278
    H_M = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = Training.get_distance(self)
        self.speed = Training.get_mean_speed(self)
        self.calories = SportsWalking.get_spent_calories(self)

    def get_spent_calories(self) -> float:
        return (((self.FIRST_KEF * self.weight
                 + (((self.speed * self.KMH_MS)**2)
                  / (self.height / self.H_M))
                  * self.SECOND_KEF * self.weight))
                * self.MIN_IN_H * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    SW_CONST = 1.1
    SW_MULTI = 2
    LEN_STEP = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.lenght_pool = length_pool
        self.count_pool = count_pool
        self.speed = Swimming.get_mean_speed(self)
        self.calories = Swimming.get_spent_calories(self)
        self.distance = Training.get_distance(self)

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.speed + self.SW_CONST) * self.SW_MULTI
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dr_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in dr_training:
        return dr_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
