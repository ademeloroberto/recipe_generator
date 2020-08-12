# app.py

# Load needed libraries 
import pickle
import pandas as pd 
import numpy as np
from flask import Flask, request, jsonify, render_template
from gensim.models import Word2Vec
from sklearn.cluster import KMeans

app = Flask(__name__) #Initialize the flask App

# load the pickle files
word2vec = pickle.load( open( "data/word2vec_trained.p", "rb" ) )
kmeans = pickle.load( open( "data/kmeans_fitted.p", "rb" ) )
model_prep_modes = pickle.load( open( "data/ingredients_prep_modes_50000_2.pkl", "rb" ) )

#This tells what to do when the app is started. -> Redirect to our start html (index.html)
@app.route('/')
def home():
    return render_template('index.html')


#This is where it reads out the given input and predicts
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    #get the input ingredients into a list
    #my_list = list([str(x) for x in request.form.values()])
    my_ingredients = str([str(x) for x in request.form.values()])
    my_list = my_ingredients.split()
    
    #Now we have to run find the proper ingredience, that go well together
    def choose_clustering(input_ingredients):
        '''Takes a list of ingredients as input, returns a subset of this list with ingredients
        that should go well together.
        Based on a trained Word2Vec model and Kmeans clusterer.'''

        embeddings = []              # For word embeddings
        chosen_ingredients = []      # For ingredients present in the Word2Vec
        group_1 = []                 # Savory ingredients
        group_2 = []                 # Sweet ingredients
        
        for w in input_ingredients:
            try: # Check if input ingredient is in the Word2Vec vocabulary
                embeddings.append(word2vec.wv[w])
                chosen_ingredients.append(w)
            except:# Print error message if not 
                print('''Oops! Seems like {0} is not in our database.
                It will not be featured in the recipe. Sorry about that!'''.format(w))
                pass
        
        input_df = pd.DataFrame(embeddings)  # Prepare data for Kmeans.predict
        clusters = kmeans.predict(input_df)  # predict clusters
        
        # Separates savory ingredients into group_1 and sweet ingredients into group_2
        for i,c in enumerate(clusters):
            if c == 0:
                group_1.append(chosen_ingredients[i])
            elif c == 1:
                group_1.append(chosen_ingredients[i])
            else:
                group_2.append(chosen_ingredients[i])
        
        # The group with more ingredients is returned
        if len(group_1) > len(group_2):
            return group_1
        else:
            return(group_2)
        
    #Now it's time to add the preparation mode for each ingredient
    def get_prep_modes(ingredients_chosen):
        '''Takes chosen ingredients and returns preparation modes for them.'''
        print('To follow your delicious recipe please: \n')

        output = []
        for ingredient in ingredients_chosen:
            try:
                instructions = list(model_prep_modes.get(ingredient).keys())[0:3]
                #print('{0} and/or {1} the {2}'.format(instructions[0], instructions[1], ingredient))
                output_prep_modes = ('{0} and/or {1} the {2}'.format(instructions[0], instructions[1], ingredient))
                output.append(output_prep_modes)
                
            except:
                #print('Seems like {0} is not in our database! It will not be featured in our recipe. Sorry about that!'.format(ingredient))
                output_prep_modes_not = ('Seems like {0} is not in our database! It will not be featured in our recipe. Sorry about that!'.format(ingredient))
                output.append(output_prep_modes_not)
                pass

        return output



    # call defined functions for ingredients and preparation mode and get output
    #my_list2 = ['butter', 'chicken', 'potato', 'spinach', 'feta']
    result1 = choose_clustering(my_list)
    output = get_prep_modes(result1)



    # Finally define what output is being displayed on the website 
    #return render_template('index.html', prediction_text='These are the ingredients, that go well together: {}'.format(result1), 
    #    prediction_text2='And this is your ultimate recipe, enjoy! {}'.format(output))
    return render_template('index.html',prediction_text='These are the ingredients, that go well together:', ingredients= result1, 
        prediction_text2="And this is your ultimate recipe, enjoy!", prep_modes=output )
    
if __name__ == "__main__":
    app.run(debug=True)
