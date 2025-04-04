import os
import random
import json
import sys

from datetime import datetime
from openai import OpenAI


def simple_chat_test(client):
    try:
        completion = client.chat.completions.create(
            model="deepseek-r1", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                #system 就是 prompt
                {'role': 'system', 'content': 'You are a helpful ElasticSearch assistant. The ElasticSearch version is 6.8.'},
                #user 就是 提问内容
                {'role': 'user', 'content': 'How to query the max age?'}
                ]
        )

        # 通过reasoning_content字段打印思考过程
        print("思考过程：")
        print(completion.choices[0].message.reasoning_content)

        # 通过content字段打印最终答案
        print("最终答案：")
        print(completion.choices[0].message.content)

    except Exception as e:
        print(f"程序出错: {e}", file=sys.stderr)
        return 1

def conversation_chat_test(client):
    def get_response(messages):
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        completion = client.chat.completions.create(model="qwen-plus", messages=messages)
        return completion

    # 初始化一个 messages 数组
    messages = [
        {
            "role": "system",
            "content": """你是一名百炼手机商店的店员，你负责给用户推荐手机。手机有两个参数：屏幕尺寸（包括6.1英寸、6.5英寸、6.7英寸）、分辨率（包括2K、4K）。
            你一次只能向用户提问一个参数。如果用户提供的信息不全，你需要反问他，让他提供没有提供的参数。如果参数收集完成，你要说：我已了解您的购买意向，然后说出收集的参数详情，并告知客户请稍等。""",
        }
    ]
    assistant_output = "欢迎光临百炼手机商店，您需要购买什么尺寸的手机呢？"
    print(f"模型输出：{assistant_output}\n")
    while "我已了解您的购买意向" not in assistant_output:
        user_input = input("请输入：")
        # 将用户问题信息添加到messages列表中
        messages.append({"role": "user", "content": user_input})
        assistant_output = get_response(messages).choices[0].message.content
        # 将大模型的回复信息添加到messages列表中
        messages.append({"role": "assistant", "content": assistant_output})
        print(f"模型输出：{assistant_output}")
        print("\n")

'''
某次返回 通，对应 UTF：E9 80 9A
0000   31 30 36 0d 0a 64 61 74 61 3a 20 7b 22 63 68 6f   106..data: {"cho
0010   69 63 65 73 22 3a 5b 7b 22 64 65 6c 74 61 22 3a   ices":[{"delta":
0020   7b 22 63 6f 6e 74 65 6e 74 22 3a 22 e9 80 9a 22   {"content":"..."
0030   7d 2c 22 66 69 6e 69 73 68 5f 72 65 61 73 6f 6e   },"finish_reason
0040   22 3a 6e 75 6c 6c 2c 22 69 6e 64 65 78 22 3a 30   ":null,"index":0
0050   2c 22 6c 6f 67 70 72 6f 62 73 22 3a 6e 75 6c 6c   ,"logprobs":null
0060   7d 5d 2c 22 6f 62 6a 65 63 74 22 3a 22 63 68 61   }],"object":"cha
0070   74 2e 63 6f 6d 70 6c 65 74 69 6f 6e 2e 63 68 75   t.completion.chu
0080   6e 6b 22 2c 22 75 73 61 67 65 22 3a 6e 75 6c 6c   nk","usage":null
0090   2c 22 63 72 65 61 74 65 64 22 3a 31 37 34 33 37   ,"created":17437
00a0   35 34 35 39 34 2c 22 73 79 73 74 65 6d 5f 66 69   54594,"system_fi
00b0   6e 67 65 72 70 72 69 6e 74 22 3a 6e 75 6c 6c 2c   ngerprint":null,
00c0   22 6d 6f 64 65 6c 22 3a 22 71 77 65 6e 2d 70 6c   "model":"qwen-pl
00d0   75 73 22 2c 22 69 64 22 3a 22 63 68 61 74 63 6d   us","id":"chatcm
00e0   70 6c 2d 63 30 61 62 63 31 66 30 2d 38 34 66 33   pl-c0abc1f0-84f3
00f0   2d 39 39 38 61 2d 61 32 31 31 2d 30 36 36 37 62   -998a-a211-0667b
0100   33 32 33 38 37 31 66 22 7d 0a 0a 0d 0a            323871f"}....

'''
def flowoutput_chat_test(client):
    completion = client.chat.completions.create(
    model="qwen-plus",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"}
    ],
    stream=True
    )

    full_content = ""
    print("流式输出内容为：")
    for chunk in completion:
        # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
        if chunk.choices:
            full_content += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content)
    print(f"完整内容为：{full_content}")

