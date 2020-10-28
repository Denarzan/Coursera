from abc import ABC, abstractmethod


class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):  # checking for changes
        self.__subscribers.add(
            subscriber)

    def unsubscribe(self, subscriber):  # stop checking for changes
        self.__subscribers.remove(subscriber)

    def notify(self, achievement):  # notify fot changes
        for subscriber in self.__subscribers:
            subscriber.update(achievement)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, achievement):
        pass


class ShortNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = set()  # empty set of achievements

    def update(self, achievement):
        self.achievements.add(achievement['title'])  # add new achievement


class FullNotificationPrinter(AbstractObserver):

    def __init__(self):
        self.achievements = list()  # empty list of achievements

    def update(self, achievement):
        if achievement not in self.achievements:  # check if there is this achievement
            self.achievements.append(achievement)  # add it
