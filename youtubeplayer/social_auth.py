# Python Socialauth Settings
# Модель пользователя. Здесь стандартная.
import os

#secrets
SECRET_KEY = 'a6587vu2uxg!zi3e*h!n!u%2t4=6hsrs38up7vwfc+-11w99g0'
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'underproof$youtubedb',
        'USER': 'underproof',
        'PASSWORD': 'F0rc0sigan',
        'HOST': 'underproof.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {'charset': 'utf8mb4'},

    }
}
FILE_CHARSET='utf-8'
DEFAULT_CHARSET='utf-8'

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "underproof2017@gmail.com"
EMAIL_HOST_PASSWORD = 'Helloworld'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
AUTH_USER_EMAIL_UNIQUE = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
'''

#DJANGO_AUTH_MODEL="socialprofile.User"
#AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_USER_MODEL = 'auth.User'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '742588645289-4092qk72icimvdnclvpc4ibns6p5tnt4'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'UKEI9q2UyFOKbnja8oM5MG7W'

SOCIAL_AUTH_VK_OAUTH2_KEY = '5874489'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '1a9axAcECf1dYjRKPd1q'
#указываем запрашиваемые поля
SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = ['sex',]
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email',]

SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = '1249860352' 
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = '6230905239628845F1E33470'
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = 'CBAMFQHLEBABABABA'
#SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_EXTRA_DATA = ['email','GET_EMAIL',]
SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SCOPE = ['GET_EMAIL'] #получить можно только через Support

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    )
AUTH_PROFILE_MODULE = 'socialprofile.SocialProfile'
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_ALWAYS_ASSOCIATE = True

# Проверка url перенаправления
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
# Важно указать последовательность (и порядок) процедур,
# которые будут выполнятся в pipeline (конвейере) авторизации.
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.mail.mail_validation',
    #'socialprofile.pipeline.create_user',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    #'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    
    'socialprofile.pipeline.socialprofile_extra_values',
    'social.pipeline.debug.debug',
   
    
)

# Настройки для username #
# При значении True SOCIAL_AUTH_SLUGIFY_USERNAMES, вы можете получить username 
# не в том виде, в котором ожидали (даже если провайдер предоставил 
# соответствующее поле) — вы получите случайную строку,
# длины определенной в SOCIAL_AUTH_UUID_LENGTH (Facebook).
SOCIAL_AUTH_SLUGIFY_USERNAMES = True
SOCIAL_AUTH_CLEAN_USERNAMES = True

# Проверяем ссылку редиректа, которую мы отправляли провайдеру,
# с той что мы получили. Можно эту задачу оставить провайдеру.
SOCIAL_AUTH_SANITIZE_REDIRECTS = True
#защита от изменений полей
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

'''
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.debug.debug',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'socialprofile.pipeline.socialprofile_extra_values',
    'social_core.pipeline.debug.debug'
)
'''

'''
# FACEBOOK
# Только для facebook, указываем запрашиваемые поля
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email',
}
# Разрешение на получение поля email

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
'''

'''
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/secure/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/secure/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/secure/'

# Core Authentication Settings
LOGIN_URL          = '/socialprofile/select/'
LOGIN_REDIRECT_URL = '/secure/'
LOGIN_ERROR_URL    = '/socialprofile/select/'
'''
