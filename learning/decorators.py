from django.contrib.auth.decorators import login_required, user_passes_test


def student(fn):
    return login_required(
        user_passes_test(lambda u: u.member.type == 'student' and
                         u.groups.count() == 1)(fn))


def teacher(fn):
    return login_required(
        user_passes_test(lambda u: u.member.type == 'teacher')(fn))


def manager(fn):
    return login_required(
        user_passes_test(lambda u: u.member.type == 'admin')(fn))
