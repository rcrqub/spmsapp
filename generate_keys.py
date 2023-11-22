import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ['Daniel Quinn', 'Adam Exley', 'Robert Craig']
usernames = ['dquinn','aexley','rcraig']
passwords = ['XXX','XXX','XXX']

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hased_pw.pk1"
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)