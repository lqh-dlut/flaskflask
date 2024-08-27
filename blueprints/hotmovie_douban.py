from flask import render_template, Blueprint
from models import HotMovie
from datetime import datetime, timedelta
from exts import db, redis_client
import requests
import json
import config

bp = Blueprint('service', __name__)

def get_hot_movies(use_cache=True):
    cache_key = 'hot_movies'
    if use_cache:
        print('use_cache')
        cache_data = redis_client.hgetall(cache_key)
        if cache_data:
            print(cache_data)
            print(type(cache_data))  # dict
            # 如果缓存有数据直接返回数据
            return [json.loads(value.decode()) for value in cache_data.values()]


    hot_movies = fetch_hotmovie_from_douban()

    if use_cache:
        # 将数据存入redis缓存
        print('cache loaded')
        pipe = redis_client.pipeline()
        for movie in hot_movies:
            movie_title = movie['title']
            #在redis存入爬取的数据
            pipe.hset(cache_key, movie_title,  json.dumps(movie))

        pipe.expire(cache_key, 3600) # 1小时后自动清除数据
        pipe.execute()

    return hot_movies
    # 使用数据库达成的
    # HotMovie.query.delete()
    # for hot_movie in hot_movies:
    #     if 'title' in hot_movie:
    #         # 创建 HotMovie 实例
    #         new_movie = HotMovie(title = hot_movie['title'])
    #         i    # 添加到会话
    #             # db.session.add(new_movie)
    #             # db.session.commit()f 'rate' and 'url' in hot_movie:
    #             new_movie.rate = hot_movie['rate']
    #             new_movie.url = hot_movie['url']
    # print(hot_movies)

#爬豆瓣API获取hot_movie
def fetch_hotmovie_from_douban():
    page_limit = 10
    page_start = 0
    url = f'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&page_limit={page_limit}&page_start={page_start}'

    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'

    resp = requests.get(url, headers={'User-Agent': useragent})
    hot_movies = []
    hot_movies += resp.json()['subjects']

    return hot_movies



@bp.route('/hotmovie')
def hotmovie():
    # clear_hot_movies()
    hotmovies = get_hot_movies()
    print(hotmovies)
    print(type(hotmovies))
    # for movie in hotmovies:
    #     print(movie)
    #     print(type(movie))
    #     print(movie['rate'])

    # hotmovies = HotMovie.query.order_by(HotMovie.rate.desc()).all()
    return render_template('hotmovie.html',movies=hotmovies)
