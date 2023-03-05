import unittest
import openai


def ask_ai(question) -> str:
    completion = openai.Completion.create(engine="text-davinci-003", prompt=question, max_tokens=1000)
    text = completion.choices[0]['text']
    return text.strip()


def generate_linkedin_post(problem: str, solution: str, cta: str, words: int = 300, writing_tone='Professional'):
    return ask_ai(
        f'''
         You are an assistant helping to draft a post for linkedin,
         about a problem: ${problem} and proposing a solution: ${solution}, 
         at the end you should mention about call to action for: ${cta}. The post should have at least 300 words.
         Using writing tone {writing_tone}.
         The output text must has at least ${words} words.
         Use this format, replacing text in brackets with the result. 
         Do not include the brackets in the output:
         
         [One Linkedin post body]
        '''
    )


class TestGenerateLinkedInPost(unittest.TestCase):

    def setUp(self):
        # Set up OpenAI API key and model
        openai.api_key = "<API KEY>"
        openai.Model.list()

    def assertIsCoveredProblem(self, problem, text):
        result = ask_ai(f'''
            Act as a boolean function that validate text on a question with return results only True or False.
            Question: "Is covered problem for in the text".
            Problem: ${problem}.
            Text: ${text}.
        ''')
        return bool(result)

    def test_generate_linkedin_post(self):
        # Test the function with sample input values
        problem = "low employee engagement"
        solution = "introduce more team-building activities"
        cta = "join our next team-building event"
        expected_output_length = 170
        expected_writing_tone = "Professional"
        output = generate_linkedin_post(problem, solution, cta, words=expected_output_length,
                                        writing_tone=expected_writing_tone)
        actual_words = len(output.split())
        print(actual_words)
        self.assertIsCoveredProblem(problem, output)
        self.assertTrue(actual_words >= expected_output_length)
        self.assertTrue(actual_words <= expected_output_length * 1.5)


if __name__ == '__main__':
    unittest.main()
