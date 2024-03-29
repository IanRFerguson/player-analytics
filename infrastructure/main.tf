terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file("../service_accounts/nba-player-analytics-service.json")

  project = "nba-player-analytics"
  region  = "us"
  zone    = "us"
}
