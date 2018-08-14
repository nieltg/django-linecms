# django-linecms

[![Build Status](https://travis-ci.org/nieltg/django-linecms.svg?branch=master)](https://travis-ci.org/nieltg/django-linecms)
[![Coverage Status](https://coveralls.io/repos/github/nieltg/django-linecms/badge.svg?branch=master)](https://coveralls.io/github/nieltg/django-linecms?branch=master)

> Ever wanted to create a LINE bot but doesn't want to type any code? This repository might be helpful for you.

**django-linecms** is a content management system for LINE bot by using Django admin page.

## Demo

A sample bot is available in [this link](https://line.me/R/ti/p/BObdVFGbW-) or can be scanned from the QR code below.

![django-linecms-demo LINE Bot QR code](https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://line.me/R/ti/p/BObdVFGbW-)

The admin page is available here: https://django-linecms-demo.now.sh/admin

```
username: demo
password: django-linecms
```

This demo is powered by these free online services:

- [Travis CI](https://travis-ci.org/) for CI/CD things
- [Now by Zeit](https://zeit.co/now) for the deployment
- [mLab](https://mlab.com/) for the database provider

## In The Future

- Add more message types like template messages, carousel, etc.
- Add Android activity-like management (stackable) to handle interaction with the bot.
- Add code integration so several responses can be coded in Python.

## License

[MIT](License)
