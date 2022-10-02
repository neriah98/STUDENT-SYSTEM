from django.core.exceptions import ValidationError


def validate_user_mail(value):
        if "@ufs.ac.za" or "@ufs4life.ac.za" in value:
            return value
        else:
            raise ValidationError("Only emails with @ufs.ac.za and @ufs4life.ac.za are allowed" )
