import config
from zhipuai import ZhipuAI

def call_zhipuai(user_input,prompt):
    client = ZhipuAI(api_key='Your API')
    response = client.chat.completions.create(
        model = 'glm-4-plus',
        messages=[
        {"role": "user", "content": f"用户需要用关键字{user_input}查询建筑相关的规范，请你根据提供的{prompt}相关的规范条目，对其进行排版，按照“规范名称、规范条目、条目内容、相关性得分的顺序排版”注意在答案中在开头写明引用规范的名称，完整保留规范的内容结果，prompt内容保留原文，不用概括，依据prompt和各个条目末尾得得分数进行相关性排序，如果没有相关规范，请提提示‘没有符合的内容’"}
        ])
    return response.choices[0].message.content

if __name__ =="__main__":
    prompt = ['9．5．3 住宅建筑的楼梯间形式应根据建筑形式、建筑层数、建筑面积以及套房户门的耐火等级等因素确定。在楼梯间的首层应设置直接对外的出口，或将对外出口设置在距离楼梯间不超过15m处。', '9．5．4 住宅建筑楼梯间顶棚、墙面和地面均应采用不燃性材料。']
    user_input = '楼梯相关的规范'
    print(call_zhipuai(user_input,prompt))
