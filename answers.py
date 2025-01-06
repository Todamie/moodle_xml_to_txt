import xml.etree.ElementTree as ET
import re

def extract_questions_and_answers(xml_string):
    root = ET.fromstring(xml_string)
    output = []
    
    for question in root.findall("question"):
        # Убираем HTML из текста вопроса
        question_text_raw = question.find("questiontext/text").text
        question_text = clean_html(question_text_raw).strip()
        
        answers = question.findall("answer")
        correct_answers = []
        for answer in answers:
            if float(answer.attrib.get("fraction", "0")) > 0:
                # Убираем HTML из текста ответа
                answer_text_raw = answer.find("text").text
                correct_answers.append(clean_html(answer_text_raw).strip())
        
        if correct_answers:
            output.append({
                "question": question_text,
                "correct_answers": correct_answers
            })
    
    return output

def clean_html(raw_html):
    """Функция для удаления HTML-тегов."""
    clean_text = re.sub(r'<[^>]+>', '', raw_html)  # Удаляет все HTML-теги
    clean_text = re.sub(r'&nbsp;', ' ', clean_text)  # Заменяет &nbsp; на пробел
    return clean_text

def format_output(parsed_data):
    formatted = ""
    for item in parsed_data:
        formatted += f"Вопрос: {item['question']}\n"
        for idx, answer in enumerate(item['correct_answers'], start=1):
            formatted += f"  Правильный ответ {idx}: {answer}\n"
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
