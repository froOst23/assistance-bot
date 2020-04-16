# assistance_bot

![](https://img.shields.io/github/languages/top/froOst23/assistance_bot)
![](https://img.shields.io/github/last-commit/froOst23/assistance_bot)
![](https://img.shields.io/github/repo-size/froOst23/assistance_bot)

### Description
It's just a bot for telegram which, uses the coordinates provided by user, shows the outside temperature.
### Deploy
For deployment on the [Heroku](https://www.heroku.com/) service, terraform v0.12 was used.

[Procfile](https://github.com/froOst23/assistance_bot/blob/master/Procfile), [requirements.txt](https://github.com/froOst23/assistance_bot/blob/master/requirements.txt) - [Heroku](https://www.heroku.com/) uses them as service files, all the necessary information can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python)

In file [variables-example.txt](https://github.com/froOst23/assistance_bot/blob/master/terraform/variables-example.txt) please pay attention on the internal secrets which transfer from [assistance_bot.py](https://github.com/froOst23/assistance_bot/blob/master/assistance_bot.py) to [Heroku](https://www.heroku.com/) Config Vars.

```
variable "sensitive_config_vars" {
  default = {
    "SECRET" = "KEY"
    "SECRET" = "KEY"
    "SECRET" = "KEY"
  }
}
```
