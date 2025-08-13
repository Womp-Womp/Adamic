#example 1
# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Imagine I just provided you Matthew 5:10
"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""**Formulating a Question**

I'm working on crafting a multiple-choice question from Matthew 5:10, focusing on the concept of persecution for righteousness. The goal is to generate a JSON object with this question and several answer choices. I need to be sure that the answer choices are well-written and appropriate in relation to the Bible verse.


**Constructing the JSON Object**

I've successfully created the JSON object based on the schema, including the version, topic, source passage, and the crafted question. The question focuses on the blessing of those persecuted for righteousness, derived directly from Matthew 5:10. I carefully selected answer choices, ensuring they are relevant to the Beatitudes and the provided verse. The 'correct_index' is set, and the question is labeled as 'easy'. Now I will double-check the object's structure and ensure it fully adheres to the schema before finalizing.


**Crafting the JSON**

I'm now putting together the final JSON object, incorporating all the elements based on the schema and my previous plan. I've focused on ensuring the question aligns precisely with Matthew 5:10 and that the answer choices reflect the relevant context within the Beatitudes. The JSON structure is finalized, with the necessary fields like version, topic, source passage, questions, choices, correct index, and difficulty. I have also added an explanation to provide further context. I'm double-checking the formatting before considering the object complete.


"""),
                types.Part.from_text(text="""{
  \"questions\": [
    {
      \"choices\": [
        \"Because they will inherit the earth\",
        \"Because theirs is the kingdom of heaven\",
        \"Because they will be shown mercy\",
        \"Because they will be comforted\"
      ],
      \"correct_index\": 1,
      \"id\": \"matthew_5_10_q1\",
      \"question\": \"According to Matthew 5:10, what is the reward for those who are persecuted because of righteousness?\",
      \"difficulty\": \"easy\",
      \"explanation\": \"The verse states, 'Blessed are those who are persecuted because of righteousness, for theirs is the kingdom of heaven.' The other options are blessings mentioned in other Beatitudes (Matthew 5:5, 5:7, and 5:4 respectively).\",
      \"tags\": [
        \"Bible\",
        \"New Testament\",
        \"Beatitudes\"
      ]
    }
  ],
  \"version\": \"1.0\",
  \"source_passage\": \"Blessed are those who are persecuted because of righteousness, for theirs is the kingdom of heaven.\",
  \"topic\": \"Matthew 5:10\"
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["questions", "version"],
            properties = {
                "topic": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "High-level subject or passage title the items pertain to.",
                ),
                "source_passage": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Optional full passage used to generate the items.",
                    nullable = "True",
                ),
                "questions": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    description = "MCQ items.",
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["id", "question", "choices", "correct_index"],
                        properties = {
                            "id": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Stable identifier, e.g., 'q1'.",
                            ),
                            "question": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "The MCQ prompt.",
                            ),
                            "choices": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                description = "Answer options in display order.",
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                            "correct_index": genai.types.Schema(
                                type = genai.types.Type.INTEGER,
                                description = "0-based index into 'choices' that indicates the correct answer.",
                            ),
                            "explanation": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Why the correct option is right (and others are not).",
                            ),
                            "difficulty": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Rough difficulty band.",
                                enum = ["easy", "medium", "hard"],
                            ),
                            "tags": genai.types.Schema(
                                type = genai.types.Type.ARRAY,
                                description = "Topical tags or skills (e.g., 'inference', 'dates').",
                                items = genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                            ),
                        },
                    ),
                ),
                "version": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Schema version",
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()


#example 2
# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Imagine we just read Matthew 5:1-10"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""**Defining JSON Structure**

I'm working on the initial JSON structure, referencing the specified schema. I've pinpointed Matthew 5:1-10 as the `source_passage`. My current focus is crafting concise, short-form questions directly derived from this biblical passage.


**Crafting Initial Questions**

