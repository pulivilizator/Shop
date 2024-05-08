from .likes import Likes

def likes(request):
    return {'likes': Likes(request)}