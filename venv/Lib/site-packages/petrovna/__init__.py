import re
from typing import Tuple, Union, List, Optional


def validate_bic(bic: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка БИК - значение из 9 цифр
    """
    error = None
    if not bic:
        error = 'БИК Пуст'
    elif not re.fullmatch(r'[0-9]+', bic):
        error = 'БИК может состоять только из цифр'
    elif len(bic) != 9:
        error = 'БИК может состоять только из 9 цифр'

    if errors:
        return not bool(error), error
    return not bool(error)


def validate_inn(inn: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка ИНН - значение из 10 или 12 цифр с проеркой контрольной суммы
    """
    error = None
    if not inn:
        error = 'ИНН Пуст'
    elif not re.fullmatch(r'[0-9]+', inn):
        error = 'ИНН может состоять только из цифр'
    elif len(inn) not in [10, 12]:
        error = 'ИНН может состоять только из 10 или 12 цифр'
    else:
        def check_digits(_inn: str, coefficients: List[int]):
            n = 0
            for idx, coefficient in enumerate(coefficients):
                n += coefficient * int(_inn[idx])
            return n % 11 % 10

        if len(inn) == 10:
            n10 = check_digits(inn, [2, 4, 10, 3, 5, 9, 4, 6, 8])
            if n10 == int(inn[9]):
                pass
        elif len(inn) == 12:
            n11 = check_digits(inn, [7, 2, 4, 10, 3, 5, 9, 4, 6, 8])
            n12 = check_digits(inn, [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8])
            if n11 == int(inn[10]) and n12 == int(inn[11]):
                pass
        else:
            error = 'Неправильно введен ИНН'

    if errors:
        return not bool(error), error
    return not bool(error)


def validate_kpp(kpp: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка ИНН - значение из 10 или 12 цифр с проеркой контрольной суммы
    """
    error = None
    if not kpp:
        error = 'КПП пуст'
    elif len(kpp) != 9:
        error = 'КПП может состоять только из 9 знаков (цифр или заглавных букв латинского алфавита от A до Z)'
    elif not re.fullmatch(r'[0-9]{4}[0-9A-Z]{2}[0-9]{3}', kpp):
        error = 'Неправильный формат КПП'
    if errors:
        return not bool(error), error
    else:
        return not bool(error)


def validate_ks(ks: str, bic: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка Кор. счета - значение из 20 цифр с проеркой контрольной суммы
    """
    error = None
    valid_bic = validate_bic(bic)
    if isinstance(valid_bic, tuple):
        error = valid_bic[1]
    elif not ks:
        error = 'К/С Пуст'
    elif not re.fullmatch(r'[0-9]+', ks):
        error = 'К/С может состоять только из цифр'
    elif len(ks) != 20:
        error = 'К/С может состоять только из 20 цифр'
    else:
        bic_ks = '0' + bic[4:6] + ks
        checksum = 0
        for idx, value in enumerate([7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1]):
            checksum += value * (int(bic_ks[idx]) % 10)
        if checksum % 10 == 0:
            pass
        else:
            error = 'Неправильно введен корреспондентский счет'
    if errors:
        return not bool(error), error
    return not bool(error)


def validate_ogrn(ogrn: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка ОГРН - значение из 13 цифр с проеркой контрольной суммы
    """
    error = None
    if not ogrn:
        error = 'ОГРН пуст'
    elif not re.fullmatch(r'[0-9]+', ogrn):
        error = 'ОГРН может состоять только из цифр'
    elif len(ogrn) != 13:
        error = 'ОГРН может состоять только из 13 цифр'
    else:
        n13 = int(ogrn[:-1]) % 11 % 10
        if n13 == int(ogrn[12]):
            pass
        else:
            error = 'Неправильно введен ОГРН'
    if errors:
        return not bool(error), error
    return not bool(error)


def validate_ogrnip(ogrnip: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка ОГРНИП - значение из 15 цифр с проеркой контрольной суммы
    """
    error = None
    if not ogrnip:
        error = 'ОГРНИП пуст'
    elif not re.fullmatch(r'[0-9]+', ogrnip):
        error = 'ОГРНИП может состоять только из цифр'
    elif len(ogrnip) != 15:
        error = 'ОГРНИП может состоять только из 15 цифр'
    else:
        n15 = int(ogrnip[:-1]) % 13 % 10
        if n15 == int(ogrnip[14]):
            pass
        else:
            error = 'Неправильно введен ОГРНИП'
    if errors:
        return not bool(error), error
    return not bool(error)


def validate_rs(rs: str, bic: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка расчетного счета - значение из 20 цифр с проеркой контрольной суммы
    """
    valid_bic = validate_bic(bic)
    error = None
    if isinstance(validate_bic, tuple):
        error = valid_bic[1]
    elif not rs:
        error = 'Р/С Пуст'
    elif not re.fullmatch(r'[0-9]+', rs):
        error = 'Р/С может состоять только из цифр'
    elif len(rs) != 20:
        error = 'Р/С может состоять только из 20 цифр'
    else:
        bic_rs = bic[-3:] + rs
        checksum = 0
        for idx, value in enumerate([7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1]):
            checksum += value * (int(bic_rs[idx]) % 10)
        if checksum % 10 == 0:
            pass
        else:
            error = 'Неправильно введен расчетный счет'
    if errors:
        return not bool(error), error
    return not bool(error)


def validate_snils(snils: str, errors: bool = False) -> Union[bool, Tuple[bool, Optional[str]]]:
    """
        Проверка расчетного счета - значение из 20 цифр с проеркой контрольной суммы
    """
    error = None
    if not snils:
        error = 'СНИЛС пуст'
    elif not re.fullmatch(r'[0-9]+', snils):
        error = 'СНИЛС может состоять только из цифр'
    elif len(snils) != 11:
        error = 'СНИЛС может состоять только из 11 цифр'
    else:
        summ = 0
        for i in range(9):
            summ += int(snils[i]) * (9 - i)
        check_digits = 0
        if summ < 100:
            check_digits = summ
        if summ in [100, 101]:
            pass
        elif summ > 101:
            check_digits = summ % 101
        if int(snils[-2:]) == check_digits:
            pass
        else:
            error = 'Неправильно введен СНИЛС'
    if errors:
        return not bool(error), error
    return not bool(error)
