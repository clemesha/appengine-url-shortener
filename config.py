import os

SITE = {
    "base_url":"http://example.com/",
    "max_stats":100,
    "debug":os.environ['SERVER_SOFTWARE'].startswith('Dev')
}
