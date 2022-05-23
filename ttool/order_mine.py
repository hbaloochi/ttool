import pandas as pd
import numpy as np
from olist.utils import haversine_distance
from olist.data import Olist


class Order:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances of Order
        self.data = Olist().get_data()

    def get_wait_time(self, is_delivered=True):
        """
        Returns a DataFrame with:
        [order_id, wait_time, expected_wait_time, delay_vs_expected, order_status]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Order in the variable self, as well as all its attributes
        filtered_orders = self.data['orders'].copy()
        filtered_orders=filtered_orders[filtered_orders['order_status']=='delivered']
        filtered_orders['order_purchase_timestamp']=pd.to_datetime(filtered_orders['order_purchase_timestamp'])
        filtered_orders['order_approved_at']=pd.to_datetime(filtered_orders['order_approved_at'])
        filtered_orders['order_delivered_carrier_date']=pd.to_datetime(filtered_orders['order_delivered_carrier_date'])
        filtered_orders['order_delivered_customer_date']=pd.to_datetime(filtered_orders['order_delivered_customer_date'])
        filtered_orders['order_estimated_delivery_date']=pd.to_datetime(filtered_orders['order_estimated_delivery_date'])
        filtered_orders['wait_time']=(filtered_orders['order_delivered_customer_date']-filtered_orders['order_purchase_timestamp']).dt.days
        filtered_orders['expected_wait_time']=(filtered_orders['order_estimated_delivery_date']-filtered_orders['order_purchase_timestamp']).dt.days.astype(float)
        filtered_orders['delay_vs_expected']=filtered_orders['wait_time']-filtered_orders['expected_wait_time']
        filtered_orders=filtered_orders[['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected', 'order_status']]
        filtered_orders=filtered_orders.dropna()
        filtered_orders['delay_vs_expected']=filtered_orders['delay_vs_expected'].apply(lambda x: max(0,x))
        return filtered_orders

    def get_review_score(self):
        """
        Returns a DataFrame with:
        order_id, dim_is_five_star, dim_is_one_star, review_score
        """
        reviews = self.data['order_reviews'].copy()
        reviews['dim_is_five_star']=reviews['review_score'].map({5:1,4:0,3:0,2:0,1:0})
        reviews['dim_is_one_star']=reviews['review_score'].map({5:0,4:0,3:0,2:0,1:1})
        return reviews[['order_id', 'dim_is_five_star', 'dim_is_one_star', 'review_score']]

    def get_number_products(self):
        """
        Returns a DataFrame with:
        order_id, number_of_products
        """
        order=self.data['orders'].copy()
        item=self.data['order_items'].copy()
        order_item=pd.merge(order,item,on='order_id')
        gbi=order_item.groupby('order_id',as_index=False).count()[['order_id','customer_id']]
        gbi['number_of_products']=gbi['customer_id']
        gbi[['order_id','number_of_products']]
        return gbi[['order_id','number_of_products']]

    def get_number_sellers(self):
        """
        Returns a DataFrame with:
        order_id, number_of_sellers
        """
        order=self.data['orders'].copy()
        item=self.data['order_items'].copy()
        order_item=pd.merge(order,item,on='order_id')
        gbi=order_item.groupby(['order_id','seller_id'],as_index=False).count()
        gbin=gbi.groupby('order_id',as_index=False).count()
        gbin['number_of_sellers']=gbin['seller_id']
        return gbin[['order_id','number_of_sellers']]

    def get_price_and_freight(self):
        """
        Returns a DataFrame with:
        order_id, price, freight_value
        """
        order=self.data['orders'].copy()
        item=self.data['order_items'].copy()
        order_item=pd.merge(order,item,on='order_id')
        gbi=order_item.groupby('order_id',as_index=False).sum()
        return gbi[['order_id', 'price', 'freight_value']]
    # Optional
    def get_distance_seller_customer(self):
        """
        Returns a DataFrame with:
        order_id, distance_seller_customer
        """
        pass  # YOUR CODE HERE

    def get_training_data(self,
                          is_delivered=True,
                          with_distance_seller_customer=False):
        """
        Returns a clean DataFrame (without NaN), with the all following columns:
        ['order_id', 'wait_time', 'expected_wait_time', 'delay_vs_expected',
        'order_status', 'dim_is_five_star', 'dim_is_one_star', 'review_score',
        'number_of_products', 'number_of_sellers', 'price', 'freight_value',
        'distance_seller_customer']
        """
        # Hint: make sure to re-use your instance methods defined above
        df1=self.get_wait_time()
        df2=self.get_review_score()
        df3=self.get_number_products()
        df4=self.get_number_sellers()
        df5=self.get_price_and_freight()
        rdf=pd.merge(df1,df2,on='order_id',how='inner')
        rdf=pd.merge(rdf,df3,on='order_id',how='inner')
        rdf=pd.merge(rdf,df4,on='order_id',how='inner')
        rdf=pd.merge(rdf,df5,on='order_id',how='inner')
        return rdf.dropna()