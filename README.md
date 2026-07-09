## 📖 Overview
 
This project is an End-to-End Data Pipeline (ETL) designed to automatically extract comment data from YouTube, process it into a structured format, and store it in AWS S3 cloud storage. The entire infrastructure is deployed on Amazon EC2, containerized with Docker, and orchestrated using Apache Airflow — making the whole workflow reproducible, schedulable, and ready to scale into analytics or machine learning use cases.
 
## 🏗️ Architecture
 
<div align="center">
  <!-- If you upload the diagram to this repo, replace the URL below with your own image path, e.g. <img src="docs/architecture.png" alt="Architecture"> -->
  <img width="981" height="248" alt="YouTube ETL pipeline architecture diagram" src="https://github.com/user-attachments/assets/61a89124-af0c-416c-96d0-511c6ba613ba" />
</div>

## 🧰 Tech Stack
 
Here's the role each technology plays in the pipeline:
 
| Technology | Role in the Pipeline |
|---|---|
| **YouTube Data API v3** | Data source — extracts thousands of comments (author, publish time, like count, comment text) from a target video. |
| **Python & Pandas** | ETL engine — `etl_youtube.py` fetches JSON from the YouTube API, transforms it into a tabular `DataFrame`, and loads it to storage via `s3fs`. |
| **Amazon EC2** | Cloud host — a 24/7 virtual server that runs the whole automation stack without using local machine resources. |
| **Docker & Docker Compose** | Containerization — packages Airflow, PostgreSQL (metadata DB), and Redis (message broker) into isolated, reproducible containers, avoiding dependency conflicts. |
| **Apache Airflow** | Orchestration & scheduling — schedules script runs (e.g. a daily cron schedule), monitors task status, and automatically retries failed API calls. |
| **Amazon S3** | Data lake — the final destination for processed `.csv` files; secure, durable, and scalable storage ready for downstream analytics or ML. |
 
## 📁 Project Structure
 
```text
youtube-etl-pipeline/
├── dags/
│   └── dag_youtube.py          # Airflow DAG definition (orchestration)
├── scripts/
│   └── etl_youtube.py          # Core ETL logic (Extract & Load to S3)
├── docker-compose.yaml         # Container infrastructure config (Airflow, Postgres, Redis)
├── requirements.txt            # Additional Python dependencies (s3fs, google-api-python-client)
└── .env                        # Environment variables (AIRFLOW_UID, credentials) — not committed to git
```
 
## ✅ Prerequisites
 
- An AWS account with permission to create EC2 instances, IAM roles, and S3 buckets
- An EC2 **key pair** (`.pem` file) for SSH access
- A **YouTube Data API v3** key (Google Cloud Console → APIs & Services → Credentials)
- **Git** installed locally
- Basic familiarity with the Linux command line


### Getting a YouTube Data API v3 Key
 
1. Open [Google Cloud Console](https://console.cloud.google.com) and create (or select) a project.
2. Go to **APIs & Services → Library**, search for **YouTube Data API v3**, and click **Enable**.
3. Go to **APIs & Services → Credentials → Create Credentials → API key**.
4. *(Recommended)* Edit the key → under **API restrictions**, restrict it to **YouTube Data API v3** only, and optionally add IP restrictions.
5. Copy the key into your `.env` file as `YOUTUBE_API_KEY`.
> Note: the default quota is **10,000 units/day**. Most `commentThreads.list` calls cost only a few units each, so this is usually enough for scraping comments from a single video — request a quota increase if you're pulling from high-traffic videos at scale.

## 🚀 Setup and Deployment Guide

### Step 1: Launch an EC2 Instance
1. In the AWS Console, go to **EC2 → Launch Instance** (Ubuntu is recommended).
2. Create or select an existing key pair — you'll need the `.pem` file to SSH in later.
3. Launch the instance and wait until its state is **Running**.
### Step 2: Configure IAM Permissions
The instance needs permission to manage S3 and EC2 resources:
1. Select the instance → **Actions → Security → Modify IAM role**.
2. If no role exists yet, create one, then attach these policies:
   - `AmazonS3FullAccess`
   - `AmazonEC2FullAccess`
> ⚠️ These are broad, account-wide policies — fine for learning or a demo. For anything production-facing, scope a custom policy down to just the S3 bucket and actions the pipeline actually needs.
 
### Step 3: Connect via SSH
In Windows connect to wsl: wsl --cd //wsl.localhost and go to your project with file airflow_ec2_key.pem to access the EC2 AWS server
```bash
ssh -i "airflow_ec2_key.pem" ubuntu@ec2-<your-public-ip>.ap-southeast-2.compute.amazonaws.com
```
Replace `airflow_ec2_key.pem` with your own key file, and `<your-public-ip>` with the instance's public IPv4 address (dashes instead of dots — the full hostname is shown on the instance's **Connect** tab). Adjust the region (`ap-southeast-2`) if your instance is elsewhere.
 
### Step 4: Install Docker & Docker Compose
```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```
*(If `docker-compose-plugin` isn't available for your Ubuntu version, follow Docker's official install guide for Ubuntu instead.)*
 
### Step 5: Create an S3 Bucket
Create a bucket (via the S3 Console or AWS CLI) to receive the pipeline's output `.csv` files. Keep the bucket name handy for the `.env` file in the next step.
 
### Step 6: Clone the Repository & Configure Environment
```bash
git clone https://github.com/StevenManurung/youtube-etl-pipeline.git
cd youtube-etl-pipeline
```
Create a `.env` file in the project root — see [Environment Variables](#-environment-variables) below for what to include.
 
### Step 7: Build and Run with Docker Compose
```bash
docker compose up -d --build
```
Confirm every container is healthy before continuing:
```bash
docker compose ps
```
 
### Step 8: Access Airflow & Trigger the DAG
1. Open `http://<your-ec2-public-ip>` in your browser.
2. Log in (check `docker-compose.yaml` / the airflow-init step for the default username and password if you haven't changed them).
3. Find the DAG defined in `dags/dag_youtube.py`, toggle it **on**, and trigger a run.
4. Watch task status in the **Grid** / **Graph** view until the run finishes successfully.
### Step 9: Verify the Output
Check your S3 bucket — the processed `.csv` file from this run should now be there.
 
## 🔐 Environment Variables
 
Create a `.env` file in the project root. Based on the scripts and dependencies involved, you'll need something along these lines:
 
```env
# Airflow
AIRFLOW_UID=1000
 
# YouTube Data API
API_TOKEN = 'your_youtube_api_key'
FERNET_KEY = 'your_fernet_key'
 
# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=your_bucket_name
AWS_REGION=ap-southeast-2
```
 
> Double-check these variable names against what `etl_youtube.py` and `dag_youtube.py` actually read in your code, and adjust as needed. Add `.env` to `.gitignore` so credentials never get committed.
 
---
 
Built by [Steven Manurung](https://github.com/StevenManurung)
