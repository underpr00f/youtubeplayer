"""Python Social Auth Pipeline Extensions"""

from social_core.backends.google import GoogleOAuth2
from social_core.backends.twitter import TwitterOAuth

from social_core.backends.vk import VKOAuth2
from social_core.backends.odnoklassniki import OdnoklassnikiOAuth2
#from social.backends.facebook import Facebook2OAuth2


def socialprofile_extra_values(backend, details, response, uid, user, *args, **kwargs):
    """Routes the extra values call to the appropriate back end"""
    if type(backend) is GoogleOAuth2:
        google_extra_values(backend, details, response, uid, user, *args, **kwargs)

    if type(backend) is TwitterOAuth:
        twitter_extra_values(backend, details, response, uid, user, *args, **kwargs)

    if type(backend) is VKOAuth2:
        vk_extra_values(backend, details, response, uid, user, *args, **kwargs)

    if type(backend) is OdnoklassnikiOAuth2:
        odnoklassniki_extra_values(backend, details, response, uid, user, *args, **kwargs)

'''
    if type(backend) is Facebook2OAuth2:
        facebook_extra_values(backend, details, response, uid, user, *args, **kwargs)
'''

def google_extra_values(backend, details, response, uid, user, *args, **kwargs):
    """Populates a UserProfile Object when a new User is created via Google Auth"""
    profile = user.social_profile
    if not profile.manually_edited:
        user.last_name = response.get('name').get('familyName', '')
        user.first_name = response.get('name').get('givenName', '')
        user.save()

        profile.gender = response.get('gender', '')
        profile.image_url = response.get('image').get('url', '')
        profile.url = response.get('url', '')
        profile.description = response.get('occupation', '')

        profile.save()

def vk_extra_values(backend, details, response, uid, user, *args, **kwargs):
    """Populates a UserProfile Object when a new User is created via Facebook Auth"""
    profile = user.social_profile
    if not profile.manually_edited:
        user.last_name = response.get('last_name', '')
        user.first_name = response.get('first_name', '')
        user.save()

        #не работает
        profile.url = response.get('url', '')
        #не работает
        profile.description = response.get('occupation', '')
        
        profile.image_url = response.get('photo','')
        #В контакте пол 1 - женский, 2- мужской
        if response.get('sex', '') == 1:
            sex = 'Женский'
        elif response.get('sex', '') == 2:
            sex = 'Мужской'
        else:
            sex = 'Другой'
        profile.gender = sex
            
        profile.save()

def odnoklassniki_extra_values(backend, details, response, uid, user, *args, **kwargs):
    profile = user.social_profile
    
    if not profile.manually_edited:
        user.last_name = response.get('last_name', '')
        user.first_name = response.get('first_name', '')
        user.save()

        #не работает
        profile.url = response.get('url', '')
        #не работает
        profile.description = response.get('occupation', '')
        
        profile.image_url = response.get('pic_3','')
        profile.gender = response.get('gender', '')
            
        profile.save()


    
'''
def facebook_extra_values(backend, details, response, uid, user, *args, **kwargs):
    """Populates a UserProfile Object when a new User is created via Facebook Auth"""
    profile = user.social_profile
    if not profile.manually_edited:
        user.last_name = response.get('last_name', '')
        user.first_name = response.get('first_name', '')
        user.save()

        profile.gender = response.get('gender', '')
        profile.url = response.get('link', '')
        if response.get('picture', False):
            profile.image_url = response.get('picture').get('data').get('url', '')

        profile.save()

    return response
'''

def twitter_extra_values(backend, details, response, uid, user, *args, **kwargs):
    profile = user.social_profile
    if not profile.manually_edited:
        try:
            first_name, last_name = response.get('name', '').split(' ', 1)
        except:
            first_name = response.get('name', '')
            last_name = ''
        user.last_name = last_name
        user.first_name = first_name
        user.save()

        profile.url = response.get('url', '')
        profile.image_url = response.get('profile_image_url_https', '')
        profile.description = response.get('description', '')

        profile.save()

    return response
