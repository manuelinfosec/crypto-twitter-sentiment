import random
import datetime
import twint_scrape
from twint_scrape import scrape

if __name__ == '__main__':
    ''' Script to run scrape function. Picks up where killed last '''
    # Parameters for scraping
    keyword = '$RLC'
    start = datetime.datetime(year = 2020, month = 9, day = 8)
    end = datetime.datetime(year = 2021, month = 12, day = 12)

    # Ensure file exists, create if not
    file = openfile = open(str(keyword) + '_terminated.txt', 'a')
    file.close()
    # Read file of where script terminated last
    file = open(str(keyword) + '_terminated.txt', 'r')
    left_off = file.read()
    file.close()
    
    if left_off != '':
        # Determine where script was killed. If this date is after the start
        # date provided, continue where it was killed.
        
        s_year = int(left_off[:4])
        s_month = int(left_off[5:7])
        s_day = int(left_off[8:10])
        s_hour = int(left_off[11:13])
        s_minute = int(left_off[14:16])
        new_start = datetime.datetime(year = s_year, month = s_month, day = s_day,
                                    hour = s_hour, minute = s_minute)
        if start < new_start:
            # Tweets scraped thus far on date new_start
            off_by = int(left_off[20:])
            print("scraping", keyword, "from", new_start, "to", end)
            output = scrape(new_start, end, keyword, start, off_by)
        
    else:
        print("scraping", keyword, "from", start, "to", end)
        output = scrape(start, end, keyword)
