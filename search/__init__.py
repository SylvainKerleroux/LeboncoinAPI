import os
import bs4
import offers

lowPrice_QueryCategory = [0, 10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300, 350, 400, 500]

highPrice_QueryCategory = [0, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000,
                           6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 11000, 12000, 13000, 14000, 15000, 17500,
                           20000, 22500, 25000, 27500, 30000, 32500, 33000, 35000, 37500, 40000, 42500, 45000, 45500,
                           47500, 50000]

class LeBonCoin:

    BASE_URL = "https://www.leboncoin.fr"

    def __init__(self, http, searched_item=None, department=None, category=None,
                 max_price=10000000000, min_price=1):

        self._http = http

        self.max_price = max_price
        self.min_price = min_price

        self.query = str(searched_item)
        self._department = department
        self._category = category

    @property
    def category(self):
        """
        Build the category part of the url
        :return: string
        """
        if self._category is None:
            return "annonces/offres"
        else:
            return self._category

    @property
    def department(self):
        """
        Transform the department number to its proper name
        :return: string
        """
        if self._department == 29:
            return "bretagne"
        elif self._department is None :
            return "ile_de_france/occasions"
        else:
            raise NotImplementedError

    @property
    def request_max_price(self):
        """
        The leboncoin.fr does not allow to set precise search prices.
        It functions with steps : 0, 250, 500, 750 ...
        :return: int (). Higher step (i.e : if max_price = 200, than returns step for 250.
        The prices will than be re-checked in self.get_offers() to return only user defined prices.
        """
        if True:
            price_category_list = lowPrice_QueryCategory
        else:
            price_category_list = highPrice_QueryCategory

        try:
            return price_category_list.index(min(value for value in price_category_list if value >= self.max_price))
        except ValueError:
            return len(price_category_list)

    @property
    def request_min_price(self):
        """
        The leboncoin.fr does not allow to set precise search prices.
        It functions with steps : 0, 250, 500, 750 ...
        :return: int (). Lower step (i.e : if min_price = 200, than returns step for 0.
        The prices will be checked in self.get_offers() to return only user defined prices.
        """
        if True:
            price_category_list = lowPrice_QueryCategory
        else:
            price_category_list = highPrice_QueryCategory

        return price_category_list.index(max(value for value in price_category_list if value <= self.min_price))

    def get_offers(self):
        """
        Get offers from all pages, skips the pages with 1euro scam offer
        :return: Offer object
        """
        API_KEY = 'ba0c2dad52b3ec'

        url_ext = os.path.join(self.category, self.department)
        final_url = os.path.join(self.BASE_URL, url_ext)

        request_parameters = {'q': self.query,
                              'o': 1,    # page number
                              'ps': self.request_min_price,
                              'pe': self.request_max_price,
                              'sp': 1,
                              'Content-Type': 'application/json',
                              'api-key': API_KEY
                              }  # filter by price (2 if by date)

        load_more_pages = True
        page = 1
        while load_more_pages:
            request_parameters['o'] = page
            print("Checking page number : {}".format(page))

            try:
                response = self._http.get(final_url, request_parameters)
                soup = bs4.BeautifulSoup(response.content, 'lxml')
                print(soup)
            except Exception as e:
                print(e)
                page += 1
                continue

            all_a = soup.find_all('a', class_='list_item clearfix trackable')
            for a in all_a:
                info_dic = eval(a['data-info'])

                try:
                    offer_id = info_dic['ad_listid']
                    offer_url = 'https:' + a['href']
                    offer_title = a['title']
                    offer_price = int(a.h3['content'])

                    if self.min_price <= offer_price <= self.max_price:
                        yield offers.Offer(offer_id, offer_url, offer_title, offer_price)

                    if int(offer_price) >= self.max_price:
                        load_more_pages = False

                except KeyError or TypeError:
                    continue

                except Exception as e:
                    print(e)
                    continue

            page += 1