My focus is now on generating concise, short-form questions derived from Matthew 5:1-10. I'm aiming to create multiple questions that target various aspects of the passage, incorporating the \"The Beatitudes\" theme. My strategy is to focus on questions around the different blessings mentioned. I'll include questions that directly ask about the content of the verse.


**Generating Targeted Questions**

I've completed the initial structure and incorporated the source passage. Now, I'm generating short-form questions, as planned. The first set of questions is complete, focusing on the core themes of the Beatitudes. I'm now refining them to ensure clarity and relevance, considering expected answer length and hints to guide the user. I'm also adding points to the questions for assessment.


**Compiling the JSON Structure**

I've assembled the question components into the final JSON structure, ensuring all strings are properly double-quoted. I've now completed the initial JSON object based on the schema, including all the questions and their respective attributes. I've ensured there are no comments and that the structure is valid. The object is ready for review.


"""),
                types.Part.from_text(text="""{
  \"questions\": [
    {
      \"id\": \"q1\",
      \"prompt\": \"Where did Jesus go when he saw the crowds?\",
      \"expected_length\": \"phrase\",
      \"hint\": \"The first sentence describes his location.\",
      \"points\": 1
    },
    {
      \"id\": \"q2\",
      \"prompt\": \"According to this passage, what is the reward for the 'poor in spirit'?\",
      \"expected_length\": \"phrase\",
      \"points\": 1
    },
    {
      \"id\": \"q3\",
      \"prompt\": \"What blessing is promised to those who mourn?\",
      \"expected_length\": \"one_sentence\",
      \"points\": 1
    },
    {
      \"id\": \"q4\",
      \"prompt\": \"The text says the meek will inherit something. What is it?\",
      \"expected_length\": \"one_word\",
      \"points\": 1
    },
    {
      \"id\": \"q5\",
      \"prompt\": \"What will happen to those who hunger and thirst for righteousness?\",
      \"expected_length\": \"phrase\",
      \"points\": 1
    },
    {
      \"id\": \"q6\",
      \"prompt\": \"What title are the peacemakers given?\",
      \"expected_length\": \"phrase\",
      \"hint\": \"The blessing relates to their relationship with God.\",
      \"points\": 1
    },
    {
      \"id\": \"q7\",
      \"prompt\": \"Which two groups are promised 'the kingdom of heaven'?\",
      \"expected_length\": \"two_to_three_sentences\",
      \"points\": 2
    }
  ],
  \"source_passage\": \"Now when Jesus saw the crowds, he went up on a mountainside and sat down. His disciples came to him, and he began to teach them. He said: 'Blessed are the poor in spirit, for theirs is the kingdom of heaven. Blessed are those who mourn, for they will be comforted. Blessed are the meek, for they will inherit the earth. Blessed are those who hunger and thirst for righteousness, for they will be filled. Blessed are the merciful, for they will be shown mercy. Blessed are the pure in heart, for they will see God. Blessed are the peacemakers, for they will be called children of God. Blessed are those who are persecuted because of righteousness, for theirs is the kingdom of heaven.'\",
  \"version\": \"1.0\",
  \"topic\": \"The Beatitudes (Matthew 5:1-10)\"
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["source_passage", "questions", "version"],
            properties = {
                "topic": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "High-level subject or passage title.",
                ),
                "source_passage": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "The passage the questions target.",
                ),
                "questions": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    description = "Short-form items with expected length hints.",
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["id", "prompt"],
                        properties = {
                            "id": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Stable identifier, e.g., 's1'.",
                            ),
                            "prompt": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "The short-form question.",
                            ),
                            "expected_length": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Guidance for response length.",
                                enum = ["one_word", "phrase", "one_sentence", "two_to_three_sentences"],
                            ),
                            "points": genai.types.Schema(
                                type = genai.types.Type.NUMBER,
                                description = "Maximum points awarded for this item.",
                            ),
                            "hint": genai.types.Schema(
                                type = genai.types.Type.STRING,
                                description = "Optional clue; omit to avoid scaffolding.",
                            ),
                        },
                    ),
                ),
                "version": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Schema version",
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
#example 3

# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Let's say we just read Matthew 5:10

with these questions
\\\"questions\\\": [
    {
      \\\"id\\\": \\\"q1\\\",
      \\\"prompt\\\": \\\"Where did Jesus go when he saw the crowds?\\\",
      \\\"expected_length\\\": \\\"phrase\\\",
      \\\"hint\\\": \\\"The first sentence describes his location.\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q2\\\",
      \\\"prompt\\\": \\\"According to this passage, what is the reward for the 'poor in spirit'?\\\",
      \\\"expected_length\\\": \\\"phrase\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q3\\\",
      \\\"prompt\\\": \\\"What blessing is promised to those who mourn?\\\",
      \\\"expected_length\\\": \\\"one_sentence\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q4\\\",
      \\\"prompt\\\": \\\"The text says the meek will inherit something. What is it?\\\",
      \\\"expected_length\\\": \\\"one_word\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q5\\\",
      \\\"prompt\\\": \\\"What will happen to those who hunger and thirst for righteousness?\\\",
      \\\"expected_length\\\": \\\"phrase\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q6\\\",
      \\\"prompt\\\": \\\"What title are the peacemakers given?\\\",
      \\\"expected_length\\\": \\\"phrase\\\",
      \\\"hint\\\": \\\"The blessing relates to their relationship with God.\\\",
      \\\"points\\\": 1
    },
    {
      \\\"id\\\": \\\"q7\\\",
      \\\"prompt\\\": \\\"Which two groups are promised 'the kingdom of heaven'?\\\",
      \\\"expected_length\\\": \\\"two_to_three_sentences\\\",
      \\\"points\\\": 2
    }
  ],
  \\\"source_passage\\\": \\\"Now when Jesus saw the crowds, he went up on a mountainside and sat down. His disciples came to him, and he began to teach them. He said: 'Blessed are the poor in spirit, for theirs is the kingdom of heaven. Blessed are those who mourn, for they will be comforted. Blessed are the meek, for they will inherit the earth. Blessed are those who hunger and thirst for righteousness, for they will be filled. Blessed are the merciful, for they will be shown mercy. Blessed are the pure in heart, for they will see God. Blessed are the peacemakers, for they will be called children of God. Blessed are those who are persecuted because of righteousness, for theirs is the kingdom of heaven.'\\\",
  \\\"version\\\": \\\"1.0\\\",
  \\\"topic\\\": \\\"The Beatitudes (Matthew 5:1-10)\\\"
}\"\"\"),

I answer correctly for all of them, except the last one where I give a half asses response
Those persecute for their righteousness is the kingdom of heaven"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(text="""**Analyzing Student Responses**

It's been quite a focus. I'm assessing the student's performance, specifically where they stumbled. The provided material is the Beatitudes, and I'm homing in on that final incorrect answer. The challenge now is to determine *why* they missed that one, and not repeating that error in future responses.


**Refining the Evaluation**

My focus is shifting to dissecting the student's incorrect answer. I'm carefully reviewing the Beatitudes passage to pinpoint the specific reasoning error. The goal is to understand why they misunderstood that final question, which will inform how I approach future evaluations. My aim is to gain a deeper insight into the conceptual hurdles, beyond a surface-level grading.


**Evaluating the Misstep**

The focus is now squarely on the final question, where the student faltered. I am comparing the incorrect answer, \"Those persecute for their righteousness is the kingdom of heaven,\" to the expected answer. I am seeing if any elements can be salvaged or if the answer is thoroughly wrong. I need to understand why they went astray. The goal is to pinpoint the exact misconception behind their response. The goal is to correct the student.


**Evaluating the Response**

I've completed the grading process, carefully examining the student's answers against the Beatitudes passage. I gave the student full marks on the first six questions. However, for the final question about the kingdom of heaven, their response was partially correct, so I awarded one point out of two. I have also prepared the JSON structure for the final output. Now, I am assessing how to convey the partial scoring.


