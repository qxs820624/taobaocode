
from taocode2.models import User
from taocode2.helper import consts
from django.db.models import Q
from hashlib import md5,sha256


def md5_pwd(pwd):
    return md5('%s'%(pwd)).hexdigest()

def sha_pwd(pwd):
    return sha256(md5_pwd(pwd)).hexdigest()

def check_password(user, raw_password):
    if user.password.startswith('sha:'):
        return user.password[4:] == sha_pwd(raw_password)
    else:
        return user.password == md5_pwd(raw_password)
    
def set_password(user, new_password):
    user.password = 'sha:'+sha_pwd(new_password)

    
class UserAuthBackend:
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(Q(name__iexact=username) | Q(email__iexact=username),
                                    status = consts.USER_ENABLE)            
        except User.DoesNotExist:
            return None
                
        if user.check_password(password) is False:
            return None
        
        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None

    def has_perm(self, user, perm):
        return False
    
    def supports_object_permissions(self):
        return False

    def supports_anonymous_user(self):
        return False
