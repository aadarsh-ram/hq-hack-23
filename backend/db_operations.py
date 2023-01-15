import databases

class Database:
    def __init__(self, host, user, password, database):
        self.DATABASE_URL = f'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}'
        self.database = databases.Database(self.DATABASE_URL)
    
    async def dbs_connect(self):
        await self.database.connect()
        print ("Connected to database")
    
    async def dbs_disconnect(self):
        await self.database.disconnect()
        print ("Disconnected from database")
    
    async def create_tables(self):
        await self.database.execute(query="CREATE TABLE IF NOT EXISTS jds (id SERIAL PRIMARY KEY, jd_content TEXT, keywords TEXT);")

    async def insert_jd(self, jd_content, keywords):
        query = "INSERT INTO jds (jd_content, keywords) VALUES (:jd_content, :keywords);"
        await self.database.execute(query=query, values={"jd_content": jd_content, "keywords": keywords})

    async def get_all_jds(self):
        query = "SELECT * FROM jds;"
        res = await self.database.fetch_all(query=query)
        return res
    
    async def get_jd(self, jd_id):
        query = "SELECT * FROM jds WHERE id=:id;"
        res = await self.database.fetch_one(query=query, values={"id": jd_id})
        return res

    async def delete_jd(self, jd_id):
        query = "DELETE FROM jds WHERE id=:id;"
        await self.database.execute(query=query, values={"id": jd_id})