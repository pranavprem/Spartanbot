# Spartanbot

Welcome to the Spartanbot wiki!

The primary objective of this project was to cover as large a solution space as possible.

The secondary objective of this project was to attempt as many different solutions as possible in order to achieve the desired solution. To start off, we experimented with 4 available natural language/question - answer type solutions - Watson NLC, chatterbot, API AI and the Google Assistant API that was released about 3 weeks ago. They all have their strengths and weaknesses fundamentally revolving around the learning process. Some are continuously learning and require colossal training sets while others are ready from the get-go but don't get smarter with time.

Our solution to the problem involves trying to combine a solution that can effectively learn large amounts of data in an instant to start replying efficiently from the get-go and further learn to reply better with time.

To achieve this, we first created a sentence engine that takes in a sentence as input and uses NLTK to fragment it down to root words. These root words are then filtered to subjects and objects to determine what is important in the sentence. The subjects are words which are proper nouns or words without synonyms (like "CMPE 273") while objects are attributes of the subjects with synonyms (like "office", "location", "instructor"). The synonyms of the objects are also added to this list and then returned as a dictionary along with the sentence.

Next, we created a learning solution that reads the green sheet sentence by sentence (including the tables) and feeds it to the sentence engine. The outputs of the sentence engine are stored in a MongoDB database. This guarantees one shot learning and a bot that is ready to reply in minutes.

When a question is asked to the bot, it sends the question to the sentence engine and the resultant dictionary is compared to the one in the atabase to find sentences that match with the subjects and objects.

Here we implemented a scoring solution to analyze and find the required response:

![Algorithm](http://pranavprem.com/spartabot/threshold.JPG)

if Size(A)>Size(C)
    confidence = size(B)/Size(C)
else
    confidence = size(B)/Size(A)


This threshold enables the bot to not only reply to the question it has been asked but additionally give related information that is related to the question.

In addition to this, to expand the solution space, we have implemented a google custom search on "sjsu.edu" domain that is accessed through the google cloud API to provide google search results for the questions.
![venn-diagram](http://pranavprem.com/spartabot/273-venn.PNG)

![Architecture](http://pranavprem.com/spartabot/spartabot.jpeg)

The project is hosted on Heroku. All configurations are put as config variables in Heroku. A GitHub webhook is set up to deploy to Heroku on pushes or merges to master branch. The bot learns when the procfile is pushed with a worker for "learn.py" and the bot replies when procfile has a worker for "spartanbot.py".

MongoDB is used here for its schemaless structure and speed of querying. The handler for MongoDB will access and return the required objects that are dealt with by the subsequent modules. The MongoDB database is hosted on mlab for the project for ease of connection with Heroku.

To track the entire project, we have used waffle.io which is integrated with slack on the channel we use. So any improvements and new features are published through waffle.io to the slack channel as well. informing everyone on the channel about the new things that can be asked to the bot.

One additional feature we have implemented over all of this is Twilio. Sending an SMS to the number configured to Twilio will send a webhook into the Twilio handle set up in heroku as a flask application. This will accept the sms message and post it to the slack channel as the bot while tagging the bot in order to trigger a response.
