import os


class Config:
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"  # os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:4586@localhost/sims"  # os.environ.get('DB_URI')
