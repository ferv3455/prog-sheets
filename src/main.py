from parser import parser


if __name__ == '__main__':
    try:
        print(parser.parse("表1 = 表0(日期,名字,成绩)[日期,最大,成绩]:名字!=\"管理员\""))
    except SyntaxError as e:
        raise SyntaxError(e.msg) from None
