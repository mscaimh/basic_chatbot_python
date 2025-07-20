The project implements a basic chatbot in Python.

## Project information
* The basic_chatbot.py file contains the source code for the chatbot.  
  The script was developed using PyCharm IDE, using Python version 3.13.0.
* The chat_templates.properties contains chat templates used by the chatbot to derive response for the chat prompts.

## Steps for deploying the chatbot program:
* Copy the contents of this archive to a local location, say C:/basic_chatbot_python. The resultant directory structure must be as below.
  ```
  C:
  |-- basic_chatbot_python
  	|-- basic_chatbot.py
  	|-- chat_templates.properties
  ```
* Open a command prompt and navigate to the C:/basic_chatbot_python directory.
* Execute the command "py" to check the Python version. Make sure the installed Python version is v3.13.
  ```
  Python 3.13.0 (tags/v3.13.0:60403a5, Oct  7 2024, 09:38:07) [MSC v.1941 64 bit (AMD64)] on win32
  ```
* Execute the below command to start the chatbot program.
  ```
  py basic_chatbot.py
  ```

## Sample chats for testing
- What are the working hours?
- What the social responsibility policy of the organisation?
- How does the organisation handle its social responsibility?
- What is the frequency of pay reviews?
- Does the company offer any employee benifits?
- What is the standard work week look like?
- What is the number of employees in the organisation?
- What tech stack is used for product development?
- Is there a tech strategy?
- What process should I follow if I need a new software installed?

## Observations from testing:
* The model employs a greedy search approach while finding the best template match. Within the derive_chat_response function, the processing workflow sequentially invokes finance, HR and engineering department-specific query handlers. The workflow greedily ends the search on _first_ match instead of completing search across all departments and deriving the _best_ match.  
  This behaviour is evident when testing with the following two input queries:  
  - What the social responsibility policy of the organisation?
  - How does the organisation handle its social responsibility?

When searching with the first input, the workflow identifies the template key "expense.policy", under the Finance department, as the correct match. This is due to the matching of the word "policy" within the input query. A search with the second input string above, which avoids the word "policy" in the input, correctly identifies the template key "social.responsibility" under HR department.  
The workflow can be improved by introducing parallelisation to search across all departments and then carrying out the match frequency comparisons against the entire dataset.
