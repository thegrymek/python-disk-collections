import collections
import string


class StringGenerator:

    letters = string.ascii_letters
    first_letter = letters[0]
    last_letter = letters[-1]
    _codes = collections.defaultdict(str)

    @classmethod
    def increase_letter(cls, letter):
        if letter == cls.last_letter:
            return cls.first_letter

        index = cls.letters.index(letter)
        return cls.letters[index + 1]

    @classmethod
    def increase_code(cls, code):
        """

        >>> StringGenerator.increase_code('c')
        'd'
        >>> StringGenerator.increase_code('b')
        'c'
        >>> StringGenerator.increase_code('z')
        'A'
        >>> StringGenerator.increase_code('aZ')
        'ba'
        >>> StringGenerator.increase_code('ZZ')
        'aaa'

        :param code: string code, that contains only letters.
        :return:
        """
        reverse_code = list(code[::-1])

        for idx, letter in enumerate(reverse_code):
            new_letter = cls.increase_letter(letter)
            reverse_code[idx] = new_letter

            if new_letter != cls.first_letter:
                break
        else:
            reverse_code += cls.first_letter
        return ''.join(reverse_code[::-1])

    @classmethod
    def next(cls, prefix):
        """Returns next letter added to string gathered from prefix.

        >>> StringGenerator.next('prefix1')
        'a'
        >>> StringGenerator.next('prefix1')
        'b'
        >>> StringGenerator.next('prefix1')
        'c'
        >>> StringGenerator.next('prefix2')
        'a'
        >>> StringGenerator.next('prefix2')
        'b'
        >>> StringGenerator.next('prefix1')
        'd'

        When generator get to 'z', next return will be 'aa'.

        :param prefix: unique string
        :return: new code
        """
        if prefix not in cls._codes:
            cls._codes[prefix] = cls.first_letter
        else:
            cls._codes[prefix] = cls.increase_code(cls._codes[prefix])

        return cls._codes[prefix]

    @classmethod
    def delete(cls, prefix):
        """Removes code in current prefix.

        :param prefix:
        :return:
        """
        cls._codes.pop(prefix, None)

    @classmethod
    def clear(cls):
        cls._codes.clear()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
