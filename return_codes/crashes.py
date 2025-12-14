# Process finished with exit code 1

def run():
    print("Example of a method that crashes fine")
    raise Exception("Some error message")

if __name__ == '__main__':
    run()
