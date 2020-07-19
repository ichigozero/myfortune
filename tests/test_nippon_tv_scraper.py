def test_extract_all_horoscope_readings(nippon_tv_scraper):
    nippon_tv_scraper.extract_all_horoscope_readings()

    assert nippon_tv_scraper._horoscope_readings[5] == {
        'rank': 1,
        'forecast': (
            '対人運に恵まれる１日。'
            'あなたの味方が現れるのでたまには甘えてみよう'
        ),
        'lucky_color': '黒'
    }

    assert nippon_tv_scraper._horoscope_readings[3] == {
        'rank': 12,
        'forecast': (
            'プレッシャーに押しつぶされそう。'
            '気を使いすぎて空回りしないでね'
        ),
        'lucky_color': '緑'
    }


def test_filter_horoscope_readings(nippon_tv_scraper):
    nippon_tv_scraper._horoscope_readings = {4: 'foo'}

    assert nippon_tv_scraper.filter_horoscope_readings('4/1') == 'foo'
