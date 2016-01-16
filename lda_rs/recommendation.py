import user_topics
import user_tags
import user_items
import db
import json

db_info = db.info()

def user_sim_matrix():
  topic_matrix = user_topics.get_topic_sim_matrix()
  tag_matrix = user_tags.get_tag_sim_matrix()
  sim_matrix = {}
  for m in topic_matrix:
    if m in tag_matrix:
      sim_matrix[m] = topic_matrix[m]*(tag_matrix[m]+0.001)
  json.dump(sim_matrix,open("matrix/100_sim_matrix.txt",'w'))
  return sim_matrix

def get_sim_matrix(path='matrix/sim_matrix.txt'):
  matrix = json.load(file(path))
  return matrix

def get_user_neighbors(userid,top):
  user_rank = []
  # global_sim_matrix = get_sim_matrix()
  global_sim_matrix = user_topics.get_topic_sim_matrix(path="matrix/50_topics_sim_matrix.txt")
  # global_sim_matrix = user_tags.get_tag_sim_matrix()
  # global_sim_matrix = user_items.get_user_items_sim_matrix()
  for other in db_info.user_list:
    if other == userid: continue
    key1 = str((userid,other))
    key2 = str((other,userid))
    if key1 in global_sim_matrix:
      user_rank.append([global_sim_matrix[key1],other])
    elif key2 in global_sim_matrix:
      user_rank.append([global_sim_matrix[key2],other])
    else: print "can not find similarity between"+ key1
  user_rank.sort(reverse=True)
  neighbor_list = [u[1] for u in user_rank[0:top]]
  top_neighbor_tuple = tuple(neighbor_list)
  return top_neighbor_tuple


def recommend_for_user(userid,top_neighbor=30,top_movie=50):
  neighbors = get_user_neighbors(userid,top=top_neighbor)
  neighbor_movies = db.get_movie_from_users(neighbors)
  movies_count = list_count(neighbor_movies)
  movies_count = filter_item_for_user(movies_count,userid)
  candidate_list = user_tags.hash2list(movies_count)
  recommend_list = [candidate_list[i][1] for i in range(0,top_movie)]
  return recommend_list


def filter_item_for_user(origin_items,userid):
  dic_copy = dict(origin_items)
  for m in origin_items:
      if m in db_info.user_train_movies(userid):
        del dic_copy[m]
  return dic_copy

def list_count(tuple_list):
  dic = {}
  for t in tuple_list:
    (userid,movieid) = t[:]
    if movieid not in dic: dic.setdefault(movieid,1)
    else: dic[movieid] += 1
  return dic

def main():
  user_topics.main()
  # user_tags.main()
  user_sim_matrix()
  # get_sim_matrix()
  # print recommend_for_user(8,50)
  # topic_matrix = user_topics.get_topic_sim_matrix()
  # print topic_matrix[str((173, 358))]
  # print len(topic_matrix)
