from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2
import traceback
import threading


class DatabaseConnection():

    def databaseConnection(self):
        databaseName = "postgres"
        databaseIP = "o17by.ddns.net"
        databaseUser = "postgres"
        databasePassword = "uM5.>BQNY<Jw"
        databasePort = 15432

        try:
            return psycopg2.connect(
                database=databaseName,
                user=databaseUser,
                password=databasePassword,
                host=databaseIP,
                port=databasePort
            )
        except:
            return False


class Splitter():
    startChar = "$"
    lastChar = "&"
    insideChar = "@"
    arr = []

    def splitter1(self, string):
        # print(string)

        string = string.replace("\"", "").replace("}", "").replace("{", "")
        user = string.split('$')[0]
        string = string.replace(user, "").replace("$$", "")
        string = string.replace("$:$", "")

        # print(string)
        arr = (string.split("$"))
        for i in range(len(arr)):
            arr[i] = arr[i].split("@")
            # print(arr[i])
        return arr, user


class S(BaseHTTPRequestHandler):
    def thread_data(self, post_data,dataB):
        spl = Splitter
        # print(content_length)
        print("post_data: " + str(post_data))
        if (post_data == '{"user_volodar":""}'):
            post_data = ""

        conn = dataB.databaseConnection()
        cursor = conn.cursor()

        data1 = spl.splitter1(self, post_data.decode("utf-8"))
        user = data1[1]
        print(len(data1[0]))

        for i in range(len(data1[0]))[1:]:
            print("cycle")
            try:
                if ((data1[0][i][1]).find(",") != (-1)):
                    data1[0][i][1] = data1[0][i][1].replace("[", "").replace("]", "").split(",")
                    if (len(data1[0][i][1]) == 3):
                        x = data1[0][i][1][0]
                        y = data1[0][i][1][1]
                        z = data1[0][i][1][2]
                        cursor.execute(
                            f"INSERT INTO userMac(username_mac,{data1[0][i][0]}_x,{data1[0][i][0]}_y,{data1[0][i][0]}_z,date_time) values('{user}',{float(x)},{float(y)},{float(z)},{int(data1[0][i][2])});")
                        conn.commit()
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                conn.rollback()
            try:
                if (len(data1[0][i][1]) == 4):
                    x = data1[0][i][1][0]
                    y = data1[0][i][1][1]
                    z = data1[0][i][1][2]
                    w = data1[0][i][1][3]
                    cursor.execute(
                        f"INSERT INTO userMac(username_mac,{data1[0][i][0]}_x,{data1[0][i][0]}_y,{data1[0][i][0]}_z,{data1[0][i][0]}_w,date_time)"
                        f" values('{user}',{float(x)},{float(y)},{float(z)},{float(w)},{int(data1[0][i][2])});")
                    cursor.commit()
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                conn.rollback()

            try:
                if (len(data1[0][i][1]) == 5):
                    x = data1[0][i][1][0]
                    y = data1[0][i][1][1]
                    z = data1[0][i][1][2]
                    w = data1[0][i][1][3]
                    f = data1[0][i][1][4]
                    cursor.execute(
                        f"INSERT INTO userMac(username_mac,{data1[0][i][0]}_x,{data1[0][i][0]}_y,{data1[0][i][0]}_z,{data1[0][i][0]}_w,{data1[0][i][0]}_f,date_time)"
                        f" values('{user}',{float(x)},{float(y)},{float(z)},{float(w)},{float(f)},{int(data1[0][i][2])});")
                    conn.commit()
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                conn.rollback()

            try:
                if (len(data1[0][i]) == 2):
                    cursor.execute(
                        f"INSERT INTO userMac(username_mac,type_{data1[0][i][0]},date_time) values('{user}',{int(data1[0][i][1])},{int(data1[0][i][1])})")
                    conn.commit()
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                conn.rollback()
            print(i)
            print(len(data1[0]))

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        print("readDATA")
        post_data = self.rfile.read(content_length)
        self._set_headers()
        #self.thread_data(post_data)
        dataB = DatabaseConnection()

        threading.Thread(target=self.thread_data, args=(post_data,dataB)).start()

        print("done")
        # exit()


def run(server_class=HTTPServer, handler_class=S, port=80):
    sever_adress = ('192.168.1.197', port)
    httpd = server_class(sever_adress, handler_class)
    print('Starting htttp.....')
    httpd.serve_forever()


if __name__ == "__main__":
    # cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);"
    print(run())
