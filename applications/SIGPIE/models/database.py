# Conectar al banco de datos
# Establecer opciones de DAL

# db = DAL(uri, pool_size, check_reserved, migrate_enabled)

db = DAL(**config.db)


