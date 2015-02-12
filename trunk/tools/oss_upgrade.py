# migrate local file into oss
#
from taocode2.contrib import oss_store
from taocode2.models import *
from taocode2.apps.main.files import get_upload_root
import time
import os,sys
import binascii

def upgrade_all(test=True):
    files = ProjectAttachment.objects.all()
    for f in files:
        fname = f.fname.encode('utf8')
        if fname.startswith('oss://'):
            print 'pass', fname
            continue
        tstr = '%s_%s'%(f.ctime.day, f.ctime.hour)
        ranname = binascii.hexlify(os.urandom(12)) 
        orig_name = f.orig_name
        ext = os.path.splitext(orig_name)[1]

        oname = '%s-%s/%s_%s%s'%(f.ctime.year, 
                                 f.ctime.month, tstr, ranname, ext)
        new_name = 'oss://'+oname
        fdata = file(os.path.join(get_upload_root(), fname),'rb').read()

        if test is False:
            oss_store.add_file(oname, fdata)
            f.fname = new_name
            f.save()

        print fname, new_name

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'true':
        upgrade_all(False)
    else:
        print 'tring runing'
        upgrade_all(True)


