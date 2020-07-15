def test_extract_all_horoscope_readings(nippon_tv_scraper):
    readings = nippon_tv_scraper.extract_all_horoscope_readings()

    assert readings[5] == {
        'rank': 1,
        'forecast': (
            '対人運に恵まれる１日。'
            'あなたの味方が現れるのでたまには甘えてみよう'
        ),
        'lucky_color': '黒'
    }

    assert readings[3] == {
        'rank': 12,
        'forecast': (
            'プレッシャーに押しつぶされそう。'
            '気を使いすぎて空回りしないでね'
        ),
        'lucky_color': '緑'
    }
