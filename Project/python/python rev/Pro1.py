def inttostr(i):
    Number = "0123456789"
    if i == 0:
        return "0"
    s = ""
    while i > 0:
        s = Number[i % 10] + s
        i = i // 10
    return s  # ← moved outside the loop
    
print(inttostr(123))


"""s = Number[i % 10] + s
Notice the digit is added to the front of s, not the back.

Step-by-step with i = 123
Iterationi % 10 (digit)OperationResult of sStart——s = ""1st123 % 10 = 3s = '3' + ""s = "3"2nd12 % 10 = 2s = '2' + "3"s = "23"3rd1 % 10 = 1s = '1' + "23"s = "123"

The Trick

Digits are extracted right to left (3 → 2 → 1)
But each new digit is prepended (added to the front)
So they get reversed back into the correct order

Think of it like a stack — the last digit extracted (1) ends up at the front, giving you "123" instead of "321".Sonnet 4.6"""