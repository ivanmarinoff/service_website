from Vehicle_service.admin_user import models
# from Vehicle_service.admin_user.models import Mechanic


class Mechanic(models.Mechanic):
    class Meta:
        proxy = True


class Request(models.Request):
    class Meta:
        proxy = True


class Attendance(models.Attendance):
    class Meta:
        proxy = True


class Feedback(models.Feedback):
    class Meta:
        proxy = True
