from .models import UserMetaData


def user_meta_data_processor(request):
    """
    Allows user meta data for the logged in user to be available for all pages' contexts
    :param request:
    :return:
    """
    user_meta_data = None
    if request.user.is_authenticated:
        username = request.user
        user_meta_data = UserMetaData.objects.get(user_id__username__exact=username)
    return {'user_meta_data': user_meta_data}