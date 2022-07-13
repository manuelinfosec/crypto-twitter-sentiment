import twint
from twint import run
import datetime

def scrape(start, finish, keyword, file_start = '', off_by = 0):
    ''' Given a start/finish datetime instance and keyword(s) to scrape for,
    search and return a dictionary with first key as start date '''
    # Initialize twint configuration
    c = twint.Config()
    c.Search = keyword
    c.Pandas = True
    # c.Hide_output = True
    # c.Retries_count = 100
    # c.Count = True #To ensure running

    # Filename equals start time if this is first time scraping
    if file_start == '':
        file_start = start
    # If script killed mid-day, num_per_day is non-zero
    num_per_day = off_by
    
    # timedelta value
    time_span = finish - start
    # Increment by a timedelta value of 1 hour
    # incr = start + datetime.timedelta(hours = 1)
    incr = finish

    # Create file write num_per_day for each day in file and name by start date
    # Use second file to keep track of parameters if terminated early
    filename = str(keyword) + '_' + str(file_start)[:10] + '.txt'
    file = open(filename, 'a')
    
    # Increment start/finish dates until the end date is reached
    while time_span != datetime.timedelta(0):
        # Use new start, incr values to search
        start_new = str(start)
        incr_new = str(incr)
        # print(incr_new)
        print("currently at", start_new, "to", incr_new)
        c.Since = start_new
        c.Until = incr_new
        print(c.Since)
        print(c.Until)
        twint.run.Search(c)
        # Store tweets in a variable, keep track of number of tweets
        tweets = twint.storage.panda.Tweets_df
        num_per_day += len(tweets)

        # If no tweets were returned, try the same search again
        if len(tweets) == 0:
            try_again = input('Potential server error, retry? (y/n): ')
            # try_again = 'y' # For mindless running
            # print('Potential server error, trying again') # For mindless running
            if try_again == 'y':
                continue
            else:
                print('Connection error')
                break
        
        # If hour & min = 0, day has changed. Thus, reset num_per_day vals
        # and increment key counter
        if incr.hour == 0 and incr.minute == 0:
            file.write(str(num_per_day) + '   ' + str(start)[:10] + '\n')
            file.close
            file = open(filename, 'a')
            num_per_day = 0

        # After a search has been conducted, keep track of where to pick up
        # again if terminated early.
        # After search & num_per_day reset to ensure that num_per_day is
        # the sum of tweets thus far on that day with start time incr
        file2 = open(str(keyword) + '_terminated.txt', 'w')
        file2.write(str(incr) + '  ' + str(num_per_day)) # time for next start
        file2.close
            
        # decrease time discrepancy and increment start, incr
        time_span = time_span - datetime.timedelta(hours = 1)
        start = incr
        # print(start) # Can comment out
        incr = incr + datetime.timedelta(hours = 1)
        # print(incr) # Can comment out
        
    file.write(str(num_per_day) + '   ' + str(start)[:10] + '\n')
    file.close
    
    return True

# Sources/Libraries
''' https://docs.python.org/3/library/datetime.html#examples-of-usage-timedelta
https://github.com/twintproject/twint '''
