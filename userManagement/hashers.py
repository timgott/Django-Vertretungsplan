from hashlib import sha1
from functools import reduce

from django.utils.crypto import (
    constant_time_compare, get_random_string, pbkdf2,
)
from django.contrib.auth.hashers import (mask_hash, BasePasswordHasher)
from django.utils.translation import gettext_noop as _


class SHA1DoubleSaltPasswordHasher(BasePasswordHasher):
    """
    The SHA1 password hashing algorithm (not recommended)
    """
    algorithm = "sha1ds"

    def encode(self, password, salt):
        assert password is not None
        assert salt and '$' not in salt
        hash = sha1((salt + sha1((salt + sha1(password.encode()).hexdigest()).encode()).hexdigest()).encode()).hexdigest()
        return "%s$%s$%s" % (self.algorithm, salt, hash)

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt)
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        algorithm, salt, hash = encoded.split('$', 2)
        assert algorithm == self.algorithm
        return {
            _('algorithm'): algorithm,
            _('salt'): mask_hash(salt, show=2),
            _('hash'): mask_hash(hash),
        }

    def harden_runtime(self, password, encoded):
        pass
