from wtforms import Form, StringField, validators, SubmitField


class BlendingForm(Form):

    # TODO: custom validator
    blended_material_name = StringField(
        label='Name',
        validators=[validators.DataRequired(
            message='Material name cannot be empty')]
    )

    submit = SubmitField('Create blended materials')
