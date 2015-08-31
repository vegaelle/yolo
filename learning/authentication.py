from django.contrib.auth.backends import ModelBackend


class RowLevelPermissionBackend(ModelBackend):

    def has_perm(self, user_obj, perm, obj=None):
        has_perm = super().has_perm(user_obj, perm)
        if has_perm:
            if hasattr(obj, 'is_owned') and callable(obj.is_owned):
                return obj.is_owned(user_obj, perm)
        return has_perm
