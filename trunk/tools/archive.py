import argparse
import os
import sys
import glob
import time

os.environ['DJANGO_SETTINGS_MODULE'] = 'taocode2.settings'

from taocode2.contrib import oss_store
from taocode2.helper import utils

def check_is_done(root_dir, done_file):
    resp = oss_store.get_file(os.path.join(root_dir, done_file))
    if resp.status == 200:
        return True
    return False
                              

def archive_repos(root_dir, r, tmp_dir):
    #print root_dir, r
    parent, name = os.path.split(r)

    ar_name = name + '.tar.gz'
    done_file = ar_name + '.done'
    
    if check_is_done(root_dir, done_file):
        return

    args = ['tar', 'zcf', os.path.join(tmp_dir, ar_name),
            '-C', parent, name]

    code, out, err = utils.exec_cmd(args)
    if code != 0:
        raise Exception('exec fail! code:%s err:%s args:%s'%(code, err, repr(args)))

    # upload to oss
    #
    #
    # REPOS/YYYY-MM-DD/parent/directory.tar.gz
    # REPOS/YYYY-MM-DD/parent/directoyr.tar.gz.done
    #

    try:
        oss_store.add_local_file(os.path.join(root_dir, ar_name),
                                 os.path.join(tmp_dir, ar_name))
        
        oss_store.add_file(os.path.join(root_dir, done_file),
                           'DONE')
    finally:
        utils.exec_cmd(['rm', os.path.join(tmp_dir, ar_name)])
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive directory to OSS.')
    parser.add_argument('--parent',help='parent directory')
    parser.add_argument('--tmp', default='/tmp/', help='tmp dir')
    
    args = parser.parse_args()
    
    if args.tmp is None or args.parent is None:
        parser.print_help()
        sys.exit(1)

    root_dir = os.path.join(time.strftime('%Y-%m-%d'), os.path.split(args.parent)[1])
    root_dir = os.path.join('REPOS', root_dir)
    repos = glob.glob(os.path.join(args.parent,'*'))

    for r in repos:
        try:
            archive_repos(root_dir, r, args.tmp)
        except Exception, e:
            print >> sys.stderr, e
