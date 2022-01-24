# Use a tiny linux distribution
FROM alpine

# Print the IP of the service model.
CMD ["/bin/sh", "-c", "ping -c 10 ${MY_SERVICE_IP} | tee /data/outputs/ping.txt"]
