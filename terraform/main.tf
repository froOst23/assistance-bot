# main.tf

# Configure the Heroku provider
provider "heroku" {
  email = "${var.heroku_account_email}"
  api_key = "${var.heroku_api_key}"
}

# Create Heroku apps for staging and production
resource "heroku_app" "staging" {
  name = "assistance-bot-staging"
  region = "eu"
  sensitive_config_vars = "${var.sensitive_config_vars_staging}"
}

resource "heroku_app" "production" {
  name = "assistance-bot-production"
  region = "eu"
  sensitive_config_vars = "${var.sensitive_config_vars_production}"
}

# Configure build apps for staging and production
resource "heroku_build" "staging" {
  app = "${heroku_app.staging.name}"
  buildpacks = ["https://github.com/heroku/heroku-buildpack-python"]
  source = {
    url = "https://github.com/froOst23/assistance_bot/archive/v1.0.tar.gz"
    version = "v1.0"
  }
}

resource "heroku_build" "production" {
  app = "${heroku_app.production.name}"
  buildpacks = ["https://github.com/heroku/heroku-buildpack-python"]
  source = {
    url = "https://github.com/froOst23/assistance_bot/archive/v1.0.tar.gz"
    version = "v1.0"
  }
}
