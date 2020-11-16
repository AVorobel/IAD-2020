import matplotlib.pyplot as plt


class Graphic:
    def __init__(self, x: list, y: list = None):
        if y is not None:
            self.__x = x
            self.__y = y
        else:
            self.__x = x
        self.__height = 10
        self.__width = 10

    def set_plot_size(self, x, y):
        self.__height = y
        self.__width = x

    def show_graphic(self, graph_type: str, **kwargs):
        if graph_type == 'gist':
            try:
                self.__y
            except AttributeError:
                fig, gr = plt.subplots()
                try:
                    for i in self.__x:
                        gr.bar(i['x'], i['y'], label=i['label'] if 'label' in i.keys() else 'no label')
                except Exception as e:
                    raise Exception('data should be type list of dictionaries')
            else:
                plt.bar(self.__x, self.__y)
        elif graph_type == 'dot':
            try:
                self.__y
            except AttributeError:
                fig, gr = plt.subplots()
                try:
                    for i in self.__x:
                        gr.scatter(i['x'], i['y'], label=i['label'] if 'label' in i.keys() else 'no label')
                except Exception as e:
                    raise Exception('data should be type list of dictionaries')
            else:
                plt.scatter(self.__x, self.__y)
        elif graph_type == 'line':
            try:
                self.__y
            except AttributeError:
                if 'plots' in kwargs:
                    for i in range(len(self.__x)):
                        plt.subplot(kwargs['plots'], 1, i + 1)
                        plt.plot(self.__x[i]['x'], self.__x[i]['y'])
                        plt.ylabel(self.__x[i]['label'] if 'label' in self.__x[i].keys() else 'no label')
                        ax = plt.gca()
                        ax.axes.xaxis.set_ticklabels([]) if 'show_xlabels' in kwargs else None
                    fig = plt.gcf()
                    fig.set_size_inches(self.__width, self.__height)
                    plt.show()
                    return
                else:
                    fig, gr = plt.subplots()
                    try:
                        for i in self.__x:
                            gr.plot(i['x'], i['y'], label=i['label'] if 'label' in i.keys() else 'no label')
                    except Exception as e:
                        raise Exception('data should be type list of dictionaries')
            else:
                plt.plot(self.__x, self.__y)
        elif graph_type == 'pie':
            try:
                self.__y
            except AttributeError:
                if isinstance(self.__x[0], str):
                    temp = {}
                    for i in self.__x:
                        if i in temp.keys():
                            temp[i] += 1
                        else:
                            temp[i] = 1
                    plt.pie(temp.values(), labels=temp.keys())
                else:
                    plt.pie(self.__x, labels=kwargs['labels'] if 'labels' in kwargs.keys() else None,
                            labeldistance=None)
            else:
                raise Exception('for the pie chart you need 1 list of data')

        plt.xlabel('x axis') if 'xlabel' not in kwargs else plt.xlabel(kwargs['xlabel'])
        plt.ylabel('y axis') if 'ylabel' not in kwargs else plt.ylabel(kwargs['ylabel'])
        plt.xticks(rotation=55)

        ax = plt.gca()
        ax.axes.xaxis.set_ticklabels([]) if 'show_xlabels' in kwargs else None
        ax.axes.yaxis.set_ticklabels([]) if 'show_ylabels' in kwargs else None

        plt.legend() if 'legend' in kwargs else None
        plt.grid(True)

        fig = plt.gcf()
        fig.set_size_inches(self.__width, self.__height)

        plt.show()
