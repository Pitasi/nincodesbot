# [@nincodesbot](https://t.me/nincodesbot) 🤖

A Telegram bot for easily share Nintendo friend's code with others.

This bot uses https://nin.codes as a database, all my thanks go to [Jimmy
Roland](https://jimmyroland.com/) who created it.


## Bot usage

This is an inline bot. Start writing `@nincodesbot someusername` in any chat.

If _someusername_ is registered in https://nin.codes just tap the button that
appears to share its friend code.


## Developers info

This project uses Python's [poetry](https://python-poetry.org), start the bot
with a couple commands:
```
$ poetry install
$ TOKEN=1234-abcdef poetry run ./main.py
```


## TODO

PRs are welcome! They are pretty easy tasks.

1. I'd like to add a LRU cache for usernames. Since the friend codes are not
   supposed to change frequently, a long-lived cache can prevent tons of API
   request.

   Probably the entire database can easily fit in RAM :)


2. I want users to be able to share their own friend code without having to
   write their username all the times.

   This can be implemented by having a small database containing a map 
   {Telegram ID -> Nintendo Username}.

   Having that, the bot can remember the username of a user even if they don't
   provide an inline query.
