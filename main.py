from modules.core.run import Client



if __name__ == '__main__':
    client = Client()
    client.run(token=client.get_token())