def function_call_test(client):
    # 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
    tools = [
        # 工具1 获取当前时刻的时间
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "当你想知道现在的时间时非常有用。",
                # 因为获取当前时间无需输入参数，因此parameters为空字典
                "parameters": {}
            }
        },  
        # 工具2 获取指定城市的天气
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {  
                    "type": "object",
                    "properties": {
                        # 查询天气时需要提供位置，因此参数设置为location
                        "location": {
                            "type": "string",
                            "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                        }
                    }
                },
                "required": [
                    "location"
                ]
            }
        }
    ]

    # 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
    def get_current_weather(arguments):
        # 定义备选的天气条件列表
        weather_conditions = ["晴天", "多云", "雨天"]
        # 随机选择一个天气条件
        random_weather = random.choice(weather_conditions)
        # 从 JSON 中提取位置信息
        location = arguments["location"]
        # 返回格式化的天气信息
        return f"{location}今天是{random_weather}。"

    # 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
    def get_current_time():
        # 获取当前日期和时间
        current_datetime = datetime.now()
        # 格式化当前日期和时间
        formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        # 返回格式化后的当前时间
        return f"当前时间：{formatted_time}。"

    # 封装模型响应函数
    def get_response(messages):
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=messages,
            tools=tools
            )
        return completion

    def call_with_messages():
        print('\n')
        messages = [
                {
                    "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
                    "role": "user"
                }
        ]
        print("-"*60)
        # 模型的第一轮调用
        i = 1
        first_response = get_response(messages)
        assistant_output = first_response.choices[0].message
        print(f"\n第{i}轮大模型输出信息：{first_response}\n")
        if  assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
        # 如果不需要调用工具，则直接返回最终答案
        if assistant_output.tool_calls == None:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
            print(f"无需调用工具，我可以直接回复：{assistant_output.content}")
            return
        # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
        while assistant_output.tool_calls != None:
            # 如果判断需要调用查询天气工具，则运行查询天气工具
            tool_info = {"content": "","role": "tool", "tool_call_id": assistant_output.tool_calls[0].id}
            if assistant_output.tool_calls[0].function.name == "get_current_weather":
                # 提取位置参数信息
                argumens = json.loads(assistant_output.tool_calls[0].function.arguments)
                tool_info["content"] = get_current_weather(argumens)
            # 如果判断需要调用查询时间工具，则运行查询时间工具
            elif assistant_output.tool_calls[0].function.name == 'get_current_time':
                tool_info["content"] = get_current_time()
            tool_output = tool_info["content"]
            print(f"工具输出信息：{tool_output}\n")
            print("-"*60)
            messages.append(tool_info)
            assistant_output = get_response(messages).choices[0].message
            if assistant_output.content is None:
                assistant_output.content = ""
            messages.append(assistant_output)
            i += 1
            print(f"第{i}轮大模型输出信息：{assistant_output}\n")
        print(f"最终答案：{assistant_output.content}")

    call_with_messages()


def multi_model_visual_understand_test(client):
    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}]},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                    },
                },
                {"type": "text", "text": "图中描绘的是什么景象？"},
            ],
        }
    ]
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=messages,
        )
    print(f"第一轮输出：{completion.choices[0].message.content}")
    assistant_message = completion.choices[0].message
    messages.append(assistant_message.model_dump())
    messages.append({
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": "做一首诗描述这个场景"
            }
            ]
        })
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=messages,
        )
    print(f"第二轮输出：{completion.choices[0].message.content}")

def multi_model_visual_think_test(client):    
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复

    # 创建聊天完成请求
    completion = client.chat.completions.create(
        model="qvq-max",  # 此处以 qvq-max 为例，可按需更换模型名称
        messages=[
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful assistant."}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN_!!6000000002727-0-tps-1024-406.jpg"
                        },
                    },
                    {"type": "text", "text": "这道题怎么解答？"},
                ],
            },
        ],
        stream=True,
        # 解除以下注释会在最后一个chunk返回Token使用量
        # stream_options={
        #     "include_usage": True
        # }
    )

    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content

    # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    # print(reasoning_content)
    # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    # print(answer_content)
    multi_model_visual_think_test(client)


def embedding_test(client):    
    completion = client.embeddings.create(
        model="text-embedding-v3",
        input='衣服的质量杠杠的，很漂亮，不枉我等了这么久啊，喜欢，以后还来这里买',
        dimensions=1024, # 指定向量维度（仅 text-embedding-v3 支持该参数）
        encoding_format="float"
    )

    print(completion.model_dump_json())

if __name__ == "__main__":    
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        #api_key='sk-12345678', # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    #simple_chat_test(client)
    #conversation_chat_test(client)
    #flowoutput_chat_test(client)
    #function_call_test(client)
    #multi_model_visual_understand_test(client)
    #multi_model_visual_think_test(client)
    embedding_test(client)


