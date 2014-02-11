To create sql schema follow these steps


If your postgresql database admin username/password is not postgres/postgres 
update mangod.conf before running 'create schema' dbAdminUser=postgres dbAdminPassword=postgres

# Note
You can also create the database by running sql scripts in psql

    cd schema
    psql -U postgres -f mango.sql
