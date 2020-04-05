# pipeline.tf

# Create a Heroku pipeline
resource "heroku_pipeline" "pipeline-app" {
  name = "${var.heroku_pipeline_name}"
}

# Couple apps to different pipeline stages
resource "heroku_pipeline_coupling" "staging" {
  app = "${heroku_app.staging.id}"
  pipeline = "${heroku_pipeline.pipeline-app.id}"
  stage = "staging"
}

resource "heroku_pipeline_coupling" "production" {
  app = "${heroku_app.production.id}"
  pipeline = "${heroku_pipeline.pipeline-app.id}"
  stage = "production"
}