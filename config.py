'''

CREATE TABLE books (
  num int(11) NOT NULL AUTO_INCREMENT,
  src varchar(50) NOT NULL,
  bid varchar(50) NOT NULL,
  update_date varchar(50) NOT NULL,
  ranking varchar(50) NOT NULL,
  link varchar(100) NOT NULL,
  thumbnail varchar(100) NOT NULL,
  title varchar(100) NOT NULL,
  author varchar(50) NOT NULL,
  publisher varchar(50) NOT NULL,
  pages varchar(20) NOT NULL,
  isbn varchar(20) NOT NULL,  
  summary text NOT NULL,
  publication_date varchar(50) NOT NULL,
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='gyunseul9.c884kf3zxudy.ap-northeast-2.rds.amazonaws.com',
        user='gyunseul9',
        password='19740806',
        database='gyunseul9',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='gyunseul9.c884kf3zxudy.ap-northeast-2.rds.amazonaws.com',
        user='gyunseul9',
        password='19740806',
        database='gyunseul9',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value


