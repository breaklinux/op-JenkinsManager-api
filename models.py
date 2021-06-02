"""
@author:lijx
@contact: 360595252@qq.com
@site: http://blog.51cto.com/breaklinux
@version: 1.0
"""
# -*- coding: utf-8 -*-
import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class cicdmg(db.Model):
    __tablename__ = "cicdmg"
    id = db.Column(db.Integer, primary_key=True)
    env = db.Column(db.String(1024), nullable=False)
    appname = db.Column(db.String(1024), nullable=False)
    appversion = db.Column(db.String(1024), nullable=False)
    branch = db.Column(db.String(1024), nullable=False)
    instance_ip = db.Column(db.Text, nullable=False)
    giturl = db.Column(db.Text, nullable=False)
    language_type = db.Column(db.String(1024), nullable=False)
    release_type = db.Column(db.String(1024), nullable=False)
    release_reason = db.Column(db.Text, nullable=False)
    jenkins_callback = db.Column(db.Text, nullable=False)
    releasetime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "env": self.env, "appname": self.appname, "appversion": self.appversion,
                "branch": self.branch, "instance_ip": self.instance_ip,
                "giturl": self.giturl, "language_type": self.language_type, "release_type": self.release_type,
                "release_reason": self.release_reason, "callback": self.jenkins_callback, "releasetime": str(self.releasetime)}


class appmg(db.Model):
    __tablename__ = "appname"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(1024), nullable=False)
    appname = db.Column(db.String(4096), nullable=False)
    apptype = db.Column(db.String(1024), nullable=False)
    giturl = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(256), nullable=False)
    used = db.Column(db.Text, nullable=False)
    createtime = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def to_dict(self):
        return {"id": self.id, "department": self.department, "appname": self.appname, "apptype": self.apptype,
                "giturl": self.giturl, "owner": self.owner, "used": self.used, "createtime": str(self.createtime)}

    def to_appNameList(self):
        return {"env": self.appname}
