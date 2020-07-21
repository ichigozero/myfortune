def test_extract_all_horoscope_readings(tv_asahi_scraper):
    tv_asahi_scraper.extract_all_horoscope_readings()

    assert tv_asahi_scraper._horoscope_readings['みずがめ座'] == {
        'rank': '1位',
        'forecast': (
            '年上の人や先輩との相性がバッチリ。'
            '会話の中に参考になる情報が。'
            '買い物は定番商品をチェック。'
        ),
        'key_of_fortune': 'イルカのグッズ',
        'lucky_color': '黒',
        'lucky_money': '5',
        'lucky_love': '5',
        'lucky_work': '4',
        'lucky_health': '5'
    }

    assert tv_asahi_scraper._horoscope_readings['おひつじ座'] == {
        'rank': '12位',
        'forecast': (
            '主張するタイミングを間違えそう。'
            '自慢話にならないように気を配りましょう。'
            '大人の対応を。'
        ),
        'key_of_fortune': 'しおり',
        'lucky_color': 'ネイビー',
        'lucky_money': '1',
        'lucky_love': '2',
        'lucky_work': '2',
        'lucky_health': '3'
    }
