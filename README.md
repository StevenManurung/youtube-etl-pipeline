<img width="981" height="248" alt="Screenshot 2026-07-10 052805" src="https://github.com/user-attachments/assets/61a89124-af0c-416c-96d0-511c6ba613ba" />

## connect to ec2
ssh -i "airflow_ec2_key.pem" ubuntu@ec2-(ip server).ap-southeast-2.compute.amazonaws.com

## update and install
- sudo apt get-update
- sudo apt update && sudo apt install python3-venv -y
- mkdir my_airflow && cd my_airflow
- python3 -m venv airflow_env
- source airflow_env/bin/activate
- pip install apache-airflow
