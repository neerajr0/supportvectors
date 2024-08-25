
SYSTEM_PROMPT = "You are emulating the functionality of the AI Engineering toolkit Marvin AI. \
    You will respond to user prompts only with the response, without any extra language, like an API would. \
    If any output schema is provided for the response, be sure to follow that schema."

CLASSIFY_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": "# OBJECTIVE # \
            Given text and a list of labels, return the label \
            that most closely classifies the text. \
            # EXAMPLE # \
            text = 'Marvin is so easy to use!' and \
            labels=['positive', 'negative'] \
            would return 'positive'. \
            # AUDIENCE # \
            Imagine that developers are using you as an API to get structured responses. \
            # RESPONSE # \
            ONLY the answer to the query formatted according to the provided schema. \
            Do not create new \
            labels other than the ones provided. \
            Do not return None or no match, always choose the label that \
            most closely classifies the text."
    }
]

EXTRACT_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
         "content": "# OBJECTIVE # \
            Given text and a Pydantic model serialized with json, \
            return a list of instances of this model reflecting \
            instances of that model present in the text. \
            # EXAMPLE # \
            model = {'properties': {'city': {'title': 'City', 'type': 'string'}, 'state': {'title': 'State', 'type': 'string'}}, 'required': ['city', 'state'], 'title': 'Location', 'type': 'object'} \
            and text = = 'I moved from NY to CHI' \
            would return \
            [ \
                Location(city='New York', state='New York'), \
                Location(city='Chicago', state='Illinois') \
            ] \
            Optionally, if instructions are specified, only return those instances \
            that meet the requirements of the instructions. For example, if in the \
            above example, if the instructions are 'locations on the east coast', you \
            would only return the model for New York. \
            # AUDIENCE # \
            Imagine that developers are using you as an API to get structured responses. \
            # RESPONSE # \
            ONLY the answer to the query formatted according to the provided schema."
    }
]

GENERATE_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
         "content": "# OBJECTIVE # \
            Given a Pydantic model, a text instruction \
            and an integer n representing the number \
            of examples to generate \
            return a list of length n of instances of the model \
            where each instance represents an example of the \
            instruction provided. \
            # EXAMPLE # \
            n = 4 \
            instruction = 'cities in the United States named after presidents' \
            and model = \
            {'properties': {'city': {'title': 'City', 'type': 'string'}, 'state': {'title': 'State', 'type': 'string'}}, 'required': ['city', 'state'], 'title': 'Location', 'type': 'object'} \
            the result would be \
            [ \
                Location(city='Washington', state='District of Columbia'), \
                Location(city='Jackson', state='Mississippi'), \
                Location(city='Cleveland', state='Ohio'), \
                Location(city='Lincoln', state='Nebraska'), \
            ] \
            # AUDIENCE # \
            Imagine that developers are using you as an API to get structured responses. \
            # RESPONSE # \
            ONLY the answer to the query formatted according to the provided schema."
    }
]

DEFINE_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": "# OBJECTIVE # \
            Given a term, provide a dictionary-style \
            definition of the term, including part(s) of speech \
            and definition(s) - (Note a term can have multiple \
            definitions or parts of speech). \
            # EXAMPLE # \
            given the term 'contract', you would return the following: \
            **contract** \
            *noun*  \
            1. A written or spoken agreement, especially one concerning employment, sales, or tenancy, that is intended to be enforceable by law. \
            2. A formal agreement between two or more parties, creating obligations that are enforceable or otherwise recognizable by law. \
            3. In business, a document that outlines terms, conditions, and obligations of parties involved in a transaction. \
            *verb* \
            1. To enter into a formal agreement with another party. \
            2. To decrease in size, number, or range; to shrink. \
            3. To acquire or develop (a disease, debt, etc.). \
            # AUDIENCE # \
            Imagine that developers are using you as an API to get structured responses. \
            # RESPONSE # \
            ONLY the answer to the query formatted according to the provided schema."
    }
]

SPELL_CHECK_MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {
        "role": "user",
        "content": "# OBJECTIVE # \
            Given some text, please correct any spelling and grammar errors and return the fixed result. \
            # EXAMPLE # \
            Given the text 'i ate wafles; pankakes; and sirup for brekfist', you would return \
            'I ate waffles, pancakes and syrup for breakfast.' \
            # AUDIENCE # \
            Imagine that developers are using you as an API to get structured responses. \
            # RESPONSE # \
            ONLY the answer to the query formatted according to the provided schema."
    },
]