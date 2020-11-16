import pandas as pd
from kn308_Vorobel_graficModule import Graphic
import requests
import io
import matplotlib.pyplot as plt
from consts import coords

print('Downloading data')
s = requests.get(
    'https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_dynamics.csv').content
df = pd.read_csv(io.StringIO(s.decode('utf-8')), index_col='zvit_date')
del s
print('Data downloaded')

answer = None
while answer != 0:
    answer = int(input('1)передивитись дані по 1 області\n2)порівняти дані областей\n3)карта заражених\n'
                       '4)імпортувати останні дані в Excel\n0)вихід\n'))
    if answer == 1:
        reg = input('Введіть область: ')
        df_reg = df.loc[df['registration_area'] == reg]
        df_reg_date_grouped = df_reg.groupby(['zvit_date']).agg('sum')
        graph = Graphic([
            {'x': df_reg_date_grouped.index.tolist(), 'y': df_reg_date_grouped['new_susp'].tolist(),
             'label': 'new_susp'},
            {'x': df_reg_date_grouped.index.tolist(), 'y': df_reg_date_grouped['new_confirm'].tolist(),
             'label': 'new_confirm'},
            {'x': df_reg_date_grouped.index.tolist(), 'y': df_reg_date_grouped['active_confirm'].tolist(),
             'label': 'active_confirm'},
            {'x': df_reg_date_grouped.index.tolist(), 'y': df_reg_date_grouped['new_death'].tolist(),
             'label': 'new_death'},
            {'x': df_reg_date_grouped.index.tolist(), 'y': df_reg_date_grouped['new_recover'].tolist(),
             'label': 'new_recover'},
        ])
        graph.show_graphic('line', plots=5, show_xlabels=False,
                           title=f'{df_reg_date_grouped.index[0]} — {df_reg_date_grouped.tail(1).index[0]}')
    elif answer == 2:
        reg = input('Введіть області(через кому): ')
        regs = reg.split(',')
        plot_data = {}
        graph_data = []
        for i in regs:
            df_reg = df.loc[df['registration_area'] == i]
            df_reg_date_grouped = df_reg.groupby(['zvit_date']).agg('sum')
            plot_data[i] = df_reg_date_grouped
        compare = None
        while compare != 0:
            compare = int(input('що порівняти?\n1)нові підозрілі\n2)нові підтверджені\n3)активні підтверджені\n'
                                '4)нові смерті\n5)нові виліковані\n0)вихід\n'))
            if compare == 1:
                for i in regs:
                    info = {'x': plot_data[i].index, 'y': plot_data[i]['new_susp'].tolist(),
                            'label': i}
                    graph_data.append(info)
            elif compare == 2:
                for i in regs:
                    info = {'x': plot_data[i].index, 'y': plot_data[i]['new_confirm'].tolist(),
                            'label': i}
                    graph_data.append(info)
            elif compare == 3:
                for i in regs:
                    info = {'x': plot_data[i].index, 'y': plot_data[i]['active_confirm'].tolist(),
                            'label': i}
                    graph_data.append(info)
            elif compare == 4:
                for i in regs:
                    info = {'x': plot_data[i].index, 'y': plot_data[i]['new_death'].tolist(),
                            'label': i}
                    graph_data.append(info)
            elif compare == 5:
                for i in regs:
                    info = {'x': plot_data[i].index, 'y': plot_data[i]['new_recover'].tolist(),
                            'label': i}
                    graph_data.append(info)
            else:
                break

            graph = Graphic(graph_data)
            graph.set_plot_size(20, 10)
            graph.show_graphic('line', xlabel='date', ylabel='stat', show_xlabels=False, legend=True)
            graph_data = []
    elif answer == 3:
        get_coord = lambda x: coords[x]
        size = lambda size, mx: (size * 10000) / mx

        BBox = (22.324, 39.983, 45.352, 52.398)  # lat min, lat max, long min, long max
        map = plt.imread('static/map2.png')

        df_lastdate = df.loc[df.index == df.index[0]]
        df_gr = df_lastdate.groupby(['registration_area']).agg('sum')
        for mode in ['new_susp', 'new_confirm', 'active_confirm', 'new_death', 'new_recover']:
            ls = df_gr[mode]
            mx = ls.max()
            fig, ax = plt.subplots(figsize=(15, 10))
            ax.scatter([get_coord(x)[0] for x in ls.index], [get_coord(x)[1] for x in ls.index],
                       alpha=0.3, s=[size(x, ls.max()) for x in ls], c='r')

            ax.set_title(f'Plotting Covid Data on Ukraine Map : {mode}')
            ax.set_xlim(BBox[0], BBox[1])
            ax.set_ylim(BBox[2], BBox[3])
            ax.imshow(map, zorder=0, extent=BBox, aspect='auto')

            ax.text(0.01, 0.01, '\n'.join([f'{ls.index[i]} : {ls[i]}' for i in range(len(ls))]), transform=ax.transAxes,
                    fontsize=9, verticalalignment='bottom', bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))

            plt.show()
    elif answer == 4:
        df_lastdate = df.loc[df.index == df.index[0]]
        df_gr = df_lastdate.groupby(['registration_area']).agg('sum')
        try:
            df_gr.to_excel('static/last_day_raport.xlsx')
        except Exception as e:
            print(e)
        else:
            print('Done, check "static" folder.')
    elif answer == 0:
        break
    else:
        continue
