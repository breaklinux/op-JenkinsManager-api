resultJobInfo="http://192.168.58.125:8080/job/sec-service-web/9/"
appname="sec-service-web"
# appname="sec-service-web"
# resultJobInfo="""http://192.168.58.125:8080/job/{appname}/detail/{appname}/9/""".format(appname=appname)
# newstr=resultJobInfo.replace("/job","/blue/organizations/jenkins")
# print(newstr)
# http://192.168.58.125:8080/blue/organizations/jenkins/sec-service-web/detail/sec-service-web/4/pipeline


def formatResultStrTwo(data, appname):
    from urllib.parse import urlparse
    o = urlparse(data)
    print(o.hostname)
    print(o.path)
    print(o.port)
    print(o.scheme)
    new=o._replace(path="/blue/organizations/jenkins/{appname}/detail/".format(appname=appname))
    print(new)




formatResultStrTwo(resultJobInfo,appname)
