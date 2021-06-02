"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
from models import db
from __init__ import create_app
app = create_app()
with app.app_context():
    db.create_all()

