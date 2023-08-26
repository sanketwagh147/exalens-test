# Exalens Demo Project

  
    
## Simple Architecture Diagram

![alt text](architechture/architechture.png?)


### To Get Started:
- Run `docker-compose up -d`  
- Visit http://localhost:8000 to check the dashboard
- keep running for a while so there would be enough readings to filter
### Or checkout live-demo of dashboard <Strong>[Here](https://www.sanketwagh.com/exalens-demo)</Strong>


### Add Devices

- To add more publishers(sensors) copy any device block in `docker-compose` and tweak environment variables as required which will spin up another container and start publishing to the broker

# Adding More Publishers (Sensors)

To add more publishers (sensors), you can copy any device block in the `docker-compose.yml` file and tweak the environment variables as required. This will spin up another container and start publishing to the broker.

<details>
<summary><strong>Device </strong></summary>

```yaml
  device_05:
    build:
      context: ./publishers/sensor
    container_name: device_05
    networks:
      - my-mosquitto
    environment:
      - FREQUENCY=120
      - RANGE=-10,30
      - SENSOR_ID=sensor_temperature_03
      - SENSOR_TYPE=temperature
      - PYTHONUNBUFFERED=1



