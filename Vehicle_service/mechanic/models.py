from Vehicle_service.admin_user import models
# from Vehicle_service.admin_user.models import Mechanic


class MechanicModel(models.Mechanic):
    class Meta:
        proxy = True


class RequestModel(models.Request):
    class Meta:
        proxy = True


class AttendanceModel(models.Attendance):
    class Meta:
        proxy = True


class FeedbackModel(models.Feedback):
    class Meta:
        proxy = True
