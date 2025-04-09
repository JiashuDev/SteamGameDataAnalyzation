import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from utils.query import querys
#user_rating = {
#    "admin" : {"CyberPunk" : 1},
#    "userA" : {"CyberPunk" : 1, "Elden Ring" : 2}
#}

def getUser_ratings():
    user_ratings = {}
    userList = list(querys('select * from user', [], "select"))
    historyList = list(querys('select * from history', [], "select"))
    for user in userList:
        userId = user[0]
        userName = user[1]
        for history in historyList:
            gameId = history[1]
            try:
                existHistory = \
                querys('select id from history where game_id = %s and user_id = %s', [gameId, userId], 'select')[0][0]
                gameName = querys('select title from games where id = %s', [gameId], 'select')[0][0]
                historyContent = history[3]
                if user_ratings.get(userName, -1) == -1:
                    user_ratings[userName] = {gameName:historyContent}
                else:
                    user_ratings[userName][gameName] = historyContent

            except:
                continue
    return user_ratings

def user_base_collaborative_filtering(user_name, user_ratings, top_n=3):
    # get Target user data
    target_user_ratings = user_ratings[user_name]

    # Save similar score
    user_similarity_scores = {}

    # Type cast target user into numpy array
    target_user_ratings_list = np.array([
        rating for _, rating in target_user_ratings.items()
    ])

    # Calculate similar score
    for user, rating in user_ratings.items():
        if user == user_name:
            continue

        # Type cast other users into numpy array
        user_ratings_list = np.array([rating.get(item, 0) for item in target_user_ratings])

        # Calculate cosine similarity
        similarity_score = cosine_similarity([user_ratings_list], [target_user_ratings_list])[0][0]
        user_similarity_scores[user] = similarity_score

    sorted_similar_user = sorted(user_similarity_scores.items(), key=lambda x: x[1], reverse=True)

    # Select top_n user as recommendation result
    recommended_items = set()

    for similar_user, _ in sorted_similar_user:
        recommended_items.update(user_ratings[similar_user].keys())


    # Filter repeated Data
    recommended_items = [item for item in recommended_items if item not in target_user_ratings]
    return recommended_items

