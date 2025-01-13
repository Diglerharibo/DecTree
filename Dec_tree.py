import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from scipy.stats import entropy
import warnings
from sklearn.exceptions import ConvergenceWarning

# Загружаем данные
data = pd.read_csv("C:/Users/egoro/Desktop/Kaggle experience/train.csv", index_col='Id')
useful = data[['LotArea', 'Condition1', 'BldgType', 'HouseStyle', 'OverallQual', 'OverallCond', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'GarageArea', 'SalePrice']]
#добрать норм признаки и приступить к формированию нодов и дерева

# Класс дерева решений
class DecTree:
    def __init__(self, data):
        # Удаляем все строки с NA
        self.data = data.dropna()
        self.features = self.data.columns.tolist()
        self.nodepack = {}
        self.node0 = Node(self.data)
        self.nodepack['node_0'] = self.node0

    def fit(self):
        while len(self.features) > 1:
            i = 0
            
            processing

            self.nodepack[f'node_{i}'].update_params(self.best_name, self.best_value, ) 
            #div_name = None, div_value = None, anc = None, desc1 = None, desc2 = None, lvl = None

            nodenamedict[f'node{i}']
            i += 2


    def identify_feature_types(self, data):
        #Определяем типы признаков: 0 - количественный, 1 - качественный.
        return [1 if not pd.api.types.is_numeric_dtype(data[col]) else 0 for col in data.columns]

    def preprocess_data(self, data, features): #Разделение признаков на качественные и количественные.
        
        # Сохраняем исходные названия колонок
        original_columns = data.columns

        # Разделяем количественные и качественные признаки
        numeric_indices = [i for i, t in enumerate(features) if t == 0]
        categorical_indices = [i for i, t in enumerate(features) if t == 1]

        numeric_data = data.iloc[:, numeric_indices]
        categorical_data = data.iloc[:, categorical_indices].copy()

        # Кодируем качественные признаки с помощью LabelEncoder
        if not categorical_data.empty:
            for col in categorical_data.columns:
                le = LabelEncoder()
                categorical_data[col] = le.fit_transform(categorical_data[col])

        # Объединяем количественные и закодированные данные
        processed_data = np.hstack([numeric_data.values, categorical_data.values])

        # Создаем новый DataFrame с объединенными данными
        processed_columns = numeric_data.columns.tolist() + categorical_data.columns.tolist()
        processed_df = pd.DataFrame(processed_data, columns=processed_columns, index=data.index)

        # Восстанавливаем исходный порядок колонок
        processed_df = processed_df[original_columns]
        '''
        # Разделяем данные на X и y
        series_list = [processed_df[col] for col in processed_df.columns]
        '''
        x = processed_df.iloc[:, :-1]  # Все кроме последнего столбца
        x = x.loc[:, (data.nunique() > 1)] #Удаление столбцов с одинаковыми значениями
        z = x.columns.tolist()
        y = processed_df.iloc[:, -1]   # Последний столбец

        #Надо провести проверку на одинаковые значения


        return x, y, z
    

    def find_split_points(self, data):
        split_list = []
        if isinstance(data, pd.DataFrame):
            for i in range(0, len(data.columns)):
                # Кластеризация
                kmeans = KMeans(n_clusters=100, random_state=42)
                kmeans.fit(data.iloc[:, i].values.reshape(-1, 1))

                # Метки кластеров
                labels = kmeans.labels_ #тут возвращается нд эррей, надо его в пд серию и индекс вернуть, порядок сохраняется

                sorted_labels = np.sort(labels)
                sorted_labels = pd.Series(sorted_labels) #labels сохраняются только для последней итерации цикла, тк
                    # Находим переходы между кластерами
                split_points = []
                for k in range(1, len(sorted_labels)):
                    if sorted_labels.iloc[k] != sorted_labels.iloc[k - 1]:
                        split_value = (data.iloc[k, i] + data.iloc[k-1, i]) / 2  #!!!!!!!!!!
                        split_points.append(split_value)

                split_list.append(split_points)
        else:
            # Если data — это Series
            kmeans = KMeans(n_clusters=100, random_state=42)
            kmeans.fit(data.values.reshape(-1, 1))  # Для Series преобразуем в массив
            labels = pd.Series(kmeans.labels_, index=data.index)
            sorted_labels = labels.sort_values()

        return split_list, sorted_labels #надо под условие загонять (хотя по логике надо) 


    def splitted_indices(self, xdata, split_list): #получает на вход [[],[],[]]
        dict_for_col = {}
        for i in range(0, len(xdata.columns)):
            dict_for_indices = {}
            column = xdata.iloc[:, i]
            sorted_column = column.sort_values(ascending=True) #разобраться почему при списках мы рабтаем с колонками
            split_value_list = split_list[i]
            for x in split_value_list:
                indices_below = sorted_column[sorted_column < x].index.tolist()
                indices_above = sorted_column[sorted_column > x].index.tolist()
                dict_for_indices[x] = (indices_below, indices_above)
            
            dict_for_col[xdata.columns[i]] = dict_for_indices

        return dict_for_col
    
    def ig_find(self, dictionary, y): #метка для разработки - dict понятно, y это список лейблов в пд серии с восстановленной индексацией (все норм должно быть)
        best_ig = 0
        best_name = None
        best_value = None
        best_before_ind = None
        best_after_ind = None
        h_parent = self.calculate_entropy(y)
        len_all = len(y)
        for col_name in dictionary:
            for split_val in dictionary[col_name]:
                before_ind = dictionary[col_name][split_val][0]
                after_ind = dictionary[col_name][split_val][1]
                
                len_before = len(before_val_y)
                len_after = len(after_val_y)
                before_val_y = y.loc[before_ind].tolist()
                after_val_y = y.loc[after_ind].tolist()
                ent_before = self.calculate_entropy(before_val_y)
                ent_after = self.calculate_entropy(after_val_y)
                ig = h_parent - ((len_before/len_all)*ent_before + (len_after/len_all)*ent_after)
                if ig > best_ig:
                    best_ig = ig
                    best_name = col_name
                    best_value = split_val
                    best_before_ind = before_ind
                    best_after_ind = after_ind

        return best_ig, best_name, best_value, best_before_ind, best_after_ind


    def calculate_entropy(self, data):
        # сюда даем список labels после kmeans
        _, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)
        return entropy(probabilities, base=2)


    def data_divider(self, data, before_ind, after_ind):
        before_data = data.loc[before_ind]
        after_data = data.loc[after_ind]

        return before_data, after_data
    
    def processing(self, data): #На вход дается датафрейм с именными столбиками. Находится лучшее разделение по признаку
        self.feature_types = self.identify_feature_types(data)
        self.x_predata, self.y_predata, self.features = self.preprocess_data(data, self.feature_types)
        self.x_split_val, _ = self.find_split_points(self.x_predata) #Списки внутри списков [[],[],[]]
        self.indices_pairs = self.splitted_indices(self.x_predata, self.x_split_val) # Словари внутри словаря вида: {Точка разделения данных : ([Indices before],[Indices after])}
        _, self.y_labels = self.find_split_points(self.y_predata)
        self.best_ig, self.best_name, self.best_value, self.best_before_ind, self.best_after_ind = self.ig_find(self.indices_pairs, self.y_labels) #что такое селф у лейблс втф; у лейблы это лейблы
        self.data = self.data.drop(columns=self.best_name)
        self.data_bef_div, self.data_aft_div = self.data_divider(self.data, self.best_before_ind, self.best_after_ind)

        return self.best_name, self.best_value, self.data_bef_div, self.data_aft_div



#Класс узлов
class Node:
    def __init__(self, data, div_name = None, div_value = None, anc = None, desc1 = None, desc2 = None, lvl = None):
        self.data = data
        self.div_name = div_name
        self.div_value = div_value
        self.anc = anc
        self.desc1 = desc1
        self.desc2 = desc2

    def update_params(self, div_name=None, div_value=None, anc=None, desc1=None, desc2=None, lvl=None):
        if div_name is not None:
            self.div_name = div_name
        if div_value is not None:
            self.div_value = div_value
        if anc is not None:
            self.anc = anc
        if desc1 is not None:
            self.desc1 = desc1
        if desc2 is not None:
            self.desc2 = desc2
        if lvl is not None:
            self.lvl = lvl


tree = DecTree(useful)
tree.fit()