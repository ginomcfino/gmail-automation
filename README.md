# How to make an API endpoint to extract Trade Confirmations through Robinhood emails.

This repository serves as an example on how to use the gmail API with Python.

I put together a way to extract a list of stocks you have traded in the past in Robinhood programatically by reading the email confirmations sent to Gmail. You wouldn't want to use this method, as I don't, in real cases.

**NOTE:** Why is the question. Robinhood does not offer an official API and offers no developer support, we are forced to bypass it. Robinhood is also raising commission fees, making their platform less ideal. I made this as a statement. 

On the bright side, other methods such as headleass browsers have been used for the past decade to get around these un-developer-friendly plots, and many useful unofficial APIs were made avaiable thanks to that.

In order to run this code, you need to have a gmail account to receive the emails from noreply@robinhood.com. I would recommend setting up automatic email forwarding, and I will show you an example how. Let's get started.

### Step-by-Step Instructions:

1. Set up Gmail forwarding.
    - In Gmail, set up filter messages from "noreply@robinhood.com"
    - Forward to annother *new* email **(For Increased Security)**
        - You can also choose: archive, label, etc. (you won't necessary need to read them in this email anymore)
2. Sign in to the *new* email account.
    - See the Robinhood emails
3. Follow the Gmail API instructions to receive file *credentials.json*
3. Run Python Script to RETURN Trade confirmations from the emails.
    - Keep it running in the background to receive continual updates (using CRON jobs or other servers).




### Features:
* nlp regular expressions extract -- an implementation using a trained model such as SpaCy to read email text and extract the stock tickers from its syntax.
* potential for automatic forwarding -- set up a table with webhooks, and send requests to table using CRON jobs or when a new email is received.

P.S. be careful with your private keys suchs as credential.json and tokens.json, make sure they don't get uploaded to github by accident ;) happy coding!
