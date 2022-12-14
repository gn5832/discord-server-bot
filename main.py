from modules.core.run import Client



def main():
    client = Client()
    client.run(token=client.get_token())


if __name__ == '__main__':
    main()