from flask import Flask, render_template, request, url_for
import pickle
import numpy as np

app = Flask(__name__, static_folder='static')

linreg = pickle.load(open('Models/linreg_model.pkl', 'rb'))
knn_model = pickle.load(open('Models/knn_model.pkl', 'rb'))
gaussian_nb = pickle.load(open('Models/nbG_model.pkl', 'rb'))
multinomial_nb = pickle.load(open('Models/nbM_model.pkl', 'rb'))
bernoulli_nb = pickle.load(open('Models/nbB_model.pkl', 'rb'))

job_map = {
    1: 'Junior',
    2: 'Senior',
    3: 'Project Manager',
    4: 'CTO',
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/classifier')
def classifier():
    return render_template('classifier.html')


@app.route('/linear', methods=['GET', 'POST'])
def linear():
    return render_template('linear.html')


@app.route('/knn', methods=['GET', 'POST'])
def knn():
    return render_template('knn.html')


@app.route('/kmeans', methods=['GET', 'POST'])
def kmeans():
    return render_template('kmeans.html')


@app.route('/naive', methods=['GET', 'POST'])
def naive():
    return render_template('naive.html')


@app.route('/predict', methods=['POST'])
def predict():
    position_level = request.form.get('comp_select')
    experience_str = request.form.get('experience')
    try:
        experience = float(experience_str)
    except ValueError:
        return render_template('linear.html', prediction_text=f"Error: Invalid input value for experience: '{experience_str}'. Please enter a valid numerical value.")

    if position_level in ['1', '2', '3', '4']:
        int_position_level = int(position_level)
        float_experience = float(experience)
        int_features = [int_position_level, float_experience]
        final_features = [np.array(int_features)]
        prediction = linreg.predict(final_features)

        
        int_position_level = job_map.get(int(position_level))
        predicted_salary_f = round(float(prediction.item()), 3)
        predicted_salary = "{:,.3f}".format(predicted_salary_f)

        return render_template('linear.html', position_level=f'Position: {int_position_level}',experience=f'Experience: {experience}', prediction_text=f'Predicted Salary Rate: ₱{predicted_salary}')

    else:
        return render_template('linear.html', prediction_text='Error: Invalid input values. Please select a valid position level and enter a numerical value for experience.')


@app.route('/predictknn', methods=['POST'])
def predictknn():
    experience_str = request.form.get('experience')
    salary_str = request.form.get('salary')
    try:
        experience = float(experience_str)
        salary = float(salary_str)
    except ValueError:
        return render_template('knn.html', prediction_text=f"Error: Invalid input value. Please enter a valid numerical value for both experience and salary.")

    features = [[experience, salary]]
    prediction = knn_model.predict(features)
    predicted_job_num = int(prediction[0])
    predicted_job = job_map[predicted_job_num]

    return render_template('knn.html', prediction_text=f'Predicted job: {predicted_job}', experience=f'Experience: {experience}', salary=f'Salary: {salary}')

@app.route('/predictnaive', methods=['GET', 'POST'])
def predictnaive():
    # Get the user's input values
    salary = float(request.form['salary'])
    experience = float(request.form['experience'])

    try:
        if float(experience) < 0 or float(salary) < 0:
            raise ValueError()
        int_features = [salary, experience]

        features = np.array(int_features).reshape(1, -1)
        gaussian_prediction = gaussian_nb.predict(features)
        multinomial_prediction = multinomial_nb.predict(features)
        bernoulli_prediction = bernoulli_nb.predict(features)

        # # Map the predicted job titles to their corresponding string values
        gaussian_prediction = job_map.get(int(gaussian_prediction))
        multinomial_prediction = job_map.get(int(multinomial_prediction))
        bernoulli_prediction = job_map.get(int(bernoulli_prediction))


          # Render the results template with the predicted job classification and accuracy scores
        return render_template('naive.html',
        gaussian_prediction=gaussian_prediction,
        multinomial_prediction=multinomial_prediction,
        bernoulli_prediction=bernoulli_prediction,
        salary=salary,
        experience=experience,
        reset=True)
    
    except:
        return render_template('naive.html')


@app.route('/predictkm', methods=['GET'])
def predictkm():

    # render the HTML template
    return render_template('kmeans.html')

    # # convert the figure to a base64 string for embedding in the HTML template
    # import io
    # import base64
    # buf = io.BytesIO()
    # fig.savefig(buf, format='png')
    # figdata = base64.b64encode(buf.getbuffer()).decode('utf-8')

    # # render the HTML template and pass the figure data to it
    # return render_template('kmeans.html', figdata=figdata)


if __name__ == '__main__':
    app.run(debug=True, port=8000)