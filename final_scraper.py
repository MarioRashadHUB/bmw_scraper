#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime


# In[2]:


name = []
mileage = []
dealer_name = []
rating = []
rating_count = []
price = []

for i in range(1,41):
    
    # Website in a variable
    website = 'https://www.cars.com/shopping/results/?page=' + str(i) + '&page_size=20&dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=bmw&maximum_distance=all&mileage_max=&models[]=bmw-335&sort=best_match_desc&stock_type=used&year_max=2011&year_min=2007&zip='

    # Request to website
    response = requests.get(website)
    
    # Soup object
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Results
    results = soup.find_all('div', {'class':'vehicle-card'})
    
    
    for result in results:
    
        # name
        try:
            name.append(result.find('h2').get_text())
        except:
            name.append('n/a')


        # mileage
        try:
            mileage.append(result.find('div', {'class':'mileage'}).get_text())
        except:
            mileage.append('n/a')

        # dealer_name
        try:
            dealer_name.append(result.find('div', {'class': 'dealer-name'}).get_text().strip())
        except:
            dealer_name.append('n/a')

        # rating
        try:
            rating.append(result.find('span',{'class':'sds-rating__count'}).get_text())
        except:
            rating.append('n/a')


        # rating_count
        try:
            rating_count.append(result.find('span', {'class': 'sds-rating__link'}).get_text())
        except:
            rating_count.append('n/a')


        # price
        try:
            price.append(result.find('span', {'class': 'primary-price'}).get_text())
        except:
            price.append('n/a')


# In[3]:


bmw_df = pd.DataFrame({'Name':name, 'Mileage': mileage,'Dealer Name': dealer_name,
                          'Rating': rating, 'Rating Count': rating_count, 'Price':price})


# In[4]:


bmw_df


# ### Data Cleaning

# In[5]:


bmw_df['Rating Count'] = bmw_df['Rating Count'].apply(lambda x: x.strip('reviews)').strip('('))


# # JUNE 2nd, 2022
# ## Further data cleaning prep for SQL

# ### Parse year

# In[6]:


bmw_df['Year'] = bmw_df['Name'].apply(lambda x: x.split(' ')[0])


# In[7]:


bmw_df


# ### Remove 'mi' from mileage

# In[8]:


bmw_df['Mileage'] = bmw_df['Mileage'].apply(lambda x: x.split(' ')[0])


# ### Remove \$ from price
# 

# In[9]:


'''
Reasoning for the -1 for future reference:
because if happens that occurrence is not in the string you'll get "IndexError: list index out of range".

Therefore -1 will not get any harm cause number of occurrences is already set to one.
'''

bmw_df['Price'] = bmw_df['Price'].apply(lambda x: x.split('$')[-1])


# In[10]:


bmw_df


# ### Remove comas from Mileage and Price

# In[11]:


bmw_df['Mileage'] = bmw_df['Mileage'].apply(lambda x: x.replace(',', ''))


# In[12]:


bmw_df['Price'] = bmw_df['Price'].apply(lambda x: x.replace(',', ''))


# ## Save CSV 

# In[13]:


filename = 'data_scrapped_' + datetime.today().strftime('%Y-%m-%d')
bmw_df.to_csv(filename, index=False)

