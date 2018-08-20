'''
Script to pull data from server

Simon Filhol, Aug 2018

'''

import db_query
import pandas as pd


#===================================================
# 1. pull latest data from server
var_oi = ['RECORD', 'TA_2_1_1_1_1',
              'RH_19_3_1_1_1',
              'WD_20_35_1_1_1', 'WS_16_33_1_1_1',
              'METNOR_99_99_1_1_1',
              'FC1DRIFTmean_99_99_1_1_1', 'FC2DRIFTmean_99_99_1_1_1','time'
              ]

df = db.query_df(serial=serial, table_name='Biomet', time__gte=start, time__lte=end, limit=25000000, fields=var_oi, interval=inter_sample)





#===================================================
# 2. Add data to local DB (sqlite?), and remove older data

