def test_extract_all_horoscope_readings(nippon_tv_scraper):
    nippon_tv_scraper.extract_all_horoscope_readings()

    assert nippon_tv_scraper._horoscope_readings[5] == {
        'rank': '1位',
        'rank_group': '超スッキリす',
        'forecast': (
            '対人運に恵まれる１日。'
            'あなたの味方が現れるのでたまには甘えてみよう'
        ),
        'lucky_color': 'ラッキーカラー：黒'
    }

    assert nippon_tv_scraper._horoscope_readings[7] == {
        'rank': '2位',
        'rank_group': 'スッキリす',
        'forecast': '次のステージに飛躍できるチャンスの時だよ',
        'lucky_color': 'ラッキーカラー：むらさき'
    }

    assert nippon_tv_scraper._horoscope_readings[4] == {
        'rank': '7位',
        'rank_group': 'まあまあスッキリす',
        'forecast': '浮かんだアイデアはメモしておけば後で役立つよ',
        'lucky_color': 'ラッキーカラー：茶'
    }

    assert nippon_tv_scraper._horoscope_readings[3] == {
        'rank': '12位',
        'rank_group': 'がっかりす',
        'forecast': (
            'プレッシャーに押しつぶされそう。'
            '気を使いすぎて空回りしないでね'
        ),
        'lucky_color': 'ラッキーカラー：緑'
    }


def test_filter_horoscope_readings(nippon_tv_scraper):
    nippon_tv_scraper._horoscope_readings = {4: 'foo'}

    assert nippon_tv_scraper.filter_horoscope_readings('4/1') == 'foo'
