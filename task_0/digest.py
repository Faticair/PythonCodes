import hashlib
import getpass

def encode_md5(strdata: str):
    if not strdata:
        return ''
    return hashlib.md5(strdata.encode('utf8')).hexdigest()

def encode_sha1(strdata: str):
    if not strdata:
        return ''
    return hashlib.sha1(strdata.encode('utf8')).hexdigest()

if __name__ == '__main__':
    username = input('input the username: ')
    password = getpass.getpass('input the password: ')
    # unDigest = hashlib.sha1(username.encode('utf8'))
    # pwDigest = hashlib.sha1(password.encode('utf8'))
    # unDigest_final = hashlib.md5(unDigest.hexdigest().encode('utf8'))
    # pwDigest_final = hashlib.md5(pwDigest.hexdigest().encode('utf8'))
    # print('username digest: ' + unDigest_final.hexdigest())
    # print('password digest: ' + pwDigest_final.hexdigest())
    usernameDigest = encode_md5(encode_md5(encode_sha1(username)))
    passwordDigest = encode_md5(encode_md5(encode_sha1(password)))
    print('username is: ' + username + '\t Digest is: ' + usernameDigest)
    print('password is: ***' + password[-3:] + '\t Digest is: ' + passwordDigest)