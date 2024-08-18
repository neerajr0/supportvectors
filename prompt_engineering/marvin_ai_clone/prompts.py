CLASSIFY_MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": " Given text and a list of labels, return the label \
            that most closely classifies the text. \
            e.g. text = 'Marvin is so easy to use!' and \
            labels=['positive', 'negative'] would return \
            'positive'. Please only return the response to the query without any extra language."
    }
]

EXTRACT_MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": "Given text and a Pydantic model serialized with json, \
            return a list of instances of this model reflecting \
            instances of that model present in the text. \
            e.g. given model = \
            {'properties': {'city': {'title': 'City', 'type': 'string'}, 'state': {'title': 'State', 'type': 'string'}}, 'required': ['city', 'state'], 'title': 'Location', 'type': 'object'} \
            and text = 'I moved from NY to CHI' \
            the result would be \
            [ \
                Location(city='New York', state='New York'), \
                Location(city='Chicago', state='Illinois') \
            ] \
            Optionally, if instructions are specified, only return those instances \
            that meet the requirements of the instructions. For example, if in the \
            above example, if the instructions are 'locations on the east coast', you \
            would only return the model for New York. \
            Please only return the response to the query without any extra language."
    }
]

GENERATE_MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": "Given a Pydantic model, a text instruction \
            and an integer n representing the number \
            of examples to generate \
            return a list of length n of instances of the model \
            where each instance represents an example of the \
            instruction provided. \
            e.g. given n = 4, instruction = 'cities in the United States named after presidents' \
            and model = \
            {'properties': {'city': {'title': 'City', 'type': 'string'}, 'state': {'title': 'State', 'type': 'string'}}, 'required': ['city', 'state'], 'title': 'Location', 'type': 'object'} \
            the result would be \
            [ \
                Location(city='Washington', state='District of Columbia'), \
                Location(city='Jackson', state='Mississippi'), \
                Location(city='Cleveland', state='Ohio'), \
                Location(city='Lincoln', state='Nebraska'), \
            ] \
            Please only return the response to the query without any extra language."
    }
]

DEFINE_MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": "Given a term, provide a dictionary-style \
            definition of the term, including part(s) of speech \
            and definition(s) - (Note a term can have multiple \
            definitions or parts of speech). \
            Please only return the response to the query without any extra language."
        },
]

SPELL_CHECK_MESSAGES = [
    {"role": "system", "content": "You are a helpful assistant."},
    {
        "role": "user",
        "content": "Given some text, please correct any spelling and grammar errors and return the fixed result. \
            e.g. 'i ate wafles; pankakes; and sirup for brekfist' would become 'I ate waffles, pancakes and syrup for breakfast. \
            Please only return the response to the query without any extra language."
    },
]