**Generating the Output Structure**

I'm now fully immersed in constructing the JSON array. Each question will be represented as an object containing detailed correctness information, justifications, and scoring. I've designed the template and populated the first few entries. Now, I'm focusing on ensuring consistency and accuracy in the JSON structure. My goal is a clear and easily interpreted output.


**Grading the Responses**

I've meticulously graded the student's answers against the provided passage. The first six responses were spot-on, earning full marks. However, the final answer presented some challenges, leading me to award a partial score. I've designed the JSON structure and populated it with the evaluation details and scoring. Now I'm working on the student's response for the seventh question.


**Compiling the Assessment**

Now I'm constructing the final JSON output, incorporating all the grading details, justifications, and scoring. I'm taking care to ensure clarity and accuracy in the JSON structure for easy interpretation. The focus is on a comprehensive and well-formatted result.


**Assembling the Evaluation**

I'm now integrating the grading data into a comprehensive JSON array. I've populated the array with assessments for each question, including justifications and scoring details. I'm finalizing the format for clarity.


"""),
                types.Part.from_text(text="""{
  \"correctness\": \"partially_correct\",
  \"justification\": \"The student correctly identifies one of the two groups ('those who are persecuted because of righteousness') but fails to mention the other group ('the poor in spirit'). Therefore, the answer is partially correct.\",
  \"max_points\": 2,
  \"points_awarded\": 1,
  \"question_id\": \"q7\",
  \"score\": 0.5,
  \"student_response\": \"Those persecute for their righteousness is the kingdom of heaven\",
  \"version\": \"1.0\",
  \"improvement_suggestions\": [
    \"Reread the passage carefully to find both groups that are promised the same reward. The question asks for two groups.\"
  ],
  \"model_answer\": \"The two groups promised the kingdom of heaven are 'the poor in spirit' and 'those who are persecuted because of righteousness'.\",
  \"question\": \"Which two groups are promised 'the kingdom of heaven'?\",
  \"rubric_criteria\": [
    {
      \"criterion\": \"Identifies 'the poor in spirit' as a group promised the kingdom of heaven.\",
      \"met\": false,
      \"notes\": \"The student did not mention this group.\"
    },
    {
      \"criterion\": \"Identifies 'those who are persecuted because of righteousness' as a group promised the kingdom of heaven.\",
      \"met\": true,
      \"notes\": \"The student correctly identified this group, though with some grammatical errors.\"
    }
  ]
}"""),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""INSERT_INPUT_HERE"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["question_id", "student_response", "correctness", "points_awarded", "max_points", "score", "justification", "version"],
            properties = {
                "question_id": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "ID linking back to the authored short-answer item.",
                ),
                "question": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "The original prompt (echoed for auditability).",
                ),
                "student_response": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Verbatim learner answer being graded.",
                ),
                "correctness": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "High-level judgment.",
                    enum = ["correct", "partially_correct", "incorrect"],
                ),
                "points_awarded": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                    description = "Points earned for this item.",
                ),
                "max_points": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                    description = "Maximum points possible.",
                ),
                "score": genai.types.Schema(
                    type = genai.types.Type.NUMBER,
                    description = "Normalized score in [0,1] for aggregation.",
                ),
                "justification": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Concise rationale referencing the passage and rubric.",
                ),
                "model_answer": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "An exemplar succinct answer.",
                ),
                "rubric_criteria": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    description = "Atomic checks used in grading.",
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["criterion", "met"],
                        properties = {
                            "criterion": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                            "met": genai.types.Schema(
                                type = genai.types.Type.BOOLEAN,
                            ),
                            "notes": genai.types.Schema(
                                type = genai.types.Type.STRING,
                            ),
                        },
                    ),
                ),
                "improvement_suggestions": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    description = "Targeted, student-friendly next steps.",
                    items = genai.types.Schema(
                        type = genai.types.Type.STRING,
                    ),
                ),
                "version": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "Schema version",
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
