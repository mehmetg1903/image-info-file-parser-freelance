from ..util.string_helper import remove_multiple_spaces, trim
import pandas as pd
import numpy as np


class BexarParser:

    def __init__(self, file_name):
        self._df = pd.read_csv(file_name, header=None, sep='\t')
        self._df = self._df.replace(np.nan, '', regex=True)

    def parse(self, db):
        inserted = 0
        for index, row in self._df.iterrows():
            try:
                business = remove_multiple_spaces(str(row[8])).split("|")
                owner = business[0].replace("OWNER ", "")
                business_name = business[-1].replace("BUSINESS NAME ", "")
                address_zip_data = remove_multiple_spaces(str(row[9])).split("/")[-1].split("|")
                address_zip_data = [trim(data) for data in address_zip_data if data and len(data.replace(" ", ""))]

                args = (remove_multiple_spaces(str(row[0])),
                        remove_multiple_spaces(str(row[5])),
                        remove_multiple_spaces(str(business_name)),
                        remove_multiple_spaces(str(owner)),
                        " ".join(address_zip_data[0:-3]),
                        address_zip_data[-3],
                        address_zip_data[-2],
                        address_zip_data[-1])

                db.run_insert_query(args)
                inserted = inserted + 1
            except:
                pass

        print("There are {} rows inserted".format(inserted))
