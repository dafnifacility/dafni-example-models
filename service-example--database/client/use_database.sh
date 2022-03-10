echo "Influx IP Is ${INFLUX_IP}"

# Create a database (if it doesn't already exists)
curl -XPOST "http://${INFLUX_IP}:8086/query" --data-urlencode "q=CREATE DATABASE mydb"

# Add a random number to the database
curl -XPOST "http://${INFLUX_IP}:8086/write?db=mydb" -d "numbers value=$((RANDOM % 100))"

# Save data to data.json
curl --silent -G "http://${INFLUX_IP}:8086/query?pretty=true" --data-urlencode "db=mydb" --data-urlencode "q=SELECT * FROM numbers" | tee /data/outputs/data.json