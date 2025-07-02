from flask import Flask, render_template, request, redirect, flash
from wtforms import Form, FloatField, IntegerField, SelectField, validators
from flask_wtf import FlaskForm
from wtforms.validators import NumberRange, InputRequired
import joblib
import pandas as pd
import numpy as np

model = joblib.load('loan_model.pkl')
encoder = joblib.load('encoder.pkl')
scaler = joblib.load('scaler.pkl')

def features_engineer(eva_df):
  to_be_scaled = ["income", 'amount_requested']
  main = ['age', 'home_owner', 'has_debt', 'risk_score_log', 'average_risk_score', 'average_ext_quality_score', 'month_current_address', 'total_month_employed', 'total_month_personal_account', 'inquiries_last_month']
  eva_df_cat = encoder.transform(eva_df[['pay_schedule']])
  # Get column names for encoded features
  encoded_columns = encoder.get_feature_names_out(['pay_schedule'])
  eva_df_cat_df = pd.DataFrame(eva_df_cat, columns=encoded_columns, index=eva_df.index)

  eva_df["month_current_address"] = eva_df['current_address_year'] * 12
  eva_df["total_month_employed"] = eva_df["months_employed"] + (12 * eva_df["years_employed"])
  eva_df["total_month_personal_account"] = eva_df["personal_account_m"] + (12 * eva_df["personal_account_y"])
  eva_df['risk_score_log'] = np.log(eva_df['risk_score'])
  eva_df['average_risk_score'] = eva_df[['risk_score_2', 'risk_score_3', 'risk_score_4', 'risk_score_5']].mean(axis=1)
  eva_df['average_ext_quality_score'] = eva_df[['ext_quality_score', 'ext_quality_score']].mean(axis=1)


  # Standardize features
  eva_df_scaled = scaler.transform(eva_df[to_be_scaled])
  eva_df_scaled_df = pd.DataFrame(eva_df_scaled, columns=eva_df[to_be_scaled].columns, index=eva_df.index)

  eva_df_encoded = pd.concat([eva_df[main], eva_df_cat_df, eva_df_scaled_df], axis=1)

  return eva_df_encoded


app = Flask(__name__)
app.secret_key = 'secret'
app.config['WTF_CSRF_ENABLED'] = False

class ApplicationForm(FlaskForm):
    age = IntegerField('Age', [InputRequired(), NumberRange(min=0)])
    pay_schedule = SelectField('Pay Schedule', choices=[
        ('bi-weekly', 'Bi-weekly'),
        ('weekly', 'Weekly'),
        ('semi-monthly', 'Semi-monthly'),
        ('monthly', 'Monthly')
    ])
    home_owner = SelectField('Home Owner', choices=[('1', 'Yes'), ('0', 'No')])
    income = FloatField('Income', [InputRequired(), NumberRange(min=0)])
    months_employed = IntegerField('Months Employed', [InputRequired(), NumberRange(min=0, max=11)])
    years_employed = IntegerField('Years Employed', [InputRequired(), NumberRange(min=0)])
    current_address_year = IntegerField('Years at Current Address', [InputRequired(), NumberRange(min=0)])
    personal_account_m = IntegerField('Personal Account Months', [InputRequired(), NumberRange(min=0, max=11)])
    personal_account_y = IntegerField('Personal Account Years', [InputRequired(), NumberRange(min=0)])
    has_debt = SelectField('Has Debt', choices=[('1', 'Yes'), ('0', 'No')])
    amount_requested = FloatField('Amount Requested', [InputRequired(), NumberRange(min=0)])
    risk_score = FloatField('Risk Score', [InputRequired(), NumberRange(min=1000, max=10000)])
    risk_score_2 = FloatField('Risk Score 2', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    risk_score_3 = FloatField('Risk Score 3', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    risk_score_4 = FloatField('Risk Score 4', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    risk_score_5 = FloatField('Risk Score 5', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    ext_quality_score = FloatField('External Quality Score', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    ext_quality_score_2 = FloatField('External Quality Score 2', [InputRequired(), NumberRange(min=0.0, max=1.0)])
    inquiries_last_month = IntegerField('Inquiries Last Month', [InputRequired(), NumberRange(min=0)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ApplicationForm()
    if form.validate_on_submit():
        data = {field.name: field.data for field in form}
        flash('Form submitted successfully!', 'success')
        df = pd.DataFrame(data, index=[0])
        input_df = features_engineer(df)
        pred = model.predict(input_df)
        data['predicted e_signed'] = pred[0]
        probability = model.predict_proba(input_df)[0][pred]

        data['percentage_certainty(%)'] = round(probability[0] * 100, 2)
        return render_template('result.html', data=data)
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)

