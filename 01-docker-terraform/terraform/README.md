### Khái niệm
* [Terraform_overview](../12-terraform-overview.md)
* Nếu bạn không thể tạo tệp khóa tài khoản dịch vụ do chính sách tổ chức, hãy tham khảo hướng dẫn [bên dưới](#fallback)

### Thực thi

```shell
# Refresh service-account's auth-token for this session
gcloud auth application-default login

# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"
```

```shell
# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```

```shell
# Delete infra after your work, to avoid costs on any running services
terraform destroy
```

### Cảnh báo
Hãy nhớ sử dụng tệp [gitignore](https://github.com/github/gitignore/blob/main/Terraform.gitignore) phù hợp trước khi xuất bản mã của bạn trên GitHub

### Dự phòng
1. Hãy tự đặt cho mình vai trò người tạo mã thông báo trên tài khoản dịch vụ thích hợp
    ```bash
    gcloud iam service-accounts add-iam-policy-binding \
        <SERVICE_ACCOUNT_EMAIL> \
        --member="user:YOUR_EMAIL@gmail.com" \
        --role="roles/iam.serviceAccountTokenCreator"
    ```
2. Thêm các phần bên dưới khối đầu tiên vào cấu hình Terraform chính của bạn
   ```terraform
    # Connect to gcp using ADC (identity verification)
    provider "google" {
      project = var.project
      region  = var.region
      zone    = var.zone
    }

    /* add these data blocks */
    
    # This data source gets a temporary token for the service account
    data "google_service_account_access_token" "default" {
      provider               = google
      target_service_account = "<SERVICE_ACCOUNT_EMAIL>"
      scopes                 = ["https://www.googleapis.com/auth/cloud-platform"]
      lifetime               = "3600s"
    }
    
    # This second provider block uses that temporary token and does the real work
    provider "google" {
      alias        = "impersonated"
      access_token = data.google_service_account_access_token.default.access_token
      project      = var.project
      region       = var.region
      zone         = var.zone
    }
   ```

3. Bây giờ, bạn có thể làm theo hướng dẫn [ở trên](#execution)
