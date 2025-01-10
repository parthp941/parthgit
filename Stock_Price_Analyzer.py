import os  # env. var.
import yfinance as yf  # stockdata
import smtplib  # send email
from email.mime.text import MIMEText  # email format
import time  # price check 

Email_Add = os.getenv("EMAIL_ADDRESS")  
Email_Pass = os.getenv("EMAIL_PASSWORD")  
SMTP_SERVER = "smtp.gmail.com"  #gmail SMTP Server
SMTP_PORT = 587  #port num. for SMTP

def send_email(user_email, stock, curr_price, target_price):
        rounded_stock_price = round(curr_price,2)
        subject = f"STOCK ALERT: {stock} has reached your target price of: {target_price}!"
        body = (
    f"ALERT! The stock has hit your target price.\n"
    f"Stock: {stock}\n"
    f"{stock} has reached your target price of {target_price}\n"
    f"Current Price: {rounded_stock_price}\n\n"
   
)

        email = MIMEText(body)  #create blank body text
        email['Subject'] = subject 
        email['From'] = Email_Add  
        email['To'] = user_email  
       
      
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as email_server:
            email_server.starttls()
            email_server.login(Email_Add, Email_Pass)
            email_server.send_message(email)


def track_stocks(stocksinfo, user_email):
    while True:  
        stocks_picked=[]
        for stock, targets in stocksinfo.items():  
            
                ticker = yf.Ticker(stock)
                curr_price = ticker.history(period="1d")['Close'].iloc[-1] # get the closing price of the last day 

                upper_target, lower_target = targets  

                if curr_price >= upper_target:
                    send_email(user_email, stock, curr_price,upper_target)
                    stocks_picked.append(stock)  # add stock to removal list 

                # Check if the stock price drops below the lower target
                elif curr_price <= lower_target:
                    send_email(user_email, stock, curr_price,lower_target)
                    stocks_picked.append(stock)  # add stock to removal list 


        for stock in stocks_picked:
         del stocksinfo[stock] #delete stocks already chosen


        if not stocksinfo:  
            break
        time.sleep(60)  #Checks every minute



def main():
    stocksinfo = {}  

    user_email = input("Enter your email address to receive alerts: ") 

    while True:  
        stock = input("Enter the stock ticker: ").upper()  
        try:
           upper_target = float(input(f"Enter the price at which you want to sell {stock} (your upper target price): ")) 
           lower_target = float(input(f"Enter the price at which you want to buy {stock} (your lower target price): ")) 
           stocksinfo[stock] = (upper_target, lower_target) 
        except ValueError:
            print("Invalid price. Please enter a valid number.")  
            continue

        add_more = input("Do you want to track another stock? (yes/no): ").lower() 
        if add_more != 'yes':  
            break

    track_stocks(stocksinfo, user_email)  #Pass all info to above function

if __name__ == "__main__":
    main()


