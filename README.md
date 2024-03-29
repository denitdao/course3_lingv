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

<img width="400" alt="image" src="https://user-images.githubusercontent.com/49095078/236812242-0d6e029a-527f-40e5-834e-184d9d06eda8.png">
<img width="300" alt="image" src="https://user-images.githubusercontent.com/49095078/236812262-b8486d82-8ff3-43c5-974a-91e06fd0a7e7.png">


### Умовний оператор

```
if <логічний вираз> then 
  <оператор>;
```
Розширено для використання послідовності операторів.

<img width="180" alt="image" src="https://user-images.githubusercontent.com/49095078/236812391-e099b378-75a8-45d2-8a2a-d80087f8a844.png">
<img width="200" alt="image" src="https://user-images.githubusercontent.com/49095078/236812408-8c16f823-8d33-43b2-8043-862536fc9ff4.png">

### Структура програмного засобу

<img alt="image" src="https://user-images.githubusercontent.com/49095078/236812820-2d01b02a-a7e7-421a-951c-f2cc4e43b6e0.png">

### Лексичний аналізатор

- Виконує перевірку допустимості наявних лексем імітуючи скінченний автомат.
- Перетворює набір символів на таблицю з токенів, виконуючи семантичні процедури.
- Результатом є набір таблиць для наступного модуля, або повідомлення про помилку з вказанням причини та місця.

<img width="800" alt="image" src="https://user-images.githubusercontent.com/49095078/236813173-f14a2982-22eb-4075-aca2-e46d4da6f2c6.png">

### Синтаксичний аналіз та трансляція у ПОЛІЗ

- Перевірка відповідності вхідої програми синтаксису мови DCh.
- Паралельна трансформація зустрінених команд у форму, яку може виконати система часу виконання.
- Визначення типів даних для оголошених змінних та додавання міток.
- Результатом є доповнений набір отриманих таблиць та програма у постфіксній нотації для наступного модуля, або повідомлення про помилку з вказанням причини та місця.

<img alt="image" src="https://user-images.githubusercontent.com/49095078/236813760-412ea5aa-fcfa-4223-82b5-18e43e2f1dc4.png">

### Інтерпретатор
- Виконання програми, записаної у постфіксній нотації.
- Відображення даних у консолі або зчитування користувацького вводу.
- Повідомлення про помилку та можливу причину у випадку виникнення такої.

<img alt="image" src="https://user-images.githubusercontent.com/49095078/236813561-f5a3d14e-74ff-48d3-805d-0f1ef78f4dd9.png">

### Приклад програми | Example

<img alt="image" src="https://user-images.githubusercontent.com/49095078/236813417-65bc68d8-20c0-4927-840f-04c990279a73.png">

