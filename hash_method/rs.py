import tagUtil
import movieUtil

# return user-candidate-tags
def getCandidateTags(user,top=20):
  (finaltags,usertags,sorttag) = ({},{},[])
  for t in tagUtil.userTopTags(user,top=50): usertags[t[1]] = t[0]
  for t in usertags: finaltags[t] = usertags[t]
  for t in usertags: finaltags = tagAffinityRecursion(t,usertags,finaltags)

  for tag in finaltags: sorttag.append([finaltags[tag],tag])
  sorttag.sort()
  sorttag.reverse()
  return sorttag[0:top]

def tagAffinityRecursion(tag,usertags,finaltags):
  for t in tagUtil.tagTopSimilarTags(tag,top=10):
    (simscore,simtag) = t[:]
    if simtag in finaltags: finaltags[simtag] += usertags[tag]*simscore
    else: finaltags[simtag] = usertags[tag]*simscore
  return finaltags


# recommend items attach to the tags for the user
def getCandidateMovies(user):
  (movierank,usertags,tags) = ({},{},getCandidateTags(user))
  for t in tags: usertags[t[1]] = t[0]
  for t in tags: movierank = movieAffinityRecursion(t[1],movierank,usertags)
  return movierank

def movieAffinityRecursion(tag,movierank,usertags):
  ms = tagUtil.tagTopMovies(tag)
  for m in ms:
    (moviescore,movieid) = m[:]
    if movieid in movierank: movierank[movieid] += moviescore*usertags[tag]
    else: movierank[movieid] = moviescore*usertags[tag]
  return movierank


# final recommendations for user
def getRecommendMovies(user,top=30):
  movies = getCandidateMovies(user)
  rankmovies = []
  for m in movies: rankmovies.append([movies[m],movieUtil.getMovieById(m)])
  rankmovies.sort()
  rankmovies.reverse()
  return rankmovies[0:top]