from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime


@dataclass
class Agent:

    ExperienceLevel: int
    AgentID: int = int(datetime.now().strftime("%Y%m%d%H%M%S"))
    State: bool = True

    def __repr__(self):

        return f"El ID del agente es: {self.AgentID}, su experiencia es {self.ExperienceLevel} & su estado es {self.State}"

@dataclass
class Message:
    InitialMessage: str
    PriorityValue: int = 0
    MessageLen: int = 0


    def CalcPriorityValue(self):
        KeywordsValue:Dict = {
            "emergencia": 10, 
            "urgente": 8,
            "fallo crítico": 9,
            "problema": 5,
            "consulta": 2,
            "duda": 1
        }
        self.InitialMessage = self.InitialMessage.lower()
        self.ConvertMessage()
        for Word in self.InitialMessage:
            if Word in KeywordsValue:
                self.PriorityValue += KeywordsValue[Word]
        return self.PriorityValue


    def ConvertMessage(self) -> None:
        self.InitialMessage = self.InitialMessage.split(" ")
    
    def CalcMessageLen(self):
        if self.ExperienceLevel == 1:
            TimeReduction = 0
            EstimatedTime = len(self.InitialMessage) / 10 
        elif self.ExperienceLevel == 1:
            TimeReduction = 0.75
        elif self.ExperienceLevel == 2:
            TimeReduction = 0.5


    def __lt__(self, other: 'Message') -> bool:
        return self.PriorityValue < other.PriorityValue

    def __repr__(self):
        return str(self.PriorityValue)

@dataclass
class PriorityQueue:

    _index: int = 0
    _queue: List[Message] = field(default_factory=list)

    def push(self, item: Message) -> None:
        self._queue.append(item)
        self._index += 1
        item.CalcPriorityValue()
        self._queue.sort(reverse=True)

    def pop(self) -> Message:
        return self._queue.pop()[2]
    
    def First(self) -> Message:
        if self._queue:
            return self._queue[0][2]
        return None
    
    def __repr__(self):
        return "[" + ", ".join(str(message.PriorityValue) for message in self._queue) + "]"
    


def ReadData(PathToTxt):
    messages = PriorityQueue()
    try:
        with open(PathToTxt, 'r', encoding='utf-8') as file:
            for line in file:
                content = line.strip()
                if content:
                    messages.push(Message(InitialMessage=content))
    except FileNotFoundError:
        print(f"Error: The file at {PathToTxt} was not found.")
    return messages

Ola = ReadData("src/Practicas/test.txt")

print(Ola)
