from dataclasses import dataclass, asdict
from typing import Union, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    info = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> None:
        return self.info.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: Union[int, float],
                 weight: Union[int, float],
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
        raise NotImplementedError("Subclasses should count calories")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT
                 )
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H
                )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_MEAN_WEIGHT_MULTIPLIER_DURATION: float = 0.029
    KMH_MS: float = 0.278
    H_M: int = 100

    def __init__(self, action: int,
                 duration: Union[float, int],
                 weight: Union[int, float],
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (((self.CALORIES_MEAN_WEIGHT_MULTIPLIER * self.weight
                 + (((self.get_mean_speed() * self.KMH_MS)**2)
                  / (self.height / self.H_M))
                  * self.CALORIES_MEAN_WEIGHT_MULTIPLIER_DURATION
                  * self.weight))
                * self.MIN_IN_H * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_SHIFT_SPEED: float = 1.1
    CALORIES_MULTI_WEIGHT: int = 2
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: Union[float, int],
                 weight: Union[float, int],
                 length_pool: Union[float, int],
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)

        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_SHIFT_SPEED)
                * self.CALORIES_MULTI_WEIGHT
                * self.weight * self.duration)


def read_package(workout_type: str,
                 data: Union[list[int], list[float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_classes: dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
    if workout_type not in dict_classes:
        raise ValueError('Передан неверный идентификатор'
                         f' тренировки. {workout_type}')
    return dict_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
