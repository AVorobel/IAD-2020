import pandas as pd
from kn308_Vorobel_graficModule import Graphic


# def data_parser(arg: list):
#     dates = list(filter(lambda x: (x != ' ' and x != '' and x != 'mph'), arg.split(' ')))
#     dates[0] += '.2019'
#     dates[1] = round((int(dates[1]) - 32) / 1.8, 2)
#     dates[2] = round((int(dates[2]) - 32) / 1.8, 2)
#     tmp = dates[3]
#     if dates[4] == 'PM':
#         tm = tmp.split(':')
#         tm[0] = str(int(tm[0]) + 12) if int(tm[0]) + 12 != 24 else str(0)
#         dates[3] = ':'.join(tm)
#     else:
#         dates[3] = tmp
#     dates[5] = float(dates[5]) * 1.61
#     dates[6] = float(dates[6]) * 1.61
#     dates[7] = float(dates[7][:-1]) / 100
#     try:
#         dates.remove('PM')
#     except ValueError:
#         dates.remove('AM')
#     dates = [x if isinstance(x, str) else str(x) for x in dates]
#     return dates

def time_format_24(time: list):
    new_time_format = {}
    for i in time:
        tmp = i.split(' ')
        if tmp[1] == 'PM':
            tm = tmp[0].split(':')
            tm[0] = str(int(tm[0]) + 12) if int(tm[0]) + 12 != 24 else str(0)
            new_time_format[i] = ':'.join(tm)
        else:
            new_time_format[i] = tmp[0]
    return new_time_format


def date_format_year(date: list, add_year: str):
    new_date_format = {}
    for i in date:
        new_date_format[i] = i + '.' + add_year
    return new_date_format


def temp_format_c(temp: list):
    new_temp = {}
    for i in temp:
        new_temp[i] = round((i - 32) / 1.8, 2)
    return new_temp


def to_float(temp: list):
    new_list = {}
    for i in temp:
        if len(list(i)) == 3:
            new_list[i] = float(i[:-1]) / 100
        else:
            new_list[i] = float(i.split(' ')[0]) * 1.61
    return new_list


dataset = pd.read_csv('Static/DATABASE.csv', delimiter=';')
# , parse_dates=[['day/month', 'Temperature',
#                                                     'Dew Point', 'Time', 'Wind Gust',
#                                                     'Wind Speed', 'Humidity']],
# date_parser=data_parser

dataset['Time'] = dataset['Time'].map(time_format_24(dataset['Time'].to_list()))
dataset['day/month'] = dataset['day/month'].map(date_format_year(dataset['day/month'].to_list(), '2019'))
dataset['Temperature'] = dataset['Temperature'].map(temp_format_c(dataset['Temperature'].to_list()))
dataset['Dew Point'] = dataset['Dew Point'].map(temp_format_c(dataset['Dew Point'].to_list()))
dataset['Wind Gust'] = dataset['Wind Gust'].map(to_float(dataset['Wind Gust'].to_list()))
dataset['Wind Speed'] = dataset['Wind Speed'].map(to_float(dataset['Wind Speed'].to_list()))
dataset['Humidity'] = dataset['Humidity'].map(to_float(dataset['Humidity'].to_list()))
pd.set_option("display.max_rows", None, "display.max_columns", None)
dataset.index = dataset['day/month']
dataset.drop('day/month', axis='columns', inplace=True)
print(dataset)

dt = [dataset['Time'].loc[dataset.index == '13.Aug.2019'].tolist(), dataset['Humidity'].tolist()]
args = [{'x': dataset['Time'].loc[dataset.index == '13.Aug.2019'].tolist(),
         'y': dataset['Temperature'].loc[dataset.index == '13.Aug.2019'].tolist(),
         'label': 'temperature'},
        {'x': dataset['Time'].loc[dataset.index == '13.Aug.2019'].tolist(),
         'y': dataset['Dew Point'].loc[dataset.index == '13.Aug.2019'].tolist(),
         'label': 'dew point'}]
# dataset['Time'].loc[dataset.index == '13.Aug.2019'].tolist(), dataset['Humidity'].tolist()
graph = Graphic(dataset['Condition'].tolist())
graph.show_graphic('pie', legend=True, xlabel='', ylabel='')
# graph = Graphic(dataset['Time'].loc[dataset.index == '13.Aug.2019'].tolist(),
#                 dataset['Humidity'].loc[dataset.index == '13.Aug.2019'].tolist())
graph = Graphic(args)
graph.set_plot_size(30, 10)
graph.show_graphic('line', legend=True, xlabel='Time', ylabel='Humidity')
graph.show_graphic('dot', legend=True, xlabel='Time', ylabel='Humidity')
graph.show_graphic('gist', legend=True, xlabel='Time', ylabel='Humidity')
