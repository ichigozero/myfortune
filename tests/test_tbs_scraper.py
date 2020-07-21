def test_extract_all_horoscope_readings(tbs_scraper):
    tbs_scraper.extract_all_horoscope_readings()

    assert tbs_scraper._horoscope_readings['てんびん座'] == {
        'rank': '1位',
        'rank_title': '',
        'forecast': 'ロックな音楽で運気上昇',
        'lucky_color': 'ラッキーカラー★オレンジ',
        'lucky_item': 'ラッキーアイテム★プレーヤー',
        'advice': ''
    }

    assert tbs_scraper._horoscope_readings['おひつじ座'] == {
        'rank': '2位',
        'rank_title': '“ぐー”な人',
        'forecast': 'ビデオ通話が大活躍',
        'lucky_color': 'ラッキーカラー★ピンク',
        'lucky_item': 'ラッキーアイテム★マイク',
        'advice': ''
    }

    assert tbs_scraper._horoscope_readings['うお座'] == {
        'rank': '6位',
        'rank_title': '“でーじょうぶ”な人',
        'forecast': 'クリエイティブな行動が吉',
        'lucky_color': 'ラッキーカラー★ベージュ',
        'lucky_item': 'ラッキーアイテム★イラスト',
        'advice': ''
    }

    assert tbs_scraper._horoscope_readings['おうし座'] == {
        'rank': '9位',
        'rank_title': '“たいへんかも…”な人',
        'forecast': '不満やイライラがたまりそう',
        'lucky_color': 'ラッキーカラー★銀色',
        'lucky_item': 'ラッキーアイテム★鍋',
        'advice': ''
    }

    assert tbs_scraper._horoscope_readings['さそり座'] == {
        'rank': '12位',
        'rank_title': '“マズイかも…”な人',
        'forecast': '職場でダメ出しの予感',
        'lucky_color': 'ラッキーカラー★黄色',
        'lucky_item': 'ラッキーアイテム★フェイスガード',
        'advice': 'イヤなことがあっても気にしない',
    }
