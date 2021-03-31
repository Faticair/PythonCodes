import json
import os
import string
import random

def gen_passwd(kword, L):
    kword = modify_key(kword)
    klen = len(kword)
    if klen > L:
        return kword[0:L] + random_char('')
    while klen < L:
        kword += random_char('digit')
        klen += 1
    return kword

def random_char(char_type):
    if char_type == 'alphabet':
        return random.choice(string.ascii_lowercase)
    elif char_type == 'digit':
        return random.choice(string.digits)
    else:
        return random.choice(['!', '@', '#', '$', '%', '*', '?', '+'])

def load_json():
    jsonpath = "D:\\Codes\\Python\\ZahiTool\\transword.json"
    with open(jsonpath, 'r') as jsonfile:
        json_dic = json.loads(jsonfile.read())
    return json_dic

def replace_char(origin):
    word_dic = load_json()
    return random.choice(word_dic[origin])

def modify_key(origin):
    while len(origin) < 4:
        origin += random_char('alphabet')
    tmp = origin.lower()
    tmp = replace_char(tmp[0]) + tmp[1:]
    if not find_special_symbol(tmp):
        tmp += random_char('')
    return tmp

def find_special_symbol(kstr):
    symbolset = ['/', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
                '[', ']', ';', '<', '>', '?', '-', '_', '+', '=']
    existflag = False
    for x in kstr:
        if x in symbolset:
            existflag = True
            break
    return existflag

def main():
    keyword = input("### Please input a string of key word([a-z] default: abcdef):")
    passwdLength = input("### Please input the length you need(default: 8):")
    if not keyword:
        keyword = 'abcdef'
    if not passwdLength:
        passwdLength = 8
    else:
        passwdLength = int(passwdLength)
    # print(keyword + num)
    # print(type(passwdLength))
    print("### The password is generating...")
    res = gen_passwd(keyword.lower(), passwdLength)
    print("### Password ###")
    print(res)

if __name__ == '__main__':
    main()