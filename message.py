

#           +---------------+-------+---------+
#           |          Name | label | Type    |
#           +---------------+-------+---------+
#           |     Base Name | bn    | String  |
#           |     Base Time | bt    | Number  |
#           |     Base Unit | bu    | String  |
#           |    Base Value | bv    | Number  |
#           |      Base Sum | bs    | Number  |
#           |       Version | bver  | Number  |
#           |          Name | n     | String  |
#           |          Unit | u     | String  |
#           |         Value | v     | Number  |
#           |  String Value | vs    | String  |
#           | Boolean Value | vb    | Boolean |
#           |    Data Value | vd    | String  |
#           |     Value Sum | s     | Number  |
#           |          Time | t     | Number  |
#           |   Update Time | ut    | Number  |
#           |          Link | l     | String  |
#           +---------------+-------+---------+

class Message:
    def __init__(self, channel, publisher, protocol,
                        b_name=None, b_time=0, b_unit=None, b_value=None,
                        b_sum=None, b_ver=5, name=None, unit=None, value=None,
                        str_value=None, bool_value=None, data_value=None,
                        sum=None, time=0, upd_time=None, link=None):
        self._channel = channel
        self._publisher = publisher
        self._protocol = protocol
        self._b_name = b_name
        self._b_time = b_time
        self._b_unit = b_unit
        self._b_value = b_value
        self._b_sum = b_sum
        self._b_ver = b_ver
        self._name = name
        self._unit = unit
        self._value = value
        self._str_value = str_value
        self._bool_value = bool_value
        self._data_value = data_value
        self._sum = sum
        self._time = time
        self._upd_time = upd_time
        self._link = link

    def get_channel(self):
        return str(self._channel)

    def get_publisher(self):
        return str(self._publisher)

    def get_protocol(self):
        return str(self._protocol)

    def get_name(self):
        if self._b_name:
            if self._name:
                return str(self._b_name) + '/' + str(self._name)
            else:
                return str(self._b_name)
        elif self._name:
            return str(self._name)
        else:
            return 'pub_' + str(self._publisher)

    def get_time(self):
        return self._b_time + self._time

    def get_unit(self):
        if self._unit:
            return str(self._unit)
        elif self._b_unit:
            return str(self._b_unit)
        else:
            return None

    def get_value(self):
        if self._value:
            if self._b_value:
                return float(self._value) + float(self._b_value)
            else:
                return float(self._value)
        elif self._str_value:
            return str(self._value)
        elif self._bool_value:
            return bool(self._value)
        elif self._data_value:
            return str(self._value)
        else:
            return None

    def get_sum(self):
        if self._b_sum:
            if self._sum:
                return float(self._sum) + float(self._b_sum)
            else:
                return float(self._b_sum)
        elif self._sum:
            return float(self._sum)
        else:
            return None

    def get_version(self):
        return self._b_ver

    def get_update_time(self):
        return self._upd_time
