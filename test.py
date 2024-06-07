import data_handling
datasets = data_handling.get_datasets()
d=datasets[['Symbol','Name']]
d=d.set_index('Symbol')
print(d.loc['MSFT']['Name'])