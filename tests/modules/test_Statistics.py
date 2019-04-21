import sys
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import Population
import ChromosomeFactory
import pytest
import Statistics
import matplotlib
import os
if os.environ.get('DISPLAY','') == '':
    print('Warning: no DISPLAY environment variable found. Using matplotlib non-interactive Agg backend')
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import array
import numpy

@pytest.mark.parametrize("statistic, value", [
( 'best-fitness', 8),
( 'worst-fitness', 3 ),
( 'avg-fitness',7 ),
( 'diversity', 0.3 ),
( 'mutation_rate',0.7 )
])
def test_add_statistic(statistic,value):
	statistics = Statistics.Statistics()
	statistics.add_statistic(statistic,value)
	assert len(statistics.statistic_dict[statistic]) == 1
	assert statistics.statistic_dict[statistic] == [value]

@pytest.mark.parametrize("statistic, value", [
( 'junk', 8),
( 'lol', 3 ),
])
def test_errors(statistic,value):
	statistics = Statistics.Statistics()
	with pytest.raises(Exception):
		statistics.add_statistic(statistic,value)

@pytest.mark.parametrize("statistic, value", [
( 'best-fitness', 8),
])
def test_plot(statistic,value):
	statistics = Statistics.Statistics()
	statistics.add_statistic(statistic,value)
	fig = statistics.plot()
	ax = plt.gca()
	line = ax.lines[0]
	assert line.get_xdata() == numpy.ndarray((1,1), buffer=numpy.array([1]),dtype=int)
	assert line.get_ydata() == numpy.ndarray((1,1), buffer=numpy.array([value]),dtype=int)

@pytest.mark.parametrize("statistic, value", [
( 'best-fitness', 8),
('worst-fitness', 2),
( 'avg-fitness',7 ),
])
def test_plot_statistic(statistic,value):
	statistics = Statistics.Statistics()
	statistics.add_statistic(statistic,value)
	fig = statistics.plot_statistic(statistic)
	ax = plt.gca()
	line = ax.lines[0]
	assert line.get_xdata() == numpy.ndarray((1,1), buffer=numpy.array([1]),dtype=int)
	assert line.get_ydata() == numpy.ndarray((1,1), buffer=numpy.array([value]),dtype=int)


@pytest.mark.parametrize("statistic, value", [
( 'best-fitness', 8),
('worst-fitness', 2),
( 'avg-fitness',7 ),
])
def test_plot_statistics(statistic,value):
	statistics = Statistics.Statistics()
	statistics.add_statistic(statistic,value)
	fig = statistics.plot_statistics([statistic])
	ax = plt.gca()
	line = ax.lines[0]
	assert line.get_xdata() == numpy.ndarray((1,1), buffer=numpy.array([1]),dtype=int)
	assert line.get_ydata() == numpy.ndarray((1,1), buffer=numpy.array([value]),dtype=int)
