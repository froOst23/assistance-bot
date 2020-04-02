# assistance_bot

### Description
It's just a bot for telegram which, using the coordinates provided by the user, shows the temperature.
### Deploy
For deployment on the [Heroku](https://www.heroku.com/) service, terraform v0.12 was used.

[:page_facing_up: Procfile](https://github.com/froOst23/assistance_bot/blob/master/Procfile), [:page_facing_up: requirements.txt](https://github.com/froOst23/assistance_bot/blob/master/requirements.txt) [Heroku](https://www.heroku.com/) uses them as service files, all the necessary information can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python)

In file [variables-example.txt](https://github.com/froOst23/assistance_bot/blob/master/terraform/variables-example.txt) it's worth noting the description of internal secrets for [:page_facing_up: assistance_bot.py](https://github.com/froOst23/assistance_bot/blob/master/assistance_bot.py)

```
variable "sensitive_config_vars" {
  default = {
    "SECRET" = "KEY"
    "SECRET" = "KEY"
    "SECRET" = "KEY"
  }
}
```
These secrets are recorded to [Heroku](https://www.heroku.com/) Config Vars.
