def test_extract_all_horoscope_readings(tv_asahi_scraper):
    tv_asahi_scraper.extract_all_horoscope_readings()

    assert tv_asahi_scraper._horoscope_readings['みずがめ座'] == {
        'rank': '1位',
        'forecast': (
            '年上の人や先輩との相性がバッチリ。'
            '会話の中に参考になる情報が。'
            '買い物は定番商品をチェック。'
        ),
        'lucky_color': 'ラッキーカラー：黒',
        'key_of_fortune': '幸運のカギ：イルカのグッズ',
        'lucky_money': '金運：★★★★★',
        'lucky_love': '恋愛運：★★★★★',
        'lucky_work': '仕事運：★★★★',
        'lucky_health': '健康運：★★★★★',
    }

    assert tv_asahi_scraper._horoscope_readings['おひつじ座'] == {
        'rank': '12位',
        'forecast': (
            '主張するタイミングを間違えそう。'
            '自慢話にならないように気を配りましょう。'
            '大人の対応を。'
        ),
        'lucky_color': 'ラッキーカラー：ネイビー',
        'key_of_fortune': '幸運のカギ：しおり',
        'lucky_money': '金運：★',
        'lucky_love': '恋愛運：★★',
        'lucky_work': '仕事運：★★',
        'lucky_health': '健康運：★★★',
    }
