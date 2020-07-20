from myfortune import Zodiac


def test_get_zodiac_sign():
    assert Zodiac.get_zodiac_sign(birthdate='3/21') == 'おひつじ座'
    assert Zodiac.get_zodiac_sign(birthdate='4/20') == 'おうし座'
    assert Zodiac.get_zodiac_sign(birthdate='5/21') == 'ふたご座'
    assert Zodiac.get_zodiac_sign(birthdate='6/22') == 'かに座'
    assert Zodiac.get_zodiac_sign(birthdate='7/23') == 'しし座'
    assert Zodiac.get_zodiac_sign(birthdate='8/23') == 'おとめ座'
    assert Zodiac.get_zodiac_sign(birthdate='9/23') == 'てんびん座'
    assert Zodiac.get_zodiac_sign(birthdate='10/24') == 'さそり座'
    assert Zodiac.get_zodiac_sign(birthdate='11/23') == 'いて座'
    assert Zodiac.get_zodiac_sign(birthdate='12/22') == 'やぎ座'
    assert Zodiac.get_zodiac_sign(birthdate='1/20') == 'みずがめ座'
