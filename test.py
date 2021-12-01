import pickle
for cookie in pickle.load(open("gCookies.pkl", "rb")):
    print(cookie)