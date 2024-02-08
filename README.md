# VPN-Service
Project Setup This project uses environment variables for configuring the connection to the PostgreSQL database and other configuration parameters.

Generating the SECRET_KEY To generate a unique SECRET_KEY, you can use the built-in Django tool:
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' Copy the generated key.

Creating the .env File Create the .env file based on .env_example. Set values for the following environment variables:
POSTGRES_HOST: The PostgreSQL database host. POSTGRES_USER: The PostgreSQL database user. POSTGRES_PASSWORD: The PostgreSQL database password. POSTGRES_DB: The PostgreSQL database name. POSTGRES_PORT: The PostgreSQL database port. PGADMIN_DEFAULT_EMAIL: The default email for PGAdmin. PGADMIN_DEFAULT_PASSWORD: The default password for PGAdmin. PGADMIN_LISTEN_PORT: The PGAdmin listening port. SECRET_KEY: The Django secret key. An example content of the .env file:

POSTGRES_HOST=localhost POSTGRES_USER=my_postgres_user POSTGRES_PASSWORD=my_postgres_password POSTGRES_DB=my_database POSTGRES_PORT=5432 PGADMIN_DEFAULT_EMAIL=admin@example.com PGADMIN_DEFAULT_PASSWORD=admin_password PGADMIN_LISTEN_PORT=5050 SECRET_KEY=<generated_secret_key>
