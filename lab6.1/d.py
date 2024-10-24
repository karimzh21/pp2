import time
import math

number = float(input())
milliseconds = int(input())

time.sleep(milliseconds / 1000)
sqrt_number = math.sqrt(number)
print(f"Square root of {number} after {milliseconds} miliseconds is {sqrt_number}")
