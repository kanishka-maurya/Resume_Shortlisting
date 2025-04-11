from langchain.prompts import PromptTemplate
Extracted_Prompt_Template = PromptTemplate(
    input_variables=["extracted_resume_text"],
    template='''You are an AI assistant specialized in extracting and summarizing key information from Resume Text. Given a Resume text data, analyze
    it and return a structured summary in valid JSON format, capturing only the most essential details.

    Resume Text:
    {extracted_resume_text}

    Return the following output strictly in the JSON format:

    "Full Name": "[Extracted Full Name of Candidate]",
    "Email": "[Extracted Email Address of Candidate (if available)]",
    "Phone Number": "[Extracted Phone Number of Candidate (if available)]",
    "Education":[
        "Extracted Education 1 (Degree,Field,University,Location,Year)",
        "Extracted Education 2 (Degree,Field,University,Location,Year)",
        "Extracted Education 3 (Degree,Field,University,Location,Year)"
    ],
    "Experiences": [
        "Experience 1 in any company with role and duration",
        "Experience 2 in any company with role and duration"
    ],
    "Skills": [
        "Extracted technical or soft skill 1",
        "Extracted technical or soft skill 2"
    ],
    "Core Qualifications": [
        " qualification 1 ",
        " qualification 2 "
    ]
    "Tech Stack":[
        "Tech Stack 1",
        "Tech Stack 2"
    ]
     ### **Guidelines:**
    - Ensure the JSON output is valid and properly formatted.
    - Omit any section if the relevant information is not available in the CV.
    - Keep responses concise and free from unnecessary text.
    - Do not include any additional explanations—only return pure JSON.
    - RETURN IT IN PURE DICTIONARY FORMAT AND NOT STRING.
    - DO NOT RETURN DICTIONARY AS STRING.
    Omit empty data Keep responses concise and free from unnecessary text.There should be no header and text 
    mentioning what you have done, it should just be pure JSON.

    "COMPULSORY"
    Keep the token size of text to be not more than 4000 that is why extract only really important information.
    '''
    )


