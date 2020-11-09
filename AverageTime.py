import pandas as pd
from datetime import datetime


class AverageTime:

    def time_conversion(self, time_string):
        """
        Function to convert time into 24hr format
        :param time_string
        :return: new_time
        """
        if time_string[-2:] == "am":
            if time_string[:2] == '12':
                new_time = str('00' + time_string[2:-2]).strip() + ':00'
            else:
                new_time = time_string[:-2].strip() + ':00'
        else:
            if time_string[:2] == '12':
                new_time = time_string[:-2].strip() + ':00'
            else:
                new_time = (str(int(time_string[:2]) + 12) + time_string[2:-2]).strip() + ':00'
        return new_time

    def convert_to_unix_time(self,date):
        """
        Function to convert time to Unix time format
        :param date:
        :return: date in unix format
        """
        return datetime.timestamp(date)

    def convert_from_unix_time(self,time):
        """
        Function to convert from Unix time format to Date time format
        :param time:
        :return: date
        """
        return datetime.fromtimestamp(time)

    def compute_average(self,file_name):
        """
        Function to find the average time for transactions in a file
        :param file_name:
        :return:
        """
        file = pd.read_csv(file_name, header=None, names=["Id", "Date", "Time", "Status"])
        file.iloc[:, 2] = file.iloc[:, 2].apply(self.time_conversion)
        file['DateTime'] = pd.to_datetime(file['Date'] + ' ' + file['Time'])
        file.drop(['Date', 'Time'], axis=1, inplace=True)
        file['UnixTime'] = file.iloc[:, 2].apply(self.convert_to_unix_time)

        id_time_dict = dict()
        row_count = len(file)

        for row in range(row_count):
            id_value = file.iloc[row, 0]
            date_value = file.iloc[row, 3]

            if id_value not in id_time_dict.keys():
                id_time_dict[id_value] = []
            id_time_dict[id_value].append(date_value)

        for id_value, date_list in id_time_dict.items():
            sum_value = 0
            for date in date_list:
                sum_value = sum_value + date
            id_time_dict[id_value] = self.convert_from_unix_time(sum_value / len(date_list))

        data = pd.DataFrame.from_dict(id_time_dict, orient='index')
        data.to_csv('Output.csv')

if __name__== '__main__':
    file_name = 'SampleFile.csv'
    avg_time_obj = AverageTime()
    avg_time_obj.compute_average(file_name)
