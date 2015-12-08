#
# svnd.py wsgi svn creator
# apache + mod_wsgi
# 
# luqi@taobao.com 2015
# 
# .apache config
#
# SetEnv REPOS_PATH /data/svn_part_path/
# WSGIScriptAlias / file_to_svnd.py
# <Directory path_to_svnd>
#   Order allow,deny
#   Allow from all
# </Directory>
#
# .query string:
#
# /svnd/{PRJ_NAME}/(new|del)
# /svn/{PRJ_NAME}/
# 

import os
import time
import traceback
import subprocess
import wsgiref
import shutil

SVN_ADMIN='svnadmin'

def exec_cmd(args, std_in = None):

    utf8_args = []
    for arg in args:
        if type(arg) != unicode:
            utf8_args.append(arg)
            continue
        try:
            u = arg.encode('utf8')
            utf8_args.append(u)
        except:
            utf8_args.append(arg)
    args = utf8_args
    p = subprocess.Popen(args,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out,err = p.communicate(std_in)
    
    code = p.wait()
    return code, out,err

def init_local_repos(admin, path):
    r, out, err = exec_cmd([admin, 'create', path])
    if r != 0:
        raise Exception(err)

    exec_cmd(['svn', 'mkdir', 'file://'+path+'/trunk', '-m', 'initial commit', '--username','""'])

def del_local_repos(prj_path):
    timetag = time.strftime('%Y-%m-%d-%H-%M-%S',
                            time.localtime(time.time()))
    del_name = prj_path + '_D_' + timetag
    shutil.move(prj_path, del_name)
    
def do_svnd(env):
    uri = env['PATH_INFO']
    args = [u for u in uri.split('/') if len(u) > 0]
    #hello, new
    
    if len(args) != 2:
        raise Exception('Invalid PATH_INFO:%s'%(uri, ))

    action = args[1].lower()
    prj_name = os.path.normpath(args[0])
    repos_path = env.get('REPOS_PATH', '/tmp/repos')

    if os.path.exists(repos_path) is False:
        os.makedirs(repos_path)

    prj_path = os.path.join(repos_path, prj_name)
    admin_path = env.get('SVN_ADMIN', SVN_ADMIN)

    if action == 'new':
        if os.path.exists(prj_path):
            raise Exception ('%s is exist!'%(prj_path,))
        init_local_repos(admin_path, prj_path)
    elif action == 'del':
        if os.path.exists(prj_path) is False:
            return
        del_local_repos(prj_path)

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    output = 'Done'

    try:
        do_svnd(environ)
    except Exception,e:
        #todo: log it!
        status = '500 Server Error'
        output = ''.join(traceback.format_exc())

    start_response(status, headers)

    return [output]

#if __name__ == '__main__':
#    from wsgiref.simple_server import make_server
#    httpd = make_server('', 8000, application)
#    print "Serving on port 8000..."
#    httpd.serve_forever()

