import time, json, populater

class Reader():
    def read_log(self):
        while True:
            # open file with name
            f_name = './dump1090/aircraft.json'

            # open file, contents = json_data, give data var value of the contents turned into json
            with open(f_name) as json_data:
                data = json.load(json_data)

            # print information from file
            print('current: ', data)

            populater.Populate.checkIfExists(None, data)

            print('sleeping')
            time.sleep(1)


if __name__ == '__main__':
    Reader.read_log(Reader)