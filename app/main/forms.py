from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange


class EditProductForm(FlaskForm):
    name = StringField('Produkt', validators=[DataRequired()])
    maker = StringField('Tillverkare', validators=[DataRequired()])
    category_id = IntegerField('Kategori', validators=[DataRequired(), NumberRange()])
    weight = IntegerField('Storlek (g)', validators=[DataRequired(), NumberRange()])
    protein_content = IntegerField('Protein (g)', validators=[DataRequired(), NumberRange()])
    url = StringField('URL', validators=[DataRequired(), URL()])
    tag_id = StringField('Tag id', validators=[DataRequired()])
    submit = SubmitField('Submit')
