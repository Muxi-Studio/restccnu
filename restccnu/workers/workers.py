# coding: utf-8
"""
    worker.py
    `````````

    celery异步任务

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
from restccnu import app, webview_board, make_celery, mail
from ..spiders.board import get_webview_board
from werkzeug.exceptions import InternalServerError
# from flask_mail import Message

celery = make_celery(app)

@celery.task(name='cute_board_spider')
def cute_board_spider():
    """
    :function: cute_board_spider

    每隔一天清空通知公告爬虫缓存
    """
    try:
        board_list = get_webview_board()
    except:
        raise InternalServerError()
    webview_board.flushdb()
    webview_board.set('webview_board_list', board_list)
    webview_board.save()


# @celery.task(name='send_mail')
# def send_async_email(msg):
#     """
#     :function: send_mail
#     :**kwargs:
#         {'feedback': feedback, 'contact': contact}
# 
#     发邮件(ios消息反馈)
#     """
#     with app.app_context():
#         mail.send(msg)
