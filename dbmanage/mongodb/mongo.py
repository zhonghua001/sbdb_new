#coding=UTF-8
import MySQLdb,sys,string,time,datetime,uuid,pymongo,json
# from django.contrib.auth.models import User
from accounts.models import UserInfo
from dbmanage.myapp.models import Db_name,Db_account,Db_instance,Db_database_permission
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from dbmanage.myapp.include.encrypt import prpcrypt
from cmdb.models import Host,HostGroup
from dbmanage.myapp.include.encrypt import prpcrypt


public_user = settings.PUBLIC_USER
export_limit = int(settings.EXPORT_LIMIT)
def get_mongodb_list(request,tag='tag',search=''):
    permission_list = ''
    if tag == 'query':
        permission_list = ('read', 'read_write', 'all')
    elif tag == 'exec':
        permission_list = ('write', 'read_write', 'all')
    elif tag == 'log':
        permission_list = ('read', 'read_write', 'all')
    elif tag == 'meta':
        permission_list = ('read', 'read_write', 'all')
    elif tag == 'incep':
        permission_list = ('write', 'read_write', 'all')

    elif tag == 'admin':
        permission_list = ('admin')
    dbtype='mongodb'
    host_list = []
    if request.GET.has_key('host_group'):
        selected_group = request.GET.get('host_group')
        login_user =  request.user.username
        user_info = UserInfo.objects.get(username=login_user)
        host = Host.objects.filter(group=selected_group)
        ip_list = list(set([x.ip for x in host]))
        if tag == 'admin':
            db_instances = Db_instance.objects.filter(ip__in=tuple(ip_list), db_type='mongodb',
                                                      status='InUse', admin_user=user_info)

        else:
            db_instances = Db_instance.objects.filter(
                db_account__db_name__db_database_permission__account__id=user_info.id,
                ip__in=tuple(ip_list), db_type='mongodb', status='InUse',
                db_account__db_name__db_database_permission__permission__in=permission_list).distinct()
        db_list = []
        for instance in db_instances:
            id = instance.id
            ip = instance.ip
            port = instance.port
            explain = instance.comments
            db_list.append({'id': id, 'port': port, 'ip': ip, 'explain': explain})

        return db_list
    elif request.GET.has_key('instance_id'):
        instance_id = request.GET.get('instance_id')
        login_user = UserInfo.objects.get(username=request.user.username)

        dbs = Db_database_permission.objects.filter(account_id=login_user.id, permission__in=permission_list) \
            .filter(db_name__dbaccount__instance__id=int(instance_id)) \
            .values('db_name__dbaccount__id', 'db_name__dbaccount__db_account_role', 'db_name__dbname',
                    'db_name__dbtag')
        data = []
        for db in dbs:
            db_account_id = db['db_name__dbaccount__id']
            db_account_role = db['db_name__dbaccount__db_account_role']
            db_name = db['db_name__dbname']
            db_tag = db['db_name__dbtag']
            data.append({'db_account_id': db_account_id, 'db_account_role': db_account_role, 'db_name': db_name,
                         'db_tag': db_tag})

        return data


def get_mongo_coninfo(hosttag,useraccount):

    pc = prpcrypt()
    # a = Db_name.objects.get(dbtag=hosttag)
    db_account_id,tar_dbname = hosttag.split(':')

    db_account = Db_account.objects.get(id=int(db_account_id))
    try:
        tar_username = db_account.user
        tar_passwd = pc.decrypt(db_account.passwd)
        tar_host = db_account.instance.ip
        tar_port = db_account.instance.port
        db_tag = db_account.instance.ip + ':' + db_account.instance.port + '__' + db_account.db_account_role
        return tar_host, tar_port, tar_username, tar_passwd, tar_dbname

    except:
        pass



def get_db_info(hosttag,useraccount):
    tar_host, tar_port, tar_username, tar_passwd, tar_dbname = get_mongo_coninfo(hosttag, useraccount)
    connect = pymongo.MongoClient(tar_host, int(tar_port))
    db = connect[tar_dbname]
    try:
        db.authenticate(tar_username, tar_passwd)
    except Exception, e:
        pass
    results = db.command({'dbstats': 1})
    return results

def get_tb_info(hosttag,tbname,useraccount):
    tar_host, tar_port, tar_username, tar_passwd, tar_dbname = get_mongo_coninfo(hosttag, useraccount)
    connect = pymongo.MongoClient(tar_host, int(tar_port))
    db = connect[tar_dbname]
    try:
        db.authenticate(tar_username, tar_passwd)
    except Exception, e:
        pass
    results = db.command({'collstats': tbname})
    return results

def get_tbindex_info(hosttag,tbname,useraccount):
    tar_host, tar_port, tar_username, tar_passwd, tar_dbname = get_mongo_coninfo(hosttag, useraccount)
    connect = pymongo.MongoClient(tar_host, int(tar_port))
    db = connect[tar_dbname]
    try:
        db.authenticate(tar_username, tar_passwd)
    except Exception, e:
        pass
    collection = db[tbname]
    results = collection.index_information()
    return results

def get_mongo_collection(hosttag,useraccount):
    try:
        tar_host, tar_port, tar_username, tar_passwd, tar_dbname = get_mongo_coninfo(hosttag, useraccount)
        # 此处根据tablename获取其他信息
        connect = pymongo.MongoClient(tar_host, int(tar_port))
        db = connect[tar_dbname]
        try:
            db.authenticate(tar_username, tar_passwd)
        except Exception, e:
            pass
        results = db.collection_names()
    except Exception, e:
        results,col = ([str(e)],''),['error']
    return results


def get_mongo_data(b,hosttag,tbname,useraccount):
    try:
        num = int(UserInfo.objects.get(username=useraccount).user_profile.export_limit)
    except Exception, e:
        num = export_limit
    try:
        tar_host, tar_port, tar_username, tar_passwd, tar_dbname = get_mongo_coninfo(hosttag, useraccount)
        #此处根据tablename获取其他信息
        connect = pymongo.MongoClient(tar_host,int(tar_port))
        db=connect[tar_dbname]
        try:
            db.authenticate(tar_username,tar_passwd)
        except Exception,e:
            pass
        #tablename = tablename
        collection = db[tbname]
        #a = '''{'currTime': 1477371861706}'''
        resulta = collection.find(eval(b),{"_id":0}).limit(num)
        # resulta = collection.find().limit(20)
        #results = db.collection_names()    #获取所有tables名字
        results = []
        for recordjson in resulta:
            #resultdict = {}
            #for k,v in recordjson:
            #    resultdict[k] = v.encode('gb18030')    #["ObjectId('580ee6e6f3de9821b20e57db') is not JSON serializable"]
            results.append(json.dumps(recordjson,ensure_ascii=False,cls=DjangoJSONEncoder))
            #results.append(recordjson)
    except Exception, e:
        results = (['error'],'')
    return results

if __name__ == '__main__':
    #x="insert /*sdfs*/into mysql.test ;truncate table mysql.db;rename mysql.db ;rename asdf;delete from  `msql`.sa set ;delete ignore from t1 mysql.test values sdasdf;insert into ysql.user values()"
    # print x
    #x=" /*! */; select /**/ #asdfasdf; \nfrom mysql_replication_history;"
    #x = " insert into item_infor (id,name) values(7,'t\\'e\"st');drop t * from test;"

    print  get_mongo_data('{"_class" : "com.mongodb.BasicDBObject"}','mongodb-easemob','message','root')