def make_pretty(func):
    def inner():
        print("I got decorated")
        func()
    return inner

