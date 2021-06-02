from flask import Blueprint
from flask import request, Response, current_app
from flask_paginate import Pagination, get_page_parameter
appMgUrl = Blueprint('app', __name__)
from tools.config import appMgHeader

@appMgUrl.route('/api/v1', methods=['GET', 'POST', 'DELETE','PUT'])
def appmgRun():
    """
    1.查询app项目默认一页5条数据
    2.创建app项目,判断是否存在该应用存在直接返回,不存在进行创建，
    3.修改app项目信息,
    4.删除app项目
    :return:
    """
    import json
    from models import appmg
    if request.method == "GET":
        return qeuryApp()
    elif request.method == "POST":
        Data = request.get_json()
        appname = Data.get('appname', None)
        department = Data.get('department', None)
        giturl = Data.get('giturl', None)
        apptype = Data.get("apptype", None)
        owner = Data.get("owner", None)
        used = Data.get("used", None)

        if appname and department and giturl and apptype and owner and  used:
            queryAppname = appmg.query.filter(appmg.appname == appname).all()
            if queryAppname:
                msg = "appname {app} existing".format(app=appname)
                return Response(json.dumps({"code": 1, "data": msg}), mimetype='application/json')
            else:
                reults = appDataAdd(appname,department,giturl, apptype, owner,used)
                data = {"code": 0, "data": reults, "message":"data insert success","appname":appname}
                return Response(json.dumps(data), mimetype='application/json')
        else:
            parameterInfo = "无效参数,请检查"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')

    elif request.method == "PUT":
         Data = request.get_json()
         id = Data.get("id")
         appname = Data.get('appname', None).strip()
         department = Data.get('department', None).strip()
         giturl = Data.get('giturl', None).strip()
         apptype = Data.get("apptype", None).strip()
         owner = Data.get("owner", None).strip()
         used = Data.get("used", None)
         if appname and giturl and apptype and used and id:
            reults=editAppdata(appname,department,giturl, apptype, owner,used,id)
            return Response(json.dumps(reults), mimetype='application/json')

    elif request.method == "DELETE":
        return deletapp()

def qeuryApp():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    from models import appmg
    queryData = appmg.query.all()
    pagesize = request.args.get('psize', 5, type=int)
    page = request.args.get('page', 1, type=int)
    if page and pagesize:
        pagination = appmg.query.order_by(appmg.createtime.desc()).paginate(page, per_page=pagesize, error_out=False)
        appData = pagination.items
    else:
        parameterInfo = "参数不足或错误,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    return Response(
        json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in appData],
                    "columns": appMgHeader}),
        mimetype='application/json')


def editAppdata(appname,department,giturl, apptype, owner,used,id):
    from models import db
    from models import appmg
    """
    1.id 更新应用信息,修改数据
    """
    try:
        appmg.query.filter_by(id=id).update({"department": department,"appname": appname, "apptype": apptype, "giturl": giturl, "owner": owner, "used": used})
        msg = "Update Success"
        db.session.commit()
        return {"code": 0, "data": True, "message": msg ,"appname":appname}

    except Exception as e:
        print(e)
        current_app.logger.warning("update appname info failure" + str(e))
        return {"code": 1, "data": None, "message": str(e)}


def appDataAdd(appname,department,giturl, apptype, owner,used):
    """
      1.app应用信息录入
      :param env:
      :param upname:
      :param giturl:
      :param apptype:
      :param used:
      :return:
      """
    from models import db
    from models import appmg
    try:
        appDataInsert = appmg(department=department,appname=appname,apptype=apptype, giturl=giturl, owner=owner,used=used)
        db.session.add(appDataInsert)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        current_app.logger.warning("app data add failure  Exception" + str(e))
        return False


def deletapp():
    from models import db
    from models import appmg
    import json
    try:
        Data = request.get_json()
        Id = Data.get('id', None)
        deleteData = appmg.query.get(Id)
        if deleteData:
            db.session.delete(deleteData)
            db.session.commit()
            data = {"code": 0, "date": True, "message": "delete success"}
            current_app.logger.warning("delele data suceess")
        else:
            current_app.logger.warning("match data failure")
            data = {"code": 0, "date": False, "message": "match data failure "}
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        current_app.logger.warning("args Parameters of the abnormal")
        data = {"code": 500, "data": "delete appname faild", "message": str(e)}
        return Response(json.dumps(data), mimetype='application/json')

