from diskcollections.generators import StringGenerator


class TestStringGenerator:

    @staticmethod
    def setup_method():
        StringGenerator.clear()

    def test_increase_letter(self):
        assert StringGenerator.increase_letter('a') == 'b'
        assert StringGenerator.increase_letter('z') == 'A'
        assert StringGenerator.increase_letter('A') == 'B'
        assert StringGenerator.increase_letter('Z') == 'a'

    def test_increase_code(self):
        assert StringGenerator.increase_code('a') == 'b'
        assert StringGenerator.increase_code('az') == 'aA'
        assert StringGenerator.increase_code('aZ') == 'ba'
        assert StringGenerator.increase_code('ZZ') == 'aaa'
        assert StringGenerator.increase_code('ZZaZZ') == 'ZZbaa'

    def test_next(self):
        assert StringGenerator.next(1) == 'a'
        assert StringGenerator.next(1) == 'b'
        assert StringGenerator.next(2) == 'a'
        assert StringGenerator.next(2) == 'b'
        assert StringGenerator.next(2) == 'c'

    def test_delete(self):
        assert StringGenerator.next(1) == 'a'
        assert StringGenerator.next(1) == 'b'
        assert StringGenerator.next(1) == 'c'
        StringGenerator.delete(1)
        assert StringGenerator.next(1) == 'a'
