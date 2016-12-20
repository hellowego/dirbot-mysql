#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from hashlib import md5
class Util(object):
    '''
    工具函数
    '''

    @classmethod
    def _get_guid(self, str):
        """Generates an unique identifier for a given item."""
        # hash based solely in the url field
        return md5(str).hexdigest()