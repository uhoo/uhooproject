#-*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _


GENERAL_STATUS_CHOICES= (
    ('A', _('Active')),
    ('I', _('Inactive')),
)
GENERAL_STATUS_ACTIVE = 'A'
GENERAL_STATUS_INACTIVE = 'I'

POINTS_GROUP_ACTION= (
    (1, _('Join')),
    (2, _('Like')),
    (4, _('Share')), 
    (8, _('Post')),
    (16, _('Invite')),
    (32, _('Buy')),    
)

ACTION_TYPE_JOIN = 1
ACTION_TYPE_LIKE = 2
ACTION_TYPE_SHARE = 4
ACTION_TYPE_POST = 8
ACTION_TYPE_INVITE = 16
ACTION_TYPE_BUY = 32


GENERAL_PRIVACY= (
    ('DF', _('Default')),
    ('PU', _('Public')),
    ('PR', _('Private')),
    ('FR', _('Friends')),
)

