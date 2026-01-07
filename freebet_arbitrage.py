import math
from typing import List, Optional


TOLERANCE = 15
MAX_ITER = 20_000
PROFIT_GOAL = 14_985

# ANSI цвета
BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"


def calculate_freebet_bets(
    freebet_amount: float,
    coef1: float,
    coef2: float,
    coef3: float
) -> Optional[List[int]]:
    if coef1 <= 1.0 or coef2 <= 1.0 or coef3 <= 1.0:
        return None

    c1m = coef1 - 1
    c2m = coef2 - 1
    c3m = coef3 - 1

    total_win = c1m * freebet_amount
    total_int = int(total_win)
    inv_c3m = 1.0 / c3m if c3m != 0 else float('inf')

    max_profit = 0
    best_result = None
    max_i = min(MAX_ITER, total_int + 1)

    for i in range(max_i):
        if c3m > 0:
            min_j = max(0, math.ceil(i * inv_c3m))
        else:
            min_j = 0

        if c2m > 0:
            max_j_cond = math.floor(i * c2m)
        else:
            max_j_cond = MAX_ITER

        max_j = min(MAX_ITER, total_int - i, max_j_cond)
        if min_j > max_j:
            continue

        for j in range(min_j, max_j + 1):
            y1 = int(total_win - i - j)
            y2 = int(i * c2m - j)
            y3 = int(j * c3m - i)

            if y1 < 0 or y2 < 0 or y3 < 0:
                continue

            if (
                abs(y1 - y2) < TOLERANCE
                and abs(y2 - y3) < TOLERANCE
                and abs(y1 - y3) < TOLERANCE
            ):
                profit = (y1 + y2 + y3) // 3
                if profit > max_profit:
                    max_profit = profit
                    best_result = [i, j, y1, y2, y3]
                    if profit >= PROFIT_GOAL:
                        return best_result
    return best_result


def main() -> None:
    print(f"{BOLD}{CYAN}Программа для расчёта ставок при отыгрыше фрибета{RESET}")
    print(f"{CYAN}{'=' * 60}{RESET}")

    while True:
        try:
            print()
            freebet_input = input(f"{BOLD}Введите сумму фрибета{RESET} (например, 1000): ").strip()
            freebet = float(freebet_input)

            print(f"\n{CYAN}(Фрибет будет поставлен на первый исход){RESET}")
            cf1 = float(input(f"{BOLD}Коэффициент на 1-й исход{RESET}: ").strip())
            cf2 = float(input(f"{BOLD}Коэффициент на 2-й исход{RESET}: ").strip())
            cf3 = float(input(f"{BOLD}Коэффициент на 3-й исход{RESET}: ").strip())

            if cf1 <= 1.0 or cf2 <= 1.0 or cf3 <= 1.0:
                print(f"\n{RED}❌ Ошибка:{RESET} Все коэффициенты должны быть больше 1.0")
                continue

        except ValueError:
            print(f"\n{RED}❌ Ошибка:{RESET} Пожалуйста, введите корректные числа (например, 2.5)")
            continue

        result = calculate_freebet_bets(freebet, cf1, cf2, cf3)

        print(f"\n{CYAN}{'-' * 50}{RESET}")
        if result is None:
            print(f"{YELLOW}⚠️  Не удалось найти подходящую стратегию отыгрыша фрибета.{RESET}")
        else:
            bet2, bet3, win1, win2, win3 = result
            avg_profit = (win1 + win2 + win3) // 3

            print(f"{GREEN}{BOLD}✅ Найдена оптимальная стратегия!{RESET}")
            print(f"\n{BOLD}Рекомендуемые ставки:{RESET}")
            print(f"  • На коэффициент {cf1}: {GREEN}фрибет {freebet} ₽{RESET} (ваши деньги не тратятся)")
            print(f"  • На коэффициент {cf2}: {GREEN}{bet2} ₽{RESET}")
            print(f"  • На коэффициент {cf3}: {GREEN}{bet3} ₽{RESET}")

            print(f"\n{BOLD}Ожидаемый выигрыш (чистая прибыль):{RESET}")
            print(f"  • Если выиграет 1-й исход: {CYAN}{win1} ₽{RESET}")
            print(f"  • Если выиграет 2-й исход: {CYAN}{win2} ₽{RESET}")
            print(f"  • Если выиграет 3-й исход: {CYAN}{win3} ₽{RESET}")
            print(f"\n{BOLD}Средний гарантированный профит:{RESET} {GREEN}~{avg_profit} ₽{RESET}")

        print(f"\n{CYAN}{'-' * 50}{RESET}")
        choice = input(
            f"\n{BOLD}Что дальше?{RESET}\n"
            "  Нажмите Enter — выйти\n"
            f"  Введите {BOLD}1{RESET} — рассчитать ещё раз\n"
            "\nВаш выбор: "
        ).strip()

        if choice == "1":
            print(f"\n{CYAN}{'=' * 60}{RESET}")
            continue
        else:
            print(f"\n{GREEN}Спасибо за использование! Удачи в ставках! 🍀{RESET}")
            break


if __name__ == "__main__":
    main()
