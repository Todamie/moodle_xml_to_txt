import xml.etree.ElementTree as ET
import re
import os

def extract_questions_and_answers(xml_string):
    root = ET.fromstring(xml_string)
    output = []
    
    for question in root.findall("question"):
        # Убираем HTML из текста вопроса
        question_text_raw = question.find("questiontext/text").text
        question_text = clean_html(question_text_raw).strip()
        
        answers = question.findall("answer")
        all_answers = []
        for answer in answers:
            # Убираем HTML из текста ответа
            answer_text_raw = answer.find("text").text
            answer_text = clean_html(answer_text_raw).strip()
            fraction = float(answer.attrib.get("fraction", "0"))
            if fraction > 0:
                all_answers.append(("Правильный ответ", answer_text))
            else:
                all_answers.append(("", answer_text))  # Неправильный ответ без подписи
        
        if all_answers:
            output.append({
                "question": question_text,
                "answers": all_answers
            })
    
    return output

def clean_html(raw_html):
    """Функция для удаления HTML-тегов."""
    clean_text = re.sub(r'<[^>]+>', '', raw_html)  # Удаляет все HTML-теги
    clean_text = re.sub(r'&nbsp;', ' ', clean_text)  # Заменяет &nbsp; на пробел
    clean_text = re.sub(r'&mdash;', '-', clean_text)  # Заменяет &mdash; на -
    clean_text = re.sub(r'&lt;', '<', clean_text)  # Заменяет &lt; на <
    clean_text = re.sub(r'&gt;', '>', clean_text)  # Заменяет &gt; на >
    return clean_text

def format_output(parsed_data):
    formatted = ""
    for item in parsed_data:
        formatted += f"Вопрос: {item['question']}\n"
        for idx, (label, answer) in enumerate(item['answers'], start=1):
            if label:
                formatted += f"{label} {idx}: {answer}\n"
            else:
                formatted += f"{answer}\n"  # Неправильный ответ без подписи
        formatted += "\n"
    return formatted

def save_to_txt(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

# Считываем данные из файла input.xml
try:
    with open("input.xml", "r", encoding="utf-8") as file:
        xml_data = file.read()
except FileNotFoundError:
    print("Файл input.xml не найден. Поместите файл в ту же директорию и повторите попытку.")
    exit(1)

parsed_data = extract_questions_and_answers(xml_data)
formatted_data = format_output(parsed_data)
save_to_txt("output.txt", formatted_data)

print("Данные сохранены в файл 'output.txt'.")
