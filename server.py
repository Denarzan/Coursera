import asyncio
"""server for storing metrics"""
database = {}


class ClientServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport

    def data_received(self, data):
        request = data.decode()[:-1].split(' ')  # request without \n in the end
        command = request[0]  # put or get
        message = request[1:]  # query
        if command == "put":
            result = self.put(message)
        elif command == "get":
            result_first = self.get(message)
            result = ''.join([str(elem) for elem in result_first])
            result += "\n"  # send back result of the request
        else:
            result = "error\nwrong command\n\n"
        self.transport.write(result.encode())

    @staticmethod
    def put(message):
        if len(message) != 3:  # 1-metric, 2-value, 3-timestamp
            return "error\nwrong command\n\n"
        try:
            message[1] = float(message[1])  # value
            message[2] = int(message[2])  # timestamp
        except ValueError:
            return "error\nwrong command\n\n"
        if message[0] not in database:  # if new metric
            database[message[0]] = [(message[1], message[2])]
        else:
            counter, flag = 0, True
            for i in database[message[0]]:
                if message[2] == i[1] and message[1] == i[0]:  # if the same metric has already been in database
                    return 'ok\n\n'
                elif message[2] == i[1]:  # if metric has been in database, but with other timestamp
                    database[message[0]][counter] = (message[1], message[2])  # change it
                    flag = False
                counter += 1
            if flag:
                database[message[0]].append((message[1], message[2]))  # if metric with new value and timestamp
        return 'ok\n\n'

    @staticmethod
    def get(message):
        data = ["ok"]
        if len(message) != 1:
            return "error\nwrong command\n"
        elif message[0] == "*":
            for metric in database:
                for value in database[metric]:
                    data.append(f"\n{metric} {value[0]} {value[1]}")  # return all metrics
            data.append("\n")
            return data
        elif message[0] in database:
            for value in database[message[0]]:
                data.append(f"\n{message[0]} {value[0]} {value[1]}")  # returns data for a given metric
            data.append("\n")
            return data
        else:
            return 'ok\n'  # if metric is not in database


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
