### Система выявления синтезированного голоса 2.0

Данная система является программной реализации разработанного алгоритма выявляения синтезированного голоса
в рамках научно-исследовательской работы по совместной программе ИТМО и Сбербанка.

Система является веб-сервисом, в который встроена проверка аудио на естественность.

Публикации по разработанному алгоритму:
1. [Methods of countering speech synthesis attacks on voice biometric
systems in banking
](https://www.elibrary.ru/item.asp?id=44805921)
2. [Алгоритм выявления синтезированного голоса на основе кепстральных коэффициентов и сверточной нейронной сети](https://www.elibrary.ru/item.asp?id=46495306)


Реализованный алгоритм был в рамках Web-приложения для демонстрации возможностей, а также способов его примения:
1. Через интерфейс браузера
2. Через api для встраивания в голосовую биометрическую систему


Используемые технологии:
1. Фреймворк Flask
2. База данных SQlite
3. Flask-migration для миграций
4. Tensorfow для создание модели CNN


Данная версия является второй по счету. Первая доступна для тестирования и была размещена на Heroku:
[Ссылка на реализацию](https://pak-vsgo.herokuapp.com/)
