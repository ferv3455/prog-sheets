import unittest

from src.parser import parser, lexer, ParseSyntaxError
from src.query import simplify_ast


class TestParser(unittest.TestCase):
    def setUp(self):
        self.lexer = lexer
        self.parser = parser

    def testBasic(self):
        ast = self.parser.parse("表1 = 表0(日期,名字,成绩)[日期,最大,成绩]:名字!=\"管理员\",性别=\"男\"")
        simplify_ast(ast)
        # ast.visualize()

    def testOmitted(self):
        strings = [
            "表1 = 表0(日期,名字,成绩)[日期,最大,成绩]:名字!=\"管理员\",性别=\"男\"",
            "表2 = 表1(日期,名字,成绩)[日期,最小,成绩]:名字!=\"学生\",性别=\"女\"",
            "表3 = 表2(日期,名字,成绩)[日期,平均,成绩]:名字!=\"老师\",性别=\"男\"",
            "表4 = 表3(日期,名字,成绩)[日期,总和,成绩]:名字!=\"校长\",性别=\"女\"",
            "表5 = 表4(日期,名字,成绩)[日期,计数]:名字!=\"职员\",性别=\"男\"",
            "表6 = 表5(日期,名字,成绩):名字!=\"管理员\",性别=\"男\"",
            "表7 = 表6(日期,名字,成绩)[日期,最大,成绩]",
            "表8 = 表7(日期,名字,成绩):性别=\"女\"",
            "表9 = 表8(日期,名字,成绩)",
            "表10 = 表9[日期,最大,成绩]",
            "表11 = 表10",
        ]

        for string in strings:
            # print(string)
            ast = self.parser.parse(string)
            simplify_ast(ast)
            # ast.visualize()

    def testParseError(self):
        strings = [
            "表1 = 表0(日期,名字,成绩)[日期,名字,成绩]:名字!=\"管理员\",性别=\"男\"",
        ]

        for string in strings:
            # print(string)
            with self.assertRaises(ParseSyntaxError):
                self.parser.parse(string)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
