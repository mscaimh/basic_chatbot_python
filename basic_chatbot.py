# basic_chatbot.py

"""
This script provides the command prompt interface for a basic chatbot.

The implementation uses a procedural workflow, wherein the processing of input query is delegated to three sub-processing
functions, for handling the processing specific to the finance, HR and engineering departments.

"""

import configparser
import sys
import re

# This function encapsulates the logic for deriving the matching key among the input
# chat template keys list for the input query. The function uses a simple frequency
# counter logic to choose the best match. The words within the input query are matched
# with the words within the chat template key. The key with the most matches is
# selected as the best key.
def derive_matching_chat_key(chat_keys, query):
    query_words = query.split()

    # initiate a map to keep track of match frequency
    match_counts = {}
    for query_word in query_words: # for each of the word within the input query
        for chat_key in chat_keys: # we search each of the template keys for match
            # pre format the input word to avoid mismatches likes "strategy?" not matching
            # with "strategy.".
            query_word = query_word.upper()
            query_word = re.sub(r'[^A-Z0-9]', '', query_word)

            # if the template key contains the current word (with either prefixed or
            # suffixed with "." to avoid partial matches - for example, "a" in source query
            # matching all a's in the template prefix).
            if (query_word + ".") in chat_key.upper() or ("." + query_word) in chat_key.upper():
                # match found
                current_count = match_counts.get(chat_key)
                if current_count is None:
                    # if this is the first match, initialise the match count to 1
                    current_count = 1
                else:
                    # if previous match exists, increment the match count
                    current_count += 1
                match_counts[chat_key] = current_count

    if match_counts: # matches were found
        # find the highest match count
        high_count = max(match_counts.values())

        # find the chat template key with the highest match count
        matching_chat_key_final = ""
        for matching_chat_key in match_counts:
            if match_counts[matching_chat_key] == high_count:
                matching_chat_key_final = matching_chat_key

        return matching_chat_key_final

    return None

# This function encapsulates Finance department-specific logic for deriving chat response.
def derive_chat_response_finance(query):
    # first, load the finance related properties
    chat_templates = configparser.RawConfigParser()
    chat_templates.read("chat_templates.properties")

    chat_template_entries = {k: v for k, v in chat_templates.items('finance')}

    # derive the matching key, if any
    matching_chat_key = derive_matching_chat_key(chat_template_entries.keys(), query)

    if matching_chat_key:
        # matching key was found, return corresponding chat response
        return chat_template_entries[matching_chat_key]

    return None

# This function encapsulates HR department-specific logic for deriving chat response.
def derive_chat_response_hr(query):
    # first, load the HR related properties
    chat_templates = configparser.RawConfigParser()
    chat_templates.read("chat_templates.properties")

    chat_template_entries = {k: v for k, v in chat_templates.items('hr')}

    # derive the matching key, if any
    matching_chat_key = derive_matching_chat_key(chat_template_entries.keys(), query)

    if matching_chat_key:
        # matching key was found, return corresponding chat response
        return chat_template_entries[matching_chat_key]

    return None

# This function encapsulates Engineering department-specific logic for deriving chat response.
def derive_chat_response_engineering(query):
    # first, load the engineering related properties
    chat_templates = configparser.RawConfigParser()
    chat_templates.read("chat_templates.properties")

    chat_template_entries = {k: v for k, v in chat_templates.items('engineering')}

    # derive the matching key, if any
    matching_chat_key = derive_matching_chat_key(chat_template_entries.keys(), query)

    if matching_chat_key:
        # matching key was found, return corresponding chat response
        return chat_template_entries[matching_chat_key]

    return None

# This function carries out the main iteration logic to find matching chat response
# across all departments. The workflow utilises a sequential approach, invoking the
# department-specific match finder functions one at a time. The workflow within this
# function employs a greedy search approach while finding the best template match.
# As mentioned earlier, the method invokes the department-specific matcher functions one
# at a time. The workflow greedily ends the search on _first_ match instead of completing
# search across all departments and deriving the _best_ match.
def derive_chat_response(query):
    # check if a matching chat response is found under finance section
    match_finance = derive_chat_response_finance(query)

    if match_finance:
        # match was found under finance section, return corresponding response
        return match_finance

    # check if a matching chat response is found under HR section
    match_hr = derive_chat_response_hr(query)

    if match_hr:
        # match was found under HR section, return corresponding response
        return match_hr

    # check if a matching chat response is found under engineering section
    match_engineering = derive_chat_response_engineering(query)

    if match_engineering:
        # match was found under engineering section, return corresponding response
        return match_engineering

    return None

# This function is the entry point for the chatbot workflow. It accepts
# query from standard input and waits indefinitely until the user
# ends the program by typing in the word "exit".
def listen_to_input_prompts():
    print("Please type your query below and hit Enter.")
    for query in sys.stdin: # waits indefinitely for user input
        if query.rstrip().casefold() == "exit".casefold(): # user has typed in "exit"
            print("ChatBot is terminating.")
            sys.exit()

        # valid query, derive the chat response
        chat_response = derive_chat_response(query)

        if chat_response:
            # a matching chat response was found
            print(chat_response)
        else:
            # no matching response was found
            print("Sorry, I can't answer that currently.")

if __name__ == "__main__":
    listen_to_input_prompts()
