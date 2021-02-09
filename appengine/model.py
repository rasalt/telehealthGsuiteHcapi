from wtforms import Form,SelectField,IntegerField,TextField, validators, StringField, FieldList, FormField, DateField

class  newoldForm(Form):
    protocol = SelectField(choices=[('yes', 'New Patient'), ('no', 'Existing Patient')])
    username = StringField()

class HomeForm(Form):
    email  = StringField()
    #datefield should be YYYY-MM-DD
    dob    = DateField()
    lastname  = StringField()
    newpatient = SelectField(u'Are you a New or Existint Patient', choices=[('yes', 'New patient'), ('no', 'Existing Patient')])


