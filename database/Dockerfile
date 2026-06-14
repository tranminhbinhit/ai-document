FROM mcr.microsoft.com/mssql/server:2022-latest

# Switch to root to install packages and set permissions
USER root

# Copy initialization scripts
COPY scripts/ /docker-entrypoint-initdb.d/

# Make scripts executable
RUN chmod +x /docker-entrypoint-initdb.d/*.sh

# Copy custom entrypoint
COPY database/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to mssql user
USER mssql

# Use custom entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]