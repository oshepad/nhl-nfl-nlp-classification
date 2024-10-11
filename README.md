# Reddit Scraper
---

### Problem Statement
---
Ever wonder if someone is talking about hockey or football?  Probably not.  Or if you do, you just choose to cheer, GO TEAM GO! Yay Sports!  You don't know how to fit in or what to say.

Well computers have your back.  More specifically this natural language processiong model has your back.  It has been studying the way people talk about football and hockey.  You can ask it to evaluate what you want to say and it will tell you if it is more likely something you would hear at the rink or the stadium.

With these tools you can collect the phrases that matter, study them, and then use our multinomial naive bayes model to test your vocabulary to see who you sound like.  

Maybe you don't care about hockey and football.  That's ok, but maybe you have the same question about two different genres of anything.  Anything on Reddit that is.  Go ahead and ask it about any two topics (subreddits).  It will study these two topics and let you know how confident it is about predicting which genre the quote came from.  

To be fair it might take a while though, depending on how popular the subreddit is, so this will take time, but in a couple of weeks you will be talking the talk.  And who knows, maybe you do like football.  You could be ready in time for the big game.  Go BRUINS!  

---

### About the Data
---
In 2023, Reddit proposed and underwent a series of changes to its API that greatly affected the ways that users, developers, and academics interact with and access the troves of data that its community freely creates.

With these changes, the process of freely collecting data has slowed down.  There are limits in place with an API request rate of 60 rps (requests per second).  You can also only requests 100 posts at a time.  Lastly, there are only 1,000 of the most hot and new posts available in a subreddit.  Therefore, it is a moving target as to how many posts you can scrape.

For this project, so far we have accumulated 2422 posts, 1506 from the NFL subreddit and 916 from the NHL

---
### How to scrape posts
---
* Launch the python script. 
* It will prompt you for your credentials and reddit communities of choice.
* It will then gather the data and save the files onto your computer.
* While you study up on the lingo, so will the model.
* After you feel comfortable, give it a shot!

---

### Requirements
---
* Reddit login, password, api client id, api client secret, and user agent name.
* A computer with an internet connection that is setup to run python script.

---

### Model Reviews
---

For this problem we ran the extracted post titles through several model configurations and tune their hyperparameters.  We also decided that we should focus on F1 Scores and Accuracy.  F1 scores hone in on the accuracy the model carries for identifying the individual classes.  We want our model to be right about both classes.

Before getting to the good stuff, keep in mind the null model.  This model is essentially the baseline, if you guessed based on how may NFL posts there were vs how many NHL posts.  The NFL was represented by 62.18% and the NHL by 37.82% of the posts.  This is not a severely imbalanced dataset, but it is a favored on one side which makes it a little more challenging.  Also, to consider, the vocabulary of the two groups are both fans of sports.  Their passion, energy, and word choice can crossover pretty well.

A short summary of the findings:

* **Logisitic Regression**
    * The CVEC model was overfit roughly 75% accurate on the testing data and 87% on the training data bearing an F1 score was 65% and 72% ROC AUC score.
    * The TVEC model was also roughly 75% but not overfit.  It did have a lower F1 score at 58% and ROC AUC at 69%
* **k-Nearest Neighbors**
    * The CVEC model was even more overfit roughly 65% accurate on the testing data and 85% on the training data bearing an F1 score was 59% and 65% ROC AUC score.
    * The TVEC model did better with accuracy at roughly 77% but not overfit.  It did have a lower F1 score at 68% and ROC AUC at 75% 
* **Multinomial Naive Bayes**
    * The CVEC model was lightly overfit roughly 78% accurate on the testing data and 86% on the training data bearing an F1 score was 69% and 75% ROC AUC score.
    * The TVEC model did better with accuracy at roughly 77% but not overfit.  It did have a lower F1 score at 66% and ROC AUC at 73% 
* **Random Forests**
    * The CVEC model was not overfit roughly 70% accurate on the testing data and 72% on the training data bearing an F1 score was 41% and 62% ROC AUC score.
    * The TVEC model did better with accuracy at roughly 68% but not overfit.  It did have a lower F1 score at 35% and ROC AUC at 59%

---

### Findings
---
The Multiomial Naive Bayes model with the CVEC transformer appears to be the favorite for this problem.  It has a combination of the best F1 score and overall Accuracy.  The model has some overfitting, but could perhaps be further tuned to bring the scores in line.  It should perform over 15% better than the null model.  On that note, whats next.

---

### Next Steps
---

While the model selected did well, an improvement of over 15% from the null model, it could be improved further.  Some of these steps would be:

* Gather more data.  With time on our side, data can be regularly fetched and the model updated.
* Consider further text preprocessing.  Finer tooth combing to remove text and characters could help improve the accuracy and F1 scores.  Though this needs to be done with care to avoid overfitting.  Also, this could affect transferability to other topics.  
* Boosting could be particularly helpful.  The TVEC transformed models and both Naive Bayes were not particularly overfit.  Boosting is a series of models that operate one after the other attempting to improve on the failures of the prior model.  This way it learns the hard parts.  In this case that will help.
* While not terribly imbalanced, the data was a bit imbalanced.  The data is free so further collection could help, but it could be a condition of the popularity of one subreddit over the other.  Synthetic data approaches, undersampling the heavier class and oversampling the ligher class would help some.
* Lastly stacking is a powerful ensemble technique that (as it sounds) places a model on top of other models.
* An interface between the user and the model to test their new vocabulary needs to be developped.
* The python script does not run in git bash (getpass issue) but does in other command line terminals.  The root cause of this issue needs to be fleshed out.

---

### Conclusion
---

While the multinomial naive bayes model is doing better than the null model, there is still quite a bit to learn from the resources available, making it not ready for production.  Namely, time to collect more data and also progressing through the techniques above.  The web scraping tool could be used in a prototype environment while the terminal platform issued is resolved.






