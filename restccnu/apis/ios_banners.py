# coding: utf-8
"""
    ios::banners.py
    ```````````````

    华师匣子bannerAPI::IOS版

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder, make sure banners hash-list exist
rds.hset('ios_banners', '_placeholder', '_placeholder')


@api.route('/ios/banner/', methods=['GET'])
def get_ios_banners():
    """ (ios版)
    :function: get_ios_banners
    :args: none
    :rv: 按资源文件名排序的所有banner列表

    redis1(6384): hash list
        key: <banner name>-<qiniu resource name>
        value: <banner url>

    获取所有banner(列表, 按资源文件名排序)
    """
    if rds.hlen('ios_banners') == 1:
        return jsonify({}), 404
    else:
        banners_list = []
        banners = rds.hgetall('ios_banners')
        for banner in banners:
            if banner != '_placeholder':
                try:
                    update = qiniu.info(banner)['putTime']
                except KeyError:
                    update = qiniu.info(banner)
                banners_list.append({
                    "img": qiniu.url(banner),
                    "url": banners.get(banner),
                    "update": update,
                    "filename":  banner,
                })
                sorted_banners_list = sorted(banners_list, key=lambda x: x['filename'])
        return json.dumps(sorted_banners_list, indent=4, ensure_ascii=False), 200


@api.route('/ios/banner/', methods=['POST'])
@admin_required
def new_ios_banner():
    """ (ios版)
    :function: new_ios_banner
    :args: none
    :rv: json message

    添加一个新的banner
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        url = request.get_json().get('url')

        # store in banners hash list
        rds.hset('ios_banners', img, url)
        rds.save()

        return jsonify({}), 201


@api.route('/ios/banner/', methods=['DELETE'])
@admin_required
def delete_ios_banner():
    """ (ios版)
    :function: delete_ios_banner
    :args: none
    :rv: json message
    
    根据名字删除banner
    """
    if request.method == 'DELETE':
        # img = request.get_json().get('img')
        img = request.args.get('name')
        banners = rds.hgetall('ios_banners')
        if img in banners:
            rds.hdel('ios_banners', img)
            rds.save()
            return jsonify({}), 200
        else: return jsonify({}), 404