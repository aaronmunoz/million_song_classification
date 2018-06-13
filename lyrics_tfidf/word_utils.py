import matplotlib.pyplot as plt

def get_word_counts(lyric_df):
    word_song_appearances = lyric_df.groupby(['word'])['count'].agg('count').reset_index()
    word_song_appearances.sort_values('count', ascending=False, inplace=True)

    word_total_appearances = lyric_df.groupby(['word'])['count'].agg('sum').reset_index()
    word_total_appearances.sort_values('count', ascending=False, inplace=True)
    
    return word_song_appearances, word_total_appearances

def get_word_total_idf(lyric_df):
    word_total_appearances = lyric_df.groupby(['word'])['tf_idf'].agg('sum').reset_index()
    word_total_appearances.sort_values('tf_idf', ascending=False, inplace=True)
    return word_total_appearances

def generate_word_charts(genre_lyrics, genre_label):
    number_of_songs = genre_lyrics.index.nunique()
    
    word_song_appearances, word_total_appearances = get_word_counts(genre_lyrics)
    
    plot_data = word_total_appearances[0:15].sort_values('count')

    ax1 = plot_data.plot(x='word', y='count', kind='barh', figsize=(15,5), legend=None)

    plt.title('Total Word Appearances (From {} \'{}\' Songs)'.format(number_of_songs, genre_label))
    plt.ylabel('Word')
    plt.xlabel('Count')

    plot_data = word_song_appearances[0:15].sort_values('count')

    ax2 = plot_data.plot(x='word', y='count', kind='barh', figsize=(15,5), legend=None)

    plt.title('Number of Song Appearances for Word (From {} \'{}\' Songs)'.format(number_of_songs, genre_label))
    plt.ylabel('Word')
    plt.xlabel('Count')
    
    return ax1, ax2