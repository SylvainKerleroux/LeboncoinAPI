import requests


DEFAULT_ENCODING = 'windows-1252'


class Response:

    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content

    def __repr__(self):
        return '<Response status_code="{status}" lenght="{lenght}">'.format(
            lenght=len(self.content), status=self.status_code)


class RequestsHTTP:

    def __init__(self):
        self.driver = requests.Session()

    def get(self, url, parameters=None):
        try:
            response = self.driver.get(url, params=parameters)
            print(response)
            print(response.url)
            return Response(
                response.status_code, response.content.decode(
                    DEFAULT_ENCODING))
        except Exception as e:
            print(e)
            return Response(500, None)
