import aiohttp, json, asyncio 
from enum import Enum

class GiphyType(Enum):
    GIF = 1
    STICKER = 2

class GiphyAPI:

    __giphy_token = None
    __validate = False
    __BASE_URL_GIFS = "http://api.giphy.com/v1/gifs/"
    __BASE_URL_STICKERS = "http://api.giphy.com/v1/stickers/"

    def __init__(self, token):
        self.__giphy_token = token

    async def get_trendings(self, giphy_type : GiphyType, limit : int) -> dict:
        session = aiohttp.ClientSession()
        params = {
            'api_key' : self.__giphy_token,
            'limit' : limit
        }

        if giphy_type.value == 1:
            trending_response = await session.get(f'{self.__BASE_URL_GIFS}trending', params = params)
        elif giphy_type.value == 2:
            trending_response = await session.get(f'{self.__BASE_URL_STICKERS}trending', params = params)
        
        trending_results = json.loads(await trending_response.text())
        await session.close()
        if not await self.verify(trending_results):
            raise Exception
        return trending_results

    async def get_search(self, giphy_type : GiphyType, search : str, limit : int) -> dict:
        session = aiohttp.ClientSession()
        query_search = search.replace(' ', '+')
        params = {
            'api_key' : self.__giphy_token,
            'q' : query_search,
            'limit' : limit
        }

        if giphy_type.value == 1:
            search_response = await session.get(f'{self.__BASE_URL_GIFS}search', params = params)
        elif giphy_type.value == 2:
            search_response = await session.get(f'{self.__BASE_URL_STICKERS}search', params = params)
        
        search_results = json.loads(await search_response.text())
        await session.close()
        if not await self.verify(search_results):
            raise Exception
        return search_results

    async def get_random_search(self, giphy_type : GiphyType, search : str) -> dict:
        session = aiohttp.ClientSession()
        query_search = search.replace(' ', '+')
        params = {
            'api_key' : self.__giphy_token,
            'tag' : query_search
        }

        if giphy_type.value == 1:
            random_response = await session.get(f'{self.__BASE_URL_GIFS}random', params = params)
        elif giphy_type.value == 2:
            random_response = await session.get(f'{self.__BASE_URL_STICKERS}random', params = params)
        
        random_results = json.loads(await random_response.text())
        await session.close()
        if not await self.verify(random_results):
            raise Exception
        return random_results

    async def verify(self, data : dict) -> bool:
        status = data['meta']
        if status['status'] not in (400, 403, 429, 404):
            self.__validate = True
            return self.__validate
        else:
            print(f"{status['status']} : {status['msg']}")
            return self.__validate
    


class TenorAPI:

    __tenor_token = None
    __validate = False
    __BASE_URL = "https://api.tenor.com/v1/"

    def __init__(self, token):
        self.__tenor_token = token

    async def get_trendings(self, limit : int) -> dict:
        session = aiohttp.ClientSession()
        params = {
            'key' : self.__tenor_token,
            'limit' : limit
        }
        trending_response = await session.get(f'{self.__BASE_URL}trending', params = params)
        trending_results = json.loads(await trending_response.text())
        await session.close()
        if not await self.verify(trending_response):
            raise Exception
        return trending_results

    async def get_search(self, search : str, limit : int) -> dict:
        session = aiohttp.ClientSession()
        query_search = search.replace(' ', '+')
        params = {
            'key' : self.__tenor_token,
            'q' : query_search,
            'limit' : limit
        }
        search_response = await session.get(f'{self.__BASE_URL}search', params = params)
        search_results = json.loads(await search_response.text())
        await session.close()
        if not await self.verify(search_response):
            raise Exception
        return search_results

    async def get_random_search(self, search : str, limit : int) -> dict:
        session = aiohttp.ClientSession()
        query_search = search.replace(' ', '+')
        params = {
            'key' : self.__tenor_token,
            'q' : query_search,
            'limit' : limit
        }
        random_response = await session.get(f'{self.__BASE_URL}random', params = params)
        random_results = json.loads(await random_response.text())
        await session.close()
        if not await self.verify(random_response):
            raise Exception
        return random_results

    async def verify(self, status : aiohttp.client_reqrep.ClientResponse) -> bool:
        if status.status == 200 or status.status == 202:
            self.__validate = True
            return self.__validate
        else:
            return self.__validate


class Giphy:

    __SOURCE = "Giphy!"
    __THUMBNAIL = "https://giphy.com/static/img/giphy_logo_square_social.png"

    def __init__(self, data):
        self._data = data
        
    @classmethod
    def get_source(cls):
        return cls.__SOURCE

    @classmethod
    def get_thumbnail(cls):
        return cls.__THUMBNAIL

    @property
    def get_author(self):
        if 'user' in self._data:
            self.author = self._data['user']['display_name']
            if self.author in ['', ' ']:
                self.author = self._data['user']['username']
                if self.author in ['', ' ']:
                    self.author = 'Autor desconocido'
        else:
            self.author = 'Autor desconocido'
        return self.author

    @property
    def get_author_url(self):
        if 'user' in self._data:
            self.author_url = self._data['user']['profile_url']
        else:
            self.author_url = ''
        return self.author_url

    @property
    def get_author_avatar(self):
        if 'user' in self._data:
            self.author_avatar = self._data['user']['avatar_url']
            return self.author_avatar
        else:
            self.author_avatar = ''
            return self.author_avatar

    @property 
    def get_title(self):
        if not self._data['title'] in ['', ' ']:
            self.title = self._data['title']
            return self.title
        else:
            self.title = 'N/A'
            return self.title

    @property
    def get_id(self):
        self.id = self._data['id']
        return self.id

    @property
    def get_url(self):
        self.url = self._data['images']['original']['url']
        return self.url

    @property
    def get_content_source(self):
        if not self._data['source'] in ['', ' ']:
            self.content_source = self._data['source']
            return self.content_source
        else:
            self.content_source = 'Fuente desconocida'
            return self.content_source

    @property
    def get_search_address(self):
        if 'stickers' in self._data['url'][:27]:
            self.search_address = f"https://giphy.com/stickers/{self.get_id}"
        else:
            self.search_address = f"https://giphy.com/gifs/{self.get_id}"
        return self.search_address


class Tenor:
    
    __SOURCE = "Tenor!"
    __THUMBNAIL = "https://www.brandchannel.com/wp-content/uploads/2017/04/tenor-logo.jpg"

    def __init__(self, data):
        self._data = data

    @classmethod
    def get_thumbnail(cls):
        return cls.__THUMBNAIL

    @classmethod
    def get_source(cls):
        return cls.__SOURCE

    @property
    def get_title(self):
        if not self._data['title'] in ['', ' ']:
            self.title = self._data['title']
        else:
            self.title = 'N/A'
        return self.title

    @property
    def get_id(self):
        self.id = self._data['id']
        return self.id

    @property
    def get_search_address(self):
        self.search_address = f"https://tenor.com/view/{self.get_id}"
        return self.search_address

    @property
    def get_url(self):
        self.url = self._data['media'][0]['gif']['url']
        return self.url


#cliente = TenorAPI("87NYM0CK0LBX")


#asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
#loop = asyncio.get_event_loop()
#try:
#	print(loop.run_until_complete(cliente.get_trendings(1)))
#	loop.run_until_complete(asyncio.sleep(1.0))
#finally:
#	loop.close()


#print(asyncio.run(cliente.get_trendings(1)))
