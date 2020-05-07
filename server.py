import asyncio
from typing import Optional, Deque, Tuple, List, Any
from aioconsole import ainput
from collections import deque
from util.func import Case
from util.levelup import LevelUp
import json
from message import Message
import names
import time
from util.card import Card, CardList, CardSuit

class Server:
    def __init__(self, addr: str = "localhost", port: int = 8888):
        self.game = LevelUp()
        self.clients = []
        self.seats = [None] * 4
        self.names = [
            names.get_full_name(), 
            names.get_full_name(),
            names.get_full_name(),
            names.get_full_name()
        ]
        self.online = []
        self.addr = addr
        self.port = port
        self.curnum = 0
        self.server = None
        self.host = True
        self.qmessage: Deque[bytes] = deque()
        self.timer = None
        self.startGame = False
        self.dispatching = False
        self.discarding = False
    async def newClient(self, reader, writer):
        writer.write(Message.encode({
                "TYPE": "RESPONSE",
                "SUCCESS": True,
                "MESSAGE": "Connected.",
                "HOST": self.host
            }))
        self.host = False
        newclient = (reader, writer, {})
        self.clients.append(newclient)
        self.online.append(newclient)

        data = await reader.read(128)
        message = Message.decode(data)
        print("Received:", message)
        name = message["NAME"]
        newclient[2]["name"] = name
        writer.write(Message.encode({
            "TYPE": "ACCEPTED",
            "MESSAGE": name
        }))
        await writer.drain()
        self.loop.create_task(self.recv(self.curnum))
        self.curnum += 1
                

    # async def recv(self):
    #    while True:
    #        for ID in range(len(self.clients)):
    #            await self._recv(ID)
    async def recv(self, ID):
        print(f"awaiting {ID}.")
        
        while True:
            if self.clients[ID] is None:
                await asyncio.sleep(0.1)
                continue
            reader, writer, info = self.clients[ID]
            data = await reader.read(2048)
            message = Message.decode(data)
            if message["TYPE"][-4:] != 'INFO':
                print("Received %r from %d" % (message, ID))
            success, value, other = self.checkMessage(message)
            if success:
                case = Case(message["TYPE"])
                if case('ROOMINFO'):
                    if self.startGame:
                        writer.write(Message.encode({
                            "TYPE": "INFORM",
                            "MESSAGE": "STARTGAME"
                        }))
                    else:
                        writer.write(Message.encode({
                            "TYPE": "RESPONSE",
                            "SEAT": value,
                            "ONLINE": other
                        }))
                elif case('STARTREQUEST'):
                    writer.write(Message.encode({
                        "TYPE": "ACCEPTED"
                    }))
                    self.startGame = True
                    _, self.dispatch_buffer, self.infomsg = self.game.inform("START")
                    self.front = [[], [], [], []]
                    self.cursuit = None
                    print(self.dispatch_buffer)
                    self.timer = time.time()
                    self.dispatching = True
                elif case('SEATCANCELREQUEST'):
                    writer.write(Message.encode({
                        "TYPE": "ACCEPTED"
                    }))
                    if "seat" in self.clients[ID][2]:
                        self.seats[self.clients[ID][2]["seat"]] = None
                        self.clients[ID][2].pop("seat")
                elif case('SEATREQUEST'):
                    writer.write(Message.encode({
                        "TYPE": "ACCEPTED"
                    }))
                    if "seat" in self.clients[ID][2]:
                        self.seats[self.clients[ID][2]["seat"]] = None
                    self.seats[value] = self.clients[ID]
                    self.clients[ID][2]["seat"] = value
                elif case('DISPATCHINFO'):
                    timer = [0, 0, 0, 0]
                    if self.dispatching:
                        ncount = int((time.time() - self.timer) / 0.5)
                    else:
                        ncount = 25
                        time_left = self.timer + 9 - time.time()
                        timer = [int(time_left) + 1] * 4
                    if ncount > 25:
                        ncount = 25
                        self.dispatching = False
                        time_left = 9
                        self.timer = time.time()
                    if not self.dispatching and time_left < 0:
                        self.game.inform("FINISH")
                        self.discarding = True
                        self.timer = time.time()
                        writer.write(Message.encode({
                            "TYPE": "INFORM",
                            "MESSAGE": "TIMEOUT"
                        }))
                    else:  
                        seat = self.clients[ID][2]["seat"]
                        cards = self.dispatch_buffer[seat][:ncount]
                        count = [ncount, ncount, ncount]
                        front = self.front
                        suit = self.infomsg['suit']
                        rank = self.infomsg['rank']
                        level = self.infomsg['level']
                        suitable = self.game.isSuitable(cards, seat, None)
                        if suit is None:
                            CardList.setHash(None, rank)
                        else:
                            CardList.setHash(suit[0], rank)
                        front = [self.front[(num + seat) % 4] for num in range(4)]
                        if suit is not None:
                            s, id, num = suit
                            suit = (s, (id - seat + 4) % 4, num)
                            timer[(id - seat + 4) % 4] = 0
                        name = [self.names[(num + seat) % 4] for num in range(4)]
                        for id, client in enumerate(self.seats):
                            if client is not None:
                                name[(id + 4 - seat) % 4] = client[2]["name"]
                        writer.write(Message.encode({
                            "TYPE": "RESPONSE",
                            'CARDS': CardList.fromlist(cards).tolist(),
                            'COUNT': count,
                            'FRONT': front,
                            'SUIT': suit,
                            'RANK': rank,
                            'LEVEL': (level[seat % 2], level[1 - seat % 2]),
                            'SUITABLE': suitable,
                            'TIMER': timer,
                            'NAME': name
                        }))
                elif case('SUITREQUEST'):
                    seat = self.clients[ID][2]["seat"]
                    res = self.game.suitRequest(seat, value)
                    if res:
                        self.front = res[0]
                        self.infomsg['suit'] = res[1]
                        if not self.dispatching:
                            self.timer = time.time()
                    writer.write(Message.encode({
                        "TYPE": "ACCEPT"
                    }))  
                elif case('GAMEINFO'):
                    timer = [0, 0, 0, 0]
                    if self.discarding:
                        time_left = 9 - (time.time() - self.timer) / 6
                        if time_left < 0:
                            pass # time out
                        else:
                            pass
                    else:
                        pass
                    seat = self.clients[ID][2]["seat"]
                    timer[(self.game.curPlayerIndex + 4 - seat) % 4] = int(time_left) + 1
                    cards = self.game.players[seat].cardInHand.tolist()
                    count = [self.game.players[(seat + i) % 4].cardInHand.size for i in range(1, 4)]
                    front = [self.game.players[(seat + i) % 4].cardFront.tolist() for i in range(4)]
                    name = [self.names[(num + seat) % 4] for num in range(4)]
                    s, id, num = self.game.suitMain
                    suit = (s, (id - seat + 4) % 4, num)
                    rank = self.game.rankMain
                    level = self.game.rankLevel
                    CardList.setHash(s, rank)
                    
                    for id, client in enumerate(self.seats):
                        if client is not None:
                            name[(id + 4 - seat) % 4] = client[2]["name"]
                    writer.write(Message.encode({
                        "TYPE": "RESPONSE",
                        'CARDS': cards,
                        'COUNT': count,
                        'FRONT': front,
                        'SUIT': suit,
                        'RANK': rank,
                        'LEVEL': (level[seat % 2], level[1 - seat % 2]),
                        'TIMER': timer,
                        'NAME': name
                    }))
            else:
                writer.write(Message.encode({
                        "TYPE": "ERROR",
                        "SUCCESS": False,
                        "MESSAGE": value
                    }))
            await writer.drain()

    def checkMessage(self, message: dict) -> Tuple[bool, Any, str]:
        if 'TYPE' not in message:
            return (False, None, 'Invalid message format. Should contain "TYPE".')
        case = Case(message['TYPE'])
        if case("ROOMINFO"):
            return (True, 
                [None if client is None else client[2]["name"] for client in self.seats], 
                [client[2]["name"] for client in self.online]
            )
        elif case("SEATREQUEST"):
            return self._checkMessageSeatAvailable(message)
        elif case("SEATCANCELREQUEST"):
            return (True, None, 'Cancel Seat.')
        elif case("STARTREQUEST"):
            return (True, None, 'Start Room.')
        elif case("DISPATCHINFO"):
            return (True, None, 'Dispatch')
        elif case("GAMEINFO"):
            return (True, None, 'Game')
        elif case("SUITREQUEST"):
            suit_list = [CardSuit.Joker, CardSuit.Spade, CardSuit.Heart, CardSuit.Club, CardSuit.Diamond]
            return (True, suit_list[message['SUIT']], None)
        else:
            return (False, None, 'Invalid message type.')
    def start(self):
        self.loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.newClient, self.addr, self.port, loop = self.loop)
        tasks = asyncio.gather(coro)
        self.loop.run_until_complete(tasks)
        self.loop.run_forever()

    ## private methods for internal checks
    def _checkMessageSeatAvailable(self, message: dict) -> Tuple[bool, str]:
        if 'ID' not in message or not isinstance(message['ID'], int):
            return (False, None, 'Missing ID or ID not an integer.')
        ID = message['ID']
        if ID < 0 or ID > 4:
            return (False, None, 'Position should be in range (0, 4).')
        if self.seats[ID] is not None:
            return (False, None, f'Position {ID} is already occupied.')
        return (True, ID, f'Assigned position: {ID}.')

if __name__ == "__main__":
    Server('127.0.0.1', 28888).start()
