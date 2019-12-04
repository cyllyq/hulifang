from examination.models import Chapter, Section, Question, SectionQuestion
import xlrd


'''
excel列：

title 题目
stem 题干
answer 答案
analysis 解析
choice_a 选项A
choice_b 选项B
choice_c 选项C
choice_d 选项D
choice_e 选项E
number 题号
chapter_num 关联章序号
section_num 关联节序号
'''

data = xlrd.open_workbook('question.xls')
sheet = data.sheet_by_index(0)

cols_count = sheet.ncols #列数
rows_count = sheet.nrows #行数

def clear(data):
    if isinstance(data, str):
        return data.strip().strip('\n')
    return data

fields = []
for index in range(cols_count):
    fields.append(sheet.cell_value(0, index))
num = 1
for row in range(1, rows_count):
    question_fields = []
    for col in range(cols_count):
        question_fields.append(clear(sheet.cell_value(row, col)))
    kwargs = dict(zip(fields[:-3], question_fields[:-3]))
    question = Question.objects.create(**kwargs)

    se = Section.objects.get(chapter__number=int(question_fields[-2]), number=int(question_fields[-1]))

    SectionQuestion.objects.create(question=question, section=se, number=int(question_fields[-3]))

    print(num)
    num += 1