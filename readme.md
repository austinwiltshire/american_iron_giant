![American Iron Giant](https://m.media-amazon.com/images/M/MV5BMTQ5NTM4NTY5MV5BMl5BanBnXkFtZTgwOTg2Mzc2NjE@._V1_QL75_UX500_CR0,0,500,281_.jpg)

This repo houses a bot that assists the American Iron Front discord server.

Currently, it:
- Scrapes images from the protest-pictures channel and emails them for analysis

To install:

```
git clone git@github.com:austinwiltshire/american_iron_giant.git
cd american_iron_giant
pip -r requirements.txt
```

You'll need to fill in the `env_template` file with your Discord and SMTP credentials, then rename it to `.env`.

To run:

```
python main.py
```

Logging will go to the screen.
