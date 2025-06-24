import xml.etree.ElementTree as ET
import re
import os
import glob

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
                all_answers.append(("+", answer_text))
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
        formatted += f"{item['question']}\n"
        
        # Выводим варианты ответов с буквами A) B) C) D)
        for idx, (label, answer) in enumerate(item['answers'], start=1):
            letter = chr(64 + idx)  # A=65, B=66, C=67, D=68
            formatted += f"{letter}) {answer}\n"
        
        # Собираем правильные ответы
        correct_answers = []
        for idx, (label, answer) in enumerate(item['answers'], start=1):
            if label == "+":
                letter = chr(64 + idx)
                correct_answers.append(letter)
        
        # Выводим правильные ответы
        if correct_answers:
            formatted += f"Ответы: {', '.join(correct_answers)}\n"
        
        formatted += "\n"
    return formatted

def save_to_txt(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

# Ищем XML файлы в текущей директории
xml_files = glob.glob("*.xml")

if not xml_files:
    print("XML файлы не найдены в текущей директории.")
    exit(1)

# Обрабатываем каждый найденный XML файл
for xml_file in xml_files:
    try:
        with open(xml_file, "r", encoding="utf-8") as file:
            xml_data = file.read()
        
        # Создаем имя выходного файла
        output_filename = os.path.splitext(xml_file)[0] + ".txt"
        
        parsed_data = extract_questions_and_answers(xml_data)
        formatted_data = format_output(parsed_data)
        save_to_txt(output_filename, formatted_data)
        
        print(f"Данные из файла '{xml_file}' сохранены в файл '{output_filename}'.")
        
    except FileNotFoundError:
        print(f"Файл {xml_file} не найден.")
    except Exception as e:
        print(f"Ошибка при обработке файла {xml_file}: {e}")
