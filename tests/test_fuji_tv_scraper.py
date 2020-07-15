def test_extract_all_horoscope_readingss(fuji_tv_scraper):
    readings = fuji_tv_scraper.extract_all_horoscope_readings()

    assert readings['やぎ座'] == {
        'rank': 1,
        'forecast': '気合い充分で前進できるパワフル運勢！現状に',
        'advice': {
            'title': 'ラッキーポイント',
            'description': '自分へのご褒美に買ったもの'
        }
    }

    assert readings['ふたご座'] == {
        'rank': 12,
        'forecast': 'つい昔のことを引き合いに出したり、古い資料を',
        'advice': {
            'title': 'おまじない',
            'description': '自分の名前を逆さ読みで3回唱える'
        }
    }
