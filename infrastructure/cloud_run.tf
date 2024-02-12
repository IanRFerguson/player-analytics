resource "google_cloud_run_service" "production_cloud_run" {
  name     = "player-analytics-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = local.json_data.DOCKER_IMAGE_NAME
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

#####

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.production_cloud_run.location
  project  = google_cloud_run_service.production_cloud_run.project
  service  = google_cloud_run_service.production_cloud_run.name

  policy_data = data.google_iam_policy.noauth.policy_data
}
