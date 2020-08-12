### About the project
This recipe generator was developed in the context of the Business Innovation Lab course from the M.Sc. in Business Intelligence & Process Management. In order to reach the results hereafter presented, 7 students dedicated themselves for the period of 6 weeks. The aim was to develop an application that would take ingredients as input, select from the given list those ingredients that work well together, and finally display suitable preparation modes for each of the selected ingredients. 
This project was highly inspired by the food2vec repository: https://github.com/altosaar/food2vec 

### Prerequisites
You must have pandas, numpy, gensim.models and sklearn.cluster and Flask (for API) installed.

Flask version: 0.12.2
conda install flask=0.12.2  (or) pip install Flask==0.12.2

### Project Structure
This project has three major parts:
1. app.py - This is the main file where the recipe generation happens. It loads the pickle-files as well as the input ingredients and return the generated recipe. It holds the two main defined functions where firstly, the input ingredients get scanned and those, that go well together get returned, and secondly, for each input ingredient defines a preparation mode. 
2. template - This folder contains the HTML template (index.html) to allow user to enter ingredients and displays the outcome recipe
3. static - This folder contains the css folder with style.css file which has the styling required for our index.html file  as well as the image displayed on the webpage. 

### Running the project

1. Run app.py using below command to start Flask API. Ensure that you in the project home directory. 
```
python app.py
```
By default, flask will run on port 5000.

2. Navigate to URL http://127.0.0.1:5000/ (or) http://localhost:5000

You should be able to view the homepage.

Enter some ingredients only separated by spaces and hit the "Generate Recipe"-Button 

If everything goes well, you should  be able to see the generated recipe as single steps on the HTML page!
check the output here: http://127.0.0.1:5000/predict

