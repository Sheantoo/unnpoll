import json
import database as db

def parse_json_document(json_arr):
    parsed_documents = []
    
    for arr in json_arr:
        data = json.loads(arr)
        doc_id = data["doc_id"]
        document_name = data["document_name"]
        doc_desc = data["doc_desc"]
        questions = data["questions"]
        
        parsed_questions = []
        for question in questions:
            question_text = question["questionText"]
            question_type = question["qustionType"]
            options = question["options"]
            open = question["open"]
            required = question["required"]
            
            parsed_question = {
                "question_text": question_text,
                "question_type": question_type,
                "options": options,
                "open": open,
                "required": required,
            }
            parsed_questions.append(parsed_question)
        
        parsed_document = {
            "doc_id": doc_id,
            "document_name": document_name,
            "doc_desc": doc_desc,
            "questions": parsed_questions,
        }
        
        parsed_documents.append(parsed_document)
    
    return parsed_documents
js_arr = [
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b170c","document_name":"фффф","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b270c","document_name":"выола","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b370c","document_name":"ылова","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b470c","document_name":"зщшз","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}',
    '{"doc_id":"41f24764-8497-180c-37d3-a566068b570c","document_name":"ывлорщ","doc_desc":"ппппп","questions":[{"questionText":"what is 2+2","qustionType":"checkbox","options":[{"optionText":"2"},{"optionText":"Berlin"},{"optionText":"4"}],"open":false,"required":true},{"questionText":"вопрос 2","qustionType":"radio","options":[{"optionText":"Option1"},{"optionText":"Option2"},{"optionText":"Option3"}],"open":true,"required":true},{"questionText":"кто убил пушкина","qustionType":"text","options":[{"optionText":"Option1"}],"open":false,"required":false}]}'
]



