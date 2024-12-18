import gradio as gr
from fastapi import FastAPI
import time
from local_query import gradio_query
import local_query

# 创建Gradio界面
def slow_echo(message,history):
    message = str(local_query.gradio_query(message))
    for i in range(len(message)):
        time.sleep(0.01)
        yield  message[: i+1]
    return message
           
demo =gr.ChatInterface(
    slow_echo,
    type="messages",
    chatbot=gr.Chatbot(height=600,show_label='检索框',placeholder='建筑规范条目快速检索'),
    textbox=gr.Textbox(placeholder="输入关键字", container=False, scale=9),
    title="建筑规范相关性条目快速查询",
    description="对现行规范向量库进行检索查询",
    theme="soft",
    examples=["查询规范", "疏散楼梯有哪些要求?", "防火分区如何设置"],
    cache_examples=True,
)

# 创建FastAPI应用
app = FastAPI()

# 将Gradio界面挂载到FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)