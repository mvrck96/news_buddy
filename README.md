# news_buddy
NameError: name 'news_buddy' is not defined

## Set up

Easy way:
1. `git clone https://github.com/mvrck96/news_buddy`
2. `pip install -r requirements.txt`
3. `cd news_buddy`
4. Add your token to `token.txt`
5. Run `python bot.py`

Docker way:
1. Make sure that docker is installed
2. Repeat steps 1-3 from easy way installation
3. `docker build -t newsbuddy .`
4. `docker run --name=NB -d newsbuddy`
5. Voila ! Bot is running now

> To view logs run `docker attach NB`