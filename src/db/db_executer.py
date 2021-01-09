import pymssql


class DB:
    def __init__(self, table_name, **kwargs):
        self._conn = pymssql.connect(host=kwargs["server"], user=kwargs["username"], password=kwargs["password"])
        print("Connection established: Server: " + kwargs["server"])
        self._table_name = table_name
        if eval(kwargs["prevent_duplicate"]):
            self._prepare_tables()
            print("Duplicate keys prevention handled...")

    def _prepare_tables(self):
        delete_duplicates_query = """WITH CTE AS(
               SELECT *,
                   RN = ROW_NUMBER()OVER(PARTITION BY Document_Number ORDER BY Document_Number)
               FROM {}
            )
            DELETE FROM CTE WHERE RN > 1;""".format(self._table_name)
        self._run_query(delete_duplicates_query)
        try:
            insert_identity_constraint = """alter table {} add constraint DocNumUniqueConst unique(Document_Number);""".format(
                self._table_name)
            self._run_query(insert_identity_constraint)
        except:
            print("Uniqueness is already defined. No need...")

    def _run_query(self, query, args=()):
        self._cursor().execute(query, tuple(args))

    def _cursor(self):
        return self._conn.cursor()

    def run_insert_query(self, args):
        query = "INSERT INTO {0} (Document_Number, Filing_Date, Name, Owner, Address, City, State, Zip) values(%s, %s, %s, %s, %s, %s, %s, %s)".format(
            self._table_name)
        self._run_query(query, args)

    def close(self):
        try:
            self._conn.commit()
        except:
            pass
        self._conn.close()
