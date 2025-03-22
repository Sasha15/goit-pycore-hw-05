import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    # use negative lookbehind and negative lookahead to find float numbers
    pattern = r"(?<!\S)\d+\.\d+(?!\S)"

    for match in re.finditer(pattern, text):
        yield float(match.group())

def sum_profit(text: str, generator_numbers: Callable[[str], Generator[float, None, None]]) -> float:
    return sum(generator_numbers(text))


if __name__ == '__main__':
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")