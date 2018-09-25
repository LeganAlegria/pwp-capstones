#User class below
class User(object):
    def __init__(self, name, email):
        self.name = name   # a string
        self.email = email # a string
        self.books = {}    # empty dictionary

    def __repre__(self):
        return self.name

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address # change email to address
        print("User {name}'s email has been updated.".format(name = self.name))

    def __repr__(self):
        temp_list = list(self.books) # make a list of books in dictionary self.books
        number_of_books = str(len(temp_list)) #count the number of books in the self.books dictionary
        return "User {name}, email: {email}, books read: {books}. ".format( name = self.name, email = self.email, books = number_of_books)

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True # both self and other user are the same
        else:
            return False # self and other user are not the same

    def read_book(self, book, rating = None):
        self.books[book] = rating
        
    def get_average_rating( self ):
        sum =0
        temp_list = list(self.books.values())
        number_of_books = len(temp_list)
        for value in self.books.values():
            sum += value
        return sum/number_of_books
    
        
# Book Class below
class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __repr__(self):
        return self.title

    def get_title(self):
        return self.title


    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print ("Book {title}'s ISBN was updated to {isbn}".format(title = self.title, isbn = self.isbn))

    def add_rating(self, rating):
        #check if rating is valid before adding to the rating list
        #acceptable values are between 0 and 4
        if rating >=0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        sum =0
        number_of_ratings = len(self.ratings)
        for i in range(len(self.ratings)):
            sum += self.ratings[i]
        if sum > 0:
            return sum/number_of_ratings
        else:
            return 0 # avoid division by zero when no ratings have been input
    

    def __hash__(self):
        return hash((self.title, self.isbn))
    
# Fiction Class below

class Fiction(Book):
    def __init__(self, title, isbn, author):
        super(Fiction,self).__init__(title, isbn)
        self.author = author  # a string

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

    
# Non_Fiction Class below
        
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super(Non_Fiction, self).__init__(title, isbn)
        self.subject = subject   # a string
        self.level = level       # a string

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__( self ):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)


# TomeRater Class below


class TomeRater:
    def __init__(self):
        self.users = {} # a dictionary of email as key and user as value
        self.books = {} # a dictionary of book as key and # of times read as value
        self.list_of_isbns = [] # a list of isbns for every book created to avoid duplicates

    def create_book(self, title, isbn):
        duplicate_isbn = False
        for test_isbn in self.list_of_isbns:
            if test_isbn == isbn:
                duplicate_isbn = True
        if duplicate_isbn:
            print( "Duplicate ISBN in this book!" )
        else:
            self.list_of_isbns.append(isbn)
            return Book(title, isbn)
        
    def create_novel(self, title, author, isbn):
        duplicate_isbn = False
        for test_isbn in self.list_of_isbns:
            if test_isbn == isbn: 
                duplicate_isbn = True
        if duplicate_isbn:
            print("Duplicate ISBN in this novel!")
        else:
            self.list_of_isbns.append(isbn)
            return Fiction(title, isbn, author)
        
    def create_non_fiction(self, title, subject, level, isbn):
        duplicate_isbn = False
        for test_isbn in self.list_of_isbns:
            if test_isbn == isbn:
                duplicate_isbn = True
        if duplicate_isbn:
            print( "Duplicate ISBN in this non-fiction!" )
        else:
            self.list_of_isbns.append(isbn)
            return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user( self, book, email, rating = None):
        if self.users.get(email):
                self.users[email].read_book(book, rating)
                book.add_rating(rating)

                if self.books.get(book):
                    self.books[book] += 1
                else:
                    self.books[book] = 1
        else:
            print("No user with email {email}!".format(email = email))


    def add_user(self, name, email, user_books = []): #user_books is a list of Book objects
        #this block checks if email is OK
        if email[-4:] == ".edu" or email[-4:] == ".com" or email[-4:] == ".org":
            valid_email = True
        else:
            valid_email = False
            print("Invalid email extension( no .edu or .com or .org found)")
        if email.find('@') >= 0:
            missing_symbol = False
        else:
            missing_symbol = True
            print("Missing @ in email!")
        #this block checks if email is duplicated in previous entry of user   
        duplicate_email = False
        for test_email in self.users.keys():
            if test_email == email:
                duplicate_email = True
                print("User already exists!")
                break
        if not duplicate_email and valid_email and not missing_symbol: # if email is not duplicate and it is valid, create user
            temporary_user = User(name,email)
            self.users[email] = temporary_user
            if len(user_books) > 0:
                for book in user_books:
                    self.add_book_to_user(book, email, book.get_average_rating())


    def print_catalog(self):
        print("Printing Catalog:") #print title of book and number of times read
        for key in self.books.keys():
            print( key.get_title() + "," + str(self.books[key]))
        print("\n")

    def print_users(self):
        print("Printing Users:") #print email and name
        for key in self.users.keys():
            print( key + ", " + self.users[key].name)
        print("\n")

    def get_most_read_book(self):
        most__read_book = ""
        max_read_temp = 0
        for book in self.books.keys():
            if self.books[book] > max_read_temp:
                most_read_book = book.title
                max_read_temp = self.books[book]
            else:
                continue
        print(most_read_book + "," + str(max_read_temp) + " times") 
    
    def highest_rated_book(self):
        highest_score_temp = 0
        highest_scored_book = ""
        for book in self.books.keys():
            if book.get_average_rating() > highest_score_temp:
                highest_score_temp = book.get_average_rating()
                highest_scored_book = book.title
       
        print(highest_scored_book)

    def most_positive_user(self):
        highest_average_rating = 0
        highest_positive_user = " "
        for user in self.users.values():
            if user.get_average_rating() > highest_average_rating:
                highest_average_rating = user.get_average_rating()
                highest_positive_user = user.name

        print(highest_positive_user)

        
    
            
    
            
        
                  
