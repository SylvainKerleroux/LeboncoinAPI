import search
import _http


def main(query, department, category, max_price, min_price):
    http = _http.RequestsHTTP()
    search_engine = search.LeBonCoin(http, query,
                                     department, category, max_price, min_price)
    for offer in search_engine.get_offers():
        print(offer)
        pass


if __name__ == "__main__":
    main("portable", 29, 'informatique', max_price=50, min_price=10)
