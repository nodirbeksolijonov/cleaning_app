from openai import OpenAI

client = OpenAI()

def generate_chart_prompt(user_prompt, columns):

    column_list = ", ".join(columns)

    system_prompt = f"""
    You are a data analyst.

    Dataset columns:
    {column_list}

    Decide which chart to generate.

    Return ONLY one of these formats:

    HISTOGRAM column_name
    SCATTER column_x column_y
    BAR column_name
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content