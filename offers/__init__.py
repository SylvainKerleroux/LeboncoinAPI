
class Offer(object):

    def __init__(self, _id, url, title, price):

        self.id = _id
        self.url = url
        self.title = title
        self.price = price

        self._contact = None
        self._address = None

        self._is_content_fetched = False

    def _ensure_content_fetched(self):
        if not self._is_content_fetched:
            self._fetch_content()

    @property
    def contact(self):
        self._ensure_content_fetched()
        return self._contact

    @property
    def address(self):
        self._ensure_content_fetched()
        return self._address

    def _fetch_content(self):
        # self._is_content_fetched = True
        raise NotImplementedError

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return '<Offer title="{title}" price={price} url="{url}">'.format(
            title=self.title, price=self.price, url=self.url)
