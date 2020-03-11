class PoliticCenterQueries:
    def get_user_info_by_id(self, user_id, mysql):
        user = None
        cur = mysql.connection.cursor()
        sql = "select * from users where id = %s"
        adr = (user_id,)
        cur.execute(sql, adr)
        data = cur.fetchall()
        keys = ('id', 'username', 'pass_hash')
        for value in data:
            dictionary = dict(zip(keys, value))
            user = dictionary
        mysql.connection.commit()
        cur.close()
        return user

    def get_user_info(self, username, mysql):
        user = None
        cur = mysql.connection.cursor()
        sql = "select * from users where username = %s"
        adr = (username,)
        cur.execute(sql, adr)
        data = cur.fetchall()
        keys = ('id', 'username', 'pass_hash')
        for value in data:
            dictionary = dict(zip(keys, value))
            user = dictionary
        mysql.connection.commit()
        cur.close()
        return user