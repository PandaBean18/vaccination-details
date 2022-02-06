from requests import Request, Session
import json
class CowinApi:
    def __init__(self):
        self.url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
        self.session = Session()
        self.data = None

    def get_data(self, pin, date):
        params = {
            'pincode': pin, 
            'date': date
        }
        response = self.session.get(url = self.url, params = params)
        self.data = json.loads(response.text)
        return self.data 

    def get_dates(self):
        dates = []

        for center in self.data['centers']:
            for session in center['sessions']:
                date = session['date']
                if date not in dates: 
                    dates.append(date)

        return dates 

    def get_sessions_for_date(self, date):
        sessions = []

        for center in self.data['centers']:
            for session in center['sessions']:
                current_date = session['date']
                if current_date == date: 
                    session['name'] = center['name']
                    session['fee_type'] = center['fee_type']
                    sessions.append(session)

        return sessions
    
api = CowinApi()
api.get_data(110010, '08-02-2022')
sessions = api.get_sessions_for_date('14-02-2022')
print(sessions)