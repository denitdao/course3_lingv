# course3_lingv
This is my repo for the 3rd-year subject - Development of translators (programming language processors)


### Загальна інформація

Назва мови програмування складена з початкових літер імені автора. DCh - Denys Churchyn.

Мова є імперативною, тобто програма є послідовним переліком дій, що необхідно виконати комп’ютеру.

За основу мови взята помісь C та Pascal.
Розроблена на мові Python.

### Особливості мови

- 3 типи даних – цілі, дійсні та логічні;
- Чотири основні лівоасоціативні операції: додавання, віднімання, ділення, множення та операція залишку від ділення;
- Правоасоціативна операція піднесення до степеня;
- Унарна операція зміни знаку;
- Логічні оператори порівняння;
- Оператори умовного переходу, повторення, введення та виведення.

### Оператор циклу

```
for ( <ідентифікатор> = <вираз>; <відношення>; <ідентифікатор> = <вираз> ) { 
  <список операторів> 
}
```
Розширено для виконання не тільки послідовності, а й одиночного оператора.
<img width="476" alt="image" src="https://user-images.githubusercontent.com/49095078/236812242-0d6e029a-527f-40e5-834e-184d9d06eda8.png">
<img width="368" alt="image" src="https://user-images.githubusercontent.com/49095078/236812262-b8486d82-8ff3-43c5-974a-91e06fd0a7e7.png">


### Умовний оператор
```
if <логічний вираз> then 
  <оператор>;
```
Розширено для використання послідовності операторів.

<img width="259" alt="image" src="https://user-images.githubusercontent.com/49095078/236812391-e099b378-75a8-45d2-8a2a-d80087f8a844.png">
<img width="272" alt="image" src="https://user-images.githubusercontent.com/49095078/236812408-8c16f823-8d33-43b2-8043-862536fc9ff4.png">


### Структура програмного засобу

<img alt="image" src="https://user-images.githubusercontent.com/49095078/236812820-2d01b02a-a7e7-421a-951c-f2cc4e43b6e0.png">

### Лексичний аналізатор

- Виконує перевірку допустимості наявних лексем імітуючи скінченний автомат.
- Перетворює набір символів на таблицю з токенів, виконуючи семантичні процедури.
- Результатом є набір таблиць для наступного модуля, або повідомлення про помилку з вказанням причини та місця.