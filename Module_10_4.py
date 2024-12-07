import threading
import random
import time
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name


    def run(self):
        time.sleep(random.randint(3, 10))


class Cafe:
    thread_list = []
    def __init__(self, *tables):
        self.queue = Queue()
        self.tables = list(tables)


    def guest_arrival(self, *guests):
        guests_list = list(guests)
        tables_list = self.tables
        len_guests_list = len(guests_list)
        for i in range(5):
            tables_list[i].guest = guests[i]
            thread1 = guests[i]
            thread1.start()
            Cafe.thread_list.append(thread1)
            print(f'{guests_list[i].name} сел(-а) за стол номер {tables_list[i].number}')
        if len_guests_list > 5:
            for i in range(5, len_guests_list):
                self.queue.put(guests[i])
                print(f'{guests_list[i].name} в очереди')


    def discuss_guests(self):
        while not (self.queue.empty()) or Cafe.table_status(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thread1 = table.guest
                    thread1.start()
                    Cafe.thread_list.append(thread1)


    def table_status(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
