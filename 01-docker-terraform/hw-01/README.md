# Module-01 Homework

## Overview

In this homework, we prepare the environment and practice using **Docker**, **Docker Compose**, and **SQL** to work with PostgreSQL and NYC Green Taxi data.

---

## Question 1: Docker Image Inspection

**Task:**  
Run the `python:3.13` Docker image and check the installed `pip` version.

**Command:**
```bash
docker run --rm -it --entrypoint=bash python:3.13
```
```
>>>pip --version
```

**Answer:**  
```
pip 25.3
```

---

## Question 2: Docker Networking

**Task:**  
Determine the PostgreSQL hostname (the service name) and port (the port exposed by the PostgreSQL container) that pgAdmin should use when both services run on the same docker-compose network.

**Answer:**  
```
db:5432
```

---

## Environment Setup
### Option 1: Using Docker

### 1. Start Services
#### PostgreSQL


```bash
docker run -it --rm \
  -e POSTGRES_USER='root' \
  -e POSTGRES_PASSWORD='root' \
  -e POSTGRES_DB='ny_taxi_hw' \
  -v hw_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```
#### pgAdmin
```bash
docker run -it --rm \
  -e PG_DEFAULT_USER='root' \
  -e PG_DEFAULT_PASS='root' \
  -p 8080:80 \
  dpage/pgadmin4
```
#### Option 2: Using Docker Compose
```bash
docker compose up
```

### 2. Prepare ingestion script

#### Convert Jupyter Notebook to Script
```bash
uv run jupyter nbconvert --to=script hw.ipynb
```
#### Containerize and Run the Ingestion Script
Build the Docker Image
```bash
docker build -t hw_ingest:v01 .
```
Run the Ingestion Script

```bash
docker run --rm -it \
  --network='homework-01_default' \
  hw_ingest:v01 \
  --pg-user='root' \
  --pg-pass='root' \
  --pg-host='hw_db' \
  --pg-port=5432 \
  --pg-db='ny_taxi_hw'
```
> ⚠️ Make sure the network name matches your Docker Compose network.

By default, the network name is `<working_folder_name>_default` if you did not explicitly specify a network.

---

## Question 3: Counting Short Trips

```sql
SELECT count(1) as ans
FROM public.green_taxi_trips
WHERE trip_distance <= 1 
AND lpep_pickup_datetime <= '2025-12-01'
AND lpep_pickup_datetime > '2025-11-01';
```

**Answer:**  
```
8,007
```

---

## Question 4: Longest Trip per Day

```sql
SELECT 
  date(lpep_pickup_datetime) AS pu_day,
  max(trip_distance) AS longest_trip
FROM public.green_taxi_trips
WHERE trip_distance < 100
GROUP BY pu_day
ORDER BY longest_trip DESC
LIMIT 1;
```

**Answer:**  
```
2025-11-14
```

---

## Question 5: Biggest Pickup Zone

```sql
SELECT 
  cast(t.lpep_pickup_datetime as date),
  z."Zone",
  sum(total_amount) as total_amount_sum
FROM public.green_taxi_trips t
JOIN zones z 
  ON "PULocationID" = "LocationID"
WHERE cast(lpep_pickup_datetime as date) = '2025-11-18'
GROUP BY 1,2
ORDER BY total_amount_sum DESC
LIMIT 1;
```

**Answer:**  
```
East Harlem North
```

---

## Question 6: Largest Tip

```sql
SELECT 
  t.lpep_pickup_datetime,
  t.lpep_dropoff_datetime,
  t.tip_amount,
  t."DOLocationID",
  zdo."Zone",
  zdo."LocationID"
FROM public.green_taxi_trips t
JOIN public.zones zpu 
  ON t."PULocationID" = zpu."LocationID"
JOIN public.zones zdo
  ON t."DOLocationID" = zdo."LocationID"
WHERE zpu."Zone" = 'East Harlem North'
AND cast(t.lpep_pickup_datetime as date) > '2025-10-31'
AND cast(t.lpep_pickup_datetime as date) < '2025-12-01'
ORDER BY t.tip_amount DESC
LIMIT 1;
```

**Answer:**  
```
Yorkville West
```

## Question 7: Terraform Workflow

**Answer:**  
```
terraform init, terraform apply -auto-approve, terraform destroy
```