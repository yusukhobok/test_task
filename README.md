# Тестовое приложение для визуализации диаграммы направленности фазированной антенной решетки

## Возможности
* Расчет диаграммы направленности антенны (в отдельном потоке);
* 3D отображение диаграммы направленности антенны;
* 2D отображение диаграммы направленности антенны (в виде цветовой карты);
* Отображение срезов ДНА по азимуту и возвышению при кликах на цветовую карту.

![скриншот](./screens/screen.png)

## Использованные библиотеки
* PyQt5: для общего интерфейса;
* PyQtGraph: для отображения двумерных диаграмм;
* Mayavi: для отображения трехмерной модели ДНА;
* PyTest, pytest-qt: для модульного тестирования интерфейса.

## Установка и запуск
* Требуемые библиотеки находятся в файле requirements.txt;
* python main.py

## 1111
![formula](https://www.codecogs.com/eqnedit.php?latex=G%20%3D%20%5Clvert%5C%20%5Ccos%5Cfrac%7B%5Cpi%20(%5Cphi%20-%20%5Cphi_s)%5Ccos%5Cphi_s%7D%7B2%20%5Cphi_0%7D%20cos%5Cfrac%7B%5Cpi%20(%5Ctheta-%5Ctheta_s)%5Ccos%5Ctheta_s%7D%7B2%20%5Ctheta_0%7D%20%5Crvert%20%5Ccdot%20l(%5Cphi%2C%20%5Ctheta)#0)
