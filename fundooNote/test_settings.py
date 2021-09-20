from .settings import *

#Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv("ENGINE") ,
        'NAME': os.getenv("TEST_DATABASE_NAME"),
        'USER': os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD"),
        'HOST': os.getenv("HOST"),
        'PORT': os.getenv("PORT"),
    }
}
