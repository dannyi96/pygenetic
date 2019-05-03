from locust import HttpLocust, TaskSet, task

class makeRequests(TaskSet):

    def on_start(self):
        self.begin()

    def begin(self):
        # GET login page
        response = self.client.get('/ga_online')
        
    @task
    def loadPage(self):
    	response = self.client.get('/ga_online')

    @task
    def runPygenetic(self):
        self.client.post('/ga_init',
                         {'gene-generation': '1drange', 'no-of-genes': '8', '1drange-min': '0', '1drange-max': '20', '1drange-duplicate': 'yes', '1dregex-regex': '', '1dregex-datatype': 'int', 'fitness': 'addition', 'custom-fitness': '#Enter fitness func here', 'extra-data': '', 'population-size': '30', 'crossover-rate': '0.4', 'mutation-rate': '0.2', 'fitness-type': 'max', 'fitness-equal': '', 'crossover-type0': 'distinct', 'crossover-weight0': '1', 'custom-crossover0': '#Enter crossover func here', 'mutation-type0': 'swap', 'mutation-weight0': '1', 'custom-mutation0': '#Enter mutation func here', 'selection-type': 'basic', 'custom-selection': '#Enter selection func here', 'no-of-evolutions': '3', 'adaptive-mutation': 'no', 'pySpark': 'no'} )


class WebsiteUser(HttpLocust):
    task_set = makeRequests
