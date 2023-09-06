# config.py

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 'postgresql://zee:7S3IPPVJAIJrHuMZnv2YYFhUWLhMz31T@dpg-cjj781ephtvs73af5bm0-a.oregon-postgres.render.com:5432/dipolevibe'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
