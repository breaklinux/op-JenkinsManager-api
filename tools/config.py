"""
1.登陆jenkins 账号信息配置;
"""
accUrl = "http://192.168.58.125:8080"
username = "admin"
password = "xiaolige@2020ABC"

"""
2.jenkins视图列表默认dev,test,ontest,prod 环境;
"""
viewList = ["Dev", "Test", "Ontest", "Prod"]


class MysqlConfig(object):
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "123456"
    HOST = "192.168.1.200"
    PORT = "3306"
    DATABASE = "devops-cicd-api"
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

appMgHeader=[
    {"name":"id","alias":"唯一标识"},{"name":"department","alias":"部门名称"},
    {"name":"appname","alias":"应用名称"}, {"name":"apptype","alias":"应用类型"},
    {"name":"giturl","alias":"git地址"}, {"name":"owner","alias":"应用负责人"},
    {"name":"used","alias":"用途"},{"name":"createtime","alias":"创建时间"}]

cicdMgHeader=[
    {"name": "id", "alias": "唯一标识"},{"name": "env", "alias": "发布环境"},
    {"name": "appname", "alias": "应用名称"},{"name": "appversion", "alias": "发布版本"},
    {"name": "instance_ip", "alias": "发布实例"},{"name": "giturl", "alias": "GIT地址"},
    {"name": "language_type", "alias": "语言类型"},{"name": "release_reason", "alias": "发布原因"},
    {"name": "jenkins_callback", "alias": "Jenkins返回"},{"name": "releasetime", "alias": "发布时间"},
]

