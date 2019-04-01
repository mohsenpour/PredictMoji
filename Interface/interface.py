import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchtext
import numpy as np

from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, InputForm
from Prediction_Message import Prediction_Message
from LSTM import TweetLSTM
from glove import Glove
from inference import predict

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

# create a glove object
glove = Glove()

# create an LSTM object and load its state dictionary from the checkpoint
model = TweetLSTM(input_size=50, hidden_size=100, num_classes=6, glove = glove.get_glove_emb(), use_gpu=False)
state_dict = torch.load('../checkpoint_biLSTM_Asad.pth', map_location='cpu')
model.load_state_dict(state_dict)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = InputForm()
    prediction_message = Prediction_Message()
    if form.validate_on_submit():
        prediction_message.initial, prediction_message.pred1, prediction_message.pred2, prediction_message.pred3 = \
             predict(model, form.tweet.data, glove.get_glove_emb(), sequence_length=62, use_gpu=False)
        # if form.tweet.data == 'helloworld':
        #     flash('Entered correct input!', 'success')
        #     return redirect(url_for('home'))
        # else:
        #     flash('Invalid Tweet!', 'danger')
    return render_template('home.html', title='DeepFeels', form = form, prediction_message = prediction_message)


if __name__ == '__main__':
    app.run(debug=True)