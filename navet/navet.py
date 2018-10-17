# -*- coding: utf-8 -*-

from __future__ import print_function

import csv
from collections import namedtuple
from itertools import islice, count
import sys

MediaMarkerItem = namedtuple(
    u'MediaMarkerItem',
    [
        u'title',
        u'url',
        u'small_image_url',
        u'image_url',
        u'category',
        u'genre',
        u'author',
        u'publisher',
        u'date_published',
        u'isbn',
        u'list_price',
        u'amazon_price',
        u'asin',
        u'date_registered',
        u'tags',
        u'comment',
        u'rating',
        u'is_wish',
        u'is_owned',
        u'is_favorite',
        u'date_purchased',
        u'purchase_price',
        u'state',
        u'date_finished',
        u'is_private',
    ],
)

def decode_row(row, code='cp932'):
    for i, field in enumerate(row):
        row[i] = field.decode(code)

def encode_row(row, code='cp932'):
    for i, field in enumerate(row):
        if field is not None:
            row[i] = field.encode(code)

def make_media_marker_item(header, row):
    d = dict(zip(header, row))
    return dict(
        title=d[u'タイトル'],
        url=d[u'リンクURL'],
        small_image_url=d[u'イメージ画像URL（小）'],
        image_url=d[u'イメージ画像URL（中）'],
        category=d[u'カテゴリ'],
        genre=d[u'ジャンル'],
        author=d[u'著者'],
        publisher=d[u'出版社（発売元）'],
        date_published=d[u'出版日（発売日）'],
        isbn=d[u'ISBN/JAN'],
        list_price=d[u'定価'],
        amazon_price=d[u'アマゾン価格'],
        asin=d[u'ASIN（アマゾン商品コード）'],
        date_registered=d[u'登録日'],
        tags=d[u'タグ'],
        comment=d[u'コメント'],
        rating=d[u'評価'],
        is_wish=d[u'ウィッシュ'],
        is_owned=d[u'所有'],
        is_favorite=d[u'お気に入り'],
        date_purchased=d[u'購入日'],
        purchase_price=d[u'購入金額'],
        state=d[u'状態'],
        date_finished=d[u'読了日'],
        is_private=d[u'公開・非公開'],
    )

def to_booklog_item(item):
    if item['rating'] == u'0':
        item['rating'] = None
    if item['state'] == u'未読':
        item['state'] = u'積読'
    elif item['state'] == u'読中':
        item['state'] = u'いま読んでる'
    elif item['state'] == u'読了':
        item['state'] = u'読み終わった'
    else:
        item['state'] = u'読みたい'
    item['tags'] = item['tags'].replace(u'\n', u',')
    if item['date_registered'] != u'':
        item['date_registered'] = item['date_registered'].replace(u'/', u'-')
    if item['date_finished'] != u'':
        item['date_finished'] += u' 00:00:00'
    elif item['state'] == u'読み終わった':
        item['date_finished'] = item['date_registered']

def migrate(path, split_lines=sys.maxint):
    outer = dict(logs=[])
    def gen():
        with open(path, 'rb') as f:
            reader = csv.reader(f)
            header = next(reader)
            decode_row(header)
            for row in reader:
                decode_row(row)
                item = make_media_marker_item(header, row)
                to_booklog_item(item)
                if item['asin'] != u'':
                    booklog_row = [
                        u'1',
                        item['asin'],
                        item['isbn'],
                        None,
                        item['rating'],
                        item['state'],
                        None,
                        item['tags'],
                        None,
                        item['date_registered'],
                        item['date_finished'],
                    ]
                    encode_row(booklog_row)
                    yield booklog_row
                else:
                    log = 'title[%s] rating[%s] state[%s] tags[%s] date_registered[%s] date_finished[%s]' % (
                          item['title'], item['rating'], item['state'], item['tags'],
                          item['date_registered'], item['date_finished'])
                    outer['logs'].append(log)
    rows = gen()
    for i in count(0):
        sub = list(islice(rows, split_lines))
        if len(sub) == 0:
            break
        fname = 'result%02d.csv' % i
        print(fname)
        with open(fname, 'wb') as w:
            writer = csv.writer(w)
            for row in sub:
                writer.writerow(row)
    if len(outer['logs']) > 0:
        with open('errors.txt', 'w') as f:
            encode_row(outer['logs'], 'utf-8')
            for line in outer['logs']:
                f.write(line + '\n')
            print('errors.txt')

