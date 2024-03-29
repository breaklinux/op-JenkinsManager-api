from flask import Blueprint
from flask import request, Response, current_app
from JenkinsManager.jenkinsApi.jenkinsApi import JeninsDeploy
from tools.config import cicdMgHeader

jenkinsUrl = Blueprint('jenkins', __name__)


@jenkinsUrl.route('/api/v1', methods=['GET', 'POST', 'DELETE'])
def jenkinsRun():
    import json
    if request.method == "GET":
        # job = JeninsDeploy()
        # return job.getAllJob()
        return cicdJobsQuery()
    elif request.method == "POST":
        Data = request.get_json()
        env = Data.get('env', None)
        appname = Data.get('appname', None)
        appversion = Data.get('appversion', None)
        branch = Data.get('branch', None)
        instance_ip = Data.get('instance_ip', None)
        giturl = Data.get('giturl', None)
        language_type = Data.get('language_type', None)
        release_type = Data.get('release_type', None)
        release_reason = Data.get('release_reason', None)
        instance_ip = ','.join(instance_ip)
        if appname and appversion and branch and instance_ip and giturl and language_type and release_type and release_reason:
            job = JeninsDeploy()
            jenkins_callback = job.jenkinsCreateJob(appname)
            job.jenkinsBuildJob(appname, appversion, giturl, branch, language_type, instance_ip)
            resultData = job.getJobInfo(appname)
            jenkinsCallbackUrl = formatResultStr(resultData,appname)
            print(jenkinsCallbackUrl)

            result = cicdJobsInsert(env, appname, appversion, branch, instance_ip, giturl, language_type, release_type,
                                    jenkins_callback, release_reason)
            return Response(json.dumps({"code": 0, "data": result, "msg": "create jobs sucess","callbackUrl":jenkinsCallbackUrl}),
                            mimetype="application/json")

        else:
            parameterInfo = "无效参数,请检查"
            return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    elif request.method == "DELETE":
        Data = request.get_json()
        appname = Data.get('appname', None)
        deletjos = JeninsDeploy()
        return deletjos.jenKinsdeleteJob(appname)


def cicdJobsQuery():
    """
    1.查询有目前有哪些应用
        :return:
    """
    import json
    from models import cicdmg
    queryData = cicdmg.query.all()
    pagesize = request.args.get('psize', 5, type=int)
    page = request.args.get('page', 1, type=int)
    if page and pagesize:
        pagination = cicdmg.query.order_by(cicdmg.releasetime.desc()).paginate(page, per_page=pagesize, error_out=False)
        cicdData = pagination.items
    else:
        parameterInfo = "参数不足或错误,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')
    return Response(
        json.dumps({"code": 0, "total": len(queryData), "data": [i.to_dict() for i in cicdData],
                    "columns": cicdMgHeader}),
        mimetype='application/json')


def cicdJobsInsert(env, appname, appversion, branch, instance_ip, giturl, language_type, release_type, release_reason,
                   jenkins_callback=None):
    """
    1.发布任务创建参数入库
     :param env:
    :param appname:
    :param appversion:
    :param branch:
    :param instance_ip:
    :param giturl:
    :param language_type:
    :param release_type:
    :param release_reason:
    :return:
    """

    from models import db
    from models import cicdmg
    try:
        cicdmagDataInsert = cicdmg(env=env, appname=appname, appversion=appversion, branch=branch,
                                   instance_ip=instance_ip, giturl=giturl, language_type=language_type,
                                   release_type=release_type, jenkins_callback=jenkins_callback,
                                   release_reason=release_reason)
        db.session.add(cicdmagDataInsert)
        db.session.commit()
        return True

    except Exception as e:
        print(e)
        current_app.logger.warning("cicd data add failure  Exception" + str(e))
        return False


def cicdJobsUpdate():
    pass


def cicidJobDelete():
    pass

def formatResultStr(data,appname):
    """
    1.url替换修改并完成字符串拼接
    2.拼接完成示例:http://192.168.58.125:8080/blue/organizations/jenkins/sec-service-web/detail/sec-service-web/4/pipeline
    :param data:
    :param appname:
    :return:
    """
    from urllib.parse import urlparse
    tempData=data.split('/',-2)
    nuber=tempData[-2]
    o = urlparse(data)
    resultJobInfo =o.scheme + "://" + o.hostname + ":" + str(o.port) + """/job/{appname}/detail/{appname}/{nuber}""".format(appname=appname,nuber=nuber)
    newstr = resultJobInfo.replace("/job", "/blue/organizations/jenkins")
    return newstr


@jenkinsUrl.route('/api/v2', methods=['GET', 'POST', 'DELETE'])
def jobOpsRun():
    import json
    if request.method == "GET":
        job = JeninsDeploy()
        return job.getAllJob()
    elif request.method == "POST":
        pass
    elif request.method == "DELETE":
        pass
    else:
        parameterInfo = "不支持该方法,请检查"
        return Response(json.dumps({"code": 1, "data": parameterInfo}), mimetype='application/json')


