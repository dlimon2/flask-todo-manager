class Config:
    SECRET_KEY = 'SuperSecureString'
    #Configuración DB
    SQLALCHEMY_DATABASE_URI  = "mariadb+mariadbconnector://root:123@127.0.0.1:3306/agenda_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False