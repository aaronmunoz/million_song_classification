# Million Song Classification

This repo was initially for a Metis Data Science Bootcamp project where I attempted to classify Hip Hop vs Pop songs based on "[Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/)' analytic data as well as music lyrics which the results can be summarized under [Aaron Munoz Project McNulty.pdf](Aaron%20Munoz%20Project%20McNulty.pdf).

**Minor Warning: Profanity can be found within some of the files in this repo due to the nature of working with song lyrics**

Unfortunately this isn't the cleanest repository. As I attempted to work with new concepts and environments at the speed they were introduced, I didn't have the time to plan out the cleanest way to develop this project. If you have any questions on my ability to develop a clean repository, please feel free to reach out to me about production repositories I've worked on in the past.

The [database_work](/database_work) folder includes files for taking the Million Song Dataset in its many different file formats and placing it into database tables. The folder also contains notebooks for some DB alterations (such as aggregated tables and adding relations).

My main interest in this project was experimenting with several different algorithms across a variety of different features. The [lyrics_word_count](/lyrics_word_count) folder contains a series of files where algorithms such as Logistic Regression, Gaussian Naive Bayes, and Random Forrest Classifiers were used against "analytic" music data from the Million Song Dataset as well as repeated runs with an increasing number of words from the lyric data based on word count. The results of these algorithms with metric scores such as Recall, Precision, F1, and AUC can be found in the notebook found in the [cross_validation_files](/cross_validation_files) folder.

This project came before we covered NLP and concepts such as vectorizing text input using TFIDF vectors. When I had a bit of spare time between projects, I attempted to run other trials using those vectors in the [lyrics_tfidf](/lyrics_tfidf) folder.
