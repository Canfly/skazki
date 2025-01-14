#include <gb/gb.h>
#include <stdio.h>

void main() {
    // Включаем дисплей и показываем фон
    DISPLAY_ON;
    SHOW_BKG;

    // Печатаем текст "CANFLY" в верхней части экрана
    printf("\n\n  CANFLY");

    // Мигающий текст "PUSH START" внизу экрана
    while (1) {
        // Печатаем текст
        printf("\n\n   PUSH START");
        delay(500);

        // Очищаем строку, печатая пробелы
        printf("\n\n            ");
        delay(500);

        // Проверка нажатия кнопки START
        if (joypad() & J_START) {
            break; // Переход к игре при нажатии
        }
    }

    // Начало игры (пока пустое место)
    printf("\n\n\n   GAME START");
    while (1) {
        // Основной игровой цикл
    }
}
