def test_extract_all_horoscope_readings(tbs_scraper):
    tbs_scraper.extract_all_horoscope_readings()

    assert tbs_scraper._horoscope_readings['てんびん座'] == {
        'rank': '1位',
        'forecast': 'ロックな音楽で運気上昇',
        'lucky_color': 'オレンジ',
        'lucky_item': 'プレーヤー',
        'advice': ''
    }

    assert tbs_scraper._horoscope_readings['さそり座'] == {
        'rank': '12位',
        'forecast': '職場でダメ出しの予感',
        'lucky_color': '黄色',
        'lucky_item': 'フェイスガード',
        'advice': 'イヤなことがあっても気にしない',
    }
