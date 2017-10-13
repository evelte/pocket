import psycopg2


class DB():

    def __init__(self, database, user):
        self.database = database
        self.user = user
        self.connection = None
        self.cursor = None


    def connect(self):
        connection = psycopg2.connect(database=self.database, user='elena')
        self.connection = connection

        cursor = connection.cursor()
        self.cursor = cursor

    def query(self, query):

        if not self.connection:
            self.connect()

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()[0][0]
        except Exception as err:
            print(err)
        else:
            return result

    def execute(self, query):

        if not self.connection:
            self.connect()

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as err:
            print(err)
        else:
            return True

    def disconnect(self):
        if self.cursor:
            self.cursor.close()


if __name__ == '__main__':

    db = DB('pocket', 'elena')

    create_table = '''DROP TABLE IF EXISTS status;
                   CREATE TABLE IF NOT EXISTS status
                   (article_id INTEGER, status_update_date DATE,
                   CONSTRAINT listing_id PRIMARY KEY (article_id, status_update_date));
                   '''

    db.execute(create_table)
