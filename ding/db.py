from utils.settings import location_dict
from ding.models import Location
for key in location_dict :
    value = ''
    for ele in location_dict[key]:
        value += ele + '\n'
    print(key)
    print(value)
    print('-'*10)
    Location.objects.get_or_create(location=key, SNcode=value)
