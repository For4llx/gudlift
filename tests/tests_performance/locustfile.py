from locust import HttpUser, task

class GDLFTPerformanceTest(HttpUser):

    @task
    def showSummary(self):
        """
        Perfomance for competitions
        should take less than 5 secondes
        """
        self.client.post('/showSummary', data={'email': "john@simplylift.co"})
    
    @task
    def purchasePlaces(self):
        """
        Perfomance for total points
        should take less than 2 secondes
        """
        data = {
            'club': 'Simply Lift',
            'competition': 'Spring Festival',
            'places': "1"
        }
        self.client.post('/purchasePlaces', data=data)
