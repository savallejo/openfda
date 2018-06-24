import http.server
import socketserver
import http.client
import json

IP = 'localhost'
Port= 8000
MAX_OPEN_REQUESTS = 5

socketserver.TCPServer.allow_reuse_address = True


class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if self.path == "/":
            with open("openfda.html", "r") as f:
                mensa = f.read()
            self.wfile.write(bytes(mensa, "utf8"))

        elif "searchDrug" in self.path:
            d = self.path.split("?")[1]
            drug = d.split("&")[0].split("=")[1]
            # lim = data.split("&")[1].split("=")[1]

            # lim = 10
            if "limit" in self.path:
                lim = self.path.split("=")[2]
                if lim == '':
                    lim = '10'
            else:
                lim = '10'


            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?search=active_ingredient=" + drug + "&limit=" + lim
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()


            mensa= '<ol>'
            for i in range(len(drugs['results'])):
                try:
                    mensa += '<li>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</li>'

                except KeyError:
                    mensa += '<li>' + str(i + 1) + '. ' + ('Unknown') + '</li>'
            mensa += '</ol>'


            self.wfile.write(bytes(mensa, "utf8"))


        elif "searchCompany" in self.path:
            d = self.path.split("?")[1]
            company= d.split("&")[0].split("=")[1]

            if "limit" in self.path:
                lim = self.path.split("=")[2]
                if self.path.split("=")[2] == '':
                    lim = '10'
            else:
                lim = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?search=manufacturer_name:" + company+ "&limit=" + lim
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            mensa = '<ol>'
            for i in range(len(drugs['results'])):
                try:
                    mensa += '<li>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</li>'

                except KeyError:
                    mensa += '<li>' + str(i + 1) + '. ' + ('Unknown') + '</li>'
            mensa += '</ol>'


            self.wfile.write(bytes(mensa, "utf8"))

        elif "listDrugs" in self.path:
            d = self.path.split("?")[1]
            if "limit" in self.path:
                lim = d.split('=')[1]
                if lim == '':
                    lim = '10'
            else:
                lim = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?limit=" + lim
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            mensa = '<ol>'
            for i in range(len(drugs['results'])):
                try:
                    mensa += '<li>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['brand_name'][0] + '</li>'

                except KeyError:
                    mensa += '<li>' + str(i + 1) + '. ' + ('Unknown') + '</li>'
            mensa += '</ol>'

            self.wfile.write(bytes(mensa, "utf8"))

        elif "listCompanies" in self.path:
            d = self.path.split("?")[1]

            if "limit" in self.path:
                lim = d.split('=')[1]
                if lim == '':
                    lim= '10'
            else:
                lim = '10'

            headers = {'User-Agent': 'http-client'}
            conn = http.client.HTTPSConnection("api.fda.gov")
            url = "/drug/label.json?limit=" + lim
            conn.request("GET", url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            drugs = json.loads(drugs_raw)
            conn.close()

            mensa = '<ol>'
            for i in range(len(drugs['results'])):
                try:
                    mensa += '<li>' + str(i + 1) + '. ' + drugs['results'][i]['openfda']['manufacturer_name'][
                        0] + '</li>'

                except KeyError:
                    mensa += '<li>' + str(i + 1) + '. ' + ('Unknown') + '</li>'
            mensa += '</ol>'

            self.wfile.write(bytes(mensa, "utf8"))
        return


Handler = HTTPRequestHandler

httpd = socketserver.TCPServer((IP, Port), Handler)
print("Serving at Port", Port)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Stop")

# Sara Vallejo