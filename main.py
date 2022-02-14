from src.config.swagger import swagger

from src.controllers.users import *

app = swagger.app

swagger.run()