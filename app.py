from flask import Flask,render_template,request
import pickle
import numpy as np

pop = pickle.load(open('popular_r.pkl','rb'))
popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
p = pickle.load(open('Top_Books','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(pop['Book-Title'].values),
                           author=list(pop['Book-Author'].values),
                           image=list(pop['Image-URL-M'].values),
                           votes=list(pop['num_ratings'].values),
                           rating=list(pop['avg_rating'].values)
                           )
@app.route('/c')
def contact():
    return render_template('c.html',
                           book_name=list(p['Book-Title'].values),
                           author=list(p['Book-Author'].values),
                           image=list(p['Image-URL-M'].values)
                           )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)