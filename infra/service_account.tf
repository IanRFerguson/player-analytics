locals {
  service_account_roles = [
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser"
  ]
}

resource "google_service_account" "service_account" {
  account_id   = "sa-nba-analytics"
  display_name = "NBA Analytics Service Account"
}

resource "google_project_iam_member" "service_account_roles" {
  for_each = toset(local.service_account_roles)
  project  = "nba-player-analytics"
  role     = each.value
  member   = "serviceAccount:${google_service_account.service_account.email}"
}

resource "google_service_account_key" "my_key" {
  service_account_id = google_service_account.service_account.name
}

resource "local_file" "default" {
  content  = base64decode(google_service_account_key.my_key.private_key)
  filename = "../service_accounts/nba-analytics.json"
}
