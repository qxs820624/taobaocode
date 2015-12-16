from taocode2.contrib.oss import oss_api
from taocode2 import settings

def get_oss_api():
    api = oss_api.OssAPI(access_id=settings.OSS_ID, 
                     secret_access_key=settings.OSS_KEY)
    return api

def add_file(fname, fobj):
    api = get_oss_api()
    resp = api.put_object_with_data(settings.OSS_NAME, fname, fobj)
    if resp.status != 200:
        raise Exception('add_file fail! code:%d len:%d %s'%(resp.status, len(fobj), fname))

def get_file(fname):
    api = get_oss_api()
    resp = api.get_object(settings.OSS_NAME, fname)
    return resp

