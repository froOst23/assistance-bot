# main.tf

# Configure the Heroku provider
provider "heroku" {
  email = "${var.heroku_account_email}"
  api_key = "${var.heroku_api_key}"
}

# Configure assistance-bot-tf app
resource "heroku_app" "develop" {
  name = "assistance-bot-tf"
  region = "eu"
  sensitive_config_vars = "${var.sensitive_config_vars}"
}

# Configure build
resource "heroku_build" "develop" {
  app = "${heroku_app.develop.name}"
  buildpacks = ["https://github.com/heroku/heroku-buildpack-python"]
  source = {
    url = "https://github.com/froOst23/assistance_bot/archive/v1.0.tar.gz"
    version = "v1.0"
  }
}