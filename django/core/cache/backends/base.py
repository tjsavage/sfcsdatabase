"Base Cache class."

import warnings

from django.core.exceptions import ImproperlyConfigured, DjangoRuntimeWarning

class InvalidCacheBackendError(ImproperlyConfigured):
    pass

class CacheKeyWarning(DjangoRuntimeWarning):
    pass

# Memcached does not accept keys longer than this.
MEMCACHE_MAX_KEY_LENGTH = 250

class BaseCache(object):
    def __init__(self, params):
        timeout = params.get('timeout', 300)
        try:
            timeout = int(timeout)
        except (ValueError, TypeError):
            timeout = 300
        self.default_timeout = timeout

        max_entries = params.get('max_entries', 300)
        try:
            self._max_entries = int(max_entries)
        except (ValueError, TypeError):
            self._max_entries = 300

        cull_frequency = params.get('cull_frequency', 3)
        try:
            self._cull_frequency = int(cull_frequency)
        except (ValueError, TypeError):
            self._cull_frequency = 3

    def add(self, key, value, timeout=None):
        """
        Set a value in the cache if the key does not already exist. If
        timeout is given, that timeout will be used for the key; otherwise
        the default cache timeout will be used.

        Returns True if the value was stored, False otherwise.
        """
        raise NotImplementedError

    def get(self, key, default=None):
        """
        Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
        raise NotImplementedError

    def set(self, key, value, timeout=None):
        """
        Set a value in the cache. If timeout is given, that timeout will be
        used for the key; otherwise the default cache timeout will be used.
        """
        raise NotImplementedError

    def delete(self, key):
        """
        Delete a key from the cache, failing silently.
        """
        raise NotImplementedError

    def get_many(self, keys):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        Returns a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        d = {}
        for k in keys:
            val = self.get(k)
            if val is not None:
                d[k] = val
        return d

    def has_key(self, key):
        """
        Returns True if the key is in the cache and has not expired.
        """
        return self.get(key) is not None

    def incr(self, key, delta=1):
        """
        Add delta to value in the cache. If the key does not exist, raise a
        ValueError exception.
        """
        if key not in self:
            raise ValueError("Key '%s' not found" % key)
        new_value = self.get(key) + delta
        self.set(key, new_value)
        return new_value

    def decr(self, key, delta=1):
        """
        Subtract delta from value in the cache. If the key does not exist, raise
        a ValueError exception.
        """
        return self.incr(key, -delta)

    def __contains__(self, key):
        """
        Returns True if the key is in the cache and has not expired.
        """
        # This is a separate method, rather than just a copy of has_key(),
        # so that it always has the same functionality as has_key(), even
        # if a subclass overrides it.
        return self.has_key(key)

    def set_many(self, data, timeout=None):
        """
        Set a bunch of values in the cache at once from a dict of key/value
        pairs.  For certain backends (memcached), this is much more efficient
        than calling set() multiple times.

        If timeout is given, that timeout will be used for the key; otherwise
        the default cache timeout will be used.
        """
        for key, value in data.items():
            self.set(key, value, timeout)

    def delete_many(self, keys):
        """
        Set a bunch of values in the cache at once.  For certain backends
        (memcached), this is much more efficient than calling delete() multiple
        times.
        """
        for key in keys:
            self.delete(key)

    def clear(self):
        """Remove *all* values from the cache at once."""
        raise NotImplementedError

    def validate_key(self, key):
        """
        Warn about keys that would not be portable to the memcached
        backend. This encourages (but does not force) writing backend-portable
        cache code.

        """
        if len(key) > MEMCACHE_MAX_KEY_LENGTH:
            warnings.warn('Cache key will cause errors if used with memcached: '
                    '%s (longer than %s)' % (key, MEMCACHE_MAX_KEY_LENGTH),
                    CacheKeyWarning)
        for char in key:
            if ord(char) < 33 or ord(char) == 127:
                warnings.warn('Cache key contains characters that will cause '
                        'errors if used with memcached: %r' % key,
                              CacheKeyWarning)

