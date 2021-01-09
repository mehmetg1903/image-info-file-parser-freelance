from ..util.string_helper import remove_multiple_spaces
import pandas as pd
import numpy as np


class TarrantParser:

    def __init__(self, file_name):
        self._df = pd.read_csv(file_name, sep='|')
        self._df = self._df.replace(np.nan, '', regex=True)

    def parse(self, db):
        inserted = 0
        for index, row in self._df.iterrows():
            try:
                args = (remove_multiple_spaces(str(row.Instrument)),
                        remove_multiple_spaces(str(row.File_Received)),
                        remove_multiple_spaces(str(row.Business_Name)),
                        remove_multiple_spaces(str(row.Owner_First_Name) + " " + str(row.Owner_Last_Name)),
                        remove_multiple_spaces(str(row.Owner_Address_1) + " " + str(row.Owner_Address_2)),
                        remove_multiple_spaces(str(row.Owner_City)),
                        remove_multiple_spaces(str(row.Owner_State)),
                        remove_multiple_spaces(str(row.Owner_Zip)))
                db.run_insert_query(args)
                inserted = inserted + 1
            except:
                pass

        print("There are {} rows inserted".format(inserted))
