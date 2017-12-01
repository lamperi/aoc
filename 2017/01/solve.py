import sys
data = sys.stdin.read().strip()

# part 1
def captcha(data, offset=1):
   s = 0
   for a, b in zip(data, data[offset:] + data[:offset]):
       if a == b:
           s += int(a)
   return data if len(data) < 20 else data[:10] + "..." + data[-10:], s

print(captcha("1122"))
print(captcha("1111"))
print(captcha("1234"))
print(captcha("91212129"))
print(captcha(data))

def captcha2(data):
   return captcha(data, len(data)/2)

print(captcha2("1212"))
print(captcha2("1221"))
print(captcha2("123425"))
print(captcha2("123123"))
print(captcha2("12131415"))
print(captcha2(data))
