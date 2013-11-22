import datetime
from model import *

u = User.objects(open_id='oip_4jl7eV4_JjzmJtMb5lbLFUX0')
d = datetime.datetime.now().replace(day=21)
u.update(set__checked_at=d)
