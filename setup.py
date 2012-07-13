
def read_movie(filename):
	movie_dic = {}
	# Reading in data from item/movie table to a dictionary with movie_id as key and info as values in embedded dictionary
	item = open (filename, "r")
	for line in item:
		stripped = line.strip()
		movie = stripped.split("|")
		movie_dic[movie[0]] = {"id": movie[0], "title" : movie[1], "released" : movie[2], "video" : movie[3], "imdb" : movie[4], "genre" : movie[5:]}
	item.close()
	return movie_dic

def fix_genres(movie_dic, filename):
	genre_dic = read_genre(filename)
	movie_dic = update_genre(movie_dic, genre_dic)
	return movie_dic

def read_genre(filename):
	genres = open (filename, "r")
	genre_dic = {}
	for line in genres:
		stripped = line.strip()
		genre = stripped.split("|")
		if genre == ['']:
			continue
		genre_dic[genre[1]] = genre[0]
	genres.close()
	return genre_dic

def update_genre(movie_dic, genre_dic):
	for movie in movie_dic:
		gen_list = movie_dic[movie]["genre"]
		glist = []
		i = 0
		while i < len(gen_list):
			if gen_list[i] == '1':
				glist.append(genre_dic['%d'%(i)])
			i += 1
		cool_genre = ", ".join(glist)
		movie_dic[movie]["genre"] = cool_genre
	return movie_dic

def create_movie():
	movie_dic = read_movie("ml-100k/u.item")
	fix_genres(movie_dic, "ml-100k/u.genre")
	return movie_dic

def create_user():
	user_dic = {}
	# Reading in data from user table to a dictionary with user_id as key and info as values in embedded dictionary
	filename = "ml-100k/u.user"
	item = open (filename, "r")
	for line in item:
		stripped = line.strip()
		user = stripped.split("|")
		user_dic[user[0]] = {"age" : user[1], "gender" : user[2], "occupation" : user[3], "zipcode" : user[4]}
	item.close()
	return user_dic

def create_rating():
	data_dic = {}
	# Reading in data from data (through) table which connects user ratings and movies,
	filename = "ml-100k/u.data"
	item = open (filename, "r")
	for line in item:
		stripped_line = line.strip()
		if len(stripped_line) == 0:
			continue
		data = stripped_line.split()
		user_id = data[0]
		movie_id = data[1]
		rating = data[2]
		if not data_dic.get(movie_id):
			data_dic[movie_id] = {user_id : rating}
		else:
			inner_dic = data_dic[movie_id]
			inner_dic[user_id] = rating
	item.close()
	return data_dic


if __name__ == "__main__":
	create_movie()
	create_user()
	create_rating()

