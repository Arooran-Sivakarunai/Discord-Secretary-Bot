from datetime import datetime 

#Create Invalid Argument Exception
class InvalidArgumentsException(Exception):
    pass

#Weekly_Event Object 
class Weekly_Event():
    def __init__(self, weekday: int, time: str, location: str, title: str) -> None:
        self.weekday = weekday
        self.time = time
        self.location = location
        self.title = title
    
    #Equates object by title and weekday
    def __eq__(self, other: object) -> bool:
        return self.title.lower() == other.title.lower() and self.weekday == other.weekday 

    #Custom Print Statement
    def __str__(self) -> str:
        return f'{self.title} | {self.location}\n{Weekly_Event.get_weekday(self.weekday)} @ {self.time}'
    
    #Helper get_weekday Function
    def get_weekday(weekday: int):
        days = {
            "0":"Monday",
            "1":"Tuesday",
            "2":"Wednesday",
            "3":"Thursday",
            "4":"Friday",
            "5":"Saturday",
            "6":"Sunday",
        }
        return days[str(weekday)]

#One_Time_Event Object
class One_Time_Event():
    def __init__(self, month: int, day: int, time: str, title: str) -> None:
        self.month = month
        self.day = day
        self.time = time
        self.title = title
    
    #Equates objects by title
    def __eq__(self, other: object) -> bool:
        return self.title.lower() == other.title.lower()
    
    #Custom Print Statement
    def __str__(self) -> str:
        return f'{self.title}\n{self.day} {self.month} @ {self.time}'


class Scheduler():
    def __init__(self) -> None:
        self.weekly_events = {
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": []
        }
        self.one_time_events = []

    def add_weekly_event(self, event: Weekly_Event) -> None:
        #Adds new Weekly_Event, else returns InvalidArgumentException
        try:
            self.weekly_events[str(event.weekday)].append(event)
        except Exception as e:
            raise InvalidArgumentsException
        
    def add_one_time_event(self, other_event: One_Time_Event) -> None:
        #Adds new One_Time_Event, else returns InvalidArgumentException
        try:
            self.one_time_events.append(other_event)
        except Exception as e:
            raise InvalidArgumentsException

    def del_weekly_event(self, other_event: Weekly_Event) -> bool:
        #Finds events, compares and deletes the found event. Else, Returns False
        try:
            events = self.weekly_events[str(other_event.weekday)]
            for event in events:
                if event == other_event:
                    events.remove(event)
                    return True
            else:
                raise InvalidArgumentsException
        except Exception as e:
            return False

    def del_one_time_event(self, event: object) -> bool:
        try:
            #Finds events, compares and deletes the found event. Else, Returns False
            self.one_time_events.remove(event)
            return True
        except Exception as e:
            return False
    
    #Resets weekly events
    def reset_weekly_events(self) -> None:
        self.weekly_events = self.weekly_events = {
            "0": [],
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": []
        }

    #Resets one time events
    def reset_one_time_events(self) -> None:
        self.one_time_events = [] 
    
    #Gets give datetime object's event
    def get_dates_events(self, date: datetime) -> str:
        wkday = str(date.weekday())
        day = date.day
        mon = date.month
        
        #Finds all events
        lst = self.weekly_events[wkday]
        for events in self.one_time_events:
            if(events.day == day and events.month == mon):
                lst.append(events)
        
        return lst
    
