import json
import os


data = {
    "doc_id": "41f24764-8497-180c-37d3-a566068b470c",
    "document_name": "фффф",
    "doc_desc": "ппппп",
    "questions": [
        {
            "questionText": "what is 2+2",
            "qustionType": "checkbox",
            "options": [
                {
                    "optionText": "2"
                },
                {
                    "optionText": "Berlin"
                },
                {
                    "optionText": "4"
                }
            ],
            "open": False,
            "required": True
        },
        {
            "questionText": "вопрос 2",
            "qustionType": "radio",
            "options": [
                {
                    "optionText": "Option1"
                },
                {
                    "optionText": "Option2"
                },
                {
                    "optionText": "Option3"
                }
            ],
            "open": True,
            "required": True
        },
        {
            "questionText": "кто убил пушкина",
            "qustionType": "text",
            "options": [
                {
                    "optionText": "Option1"
                }
            ],
            "open": False,
            "required": False
        }
    ]
}

json_str = json.dumps(data)


with open('data.bin', 'wb') as file:
    file.write(json_str.encode('utf-8'))