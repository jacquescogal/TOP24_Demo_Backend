
from src.models.game_model import GameModel
from src.schemas.game_schemas import GameFacility
class BookingController:
    instance = None
    def __init__(self):
        self.game_model = GameModel()
    
    @classmethod
    async def get_instance(cls):
        if cls.instance is None:
            cls.instance = BookingController()
            await cls.instance.init_all_games()
        return cls.instance
    
    async def init_all_games(self):
        self.bookings = {}
        games = await self.game_model.get_all_games()
        for game in games:
            print(game)
            self.bookings[game['game_name']] = {
                'points_given': game['points_given'],
                'facilitators': game['facilitators'],
                'booked': game.get('booked',None)
            }

    async def check_availability(self, game_name):
        return self.bookings[game_name]['booked'] == None
    
    
    async def book(self, game_name, team_name):
        if self.bookings[game_name]['booked'] == team_name:
            self.bookings[game_name]['booked'] = None
            await self.game_model.remove_booked(game_name)
            return True
        elif self.bookings[game_name]['booked'] != None:
            return False
        # check if the team_name has already booked a slot then cancel it
        for key, value in self.bookings.items():
            if value['booked'] == team_name:
                self.bookings[key]['booked'] = None
        self.bookings[game_name]['booked'] = team_name
        await self.game_model.set_booked(game_name, team_name)
        return True



    async def cancel_team_name(self, team_name):
        for key, value in self.bookings.items():
            if value['booked'] == team_name:
                await self.game_model.remove_booked(key)
                self.bookings[key]['booked'] = None

    async def get_bookings(self):
        return self.bookings
    

    async def award_team_name(self, team_name, points):
        for key, value in self.bookings.items():
            if value['booked'] == team_name:
                self.bookings[key]['points_given'][team_name] = points
                await self.game_model.set_game_points(key, points, team_name)
                await self.cancel_team_name(team_name)
                return True
        return False
    
    async def delete_game(self, game_name):
        if game_name in self.bookings:
            del self.bookings[game_name]
            await self.game_model.delete_game(game_name)
            return True
        return False
    
    async def create_game(self, game_name, game_facilitators):
        print("test,hello")
        if game_name in self.bookings:
            return False
        print(game_facilitators,game_name)
        self.bookings[game_name] = {
            'points_given': {},
            'facilitators': game_facilitators,
            'booked': None
        }
        return True