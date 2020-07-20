def test_extract_all_horoscope_readingss(fuji_tv_scraper):
    fuji_tv_scraper.extract_all_horoscope_readings()

    assert fuji_tv_scraper._horoscope_readings['やぎ座'] == {
        'rank': '1位',
        'forecast': '気合い充分で前進できるパワフル運勢！現状に',
        'advice_title': '★ラッキーポイント',
        'advice_description': '自分へのご褒美に買ったもの'
    }

    assert fuji_tv_scraper._horoscope_readings['ふたご座'] == {
        'rank': '12位',
        'forecast': 'つい昔のことを引き合いに出したり、古い資料を',
        'advice_title': '★おまじない',
        'advice_description': '自分の名前を逆さ読みで3回唱える'
    }
