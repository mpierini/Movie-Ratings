from setup import create_movie, create_user, create_rating
from correlation import pearson_similarity
from sys import exit

MOVIE_DIC = None
USER_DIC = None
DATA_DIC = None
YOU_DIC = None
		
def movie_details(movie_id):
	"""Returns a string containing the movie details for the movie with the
    given id."""
	movie_name = MOVIE_DIC[movie_id]['title']
	movie_genre = MOVIE_DIC[movie_id]['genre']
	return "Movie %s: %s\n%s" % (movie_id, movie_name, movie_genre)

def get_user(user_id):
	"""Returns string containing user details with given id. """
	gender = USER_DIC[user_id]['gender']
	if gender == 'M':
		gender = 'Male'
	elif gender == 'F':
		gender = 'Female'
	age = USER_DIC[user_id]['age']
	occupation = USER_DIC[user_id]['occupation']
	return "%s %s, age %s" %(gender, occupation, age)


def user_rating(movie_id, user_id):
	"""Returns string containing a user's rating for a specific movie 
	using the user's id & movie id if they exist in the DATA_DIC, 
	KEYERROR will appear if not. """
	rating = DATA_DIC[movie_id][user_id]
	return "User %s rated movie %s at %s stars" % (user_id, movie_id, rating)

def average_movie_rating(movie_id):
	"""Returns the average movie rating of a movie with a given movie id. """
	i = 0
	sum_ratings = 0
	for user, rating in DATA_DIC[movie_id].items():
		sum_ratings += int(rating)
		i+=1
	average = sum_ratings/i
	return average

def rate(movie_id, rating):
	"""Returns a new rating from a user with given movie id and star rating. 
	Dictionary for user input is created in this function. """
	global YOU_DIC
	YOU_DIC = {}
	YOU_DIC[movie_id] = rating
	movie_title = MOVIE_DIC[movie_id]['title']
	return "You have rated movie %s: %s at %s stars" %(movie_id, movie_title, rating)

def predict(movie_id):
	"""Returns a prediction of movie rating based on other movies 
	user has rated using given movie id. If YOU_DIC is not populated 
	with movie ratings, an error is returned. """
	movie_ratings = make_movie_ratings()
	movie_title = MOVIE_DIC[movie_id]['title']
	a = 0
	for each in YOU_DIC:
		similarity = pearson_similarity(movie_ratings, movie_title, MOVIE_DIC[each]['title'])
		if similarity > .5:
			a = YOU_DIC[each] #rating of a movie that's pretty similar to this one
			break
	if a == 0:
		return "Watch at your own risk!"
	else:
		rating = a
		return "Best guess for movie %s: %s is %s stars" %(movie_id, movie_title, rating)

def make_movie_ratings():
	"""Helper function for predict. Generates dictionary of titles, users, and ratings. """
	movie_ratings = {} # {movie_title1 {user_id1 : rating1, user_id2 : rating2}, movie_title2 ...}
	for key in DATA_DIC: #movie_ID
		newkey = MOVIE_DIC[key]['title'] #movie_title
		movie_ratings[newkey] = DATA_DIC[key] #creating record in movie_ratings with title and inner_dic with users and ratings from DATA_DIC
	return movie_ratings

def main():
	print "Welcome to the MOVIE MIXER MACHINE!!!"
	global MOVIE_DIC 
	MOVIE_DIC = create_movie()
	global USER_DIC
	USER_DIC = create_user()
	global DATA_DIC
	DATA_DIC = create_rating()
	mixology = True
	while mixology == True:
		print """
Choose from the following functions:
movie details
get user
user rating
average movie rating
rate
predict
or type "quit" to exit the MMM
"""
		function = raw_input("> ")
		if function == "quit":
			sure = raw_input("Your ratings will not be saved when you leave. Are you SURE you want to exit? (y/n) ")
			if sure == "y":
				print "MOVIE MIXER MACHINE will miss you!"
				exit()

		elif function == "movie details":
			parameter = raw_input("Enter a movie ID: ")
			try:
				print movie_details(parameter)
			except Exception, e:
				print "That's not right. Maybe you aren't cut out for watching movies."
			
		elif function == "get user":
			parameter = raw_input("Enter a user ID: ")
			try:
				print get_user(parameter)
			except Exception, e:
				print "Try again. That is not a valid user ID."

		elif function == "user rating":
			param1 = raw_input("Enter a movie ID: ")
			param2 = raw_input("Enter a user ID: ")
			try:
				print user_rating(param1, param2)
			except Exception, e:
				print "Either your user ID or movie ID was not valid. Try again."

		elif function == "average movie rating":
			parameter = raw_input("Enter a movie ID: ")
			try:
				print average_movie_rating(parameter)
			except Exception, e:
				print "Interesting... why don't you try that again?"

		elif function == "rate":
			param1 = raw_input("Enter a movie ID: ")
			param2 = raw_input("Enter a rating in stars, 1 to 5: ")
			try:
				print rate(param1, param2)
			except Exception, e:
				print "Um, maybe you could just write your ratings on a piece of paper."

		elif function == "predict":
			parameter = raw_input("Enter a movie ID: ")
			try:
				print predict(parameter)
			except Exception, e:
				print "This isn't working out."

		else:
			print "You're not very good at computer stuff, huh? Try again."



if __name__ == '__main__':
	main()