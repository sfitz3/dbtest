import re

phoneNumRegex = re.compile( r'\ d\ d\ d-\ d\ d\ d-\ d\ d\ d\ d')

def isPhoneNumber(text):
    if len(text) !=12:
        return False
    for i in range(0,3):
        if not text[i].isdecimal():
            return False
    if text[3] != '-':
        return False
    for i in range(4, 7):
        if not text[i].isdecimal():
            return False
    if text[7] != '-':
        return False
    for i in range(8, 12):
        if not text[i].isdecimal():
            return False
    return True

mo = phoneNumRegex.search('415-555-4242')
print(mo)
print(' Phone number found: ' + mo.group())

