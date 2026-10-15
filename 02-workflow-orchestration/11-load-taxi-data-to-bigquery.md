---
video_url: https://www.youtube.com/watch?v=52u9X_bfTAo
prev_url: 10-setup-google-cloud-platform.md
next_url: 12-schedule-and-backfill-full-dataset.md
---
# Quy trình làm việc của GCP: Tải dữ liệu Taxi vào BigQuery

Bây giờ Google Cloud đã được thiết lập với nhóm lưu trữ, chúng ta có thể bắt đầu quá trình ELT.


```mermaid
graph LR
  SetLabel[Set Labels] --> Extract[Extract CSV Data]
  Extract --> UploadToGCS[Upload Data to GCS]
  UploadToGCS -->|Taxi=Yellow| BQYellowTripdata[Main Yellow Tripdata Table]:::yellow
  UploadToGCS -->|Taxi=Green| BQGreenTripdata[Main Green Tripdata Table]:::green
  BQYellowTripdata --> BQYellowTableExt[External Table]:::yellow
  BQGreenTripdata --> BQGreenTableExt[External Table]:::green
  BQYellowTableExt --> BQYellowTableTmp[Monthly Table]:::yellow
  BQGreenTableExt --> BQGreenTableTmp[Monthly Table]:::green
  BQYellowTableTmp --> BQYellowMerge[Merge to Main Table]:::yellow
  BQGreenTableTmp --> BQGreenMerge[Merge to Main Table]:::green
  BQYellowMerge --> PurgeFiles[Purge Files]
  BQGreenMerge --> PurgeFiles[Purge Files]

  classDef yellow fill:#FFD700,stroke:#000,stroke-width:1px,color:#000
  classDef green fill:#32CD32,stroke:#000,stroke-width:1px,color:#000
```

Mã luồng: [`08_gcp_taxi.yaml`](flows/08_gcp_taxi.yaml).
