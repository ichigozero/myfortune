from datetime import datetime


class Zodiac:
    @staticmethod
    def get_zodiac_sign(birthdate):
        def _is_birthdate_between_dates(date_1, date_2):
            parsed_date_1 = datetime.strptime(date_1, '%m/%d')
            parsed_date_2 = datetime.strptime(date_2, '%m/%d')
            parsed_birthdate = datetime.strptime(birthdate, '%m/%d')

            # In such case where date_1 = '12/22' and date_2 = '1/19',
            # which leads to parsed_date_1 larger than parsed_2,
            # the year component of parsed_date_2 should be
            # incremented by 1 year so that parsed_date_1
            # will always be less than parsed_date_2
            if parsed_date_1 > parsed_date_2:
                parsed_date_2 = datetime(
                    1901,
                    parsed_date_2.month,
                    parsed_date_2.day
                )

            return parsed_date_1 <= parsed_birthdate <= parsed_date_2

        if _is_birthdate_between_dates('3/21', '4/19'):
            zodiac_sign = 'おひつじ座'
        elif _is_birthdate_between_dates('4/20', '5/20'):
            zodiac_sign = 'おうし座'
        elif _is_birthdate_between_dates('5/21', '6/21'):
            zodiac_sign = 'ふたご座'
        elif _is_birthdate_between_dates('6/22', '7/22'):
            zodiac_sign = 'かに座'
        elif _is_birthdate_between_dates('7/23', '8/22'):
            zodiac_sign = 'しし座'
        elif _is_birthdate_between_dates('8/23', '9/22'):
            zodiac_sign = 'おとめ座'
        elif _is_birthdate_between_dates('9/23', '10/23'):
            zodiac_sign = 'てんびん座'
        elif _is_birthdate_between_dates('10/24', '11/22'):
            zodiac_sign = 'さそり座'
        elif _is_birthdate_between_dates('11/23', '12/21'):
            zodiac_sign = 'いて座'
        elif _is_birthdate_between_dates('12/22', '1/19'):
            zodiac_sign = 'やぎ座'
        elif _is_birthdate_between_dates('1/20', '2/18'):
            zodiac_sign = 'みずがめ座'
        else:
            zodiac_sign = 'うお座'

        return zodiac_sign
