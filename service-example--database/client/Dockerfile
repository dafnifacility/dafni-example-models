# Use a tiny linux distribution
FROM curlimages/curl
USER root

RUN mkdir -p /data/outputs/
COPY use_database.sh /use_database.sh

# Run a file with database access
CMD ["/bin/sh", "-c", "/use_database.sh"]
