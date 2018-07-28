import datetime
import requests
import pandas as pd
import xmltodict

def datetime_now():
    return "This web page was generated at: " + datetime.datetime.now().strftime("%H:%M:%S")



criteria = ["category","listing_id","num_bathrooms","num_bedrooms","outcode","post_town","price","first_published_date"]

class Property():
    """
    PLACEHOLDER: Add some details
    """

    def __init__(self, postcode="EH10", beds=2, baths=1, price=400000, page_size=100, status="sale"):
        self.postcode = postcode
        self.max_beds = beds
        self.min_beds = beds
        self.baths = baths
        self.price = price
        self.page_size = page_size
        self.status = status

    def create_data(self, status=None):
        if status == None:
            status = self.status
        else:
            status = status
        pw = "3jxm2trkjx4ekrfqp6d2vvkc"
        url_base = "http://api.zoopla.co.uk/api/v1/property_listings.xml?api_key={}".format(pw)
        url = url_base + "&listing_status={}&postcode={}&page_size={}&maximum_beds={}&minimum_beds={}&maximum_price={}".format(status,self.postcode,self.page_size,self.max_beds,self.min_beds,self.price)
        response = requests.get(url)
        xml_string = response.content
        data = xmltodict.parse(xml_string)
        return data
    
    def basic_table(self):
        data = self.create_data()
        listing = data["response"]["listing"]
        df = pd.DataFrame.from_dict(listing)
        df = pd.DataFrame(df, columns = criteria)
        df["average_sale_price"] = df["price"].apply(lambda x: float(x)).mean()
        df["relative_sale_price"] = (df["price"].apply(lambda x: float(x)) /  df["average_sale_price"]).round(2)
        df["price"] = df["price"].apply(lambda x: int(x)).apply('{:,}'.format)
        df["average_sale_price"] = df["average_sale_price"].apply(lambda x: int(x)).apply('{:,}'.format)
        return df
        
    def listing_count(self):
        data = self.create_data()
        listing = data["response"]["result_count"]
        return listing

    def average_rent(self):
        data = self.create_data(status="rent")
        listing = data["response"]["listing"]
        df = pd.DataFrame.from_dict(listing)
        df = pd.DataFrame(df, columns = ["price","listing_id"])
        df["average_rent"] = df["price"].apply(lambda x: float(x)).mean()
        return df["average_rent"]

    def table_with_rent(self):
        df = self.basic_table()  
        df["average_rent"] = self.average_rent().round()[1]*4
        df["average_rent"] = df["average_rent"].apply(lambda x: int(x)).apply('{:,}'.format)
        return df