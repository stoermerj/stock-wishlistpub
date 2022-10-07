This application is a wishlist for stocks. It sends an automated update once a week per e-mail, so you don't have to manually check. 
Within the sent e-mail, it provides a quick table for its performance as well as a few charts. 

To use this application, the following steps should be followed:
1. Create an account on https://www.alphavantage.co to use their API. Retrieve the app-password and save for step 3. 
2. Create a Gmail account and generate an app-password here. https://myaccount.google.com/apppasswords. Retrieve the app-password and save for step 3. 
3. Add the generated passwords to credentials.py next to the relevant object.
4. Add the e-mail to credentials.py you would like to send the e-mail from. The app is set up in a way that the same e-mail is used for sending and receiving e-mails.
5. Define the stocks you want to follow by adding the tickers in the list STOCK_INPUT und main.py. You can get the tickers e.g from yahoo.  
6. Define the period you want to track by adding it to PERIOD_INPUT under main.py.
7. Set up a secret in github to use github actions
8. Run the program.

Note:
- Constructive feedback is welcome. 
- The period is optimized for monthly inputs. Weekly works
- Retrieving the tickers for the individual stocks may be a bit of a hustle
- wishlist_schedule.yml is set up to run manually.


