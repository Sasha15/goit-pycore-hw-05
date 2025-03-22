def caching_fibonacci() -> callable:
    cache = {}
    def fibonacci(n: int) -> int:
        if n in (0, 1):
            return n
        if n in cache: 
            return cache[n] # Return cached value if it exists

        # Calculate and cache the Fibonacci number
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == '__main__':
    fib = caching_fibonacci()

    print(fib(10))
    print(fib(15))