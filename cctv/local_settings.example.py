# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "t6e%#%(w!lg1@1bk1$lhh%q_d4h&z*s3utakds-bzu-3b(bebe"
NEVERCACHE_KEY = "dit-cgsc$(w%xx)z*=l1-1vtz%a6v1hwhv9jtlsm0_kcg(md0z"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
ALLOWED_HOSTS_PRODUCTION = ["example.com", ]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

FABRIC = {
    "DEPLOY_TOOL": "git",  # Deploy with "git", "hg", or "rsync"
    "SSH_PASS": "yourpass",  # SSH password (consider key-based authentication)
    "REPO_PATH": "git@github.com:linuxluigi/Django_CCTV.git",  # Github Repo
    "SSH_USER": "pi",  # VPS SSH username
    "HOSTS": ["django-cctv"],  # The IP address of your VPS
    "DOMAINS": ALLOWED_HOSTS_PRODUCTION,  # Edit domains in ALLOWED_HOSTS
    "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
    "LOCALE": "de_DE.UTF-8",  # Should end with ".UTF-8"
    "DB_PASS": "h@cn8ExAvdFg!AFWyRULgOqdnXGS!@hcbEJumZSzoHL57Nrj7LwFaLtgo2UC",  # Live database password
    "ADMIN_PASS": "3zX4sMLTbM@M5wxd4e39dCDp5cN!lBVOcFia$U8uJN9X4^r0comSY%1S^bigyo99!s&Yau",  # Live admin user password
    "SECRET_KEY": SECRET_KEY,
    "NEVERCACHE_KEY": NEVERCACHE_KEY,
    "NGINX_AUTH_USER": "user",
    "NGINX_AUTH_PASS": "w4$Y%nMtu!W&04XiWPOFY6OZxVchx5",
    "CLOUDFLARE_ZONE": "example.com",
    "CLOUDFLARE_SUBDOMAIN": "cctv",
    "CLOUDFLARE_EMAIL": "name@server.com",
    "CLOUDFLARE_TOKEN": "0000000000000000000000000000000000000",
}
