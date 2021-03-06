# Тестовое приложение для визуализации диаграммы направленности фазированной антенной решетки

![скриншот](./screens/screen.png)

## Возможности
* Расчет диаграммы направленности антенны (в отдельном потоке);
* 3D отображение диаграммы направленности антенны;
* 2D отображение диаграммы направленности антенны (в виде цветовой карты);
* Отображение срезов ДНА по азимуту и возвышению при кликах на цветовую карту.

## Использованные библиотеки
* PyQt5: для общего интерфейса;
* PyQtGraph: для отображения двумерных диаграмм;
* Mayavi: для отображения трехмерной модели ДНА;
* PyTest, pytest-qt: для модульного тестирования интерфейса.

## Алгоритм расчета ДНА
Диаграмма направленности антенны рассчитывается по следующей формуле:

![скриншот](./screens/formula1.gif)

![скриншот](./screens/formula2.gif)

_φ_ - угол по азимуту (из расчётной сетки)

_θ_ - угол по возвышению (из расчётной сетки)

_φ<sub>s</sub>_ - угол установки луча по азимуту

_θ<sub>s</sub>_ - угол установки луча по возвышению

_φ<sub>0</sub>_ - ширина главного лепестка по азимуту

_θ<sub>0</sub>_ - ширина главного лепестка по возвышению

_l<sub>main</sub>_ - уровень главного лепестка ДНА

_l<sub>side</sub>_ - уровень бокового лепестка ДНА