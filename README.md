# SocialVolume

The goal of CryptoVolume is to effectively predict the pricing of cryptocurrencies using a machine learning model. Sentiment analysis has existed for years in the form of [market sentiment](https://en.wikipedia.org/wiki/Market_sentiment#Theory_of_investor_attention), where traders' perception of the market & individual stocks is measured in terms of bullish or bearish, indicating if the market is moving upwards or downwards, respectively. Recently, many researchers have analyzed the impact of social media sentiment on the market.  While market sentiment measures traders' perspective of the market,  social media sentiment statistically measures the sentiment of users on Twitter, (and/or other sites such as Facebook, Instagram, Reddit, etc.) many of which may not even be trading in the actual market. Ideally, social media sentiment abstracts out generic news and captures the general public's view on a specific company or stock. Some examples of incidents that would lead to a strong social media sentiment would be the [United Airlines incident (2017)](https://en.wikipedia.org/wiki/United_Express_Flight_3411_incident#Cultural_impact) or [Blizzard's Hong Kong player (2019)](https://www.cbsnews.com/news/blizzard-china-statement-blizzard-president-apologizes-for-hong-kong-player-ban-we-moved-too-quickly/), where both situations were EXTREMELY controversial.

Since cryptocurrencies are a newer part of the market, many uncertainties still exist. The price trends do not seem to have a strong basis and the idea of cryptocurrencies are very controversial as well, making social media sentiment analysis an obvious choice to predict the behavior of cryptocurrencies.

## Objective
So now that we know all of these forms of sentiment-related predictions exist, what will CryptoVolume do differently? The impact of social media sentiment has been analyzed **too** frequently. While it is clearly a powerful tool, I wanted to use a lesser known metric. Instead of analyzing the social media sentiment, CryptoVolume scrapes the volume of tweets per day mentioning a specific cryptocurrency. The assumption is that a stronger volume of tweets will correspond to a greater volume in which the stock is being traded, whether it is being bought or sold. In the proof of concept, I chose to scrape and analyze Bitcoin, the most widely known cryptocurrency. After obtaining this data, the goal is to combine it with pricing factors of the respective cryptocurrency and create predictions of the price, given this data with a nueral network.

While asset-backed stocks are easier to predict given market data, these predictions cannot be made with machine learning due to a key reason. These stocks are extremely volatile towards reports and news that depend on the companies performance, which generally cannot be predicted by past data. As a result, most machine learning models will choose the previous day's pricing as the most likely value. However, cryptocurrencies differ in that they are NOT asset-backed. There is no performance reports and news is generally far more infrequent, but also potentially more severe. As a result, these predictions will be limited to short term, but also have the potential to be more accurately predicted given past data.

## Disclaimer
There are risks associated with trading, especially in the volatile crypto market. I do not recommend that any cryptocurrency should be bought, sold, or held by you. Do conduct your own due diligence and risk what you can afford to lose. All contents in this repository and beyond are solely for educational purposes.

## Scraping & Data
The greatest limitation in this project is access to the data. Twitter does not provide an exhaustive search feature or counts endpoint in their non-enterprise API. As a result, I chose to use Twint which acts as a bot, retrieving data from each webpage. The script that was created ran on AWS using cron job's task management to schedule and kill the script by the hour, preventing parallelization which would kill the instance. After roughly 140 hours, the data was scraped for the first 306 days of 2019 and recorded into a text file. The scraped data is depicted below.

<p align="center">
 <sup>Close Price vs. Tweet Count</sup>
 </p>

![Close Price vs. Tweet Count](https://i.imgur.com/O0AxsHe.png)

## Predictions
After creating the model & scraping the data, the validity of the assumption that tweet count would be a strong indicator needed to be tested. Initially, I tested various parameters to determine what predicted Bitcoin pricing best, given pricing and dollar volume. After settling on these parameters, the model was given two additional columns -- a simple moving average and the tweet count. The results are depicted below.

There are 2 sets of graphs. The first pair of graphs are predictions given Open/Close/Low/High/Volume. The orange line indicates the actual pricing, while blue indicates predictions. The first 240 days are the training set, and indicated by the graph prior to the vertical blue line. Rightward of the line are the predictions, where the actual pricing for these days is NOT used in these predictions. Instead, it is merely graphed to show the accuracy of the model. The predictions are blown up to better show the accuracy and the vertical lines in this graph are used to show the start date of large price movements and allow a better visualization of when these large movements line up with the predictions on these given days. The second pair of graphs are predictions given Open/Close/Low/High/Volume/Tweet Count/7-Day SMA. The training set and parameters of the model are identical.

<p align="center">
 <sup>Volume Predictions & Training</sup>
 </p>

![Volume Predictions & Training](https://i.imgur.com/ut9M4Nm.png)

<p align="center">
 <sup>Volume Predictions (Enlarged)</sup>
 </p>

![Volume Predictions (Enlarged)](https://i.imgur.com/m1GU7t3.png)

<p align="center">
 <sup>Tweet Predictions & Training</sup>
 </p>

![Tweet Predictions & Training](https://i.imgur.com/v7M509t.png)

<p align="center">
 <sup>Tweet Predictions (Enlarged)</sup>
 </p>

![Tweet Predictions (Enlarged)](https://i.imgur.com/W9oETUl.png)

Evidently, the tweet count and moving average of this data *strongly* improves accuracy of the predictions. While small day to day movements are not accurately predicted, the tweet-based model perfectly predicts the large movements, while the model with exclusively volume/pricing data struggles to accurately make these predictions. This reinforces the idea that cryptocurrencies can be predicted by machine learning due to the fact that they are a non-asset-backed equity. Furthermore, this implies that the model is best at predicting large movements in the short term, but that the oscillation of price day to day is not easily predicted.

In an attempt to analyze the error, I attempted to measure the risk of these predictions. While a statistical error analysis would be useful, it would contain bias. As I mentioned, "large" jumps are best predicted, but what indicates "large"? By choosing a value, this is inserting bias into the model, as this value would clearly be tuned to best fit the model and as a result, potentially make the model look better than it is.

Instead, I chose to create a model on the basis that there are 4 possible situations, only one of which, is a risky and bad situation. If the model predicts an increase and the actual pricing increases or the model predicts a decrease and the actual pricing decreases, this is a positive. When the model predicts a decrease and the actual pricing increases, it is not an ideal situation, but there is no risk, as the predictions do not cause you to lose money. *However*, if the model predicts an increase and the actual pricing decreases, the model is extremely risky. As a result, I weighted the values as such, and created a graph where negative values indicate risk. Furthermore, the discrepancy from zero indicates the discrepancy between the predicted and actual.

<p align="center">
 <sup>Error Analysis</sup>
 </p>

![Error Analysis](https://i.imgur.com/mlOUdSy.png)

Thus, after seeing the graph, the conclusion that the model is risk adverse can be made. This further strengthens the proof of concept that tweet count can be used to predict the pricing of cryptocurrencies. The negative dips are minimal, and most likely due to inaccurate predictions of the oscillating price.

## Improvements
Although the results are promising, there are various areas for improvement that will be added to this repository and are listed below.
* Additional scraped data for a given cryptocurrency, especially late 2018 for Bitcoin, where it spiked to roughly $18,000. Given the current state of scraping, this would be extremely time costly as there are upwards of 100,000 tweets per day mentioning the cryptocurrency. As a result, access to Twitter's enterprise API or a better method for scraping would be a strong improvement as well.
* Analysis of additional cryptocurrencies, especially those that are lesser known, but not 'penny stocks'. (Ethereum, Litecoin, etc.) With these cryptocurrencies, the idea is that their Twitter volume may be entirely based on traders. As a result, the predictions may be more accurate and impactful news may be even more infrequent.
* Indications of pump and dumps. The assumption is that stocks, in general, are based on a few main factors: previous pricing, general sentiment, news reports, and larger companies pumping and dumping, which essentially forces the market to behave in a certain way. Contrarily, cryptocurrencies lack the significant impact of news reports on the price. The model has access to previous pricing and general sentiment and thus, an indicator that a market movement is artificial could significantly improve the performance of the model. However, this is most likely far more difficult to predict.
* Representing the error better, preventing bias from favoring the model. I would love to research a more statistically sound analysis for interpretting the error.

These are simply ideas that I'd love to test, but the possibility of testing some may be far too difficult. However, this is still a work in progress that I hope to improve. If you have any suggestions or would like to discuss this research, please contact me at manuelinfosec@gmail.com.

You can also find me on [LinkedIn](https://www.linkedin.com/in/manuelinfosec/) 

Thank you for reading!!
