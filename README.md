flowchart LR
    Source[YouTube API] -->|Ekstrak Komentar| ETL[Python Script]
    
    subgraph Server [Amazon EC2 Instance]
        direction TB
        subgraph Container [Docker Environment]
            Orchestrator[Apache Airflow] -.->|Menjadwalkan & Menjalankan| ETL
        end
    end
    
    ETL -->|Mengunggah File CSV| Destination[(Amazon S3)]
    
    %% Warna dan Gaya Desain
    style Source fill:#ff0000,stroke:#333,stroke-width:2px,color:#fff
    style ETL fill:#FFD43B,stroke:#306998,stroke-width:2px,color:#000
    style Orchestrator fill:#017CEE,stroke:#333,stroke-width:2px,color:#fff
    style Server fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:#000
    style Container fill:#2496ED,stroke:#0db7ed,stroke-width:2px,color:#fff
    style Destination fill:#569A31,stroke:#333,stroke-width:2px,color:#fff

## connect to ec2
ssh -i "airflow_ec2_key.pem" ubuntu@ec2-(ip server).ap-southeast-2.compute.amazonaws.com

## update and install
- sudo apt get-update
- sudo apt update && sudo apt install python3-venv -y
- mkdir my_airflow && cd my_airflow
- python3 -m venv airflow_env
- source airflow_env/bin/activate
- pip install apache-airflow
