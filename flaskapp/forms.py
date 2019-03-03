from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class PyGeneticForm(FlaskForm):
    chromosome =  StringField('Gene',validators=[DataRequired()])
    genes_per_chromosome = IntegerField('Genes Per Chromosome')
    crossover_prob = FloatField('Crossover Probability')
    mutation_prob = FloatField('Mutation Probability')
    population_size = FloatField('Population Size')
    fitness_func = StringField('Fitness Function',validators=[DataRequired()])
    max_iteration = IntegerField('Maximum Iterations')
    crossover_type = StringField('Crossover Type')
    mutation_type = StringField('Mutation Type')
    selection = StringField('Selection Type')
    submit = SubmitField('Run')
