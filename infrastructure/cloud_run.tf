# resource "google_cloud_run_service" "production" {
#   name     = "player-analytics-service"
#   location = "us-central1"

#   template {
#     spec {
#       containers {
#         image = "docker.io/ianrichardferguson/nba-player-analytics"
#       }
#     }
#   }

#   traffic {
#     percent         = 100
#     latest_revision = true
#   }
# }
