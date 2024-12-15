from django.db import models

class CustomUserInfo(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # For admin permissions
    date_joined = models.DateTimeField(auto_now_add=True)

    # def set_password(self, password):
    #     self.password = make_password(password)

    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
