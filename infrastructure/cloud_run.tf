resource "google_cloud_run_service" "production" {
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
