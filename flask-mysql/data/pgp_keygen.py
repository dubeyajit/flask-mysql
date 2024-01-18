# Program to check the GnuPG

import gnupg
import os

print(gnupg.__version__)

#homedir='/home/ajitdubey/.gnupg'

#gpg =gnupg.GPG(gnupghome='/home/ajitdubey/.gnupg/')
#gpg = gnupg.GPG(gnupghome=homedir)
#gpg = gnupg.GPG(homedir=homedir)
gpg = gnupg.GPG(homedir='/home/ajitdubey/.gnupg')

gpg.encoding = 'utf-8'

key_input_data = gpg.gen_key_input(
    name_email ='ajitdubey@gmail.com',
    passphrase = 'iliveincedarrapids',
    key_type = 'RSA',
    key_length = 4096)

key = gpg.gen_key(key_input_data)

print(key)