from django.test import TestCase

# Create your tests here.

import pandas as pd
path=r"C:\Users\Administrator.DESKTOP-E3H20V7\Desktop\tradelist_2021-07-15.csv"
df = pd.read_csv(path,encoding='gb2312')
print(df)
