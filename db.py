import pymysql

class DBConnection:
	def __init__(self,host,user,password,database,charset,port):
		self.connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			db=database,
			charset=charset,
			port=port,
			cursorclass=pymysql.cursors.DictCursor)

	def exec_select_books(self,bid,update):
		with self.connection.cursor() as cursor:
			query = Query().get_select_books(bid,update)
			cursor.execute(query)
			for row in cursor:
				data = row.get('cnt')
		return data	

	def exec_insert_books(self,src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date): 
		query = Query().get_insert_books(src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date) 
		with self.connection as cur:
			cur.execute(query)

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

class Query:
	def get_select_books(self,bid,update):
		query = 'select \
		count(*) as cnt \
		from books \
		where bid={} and update_date=\'{}\''.format(bid,update)

		return query

	def get_insert_books(self,src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date):
		query = 'insert into books (src,bid,update_date,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,publication_date) \
		values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'.format(src,bid,update,ranking,link,thumbnail,title,author,publisher,pages,isbn,summary,date)

		return query		