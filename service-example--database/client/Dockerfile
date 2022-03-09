# Use a tiny linux distribution
FROM curlimages/curl

# Create a folder where DAFNI will pick up output files
USER root
RUN mkdir -p /data/outputs/ && chown curl_user: /data/outputs/

# Copy the file to use to connect to the database...
USER curl_user
COPY use_database.sh /use_database.sh

# ...and then run the file
CMD ["/bin/sh", "-c", "/use_database.sh"]
