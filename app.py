from flask import Flask,render_template,request,jsonify
import recommend


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recommend', methods =['POST'])
def Movie_name():
    movie_title = request.form.get('movie_name')
    if movie_title.strip() == '':
        return render_template('Error.html',valid ='null')
    
    movie_id = recommend.search_movieId(movie_title)
    rec_list = list(recommend.recommendation(movie_id))[1:] # leaving first movie name as it was entered by user

    if len(rec_list)==0:
        return render_template('Error.html', empty =0)
    else:
        for i,m in enumerate(rec_list):
            m = m.strip() # removing trailing spaces
            if len(m)-m.rfind('The')==3:
                m = m.rstrip('The') # removing last 'The'
                m = 'The '+ m # concatenating 'The' at beginning
                rec_list[i] = m

        return render_template('home.html' , movie_list = rec_list)

if __name__ =='__main__':
    app.run(host='0.0.0.0',port=8080)
