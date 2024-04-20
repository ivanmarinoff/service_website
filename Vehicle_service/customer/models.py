from Vehicle_service.admin_user import models


class Customer(models.Customer):
    class Meta:
        proxy = True
