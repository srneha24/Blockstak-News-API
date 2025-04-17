from .vars import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD


TORTOISE_CONFIG = {
    "connections": {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': DB_HOST,
                'port': DB_PORT,
                'user': DB_USERNAME,
                'password': DB_PASSWORD,
                'database': DB_NAME,
            }
        }
    },
    'apps': {
        'models': {
            'models': ["models", "aerich.models"],
            'default_connection': 'default',
        }
    }
}
