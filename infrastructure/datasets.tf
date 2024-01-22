# These datasets need to be created in your project prior to 
# running the ELT pipeline

# Production dataset
resource "google_bigquery_dataset" "prod_dataset" {
    dataset_id = "raw__nyk_data"
    friendly_name = "[PROD] Raw NYK Data"
    description = "Output dataset for production ELT runs"
    location = "US"
    default_table_expiration_ms = null

    # TODO: Make this modular + play with groups
    access {
        role = "OWNER"
        user_by_email = "IANFERGUSONRVA@gmail.com"
    }

    access {
        role = "READER"
        domain = "hashicorp.com"
    }
  
}

# Testing dataset
resource "google_bigquery_dataset" "dev_dataset" {
    dataset_id = "raw__nyk_data__test"
    friendly_name = "[DEV] Raw NYK Data"
    description = "Output dataset for development ELT runs"
    location = "US"
    default_table_expiration_ms = null

    access {
        role = "OWNER"
        user_by_email = "IANFERGUSONRVA@gmail.com"
    }

    access {
        role = "READER"
        domain = "hashicorp.com"
    }
  
}